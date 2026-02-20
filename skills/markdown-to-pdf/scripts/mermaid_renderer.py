#!/usr/bin/env python3
"""
MermaidRenderer — unified Mermaid diagram rendering with AUTO fallback.

Provides a single MermaidRenderer class that supports mmdc (mermaid-cli)
and Playwright backends with SHA256-based caching, error categorization,
and strict/permissive control via MermaidRenderError.

Usage:
    from mermaid_renderer import MermaidRenderer, MermaidBackend, MermaidRenderError

    renderer = MermaidRenderer(backend=MermaidBackend.AUTO)
    result = renderer.render("graph TD; A-->B", output_path="/tmp/out.png")
    if not result.success:
        print(result.fix_suggestion)
"""

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class MermaidBackend(Enum):
    AUTO = "auto"  # mmdc -> playwright (SYNTAX_ERROR blocks fallback)
    MMDC = "mmdc"
    PLAYWRIGHT = "playwright"


class MermaidErrorCategory(Enum):
    MMDC_NOT_FOUND = "mmdc_not_found"
    BROWSER_LAUNCH_FAILED = "browser_launch_failed"
    SYNTAX_ERROR = "syntax_error"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


@dataclass
class MermaidResult:
    success: bool
    image_path: Optional[str] = None
    error_category: Optional[MermaidErrorCategory] = None
    error_message: Optional[str] = None
    backend_used: Optional[str] = None

    @property
    def fix_suggestion(self) -> Optional[str]:
        """Return actionable fix message per error category."""
        if self.error_category is None:
            return None
        suggestions = {
            MermaidErrorCategory.MMDC_NOT_FOUND: "Install mermaid-cli: npm install -g @mermaid-js/mermaid-cli",
            MermaidErrorCategory.BROWSER_LAUNCH_FAILED: "Install Playwright: pip install playwright && playwright install chromium",
            MermaidErrorCategory.SYNTAX_ERROR: "Check Mermaid syntax at https://mermaid.live/",
            MermaidErrorCategory.TIMEOUT: "Simplify the diagram or increase --timeout",
            MermaidErrorCategory.UNKNOWN: "Run with --debug-mermaid for details",
        }
        return suggestions.get(self.error_category)


class MermaidRenderError(Exception):
    """Raised by callers in strict mode when Mermaid conversion fails."""

    def __init__(self, result: MermaidResult):
        self.result = result
        cat = result.error_category.value if result.error_category else "unknown"
        super().__init__(f"Mermaid render failed [{cat}]: {result.error_message}")


class MermaidRenderer:
    """Unified Mermaid renderer with mmdc/Playwright backends and caching."""

    def __init__(
        self,
        backend: MermaidBackend = MermaidBackend.AUTO,
        output_format: str = "png",
        theme: str = "default",
        background: str = "white",
        width: int = 3200,
        height: int = 2400,
        timeout: int = 60,
        cache_dir: Optional[str] = None,
        debug: bool = False,
    ):
        self.backend = backend
        self.output_format = output_format
        self.theme = theme
        self.background = background
        self.width = width
        self.height = height
        self.timeout = timeout
        self.debug = debug
        self.cache_dir = cache_dir or tempfile.mkdtemp(prefix="mermaid_cache_")
        self._cache: dict = {}  # key -> cached file path

    def render(self, mermaid_code: str, output_path: Optional[str] = None) -> MermaidResult:
        """Render Mermaid code to an image file.

        Args:
            mermaid_code: Mermaid diagram source code.
            output_path: Destination file path. If None, a cached temp path is used.

        Returns:
            MermaidResult with success status and image path or error details.
        """
        code = mermaid_code.strip()

        # Check cache
        cache_key = self._compute_cache_key(code)
        cached = self._get_cached_path(cache_key)
        if cached and Path(cached).exists() and Path(cached).stat().st_size > 0:
            if output_path:
                shutil.copy2(cached, output_path)
                return MermaidResult(success=True, image_path=output_path, backend_used="cache")
            return MermaidResult(success=True, image_path=cached, backend_used="cache")

        # Determine effective output path
        effective_path = output_path or os.path.join(self.cache_dir, f"{cache_key}.{self.output_format}")

        # Route to backend
        if self.backend == MermaidBackend.AUTO:
            result = self._try_mmdc(code, effective_path)
            if result.success:
                self._store_cache(cache_key, effective_path)
                return result
            # SYNTAX_ERROR is a code problem — different backend won't help
            if result.error_category == MermaidErrorCategory.SYNTAX_ERROR:
                return result
            # All other failures: try Playwright
            if self.debug:
                print(
                    f"  mmdc failed ({result.error_category.value}), trying Playwright...",
                    file=sys.stderr,
                )
            result = self._try_playwright(code, effective_path)
            if result.success:
                self._store_cache(cache_key, effective_path)
            return result

        elif self.backend == MermaidBackend.MMDC:
            result = self._try_mmdc(code, effective_path)
            if result.success:
                self._store_cache(cache_key, effective_path)
            return result

        else:  # PLAYWRIGHT
            result = self._try_playwright(code, effective_path)
            if result.success:
                self._store_cache(cache_key, effective_path)
            return result

    def _compute_cache_key(self, code: str) -> str:
        """SHA256 of code + format + theme + background."""
        content = f"{code}|{self.output_format}|{self.theme}|{self.background}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

    def _get_cached_path(self, key: str) -> Optional[str]:
        return self._cache.get(key)

    def _store_cache(self, key: str, path: str) -> None:
        self._cache[key] = path

    def _try_mmdc(self, code: str, output_path: str) -> MermaidResult:
        """Try rendering with mermaid-cli (mmdc)."""
        # Write code to temp file
        tmp_input = None
        try:
            tmp_input = tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False, encoding="utf-8")
            tmp_input.write(code)
            tmp_input.close()

            cmd = ["mmdc", "-i", tmp_input.name, "-o", output_path]
            if self.output_format != "svg":
                cmd.extend(["-w", str(self.width), "-H", str(self.height)])
            cmd.extend(["-t", self.theme, "-b", self.background])

            if self.debug:
                print(f"  mmdc cmd: {' '.join(cmd)}", file=sys.stderr)

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)

            if result.returncode == 0 and Path(output_path).exists():
                return MermaidResult(success=True, image_path=output_path, backend_used="mmdc")

            # Classify error
            stderr = result.stderr or ""
            if self.debug:
                print(f"  mmdc stderr: {stderr}", file=sys.stderr)

            if "Parse error" in stderr or "error" in stderr.lower() and "syntax" in stderr.lower():
                return MermaidResult(
                    success=False,
                    error_category=MermaidErrorCategory.SYNTAX_ERROR,
                    error_message=stderr.strip()[:200],
                )
            return MermaidResult(
                success=False,
                error_category=MermaidErrorCategory.UNKNOWN,
                error_message=stderr.strip()[:200] or f"mmdc exited with code {result.returncode}",
            )

        except FileNotFoundError:
            return MermaidResult(
                success=False,
                error_category=MermaidErrorCategory.MMDC_NOT_FOUND,
                error_message="mmdc command not found. Install: npm install -g @mermaid-js/mermaid-cli",
            )
        except subprocess.TimeoutExpired:
            return MermaidResult(
                success=False,
                error_category=MermaidErrorCategory.TIMEOUT,
                error_message=f"mmdc timed out after {self.timeout}s",
            )
        except Exception as e:
            return MermaidResult(
                success=False,
                error_category=MermaidErrorCategory.UNKNOWN,
                error_message=str(e)[:200],
            )
        finally:
            if tmp_input and os.path.exists(tmp_input.name):
                try:
                    os.unlink(tmp_input.name)
                except OSError:
                    pass

    def _try_playwright(self, code: str, output_path: str) -> MermaidResult:
        """Try rendering with Playwright (CDN-dependent)."""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            return MermaidResult(
                success=False,
                error_category=MermaidErrorCategory.BROWSER_LAUNCH_FAILED,
                error_message="Playwright not installed. Install: pip install playwright && playwright install chromium",
            )

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{
                    startOnLoad: true,
                    theme: '{self.theme}',
                    themeVariables: {{
                        background: '{self.background}'
                    }}
                }});
            </script>
            <style>
                body {{
                    margin: 0;
                    padding: 20px;
                    background: {self.background};
                }}
            </style>
        </head>
        <body>
            <div class="mermaid">
{code}
            </div>
        </body>
        </html>
        """

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(
                    viewport={"width": self.width, "height": self.height},
                    device_scale_factor=2.0,
                )
                page.set_content(html_content)
                page.wait_for_timeout(2000)

                svg_element = page.query_selector(".mermaid svg")
                if not svg_element:
                    browser.close()
                    return MermaidResult(
                        success=False,
                        error_category=MermaidErrorCategory.SYNTAX_ERROR,
                        error_message="Mermaid diagram failed to render (no SVG element found). Note: Playwright backend requires CDN access (cdn.jsdelivr.net).",
                    )

                if self.output_format == "svg":
                    svg_content = svg_element.evaluate("el => el.outerHTML")
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(svg_content)
                else:
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    svg_element.screenshot(path=output_path)

                browser.close()
                return MermaidResult(success=True, image_path=output_path, backend_used="playwright")

        except Exception as e:
            err_msg = str(e)
            if "browser" in err_msg.lower() or "launch" in err_msg.lower():
                return MermaidResult(
                    success=False,
                    error_category=MermaidErrorCategory.BROWSER_LAUNCH_FAILED,
                    error_message=err_msg[:200],
                )
            return MermaidResult(
                success=False,
                error_category=MermaidErrorCategory.UNKNOWN,
                error_message=f"Playwright error: {err_msg[:200]}",
            )

    @staticmethod
    def check_mmdc_available() -> bool:
        """Check if mermaid-cli (mmdc) is installed and callable."""
        try:
            result = subprocess.run(["mmdc", "--version"], capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def cleanup_cache(self) -> None:
        """Remove the cache directory and all cached files."""
        if self.cache_dir and Path(self.cache_dir).exists():
            shutil.rmtree(self.cache_dir, ignore_errors=True)
        self._cache.clear()
