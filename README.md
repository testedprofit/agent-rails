# Agent Rails

Portable guardrails for AI-assisted repos.

Agent Rails turns a lightweight project operating system into something a team can actually run. It gives each repo an `AGENTS.md`, compact start context, a gated progress protocol, and a CLI/GitHub Action that checks for missing rails, malformed gate status blocks, secret-looking values, and high-risk work that needs human review.

## Why this repo is worth spinning up

AI coding agents are fast, but most repos do not have a clear answer to:

- What is the agent allowed to do?
- What must stay blocked until a human reviews it?
- Did this PR touch secrets, wallets, payments, releases, deploys, or production configuration?
- Is there evidence for the claimed progress?
- What is the next safe action?

Agent Rails answers those questions with files humans can read and checks automation can enforce.

## Quick start

```bash
python -m pip install -e .
agent-rails check --report agent-rails-report.md
```

To add the rails to another project:

```bash
agent-rails init /path/to/project
agent-rails check /path/to/project --report /path/to/project/agent-rails-report.md
```

## What it checks

- Required operating docs are present:
  - `AGENTS.md`
  - `AI_START_HERE.md`
  - `MASTER_AI_PROJECT_OPERATING_SYSTEM_PERSONAL.md`
  - `GATED_AI_PROGRESS_PROTOCOL.md`
- Any `## Current Gate Status` section has all required fields.
- Secret-looking values are not committed.
- High-risk terms are surfaced for review, including MainNet, payments, production deploys, wallet/signing paths, package publishing, credentials, and automation.

## Config

Use `.agent-rails.json` to ignore expected risk vocabulary in policy files, generated examples, or tests:

```json
{
  "risk_ignore": [
    "src/policy/*.py",
    "tests/*.py"
  ]
}
```

## GitHub Action

This starter includes `.github/workflows/agent-rails.yml`. It installs the package, runs the checks, and uploads the markdown report as a workflow artifact.

## Repo shape

```text
.
├── AGENTS.md
├── AI_START_HERE.md
├── GATED_AI_PROGRESS_PROTOCOL.md
├── MASTER_AI_PROJECT_OPERATING_SYSTEM_PERSONAL.md
├── src/agent_rails/
├── tests/
├── docs/
└── .github/workflows/agent-rails.yml
```

## Project thesis

Speed without gates creates hidden risk. Safety without direction creates churn. Gated progress gives teams useful, safe, reviewable action.
