# Review system rules

Read this reference whenever creating or updating the review center, scheduling practice, scoring answers, or auditing progress.

## 快速导航

- 初始化或更新 `复习中心.md`：阅读 [`00-导航/复习中心.md` format](#00-导航复习中心md-format) 和 [Ingest update rules](#ingest-update-rules)。
- 生成今天的 checklist：阅读 [Daily task format](#daily-task-format) 和 [Regenerating the daily plan](#regenerating-the-daily-plan)。
- 计算优先级、状态或复习日期：阅读 [Priority](#priority)、[Evidence-first scoring fallback](#evidence-first-scoring-fallback)、[Status](#status) 和 [Scheduling](#scheduling)。
- 闭卷复测或周度审计：阅读 [Mastery evidence](#mastery-evidence)、[Scoring rubric](#scoring-rubric) 和 [Active-recall action by topic](#active-recall-action-by-topic)。
- 写入 `复习中心.md` 或 `当前任务.md` 后：阅读 [复习系统校验器](#复习系统校验器)。

不要为了单一模式加载或套用其他模式的格式规则。

## Stable topic taxonomy

Normalize weaknesses into the smallest stable cluster that remains useful across interviews. Prefer these domains for this vault:

- C++ concurrency: condition variables, wakeups, locks, thread pools, shared state, atomics.
- C++ object model and ownership: virtual dispatch, multiple inheritance, RAII, smart pointers, move semantics, special member functions.
- STL and memory: containers, iterator invalidation, allocation, stack/heap, `new`/`delete`.
- Linux and networking: epoll, Reactor, TCP states, RST, mmap, writev, timers.
- Debugging and performance: ASan, GDB/core, Valgrind, perf, P99 diagnosis.
- AI inference: TensorRT, precision, quantization, calibration, context pools, memory budgets.
- Edge deployment: RGA, DMA-BUF, fences, cache coherence, NPU scheduling.
- Project communication: scope, trade-offs, ownership, metrics, troubleshooting narrative.
- Automotive domain: ADAS, vehicle-grade constraints, production trade-offs, industry understanding.
- Coding execution: correctness, naming consistency, bounds, returns, cleanup, compilation and tests.

Keep distinct mechanisms separate when they need different practice. For example, virtual wakeups and lost wakeups share a parent topic but must not be treated as the same mechanism. Treat common abbreviations and name variants such as TRT/TensorRT or rule of five/三五法则 as the same topic.

## Priority

- `P0`: repeated failure with latest score below 6; or a role-critical topic with a score of 0–3 or an explicit blank.
- `P1`: one failure below 6; a score of 6–7 needing consolidation; or a former P0 that improved only once.
- `P2`: stable score of at least 8, low-frequency/low-relevance material, or maintenance-only strengths.
- `待评估`: there is not yet comparable performance evidence. This is a routing state, not a score and not an urgency claim.

When evidence conflicts, role relevance and recent closed-book performance matter more than document length or how often an answer appears in notes.

## Evidence-first scoring fallback

评分不是复盘的必填字段。先判断来源中到底有什么证据，再决定是否能产生优先级和日期；不要为了填满模板而补一个数字。

Classify the evidence for each topic into one of these modes:

- `explicit-score`: the source explicitly gives a score and scale, such as `4/10`, `B-`, or `3/5`. Preserve the raw value and scale exactly. Apply the numeric rubric and interval rules only when the scale is explicitly `0–10`; do not silently normalize `3/5` or a letter grade to `/10`.
- `explicit-label`: the source gives a label such as `通过`, `需加强`, or `不合格`, but no declared mapping. Preserve the label verbatim. Map it to P0/P1/P2 only when the simulator/user has supplied a stable mapping; otherwise use `待评估`.
- `qualitative-evidence`: the source describes what happened without a score, for example “明确答不上来”“核心机制讲反”“能答主线但追问断掉”. Preserve a short faithful evidence note; never reverse-engineer a number from the wording.
- `unassessed`: the source has a question but no answer-quality evidence, score, or feedback. Do not call it a failure. Use `首答：未量化` and `面试证据：未记录`, and keep it out of the weakness queue unless the user explicitly asks for a diagnostic.
- `conflict`: score, label, and prose disagree, or two attempts use incompatible scales. Stop automatic score/date updates, show the conflicting raw evidence, and request confirmation.

Use the following conservative mapping when there is no numeric score:

- An explicit blank, fundamental error, or “无法回答” on a role-critical topic → `P0 · learning`.
- One clearly documented mechanism gap or failed follow-up without a score → `P1 · learning` (raise to P0 only when the source says it is repeated or role-critical and severe).
- No performance evidence → `待评估 · new`; no review interval is implied.
- A qualitative strength without a score is not evidence for `P2`; keep it as a maintenance candidate only when the topic is role-critical.

Review-center examples:

```markdown
- **ARM 微架构与 Linux 调度** · P0 · learning · 首答：未量化 · 面试证据：明确答不上来 · 下次：待安排
  - 题目：[[03-真实面试/卓驭/卓驭-一面复盘#十、平台、芯片、ARM 架构与操作系统|卓驭一面·ARM与调度]]
  - 核对：待补充（missing） · 建议：`01-知识库/操作系统/ARM微架构与Linux调度`

- **反问准备** · 待评估 · new · 首答：未量化 · 面试证据：未记录
  - 题目：[[03-真实面试/卓驭/卓驭-一面复盘#十四、反问环节|卓驭一面·反问]]
  - 核对：待评估（没有可用作答证据）
```

`首答：未量化` means only that no comparable score was supplied; it does not mean zero. `面试证据：未记录` means the source is silent; it must not be rewritten as “答不上来”.

## Status

- `new`: newly discovered and not yet remediated.
- `learning`: answer/mechanism is incomplete or latest score is below 6.
- `consolidating`: latest score is 6–7 or one successful retry exists.
- `mastered`: mastery criteria below are satisfied.
- `parked`: intentionally deferred because relevance is low.

## Scheduling

Use the latest evidenced closed-book first-attempt score and its evidenced attempt date:

- 0–5: review the next day.
- 6–7: review after 3 days.
- 8–10: review after 7–14 days.
- After two qualifying passes: maintenance after 30 days or before a relevant interview.

These intervals are default heuristics, not observed facts about the user. A calculated date is the earliest eligible review date, not a hard deadline.

- Use an explicit interview/review date, tracked drill date, or a date confirmed by the user as the base date.
- Never use `indexed_at`, file modification time, or the current date as a substitute for an unknown attempt date.
- When the score exists but its attempt date is unknown, record `待安排`; if generating today's plan, the item may still be selected by priority without fabricating a historical date.
- When the score is absent or the scale is not comparable, do not calculate a next-review interval. For a documented weakness use `下次：待安排`; for `待评估` use no date or `下次：待评估`. A today's-plan item in this state must be a `闭卷诊断`, whose result establishes the first comparable evidence.
- If the user supplies a deadline, compress intervals while preserving at least one delayed retrieval attempt.
- Do not schedule every known topic on the same day. Daily capacity wins over the number of due items.

## Mastery evidence

Mark mastered only when all applicable conditions hold:

1. Two closed-book first-attempt scores are at least 8.
2. The attempts are at least 3 days apart unless an imminent interview forces a disclosed compressed schedule.
3. The user handles at least one follow-up, boundary, or trade-off question.
4. A coding topic is written without the answer and passes a basic compile/test or a careful trace when execution is unavailable.

An immediate retry measures correction, not durable mastery.

## Scoring rubric

Apply this rubric only to an explicitly established 0–10 score. It is not a translation table for prose, letter grades, pass/fail labels, or another scale.

- 0–2: blank, unrelated, or fundamental model is wrong.
- 3–4: recognizes the topic but misses the core mechanism or reverses a key conclusion.
- 5–6: main direction is correct, with important gaps, boundaries, or implementation errors.
- 7–8: correct and usable answer with minor omissions; 8 requires a coherent mechanism and at least one boundary/example.
- 9–10: precise, structured, handles trade-offs and follow-ups, and connects correctly to project evidence where relevant.

Score the user's first closed-book answer. Do not score the model answer or copied notes.

## Active-recall action by topic

- Concept/mechanism: 30–90 second closed-book explanation.
- Concurrency: draw a time line or state transition, then explain the race boundary.
- Comparison/selection: reconstruct a table and choose under a concrete constraint.
- Coding: write, compile/test or trace, then run a fixed checklist for bounds, returns, cleanup, and requirements.
- Project: deliver a 3-minute narrative covering context, ownership, decision, trade-off, result, and follow-up.
- Troubleshooting: answer as symptom → hypotheses → evidence/tools → root cause → fix → verification.
- Performance/data: reproduce the metric, measurement method, baseline, result, and limitation.

## `00-导航/复习中心.md` format

Create this file only when missing and the user asks to initialize or use tracked review management.

```markdown
---
type: review-dashboard
updated: YYYY-MM-DD
---

# 复习中心

## 今日任务

![[当前任务#今日任务]]

## 待加强

- **线程池优雅退出** · P0 · learning · 首答 4/10 · 下次：YYYY-MM-DD
  - 题目：[[04-模拟面试/复盘#^q-id|某次模拟·Q1]]
  - 核对：[[01-知识库/知识页#标题|线程池标准答案]]

## 已掌握

- **示例主题** · 最近两次 8/10、9/10 · 维护：YYYY-MM-DD
  - 答案：[[01-知识库/知识页#标题|标准答案]]

## 复习记录

- YYYY-MM-DD · 线程池优雅退出 · 首答 4/10 · 重答 7/10 · 仍缺失：退出边界 · 下次：YYYY-MM-DD
```

Rules:

- `复习中心.md` embeds `![[当前任务#今日任务]]` exactly once. The checklist itself lives only in `当前任务.md`.
- One compact list item per normalized topic. Add multiple source links to the same item instead of duplicating it.
- Keep only decision-useful state on the first line: topic, priority/status, evidenced latest score or an explicit scoreless marker, and next eligible date when known. For scoreless evidence use `首答：未量化`, `评分尺度：未知`, `面试证据：...`, or `待评估`; never use a made-up numeric placeholder. Never write a calculated date without a valid base date and comparable score; `下次：待安排`/`下次：待评估` are explicit non-dates and are allowed when they clarify the next action.
- Do not display domain/type when the destination links already make it obvious. Preserve those classifications internally while processing.
- `核对` points to exact canonical headings or blocks when possible. If an answer exists only in a review, show `临时答案（source-only）` with its exact link and an intent-appropriate proposed destination. Otherwise show a concise `partial`, `ambiguous`, or `missing` marker; do not silently create a large new note.
- `题目` is mandatory and links to the exact interview question heading or block. Add multiple aliased source links under the same topic when it recurs.
- Keep full explanations and detailed task instructions out of the review center; they belong in canonical notes and `当前任务.md` respectively.
- Update the top-level `updated` date whenever the queue changes.

## Daily task format

Use this stable structure for `00-导航/当前任务.md`. Merge or normalize its Properties when generating a plan, but preserve unrelated existing Properties and body sections.

```markdown
---
type: daily-plan
date: YYYY-MM-DD
updated: YYYY-MM-DD
---

# 当前任务

## 今日任务

- [ ] [[04-模拟面试/某次复盘#^q-thread-pool|某次模拟·线程池题]]：闭卷默写 shutdown、notify_all、join（15 分钟；通过标准：代码可正确退出且能解释三种并发风险）
  - 回答后核对：[[01-知识库/C++并发/线程池#优雅退出|线程池标准答案]]
```

Each task must start with an exact source-question link. Daily tasks are always Markdown checkboxes; never render the daily plan as a table.

### Regenerating the daily plan

Before replacing the contents of `## 今日任务`:

1. Read the existing section.
2. Treat `[x]` as action completion only. Do not change topic score or mastery unless a tracked closed-book result exists.
3. Return unchecked due P0/P1 tasks to the candidate pool, deduplicate them by normalized topic plus source question, and carry over only those still selected within the three-task limit.
4. If the same task was repeatedly left unfinished, reduce it to a smaller testable action.
5. Replace only the `## 今日任务` body. Preserve `## 当前方向`, `## 计划入口`, `## 本周任务`, and any other unrelated sections.
6. Use one stable `## 今日任务` heading so `![[当前任务#今日任务]]` continues to resolve.

For a weekly request, update `## 本周任务` separately; do not silently replace the daily section.

Avoid vague tasks such as `复习线程池`, `看看知识手册`, or `阅读这篇文档`.

## 复习系统校验器

After changing `00-导航/复习中心.md` or `00-导航/当前任务.md`, run:

```powershell
py scripts/validate_review_system.py "C:\path\to\vault" --require-sections
```

The validator is read-only. It checks:

- exactly one `![[当前任务#今日任务]]` embed in an existing review center;
- one compact item per normalized topic, with an exact `题目` link and either a `核对` link or an explicit answer-gap marker plus `建议`;
- a single `## 今日任务` section, no more than three top-level checkboxes, and an exact source link at the start of each task.

Without `--require-sections`, it skips a dashboard file or section that has not yet been initialized; use that mode only to inspect a partially initialized vault. Run `scripts/validate_obsidian_links.py` separately whenever links or anchors changed; this script checks structure, not whether targets resolve.

## Ingest update rules

For each extracted weakness:

1. Search the review center for the canonical topic and common synonyms.
2. Extract the raw evidence mode and value before updating anything. If found, update only an evidenced score/label on a compatible scale, the evidence note, status, priority, and next eligible date when its base date is known; append the new source link. Never replace an explicit score with an estimate or compare incompatible scales.
3. If not found, add one compact item using a stable topic name.
4. Preserve improvement history in the review log; do not replace a low first-attempt score with an immediate corrected score. A scoreless event records its evidence mode and wording instead of a number.
5. When a review reports a demonstrated strength, add it only as a maintenance item if it is role-critical. Do not flood the queue with strengths.
6. If an answer exists only in the review itself, record it as `source-only`, link its exact answer block temporarily, and propose the destination selected from the question's intent. Project answers do not need a duplicate knowledge note.
7. A question with no score is not automatically a weakness. Add it to the review center only when the source contains an explicit gap or the user asks to establish a baseline; otherwise add source links/annotations only. If a baseline is requested, mark it `待评估 · new` and create a diagnostic task rather than a spaced-review task.
