from __future__ import annotations

import argparse
import hashlib
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

try:
    from .render_session_markdown import default_markdown_path, render_text
except ImportError:
    from render_session_markdown import default_markdown_path, render_text


@dataclass
class Check:
    name: str
    passed: bool
    detail: str


STAGE_ORDER = ["knowledge", "idea", "claims", "evidence", "independent_reading", "delta"]
ALLOWED_STAGES = set(STAGE_ORDER) | {"complete"}
ALLOWED_DISPOSITIONS = {"completed", "skipped", "not_applicable", "in_progress"}
TERMINAL_DISPOSITIONS = {"completed", "skipped", "not_applicable"}
AMBIGUOUS_STATUSES = {"open", "active", "human_designed"}
PREFILLED_PACKET_FIELDS = (
    "id",
    "target_stage",
    "eligible_levels",
    "reveal_claim_ids",
    "reveal_evidence_ids",
    "source_node_ids",
    "dynamic_slots",
    "locale",
    "content",
    "prompt_id",
    "prompt_text",
)
BABYSITTING_PACKET_FIELDS = PREFILLED_PACKET_FIELDS + (
    "display_claim_ids",
    "terminology_ids",
    "logical_edge_ids",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _ids(records: list[dict]) -> list[str]:
    return [record.get("id", "") for record in records]


def _target_values(record: dict, *keys: str) -> list[str]:
    values: list[str] = []
    for key in keys:
        value = record.get(key, [])
        if isinstance(value, str):
            values.append(value)
        elif isinstance(value, list):
            values.extend(str(item) for item in value)
    return values


def _check_record_ids(checks: list[Check], state: dict) -> tuple[dict[str, set[str]], set[str]]:
    collections = {
        "human nodes": state.get("human_nodes", []),
        "human evidence designs": state.get("human_evidence_designs", []),
        "human control designs": state.get("human_control_designs", []),
        "human application metadata": state.get("human_application_metadata", []),
        "human evidence candidates": state.get("human_evidence_candidates", []),
    }
    by_collection: dict[str, set[str]] = {}
    all_ids: list[str] = []
    for name, records in collections.items():
        values = _ids(records)
        duplicates = sorted({item for item in values if values.count(item) > 1 or not item})
        checks.append(Check(f"{name} IDs are unique", not duplicates, f"duplicates={duplicates}"))
        by_collection[name] = set(values)
        all_ids.extend(values)
    duplicates = sorted({item for item in all_ids if all_ids.count(item) > 1 or not item})
    checks.append(Check("Human record IDs are unique across collections", not duplicates, f"duplicates={duplicates}"))
    return by_collection, set(all_ids)


def _status_checks(checks: list[Check], state: dict, completed_stages: list[str]) -> None:
    records = []
    for key in ("human_nodes", "human_evidence_designs", "human_control_designs", "human_application_metadata", "human_evidence_candidates"):
        records.extend(state.get(key, []))
    ambiguous_in_finished = sorted(
        record.get("id", "")
        for record in records
        if record.get("stage") in completed_stages and record.get("status") in AMBIGUOUS_STATUSES
    )
    checks.append(Check("Finished-stage records have explicit terminal status", not ambiguous_in_finished, f"ambiguous={ambiguous_in_finished}"))

    human_nodes = {record.get("id"): record for record in state.get("human_nodes", [])}
    child_map: dict[str, list[dict]] = {}
    for child in state.get("human_nodes", []):
        for parent in child.get("parents", []):
            child_map.setdefault(parent, []).append(child)
    invalid_closed_children = sorted(
        parent_id
        for parent_id, children in child_map.items()
        if human_nodes.get(parent_id, {}).get("status") == "closed"
        and any(child.get("status") in AMBIGUOUS_STATUSES for child in children)
    )
    checks.append(Check("Closed human parents have no ambiguous open children", not invalid_closed_children, f"parents={invalid_closed_children}"))


def _paper_evidence_checks(checks: list[Check], state: dict, model: dict, model_claim_ids: set[str]) -> None:
    model_evidence = {node.get("id"): node for node in model.get("evidence_nodes", [])}
    revealed = state.get("revealed_paper_evidence_ids", [])
    invalid_revealed = sorted(set(revealed) - set(model_evidence))
    checks.append(Check("Revealed paper-evidence IDs resolve", not invalid_revealed, f"missing={invalid_revealed}"))

    session_designs = state.get("paper_evidence_designs", [])
    session_by_id = {node.get("id"): node for node in session_designs}
    expected_ids = set(model_evidence)
    design_ids_ok = set(session_by_id) == expected_ids and len(session_designs) == len(expected_ids)
    checks.append(Check("Session paper-evidence design IDs match model", design_ids_ok, f"missing={sorted(expected_ids - set(session_by_id))}, extra={sorted(set(session_by_id) - expected_ids)}"))
    design_fields = ("target_claims", "evidence_type", "control_roles", "source_anchors")
    drift: list[str] = []
    leaks: list[str] = []
    for evidence_id, expected in model_evidence.items():
        actual = session_by_id.get(evidence_id, {})
        if any(key in actual for key in ("result_detail", "result_details", "result")):
            leaks.append(evidence_id)
        if {key: actual.get(key) for key in design_fields} != {key: expected.get(key) for key in design_fields}:
            drift.append(evidence_id)
        invalid_targets = sorted(set(_target_values(actual, "target_claims")) - model_claim_ids)
        if invalid_targets:
            drift.append(f"{evidence_id}:targets={invalid_targets}")
    checks.append(Check("Session paper-evidence designs equal frozen design fields", not drift, f"drift={drift}"))
    checks.append(Check("Session paper-evidence designs contain no result details", not leaks, f"leaks={leaks}"))


def _transition_packet_checks(checks: list[Check], state: dict, model: dict) -> None:
    expected_packets = model.get("transition_packets", [])
    actual_packets = state.get("prefilled_transition_packets", [])
    if not expected_packets:
        checks.append(
            Check(
                "Session transition packets (legacy model)",
                not actual_packets,
                f"unexpected={len(actual_packets)}",
            )
        )
        return

    def fields_for(packet: dict) -> tuple[str, ...]:
        return BABYSITTING_PACKET_FIELDS if packet.get("id") == "BABYSITTING_START" else PREFILLED_PACKET_FIELDS

    expected = [
        {key: packet.get(key) for key in fields_for(packet)}
        for packet in expected_packets
    ]
    actual = [
        {key: packet.get(key) for key in fields_for(packet)}
        for packet in actual_packets
    ]
    schema_drift = [
        packet.get("id", "")
        for packet in actual_packets
        if set(packet) != set(fields_for(packet))
    ]
    checks.append(Check("Session transition-packet schemas are frozen", not schema_drift, f"drift={schema_drift}"))
    checks.append(
        Check(
            "Session transition packets equal pinned model",
            actual == expected,
            f"expected_ids={[packet.get('id') for packet in expected_packets]}, actual_ids={[packet.get('id') for packet in actual_packets]}",
        )
    )
    leaks = [
        packet.get("id", "")
        for packet in actual_packets
        if any(key in packet for key in ("result_detail", "result_details", "result"))
    ]
    checks.append(Check("Session transition packets contain no result details", not leaks, f"leaks={leaks}"))


def _babysitting_checks(checks: list[Check], state: dict, model: dict) -> None:
    """Validate resumable BABYSITTING state and its frozen reusable assets."""
    packets = [
        packet for packet in model.get("transition_packets", [])
        if packet.get("id") == "BABYSITTING_START"
    ]
    if not state.get("babysitting_supported", model.get("babysitting_supported", False)):
        checks.append(Check("BABYSITTING model support is declared", False, "state/model does not declare support"))
    if len(packets) != 1:
        checks.append(Check("BABYSITTING_START packet is available for session", False, f"count={len(packets)}"))
        return
    packet = packets[0]
    state_terms = state.get("babysitting_terminology_nodes", [])
    state_edges = state.get("babysitting_logical_edges", [])
    model_terms = model.get("terminology_nodes", [])
    model_edges = model.get("logical_edges", [])
    term_fields = ("id", "term", "aliases", "definition", "prerequisites", "related_claim_ids", "source_anchors")
    edge_fields = ("id", "source_claim_ids", "target_claim_id", "relation", "explanation", "source_anchors")
    term_by_id = {item.get("id"): item for item in model_terms}
    edge_by_id = {item.get("id"): item for item in model_edges}
    expected_term_ids = packet.get("terminology_ids", [])
    expected_edge_ids = packet.get("logical_edge_ids", [])
    expected_terms = [{key: term_by_id[item_id].get(key) for key in term_fields} for item_id in expected_term_ids if item_id in term_by_id]
    actual_terms = [{key: item.get(key) for key in term_fields} for item in state_terms]
    expected_edges = [{key: edge_by_id[item_id].get(key) for key in edge_fields} for item_id in expected_edge_ids if item_id in edge_by_id]
    actual_edges = [{key: item.get(key) for key in edge_fields} for item in state_edges]
    checks.append(Check("Session BABYSITTING terminology assets are frozen", actual_terms == expected_terms, f"expected={len(expected_terms)}, actual={len(actual_terms)}"))
    checks.append(Check("Session BABYSITTING logical-edge assets are frozen", actual_edges == expected_edges, f"expected={len(expected_edges)}, actual={len(actual_edges)}"))

    session_packet = next((item for item in state.get("prefilled_transition_packets", []) if item.get("id") == "BABYSITTING_START"), None)
    packet_keys = set(BABYSITTING_PACKET_FIELDS)
    packet_match = session_packet is not None and {key: session_packet.get(key) for key in BABYSITTING_PACKET_FIELDS} == {key: packet.get(key) for key in BABYSITTING_PACKET_FIELDS}
    checks.append(Check("Session BABYSITTING disclosure packet is frozen", packet_match, f"packet_present={session_packet is not None}"))
    term_ids = set(expected_term_ids)
    edge_ids = set(expected_edge_ids)
    claim_ids = {item.get("id") for item in model.get("claim_nodes", [])}
    checks.append(Check("Session BABYSITTING display claim list is exact", state.get("babysitting_display_claim_ids", []) == packet.get("display_claim_ids", []), "display claims equal packet"))
    checks.append(Check("Session BABYSITTING display terminology list is exact", state.get("babysitting_display_terminology_ids", []) == expected_term_ids, "display terminology equal packet"))
    checks.append(Check("Session BABYSITTING display logical-edge list is exact", state.get("babysitting_display_logical_edge_ids", []) == expected_edge_ids, "display edges equal packet"))
    checks.append(Check("Session BABYSITTING display references resolve", set(state.get("babysitting_display_claim_ids", [])) <= claim_ids and set(state.get("babysitting_display_terminology_ids", [])) <= term_ids and set(state.get("babysitting_display_logical_edge_ids", [])) <= edge_ids, "display references checked"))
    checks.append(Check("BABYSITTING disclosure contains no evidence IDs", packet.get("reveal_evidence_ids") == [] and state.get("revealed_paper_evidence_ids", []) == [], f"packet={packet.get('reveal_evidence_ids')}, state={state.get('revealed_paper_evidence_ids')}"))

    all_term_ids = set(packet.get("terminology_ids", []))
    all_edge_ids = set(packet.get("logical_edge_ids", []))
    explained_terms = set(state.get("explained_terminology_ids", []))
    explained_edges = set(state.get("explained_relation_ids", []))
    verified_terms = set(state.get("verified_terminology_ids", []))
    verified_edges = set(state.get("verified_relation_ids", []))
    unresolved_terms = set(state.get("unresolved_terminology_ids", []))
    unresolved_edges = set(state.get("unresolved_relation_ids", []))
    inventory_ok = (
        (verified_terms | unresolved_terms) == all_term_ids
        and (verified_edges | unresolved_edges) == all_edge_ids
        and not (verified_terms & unresolved_terms)
        and not (verified_edges & unresolved_edges)
        and explained_terms <= all_term_ids
        and explained_edges <= all_edge_ids
    )
    checks.append(Check("BABYSITTING item inventories cover and partition", inventory_ok, f"terms={sorted(all_term_ids)}, edges={sorted(all_edge_ids)}"))
    active_id = state.get("active_item_id", "")
    active_kind = state.get("active_item_kind", "")
    valid_active = not active_id or (active_kind == "terminology" and active_id in all_term_ids) or (active_kind == "relation" and active_id in all_edge_ids)
    checks.append(Check("BABYSITTING active item and kind resolve", valid_active, f"id={active_id}, kind={active_kind}"))
    if active_id:
        active_unresolved = (active_kind == "terminology" and active_id in unresolved_terms) or (active_kind == "relation" and active_id in unresolved_edges)
        expected_cursor = f"BABYSITTING.check.{active_id}.await_response"
        checks.append(Check("BABYSITTING active item remains unresolved", active_unresolved, f"id={active_id}, kind={active_kind}"))
        checks.append(Check("BABYSITTING active item has an exact check cursor", bool(state.get("pending_prompt_id")) and state.get("resume_cursor") == expected_cursor, f"expected={expected_cursor}, actual={state.get('resume_cursor')}"))
        checks.append(Check("BABYSITTING active check matches pending prompt", bool(state.get("current_check_prompt")) and state.get("current_check_prompt") == state.get("pending_prompt_text"), "current_check_prompt must equal pending_prompt_text"))
    elif state.get("current_stage") == "complete":
        checks.append(Check("BABYSITTING terminal cursor is explicit", state.get("resume_cursor") == "COMPLETE.terminal", str(state.get("resume_cursor"))))
    else:
        checks.append(Check("BABYSITTING empty active item has empty kind", not active_kind, f"kind={active_kind}"))
        checks.append(Check("BABYSITTING selection cursor is explicit", state.get("resume_cursor") == "BABYSITTING.select_item.await_response", str(state.get("resume_cursor"))))
    checks.append(Check("BABYSITTING verified items are explained", verified_terms <= explained_terms and verified_edges <= explained_edges, "verified subset of explained"))
    if state.get("current_stage") == "complete":
        checks.append(Check("BABYSITTING terminal inventory is resolved", not unresolved_terms and not unresolved_edges and verified_terms == all_term_ids and verified_edges == all_edge_ids, f"unresolved_terms={sorted(unresolved_terms)}, unresolved_edges={sorted(unresolved_edges)}"))
        terminal_dispositions = {
            "knowledge": "completed",
            "idea": "not_applicable",
            "claims": "not_applicable",
            "evidence": "not_applicable",
            "independent_reading": "not_applicable",
            "delta": "not_applicable",
        }
        checks.append(Check("BABYSITTING terminal dispositions are exact", state.get("stage_dispositions") == terminal_dispositions and state.get("completed_stages") == ["knowledge"], f"dispositions={state.get('stage_dispositions')}, completed={state.get('completed_stages')}"))
        checks.append(Check("BABYSITTING terminal active item is cleared", not state.get("active_item_id") and not state.get("active_item_kind") and not state.get("current_check_prompt"), f"active={state.get('active_item_id')}, check={bool(state.get('current_check_prompt'))}"))


def _event_checks(checks: list[Check], state: dict, model: dict) -> None:
    events = state.get("events", [])
    sequences = [event.get("sequence") for event in events]
    checks.append(Check("Event sequence is contiguous", sequences == list(range(1, len(events) + 1)), f"events={len(events)}"))
    event_ids = [event.get("prompt_id") for event in events]
    checks.append(Check("Event prompt IDs are unique", len(event_ids) == len(set(event_ids)) and all(event_ids), f"duplicates={sorted({item for item in event_ids if event_ids.count(item) > 1})}"))
    missing_fields = [event.get("sequence") for event in events if not event.get("prompt_text") or not event.get("selection_policy_version")]
    checks.append(Check("Every event has prompt text and policy provenance", not missing_fields, f"missing={missing_fields}"))
    policies = [event.get("selection_policy_version") for event in events]
    checks.append(Check("Event policy provenance is well-formed", all(isinstance(value, str) and value for value in policies), f"policies={sorted(set(policies))}"))

    asked_ids = state.get("asked_ids", [])
    terminal = state.get("current_stage") == "complete" or state.get("rollout_complete") is True
    pending_id = state.get("pending_prompt_id", "")
    expected_asked = event_ids if terminal else event_ids + [pending_id]
    checks.append(Check("Asked IDs match responded events and pending prompt", asked_ids == expected_asked and len(asked_ids) == len(set(asked_ids)), f"expected={expected_asked}, actual={asked_ids}"))
    checks.append(Check("Terminal state has no pending prompt", not terminal or (not pending_id and not state.get("pending_prompt_text")), f"pending_id={pending_id}"))
    checks.append(Check("Nonterminal state has one unasked pending prompt", terminal or (bool(pending_id) and pending_id not in event_ids and bool(state.get("pending_prompt_text"))), f"pending_id={pending_id}"))
    checks.append(Check("Selection policy provenance is present on every event", all(event.get("selection_policy_version") for event in events), f"model_current={model.get('selection_policy_version')}"))


def _markdown_check(checks: list[Check], state: dict, markdown_path: Path | None) -> None:
    if markdown_path is None or not markdown_path.exists():
        checks.append(Check("Markdown renderer parity", True, "skipped: Markdown path not supplied or missing"))
        return
    try:
        actual = markdown_path.read_text(encoding="utf-8")
        expected = render_text(state, actual)
        checks.append(Check("Markdown renderer parity", actual == expected, str(markdown_path)))
        headings = [int(match.group(1)) for match in re.finditer(r"(?m)^### Event (\d+) —", actual)]
        expected_headings = [event["sequence"] for event in state.get("events", [])]
        checks.append(Check("Markdown event chronology matches state", headings == expected_headings, f"headings={headings}"))
    except Exception as exc:
        checks.append(Check("Markdown renderer parity", False, str(exc)))


def validate_state(state_path: Path, markdown_path: Path | None = None) -> list[Check]:
    checks: list[Check] = []
    try:
        with state_path.open("rb") as stream:
            state = tomllib.load(stream)
        checks.append(Check("Session TOML parses", True, "tomllib loaded the state"))
    except Exception as exc:
        return [Check("Session TOML parses", False, str(exc))]

    model_path = (state_path.parent / state.get("paper_model_path", "")).resolve()
    exists = model_path.is_file()
    checks.append(Check("Pinned paper model exists", exists, str(model_path)))
    model: dict = {}
    if exists:
        with model_path.open("rb") as stream:
            model = tomllib.load(stream)
    expected_hash = str(state.get("paper_model_sha256", "")).upper()
    actual_hash = sha256(model_path) if exists else ""
    checks.append(Check("Pinned paper-model SHA-256 matches", bool(re.fullmatch(r"[0-9A-F]{64}", expected_hash)) and actual_hash == expected_hash, f"expected={expected_hash}, actual={actual_hash}"))
    checks.append(Check("Paper-model version matches", state.get("paper_model_version") == model.get("model_version"), f"state={state.get('paper_model_version')}, model={model.get('model_version')}"))
    checks.append(Check("Selection-policy version matches", state.get("selection_policy_version") == model.get("selection_policy_version"), f"state={state.get('selection_policy_version')}, model={model.get('selection_policy_version')}"))
    checks.append(Check("Main-source hash matches model", state.get("main_source_sha256") == model.get("source_sha256"), f"state={state.get('main_source_sha256')}, model={model.get('source_sha256')}"))
    checks.append(Check("Supplement hash matches model", state.get("supplement_sha256") == model.get("supplement_sha256"), f"state={state.get('supplement_sha256')}, model={model.get('supplement_sha256')}"))

    current_stage = state.get("current_stage")
    checks.append(Check("Current stage is valid", current_stage in ALLOWED_STAGES, str(current_stage)))
    dispositions = state.get("stage_dispositions", {})
    disposition_ok = (
        isinstance(dispositions, dict)
        and set(dispositions) == set(STAGE_ORDER)
        and all(value in ALLOWED_DISPOSITIONS for value in dispositions.values())
    )
    checks.append(Check("Stage dispositions are legal", disposition_ok, str(dispositions)))
    completed_stages = state.get("completed_stages", [])
    expected_completed = [stage for stage in STAGE_ORDER if dispositions.get(stage) == "completed"]
    checks.append(Check("Completed stages agree with dispositions", completed_stages == expected_completed, f"completed={completed_stages}, expected={expected_completed}"))
    babysitting = state.get("level") == "babysitting"
    if babysitting and current_stage == "knowledge":
        order_ok = (
            disposition_ok
            and dispositions.get("knowledge") == "in_progress"
            and all(dispositions.get(stage) == "not_applicable" for stage in STAGE_ORDER[1:])
        )
    elif current_stage == "complete":
        order_ok = disposition_ok and all(
            dispositions.get(stage) in TERMINAL_DISPOSITIONS for stage in STAGE_ORDER
        )
    elif current_stage in STAGE_ORDER:
        current_index = STAGE_ORDER.index(current_stage)
        order_ok = (
            disposition_ok
            and dispositions.get(current_stage) == "in_progress"
            and all(
                dispositions.get(stage) in TERMINAL_DISPOSITIONS
                for stage in STAGE_ORDER[:current_index]
            )
            and all(
                dispositions.get(stage) == "in_progress"
                for stage in STAGE_ORDER[current_index + 1 :]
            )
        )
    else:
        order_ok = False
    checks.append(Check("Stage disposition order is coherent", order_ok, f"current={current_stage}"))
    checks.append(
        Check(
            "Rollout terminal flag matches current stage",
            bool(state.get("rollout_complete")) == (current_stage == "complete"),
            f"current={current_stage}, rollout_complete={state.get('rollout_complete')}",
        )
    )
    checks.append(Check("Selection seed is persisted", isinstance(state.get("selection_seed"), int) and state.get("selection_seed") > 0, str(state.get("selection_seed"))))

    model_claim_ids = {node.get("id") for node in model.get("claim_nodes", [])}
    revealed_claims = state.get("revealed_paper_claim_ids", [])
    invalid_claims = sorted(set(revealed_claims) - model_claim_ids)
    checks.append(Check("Revealed paper-claim IDs resolve", not invalid_claims, f"missing={invalid_claims}"))
    _, human_ids = _check_record_ids(checks, state)
    allowed_parent_ids = human_ids | set(revealed_claims)
    unresolved_parents = sorted({parent for node in state.get("human_nodes", []) for parent in node.get("parents", []) if parent not in allowed_parent_ids})
    checks.append(Check("Human-node parents resolve", not unresolved_parents, f"missing={unresolved_parents}"))

    target_errors: list[str] = []
    for key in ("human_evidence_designs", "human_control_designs"):
        for record in state.get(key, []):
            target_errors.extend(f"{record.get('id')}:{target}" for target in _target_values(record, "target_paper_claims") if target not in model_claim_ids)
    for key in ("human_evidence_candidates", "human_application_metadata"):
        for record in state.get(key, []):
            target_errors.extend(f"{record.get('id')}:{target}" for target in _target_values(record, "target_claims", "parent_claims") if target not in human_ids and target not in model_claim_ids)
    design_ids = {record.get("id") for record in state.get("human_evidence_designs", [])}
    for key in ("human_evidence_designs", "human_control_designs"):
        for record in state.get(key, []):
            target_errors.extend(
                f"{record.get('id')}:{target}"
                for target in _target_values(
                    record, "target_evidence_designs", "parent_evidence_designs"
                )
                if target not in design_ids
            )
    checks.append(Check("Human targets resolve", not target_errors, f"missing={target_errors}"))
    _paper_evidence_checks(checks, state, model, model_claim_ids)
    _transition_packet_checks(checks, state, model)
    if babysitting:
        _babysitting_checks(checks, state, model)
    finished_stages = [
        stage for stage in STAGE_ORDER if dispositions.get(stage) in TERMINAL_DISPOSITIONS
    ]
    _status_checks(checks, state, finished_stages)
    _event_checks(checks, state, model)
    if current_stage == "complete":
        checks.append(Check("Terminal cursor is explicit", state.get("resume_cursor") == "COMPLETE.terminal", str(state.get("resume_cursor"))))
    _markdown_check(checks, state, markdown_path)
    return checks


def report_text(state_path: Path, checks: list[Check]) -> str:
    passed = sum(check.passed for check in checks)
    lines = ["# Session-State Recovery Audit", "", f"- **State:** `{state_path.name}`", f"- **Overall:** {'PASS' if passed == len(checks) else 'FAIL'}", f"- **Checks passed:** {passed}/{len(checks)}", "", "| Check | Result | Detail |", "|---|---|---|"]
    for check in checks:
        lines.append(f"| {check.name} | {'PASS' if check.passed else 'FAIL'} | {check.detail.replace('|', '\\|').replace(chr(10), ' ')} |")
    lines.extend(["", "The audit covers model identity, stage disposition, event provenance/order, graph and evidence consistency, terminal recovery semantics, and deterministic Markdown parity.", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a paper-harness session state.")
    parser.add_argument("state", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--markdown", type=Path)
    args = parser.parse_args()
    state_path = args.state.resolve()
    markdown_path = (args.markdown or default_markdown_path(state_path)).resolve()
    checks = validate_state(state_path, markdown_path)
    text = report_text(state_path, checks)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text, encoding="utf-8", newline="\n")
    print(text)
    return 0 if all(check.passed for check in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
