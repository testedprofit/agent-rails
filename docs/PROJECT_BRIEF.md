# Project Brief

## Project

Agent Rails: portable guardrails for AI-assisted repositories.

## Goal

Create a GitHub-ready utility that helps developers and small teams keep AI-assisted work reviewable, secret-safe, and gated before high-risk changes become releases.

## Audience

- Solo builders using coding agents.
- Small teams adopting AI pair-programming.
- Web3, fintech, automation, or infrastructure projects that need extra caution around irreversible actions.
- Open-source maintainers who want a clear `AGENTS.md` plus automated checks.

## Utility

Agent Rails is useful because it converts project behavior rules into runnable checks:

- Missing project operating docs are detected.
- Gate status blocks are validated.
- Secret-looking strings are blocked.
- Risky work is surfaced for review.

## Skill Showcase

- CLI design with Python standard library.
- Static analysis and text scanning.
- GitHub Actions workflow.
- Security-minded defaults.
- Documentation architecture.
- Testable agent operating procedures.
- Web3-ready gates without requiring a blockchain dependency.

## Acceptance Criteria

- `python -m unittest discover` passes.
- `agent-rails check --report agent-rails-report.md` runs locally.
- GitHub Action can run on push and pull request.
- README explains install, init, and check workflows.
- Gated progress docs are present and coherent.

## Current Gate Status
- Gate name: Implementation
- Status: READY FOR REVIEW
- Evidence produced: Starter repo files, CLI, tests, GitHub workflow, and docs.
- Human review required: Yes before publishing to package registries or using as an official policy gate.
- Stop conditions: Do not publish, deploy, create external services, or claim complete security coverage without review.
- Next safe action: Run tests locally and inspect the generated report.
- Next prompt: Review Agent Rails and tighten any rules you want enforced in your own repos.

