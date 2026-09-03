---
name: interview-review-manager
description: "Manage an Obsidian interview-preparation vault by linking interview questions to exact knowledge or project blocks, detecting answer gaps, adding indexing metadata, maintaining a compact source-traceable review center, generating active-recall plans, conducting tracked drills, and auditing progress. Use for 面试知识链接整理、复盘吸收、写入或更新复习中心、薄弱点整理、复习计划、闭卷测试、模拟面试复测或知识库复习管理; do not use for ordinary technical Q&A, incidental file reading, or a general mock interview unless link or review tracking is requested."
---

# Interview Review Manager

Turn scattered interview reviews into a source-traceable knowledge graph and a small, executable review queue. Every tracked item must lead back to the exact interview question and forward to an intent-appropriate canonical knowledge block, project block, expression block, or an explicit answer-gap marker.

## Locate the vault

Treat the current workspace as the vault when it contains `00-导航`, `01-知识库`, and `04-模拟面试`. Otherwise locate the intended vault from user context or ask for its path before writing.

Use these roles:

- `00-导航/复习中心.md`: compact source of truth for weak topics, scheduling, and review history; it embeds, but does not duplicate, today's checklist from `当前任务.md`.
- `00-导航/当前任务.md`: the only source of truth for current day or week checklist actions.
- `01-知识库`: canonical interview fundamentals and reusable 八股 explanations.
- `02-项目库`: a peer of `01-知识库`, containing canonical internship/project facts, implementations, decisions, metrics, incidents, and project-specific answers. Project material does not need to be duplicated into `01-知识库` merely because it contains a reusable technical mechanism.
- `03-真实面试` and `04-模拟面试`: source evidence; preserve by default.
- `05-简历与表达`: canonical self-introduction, behavioral, motivation, and communication answers.
- `06-计划与状态`: longer-term direction, not the daily queue.

Before initializing or changing the review system, generating a schedule, scoring a drill, or running a weekly audit, read [references/review-system.md](references/review-system.md) and use its quick navigation to load the relevant section. Before adding or repairing links, adding anchors, classifying answer destinations, marking an answer gap, or changing note Properties, read [references/linking-and-metadata.md](references/linking-and-metadata.md) and use its quick navigation to load the relevant section.

## Choose the operating mode

Infer the mode from the request. Link organization is triggered when the user asks to整理面试知识链接、关联题目与知识库、检查未链接题目, or when an item will be written to `复习中心.md`. If several modes are requested, run them in this order: organize links, ingest, plan, drill, audit.

### Organize interview knowledge links

Use when the user asks to organize or repair links, or as a required sub-step before adding an item to the review center.

1. Read the named interview review and the existing review center. Search `01-知识库`, `02-项目库`, and when relevant `05-简历与表达` by filenames and headings; read only plausible candidate notes or sections.
2. Identify each interview question and ensure it has a stable exact target. Prefer a unique question heading; add a stable block ID only when the heading is missing, duplicated, or likely to change.
3. Classify by the question's interview intent, not by whether individual words sound reusable: standalone fundamentals/八股 go to `01-知识库`; questions framed around the user's internship, project, implementation, metrics, incidents, or ownership go to `02-项目库`; use `mixed` only when the question genuinely requires both a standalone principle and project application to be complete. The two libraries are peers, and a resolved project answer is not a knowledge-library gap.
4. Add vault-relative Obsidian links with useful aliases according to the linking reference. When link enrichment was requested, add a compact `关联内容` annotation to the question without rewriting its original wording, answer, score, or feedback.
5. A missing link is not automatically a missing concept. Distinguish an existing-but-unlinked answer, an ambiguous candidate, and a genuinely missing answer. Record unresolved cases explicitly.
6. Add or merge indexing metadata only for notes actually semantically classified or link-enriched by this operation. Incidental reads do not count as indexing.
7. Make the operation idempotent: reuse existing anchors and annotations, merge equivalent links, and never append a duplicate merely because the skill is run again.
8. Validate every link and anchor added by the task.

### Ingest a review

Use when the user asks to absorb,整理,汇总, or update from one or more interview reviews.

1. Read only the named/new reviews plus the existing review center. For a first-time initialization, scan all relevant reviews when the user requests a full baseline.
2. Extract questions, scores, feedback, repeated failures, improvements, and recommended actions. Run the link-organization rules for every item that will enter the review center.
3. Normalize each issue into a stable topic. Update an existing compact item when the concept is equivalent; do not create synonyms as separate weaknesses.
4. Assign priority, status, and action using the reference rules. Assign a next-review date only when the latest closed-book attempt date is evidenced; otherwise record `待安排`, never the indexing date as a substitute.
5. Update `复习中心.md`. Every compact topic item must contain an exact source-question link and either one or more exact answer links or an explicit missing/ambiguous marker with a proposed destination.
6. When a usable answer exists only inside an interview review, mark it `source-only`, link that exact temporary answer block, and propose the intent-appropriate canonical destination. Do not default that destination to `01-知识库`, and do not misclassify it as fully linked or fully missing.
7. Do not create or expand a canonical answer note unless the user also asks for knowledge consolidation. If requested, create only the smallest useful canonical block first; never present an AI-generated note as learned knowledge.
8. For a full baseline, process one named company/specialty directory or a bounded group of files at a time. Complete and validate each file before marking it indexed; report a resumable summary after every batch.

### Generate a daily plan

Use when the user asks what to study today or requests a time-bounded review plan.

1. Read the existing `00-导航/当前任务.md` before planning. Reconcile its prior `## 今日任务`: completed checkboxes are execution evidence only, while unchecked P0/P1 tasks return to the candidate pool without duplication.
2. Select due items first, then overdue P0/P1 items, then one maintenance item from a demonstrated strength when time allows.
3. Default to 30–45 minutes and at most three tasks: up to two weak topics plus one optional maintenance item. A due date means the item is eligible for selection, not that every due item must appear today. When an unchecked task is repeatedly carried over, shrink it to a smaller active-recall action rather than copying an ever-growing task.
4. Every task must state the topic, active-recall action, time box, and pass criterion. “Read/review this whole file” is not an acceptable task.
5. Update only the stable `## 今日任务` section when the user asks for a daily plan. Preserve `当前方向`, `计划入口`, `本周任务`, and all unrelated sections. Daily tasks must be Markdown checkboxes (`- [ ]`), never a table.
6. Every task must link to the exact source question. Add answer links as indented post-recall checks when they exist; keep `source-only`, partial, ambiguous, and missing answers visibly marked.
7. Ensure `复习中心.md` contains exactly one `![[当前任务#今日任务]]` embed under its `## 今日任务` heading. Never copy the checklist into both files.

### Conduct a drill

Use when the user asks to test,复测,抽查, or practice items from the review center. This complements an interview-simulator skill: use this skill for targeted remediation and tracking, not for a fresh general interview.

1. Ask one question at a time and wait for the user's closed-book answer. Do not reveal the answer first.
2. Match the test to the topic: oral explanation, mechanism diagram, comparison/selection, code, project narrative, or troubleshooting chain.
3. Score the first answer with the reference rubric; state the missing mechanism or boundary precisely.
4. Allow one immediate retry after feedback when useful, but keep the original score as evidence and record the retry separately.
5. At session end, update the review log, status, and next-review date if the user requested tracked practice. Never infer mastery merely because an answer exists in the vault.

### Run a weekly audit

Use when the user asks for a weekly review, progress report, or next-week focus.

Report completed reviews, overdue items, repeated failures, improved topics, mastery candidates, and the next five priorities. Move a topic to mastered only when the reference criteria are met. Prefer revising priorities over adding more notes.

## Non-negotiable invariants

- Preserve raw and historical interview content. In an explicit link-organization or tracked-ingest request, only additive YAML Properties, stable block IDs, and compact `关联内容` annotations may be added; never rewrite the original question, answer, score, or feedback.
- Never delete, rename, or restructure the vault as a side effect of review management.
- Preserve YAML Properties and existing Obsidian links.
- Merge metadata instead of replacing existing frontmatter. Never add `last_accessed` or mutate a note merely because it was opened.
- Re-running the same operation must not duplicate block IDs, aliases, `关联内容` sections, source links, queue items, embeds, or checklist tasks.
- Do not duplicate complete answers in `复习中心.md`; link to the canonical answer.
- Do not equate reading, note existence, AI-generated content, or a checked task with mastery. A checkbox means the action was performed; only tracked closed-book performance changes mastery evidence.
- Treat `01-知识库` and `02-项目库` as peer canonical destinations. Never require duplicate notes across them to make a topic look complete.
- Prefer a small queue of stable topic clusters over one file per question or uncontrolled tags.
- When the requested change is ambiguous, provide a proposed update without writing it.

## Finish checks

After writes, verify that edited Markdown files exist; every added path, heading, and block anchor resolves; aliases inside any existing Markdown tables are escaped correctly; existing frontmatter was preserved; no historical content changed unintentionally; today's tasks are checkboxes rather than a table; and the daily queue remains small and actionable. Run `scripts/validate_obsidian_links.py` against files with added or repaired links. When `复习中心.md` or `当前任务.md` changed, also run `scripts/validate_review_system.py <vault> --require-sections`. Summarize linked questions, `source-only` answers, unresolved answer gaps, files indexed, carried-over tasks, and the next eligible item.
