import json
import tempfile
import unittest
from pathlib import Path
import importlib.util


MODULE_PATH = Path(__file__).resolve().parents[1] / "infra" / "splunk" / "sync_splunk_objects.py"
SPEC = importlib.util.spec_from_file_location("sync_splunk_objects", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def render_context():
    return {
        "deployment_environment": "demo",
        "instance": "student-001",
        "orchestrator_webhook_url": "https://example.trycloudflare.com/webhooks/splunk/detector",
        "filesystem_utilization_threshold": "85",
        "apm_latency_threshold_ns": "1800000000",
        "apm_error_threshold": "0.05",
    }


class SyncSplunkObjectsTests(unittest.TestCase):
    def test_render_template_replaces_placeholders_recursively(self):
        rendered = MODULE.render_template(
            {
                "text": "hello {{name}}",
                "items": ["{{name}}", {"value": "{{env}}"}],
            },
            {"name": "demo", "env": "test"},
        )

        self.assertEqual(
            rendered,
            {"text": "hello demo", "items": ["demo", {"value": "test"}]},
        )

    def test_build_payloads_links_dashboards_to_group_name(self):
        payloads = MODULE.build_payloads(render_context())

        self.assertEqual(payloads["dashboard_group"]["name"], "IBOBS 2002 Demo")
        self.assertEqual(payloads["dashboards"][0]["dashboardGroupName"], "IBOBS 2002 Demo")
        self.assertIn("charts", payloads["dashboards"][0])
        self.assertGreater(len(payloads["detectors"]), 0)

    def test_detector_payload_includes_rendered_runbook_url_when_present(self):
        payloads = MODULE.build_payloads(render_context())

        latency_detector = next(
            detector for detector in payloads["detectors"] if detector["key"] == "claims_knowledge_filesystem_pressure"
        )
        self.assertEqual(
            latency_detector["rule"]["runbookUrl"],
            "https://example.trycloudflare.com/webhooks/splunk/detector",
        )

    def test_load_state_defaults_when_manifest_is_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_path = Path(temp_dir) / "missing.json"
            self.assertEqual(
                MODULE.load_state(missing_path),
                {"dashboard_group": {}, "dashboards": {}, "detectors": {}},
            )

    def test_apply_payloads_uses_put_for_known_object_ids(self):
        payloads = MODULE.build_payloads(render_context())
        state = {
            "dashboard_group": {"default": {"id": "group-1"}},
            "dashboards": {"executive_story": {"id": "dash-1"}},
            "detectors": {"claims_knowledge_filesystem_pressure": {"id": "det-1"}},
        }
        calls = []

        def fake_request_json(base_url, token, method, path, payload=None):
            calls.append((method, path, payload["name"] if payload else None))
            suffix = path.rsplit("/", 1)[-1]
            return {"id": suffix, "name": payload["name"], "url": f"https://example.com/{suffix}"}

        original = MODULE.request_json
        MODULE.request_json = fake_request_json
        try:
            _, updated_state = MODULE.apply_payloads(payloads, "https://api.example.com", "token", state)
        finally:
            MODULE.request_json = original

        self.assertEqual(calls[0][0], "PUT")
        self.assertEqual(calls[0][1], "/v2/dashboardgroup/group-1")
        self.assertEqual(calls[1][0], "PUT")
        self.assertEqual(calls[1][1], "/v2/dashboard/dash-1")
        self.assertEqual(calls[-1][0], "POST")
        self.assertIn("claims_knowledge_error_rate", updated_state["detectors"])

    def test_specs_are_valid_json(self):
        specs_dir = Path(__file__).resolve().parents[1] / "infra" / "splunk" / "specs"
        for path in specs_dir.glob("*.json"):
            with self.subTest(path=path.name):
                json.loads(path.read_text())


if __name__ == "__main__":
    unittest.main()
