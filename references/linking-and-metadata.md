# Obsidian linking and metadata rules

Read this reference before organizing interview links, adding source anchors, deciding between knowledge and project notes, marking missing answers, or adding note Properties.

## 快速导航

- 判断链接应该落在知识库、项目库还是表达库：阅读 [Classify the answer destination](#classify-the-answer-destination)。
- 新增或修复 Obsidian 链接与题目定位：阅读 [Canonical link syntax](#canonical-link-syntax) 和 [Source anchors](#source-anchors)。
- 给复盘题目增加关联内容：阅读 [Source-note enrichment](#source-note-enrichment)。
- 判断已链接、临时答案或真正缺口：阅读 [Determine answer status before declaring an answer gap](#determine-answer-status-before-declaring-an-answer-gap)。
- 添加 YAML Properties：阅读 [Metadata policy](#metadata-policy)。
- 写入复习中心或当前任务：阅读 [Review-center representation](#review-center-representation) 和 [Daily-task representation](#daily-task-representation)。
- 写完后的链接检查：阅读 [Bundled validator](#bundled-validator) 和 [Validation checklist](#validation-checklist)。

不要因为一个项目答案包含通用机制，就跳过“按题目意图分类”。

## Link contract

Every topic written to `00-导航/复习中心.md` must provide:

1. An exact link to the originating interview question.
2. An exact link to each canonical answer block that exists.
3. An explicit marker when an answer is source-only, missing, ambiguous, or only partially covered.

Every task written to `00-导航/当前任务.md` must link to its exact source question. Put answer links after the recall instruction so they function as post-answer checks rather than previews.

When the user requests interview-link organization or tracked ingestion, enrich the source question with compact `关联内容` links. Preserve the original question, answer, score, and feedback verbatim.

## Classify the answer destination

`01-知识库` and `02-项目库` are peer canonical destinations. Route by the question's interview intent, not by keywords or by whether a mechanism could theoretically be reused.

| Type | Destination | Test |
|---|---|---|
| 八股/通用知识 | `01-知识库` | The interviewer asks for a standalone concept, mechanism, comparison, language rule, or system principle independent of the user's experience. |
| 项目/实习 | `02-项目库` | The question is framed around the user's project, internship, role, implementation, measurements, constraints, incident, ownership, or trade-off. A project note may explain underlying mechanisms without creating a knowledge-library obligation. |
| Mixed | Both when needed | The question explicitly asks both a standalone principle and its project application, and neither existing destination alone answers the full intent. |
| Expression/behavioral | `05-简历与表达` | The answer is primarily self-introduction, behavioral evidence, motivation, or communication framing. |

Do not infer `mixed` merely because a project answer contains reusable technology. For example, “你在 TSR 项目中如何保证 RGA 与 NPU 的同步？” is a project question and may be fully linked to `02-项目库`, even when its answer explains DMA-BUF and fences. A separate “解释 Linux DMA-BUF 的同步机制” question is 八股 and routes to `01-知识库`. Link both only when the actual question requires both layers.

Never mark a resolved project question as `partial` or `missing` solely because `01-知识库` has no duplicate note. Likewise, a resolved 八股 question does not require a project example unless the question asks for one.

## Canonical link syntax

Use vault-relative paths, omit `.md`, target the narrowest stable heading or block, and add a short meaningful alias:

```markdown
[[01-知识库/C++/并发/条件变量#虚假唤醒与谓词检查|条件变量标准答案]]
[[02-项目库/TSR端侧部署项目/TSR部署与量化细节#DMA-BUF与RGA链路|TSR零拷贝实践]]
[[04-模拟面试/卓驭专项/06-卓驭第六轮模拟面试复盘#^q-zy-mock06-02|卓驭六模·Q2]]
```

Inside a Markdown table, escape the alias separator:

```markdown
[[01-知识库/C++/并发/条件变量#虚假唤醒与谓词检查\|条件变量标准答案]]
```

Use a full vault-relative path whenever duplicate filenames are possible. Do not create a link to a guessed filename or heading.

### Alias conventions

- Source question: `公司/专项 + 轮次 + Q号`, for example `卓驭六模·Q2` or `腾讯一面·Q5`.
- Knowledge answer: concise concept label, for example `条件变量标准答案`.
- Project answer: project plus evidence label, for example `TSR零拷贝实践`.
- Keep the alias human-readable; do not expose a long raw heading in the review center.

## Source anchors

Prefer targets in this order:

1. An existing unique, stable question heading, even if it is long. The visible alias keeps links readable in the review center.
2. A new stable block ID only when the heading is absent, actually duplicated/unstable, or the desired target is a paragraph inside a larger section. Do not add block IDs to every heading in a nonstandard note just to make it look indexed.

Use lowercase ASCII block IDs with no spaces. Attach the ID to the actual question paragraph so the link lands on the question text:

```markdown
### 题 2：零拷贝的同步与缓存一致性

**面试官题目：** RGA 写 NPU 输入 buffer 和 NPU 读之间怎样保证同步？ ^q-zy-mock06-02
```

Link to it with:

```markdown
[[04-模拟面试/卓驭专项/06-卓驭第六轮模拟面试复盘#^q-zy-mock06-02|卓驭六模·Q2]]
```

Use a stable pattern such as `q-<company-or-track>-<date-or-round>-<number>`. Check the whole target note before adding an ID so it remains unique. Do not rename an existing question heading merely to make a link shorter. In source mode a block ID is visible text; it is a locator, not content. If a unique heading works, prefer the heading so the source note stays visually clean.

## Source-note enrichment

When enrichment is in scope, add a compact section inside or immediately after the question block:

```markdown
**关联内容：**

- 项目回答：[[02-项目库/TSR端侧部署项目/TSR部署与量化细节#零拷贝的同步与 cache 一致性|TSR零拷贝同步]]
```

For a genuinely mixed question, include both `通用原理` and `项目回答`. For a single-destination question, include only the relevant line.

Add only links that resolve. Rely on Obsidian backlinks for the reverse relationship by default; do not maintain redundant manual backlink lists unless the user requests them.

## Determine answer status before declaring an answer gap

A missing link can mean different things:

- `linked`: a canonical exact answer block exists and resolves.
- `source-only`: a usable answer exists inside a real or mock interview review, but no canonical answer exists yet in the appropriate destination library.
- `partial`: some of the answer exists, but an important mechanism, boundary, or project evidence is missing.
- `ambiguous`: several plausible answer blocks exist and none can be selected safely.
- `missing`: no suitable canonical answer exists after searching relevant filenames, headings, aliases, and common synonyms.
- `unlinked`: the note has not yet been processed.

Do not call a topic new merely because no link was already present. Search first.

For `source-only`, link the exact temporary answer heading or block inside the review and add a proposed intent-appropriate canonical destination. For `partial`, `ambiguous`, or `missing`, keep the exact source link and record a plain-language marker plus a proposed destination in the review center. Do not default to `01-知识库`, and do not create a broken wiki link just to make the graph look complete.

Example:

```text
待沉淀（missing）→ 建议：01-知识库/C++/C++20协程.md#协程基本执行模型
```

```text
临时答案（source-only）：[[04-模拟面试/卓驭专项/06-卓驭第六轮模拟面试复盘#标准答案|本次复盘答案]]
→ 建议沉淀：01-知识库/边缘部署/DMA-BUF.md#缓存一致性
```

### Creating a missing answer

Create a new canonical note or block only when the user requests knowledge consolidation. Prefer creating it for P0 items, role-relevant P1 items, or topics repeated across reviews. Park low-relevance gaps rather than creating empty-note sprawl.

Start with the smallest useful structure:

```markdown
---
type: knowledge
domain: cpp
status: to-complete
indexed_at: YYYY-MM-DD
link_status: partial
---

# C++20 协程

## 30秒回答

待验证和补充。

## 核心机制

待验证和补充。

## 边界与常见追问

待验证和补充。
```

For project/实习 questions, create or extend the smallest suitable block under `02-项目库` instead, preserving the distinction between verified project facts and an AI-proposed answer. AI-generated content is a draft answer, not evidence of mastery.

## Metadata policy

Metadata means semantic indexing, not access logging. Add or update it only when a note was actually classified, link-enriched, or included in a requested indexing pass. Do not add `last_accessed` and do not touch incidental candidate files that were merely opened and rejected.

Merge with existing YAML frontmatter. Preserve unknown keys, list values, aliases, tags, and valid dates. Do not fabricate company, round, interview date, attempt date, creation date, score, or project facts. A scheduling date may be calculated only from an evidenced attempt date; `indexed_at` is never that evidence.

Recommended common fields:

```yaml
type: knowledge
domain: cpp-concurrency
aliases:
  - 条件变量
status: active
indexed_at: YYYY-MM-DD
link_status: linked
```

Recommended `type` values:

- `knowledge`
- `project`
- `real-interview-review`
- `mock-interview-review`
- `review-dashboard`
- `daily-plan`

Useful type-specific fields, only when known:

```yaml
company: 卓驭
round: 6
project: RV1126B-ADAS-TSR
```

Use `indexed_at` for the latest completed semantic indexing pass. Use `updated` only when that note's maintained content or review state changed; do not treat reading as a content update.

### Note-level `link_status`

Topic answer status and note-level metadata are different. Use only these note-level values:

- `unlinked`: no requested semantic linking pass has been completed.
- `partial`: only part of the requested question scope has been processed, or at least one item remains `source-only`, partial, ambiguous, or missing.
- `linked`: every in-scope question has an exact source anchor and a resolved canonical answer link in the intent-appropriate peer destination; duplicate links across `01-知识库` and `02-项目库` are not required.
- `needs-review`: links exist but validation found a broken, duplicate, or unsafe target.

Set `linked` only after validating the whole requested scope. If a batch stops partway through a note, leave it `partial`. Do not use `source-only`, `ambiguous`, or `missing` as a note-level `link_status`; those are per-topic answer states recorded in the review center or source annotation.

## Idempotent update rules

Every operation must be safe to repeat:

1. Reuse an existing valid question block ID; never add a second ID to the same question.
2. Reuse an existing `关联内容` section and merge only missing canonical links.
3. Compare normalized vault-relative targets before appending links; aliases may differ while the target is the same.
4. Merge a repeated interview occurrence into the existing canonical topic item.
5. Keep one `![[当前任务#今日任务]]` embed and one checklist task per normalized topic plus source question.
6. Merge YAML keys and list values without reordering or deleting unrelated data.
7. A no-op rerun must not rewrite or reorder a file. Update `indexed_at` only when a requested semantic indexing pass actually completed.

## Batch and resume rules

For a large baseline, work in bounded batches, preferably one company or specialty directory at a time. For each source file:

1. Discover questions and candidate destinations without writing.
2. Resolve canonical, source-only, partial, ambiguous, and missing statuses.
3. Apply source annotations, review-center items, and metadata as one file-level unit.
4. Validate the links added for that file.
5. Only then set its note-level `link_status` and `indexed_at`.

If interrupted, already validated files remain complete and unfinished files remain `partial` or unchanged. End every batch with counts for files, questions, canonical links, source-only answers, partial answers, ambiguous answers, missing answers, and validation failures, plus the next unprocessed file.

## Review-center representation

One normalized topic occupies one compact list item. Multiple interview occurrences are multiple exact source links under that item. A genuinely mixed answer may have multiple canonical links.

```markdown
- **DMA-BUF同步与缓存一致性** · P0 · learning · 首答 1/10 · 下次：待安排
  - 题目：[[04-模拟面试/卓驭专项/06-卓驭第六轮模拟面试复盘#^q-zy-mock06-02|卓驭六模·Q2]]
  - 核对：[[02-项目库/TSR端侧部署项目/TSR部署与量化细节#零拷贝的同步与 cache 一致性|TSR项目回答]]
```

## Daily-task representation

```markdown
- [ ] [[04-模拟面试/卓驭专项/06-卓驭第六轮模拟面试复盘#^q-zy-mock06-02|卓驭六模·Q2]]：闭卷解释 fence 和 cache 一致性（15 分钟；通过标准：能画出 RGA 写、fence 等待、NPU 读的完整时序）
  - 回答后核对：[[02-项目库/TSR端侧部署项目/TSR部署与量化细节#零拷贝的同步与 cache 一致性|TSR项目回答]]
```

The checklist lives only in `当前任务.md`. `复习中心.md` displays it with `![[当前任务#今日任务]]`. A checked item records execution, not mastery. When regenerating the plan, reconcile old checked and unchecked items using the review-system rules instead of blindly appending or overwriting the file.

## Bundled validator

Use the read-only validator after adding or repairing links. From the skill directory:

```powershell
py scripts/validate_obsidian_links.py "C:\path\to\vault" --scope "00-导航/当前任务.md" --scope "03-真实面试/公司/复盘.md"
```

Omit `--scope` only when the user requested a full-vault audit. The validator reports missing files, ambiguous filename-only targets, missing headings or block IDs, and duplicate block IDs. It never edits the vault.

## Validation checklist

After writing:

1. Confirm every linked file exists.
2. Confirm every linked heading matches exactly or every block ID exists exactly once.
3. Confirm aliases inside Markdown tables use `\|`.
4. Confirm multiple sources were merged into one canonical topic rather than duplicated.
5. Confirm metadata was merged without removing existing Properties.
6. Confirm only permitted annotations changed in historical reviews.
7. Report unresolved `partial`, `ambiguous`, and `missing` items explicitly.
8. Report `source-only` answers separately from fully canonical links.
9. Confirm a repeated run would not add duplicate anchors, annotations, items, embeds, or tasks.
