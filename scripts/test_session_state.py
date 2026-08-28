from __future__ import annotations

import re
import shutil
import tempfile
import tomllib
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from scripts.render_session_markdown import render, render_text
from scripts.validate_session_state import validate_state


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "papers/zhu_2023_srp_microscopy/sessions/2026-08-27_core_training.state.toml"
MODEL = ROOT / "papers/zhu_2023_srp_microscopy/model/paper_model.pending.toml"


class SessionStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.state_text = STATE.read_text(encoding="utf-8")

    def checks_for(self, mutate=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            model_path = root / "model" / "paper_model.pending.toml"
            model_path.parent.mkdir()
            shutil.copy2(MODEL, model_path)
            state_text = self.state_text.replace(
                'paper_model_path = "../model/paper_model.pending.toml"',
                'paper_model_path = "model/paper_model.pending.toml"',
            )
            if mutate:
                state_text = mutate(state_text)
            state_path = root / "session.state.toml"
            state_path.write_text(state_text, encoding="utf-8")
            state = tomllib.loads(state_text)
            markdown_path = root / "session.md"
            markdown_path.write_text(render_text(state, "# Test session\n"), encoding="utf-8")
            return validate_state(state_path, markdown_path)

    @staticmethod
    def failed_names(checks):
        return {check.name for check in checks if not check.passed}

    def test_renderer_sorts_legacy_event_reorder(self):
        state = tomllib.loads(self.state_text)
        source = "# Test\n\nEvent 27 — `EVIDENCE_FINISH`\n\nEvent 24 — `EVIDENCE_M3_APPLICATION_PERFORMANCE_LINK`\n"
        rendered = render_text(state, source)
        numbers = [int(match.group(1)) for match in re.finditer(r"^### Event (\d+) —", rendered, re.MULTILINE)]
        self.assertEqual(numbers, list(range(1, 29)))
        self.assertNotRegex(rendered, r"(?m)^Event \d+ —")

    def test_renderer_check_rejects_stale_projection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state_path = root / "session.state.toml"
            state_path.write_text(self.state_text, encoding="utf-8")
            markdown_path = root / "session.md"
            markdown_path.write_text("# stale\n", encoding="utf-8")
            with redirect_stdout(StringIO()):
                self.assertFalse(render(state_path, markdown_path, check=True))

    def test_bad_evidence_id_is_rejected(self):
        checks = self.checks_for(lambda text: text.replace('revealed_paper_evidence_ids = ["E1"', 'revealed_paper_evidence_ids = ["BAD", "E1"'))
        self.assertIn("Revealed paper-evidence IDs resolve", self.failed_names(checks))

    def test_bad_human_evidence_parent_is_rejected(self):
        checks = self.checks_for(
            lambda text: text.replace(
                'parent_evidence_designs = ["H-E-M3-APPLICATION-PERFORMANCE-LINK"]',
                'parent_evidence_designs = ["BAD-HUMAN-EVIDENCE"]',
                1,
            )
        )
        self.assertIn("Human targets resolve", self.failed_names(checks))

    def test_paper_evidence_drift_is_rejected(self):
        checks = self.checks_for(lambda text: text.replace('id = "E1"\ntarget_claims = ["S1.1"]\nevidence_type = "energy-deposition', 'id = "E1"\ntarget_claims = ["S1.1"]\nevidence_type = "DRIFT', 1))
        self.assertIn("Session paper-evidence designs equal frozen design fields", self.failed_names(checks))

    def test_result_detail_leak_is_rejected(self):
        checks = self.checks_for(lambda text: text.replace('id = "E1"\ntarget_claims = ["S1.1"]', 'id = "E1"\ntarget_claims = ["S1.1"]\nresult_detail = "leak"', 1))
        self.assertIn("Session paper-evidence designs contain no result details", self.failed_names(checks))

    def test_closed_parent_open_child_is_rejected(self):
        checks = self.checks_for(lambda text: text.replace('id = "H-C4.1"\nstage = "claims"\nparents = ["H-C4"]\nstatus = "closed"', 'id = "H-C4.1"\nstage = "claims"\nparents = ["H-C4"]\nstatus = "open"', 1))
        self.assertIn("Finished-stage records have explicit terminal status", self.failed_names(checks))
        self.assertIn("Closed human parents have no ambiguous open children", self.failed_names(checks))

    def test_asked_event_mismatch_is_rejected(self):
        checks = self.checks_for(lambda text: text.replace(', "INDEPENDENT_READING_COMPLETE"]', ']'))
        self.assertIn("Asked IDs match responded events and pending prompt", self.failed_names(checks))

    def test_policy_provenance_is_rejected_when_missing(self):
        checks = self.checks_for(lambda text: text.replace('sequence = 28\nprompt_id = "INDEPENDENT_READING_COMPLETE"\nprompt_text = "现在请你独立查看论文中的 evidence details；完成后告诉我。"\nstage = "independent_reading"\nselection_policy_version = "1.2"', 'sequence = 28\nprompt_id = "INDEPENDENT_READING_COMPLETE"\nprompt_text = "现在请你独立查看论文中的 evidence details；完成后告诉我。"\nstage = "independent_reading"\nselection_policy_version = ""', 1))
        self.assertIn("Every event has prompt text and policy provenance", self.failed_names(checks))

    def test_skipped_delta_terminal_state_passes(self):
        checks = self.checks_for()
        self.assertFalse(self.failed_names(checks), sorted(self.failed_names(checks)))

    def test_complete_state_requires_every_stage_disposition(self):
        checks = self.checks_for(
            lambda text: text.replace(' knowledge = "completed",', "", 1)
        )
        self.assertIn("Stage dispositions are legal", self.failed_names(checks))
        self.assertIn("Stage disposition order is coherent", self.failed_names(checks))

    def test_complete_state_rejects_in_progress_stage(self):
        checks = self.checks_for(
            lambda text: text.replace('knowledge = "completed"', 'knowledge = "in_progress"', 1)
        )
        self.assertIn("Stage disposition order is coherent", self.failed_names(checks))

    def test_terminal_flag_must_match_complete_stage(self):
        checks = self.checks_for(
            lambda text: text.replace("rollout_complete = true", "rollout_complete = false", 1)
        )
        self.assertIn("Rollout terminal flag matches current stage", self.failed_names(checks))


if __name__ == "__main__":
    unittest.main()
