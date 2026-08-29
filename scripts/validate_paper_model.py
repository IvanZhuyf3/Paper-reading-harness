from __future__ import annotations

import argparse
import hashlib
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Check:
    name: str
    passed: bool
    detail: str


TRANSITION_STAGES = {"idea", "claims", "evidence", "independent_reading", "delta"}
BABYSITTING_RELATIONS = {
    "establishes_context",
    "creates_tension",
    "defines_gap",
    "motivates_significance",
    "resolves_gap",
    "decomposes",
    "supports",
    "operationalizes",
}
TRANSITION_PACKET_FIELDS = (
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


def _is_packet_model(model_version: object) -> bool:
    try:
        major, minor, *_ = (int(part) for part in str(model_version).split("."))
    except (TypeError, ValueError):
        return False
    return (major, minor) >= (0, 2)


def _is_babysitting_model(model_version: object) -> bool:
    try:
        major, minor, *_ = (int(part) for part in str(model_version).split("."))
    except (TypeError, ValueError):
        return False
    return (major, minor) >= (0, 3)


def validate_transition_packets(
    checks: list[Check],
    model: dict,
    node_ids: set[str],
    claim_ids: set[str],
    evidence_ids: set[str],
) -> None:
    packets = model.get("transition_packets", [])
    requires_packets = _is_packet_model(model.get("model_version"))
    babysitting_packets = [packet for packet in packets if packet.get("id") == "BABYSITTING_START"]
    ordinary_packets = [packet for packet in packets if packet.get("id") != "BABYSITTING_START"]
    if not packets:
        checks.append(
            Check(
                "Transition packets are present",
                not requires_packets,
                "legacy model: not required" if not requires_packets else "missing packets for model >= 0.2",
            )
        )
        if requires_packets:
            checks.append(Check("Transition-packet audit flag is finalized", False, "compiler.transition_packet_audit is not pass"))
        return

    packet_ids = [packet.get("id", "") for packet in packets]
    duplicate_ids = sorted({packet_id for packet_id in packet_ids if not packet_id or packet_ids.count(packet_id) > 1})
    checks.append(Check("Transition-packet IDs are present and unique", not duplicate_ids, f"duplicates={duplicate_ids}"))

    stages = [packet.get("target_stage", "") for packet in ordinary_packets]
    invalid_stages = sorted(set(stages) - TRANSITION_STAGES)
    missing_stages = sorted(TRANSITION_STAGES - set(stages))
    duplicate_stages = sorted({stage for stage in stages if stages.count(stage) > 1})
    checks.append(Check("Transition-packet stages are complete and unique", not invalid_stages and not missing_stages and not duplicate_stages, f"invalid={invalid_stages}, missing={missing_stages}, duplicates={duplicate_stages}"))

    allowed_levels = {"foundation", "core", "advanced"}
    invalid_levels = sorted(
        f"{packet.get('id')}: {level}"
        for packet in ordinary_packets
        for level in packet.get("eligible_levels", [])
        if level not in allowed_levels
    )
    checks.append(Check("Transition-packet levels are valid", not invalid_levels, f"invalid={invalid_levels}"))

    invalid_references: list[str] = []
    malformed: list[str] = []
    missing_schema_fields: list[str] = []
    for packet in ordinary_packets:
        packet_id = packet.get("id", "")
        missing_schema_fields.extend(
            f"{packet_id}:{field}"
            for field in TRANSITION_PACKET_FIELDS
            if field not in packet
        )
        if not all(packet.get(field) for field in ("target_stage", "eligible_levels", "content", "prompt_id", "prompt_text")):
            malformed.append(packet_id)
        invalid_references.extend(
            f"{packet_id}:reveal_claim:{item_id}"
            for item_id in packet.get("reveal_claim_ids", [])
            if item_id not in claim_ids
        )
        invalid_references.extend(
            f"{packet_id}:reveal_evidence:{item_id}"
            for item_id in packet.get("reveal_evidence_ids", [])
            if item_id not in evidence_ids
        )
        invalid_references.extend(
            f"{packet_id}:source:{item_id}"
            for item_id in packet.get("source_node_ids", [])
            if item_id not in node_ids
        )
    checks.append(Check("Transition-packet content and prompts are present", not malformed, f"missing={malformed}"))
    checks.append(Check("Transition-packet schema is complete", not missing_schema_fields, f"missing={missing_schema_fields}"))
    checks.append(Check("Transition-packet references resolve", not invalid_references, f"missing={sorted(invalid_references)}"))

    if requires_packets:
        compiler = model.get("compiler", {})
        checks.append(Check("Transition-packet audit flag is finalized", compiler.get("transition_packet_audit") == "pass", str(compiler.get("transition_packet_audit"))))

    validate_babysitting_assets(checks, model, claim_ids, node_ids, babysitting_packets)


def validate_babysitting_assets(
    checks: list[Check],
    model: dict,
    claim_ids: set[str],
    node_ids: set[str],
    packets: list[dict] | None = None,
) -> None:
    """Validate the reusable, evidence-detail-free disclosure assets for BABYSITTING.

    This is deliberately independent of the ordinary transition packet checks so
    0.1/0.2 models remain valid and simply report that BABYSITTING is unavailable.
    """
    terminology = model.get("terminology_nodes", [])
    edges = model.get("logical_edges", [])
    model_claims = set(claim_ids)
    model_claim_order = [item.get("id", "") for item in model.get("claim_nodes", [])]
    term_ids = {item.get("id") for item in terminology if item.get("id")}
    edge_ids = {item.get("id") for item in edges if item.get("id")}
    term_order = [item.get("id", "") for item in terminology]
    edge_order = [item.get("id", "") for item in edges]
    supports = bool(model.get("babysitting_supported", False))
    packets = packets if packets is not None else [
        packet for packet in model.get("transition_packets", [])
        if packet.get("id") == "BABYSITTING_START"
    ]
    schema_requires = _is_babysitting_model(model.get("model_version"))

    if not supports and not packets:
        checks.append(Check("BABYSITTING assets (legacy model)", True, "not declared; unavailable by design"))
        return

    checks.append(Check("BABYSITTING support declaration is valid", supports and schema_requires, f"supported={supports}, model_version={model.get('model_version')}"))
    checks.append(Check("Terminology-node IDs are present and unique", unique_ids(terminology, "Terminology-node").passed, f"count={len(terminology)}"))
    checks.append(Check("Logical-edge IDs are present and unique", unique_ids(edges, "Logical-edge").passed, f"count={len(edges)}"))

    missing_terms: list[str] = []
    invalid_term_refs: list[str] = []
    weak_asset_anchors: list[str] = []
    anchor_pattern = re.compile(r"(PDF p\.|Fig\.|Figs\.|Eq\.|Eqs\.|Supplementary)")
    for item in terminology:
        item_id = item.get("id", "")
        if not item.get("term") or not item.get("definition") or not item.get("source_anchors"):
            missing_terms.append(item_id)
        invalid_term_refs.extend(
            f"{item_id}:prerequisite:{ref}"
            for ref in item.get("prerequisites", [])
            if ref not in term_ids
        )
        invalid_term_refs.extend(
            f"{item_id}:claim:{ref}"
            for ref in item.get("related_claim_ids", [])
            if ref not in model_claims
        )
        weak_asset_anchors.extend(
            f"{item_id}: {anchor}"
            for anchor in item.get("source_anchors", [])
            if not anchor_pattern.search(anchor)
        )
    checks.append(Check("Terminology definitions and anchors are present", not missing_terms, f"missing={missing_terms}"))
    checks.append(Check("Terminology prerequisites and related claims resolve", not invalid_term_refs, f"missing={sorted(invalid_term_refs)}"))

    invalid_edges: list[str] = []
    malformed_edges: list[str] = []
    for edge in edges:
        edge_id = edge.get("id", "")
        if (
            not edge.get("source_claim_ids")
            or not edge.get("target_claim_id")
            or edge.get("relation") not in BABYSITTING_RELATIONS
            or not edge.get("explanation")
            or not edge.get("source_anchors")
        ):
            malformed_edges.append(edge_id)
        invalid_edges.extend(
            f"{edge_id}:source:{ref}"
            for ref in edge.get("source_claim_ids", [])
            if ref not in model_claims
        )
        if edge.get("target_claim_id") not in model_claims:
            invalid_edges.append(f"{edge_id}:target:{edge.get('target_claim_id')}")
        weak_asset_anchors.extend(
            f"{edge_id}: {anchor}"
            for anchor in edge.get("source_anchors", [])
            if not anchor_pattern.search(anchor)
        )
    checks.append(Check("Logical-edge schema and relation labels are valid", not malformed_edges, f"malformed={malformed_edges}"))
    checks.append(Check("Logical-edge claim references resolve", not invalid_edges, f"missing={sorted(invalid_edges)}"))
    checks.append(Check("BABYSITTING asset anchors are reader-locatable", not weak_asset_anchors, f"weak={weak_asset_anchors}"))

    duplicate_packets = len(packets) != 1
    checks.append(Check("Exactly one BABYSITTING_START packet exists", not duplicate_packets, f"count={len(packets)}"))
    if duplicate_packets:
        return
    packet = packets[0]
    required_fields = {
        "id", "target_stage", "eligible_levels", "reveal_claim_ids",
        "reveal_evidence_ids", "source_node_ids", "dynamic_slots", "locale",
        "content", "prompt_id", "prompt_text", "display_claim_ids",
        "terminology_ids", "logical_edge_ids",
    }
    missing_fields = sorted(required_fields - set(packet))
    checks.append(Check("BABYSITTING_START packet schema is complete", not missing_fields, f"missing={missing_fields}"))
    checks.append(Check("BABYSITTING_START packet target and level are fixed", packet.get("target_stage") == "knowledge" and packet.get("eligible_levels") == ["babysitting"], f"target={packet.get('target_stage')}, levels={packet.get('eligible_levels')}"))
    display_claims = packet.get("display_claim_ids", [])
    packet_refs = []
    packet_refs.extend(f"claim:{ref}" for ref in display_claims if ref not in model_claims)
    packet_refs.extend(f"reveal_claim:{ref}" for ref in packet.get("reveal_claim_ids", []) if ref not in model_claims)
    packet_refs.extend(f"term:{ref}" for ref in packet.get("terminology_ids", []) if ref not in term_ids)
    packet_refs.extend(f"edge:{ref}" for ref in packet.get("logical_edge_ids", []) if ref not in edge_ids)
    packet_refs.extend(f"source:{ref}" for ref in packet.get("source_node_ids", []) if ref not in node_ids)
    checks.append(Check("BABYSITTING_START packet references resolve", not packet_refs, f"missing={sorted(packet_refs)}"))
    declared_view = model.get("disclosure_views", {}).get("babysitting", [])
    expected_view = display_claims + packet.get("terminology_ids", []) + packet.get("logical_edge_ids", [])
    checks.append(Check("BABYSITTING disclosure view matches packet", declared_view == expected_view, f"view_count={len(declared_view)}, packet_count={len(expected_view)}"))
    complete_claims = display_claims == model_claim_order and packet.get("reveal_claim_ids") == display_claims and packet.get("source_node_ids") == display_claims
    complete_terms = packet.get("terminology_ids") == term_order
    complete_edges = packet.get("logical_edge_ids") == edge_order
    checks.append(Check("BABYSITTING packet claim disclosure is complete", complete_claims, f"display={len(display_claims)}, model={len(model_claim_order)}"))
    checks.append(Check("BABYSITTING packet terminology disclosure is complete", complete_terms, f"packet={len(packet.get('terminology_ids', []))}, model={len(term_order)}"))
    checks.append(Check("BABYSITTING packet logical-edge disclosure is complete", complete_edges, f"packet={len(packet.get('logical_edge_ids', []))}, model={len(edge_order)}"))
    checks.append(Check("BABYSITTING_START does not reveal evidence", packet.get("reveal_evidence_ids") == [], f"revealed={packet.get('reveal_evidence_ids')}"))
    checks.append(Check("BABYSITTING_START fixed prompt is present", packet.get("prompt_id") == "BABYSITTING_START_PROMPT" and packet.get("prompt_text") == "Which term or logical relation is unclear? Pick one.", f"prompt_id={packet.get('prompt_id')}, prompt_text={packet.get('prompt_text')}"))
    compiler = model.get("compiler", {})
    checks.append(Check("BABYSITTING audit flag is finalized", compiler.get("babysitting_audit") == "pass", str(compiler.get("babysitting_audit"))))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def unique_ids(items: list[dict], label: str) -> Check:
    ids = [item.get("id", "") for item in items]
    duplicates = sorted({item_id for item_id in ids if ids.count(item_id) > 1})
    missing = sum(not item_id for item_id in ids)
    passed = not duplicates and missing == 0
    return Check(
        f"{label} IDs are present and unique",
        passed,
        f"count={len(ids)}, missing={missing}, duplicates={duplicates}",
    )


def cross_type_duplicates(collections: dict[str, set[str]]) -> set[str]:
    """Return IDs shared by any two model node/asset collections."""
    all_values: dict[str, set[str]] = {}
    for name, values in collections.items():
        for value in values:
            all_values.setdefault(value, set()).add(name)
    return {value for value, owners in all_values.items() if len(owners) > 1}


def render_report(model_path: Path, checks: list[Check], counts: dict[str, int]) -> str:
    passed = sum(check.passed for check in checks)
    overall = "PASS" if passed == len(checks) else "FAIL"
    lines = [
        "# Paper-Model Mechanical Audit",
        "",
        f"- **Model:** `{model_path.name}`",
        f"- **Overall:** {overall}",
        f"- **Checks passed:** {passed}/{len(checks)}",
        f"- **Knowledge nodes:** {counts['knowledge']}",
        f"- **Claim nodes:** {counts['claims']}",
        f"- **Evidence nodes:** {counts['evidence']}",
        "",
        "## Checks",
        "",
        "| Check | Result | Detail |",
        "|---|---|---|",
    ]
    for check in checks:
        result = "PASS" if check.passed else "FAIL"
        detail = check.detail.replace("|", "\\|")
        lines.append(f"| {check.name} | {result} | {detail} |")
    lines.extend(
        [
            "",
            "## Scope",
            "",
            "This report validates parseability, identity/hash linkage, graph references, anchor presence, disclosure-view membership, and selection-policy invariants. It does not determine whether the paper's scientific trajectory is normatively optimal, and it does not visually prove that every prose anchor points to the intended paragraph.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a pending paper-model TOML file.")
    parser.add_argument("model", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    model_path = args.model.resolve()
    checks: list[Check] = []

    try:
        with model_path.open("rb") as stream:
            model = tomllib.load(stream)
        checks.append(Check("TOML parses", True, "tomllib loaded the model"))
    except Exception as exc:
        report = render_report(
            model_path,
            [Check("TOML parses", False, f"{type(exc).__name__}: {exc}")],
            {"knowledge": 0, "claims": 0, "evidence": 0},
        )
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(report, encoding="utf-8", newline="\n")
        print(report)
        return 1

    knowledge = model.get("knowledge_nodes", [])
    claims = model.get("claim_nodes", [])
    evidence = model.get("evidence_nodes", [])
    counts = {"knowledge": len(knowledge), "claims": len(claims), "evidence": len(evidence)}

    checks.extend(
        [
            unique_ids(knowledge, "Knowledge-node"),
            unique_ids(claims, "Claim-node"),
            unique_ids(evidence, "Evidence-node"),
        ]
    )

    knowledge_ids = {item["id"] for item in knowledge if item.get("id")}
    claim_ids = {item["id"] for item in claims if item.get("id")}
    evidence_ids = {item["id"] for item in evidence if item.get("id")}
    terminology_ids = {item["id"] for item in model.get("terminology_nodes", []) if item.get("id")}
    logical_edge_ids = {item["id"] for item in model.get("logical_edges", []) if item.get("id")}

    all_ids = knowledge_ids | claim_ids | evidence_ids | terminology_ids | logical_edge_ids
    cross_duplicates = cross_type_duplicates(
        {
            "knowledge": knowledge_ids,
            "claims": claim_ids,
            "evidence": evidence_ids,
            "terminology": terminology_ids,
            "logical_edges": logical_edge_ids,
        }
    )
    checks.append(
        Check(
            "IDs are unique across node types",
            not cross_duplicates,
            f"cross-type duplicates={sorted(cross_duplicates)}",
        )
    )

    missing_prereqs = sorted(
        {
            prereq
            for item in knowledge
            for prereq in item.get("prerequisites", [])
            if prereq not in knowledge_ids
        }
    )
    checks.append(
        Check(
            "Knowledge prerequisites resolve",
            not missing_prereqs,
            f"missing={missing_prereqs}",
        )
    )

    missing_parents = sorted(
        {
            parent
            for item in claims
            for parent in item.get("parents", [])
            if parent not in claim_ids
        }
    )
    checks.append(
        Check("Claim parents resolve", not missing_parents, f"missing={missing_parents}")
    )

    missing_targets = sorted(
        {
            target
            for item in evidence
            for target in item.get("target_claims", [])
            if target not in claim_ids
        }
    )
    checks.append(
        Check(
            "Evidence targets resolve",
            not missing_targets,
            f"missing={missing_targets}",
        )
    )

    nodes_without_anchors = sorted(
        item["id"]
        for item in [*knowledge, *claims, *evidence]
        if not item.get("source_anchors")
    )
    checks.append(
        Check(
            "Every node has a source anchor",
            not nodes_without_anchors,
            f"missing={nodes_without_anchors}",
        )
    )

    weak_anchors = []
    anchor_pattern = re.compile(r"(PDF p\.|Fig\.|Figs\.|Eq\.|Supplementary)")
    for item in [*knowledge, *claims, *evidence]:
        for anchor in item.get("source_anchors", []):
            if not anchor_pattern.search(anchor):
                weak_anchors.append(f"{item['id']}: {anchor}")
    checks.append(
        Check(
            "Anchors use reader-locatable forms",
            not weak_anchors,
            f"weak={weak_anchors}",
        )
    )

    claims_without_author = sorted(item["id"] for item in claims if not item.get("author_claim"))
    claims_without_interpretation = sorted(
        item["id"] for item in claims if not item.get("agent_interpretation")
    )
    checks.append(
        Check(
            "Claim nodes separate author claim and agent interpretation",
            not claims_without_author and not claims_without_interpretation,
            f"missing_author={claims_without_author}, missing_interpretation={claims_without_interpretation}",
        )
    )

    views = model.get("disclosure_views", {})
    special_tokens = {"all_claim_nodes", "all_evidence_nodes", "result_detail"}
    unresolved_view_ids = sorted(
        {
            item_id
            for values in views.values()
            for item_id in values
            if item_id not in all_ids and item_id not in special_tokens
        }
    )
    checks.append(
        Check(
            "Disclosure-view IDs resolve",
            not unresolved_view_ids,
            f"missing={unresolved_view_ids}",
        )
    )

    validate_transition_packets(checks, model, all_ids, claim_ids, evidence_ids)

    role_by_id = {item["id"]: item.get("role") for item in claims}
    idea_roles = {role_by_id.get(item_id) for item_id in views.get("idea_problem_state", [])}
    allowed_idea_roles = {"background", "limitation", "constraint", "existing_routes", "gap"}
    checks.append(
        Check(
            "IDEA view contains only problem-state roles",
            idea_roles <= allowed_idea_roles,
            f"roles={sorted(role for role in idea_roles if role)}",
        )
    )

    checks.append(
        Check(
            "CLAIMS starts only from T0",
            views.get("claims_start") == ["T0"],
            f"claims_start={views.get('claims_start')}",
        )
    )

    early_result_nodes = sorted(
        item["id"]
        for item in evidence
        if item.get("reveal_result_after") != "independent_reading_started"
    )
    checks.append(
        Check(
            "Evidence results remain hidden until independent reading",
            not early_result_nodes,
            f"violations={early_result_nodes}",
        )
    )

    expected_selection = {
        "knowledge_policy": "seeded_dependency_eligible",
        "idea_policy": "complete_problem_state_fixed_prompt_minimal_checkability_gate",
        "claims_policy": "human_tree_open_nodes_only_transferability_filtered",
        "evidence_policy": "revealed_claims_only_transferability_filtered",
        "transferability_filter": "default_reusable_reasoning_primitives",
        "delta_policy": "fixed_prompt",
    }
    selection = model.get("selection", {})
    checks.append(
        Check(
            "Selection-policy version is current",
            model.get("selection_policy_version") == "1.2",
            f"version={model.get('selection_policy_version')}",
        )
    )
    selection_mismatch = {
        key: selection.get(key)
        for key, expected in expected_selection.items()
        if selection.get(key) != expected
    }
    checks.append(
        Check(
            "Selection policies match protocol",
            not selection_mismatch,
            f"mismatch={selection_mismatch}",
        )
    )

    source_path = (model_path.parent / model.get("source_path", "")).resolve()
    source_exists = source_path.is_file()
    checks.append(Check("Source PDF exists", source_exists, str(source_path)))
    expected_hash = model.get("source_sha256", "").upper()
    actual_hash = sha256(source_path) if source_exists else ""
    checks.append(
        Check(
            "Source SHA-256 matches",
            bool(re.fullmatch(r"[0-9A-F]{64}", expected_hash)) and actual_hash == expected_hash,
            f"expected={expected_hash}, actual={actual_hash}",
        )
    )

    supplement_value = model.get("supplement_path")
    if supplement_value:
        supplement_path = (model_path.parent / supplement_value).resolve()
        supplement_exists = supplement_path.is_file()
        checks.append(Check("Supplement PDF exists", supplement_exists, str(supplement_path)))
        expected_supplement_hash = model.get("supplement_sha256", "").upper()
        actual_supplement_hash = sha256(supplement_path) if supplement_exists else ""
        checks.append(
            Check(
                "Supplement SHA-256 matches",
                bool(re.fullmatch(r"[0-9A-F]{64}", expected_supplement_hash))
                and actual_supplement_hash == expected_supplement_hash,
                f"expected={expected_supplement_hash}, actual={actual_supplement_hash}",
            )
        )

    compiler = model.get("compiler", {})
    compiler_flags = {
        "parse_validated": compiler.get("parse_validated"),
        "anchor_audit": compiler.get("anchor_audit"),
        "visibility_audit": compiler.get("visibility_audit"),
    }
    flags_pass = (
        compiler_flags["parse_validated"] is True
        and compiler_flags["anchor_audit"] == "pass"
        and compiler_flags["visibility_audit"] == "pass"
    )
    checks.append(Check("Compiler audit flags are finalized", flags_pass, str(compiler_flags)))

    report = render_report(model_path, checks, counts)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report, encoding="utf-8", newline="\n")
    print(report)
    return 0 if all(check.passed for check in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
