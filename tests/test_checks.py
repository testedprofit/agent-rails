from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import json
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agent_rails.checks import render_report, run_checks  # noqa: E402
from agent_rails.cli import check_command  # noqa: E402
from agent_rails.templates import TEMPLATES  # noqa: E402


class AgentRailsChecksTest(unittest.TestCase):
    def test_template_project_has_no_failures(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_templates(root)
            (root / "work-note.md").write_text(
                """# Work Note

## Current Gate Status
- Gate name: Verification
- Status: READY FOR REVIEW
- Evidence produced: Unit test fixture created.
- Human review required: No.
- Stop conditions: Do not publish or deploy.
- Next safe action: Review report output.
- Next prompt: Summarize findings.
""",
                encoding="utf-8",
            )

            results = run_checks(root)

        self.assertFalse([result for result in results if result.is_failure])

    def test_secret_like_values_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_templates(root)
            fake_key = "sk-" + ("a" * 32)
            (root / ".env").write_text(f"OPENAI_API_KEY={fake_key}\n", encoding="utf-8")

            results = run_checks(root)

        self.assertTrue(any(result.name == "secret-scan" and result.is_failure for result in results))

    def test_gate_status_requires_all_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_templates(root)
            (root / "bad-note.md").write_text(
                """# Bad Note

## Current Gate Status
- Gate name: Implementation
- Status:
""",
                encoding="utf-8",
            )

            results = run_checks(root)
            report = render_report(results)

        self.assertIn("Current Gate Status is missing a value for 'Status'", report)
        self.assertTrue(any(result.name == "gate-status" and result.is_failure for result in results))

    def test_prose_mentions_do_not_count_as_gate_sections(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_templates(root)
            (root / "README.md").write_text(
                "Mention `## Current Gate Status` in prose without creating a real section.\n",
                encoding="utf-8",
            )

            results = run_checks(root)

        self.assertFalse([result for result in results if result.is_failure])

    def test_readme_risk_terms_are_scanned_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_templates(root)
            (root / "README.md").write_text("Production deploy steps go here.\n", encoding="utf-8")

            results = run_checks(root)

        self.assertTrue(
            any(result.name == "risk-review" and result.path == "README.md" and result.is_warning for result in results)
        )

    def test_config_can_ignore_expected_risk_terms(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_templates(root)
            (root / ".agent-rails.json").write_text(json.dumps({"risk_ignore": ["README.md"]}), encoding="utf-8")
            (root / "README.md").write_text("Production deploy steps go here.\n", encoding="utf-8")

            results = run_checks(root)

        self.assertFalse(any(result.name == "risk-review" and result.path == "README.md" for result in results))

    def test_strict_mode_fails_when_warnings_exist(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_templates(root)
            (root / "README.md").write_text("Production deploy steps go here.\n", encoding="utf-8")

            with redirect_stdout(StringIO()):
                exit_code = check_command(root, report_path=None, strict=True)

        self.assertEqual(exit_code, 1)


def write_templates(root: Path) -> None:
    for name, content in TEMPLATES.items():
        (root / name).write_text(content.rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
