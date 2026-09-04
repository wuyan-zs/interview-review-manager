# Interview Review Manager

一个面向 Obsidian 面试准备库的 Skill。它把真实面试或模拟面试的结果串成可追溯的复习闭环：从具体题目跳到精确答案，再生成少量可执行的闭卷复习任务。

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

## 你只需要使用 3 个入口

1. **整理一份面试复盘**：处理一个指定复盘文件或目录。即使文件是“问题 → 完整答案 → 记忆要点”的手册，也会按语义识别题目；为原题补精确链接，并链接到知识库、项目库或表达库；需要时更新复习中心。
2. **给我今天的复习任务**：从复习中心生成最多 3 条闭卷 checklist，不会让任务堆成清单海洋。
3. **导入一场模拟面试结果**：把 DSH 的模拟题、首答、评分和反馈沉淀到 `04-模拟面试`，再连接到对应答案和复习任务。

周报、定向抽查、知识点补全不再单独占用菜单。直接用自然语言提出，例如“给我本周复盘”或“抽查我线程池优雅退出”。

发现 `partial` 或 `missing` 时，默认只给补充建议、目标位置和最小草案，不直接改知识库。你确认“写入”后，才会创建或补充正式内容；项目职责、指标和事故等事实必须由你确认。

## 和 DSH Interview Simulator 联动

两者分工明确：Interview Simulator 负责一问一答、追问、评分与反馈；本 Skill 负责保存结果、Obsidian 链接、识别答案缺口，以及复习计划。

不需要把模拟器复制到本 Skill 的目录中。它们通过一份 Markdown 模拟面试记录交接，因此不依赖某个平台是否支持 Skill 自动调用 Skill。

整理时优先链接到唯一的完整题目标题。只有标题缺失、重复或需要定位标题内部段落时，才会添加形如 `^q-...` 的块 ID；它是 Obsidian 定位符，不是知识内容。

### 非标准文件也有兜底

像“知识补强手册”“速成手册”“面试题整理”这类没有 YAML、日期或统一字段的文件，会按“问题 → 答案 → 记忆要点”、`Q1`、编号问题等语义单元处理。题目边界明确时，题目下方会保留一个固定标记：

```markdown
**关联内容：**
- 项目回答：[[02-项目库/TSR端侧部署项目/TSR部署与量化细节#RGA链路|TSR零拷贝链路]]
```

如果没有安全的目标，会写成“待补充（missing）”并给出建议位置，而不是生成断链；如果连题目边界都无法确定，只输出预览，不修改原文。

### 为什么可能需要分批

单个文件默认走快速路径：先扫描题目标题，再一次性检索候选标题，只打开需要核对的段落。一个文件超过 12 道题时，默认按约 6–8 道一批处理，并在每批后校验和报告进度。这样可以避免逐题重复读取大型知识库，也能在 DSH 中随时续接，不必重新处理已经完成的题目。

推荐流程：

```text
DSH 模拟面试 → 得到题目/首答/评分/反馈 → 保存或粘贴为 Markdown
→ 导入复习管家 → 原题链接 + 知识/项目答案链接 + 复习中心
→ 需要时生成今日 3 项任务
```

模拟结束后，在 DSH 中使用：

```text
导入刚才的模拟面试结果。保存到 04-模拟面试/卓驭专项，
链接到对应知识库或项目库；先给写入预览，不要修改文件。
```

如果 DSH 无法把上一段模拟对话直接交给复习管家，先把最终 scorecard 粘贴或保存到目标 Markdown 文件即可。具体格式见 [`references/simulator-handoff.md`](references/simulator-handoff.md)。

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
使用 $interview-review-manager 整理 04-模拟面试/卓驭专项/某次复盘.md，
补齐原题和对应答案链接；先输出修改预览，不要写入文件。
```

```text
使用 $interview-review-manager 给我今天 30 分钟的复习任务。
```

```text
使用 $interview-review-manager 导入刚才的模拟面试结果，先给预览。
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
│   ├── review-system.md
│   └── simulator-handoff.md
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
