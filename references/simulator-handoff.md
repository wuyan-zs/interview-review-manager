# 模拟面试交接格式

Read this reference only when importing a completed mock-interview session.

The simulator and the review manager are separate skills. Use a Markdown file as their stable handoff: the simulator conducts the session; this skill organizes the result. Do not depend on one skill being able to programmatically invoke the other.

## Recommended location

Save one completed session under `04-模拟面试/<公司或专题>/`, for example:

```text
04-模拟面试/卓驭专项/2026-09-03-卓驭模拟面试.md
```

If a date is unknown, do not put a fabricated date in frontmatter or review scheduling. A descriptive filename without a date is acceptable.

## Minimum record

Keep the simulator's output as source evidence. One question may use this compact structure:

```markdown
---
type: mock-interview-review
company: 卓驭
interview_date: 2026-09-03
---

# 卓驭模拟面试

## Q1：条件变量为什么要配合谓词循环？

**我的首答：** ……

**首答评分：** 5/10

**反馈：** ……

**缺失点：** 虚假唤醒、通知与状态检查之间的边界。

**建议核对：** ……
```

Required for useful import: question, first answer or an explicit blank, and score/feedback when the simulator supplied them. Preserve follow-up questions and retries, but label them separately from the first answer.

## Import contract

For each question, the manager should:

1. Add a stable source anchor only if its heading is not a safe exact target.
2. Link a standalone question to `01-知识库`, a project question to `02-项目库`, and a behavioral question to `05-简历与表达`.
3. Treat an answer that exists only in this record as `source-only`; propose, but do not automatically write, a canonical note unless the user asks for consolidation.
4. Use the recorded first-answer score and `interview_date` only when actually present. The date is the evidence base for a calculated next review; otherwise use `待安排`.
5. Merge repeated weaknesses into the existing review-center topic and create a daily task only when the user asks for today's plan.

## DSH use

After DSH's Interview Simulator ends, ask the review manager in the same conversation or a new one:

```text
导入刚才的模拟面试结果。保存到 04-模拟面试/卓驭专项，
链接到对应知识库或项目库；先给写入预览，不要修改文件。
```

If DSH does not expose the previous simulator transcript to the review-manager turn, paste or save the simulator's final scorecard into the Markdown record first. This manual handoff remains reliable across agent runtimes.
