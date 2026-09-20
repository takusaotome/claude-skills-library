"""Documented TypeSafe HTTP contract, strict validation and bounded retries."""

from __future__ import annotations

import json
import os
import random
import threading
import time
from urllib import error, request

from .common import ReviewError, finite_number
from .questions import check_request_budget

ENDPOINT = "https://api.typesafe.ai/v1/systemone"


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward Authorization to a redirect destination.


def validate_response(payload: dict, response: dict) -> dict:
    if not isinstance(response, dict) or not isinstance(response.get("model"), str) or not response["model"]:
        raise ReviewError("Invalid provider response: model field missing.")
    answers = response.get("answers")
    if not isinstance(answers, dict) or set(answers) != set(payload["questions"]):
        raise ReviewError("Invalid provider response: missing or unexpected answer IDs.")
    usage = response.get("usage")
    if not isinstance(usage, dict) or any(
        not isinstance(usage.get(k), int) or isinstance(usage.get(k), bool) or usage[k] < 0
        for k in ["input_tokens", "output_tokens"]
    ):
        raise ReviewError("Invalid provider response: token usage missing or malformed.")
    for key, q in payload["questions"].items():
        a = answers[key]
        if not isinstance(a, dict) or a.get("type") != q["type"]:
            raise ReviewError("Invalid provider response: answer type mismatch.")
        if q["type"] == "noul":
            if not finite_number(a.get("noul"), 0, 1):
                raise ReviewError("Invalid Noul probability.")
            continue
        if not finite_number(a.get("confidence"), 0, 1):
            raise ReviewError("Invalid confidence.")
        probs = a.get("probabilities")
        expected = set(q["criteria"]) if q["type"] == "choice" else {str(i) for i in range(len(q["criteria"]))}
        if (
            not isinstance(probs, dict)
            or set(probs) != expected
            or any(not finite_number(v, 0, 1) for v in probs.values())
        ):
            raise ReviewError("Invalid probability distribution or option set.")
        if abs(sum(probs.values()) - 1) > 0.02:
            raise ReviewError("Provider probabilities do not sum to one.")
        if q["type"] == "choice":
            if a.get("choice") not in expected:
                raise ReviewError("Unknown Choice option.")
            if probs[a["choice"]] + 0.02 < max(probs.values()):
                raise ReviewError("Choice does not match distribution.")
        else:
            if not finite_number(a.get("score"), 0, len(q["criteria"]) - 1):
                raise ReviewError("Score outside its zero-based rubric.")
            legend = a.get("legend")
            if not isinstance(legend, dict) or set(legend) != expected:
                raise ReviewError("Score legend is missing or not zero-based.")
            if any(legend[str(i)] != level for i, level in enumerate(q["criteria"])):
                raise ReviewError("Score legend does not match requested rubric.")
            # A small allowance handles normal wire rounding; never reinterpret a 0-based score as 1-based.
            expectation = sum(int(k) * v for k, v in probs.items())
            if abs(expectation - a["score"]) > 0.06:
                raise ReviewError("Score does not match its probability-weighted expectation.")
    return response


class JevClient:
    mode = "jev_live"

    def __init__(
        self,
        *,
        allow_remote: bool,
        max_requests: int = 150,
        timeout: float = 30,
        retries: int = 2,
        api_key: str | None = None,
    ):
        if not allow_remote:
            raise ReviewError("Remote sending requires explicit --allow-remote authorization.")
        self.api_key = api_key or os.environ.get("TYPESAFE_API_KEY", "")
        if not self.api_key:
            raise ReviewError("Set TYPESAFE_API_KEY in the local environment; never paste it into a prompt.")
        self.max_requests = max_requests
        self.timeout = timeout
        self.retries = retries
        self.calls = 0
        self.attempts = 0
        self.lock = threading.Lock()

    def evaluate(self, payload: dict) -> dict:
        check_request_budget(payload)
        with self.lock:
            if self.calls >= self.max_requests:
                raise ReviewError("Logical API request budget exhausted.")
            self.calls += 1
        data = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8")
        for attempt in range(self.retries + 1):
            with self.lock:
                self.attempts += 1
            retry_after = None
            req = request.Request(
                ENDPOINT,
                data=data,
                method="POST",
                headers={
                    "Authorization": "Bearer " + self.api_key,
                    "Content-Type": "application/json",
                    "User-Agent": "jev-artifact-style-review/1.0.0",
                },
            )
            try:
                opener = request.build_opener(NoRedirect())
                with opener.open(req, timeout=self.timeout) as response:
                    body = response.read(4_000_001)
                if len(body) > 4_000_000:
                    raise ReviewError("Provider response exceeded the size safety limit.")
                try:
                    parsed = json.loads(body, parse_constant=lambda x: (_ for _ in ()).throw(ValueError("non-finite")))
                except (ValueError, UnicodeError) as exc:
                    raise ReviewError("Provider returned malformed JSON.") from exc
                return validate_response(payload, parsed)
            except error.HTTPError as exc:
                # Do not log body, URL query, headers or authorization: the provider may echo private content.
                if exc.code not in {408, 429, 500, 502, 503, 504, 529}:
                    raise ReviewError(
                        f"TypeSafe HTTP {exc.code}; evaluation stopped. No pass score was produced."
                    ) from None
                raw = exc.headers.get("Retry-After", "") if exc.headers else ""
                try:
                    retry_after = min(60, max(0, float(raw)))
                except ValueError:
                    pass
            except (error.URLError, TimeoutError, OSError):
                pass
            if attempt < self.retries:
                time.sleep(retry_after if retry_after is not None else min(20, 2**attempt + random.random()))
        raise ReviewError("TypeSafe request failed after bounded retries; no passing evaluation was produced.")
