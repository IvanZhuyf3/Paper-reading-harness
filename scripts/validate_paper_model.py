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

    all_ids = knowledge_ids | claim_ids | evidence_ids
    cross_duplicates = (
        (knowledge_ids & claim_ids) | (knowledge_ids & evidence_ids) | (claim_ids & evidence_ids)
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
        "claims_policy": "human_tree_open_nodes_only",
        "evidence_policy": "revealed_claims_only",
        "delta_policy": "fixed_prompt",
    }
    selection = model.get("selection", {})
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
