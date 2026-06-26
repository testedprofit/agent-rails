# QA Runbook

Use this checklist before opening a pull request, tagging a release, or changing guardrail behavior.

## Local Commands

```bash
python -m pip install -e .
python -m unittest discover
python -m compileall -q src tests
agent-rails check --strict --report agent-rails-report.md
agent-rails --version
git diff --check
```

## CLI Smoke Tests

```bash
agent-rails --help
agent-rails check --help
agent-rails init --help
```

## Init Smoke Test

POSIX shell:

```bash
tmpdir="$(mktemp -d)"
agent-rails init "$tmpdir"
agent-rails check "$tmpdir" --strict --report "$tmpdir/report.md"
rm -rf "$tmpdir"
```

PowerShell:

```powershell
$tmpdir = Join-Path $env:TEMP ("agent-rails-qa-" + [guid]::NewGuid().ToString("N"))
agent-rails init $tmpdir
agent-rails check $tmpdir --strict --report (Join-Path $tmpdir "report.md")
Remove-Item -LiteralPath $tmpdir -Recurse -Force
```

## Changed-File Mode Smoke Test

```bash
printf "README.md\n" > changed-files.txt
agent-rails check --changed-files-list changed-files.txt --report agent-rails-report.md
```

Use `--strict` in changed-file mode when the changed-file list is produced reliably by CI.

## Review Expectations

- Warnings should be actionable and visible in CLI output.
- Strict mode should fail on warnings.
- New behavior should have tests for positive and negative cases.
- Generated metadata such as `*.egg-info` must not affect scan results.
- Do not add external services, telemetry, package publishing, or release creation without explicit maintainer approval.

## Current Gate Status
- Gate name: QA documentation
- Status: READY FOR REVIEW
- Evidence produced: Local QA commands, smoke tests, and review expectations.
- Human review required: Yes before using as release certification.
- Stop conditions: Do not publish packages, create releases, or claim compliance coverage from this checklist alone.
- Next safe action: Run the checklist before the next release draft.
- Next prompt: Execute the QA runbook and summarize evidence.
