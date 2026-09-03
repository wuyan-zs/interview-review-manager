# Interview Review Manager

一个面向 Obsidian 面试准备库的 Codex Skill。它把分散在真实面试、模拟面试、知识库和项目库中的内容串成可追溯的复习闭环：从具体题目跳到精确答案，再生成少量可执行的闭卷复习任务。

适用于已有类似目录结构的面试知识库：

```text
00-导航/
01-知识库/
02-项目库/
03-真实面试/
04-模拟面试/
05-简历与表达/
06-计划与状态/
```

## 能做什么

- 为面试题添加精确 Obsidian 链接，必要时使用稳定块 ID。
- 按题目意图将答案链接到知识库、项目库或表达库。
- 识别已链接、临时答案、部分覆盖、歧义和真正缺口。
- 维护简洁的 `复习中心.md`，每个主题都能回到原题和答案。
- 在 `当前任务.md` 生成不超过三项的闭卷复习 checklist。
- 追踪首答成绩、复测表现和掌握状态；不把“看过笔记”当成掌握。
- 校验 Obsidian 链接、锚点以及复习中心和今日任务的结构。

## 核心约定

`01-知识库` 与 `02-项目库` 是平级库：

- 独立八股、语言机制、通用原理 → `01-知识库`
- 项目实现、实习职责、指标、故障排查、取舍 → `02-项目库`
- 只有题目确实同时要求原理和项目应用时，才同时链接两边。

项目笔记中包含通用技术机制，不意味着必须在知识库重复创建一份笔记。

复习日期只从有证据的作答日期计算。没有明确日期时，Skill 会写 `待安排`，不会把整理当天伪装成作答日期。

## 常见用法

在 Codex 中直接描述任务，或显式调用：

```text
使用 $interview-review-manager 整理这份模拟面试复盘，关联每道题的原题和答案。
```

```text
把这份复盘中的薄弱点写入复习中心，并生成今天 30 分钟的闭卷任务。
```

```text
对复习中心里的 P0 题目做一次闭卷复测，并记录结果。
```

## 写入范围与安全性

Skill 默认保留原始面试内容。进行明确的链接整理或复盘吸收时，只会做增量修改：

- YAML Properties
- 稳定块 ID
- 紧凑的 `关联内容` 链接
- `00-导航/复习中心.md` 和 `00-导航/当前任务.md` 中的复习状态

它不会删除、重命名或重构你的知识库，也不会重写原始题目、回答、得分或点评。

## 目录结构

```text
interview-review-manager/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── linking-and-metadata.md
│   └── review-system.md
└── scripts/
    ├── validate_obsidian_links.py
    └── validate_review_system.py
```

## 校验

链接或锚点发生变化后运行：

```powershell
py scripts/validate_obsidian_links.py "C:\path\to\vault" --scope "00-导航/复习中心.md"
```

更新复习中心或今日任务后运行：

```powershell
py scripts/validate_review_system.py "C:\path\to\vault" --require-sections
```

第一个脚本检查链接目标、标题和块 ID 是否存在；第二个脚本检查复习中心嵌入、题目出处、答案/缺口标记，以及每日任务不超过三项。

## 安装

将整个 `interview-review-manager` 目录放入 Codex 可发现的 Skills 目录，然后重新加载 Skills。保留目录名与 `SKILL.md` 中的 `name: interview-review-manager` 一致。

## 开发检查

修改 Skill 后，运行 Codex 自带的结构校验：

```powershell
py path\to\skill-creator\scripts\quick_validate.py path\to\interview-review-manager
```

该检查验证 frontmatter 和目录结构；建议再用一个临时 vault 运行两个校验脚本，验证真实链接和复习任务格式。
