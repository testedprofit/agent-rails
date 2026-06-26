# GitHub Release Notes

Tag: `v0.1.0`
Title: `Agent Rails v0.1.0`
Status: Published as a prerelease at https://github.com/testedprofit/agent-rails/releases/tag/v0.1.0

## Summary

Agent Rails v0.1.0 is the first alpha release of a lightweight Python CLI and GitHub Action for AI-assisted repositories. It installs readable project rails, validates gated progress blocks, flags obvious secret-looking values, surfaces high-risk workflow terms, and can enforce warnings in CI.

## Highlights

- Added `agent-rails init` for installing project rail docs.
- Added `agent-rails check` for local and CI guardrail checks.
- Added strict mode so warnings can fail CI.
- Added changed-file mode for PR-focused scanning.
- Added markdown report output.
- Added visible `.agent-rails.json` config for expected risk vocabulary.
- Added GitHub Actions workflow with tests, compile check, CLI version smoke test, and strict self-check.
- Added QA runbook, release notes, case study, issue templates, and PR template.

## Install

From GitHub:

```bash
python -m pip install git+https://github.com/testedprofit/agent-rails.git
```

Local development:

```bash
python -m pip install -e .
python -m unittest discover
agent-rails check --strict --report agent-rails-report.md
```

## Boundaries

Agent Rails is not a complete secret scanner, vulnerability scanner, compliance framework, or replacement for human review. It is intended as AI workflow hygiene: make obvious risk visible, keep progress reviewable, and help teams define what agents may safely do.

## Verification

```text
python -m unittest discover
python -m compileall -q src tests
agent-rails --version
agent-rails check --strict --report agent-rails-report.md
python -m pip wheel .
```

## Current Gate Status
- Gate name: Release draft
- Status: COMPLETE
- Evidence produced: Published GitHub release text for v0.1.0.
- Human review required: Yes before publishing packages or making security/compliance claims.
- Stop conditions: Do not upload packages, add telemetry, or make security/compliance claims without explicit maintainer approval.
- Next safe action: Monitor issues and feedback.
- Next prompt: Plan v0.1.1 from release feedback.
