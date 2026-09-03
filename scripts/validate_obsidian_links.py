#!/usr/bin/env python3
"""Read-only validation for Obsidian wiki links in a vault or selected scopes."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


WIKILINK_RE = re.compile(r"!?\[\[([^\[\]]+)\]\]")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$")
BLOCK_ID_RE = re.compile(r"(?:^|\s)\^([A-Za-z0-9-]+)\s*$")
FENCE_RE = re.compile(r"^\s*(```+|~~~+)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
HIDDEN_DIRS = {".git", ".obsidian", ".trash"}


@dataclass(frozen=True)
class Issue:
    source: Path
    line: int
    kind: str
    detail: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def markdown_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.md")
        if not any(part in HIDDEN_DIRS for part in path.relative_to(root).parts)
    )


def vault_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and not any(part in HIDDEN_DIRS for part in path.relative_to(root).parts)
    )


def scoped_files(root: Path, scopes: list[str]) -> list[Path]:
    if not scopes:
        return markdown_files(root)

    result: set[Path] = set()
    for raw_scope in scopes:
        candidate = (root / raw_scope).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"scope escapes vault: {raw_scope}") from exc
        if not candidate.exists():
            raise ValueError(f"scope does not exist: {raw_scope}")
        if candidate.is_dir():
            result.update(
                path
                for path in candidate.rglob("*.md")
                if not any(part in HIDDEN_DIRS for part in path.relative_to(root).parts)
            )
        elif candidate.suffix.lower() == ".md":
            result.add(candidate)
        else:
            raise ValueError(f"scope is not a Markdown file or directory: {raw_scope}")
    return sorted(result)


def visible_lines(text: str):
    fence_marker: str | None = None
    for number, line in enumerate(text.splitlines(), start=1):
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)[0]
            if fence_marker is None:
                fence_marker = marker
            elif fence_marker == marker:
                fence_marker = None
            continue
        if fence_marker is None:
            yield number, INLINE_CODE_RE.sub("", line)


def normalize_heading(value: str) -> str:
    value = re.sub(r"\s+#+\s*$", "", value.strip())
    value = value.replace("**", "").replace("__", "")
    value = value.replace("`", "").replace("*", "").replace("_", "")
    return re.sub(r"\s+", " ", value).strip().casefold()


def note_index(path: Path) -> tuple[set[str], Counter[str]]:
    headings: set[str] = set()
    block_ids: Counter[str] = Counter()
    for _, line in visible_lines(read_text(path)):
        heading = HEADING_RE.match(line)
        if heading:
            headings.add(normalize_heading(heading.group(1)))
        block = BLOCK_ID_RE.search(line)
        if block:
            block_ids[block.group(1).casefold()] += 1
    return headings, block_ids


def split_link(raw: str) -> tuple[str, str | None]:
    if r"\|" in raw:
        target, alias = raw.split(r"\|", 1)
    elif "|" in raw:
        target, alias = raw.split("|", 1)
    else:
        target, alias = raw, None
    return target.strip(), alias.strip() if alias else None


def resolve_note(
    root: Path,
    source: Path,
    path_part: str,
    by_stem: dict[str, list[Path]],
    by_name: dict[str, list[Path]],
) -> tuple[Path | None, str | None]:
    if not path_part:
        return source, None

    cleaned = path_part.replace("\\", "/").strip("/")
    if "/" not in cleaned:
        cleaned_path = Path(cleaned)
        if cleaned_path.suffix and cleaned_path.suffix.lower() != ".md":
            matches = by_name.get(cleaned_path.name.casefold(), [])
        else:
            matches = by_stem.get(cleaned_path.stem.casefold(), [])
        if len(matches) == 1:
            return matches[0], None
        if len(matches) > 1:
            choices = ", ".join(str(path.relative_to(root)) for path in matches[:5])
            return None, f"ambiguous filename-only target '{path_part}': {choices}"

    relative = Path(cleaned)
    if not relative.suffix:
        relative = relative.with_suffix(".md")
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None, f"target escapes vault: {path_part}"
    if candidate.exists():
        return candidate, None
    return None, f"missing target file: {path_part}"


def validate(root: Path, sources: list[Path]) -> tuple[list[Issue], int]:
    all_notes = markdown_files(root)
    by_stem: dict[str, list[Path]] = defaultdict(list)
    by_name: dict[str, list[Path]] = defaultdict(list)
    indexes: dict[Path, tuple[set[str], Counter[str]]] = {}
    for vault_file in vault_files(root):
        by_name[vault_file.name.casefold()].append(vault_file)
    for note in all_notes:
        by_stem[note.stem.casefold()].append(note)
        indexes[note] = note_index(note)

    issues: list[Issue] = []
    links_checked = 0

    for source in sources:
        source_headings, source_blocks = indexes[source]
        for block_id, count in source_blocks.items():
            if count > 1:
                issues.append(Issue(source, 0, "duplicate-block-id", f"^{block_id} occurs {count} times"))

        for line_number, line in visible_lines(read_text(source)):
            for match in WIKILINK_RE.finditer(line):
                raw_target, _ = split_link(match.group(1))
                if not raw_target:
                    issues.append(Issue(source, line_number, "empty-link", match.group(0)))
                    continue

                if "#" in raw_target:
                    path_part, anchor = raw_target.split("#", 1)
                else:
                    path_part, anchor = raw_target, None

                target, error = resolve_note(root, source, path_part, by_stem, by_name)
                links_checked += 1
                if error:
                    issues.append(Issue(source, line_number, "target", error))
                    continue
                if target is None or not anchor or target.suffix.lower() != ".md":
                    continue

                headings, block_ids = indexes[target]
                if anchor.startswith("^"):
                    block_id = anchor[1:].casefold()
                    count = block_ids.get(block_id, 0)
                    if count == 0:
                        issues.append(Issue(source, line_number, "anchor", f"missing block ^{anchor[1:]} in {target.relative_to(root)}"))
                    elif count > 1:
                        issues.append(Issue(source, line_number, "anchor", f"duplicate block ^{anchor[1:]} in {target.relative_to(root)}"))
                elif normalize_heading(anchor) not in headings:
                    issues.append(Issue(source, line_number, "anchor", f"missing heading '{anchor}' in {target.relative_to(root)}"))

    return issues, links_checked


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Obsidian wiki-link files and anchors without editing the vault.")
    parser.add_argument("vault", help="Path to the Obsidian vault root")
    parser.add_argument("--scope", action="append", default=[], help="Vault-relative Markdown file or directory; repeat as needed")
    args = parser.parse_args()

    root = Path(args.vault).expanduser().resolve()
    if not root.is_dir():
        print(f"error: vault is not a directory: {root}", file=sys.stderr)
        return 2

    try:
        sources = scoped_files(root, args.scope)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    issues, links_checked = validate(root, sources)
    for issue in issues:
        location = str(issue.source.relative_to(root))
        if issue.line:
            location += f":{issue.line}"
        print(f"{location}: {issue.kind}: {issue.detail}")

    print(f"Checked {links_checked} wiki links in {len(sources)} Markdown files; issues: {len(issues)}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
