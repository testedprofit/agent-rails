# Agent Rails

[![Agent Rails](https://github.com/testedprofit/agent-rails/actions/workflows/agent-rails.yml/badge.svg)](https://github.com/testedprofit/agent-rails/actions/workflows/agent-rails.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Portable guardrails for AI-assisted repositories.

Agent Rails gives a repo the basic rails most AI-assisted projects are missing: clear agent instructions, compact project context, a gated progress protocol, local checks, and a GitHub Action. It helps teams move quickly without losing sight of secrets, risky work, human review, or the next safe action.

## Why It Exists

AI coding agents are fast. Repos are often vague.

Most teams do not have crisp answers to:

- What is the agent allowed to do?
- What must stop until a human reviews it?
- Did this PR touch secrets, wallets, payments, releases, deploys, or production configuration?
- Is there evidence for the claimed progress?
- What is the next safe action?

Agent Rails turns those answers into markdown files humans can read and checks automation can enforce.

## What You Get

- `AGENTS.md` instructions for AI coding agents.
- `AI_START_HERE.md` for compact project context.
- `GATED_AI_PROGRESS_PROTOCOL.md` for reviewable work gates.
- `MASTER_AI_PROJECT_OPERATING_SYSTEM_PERSONAL.md` for the deeper operating model.
- A Python CLI with `init` and `check`.
- A GitHub Action that runs guardrail checks on push and pull request.
- A markdown report that is easy to attach to reviews.

## Quick Start

Run Agent Rails inside this repo:

```bash
python -m pip install -e .
python -m unittest discover
agent-rails check --strict --report agent-rails-report.md
agent-rails --version
```

Install from GitHub into another project:

```bash
python -m pip install git+https://github.com/testedprofit/agent-rails.git
agent-rails init /path/to/project
agent-rails check /path/to/project --report /path/to/project/agent-rails-report.md
```

## Example Output

```text
Agent Rails checked /path/to/project
failures=0 warnings=0
```

The markdown report includes failures, warnings, passes, file paths, and line numbers when available.

## Changed-File Mode

For pull request workflows, use changed-file mode to keep required-doc checks global while limiting gate, secret, and risk scans to files touched by the PR:

```bash
agent-rails check --strict --changed-files README.md src/example.py
```

Or read changed files from a newline-delimited file:

```bash
git diff --name-only origin/main...HEAD > changed-files.txt
agent-rails check --strict --changed-files-list changed-files.txt
```

## What It Checks

- Required operating docs are present:
  - `AGENTS.md`
  - `AI_START_HERE.md`
  - `MASTER_AI_PROJECT_OPERATING_SYSTEM_PERSONAL.md`
  - `GATED_AI_PROGRESS_PROTOCOL.md`
- Any real `## Current Gate Status` section has all required fields.
- Obvious secret-looking values are flagged before they are committed.
- High-risk terms are surfaced for review unless explicitly ignored in `.agent-rails.json`, including MainNet, payments, production deploys, wallet/signing paths, package publishing, credentials, and automation.

## Config

Use `.agent-rails.json` to ignore expected risk vocabulary in policy files, generated examples, or tests:

```json
{
  "risk_ignore": [
    "AGENTS.md",
    "src/policy/*.py",
    "tests/*.py"
  ]
}
```

## GitHub Action

This starter includes `.github/workflows/agent-rails.yml`. It installs the package, runs the checks, and uploads the markdown report as a workflow artifact.

The default workflow runs full-repo strict checks. Changed-file mode is available for teams that want PR-focused signal after they wire a changed-file list into their workflow.

For local review commands, see `docs/QA.md`.

## Project Shape

```text
.
├── AGENTS.md
├── AI_START_HERE.md
├── GATED_AI_PROGRESS_PROTOCOL.md
├── MASTER_AI_PROJECT_OPERATING_SYSTEM_PERSONAL.md
├── src/agent_rails/
├── tests/
├── docs/
├── RELEASE_NOTES.md
└── .github/workflows/agent-rails.yml
```

## Good Fit

Agent Rails is especially useful for:

- Solo builders using coding agents.
- Open-source maintainers who want clear agent rules.
- Teams adopting AI pair-programming.
- Web3, fintech, infrastructure, and automation projects where irreversible changes need review.

## Boundaries

Agent Rails is intentionally lightweight. It is not a complete secret scanner, vulnerability scanner, compliance framework, or substitute for security review. It is a practical repo rail: it catches obvious problems, makes risk visible, and nudges work back into a reviewable path. Files above 1 MB and unreadable/binary files are skipped by the current scanner.

## Project Thesis

Speed without gates creates hidden risk. Safety without direction creates churn. Gated progress gives teams useful, safe, reviewable action.
