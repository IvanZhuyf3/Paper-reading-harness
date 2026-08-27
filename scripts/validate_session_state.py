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


def report_text(state_path: Path, checks: list[Check]) -> str:
    passed = sum(check.passed for check in checks)
    overall = "PASS" if passed == len(checks) else "FAIL"
    lines = [
        "# Session-State Recovery Audit",
        "",
        f"- **State:** `{state_path.name}`",
        f"- **Overall:** {overall}",
        f"- **Checks passed:** {passed}/{len(checks)}",
        "",
        "| Check | Result | Detail |",
        "|---|---|---|",
    ]
    for check in checks:
        result = "PASS" if check.passed else "FAIL"
        lines.append(f"| {check.name} | {result} | {check.detail.replace('|', '\\|')} |")
    lines.extend(
        [
            "",
            "The audit verifies that the persisted TOML state can identify its frozen paper model and recover a unique next interaction. It does not evaluate the scientific content of the human rollout.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a paper-harness session state.")
    parser.add_argument("state", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    state_path = args.state.resolve()
    checks: list[Check] = []

    try:
        with state_path.open("rb") as stream:
            state = tomllib.load(stream)
        checks.append(Check("Session TOML parses", True, "tomllib loaded the state"))
    except Exception as exc:
        text = report_text(state_path, [Check("Session TOML parses", False, str(exc))])
        if args.report:
            args.report.write_text(text, encoding="utf-8", newline="\n")
        print(text)
        return 1

    model_path = (state_path.parent / state.get("paper_model_path", "")).resolve()
    model_exists = model_path.is_file()
    checks.append(Check("Pinned paper model exists", model_exists, str(model_path)))

    model = {}
    if model_exists:
        with model_path.open("rb") as stream:
            model = tomllib.load(stream)

    expected_model_hash = state.get("paper_model_sha256", "").upper()
    actual_model_hash = sha256(model_path) if model_exists else ""
    checks.append(
        Check(
            "Pinned paper-model SHA-256 matches",
            bool(re.fullmatch(r"[0-9A-F]{64}", expected_model_hash))
            and actual_model_hash == expected_model_hash,
            f"expected={expected_model_hash}, actual={actual_model_hash}",
        )
    )

    checks.append(
        Check(
            "Paper-model version matches",
            state.get("paper_model_version") == model.get("model_version"),
            f"state={state.get('paper_model_version')}, model={model.get('model_version')}",
        )
    )
    checks.append(
        Check(
            "Selection-policy version matches",
            state.get("selection_policy_version") == model.get("selection_policy_version"),
            f"state={state.get('selection_policy_version')}, model={model.get('selection_policy_version')}",
        )
    )
    checks.append(
        Check(
            "Main-source hash matches model",
            state.get("main_source_sha256") == model.get("source_sha256"),
            f"state={state.get('main_source_sha256')}, model={model.get('source_sha256')}",
        )
    )
    checks.append(
        Check(
            "Supplement hash matches model",
            state.get("supplement_sha256") == model.get("supplement_sha256"),
            f"state={state.get('supplement_sha256')}, model={model.get('supplement_sha256')}",
        )
    )

    allowed_stages = {"knowledge", "idea", "claims", "evidence", "independent_reading", "delta", "complete"}
    checks.append(
        Check(
            "Current stage is valid",
            state.get("current_stage") in allowed_stages,
            str(state.get("current_stage")),
        )
    )

    stage_order = ["knowledge", "idea", "claims", "evidence", "independent_reading", "delta"]
    completed_stages = state.get("completed_stages", [])
    current_stage = state.get("current_stage")
    expected_prefix = (
        stage_order[: stage_order.index(current_stage)]
        if current_stage in stage_order
        else stage_order
        if current_stage == "complete"
        else []
    )
    checks.append(
        Check(
            "Completed stages form the prefix before the current stage",
            completed_stages == expected_prefix,
            f"completed={completed_stages}, expected={expected_prefix}",
        )
    )

    asked_ids = state.get("asked_ids", [])
    checks.append(
        Check(
            "Asked IDs are unique",
            len(asked_ids) == len(set(asked_ids)),
            f"count={len(asked_ids)}",
        )
    )
    checks.append(
        Check(
            "Selection seed is persisted",
            isinstance(state.get("selection_seed"), int) and state.get("selection_seed") > 0,
            str(state.get("selection_seed")),
        )
    )

    human_nodes = state.get("human_nodes", [])
    human_ids = {node.get("id") for node in human_nodes}
    unresolved_parents = sorted(
        {
            parent
            for node in human_nodes
            for parent in node.get("parents", [])
            if parent not in human_ids
        }
    )
    checks.append(
        Check("Human-node parents resolve", not unresolved_parents, f"missing={unresolved_parents}")
    )

    cursor_present = bool(state.get("resume_cursor"))
    pending_present = bool(state.get("pending_prompt_id") and state.get("pending_prompt_text"))
    checks.append(
        Check(
            "Unique next interaction is persisted",
            cursor_present and (state.get("rollout_complete") is True or pending_present),
            f"cursor={state.get('resume_cursor')}, pending_prompt={state.get('pending_prompt_id')}",
        )
    )

    checks.append(
        Check(
            "Event sequence is contiguous",
            [event.get("sequence") for event in state.get("events", [])]
            == list(range(1, len(state.get("events", [])) + 1)),
            f"events={len(state.get('events', []))}",
        )
    )

    text = report_text(state_path, checks)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text, encoding="utf-8", newline="\n")
    print(text)
    return 0 if all(check.passed for check in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
