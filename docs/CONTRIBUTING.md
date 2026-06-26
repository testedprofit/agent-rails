# Contributing

Thanks for helping improve Agent Rails.

## Local Setup

```bash
python -m pip install -e .
python -m unittest discover
agent-rails check --report agent-rails-report.md
```

## Contribution Rules

- Keep changes small and reviewable.
- Do not add dependencies without a clear reason.
- Do not include real secrets, tokens, mnemonics, private keys, production `.env`, or customer data in tests or docs.
- Add tests for new checks.
- Update docs when behavior changes.
- Use a `## Current Gate Status` block for substantial changes.

## Review Checklist

- Is the behavior useful to real projects?
- Is the finding actionable?
- Is the false-positive risk acceptable?
- Does the check avoid external irreversible actions?
- Are secrets and sensitive values protected?

