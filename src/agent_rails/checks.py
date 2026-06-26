"""Core checks for Agent Rails."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import fnmatch
import json
from pathlib import Path
import re
from typing import Iterable


REQUIRED_DOCS = (
    "AGENTS.md",
    "AI_START_HERE.md",
    "MASTER_AI_PROJECT_OPERATING_SYSTEM_PERSONAL.md",
    "GATED_AI_PROGRESS_PROTOCOL.md",
)

GATE_FIELDS = (
    "Gate name",
    "Status",
    "Evidence produced",
    "Human review required",
    "Stop conditions",
    "Next safe action",
    "Next prompt",
)

SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".next",
    ".turbo",
}

SKIP_FILE_NAMES = {
    "agent-rails-report.md",
}

SECRET_PATTERNS = (
    ("private-key-block", re.compile(r"-----BEGIN (?:RSA |DSA |EC |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("seed-or-mnemonic-assignment", re.compile(r"\b(?:seed phrase|mnemonic|recovery phrase)\b\s*[:=]", re.IGNORECASE)),
    ("private-key-assignment", re.compile(r"\bprivate[_-]?key\b\s*[:=]\s*['\"]?[A-Za-z0-9_/\+=-]{16,}", re.IGNORECASE)),
    ("openai-api-key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("aws-access-key-id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
)

RISK_PATTERNS = (
    ("mainnet", re.compile(r"\bmainnet\b", re.IGNORECASE)),
    ("production-deploy", re.compile(r"\b(prod(?:uction)? deploy|production deployment)\b", re.IGNORECASE)),
    ("wallet-or-signer", re.compile(r"\b(wallet|signer|transaction submission|hot wallet)\b", re.IGNORECASE)),
    ("payments", re.compile(r"\b(payment|stripe|billing)\b", re.IGNORECASE)),
    ("package-release", re.compile(r"\b(npm publish|pypi upload|dist-tag|package publishing|registry state)\b", re.IGNORECASE)),
    ("credentials", re.compile(r"\b(secret|credential|api key|token)\b", re.IGNORECASE)),
    ("automation", re.compile(r"\b(automation|scheduled task|webhook)\b", re.IGNORECASE)),
)

@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    message: str
    path: str | None = None
    line: int | None = None

    @property
    def is_failure(self) -> bool:
        return self.status == "FAIL"

    @property
    def is_warning(self) -> bool:
        return self.status == "WARN"


@dataclass(frozen=True)
class AgentRailsConfig:
    risk_ignore: tuple[str, ...] = ()


def run_checks(root: Path, changed_files: Iterable[str | Path] | None = None) -> list[CheckResult]:
    root = root.resolve()
    config, config_results = load_config(root)
    scan_paths = resolve_scan_paths(root, changed_files)
    results: list[CheckResult] = []
    if scan_paths is not None:
        results.append(CheckResult("scope", "PASS", f"Changed-file mode enabled for {len(scan_paths)} existing in-root file(s)."))
    results.extend(config_results)
    results.extend(check_required_docs(root))
    results.extend(check_gate_status_sections(root, scan_paths=scan_paths))
    results.extend(scan_for_secrets(root, scan_paths=scan_paths))
    results.extend(scan_for_risk_terms(root, risk_ignore=config.risk_ignore, scan_paths=scan_paths))

    if not any(result.is_failure for result in results):
        results.append(CheckResult("summary", "PASS", "No blocking Agent Rails findings found."))

    return results


def resolve_scan_paths(root: Path, changed_files: Iterable[str | Path] | None) -> tuple[Path, ...] | None:
    if changed_files is None:
        return None

    paths: list[Path] = []
    seen: set[Path] = set()
    for raw_path in changed_files:
        path = Path(raw_path)
        candidate = path if path.is_absolute() else root / path
        try:
            resolved = candidate.resolve()
            resolved.relative_to(root)
        except (OSError, ValueError):
            continue

        if resolved.exists() and resolved.is_file() and resolved not in seen:
            paths.append(resolved)
            seen.add(resolved)

    return tuple(paths)


def load_config(root: Path) -> tuple[AgentRailsConfig, list[CheckResult]]:
    path = root / ".agent-rails.json"
    if not path.exists():
        return AgentRailsConfig(), [CheckResult("config", "PASS", "No config file found; using defaults.")]

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        return AgentRailsConfig(), [CheckResult("config", "FAIL", f"Could not read .agent-rails.json: {error}", ".agent-rails.json")]

    risk_ignore = data.get("risk_ignore", [])
    if not isinstance(risk_ignore, list) or not all(isinstance(item, str) for item in risk_ignore):
        return AgentRailsConfig(), [CheckResult("config", "FAIL", "Config key 'risk_ignore' must be a list of strings.", ".agent-rails.json")]

    return AgentRailsConfig(risk_ignore=tuple(risk_ignore)), [
        CheckResult("config", "PASS", f"Loaded .agent-rails.json with {len(risk_ignore)} risk ignore pattern(s).", ".agent-rails.json")
    ]


def check_required_docs(root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []

    for name in REQUIRED_DOCS:
        path = root / name
        if path.exists():
            results.append(CheckResult("required-docs", "PASS", f"Found {name}.", name))
        else:
            results.append(CheckResult("required-docs", "FAIL", f"Missing required rail doc: {name}.", name))

    agents_text = read_text(root / "AGENTS.md")
    if agents_text is not None:
        if "AI_START_HERE.md" not in agents_text:
            results.append(CheckResult("load-order", "WARN", "AGENTS.md should point agents to AI_START_HERE.md.", "AGENTS.md"))
        if "Current Gate Status" not in agents_text:
            results.append(CheckResult("gate-template", "WARN", "AGENTS.md should include the Current Gate Status template.", "AGENTS.md"))

    return results


def check_gate_status_sections(root: Path, *, scan_paths: tuple[Path, ...] | None = None) -> list[CheckResult]:
    results: list[CheckResult] = []
    found_section = False
    scoped = scan_paths is not None

    for path in iter_text_files(root, scan_paths=scan_paths):
        if path.suffix.lower() != ".md":
            continue

        text = read_text(path)
        if text is None:
            continue

        rel_path = relative_path(root, path)
        for section, section_line in iter_gate_sections(text):
            found_section = True
            for field in GATE_FIELDS:
                pattern = re.compile(rf"^- {re.escape(field)}:[ \t]*(.*)$", re.MULTILINE)
                match = pattern.search(section)
                if not match or not match.group(1).strip():
                    results.append(
                        CheckResult(
                            "gate-status",
                            "FAIL",
                            f"Current Gate Status is missing a value for '{field}'.",
                            rel_path,
                            section_line,
                        )
                    )

    if found_section:
        if not any(result.name == "gate-status" and result.is_failure for result in results):
            results.append(CheckResult("gate-status", "PASS", "All Current Gate Status sections are complete."))
    elif scoped:
        results.append(CheckResult("gate-status", "PASS", "No Current Gate Status sections found in changed files."))
    else:
        results.append(CheckResult("gate-status", "WARN", "No Current Gate Status sections found. Add one for substantial gated work."))

    return results


def scan_for_secrets(root: Path, *, scan_paths: tuple[Path, ...] | None = None, max_findings: int = 50) -> list[CheckResult]:
    results: list[CheckResult] = []

    for path in iter_text_files(root, scan_paths=scan_paths):
        text = read_text(path)
        if text is None:
            continue

        rel_path = relative_path(root, path)
        for name, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                results.append(
                    CheckResult(
                        "secret-scan",
                        "FAIL",
                        f"Secret-looking value matched pattern '{name}'.",
                        rel_path,
                        line_for_offset(text, match.start()),
                    )
                )
                if len(results) >= max_findings:
                    results.append(CheckResult("secret-scan", "WARN", "Secret scan stopped after maximum findings."))
                    return results

    if not results:
        results.append(CheckResult("secret-scan", "PASS", "No secret-looking values found."))

    return results


def scan_for_risk_terms(
    root: Path,
    *,
    risk_ignore: tuple[str, ...] = (),
    scan_paths: tuple[Path, ...] | None = None,
    max_findings: int = 25,
) -> list[CheckResult]:
    results: list[CheckResult] = []

    for path in iter_text_files(root, scan_paths=scan_paths):
        rel_path = relative_path(root, path)
        if matches_any(rel_path, risk_ignore):
            continue

        text = read_text(path)
        if text is None:
            continue

        for name, pattern in RISK_PATTERNS:
            match = pattern.search(text)
            if match:
                results.append(
                    CheckResult(
                        "risk-review",
                        "WARN",
                        f"Review gate may be required for risk term '{name}'.",
                        rel_path,
                        line_for_offset(text, match.start()),
                    )
                )
                if len(results) >= max_findings:
                    results.append(CheckResult("risk-review", "WARN", "Risk scan stopped after maximum findings."))
                    return results

    if not results:
        results.append(CheckResult("risk-review", "PASS", "No high-risk terms found outside configured ignored paths."))

    return results


def render_report(results: Iterable[CheckResult]) -> str:
    result_list = list(results)
    failures = [result for result in result_list if result.is_failure]
    warnings = [result for result in result_list if result.is_warning]
    passes = [result for result in result_list if result.status == "PASS"]
    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")

    lines = [
        "# Agent Rails Report",
        "",
        f"Generated: {generated}",
        "",
        "## Summary",
        "",
        f"- Failures: {len(failures)}",
        f"- Warnings: {len(warnings)}",
        f"- Passes: {len(passes)}",
        "",
    ]

    for title, items in (("Failures", failures), ("Warnings", warnings), ("Passes", passes)):
        lines.extend([f"## {title}", ""])
        if not items:
            lines.extend(["None.", ""])
            continue

        for item in items:
            location = ""
            if item.path:
                location = f" ({item.path}"
                if item.line:
                    location += f":{item.line}"
                location += ")"
            lines.append(f"- [{item.status}] {item.name}{location}: {item.message}")
        lines.append("")

    return "\n".join(lines)


def iter_text_files(root: Path, *, scan_paths: tuple[Path, ...] | None = None) -> Iterable[Path]:
    candidates = root.rglob("*") if scan_paths is None else scan_paths
    for path in candidates:
        if not path.is_file():
            continue

        if path.name in SKIP_FILE_NAMES:
            continue

        try:
            relative_parts = path.relative_to(root).parts
        except ValueError:
            relative_parts = path.parts

        if any(part in SKIP_DIR_NAMES or part.endswith(".egg-info") for part in relative_parts):
            continue

        try:
            if path.stat().st_size > 1_000_000:
                continue
        except OSError:
            continue

        yield path


def iter_gate_sections(text: str) -> Iterable[tuple[str, int]]:
    lines = text.splitlines(keepends=True)
    section_starts: list[int] = []
    in_fence = False
    fence_marker = ""

    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            continue

        if not in_fence and stripped == "## Current Gate Status":
            section_starts.append(index)

    for start in section_starts:
        end = len(lines)
        in_fence = False
        fence_marker = ""
        for index in range(start + 1, len(lines)):
            stripped = lines[index].strip()
            if stripped.startswith(("```", "~~~")):
                marker = stripped[:3]
                if not in_fence:
                    in_fence = True
                    fence_marker = marker
                elif marker == fence_marker:
                    in_fence = False
                    fence_marker = ""
                continue
            if not in_fence and lines[index].startswith("## "):
                end = index
                break

        yield "".join(lines[start:end]), start + 1


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def relative_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def line_for_heading(text: str, heading: str) -> int:
    offset = text.find(heading)
    if offset == -1:
        return 1
    return line_for_offset(text, offset)


def matches_any(path: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)
