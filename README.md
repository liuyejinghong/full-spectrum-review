# Full-Spectrum Review

> 面向 AI Coding Agent 的全方位软件审计 Skill：先重建"这个系统到底在解决什么问题"，再统一审判工程正确性、业务真相、可靠性与成本，最后把结论沉淀成可复审的审计资产——而不是一份看完就丢的 review 意见。

**当前 Core 版本：`v0.4.0`** · [CHANGELOG](CHANGELOG.md) · **简体中文** · [English](README.en.md)

## 普通 AI review 缺的那一块

让 AI 审代码，通常得到两种结果之一：盯着 diff 逐行找 bug，或者拿着一张超长 checklist 逐项打勾。这两种都回答不了一个更要紧的问题——

**代码没有 bug、测试全绿，但它在一道错题上写出了完美答案，怎么办？**

真实项目里最贵的病根往往不是某行代码写错，而是：只需要一个权威状态，却长出了缓存、注册表、重试协调器、看门狗、兜底对账、清理 worker 六层机制互相打补丁；或者代码忠实实现了某条业务规则——而那条规则从第一天就理解错了。

`full-spectrum-review` 为这一层审查而生：让一个没参与开发的第三方 Agent，先理解问题本身，再判断系统是不是以正确、必要、且可持续的方式解决了它。

## 六个核心判断

规则文件只是这六条判断的展开：

### 一、先重建问题，再接受方案

审判任何重要设计之前，Reviewer 先独立推导：真实要的结果是什么、哪些约束不可约、最小充分的机制是什么——然后才拿它与现状比较。**现有架构是待审的答案，不是题目的定义。**即使代码没有已知 bug，"本来一个权威状态就能解决的事长出了六层机制"也可以成为正式 finding。

### 二、没有发现问题 ≠ 没有审到

报告里的 Coverage Ledger（覆盖台账）逐块记录实际审到的深度：deep / sampled / 没审 / 证据不足。一份"全部通过"但覆盖含糊的报告，不如一份"这两块我不敢下结论"的报告可信。全面审计的"全面"，指的是所有重要边界和流程都进入计划并诚实交待覆盖状态，不是每个文件都逐行扫一遍。

### 三、"该不该存在"与"存在了贵不贵"分开审

必要性（First Principles 轴）与成本（Optimization 轴）是两个独立问题，由两套独立规则审。混在一起的后果是开错药方：嫌它慢就建议删掉，嫌它多余就建议优化。优化审查中若发现某机制根本不该存在，移交必要性门槛处理，不另立一条竞争规则。

### 四、指控过度设计，先找反证

发布"这层是过度工程"的指控之前，必须主动调查**它为什么存在**：翻提交历史、ADR、测试、调用方、运维约束，寻找"它确实有理"的反面证据。做过认真反证仍找不到独立存在理由，指控才成立；没调查过就只能记为疑问。这让它区别于"看什么都像过度设计"的 review 工具——防 agent 别过度建设、与指控既有层须举证，是一枚硬币的两面。

### 五、业务真相不默认等于代码

代码、测试、文档都只是证据，不自动等于"对"。Reviewer 先为当前项目建立 Business Authority Map（业务权威地图）：这个领域里什么证据说了算——外部协议、正式 spec、用户承诺还是实现本身？权威顺序因领域而异，不写死在 Core。业务意图无法可靠确立时，如实提出 Open Question 交给维护者，而不是伪装成一个 P1/P2 finding。

### 六、审计是资产，不是快照

Finding 用稳定 ID 沉淀（FSR-001、FSR-002……）带生命周期：OPEN / FIXED / ACCEPTED / SUPERSEDED / REOPENED。复审接着上次的结论走，优先级变了 ID 不变；值得保留的设计决策记入 Keep-As-Is，防止后来的 agent 手痒"简化"掉不该动的东西。目标仓库若没有自己的审计体系，默认落在 `docs/reviews/` 的轻量台账里——不是再造一个 Jira。

## 一个真实 finding 的样子

（缩略自完整范例 [`references/example-finding.md`](references/example-finding.md)。场景：一个量化交易系统里，三个组件各自独立维护"这笔订单是否还在提交中"这一件事。）

> **FSR-042 · 重复的订单恢复所有权**（P1 · Accidental Complexity · Confidence: High）
>
> 业务要求的不是三份 pending 状态，而是"提交结果未知时，不得造成重复经济动作"。现状是提交缓存、pending 注册表、恢复看门狗三个所有者各带重试/清理转换，恢复正确性取决于内部副本之间的同步。
>
> **反证调查**：查了引入提交、重启测试、当前调用方和运维恢复文档——两个额外层来自两次历史事故修复，需求仍然真实；但两者都可以由"一份持久化的未决意图 + 交易所对账"一并提供，没有任何调用方需要独立的可变所有权。
>
> **方向**：让持久化的未决意图/对账组件成为唯一所有者，其余转为派生视图或移除；仅在 reconciliation 证明外部不存在之后才允许有界重试。测试全绿不是反驳——它只证明三条同步路径今天恰好一致。

一次审计跑完"高召回找候选 → 证据验证 → 反证调查 → 跨边界核验 → 根因去重 → 统一排序"，落在纸面上就是这样的东西。

## 怎么运作

一次调用默认就是全面审计（专项审查是显式例外）。按目标大小选执行形态，协议与最终产物不变：

```text
锁定目标与精确版本
        ↓
审计计划 + 覆盖台账
        ↓        小目标 → 单单元直查
中大目标 → 按子系统/业务流拆成有界审计单元（Audit Unit）
        ↓        有 subagent 就并发，没有就同边界串行
共享事实包（Brief，只装改变行为的事实）→ 各单元独立全谱审查 → 候选证据包（Packet）
        ↓
跨边界核验 → 证据验证/反证 → 根因去重 → P0–P3 排序
        ↓
唯一权威报告 + 可续审的 finding 台账
```

几个关键取舍：

- **按子系统拆，不按"工程/业务/优化"拆**——后者每个 agent 都得重读整个仓库。每个单元在自己的 scope 内跑全部视角和领域包；跨系统的所有权、端到端业务链另设少量横切单元。
- **共享事实，不共享初步结论**——既防 worker 互相锚定，又防重复推导。
- **worker 只有候选权**——正式 ID、最终优先级、blocking、终审结论只能由 Lead 统一裁定。并发审计不会变成"把八份报告拼在一起"。
- **上下文靠方法省，不靠字数省**——重复阅读由结构消灭：每个模块只归一个单元审，跨边界代码只读记 concern，事实包只装"能改变某个单元看法或做法"的事实。不设任何字数预算：入选的事实不因长度被删，packet 里的候选证据一条不少地保留（packet 漏掉的候选随 worker 上下文一起消失），被排除的只有过程叙事；跟进单元必须先说出它要解决的、仍悬而未决的问题。
- **领域知识插拔**——Domain Pack 管"这个领域有哪些从源码推导不出来的真实规则"，Core 管"怎么审"。内置 trading 包（K 线时间语义、UNKNOWN 订单结果、对账、精度、限频、多实例 ownership……），新增 payments / accounting 等包不需要改 SKILL.md。

最终交付一份报告：元数据与精确版本、覆盖台账、执行摘要、按优先级排序的 findings、推荐修复顺序、给维护者的开放问题、Keep-As-Is 与证据缺口——形态随目标伸缩，窄 PR 紧凑、全仓库详尽。

权威规则都在 [`references/`](references/) 与 [`domains/_CONTRACT.md`](domains/_CONTRACT.md) 各文件里，本 README 只做导览。

## 什么时候用，什么时候别用

**用它**：仓库级全面审计；重要 PR / commit 的合并决策；上线前的生产就绪评估；架构与所有权审查；量化交易等高风险领域（加载对应 Domain Pack）。

**别用它**：两行的改动想要快速过目——普通 review 就够，全套协议是杀鸡用牛刀；想直接修代码——本 Skill 对被审实现默认只读，修复是另行授权的后续任务；想替代测试与 CI——它消费证据，不生产覆盖率。

诚实的边界：它不保证每次都揪出问题；它保证的是**审到了什么、没审到什么、为什么、先修什么、哪些不要乱动**这五件事说得清。

## 安装

本仓库遵循 `SKILL.md` Agent Skills 目录格式。客户端支持厂商中立的 `.agents/skills/` 时优先使用：

```bash
git clone https://github.com/liuyejinghong/full-spectrum-review.git .agents/skills/full-spectrum-review
```

已核实的常见位置：

| Client | Project / workspace | User / global |
|---|---|---|
| Cursor | `.agents/skills/` 或 `.cursor/skills/` | `~/.agents/skills/` 或 `~/.cursor/skills/` |
| Gemini CLI | `.agents/skills/` 或 `.gemini/skills/` | `~/.agents/skills/` 或 `~/.gemini/skills/` |
| GitHub Copilot | `.agents/skills/` / `.github/skills/` / `.claude/skills/` | `~/.agents/skills/` / `~/.copilot/skills/` |
| Codex | `.codex/skills/` | `$CODEX_HOME/skills/`（通常为 `~/.codex/skills/`） |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |

各客户端的发现/激活机制会变，以其当前官方文档为准；Skill 本身不依赖任何 harness 的工具名、subagent 或 GitHub API。

## 使用

仓库级审计：

```text
使用 full-spectrum-review 对这个项目做一次全面审计。
理解业务和架构，从第一性原理重建关键机制，加载所有适用 Domain Packs；
目标较大且 harness 支持 worker 时按审计单元并发执行，否则同边界串行；
诚实记录覆盖，统一验证/去重/排序，最终沉淀报告 + 审计台账。
```

PR 审计：

```text
使用 full-spectrum-review 全面审查 PR #123。
绑定 exact head，覆盖所有重要受影响链路，产出紧凑的权威报告；
存在 blocking finding 时给出 REQUEST_CHANGES。
```

## 目录

```text
full-spectrum-review/
├── SKILL.md                 # 精简主流程与契约
├── VERSION / CHANGELOG.md
├── references/
│   ├── orchestration-protocol.md   # 审计单元分解、并发/串行、上下文节省方法
│   ├── first-principles-review.md  # 必要性：最小充分机制
│   ├── engineering-review.md       # 正确性/状态/故障/并发/兼容
│   ├── business-logic-review.md    # 业务权威地图/领域模型/生命周期
│   ├── optimization-review.md      # 成本：给已证明必要的机制算账
│   ├── finding-protocol.md         # finding 类型/门槛/优先级/ID 的唯一权威
│   ├── reporting-protocol.md       # 覆盖台账/报告/复审生命周期
│   └── example-finding.md          # 完整 finding 范例
└── domains/
    ├── _CONTRACT.md                # Domain Pack 编写契约（审计时不加载）
    └── trading/DOMAIN.md           # 交易领域包 v2
```

`SKILL.md` 保持精简，细节按需加载，避免固定巨型 Prompt 挤占被审代码的上下文。

## 版本与领域包

[`VERSION`](VERSION) 唯一确定当前 Core 版本（pre-1.0 SemVer，政策见 [CHANGELOG](CHANGELOG.md) 开头）。Domain Pack 独立版本化——Core 可以是 `0.4.0`，同时 Trading Pack 是 `v2`，审计报告会同时记录二者。

## 参考标准

- Agent Skills open standard: https://agentskills.io/
- Cursor Agent Skills: https://cursor.com/docs/skills
- Gemini CLI Agent Skills: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md
- GitHub Copilot Agent Skills: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
- OpenAI Codex skills examples/docs: https://github.com/openai/codex/tree/main/.codex/skills
- Claude Agent Skills authoring guidance: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices

## License

MIT
