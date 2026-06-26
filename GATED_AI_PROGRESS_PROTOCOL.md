# Gated AI Progress Protocol

Use this protocol when work touches meaningful code, security, deployment, releases, packages, payments, wallets, Web3, automation, credentials, or other irreversible operations.

## Gate Anatomy

Each gate defines:

- Purpose
- Safe work
- Blocked work
- Evidence required
- Human review required
- Exit criteria
- Next safe action

## Gate States

```text
NOT STARTED
IN PROGRESS
READY FOR REVIEW
BLOCKED
COMPLETE
```

Passing tests can move work to `READY FOR REVIEW`. It does not automatically mean `COMPLETE`.

## Default Gates

| Gate | Use When | Safe Work | Blocked Work |
|---|---|---|---|
| Context | Starting a task | Read required docs, classify risk, define acceptance | Making irreversible changes |
| Design | Choosing approach | Propose scope, files, tests, review path | Adding dependencies without reason |
| Implementation | Editing code/docs | Small reviewable changes, local tests | Production deploys, credentials, MainNet |
| Verification | Checking outcome | Unit tests, lint, reports, screenshots | Claiming production readiness without review |
| Release Review | Publishing or deploying | Draft notes, dry runs, evidence package | Actual publish/deploy without approval |

## Required Status Block

```text
## Current Gate Status
- Gate name:
- Status:
- Evidence produced:
- Human review required:
- Stop conditions:
- Next safe action:
- Next prompt:
```

## Stop Conditions

Stop and ask for human approval before:

- Exposing or changing secrets, credentials, private keys, mnemonics, or production `.env`.
- Changing signer logic, hot-wallet logic, transaction submission, custody paths, or wallet permissions.
- Deploying to production, MainNet, package registries, payment systems, or customer-facing infrastructure.
- Making public profit, risk-free, passive-income, managed-strategy, or copy-trading claims.
- Taking external irreversible actions.

