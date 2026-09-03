#!/usr/bin/env python3
"""Read-only validation for the compact interview review-center and daily-task format."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^\s*(```+|~~~+)")
TOPIC_RE = re.compile(r"^- \*\*(.+?)\*\*(?:\s|$)")
TASK_RE = re.compile(r"^- \[[ xX]\] \[\[")
SOURCE_RE = re.compile(r"^\s{2,}-\s*题目：\s*!?\[\[")
ANSWER_RE = re.compile(r"^\s{2,}-\s*核对：\s*!?\[\[")
GAP_RE = re.compile(r"\b(?:source-only|partial|ambiguous|missing)\b")


@dataclass(frozen=True)
class Issue:
    path: Path
    line: int
    detail: str


def read_visible_lines(path: Path) -> list[tuple[int, str]]:
    fence_marker: str | None = None
    lines: list[tuple[int, str]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8-sig", errors="replace").splitlines(), start=1):
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)[0]
            if fence_marker is None:
                fence_marker = marker
            elif fence_marker == marker:
                fence_marker = None
            continue
        if fence_marker is None:
            lines.append((number, line))
    return lines


def section(lines: list[tuple[int, str]], name: str) -> list[tuple[int, str]] | None:
    start: int | None = None
    for index, (_, line) in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        title = re.sub(r"\s+#+\s*$", "", match.group(2)).strip()
        if start is None and level == 2 and title == name:
            start = index + 1
            continue
        if start is not None and level <= 2:
            return lines[start:index]
    return lines[start:] if start is not None else None


def issue(issues: list[Issue], path: Path, line: int, detail: str) -> None:
    issues.append(Issue(path, line, detail))


def validate_review_center(path: Path, require_sections: bool) -> tuple[list[Issue], int]:
    lines = read_visible_lines(path)
    issues: list[Issue] = []
    checks = 0

    embeds = [(number, line) for number, line in lines if "![[当前任务#今日任务]]" in line]
    checks += 1
    if len(embeds) != 1:
        issue(issues, path, 0, f"expected exactly one ![[当前任务#今日任务]] embed; found {len(embeds)}")

    queue = section(lines, "待加强")
    checks += 1
    if queue is None:
        if require_sections:
            issue(issues, path, 0, "missing ## 待加强 section")
        return issues, checks

    topic_positions = [(index, number, match.group(1).strip()) for index, (number, line) in enumerate(queue) if (match := TOPIC_RE.match(line))]
    seen: set[str] = set()
    for position, line_number, topic in topic_positions:
        checks += 1
        normalized = re.sub(r"\s+", " ", topic).casefold()
        if normalized in seen:
            issue(issues, path, line_number, f"duplicate normalized topic: {topic}")
        seen.add(normalized)

        next_position = next((other for other, _, _ in topic_positions if other > position), len(queue))
        children = queue[position + 1 : next_position]
        has_source = any(SOURCE_RE.match(line) for _, line in children)
        has_answer = any(ANSWER_RE.match(line) for _, line in children)
        has_gap = any(GAP_RE.search(line) for _, line in children)
        has_proposal = any("建议：" in line for _, line in children)

        checks += 2
        if not has_source:
            issue(issues, path, line_number, f"topic '{topic}' lacks an indented 题目：[[...]] source link")
        if not has_answer and not (has_gap and has_proposal):
            issue(issues, path, line_number, f"topic '{topic}' lacks 核对：[[...]] or an answer-gap marker plus 建议：")

    return issues, checks


def validate_daily_tasks(path: Path, require_sections: bool) -> tuple[list[Issue], int]:
    lines = read_visible_lines(path)
    issues: list[Issue] = []
    checks = 0
    daily = section(lines, "今日任务")
    checks += 1
    if daily is None:
        if require_sections:
            issue(issues, path, 0, "missing ## 今日任务 section")
        return issues, checks

    tasks = [(number, line) for number, line in daily if line.startswith("- [")]
    checks += 1
    if len(tasks) > 3:
        issue(issues, path, 0, f"daily queue has {len(tasks)} checklist tasks; maximum is 3")
    for line_number, line in tasks:
        checks += 1
        if not TASK_RE.match(line):
            issue(issues, path, line_number, "task must start with '- [ ]' or '- [x]' followed by an exact [[source question]] link")
    return issues, checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate compact interview review-center and daily-task structure without editing the vault.")
    parser.add_argument("vault", help="Path to the Obsidian vault root")
    parser.add_argument("--review-center", default="00-导航/复习中心.md", help="Vault-relative review-center path")
    parser.add_argument("--current-tasks", default="00-导航/当前任务.md", help="Vault-relative current-task path")
    parser.add_argument("--require-sections", action="store_true", help="Treat missing required sections in existing dashboard files as errors")
    args = parser.parse_args()

    root = Path(args.vault).expanduser().resolve()
    if not root.is_dir():
        print(f"error: vault is not a directory: {root}", file=sys.stderr)
        return 2

    issues: list[Issue] = []
    checks = 0
    checked_files = 0
    for raw_path, validator in ((args.review_center, validate_review_center), (args.current_tasks, validate_daily_tasks)):
        path = (root / raw_path).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            print(f"error: path escapes vault: {raw_path}", file=sys.stderr)
            return 2
        if not path.exists():
            print(f"Skipped missing optional file: {raw_path}")
            continue
        if not path.is_file():
            print(f"error: path is not a file: {raw_path}", file=sys.stderr)
            return 2
        file_issues, file_checks = validator(path, args.require_sections)
        issues.extend(file_issues)
        checks += file_checks
        checked_files += 1

    for item in issues:
        location = str(item.path.relative_to(root))
        if item.line:
            location += f":{item.line}"
        print(f"{location}: review-system: {item.detail}")
    print(f"Checked {checks} review-system rules in {checked_files} Markdown files; issues: {len(issues)}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
