# Launch Checklist

Use this before announcing or publishing Agent Rails more broadly.

## Repository

- [ ] README explains the problem, install path, checks, and boundaries.
- [ ] GitHub Action is passing on `main`.
- [ ] Topics are set on the GitHub repository.
- [ ] Roadmap issues exist for the next meaningful improvements.
- [ ] Issue templates and PR template are present.

## Quality

- [ ] `python -m unittest discover` passes.
- [ ] `agent-rails check --report agent-rails-report.md` passes with zero failures.
- [ ] Generated reports are not committed.
- [ ] No real secrets, private keys, tokens, or production `.env` files are present.

## Public Positioning

- [ ] Describe Agent Rails as a lightweight guardrail utility.
- [ ] Do not claim complete security, compliance, or production readiness.
- [ ] Make clear that human review is still required for high-risk work.

## Current Gate Status
- Gate name: Launch polish
- Status: READY FOR REVIEW
- Evidence produced: README, templates, checklist, tests, and Agent Rails self-check.
- Human review required: Yes before package registry publishing or broad public announcement.
- Stop conditions: Do not publish packages or make compliance/security guarantees without review.
- Next safe action: Review the public repo page and roadmap issues.
- Next prompt: Prepare a concise launch post and first release notes.
