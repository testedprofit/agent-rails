# Master AI Project Operating System

Reusable source layer for AI-assisted projects, coding agents, documentation, QA, product design, safety review, and Web3-ready architecture.

## 1. Core Thesis

```text
Speed without gates -> fragile systems and hidden risk.
Safety without direction -> audit churn and no progress.
Gated progress -> useful, safe, reviewable action.
```

## 2. Two 4D Frameworks

### AI Fluency 4Ds

| D | Meaning |
|---|---|
| Delegation | Decide what AI does, what humans do, and what is blocked. |
| Description | Explain goal, process, constraints, and expected behavior. |
| Discernment | Judge usefulness, accuracy, scope, and evidence. |
| Diligence | Own safety, disclosure, verification, and final use. |

### Prompt Construction 4Ds

| D | Meaning |
|---|---|
| Define | Persona, objective, scope, boundaries. |
| Direct | Steps, constraints, tone, stop conditions. |
| Data | Files, examples, variables, evidence. |
| Design | Output format for review/downstream use. |

## 3. Gated Progress

Every gate needs purpose, safe work, blocked work, evidence, review, exit criteria, and next gate.

Gate states:

```text
NOT STARTED / IN PROGRESS / READY FOR REVIEW / BLOCKED / COMPLETE
```

Passing tests usually means READY FOR REVIEW, not production-safe.

## 4. Anti-Churn Rule

Every warning becomes one of:

1. Completed item
2. Safe implementation item
3. Test-planning item
4. Human-review item
5. Blocked item

## 5. Anti-Bloat Rules

- One small reviewable diff.
- No unrelated refactors.
- No new dependency without reason.
- Keep mock/live data separated.
- Keep public/admin/backend/wallet/payment/execution logic separated.
- Do not combine audit, planning, and broad implementation in one prompt.

## 6. Web3 Hard Rules

- No mnemonics, private keys, seed phrases, or production `.env` in prompts/repos/frontend.
- Use separate deployer/admin/platform/hot/personal wallets.
- Use TestNet/localnet and negative tests before MainNet.
- Frontend role gates are UX only.
- Wallet, signer, transaction submission, hot wallet, risk-policy, and MainNet work need human review.
- Avoid guaranteed-profit, risk-free, passive-income, copy-trading, managed-strategy, or deposit-and-earn claims.

## 7. Default Prompt Block

```text
Task boundary: analysis-only / docs-only / test-only / implementation.
Goal: [one sentence]
Scope: [files/folders]
Out of scope: [blocked areas]
Data: [trusted files/evidence]
Output: [format]
Acceptance: [objective proof]
Diligence: [secrets/safety/review boundaries]
End with Current Gate Status.
```

