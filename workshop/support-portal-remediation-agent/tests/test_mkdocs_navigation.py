from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class MkdocsNavigationTest(unittest.TestCase):
    def test_splunk_validation_page_is_linked_and_actionable(self) -> None:
        mkdocs = (REPO_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        page = REPO_ROOT / "docs" / "workshop" / "splunk-validation.md"
        self.assertIn("Splunk Validation: workshop/splunk-validation.md", mkdocs)
        self.assertTrue(page.exists())

        content = page.read_text(encoding="utf-8")
        for required_text in [
            "service.instance.id",
            "deployment.environment",
            "ibobs-claims-portal",
            "claims-knowledge",
            "/var/cache/claims-knowledge",
            "system.filesystem.utilization",
            "service.request.duration.ns",
            "Gather MCP Evidence",
            "clean_claims_knowledge_cache",
            "remediation.evaluate",
            "showcase.guardrail_pre_action_check",
            "npm run simulate:traffic",
            "npm run simulate:rum",
        ]:
            with self.subTest(required_text=required_text):
                self.assertIn(required_text, content)


if __name__ == "__main__":
    unittest.main()
