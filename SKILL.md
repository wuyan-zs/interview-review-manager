---
name: interview-review-manager
description: >-
  Organize Obsidian interview reviews into linked knowledge or project answers and
  a small review queue. Use after a real/mock interview or when planning today's
  review. Do not use for conducting a standalone mock interview.
---

# Interview Review Manager

Turn an interview review or a completed mock-interview record into a traceable, small review loop. The user-facing operations are deliberately limited to these three:

1. **整理一份面试复盘** — organize one named review file or bounded folder; add precise source and answer links, then update the review center when requested.
2. **给我今天的复习任务** — create at most three active-recall checkboxes from the existing review center.
3. **导入一场模拟面试结果** — turn a completed simulator transcript/scorecard into a linked review record and review-center items.

For a weekly report, targeted closed-book retest, or knowledge consolidation, handle the natural-language request as a supporting action; do not present it as another menu choice.

## Locate the vault

Treat the current workspace as the vault when it contains `00-导航`, `01-知识库`, and `04-模拟面试`. Otherwise locate the intended vault from user context or ask for its path before writing.

The library roles are:

- `00-导航/复习中心.md`: compact source of truth for weaknesses, schedule, and review evidence; embeds today's checklist.
- `00-导航/当前任务.md`: the only source of truth for current checklist actions.
- `01-知识库`: canonical standalone interview fundamentals and reusable 八股 explanations.
- `02-项目库`: a peer of `01-知识库`; canonical project/internship facts, implementations, metrics, incidents, and project-specific answers.
- `03-真实面试` and `04-模拟面试`: source evidence; preserve by default.
- `05-简历与表达`: canonical behavioral and expression answers.

Before organizing links, classifying answers, adding anchors, marking an answer gap, or editing Properties, read [references/linking-and-metadata.md](references/linking-and-metadata.md). Before writing the review center, planning, scoring a targeted retest, or reviewing a week, read [references/review-system.md](references/review-system.md).

## 1. 整理一份面试复盘

Use for a named real/mock interview review, or before adding its items to the review center.

1. Work on the named file or bounded directory only. A full-vault baseline requires an explicit request.
2. For one named file, use the fast path by default: inventory headings and question cues first, then search candidate filenames/headings/aliases once per topic cluster. Do not read every large canonical note in full; open only the sections needed to verify a proposed link. Reuse one candidate search for repeated questions.
3. Detect semantic question units, not one rigid template. Recognize headings such as `问题`, `面试官题目`, `Q1`, numbered questions, and a handbook pattern such as `问题 → 完整答案 → 记忆要点`. Treat each question heading plus its answer/feedback until the next question or section as one unit. If a file is a handbook, guide, or knowledge supplement rather than a scored review, preserve its type and do not require interview-date or score fields.
4. Give each question a stable exact target. Prefer its full unique heading even when the heading is long. Add a visible block ID only when there is no safe heading target, headings are actually duplicated/unstable, or the user explicitly requests block IDs. Never add an ID merely because the file is nonstandard.
5. Route by the question's intent: standalone 八股 → `01-知识库`; project/internship implementation, ownership, metrics, incident, or trade-off → `02-项目库`; behavioral → `05-简历与表达`; use both only for a genuinely mixed question.
6. Search filenames, headings, aliases, and distinctive terms in both peer libraries before declaring a gap. Add vault-relative links and compact `关联内容` annotations for every confidently matched in-scope question, without changing original questions, answers, scores, or feedback.
7. Apply the fallback in [references/linking-and-metadata.md](references/linking-and-metadata.md#nonstandard-note-fallback). When a question unit is confidently detected but its answer destination is not, still add the label `**关联内容：**` immediately below the question with a plain-language status and a proposed destination; never create a guessed/broken wiki link. If the question boundary itself is uncertain, leave the source unchanged and show a preview with the suspected range and reason.
8. Distinguish `linked`, `source-only`, `partial`, `ambiguous`, `missing`, and `unlinked`.
9. If a named file contains more than 12 question units, show an inventory and process it in resumable batches of about 6–8 units unless the user explicitly requests one uninterrupted pass. Finish and validate each batch before starting the next; do not silently scan the whole vault.
10. For `partial`, `missing`, or `ambiguous` answer content, default to proposal-only: explain the exact gap, suggested destination, and smallest draft or patch, but do not create or edit a canonical knowledge/project answer until the user explicitly confirms. A request to organize or import permits source annotations and review-center markers, not unapproved canonical content. Project facts, responsibilities, metrics, and incidents require the user's confirmation.
11. If the user asked to update the review center, merge each weakness into one stable topic item with exact source-question and answer links. Do not copy whole answers into the center.
12. Add or merge indexing metadata only for notes actually classified or link-enriched. Validate every link and anchor.

## 2. 给我今天的复习任务

Use for a time-bounded plan. Read the existing `00-导航/当前任务.md` first.

- Default to 30–45 minutes and at most three tasks: due items first, then overdue P0/P1, then an optional maintenance item.
- Write only Markdown checkboxes under `## 今日任务`; preserve unrelated sections.
- Each task starts with an exact source-question link, states an active-recall action, time box, and pass criterion. Put answer links beneath it as post-answer checks.
- Keep one `![[当前任务#今日任务]]` embed in `复习中心.md`; never duplicate the checklist there.

## 3. 导入一场模拟面试结果

Use after a simulator has completed its session. This skill does not need to call the simulator directly: it receives the saved transcript or scorecard and makes it useful in the vault.

1. Read [references/simulator-handoff.md](references/simulator-handoff.md).
2. Save or locate the session under `04-模拟面试`, preserving the simulator's original questions, responses, scores, and feedback as source evidence.
3. Apply the same link-routing and answer-status rules as operation 1.
4. Record the *first-answer* score and an evidenced session date when supplied. Do not invent dates or treat an immediate retry as mastery.
5. Add only genuine weaknesses to the review center; strong topics are maintenance candidates, not automatic queue entries. If the import reveals `partial` or `missing` canonical content, follow the proposal-only rule in operation 1 rather than silently writing a new answer.

## Shared safeguards

- Preserve raw/historical interview content. In an explicit organizing or importing request, only additive YAML Properties, block IDs, and compact `关联内容` annotations may be added.
- Never delete, rename, or restructure vault files as a side effect.
- Merge existing YAML and Obsidian links; never add `last_accessed` merely because a note was read.
- Re-running must not duplicate IDs, annotations, links, queue items, embeds, or checklist tasks.
- A checked task means an action was performed, not that the topic is mastered. Only tracked closed-book performance changes mastery evidence.
- `01-知识库` and `02-项目库` are peer destinations; a resolved project answer does not require a duplicate general knowledge note.
- When the requested write is ambiguous, show a proposed update rather than writing it.

## Finish checks

After writes, run `scripts/validate_obsidian_links.py` for files with added links. When `复习中心.md` or `当前任务.md` changed, also run `scripts/validate_review_system.py <vault> --require-sections`. Summarize linked questions, source-only answers, unresolved gaps, indexed files, carried-over tasks, and the next eligible item.
