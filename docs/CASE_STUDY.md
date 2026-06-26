# Case Study: Agent Rails

## Problem

AI coding agents can move quickly, but many repositories do not define what the agent may do, what requires human review, or how risky work should be surfaced in CI.

Agent Rails was built to make that operating model concrete: readable markdown rails for people, and runnable checks for automation.

## What Was Built

Agent Rails includes:

- A Python CLI with `init` and `check`.
- Project rail templates for AI-assisted work.
- A GitHub Action that runs tests and strict guardrail checks.
- A markdown report with failures, warnings, passes, file paths, and line numbers.
- Changed-file mode for PR-focused scanning.
- Visible config for expected risk vocabulary.
- Unit tests covering parser behavior, strict mode, config ignores, generated metadata skips, and changed-file scanning.

## Key Technical Decisions

### Dependency-Free Core

The tool uses the Python standard library so it is easy to install, audit, and run in CI.

### Human-Readable Rails

The operating model lives in markdown files that humans can review and agents can load.

### Strict CI Option

Warnings can be treated as failures with `--strict`, making the tool useful as a real review gate rather than a passive report.

### Changed-File Mode

Changed-file mode keeps required project-doc checks global while scoping gate, secret, and risk scans to files changed in a PR.

## Current Evidence

- Public repo: https://github.com/testedprofit/agent-rails
- CI status: latest run passing.
- Tests: 11 local unit tests after changed-file mode.
- Roadmap issues: changed-file mode, PR comments, severity config, policy packs, and evidence checklists.

## Resume Framing

Designed and implemented `agent-rails`, a Python CLI and GitHub Action that enforces AI workflow guardrails across repositories; added strict CI mode, changed-file scanning, markdown reporting, repo templates, and unit tests to make AI-assisted work more reviewable.

## Limits

Agent Rails is not a complete security scanner or compliance framework. Its value is workflow hygiene: making obvious risk visible and pushing work toward reviewable gates.

## Next Steps

- Add PR comment summaries.
- Add configurable severities and ignore rules for all check families.
- Create optional policy packs for high-risk repo types.
- Add measured adoption or pilot results before making impact claims.

## Current Gate Status
- Gate name: Case study
- Status: READY FOR REVIEW
- Evidence produced: Current project summary, design decisions, evidence, limits, and resume framing.
- Human review required: Yes before using as public launch copy or formal resume language.
- Stop conditions: Do not add unverified adoption numbers or publish package/release artifacts without approval.
- Next safe action: Review wording and replace qualitative impact with measured results when available.
- Next prompt: Tailor the case study into resume bullets for a senior software engineer role.
