# Question Strategy

Ask only the missing, decision-shaping questions. Do not turn bootstrap into a full interview.

## 1. Question Ordering

Ask in this order:

1. project purpose and success criteria
2. owner / team / current phase
3. highest-risk technical areas
4. commands or environments that cannot be inferred
5. install profile preference
6. overwrite vs merge preference for existing files

## 2. Batch Size

Ask 2–4 questions per round.
More than 4 usually slows the user down.
If a single answer clearly resolves several placeholders, ask that first.

## 3. Prefer Confirmation

Good:
- “I found `pytest`, `ruff`, and `mypy` in the repo. Should I use those as the standard test/lint/typecheck commands?”

Less good:
- “What are your standard commands?”

Good:
- “The repo appears to use `src/` and `tests/`. Is that the correct main source and test layout?”

## 4. Preserve Uncertainty Honestly

If the user does not know:
- write `TBD`
- continue scaffolding
- list the unresolved field in the final summary

## 5. High-Leverage Confirmation Prompts

Use prompts like:
- “What is the one-sentence purpose of this project?”
- “Which areas would hurt most if they broke in production?”
- “Do you want the lightest install, the default install, or the full install with local slash command?”
- “If a kickoff doc already exists, should I merge carefully or replace the template sections?”

## 6. Capture Rule

After each answer:
- update the bootstrap input sheet
- burn down affected placeholders immediately
- avoid asking the same question twice in different wording
