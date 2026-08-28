#!/usr/bin/env python3
"""Create a validated, model-pinned TRAINING session before its first prompt."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import tomllib
from pathlib import Path

try:
    from .render_session_markdown import render
except ImportError:
    from render_session_markdown import render


LEVELS = {"foundation", "core", "advanced"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def toml_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(item) for item in value) + "]"
    if isinstance(value, dict):
        return "{ " + ", ".join(f"{key} = {toml_value(item)}" for key, item in value.items()) + " }"
    raise TypeError(f"unsupported TOML value: {type(value).__name__}")


def first_knowledge_node(model: dict, level: str, seed: int) -> dict:
    allowed_ids = set(model.get("disclosure_views", {}).get("knowledge", []))
    candidates = [
        node
        for node in model.get("knowledge_nodes", [])
        if node.get("id") in allowed_ids
        and level in node.get("required_levels", [])
        and node.get("visibility") == "pre_idea"
        and node.get("question_eligible") is True
        and not node.get("prerequisites", [])
    ]
    if not candidates:
        raise ValueError(f"no initial KNOWLEDGE node is eligible for {level}")
    minimum = min(node.get("priority", 0) for node in candidates)
    tied = sorted(
        (node for node in candidates if node.get("priority", 0) == minimum),
        key=lambda node: node["id"],
    )
    return random.Random(seed).choice(tied)


def write_state(
    output: Path,
    model_path: Path,
    model: dict,
    session_id: str,
    level: str,
    seed: int,
    prompt_id: str,
    prompt_text: str,
) -> None:
    relative_model = os.path.relpath(model_path, output.parent).replace("\\", "/")
    fields: list[tuple[str, object]] = [
        ("state_version", "1.0"),
        ("session_id", session_id),
        ("runner", "training"),
        ("level", level),
        ("paper_model_path", relative_model),
        ("paper_model_version", model["model_version"]),
        ("paper_model_sha256", sha256(model_path)),
        ("main_source_sha256", model["source_sha256"]),
    ]
    if model.get("supplement_sha256"):
        fields.append(("supplement_sha256", model["supplement_sha256"]))
    fields.extend(
        [
            ("selection_policy_version", model["selection_policy_version"]),
            ("selection_seed", seed),
            ("current_stage", "knowledge"),
            ("resume_cursor", f"KNOWLEDGE.{prompt_id}.await_response"),
            ("asked_ids", [prompt_id]),
            ("verified_knowledge_ids", []),
            ("rollout_complete", False),
            ("completed_stages", []),
            ("revealed_paper_claim_ids", []),
            ("revealed_paper_evidence_ids", []),
            ("pending_prompt_id", prompt_id),
            ("pending_prompt_text", prompt_text),
            (
                "stage_dispositions",
                {
                    "knowledge": "in_progress",
                    "idea": "in_progress",
                    "claims": "in_progress",
                    "evidence": "in_progress",
                    "independent_reading": "in_progress",
                    "delta": "in_progress",
                },
            ),
            ("human_had_not_read_at_entry", True),
        ]
    )
    lines = [f"{key} = {toml_value(value)}" for key, value in fields]
    for evidence in model.get("evidence_nodes", []):
        lines.extend(["", "[[paper_evidence_designs]]"])
        for key in ("id", "target_claims", "evidence_type", "control_roles", "source_anchors"):
            lines.append(f"{key} = {toml_value(evidence[key])}")
    packet_fields = (
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
    for packet in model.get("transition_packets", []):
        lines.extend(["", "[[prefilled_transition_packets]]"])
        for key in packet_fields:
            lines.append(f"{key} = {toml_value(packet[key])}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_markdown(
    output: Path,
    model: dict,
    model_path: Path,
    level: str,
    seed: int,
    prompt_id: str,
    prompt_text: str,
) -> None:
    relative_model = os.path.relpath(model_path, output.parent).replace("\\", "/")
    header = f"""# {level.upper()} Training Session - {output.stem}

**Paper:** {model['title']}
**Identifier:** {model.get('manuscript_id') or model.get('doi') or 'local source'}
**Runner:** TRAINING
**Level:** {level.upper()}
**Paper-model source:** compiled pending model for originating session
**Paper-model path:** `{relative_model}`
**Paper-model version:** {model['model_version']}
**Paper-model SHA-256:** `{sha256(model_path)}`
**Main-source SHA-256:** `{model['source_sha256']}`
**Selection-policy version:** {model['selection_policy_version']}
**Selection seed:** {seed}
**Human had not read paper at entry:** YES
**Current state:** KNOWLEDGE
**Resume cursor:** `KNOWLEDGE.{prompt_id}.await_response`
**Pending prompt:** `{prompt_id}`

## Disclosure note

The title and supplied filename may expose terminology from the author solution.
KNOWLEDGE prompts must be selected from prerequisite concepts and must not use
the hidden paper claim tree to steer the human.

## Pending interaction

> {prompt_text}
"""
    output.write_text(header, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("model", type=Path)
    parser.add_argument("state", type=Path)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--level", required=True, choices=sorted(LEVELS))
    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--prompt-text")
    args = parser.parse_args()

    model_path = args.model.resolve()
    state_path = args.state.resolve()
    with model_path.open("rb") as stream:
        model = tomllib.load(stream)
    selected = first_knowledge_node(model, args.level, args.seed)
    prompt_text = args.prompt_text or selected["prompt"]
    write_state(
        state_path,
        model_path,
        model,
        args.session_id,
        args.level,
        args.seed,
        selected["id"],
        prompt_text,
    )
    markdown_path = state_path.with_name(state_path.name.replace(".state.toml", ".md"))
    write_markdown(
        markdown_path,
        model,
        model_path,
        args.level,
        args.seed,
        selected["id"],
        prompt_text,
    )
    render(state_path, markdown_path)
    print(f"created {state_path}")
    print(f"selected {selected['id']}: {prompt_text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
