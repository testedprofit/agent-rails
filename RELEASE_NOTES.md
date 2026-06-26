# Release Notes

## v0.1.0 - Released 2026-06-26

Initial public baseline for Agent Rails.

### Highlights

- Added `agent-rails init` to install project rail docs into another repository.
- Added `agent-rails check` to validate required docs, gate status blocks, obvious secret-looking values, and high-risk workflow terms.
- Added strict mode so warnings can fail CI.
- Added changed-file mode through `--changed-files` and `--changed-files-list`.
- Changed-file mode now warns when no provided files resolve inside the project.
- Added GitHub Actions workflow with tests and strict guardrail checks.
- Added visible `.agent-rails.json` config for expected risk vocabulary.
- Added unit tests for parser behavior, strict mode, generated metadata skips, initialized-project behavior, and changed-file scanning.

### Not Included

- No PyPI package has been published.
- No telemetry, external service, or marketplace listing is included.

### Verification

```text
python -m unittest discover
agent-rails check --strict --report agent-rails-report.md
```

## Current Gate Status
- Gate name: Release notes
- Status: COMPLETE
- Evidence produced: Published GitHub release `v0.1.0`, local tests, strict self-check, and successful CI.
- Human review required: Yes before publishing to PyPI or claiming production security/compliance coverage.
- Stop conditions: Do not publish packages, add telemetry, or make security/compliance claims without review.
- Next safe action: Monitor issues and feedback from the v0.1.0 release.
- Next prompt: Plan v0.1.1 based on reviewer feedback.
