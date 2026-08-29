from __future__ import annotations

import shutil
import tempfile
import tomllib
import unittest
from pathlib import Path

from scripts.create_training_session import babysitting_start_packet, write_state
from scripts.render_session_markdown import render_text
from scripts.validate_paper_model import cross_type_duplicates, validate_babysitting_assets
from scripts.validate_session_state import validate_state


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "papers/li_2026_ft_opt/model/paper_model.pending.toml"
SOURCE = ROOT / "papers/li_2026_ft_opt/source/Li_et_al_2026_FT_OPT_proof.pdf"
LEGACY_MODEL = ROOT / "papers/zhu_2023_srp_microscopy/model/paper_model.pending.toml"


class BabysittingTests(unittest.TestCase):
    def make_session(self, model_source: Path = MODEL, level: str = "babysitting"):
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        model_path = root / "model" / "paper_model.pending.toml"
        model_path.parent.mkdir()
        shutil.copy2(model_source, model_path)
        with model_path.open("rb") as stream:
            model = tomllib.load(stream)
        source = root / "source" / SOURCE.name
        source.parent.mkdir()
        shutil.copy2(SOURCE, source)
        state_path = root / "session.state.toml"
        write_state(state_path, model_path, model, "babysitting_test", level, 991, "unused", "unused")
        state = tomllib.loads(state_path.read_text(encoding="utf-8"))
        markdown_path = root / "session.md"
        markdown_path.write_text(render_text(state, "# Test session\n"), encoding="utf-8")
        return directory, root, model, state_path, markdown_path

    @staticmethod
    def failed(checks):
        return {check.name for check in checks if not check.passed}

    @staticmethod
    def make_active_check(text: str) -> str:
        text = text.replace('active_item_id = ""', 'active_item_id = "TERM_PHOTOTHERMAL"')
        text = text.replace('active_item_kind = ""', 'active_item_kind = "terminology"')
        text = text.replace('current_check_prompt = ""', 'current_check_prompt = "In one sentence, what converts absorption into the probe signal?"')
        text = text.replace('resume_cursor = "BABYSITTING.select_item.await_response"', 'resume_cursor = "BABYSITTING.check.TERM_PHOTOTHERMAL.await_response"')
        text = text.replace('asked_ids = ["BABYSITTING_START_PROMPT"]', 'asked_ids = ["BABYSITTING_START_PROMPT", "BABYSITTING_CHECK_TERM_PHOTOTHERMAL"]')
        text = text.replace('pending_prompt_id = "BABYSITTING_START_PROMPT"', 'pending_prompt_id = "BABYSITTING_CHECK_TERM_PHOTOTHERMAL"')
        text = text.replace('pending_prompt_text = "Which term or logical relation is unclear? Pick one."', 'pending_prompt_text = "In one sentence, what converts absorption into the probe signal?"')
        return text + '\n[[events]]\nsequence = 1\nprompt_id = "BABYSITTING_START_PROMPT"\nprompt_text = "Which term or logical relation is unclear? Pick one."\nstage = "knowledge"\nselection_policy_version = "1.2"\nhuman_response = "TERM_PHOTOTHERMAL"\n'

    def test_initialization_freezes_packet_and_assets(self):
        directory, _, model, state_path, markdown_path = self.make_session()
        self.addCleanup(directory.cleanup)
        state = tomllib.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(state["resume_cursor"], "BABYSITTING.select_item.await_response")
        self.assertEqual(state["stage_dispositions"]["idea"], "not_applicable")
        self.assertEqual(state["pending_prompt_text"], "Which term or logical relation is unclear? Pick one.")
        self.assertEqual(len(state["babysitting_terminology_nodes"]), len(model["terminology_nodes"]))
        self.assertEqual(len(state["babysitting_logical_edges"]), len(model["logical_edges"]))
        self.assertFalse(self.failed(validate_state(state_path, markdown_path)))

    def test_active_item_and_check_cursor_recover(self):
        directory, _, _, state_path, _ = self.make_session()
        self.addCleanup(directory.cleanup)
        text = self.make_active_check(state_path.read_text(encoding="utf-8"))
        state_path.write_text(text, encoding="utf-8")
        state = tomllib.loads(text)
        markdown_path = state_path.with_name("session.md")
        markdown_path.write_text(render_text(state, "# Test session\n"), encoding="utf-8")
        self.assertFalse(self.failed(validate_state(state_path, markdown_path)))

    def test_dropped_inventory_item_is_rejected(self):
        directory, _, _, state_path, _ = self.make_session()
        self.addCleanup(directory.cleanup)
        text = state_path.read_text(encoding="utf-8")
        text = text.replace('unresolved_terminology_ids = ["TERM_VIBRATIONAL_OVERTONE", ', 'unresolved_terminology_ids = [')
        state_path.write_text(text, encoding="utf-8")
        state = tomllib.loads(text)
        markdown_path = state_path.with_name("session.md")
        markdown_path.write_text(render_text(state, "# Test session\n"), encoding="utf-8")
        self.assertIn("BABYSITTING item inventories cover and partition", self.failed(validate_state(state_path, markdown_path)))

    def test_stale_or_mismatched_pending_check_is_rejected(self):
        directory, _, _, state_path, _ = self.make_session()
        self.addCleanup(directory.cleanup)
        text = self.make_active_check(state_path.read_text(encoding="utf-8"))
        text = text.replace('pending_prompt_text = "In one sentence, what converts absorption into the probe signal?"', 'pending_prompt_text = "Stale check"')
        state_path.write_text(text, encoding="utf-8")
        state = tomllib.loads(text)
        markdown_path = state_path.with_name("session.md")
        markdown_path.write_text(render_text(state, "# Test session\n"), encoding="utf-8")
        self.assertIn("BABYSITTING active check matches pending prompt", self.failed(validate_state(state_path, markdown_path)))

    def test_complete_babysitting_requires_resolved_inventory(self):
        directory, _, _, state_path, _ = self.make_session()
        self.addCleanup(directory.cleanup)
        text = state_path.read_text(encoding="utf-8")
        text = text.replace('current_stage = "knowledge"', 'current_stage = "complete"')
        text = text.replace('resume_cursor = "BABYSITTING.select_item.await_response"', 'resume_cursor = "COMPLETE.terminal"')
        text = text.replace('asked_ids = ["BABYSITTING_START_PROMPT"]', 'asked_ids = []')
        text = text.replace('pending_prompt_id = "BABYSITTING_START_PROMPT"', 'pending_prompt_id = ""')
        text = text.replace('pending_prompt_text = "Which term or logical relation is unclear? Pick one."', 'pending_prompt_text = ""')
        text = text.replace('rollout_complete = false', 'rollout_complete = true')
        text = text.replace('completed_stages = []', 'completed_stages = ["knowledge"]')
        text = text.replace('stage_dispositions = { knowledge = "in_progress", idea = "not_applicable", claims = "not_applicable", evidence = "not_applicable", independent_reading = "not_applicable", delta = "not_applicable" }', 'stage_dispositions = { knowledge = "completed", idea = "not_applicable", claims = "not_applicable", evidence = "not_applicable", independent_reading = "not_applicable", delta = "not_applicable" }')
        text = text.replace('verified_terminology_ids = []', 'verified_terminology_ids = ["TERM_VIBRATIONAL_OVERTONE", "TERM_PHOTOTHERMAL", "TERM_MIR_SWIR", "TERM_TIME_DOMAIN", "TERM_INTERFEROGRAM", "TERM_FOURIER_TRANSFORM", "TERM_BANDWIDTH_RESOLUTION", "TERM_SUPERCONTINUUM", "TERM_PUMP_PROBE", "TERM_MULTIPLEX", "TERM_POINT_SPREAD", "TERM_SPECTRAL_UNMIXING", "TERM_SPECTRAL_FLOW", "TERM_HYPERSPECTRAL"]', 1)
        text = text.replace('explained_terminology_ids = []', 'explained_terminology_ids = ["TERM_VIBRATIONAL_OVERTONE", "TERM_PHOTOTHERMAL", "TERM_MIR_SWIR", "TERM_TIME_DOMAIN", "TERM_INTERFEROGRAM", "TERM_FOURIER_TRANSFORM", "TERM_BANDWIDTH_RESOLUTION", "TERM_SUPERCONTINUUM", "TERM_PUMP_PROBE", "TERM_MULTIPLEX", "TERM_POINT_SPREAD", "TERM_SPECTRAL_UNMIXING", "TERM_SPECTRAL_FLOW", "TERM_HYPERSPECTRAL"]', 1)
        text = text.replace('unresolved_terminology_ids = ["TERM_VIBRATIONAL_OVERTONE", "TERM_PHOTOTHERMAL", "TERM_MIR_SWIR", "TERM_TIME_DOMAIN", "TERM_INTERFEROGRAM", "TERM_FOURIER_TRANSFORM", "TERM_BANDWIDTH_RESOLUTION", "TERM_SUPERCONTINUUM", "TERM_PUMP_PROBE", "TERM_MULTIPLEX", "TERM_POINT_SPREAD", "TERM_SPECTRAL_UNMIXING", "TERM_SPECTRAL_FLOW", "TERM_HYPERSPECTRAL"]', 'unresolved_terminology_ids = []')
        text = text.replace('verified_relation_ids = []', 'verified_relation_ids = ["EDGE_I1_I2", "EDGE_I2_I3", "EDGE_I3_I4", "EDGE_I4_I5", "EDGE_I4_I5_G1", "EDGE_G1_T0", "EDGE_T0_M1", "EDGE_M1_S11", "EDGE_M1_S12", "EDGE_M1_S13", "EDGE_T0_M2", "EDGE_M2_S21", "EDGE_M2_S22", "EDGE_M2_S23", "EDGE_M2_S24", "EDGE_T0_M3", "EDGE_M3_S31", "EDGE_M3_S32", "EDGE_T0_M4", "EDGE_M4_S41", "EDGE_M4_S42", "EDGE_T0_M5", "EDGE_M5_S51", "EDGE_M5_S52", "EDGE_M5_S53"]', 1)
        text = text.replace('explained_relation_ids = []', 'explained_relation_ids = ["EDGE_I1_I2", "EDGE_I2_I3", "EDGE_I3_I4", "EDGE_I4_I5", "EDGE_I4_I5_G1", "EDGE_G1_T0", "EDGE_T0_M1", "EDGE_M1_S11", "EDGE_M1_S12", "EDGE_M1_S13", "EDGE_T0_M2", "EDGE_M2_S21", "EDGE_M2_S22", "EDGE_M2_S23", "EDGE_M2_S24", "EDGE_T0_M3", "EDGE_M3_S31", "EDGE_M3_S32", "EDGE_T0_M4", "EDGE_M4_S41", "EDGE_M4_S42", "EDGE_T0_M5", "EDGE_M5_S51", "EDGE_M5_S52", "EDGE_M5_S53"]', 1)
        text = text.replace('unresolved_relation_ids = [', 'unresolved_relation_ids = [', 1)
        relation_values = '["EDGE_I1_I2", "EDGE_I2_I3", "EDGE_I3_I4", "EDGE_I4_I5", "EDGE_I4_I5_G1", "EDGE_G1_T0", "EDGE_T0_M1", "EDGE_M1_S11", "EDGE_M1_S12", "EDGE_M1_S13", "EDGE_T0_M2", "EDGE_M2_S21", "EDGE_M2_S22", "EDGE_M2_S23", "EDGE_M2_S24", "EDGE_T0_M3", "EDGE_M3_S31", "EDGE_M3_S32", "EDGE_T0_M4", "EDGE_M4_S41", "EDGE_M4_S42", "EDGE_T0_M5", "EDGE_M5_S51", "EDGE_M5_S52", "EDGE_M5_S53"]'
        text = text.replace(f'unresolved_relation_ids = {relation_values}', 'unresolved_relation_ids = []')
        state_path.write_text(text, encoding="utf-8")
        state = tomllib.loads(text)
        markdown_path = state_path.with_name("session.md")
        markdown_path.write_text(render_text(state, "# Test session\n"), encoding="utf-8")
        self.assertFalse(self.failed(validate_state(state_path, markdown_path)))

    def test_legacy_model_cannot_initialize_babysitting(self):
        with LEGACY_MODEL.open("rb") as stream:
            model = tomllib.load(stream)
        with self.assertRaisesRegex(ValueError, "BABYSITTING"):
            babysitting_start_packet(model)

    def test_missing_or_duplicate_start_packet_is_rejected(self):
        with MODEL.open("rb") as stream:
            model = tomllib.load(stream)
        original = next(packet for packet in model["transition_packets"] if packet["id"] == "BABYSITTING_START")
        model["transition_packets"] = [packet for packet in model["transition_packets"] if packet["id"] != "BABYSITTING_START"]
        checks = []
        validate_babysitting_assets(checks, model, {node["id"] for node in model["claim_nodes"]}, {node["id"] for node in model["claim_nodes"]})
        self.assertIn("Exactly one BABYSITTING_START packet exists", self.failed(checks))
        model["transition_packets"].extend([original, dict(original)])
        checks = []
        validate_babysitting_assets(checks, model, {node["id"] for node in model["claim_nodes"]}, {node["id"] for node in model["claim_nodes"]})
        self.assertIn("Exactly one BABYSITTING_START packet exists", self.failed(checks))

    def test_duplicate_term_edge_and_cross_type_ids_are_rejected(self):
        with MODEL.open("rb") as stream:
            model = tomllib.load(stream)
        model["terminology_nodes"][1]["id"] = model["terminology_nodes"][0]["id"]
        model["logical_edges"][1]["id"] = model["logical_edges"][0]["id"]
        checks = []
        validate_babysitting_assets(checks, model, {node["id"] for node in model["claim_nodes"]}, {node["id"] for node in model["claim_nodes"]})
        self.assertIn("Terminology-node IDs are present and unique", self.failed(checks))
        self.assertIn("Logical-edge IDs are present and unique", self.failed(checks))
        model["terminology_nodes"][1]["id"] = "T0"
        duplicate_ids = cross_type_duplicates({
            "claims": {node["id"] for node in model["claim_nodes"]},
            "terminology": {node["id"] for node in model["terminology_nodes"]},
            "logical_edges": {node["id"] for node in model["logical_edges"]},
        })
        self.assertIn("T0", duplicate_ids)

    def test_dangling_edge_and_partial_disclosure_are_rejected(self):
        with MODEL.open("rb") as stream:
            model = tomllib.load(stream)
        model["logical_edges"][0]["target_claim_id"] = "BAD"
        checks = []
        validate_babysitting_assets(checks, model, {node["id"] for node in model["claim_nodes"]}, {node["id"] for node in model["claim_nodes"]})
        self.assertIn("Logical-edge claim references resolve", self.failed(checks))
        with MODEL.open("rb") as stream:
            model = tomllib.load(stream)
        model["transition_packets"][-1]["terminology_ids"] = model["transition_packets"][-1]["terminology_ids"][:-1]
        checks = []
        validate_babysitting_assets(checks, model, {node["id"] for node in model["claim_nodes"]}, {node["id"] for node in model["claim_nodes"]})
        self.assertIn("BABYSITTING packet terminology disclosure is complete", self.failed(checks))

    def test_invalid_terminal_disposition_is_rejected(self):
        directory, _, _, state_path, _ = self.make_session()
        self.addCleanup(directory.cleanup)
        text = state_path.read_text(encoding="utf-8")
        text = text.replace('current_stage = "knowledge"', 'current_stage = "complete"')
        text = text.replace('resume_cursor = "BABYSITTING.select_item.await_response"', 'resume_cursor = "COMPLETE.terminal"')
        text = text.replace('asked_ids = ["BABYSITTING_START_PROMPT"]', 'asked_ids = []')
        text = text.replace('pending_prompt_id = "BABYSITTING_START_PROMPT"', 'pending_prompt_id = ""')
        text = text.replace('pending_prompt_text = "Which term or logical relation is unclear? Pick one."', 'pending_prompt_text = ""')
        text = text.replace('rollout_complete = false', 'rollout_complete = true')
        text = text.replace('completed_stages = []', 'completed_stages = ["knowledge"]')
        text = text.replace('stage_dispositions = { knowledge = "in_progress", idea = "not_applicable", claims = "not_applicable", evidence = "not_applicable", independent_reading = "not_applicable", delta = "not_applicable" }', 'stage_dispositions = { knowledge = "skipped", idea = "not_applicable", claims = "not_applicable", evidence = "not_applicable", independent_reading = "not_applicable", delta = "not_applicable" }')
        state_path.write_text(text, encoding="utf-8")
        state = tomllib.loads(text)
        markdown_path = state_path.with_name("session.md")
        markdown_path.write_text(render_text(state, "# Test session\n"), encoding="utf-8")
        self.assertIn("BABYSITTING terminal dispositions are exact", self.failed(validate_state(state_path, markdown_path)))

    def test_dangling_assets_are_rejected_by_model_validator(self):
        with MODEL.open("rb") as stream:
            model = tomllib.load(stream)
        model["terminology_nodes"][0]["related_claim_ids"] = ["BAD"]
        checks = []
        validate_babysitting_assets(checks, model, {node["id"] for node in model["claim_nodes"]}, {node["id"] for node in model["claim_nodes"]})
        self.assertIn("Terminology prerequisites and related claims resolve", self.failed(checks))


if __name__ == "__main__":
    unittest.main()
