# Release Notes

## v0.1.0 - Draft

Initial public baseline for Agent Rails.

### Highlights

- Added `agent-rails init` to install project rail docs into another repository.
- Added `agent-rails check` to validate required docs, gate status blocks, obvious secret-looking values, and high-risk workflow terms.
- Added strict mode so warnings can fail CI.
- Added changed-file mode through `--changed-files` and `--changed-files-list`.
- Added GitHub Actions workflow with tests and strict guardrail checks.
- Added visible `.agent-rails.json` config for expected risk vocabulary.
- Added unit tests for parser behavior, strict mode, generated metadata skips, and changed-file scanning.

### Not Included

- No PyPI package has been published.
- No GitHub release has been created.
- No telemetry, external service, or marketplace listing is included.

### Verification

```text
python -m unittest discover
agent-rails check --strict --report agent-rails-report.md
```

## Current Gate Status
- Gate name: Release notes
- Status: READY FOR REVIEW
- Evidence produced: Draft v0.1.0 notes, local tests, and strict self-check.
- Human review required: Yes before creating a GitHub release or publishing to PyPI.
- Stop conditions: Do not publish packages, create releases, or claim production security coverage without review.
- Next safe action: Review notes and decide whether to tag v0.1.0.
- Next prompt: Prepare a reviewed v0.1.0 GitHub release draft.
