from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path


GENERATED_BEGIN = "<!-- BEGIN GENERATED EVENT TIMELINE -->"
GENERATED_END = "<!-- END GENERATED EVENT TIMELINE -->"
NARRATIVE_BEGIN = "<!-- BEGIN HUMAN NARRATIVE -->"
NARRATIVE_END = "<!-- END HUMAN NARRATIVE -->"
EVENT_HEADING = re.compile(r"(?m)^Event (\d+) — .*$")
NARRATIVE_HEADING = re.compile(r"(?m)^### Human narrative record — #(\d+) — .*$")


def default_markdown_path(state_path: Path) -> Path:
    if state_path.name.endswith(".state.toml"):
        return state_path.with_name(state_path.name[: -len(".state.toml")] + ".md")
    return state_path.with_suffix(".md")


def _remove_region(text: str, begin: str, end: str) -> tuple[str, str | None]:
    match = re.search(re.escape(begin) + r"\n?(.*?)\n?" + re.escape(end), text, re.DOTALL)
    if not match:
        return text, None
    outside = text[: match.start()] + text[match.end() :]
    return outside, match.group(1)


def _extract_narrative(text: str) -> tuple[str, list[tuple[int, str]]]:
    outside, region = _remove_region(text, NARRATIVE_BEGIN, NARRATIVE_END)
    source = region if region is not None else outside
    heading_matches = list(EVENT_HEADING.finditer(source))
    if not heading_matches:
        heading_matches = list(NARRATIVE_HEADING.finditer(source))
    if not heading_matches:
        return outside if region is not None else source, []

    prefix = (outside if region is not None else source[: heading_matches[0].start()]).rstrip()
    chunks: list[tuple[int, str]] = []
    for index, match in enumerate(heading_matches):
        end = heading_matches[index + 1].start() if index + 1 < len(heading_matches) else len(source)
        block = source[match.start() : end].strip()
        number = int(match.group(1) or match.group(2))
        block = re.sub(
            r"^Event (\d+) — (.*)$",
            r"### Human narrative record — #\1 — \2",
            block,
            count=1,
            flags=re.MULTILINE,
        )
        chunks.append((number, block))
    return prefix, sorted(chunks, key=lambda item: item[0])


def _quote(text: str) -> str:
    return "\n".join("> " + line for line in str(text).splitlines())


def render_text(state: dict, existing_markdown: str) -> str:
    events = state.get("events", [])
    sequences = [event.get("sequence") for event in events]
    expected = list(range(1, len(events) + 1))
    if sequences != expected:
        raise ValueError(f"event sequence must be contiguous: {sequences}")

    without_generated, _ = _remove_region(existing_markdown, GENERATED_BEGIN, GENERATED_END)
    prefix, narrative = _extract_narrative(without_generated)
    parts = [prefix.rstrip()]
    if narrative:
        parts.extend(["", NARRATIVE_BEGIN, "## Chronological human narrative", ""])
        parts.extend(block for _, block in narrative)
        parts.extend([NARRATIVE_END])

    parts.extend(["", GENERATED_BEGIN, "## Machine-generated event timeline", ""])
    for event in events:
        sequence = event["sequence"]
        parts.extend(
            [
                f"### Event {sequence} — `{event['prompt_id']}`",
                "",
                f"**Stage:** `{event.get('stage', '')}`",
                f"**Selection policy:** `{event.get('selection_policy_version', '')}`",
                "",
                "**Prompt:**",
                "",
                _quote(event["prompt_text"]),
                "",
                "**Human response:**",
                "",
                _quote(event["human_response"]),
                "",
            ]
        )
    parts.extend([GENERATED_END, ""])
    return "\n".join(parts)


def render(state_path: Path, markdown_path: Path, check: bool = False) -> bool:
    with state_path.open("rb") as stream:
        state = tomllib.load(stream)
    existing = markdown_path.read_text(encoding="utf-8") if markdown_path.exists() else ""
    rendered = render_text(state, existing)
    if check:
        if existing != rendered:
            print(f"Markdown is not deterministic-render parity: {markdown_path}")
            return False
        return True
    markdown_path.write_text(rendered, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a session Markdown audit from canonical TOML events.")
    parser.add_argument("state", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true", help="fail if Markdown differs from deterministic output")
    args = parser.parse_args()
    state_path = args.state.resolve()
    markdown_path = (args.output or default_markdown_path(state_path)).resolve()
    try:
        return 0 if render(state_path, markdown_path, check=args.check) else 1
    except (OSError, tomllib.TOMLDecodeError, ValueError) as exc:
        print(f"session Markdown render failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
