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


LEVELS = {"foundation", "core", "advanced", "babysitting"}


def _version_at_least(version: object, minimum: tuple[int, int]) -> bool:
    try:
        parts = [int(part) for part in str(version).split(".")]
    except (TypeError, ValueError):
        return False
    return tuple((parts + [0, 0])[:2]) >= minimum


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


def babysitting_start_packet(model: dict) -> dict:
    """Return the validated frozen disclosure packet required by BABYSITTING."""
    if not model.get("babysitting_supported", False):
        raise ValueError(
            "BABYSITTING is unavailable: pinned paper model does not declare babysitting_supported"
        )
    packets = [
        packet for packet in model.get("transition_packets", [])
        if packet.get("id") == "BABYSITTING_START"
    ]
    if len(packets) != 1:
        raise ValueError(
            f"BABYSITTING requires exactly one validated BABYSITTING_START packet; found {len(packets)}"
        )
    packet = packets[0]
    required = (
        "display_claim_ids",
        "terminology_ids",
        "logical_edge_ids",
        "content",
        "prompt_id",
        "prompt_text",
    )
    missing = [key for key in required if not packet.get(key)]
    if missing:
        raise ValueError(f"BABYSITTING_START packet is incomplete: missing {missing}")
    if packet.get("target_stage") != "knowledge" or packet.get("eligible_levels") != ["babysitting"]:
        raise ValueError("BABYSITTING_START packet must target knowledge and eligible_levels=['babysitting']")
    if packet.get("reveal_evidence_ids") != []:
        raise ValueError("BABYSITTING_START packet must not reveal evidence IDs")
    terminology = {item.get("id") for item in model.get("terminology_nodes", [])}
    edges = {item.get("id") for item in model.get("logical_edges", [])}
    claims = {item.get("id") for item in model.get("claim_nodes", [])}
    model_claim_order = [item.get("id") for item in model.get("claim_nodes", [])]
    model_term_order = [item.get("id") for item in model.get("terminology_nodes", [])]
    model_edge_order = [item.get("id") for item in model.get("logical_edges", [])]
    if not _version_at_least(model.get("model_version"), (0, 3)) or model.get("compiler", {}).get("babysitting_audit") != "pass":
        raise ValueError("BABYSITTING requires a model version 0.3+ with compiler.babysitting_audit='pass'")
    if len(terminology) != len(model.get("terminology_nodes", [])) or len(edges) != len(model.get("logical_edges", [])):
        raise ValueError("BABYSITTING terminology and logical-edge IDs must be unique and non-empty")
    for term in model.get("terminology_nodes", []):
        if not term.get("term") or not term.get("definition") or not term.get("source_anchors"):
            raise ValueError(f"BABYSITTING terminology node {term.get('id')} is incomplete")
        if set(term.get("prerequisites", [])) - terminology or set(term.get("related_claim_ids", [])) - claims:
            raise ValueError(f"BABYSITTING terminology node {term.get('id')} has dangling references")
    for edge in model.get("logical_edges", []):
        if not edge.get("source_claim_ids") or edge.get("target_claim_id") not in claims or not edge.get("explanation") or not edge.get("source_anchors"):
            raise ValueError(f"BABYSITTING logical edge {edge.get('id')} is incomplete")
        if set(edge.get("source_claim_ids", [])) - claims:
            raise ValueError(f"BABYSITTING logical edge {edge.get('id')} has dangling source claims")
    if packet.get("display_claim_ids") != model_claim_order or packet.get("reveal_claim_ids") != model_claim_order or packet.get("source_node_ids") != model_claim_order:
        raise ValueError("BABYSITTING_START packet must disclose every claim node in model order")
    if packet.get("terminology_ids") != model_term_order:
        raise ValueError("BABYSITTING_START packet must disclose every terminology node in model order")
    if packet.get("logical_edge_ids") != model_edge_order:
        raise ValueError("BABYSITTING_START packet must disclose every logical edge in model order")
    if len(packet.get("display_claim_ids", [])) != len(set(packet.get("display_claim_ids", []))) or len(packet.get("terminology_ids", [])) != len(set(packet.get("terminology_ids", []))) or len(packet.get("logical_edge_ids", [])) != len(set(packet.get("logical_edge_ids", []))):
        raise ValueError("BABYSITTING_START packet disclosure lists must contain unique IDs")
    if set(packet["display_claim_ids"]) - claims:
        raise ValueError("BABYSITTING_START packet contains dangling claim IDs")
    if set(packet["terminology_ids"]) - terminology:
        raise ValueError("BABYSITTING_START packet contains dangling terminology IDs")
    if set(packet["logical_edge_ids"]) - edges:
        raise ValueError("BABYSITTING_START packet contains dangling logical-edge IDs")
    return packet


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
    babysitting = level == "babysitting"
    packet = babysitting_start_packet(model) if babysitting else None
    if babysitting:
        prompt_id = packet["prompt_id"]
        prompt_text = packet["prompt_text"]
    fields: list[tuple[str, object]] = [
        ("state_version", "1.0"),
        ("session_id", session_id),
        ("runner", "training"),
        ("level", level),
        ("paper_model_path", relative_model),
        ("paper_model_version", model["model_version"]),
        ("paper_model_sha256", sha256(model_path)),
        ("main_source_sha256", model["source_sha256"]),
        ("babysitting_supported", bool(model.get("babysitting_supported", False))),
    ]
    if model.get("supplement_sha256"):
        fields.append(("supplement_sha256", model["supplement_sha256"]))
    fields.extend(
        [
            ("selection_policy_version", model["selection_policy_version"]),
            ("selection_seed", seed),
            ("current_stage", "knowledge"),
            ("resume_cursor", "BABYSITTING.select_item.await_response" if babysitting else f"KNOWLEDGE.{prompt_id}.await_response"),
            ("asked_ids", [prompt_id]),
            ("verified_knowledge_ids", []),
            ("rollout_complete", False),
            ("completed_stages", []),
            ("revealed_paper_claim_ids", packet["display_claim_ids"] if babysitting else []),
            ("revealed_paper_evidence_ids", []),
            ("pending_prompt_id", prompt_id),
            ("pending_prompt_text", prompt_text),
            (
                "stage_dispositions",
                ({
                    "knowledge": "in_progress",
                    "idea": "not_applicable",
                    "claims": "not_applicable",
                    "evidence": "not_applicable",
                    "independent_reading": "not_applicable",
                    "delta": "not_applicable",
                } if babysitting else {
                    "knowledge": "in_progress",
                    "idea": "in_progress",
                    "claims": "in_progress",
                    "evidence": "in_progress",
                    "independent_reading": "in_progress",
                    "delta": "in_progress",
                }),
            ),
            ("human_had_not_read_at_entry", True),
        ]
    )
    if babysitting:
        fields.extend(
            [
                ("active_item_id", ""),
                ("active_item_kind", ""),
                ("explained_terminology_ids", []),
                ("explained_relation_ids", []),
                ("verified_terminology_ids", []),
                ("verified_relation_ids", []),
                ("unresolved_terminology_ids", packet["terminology_ids"]),
                ("unresolved_relation_ids", packet["logical_edge_ids"]),
                ("current_check_prompt", ""),
                ("babysitting_display_claim_ids", packet["display_claim_ids"]),
                ("babysitting_display_terminology_ids", packet["terminology_ids"]),
                ("babysitting_display_logical_edge_ids", packet["logical_edge_ids"]),
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
    for transition_packet in model.get("transition_packets", []):
        lines.extend(["", "[[prefilled_transition_packets]]"])
        fields_to_write = list(packet_fields)
        for key in ("display_claim_ids", "terminology_ids", "logical_edge_ids"):
            if key in transition_packet:
                fields_to_write.append(key)
        for key in fields_to_write:
            lines.append(f"{key} = {toml_value(transition_packet[key])}")
    if babysitting:
        term_by_id = {term.get("id"): term for term in model.get("terminology_nodes", [])}
        edge_by_id = {edge.get("id"): edge for edge in model.get("logical_edges", [])}
        for term_id in packet["terminology_ids"]:
            term = term_by_id[term_id]
            lines.extend(["", "[[babysitting_terminology_nodes]]"])
            for key in ("id", "term", "aliases", "definition", "prerequisites", "related_claim_ids", "source_anchors"):
                lines.append(f"{key} = {toml_value(term.get(key, [] if key in { 'aliases', 'prerequisites', 'related_claim_ids', 'source_anchors' } else ''))}")
        for edge_id in packet["logical_edge_ids"]:
            edge = edge_by_id[edge_id]
            lines.extend(["", "[[babysitting_logical_edges]]"])
            for key in ("id", "source_claim_ids", "target_claim_id", "relation", "explanation", "source_anchors"):
                lines.append(f"{key} = {toml_value(edge.get(key, [] if key in { 'source_claim_ids', 'source_anchors' } else ''))}")
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
    babysitting_packet = babysitting_start_packet(model) if level == "babysitting" else None
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
**Resume cursor:** `{('BABYSITTING.select_item.await_response' if babysitting_packet else f'KNOWLEDGE.{prompt_id}.await_response')}`
**Pending prompt:** `{prompt_id}`

## Disclosure note

{('The complete source-anchored claim tree, logical-edge explanations, and terminology inventory are disclosed from the frozen BABYSITTING_START packet. Evidence result details remain hidden.' if babysitting_packet else 'The title and supplied filename may expose terminology from the author solution.\nKNOWLEDGE prompts must be selected from prerequisite concepts and must not use\nthe hidden paper claim tree to steer the human.')}

{babysitting_packet['content'] if babysitting_packet else ''}

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
    if args.level == "babysitting":
        packet = babysitting_start_packet(model)
        selected = {"id": packet["prompt_id"]}
        prompt_text = packet["prompt_text"]
    else:
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
