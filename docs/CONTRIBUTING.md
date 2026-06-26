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

## Adding Checks

Prefer checks that produce actionable findings with file and line context. Add focused unit tests for positive cases, negative cases, config behavior, and CLI behavior when relevant.

New checks should avoid external network calls and irreversible actions. Keep the default tool dependency-free unless a new dependency has a clear maintenance and user value case.

## Adding Policy Packs

Policy packs should be optional and narrowly scoped to a risk domain such as Web3, package publishing, SaaS deployment, or data/privacy-sensitive projects.

Each policy pack should document:

- What it protects.
- What it scans.
- What it intentionally ignores.
- When human review is required.
