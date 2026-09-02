# Full-Spectrum Review

> 面向 AI Coding Agent 的**全方位软件审计 Skill**：从第一性原理理解系统，再统一审查工程正确性、业务逻辑、架构、可靠性、性能与复杂度；支持按上下文/Agent 能力拆分并发 Audit Units，并把结果沉淀为可复审、按优先级管理的审计资产。

**当前 Core 版本：`v0.3.0`** · [CHANGELOG](CHANGELOG.md) · **简体中文** · [English](README.en.md)

## 它解决什么问题

普通 AI Code Review 往往只做两件事之一：盯 diff 找 bug，或者拿一张超长 checklist 逐项打勾。

`full-spectrum-review` 的目标不同：让一个没有参与项目开发的第三方 Agent 先理解**问题本身**，再判断系统是不是以正确、必要且可持续的方式解决它。

```text
锁定 exact target / revision
        ↓
建立 Audit Plan + Coverage Ledger
        ↓
按系统边界拆分 Audit Units（需要时并发）
        ↓
理解系统 / 业务 / ownership / invariants
        ↓
First Principles：什么是最小充分机制？
        ↓
加载 0..N 个适用 Domain Packs
        ↓
Engineering + Business + Cost Review
        ↓
高召回候选 → 证据验证 → 反证调查
        ↓
跨单元 verification + Root-cause dedup
        ↓
P0/P1/P2/P3 + Recommended Execution Order
        ↓
持久化 Report + Stable Finding Ledger
```

## 默认就是全面审计

正常调用这个 Skill 时，不需要再让用户选择“工程 / 业务 / 优化”模式。

这里的“全面”不是要求每个文件都逐行读一遍，而是：**所有对目标有实质影响的系统边界、业务流程和风险面，都必须进入 Audit Plan，并在最终 Coverage Ledger 中诚实标记实际覆盖深度。**

因此报告能明确区分：

```text
没有发现问题
≠
这部分根本没有审到
```

对于 PR，全面审查的是 PR 及其所有重要影响链路；对于 repository-wide audit，才覆盖整个系统的重要生产/业务路径。

## 大仓库与有限上下文：可并发 Audit Orchestration

`full-spectrum-review` **不要求模型拥有 1M context**。

大型仓库可以被拆成多个有界 **Audit Units**。如果当前 harness 支持隔离 worker/subagent，可以并发执行；如果不支持，就按完全相同的 Audit Unit 边界串行执行。

```text
                    Lead / Coordinator
                           │
                  Shared Audit Brief
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   Execution Unit     Position Unit      Backtest Unit
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                 Cross-boundary Verify
                           │
              Evidence + Root-cause Dedup
                           │
                    Canonical Report
```

默认优先按**子系统 / 业务流 / 外部边界**拆，而不是简单拆成“Engineering Agent / Business Agent / Optimization Agent”。原因是后者往往要求每个 Agent 重复读取整个仓库。

每个 subsystem worker 在自己的 scope 内执行完整的 Engineering / Business / First-Principles / Cost / Domain-Pack reasoning；跨系统的 ownership、端到端业务链、长期资源问题再由少量 cross-cutting Audit Units 复核。

### Shared Audit Brief

Lead 会给所有 Audit Units 一个紧凑的事实包，例如：

- exact target / revision；
- repository purpose / architecture map；
- authoritative state / ownership；
- critical invariants；
- Business Authority Map；
- Domain Packs + versions；
- prior open findings / Keep-As-Is；
- 当前 Audit Unit 的 scope。

**共享事实，不提前共享 tentative findings**，尽量避免 worker 互相锚定。

### Reviewer Packet

worker/subagent 返回的是统一的候选证据包，而不是最终报告：

```text
Audit Unit / revision / coverage
Inspected components / contracts
Relevant invariants
Candidate Findings + evidence
Cross-boundary concerns
Keep-As-Is candidates
Evidence gaps
```

worker **不能**自行分配正式 `FSR-###`、最终 Priority、Blocking、Status 或 terminal verdict。最终证据核验、跨单元矛盾解析、root-cause dedup、stable ID 和 canonical report 只能由 Lead/Coordinator 统一完成。

因此并发审计不会变成“把 8 份 worker 报告拼在一起”。

权威规则见 [`references/orchestration-protocol.md`](references/orchestration-protocol.md)。

## 第一性原理：不把现有架构当成问题定义

这是本 Skill 的核心特色之一。

Reviewer 在接受一个重要 subsystem 的现有设计之前，要先独立重建：

```text
Required Outcome
+ Irreducible Constraints
+ Required Invariants
→ Minimum Sufficient Mechanism
```

再拿它与当前实现比较。

因此即使代码**没有已知 bug、测试全部通过**，下面这种情况仍然可以成为正式 finding：

```text
本来只需要：
单一 authoritative state
→ explicit UNKNOWN
→ reconciliation

实际却变成：
cache
+ registry
+ retry coordinator
+ watchdog
+ fallback reconciler
+ cleanup worker
```

但 First Principles 不是“删代码许可证”。

任何 `Accidental Complexity` finding 在发布前都必须主动调查：

> **Why does this layer exist?**

Reviewer 要尽可能查历史、测试、ADR、caller、operator workflow、外部契约等反向证据。如果没有做 meaningful disconfirmation attempt，只能记为 observation/hypothesis，不能作为正式复杂度 finding。

权威规则见 [`references/first-principles-review.md`](references/first-principles-review.md) 与 [`references/finding-protocol.md`](references/finding-protocol.md)。

## Necessity 与 Cost 分开

为了避免两个 reviewer 重复判断同一件事，现在职责明确分为：

### First Principles = Necessity

回答：

> **这个东西该不该存在？**

包括 duplicated ownership/state、无必要 abstraction、recovery layer、compatibility path、config branch、worker/cache/state-machine complexity 等。

### Optimization = Cost

回答：

> **既然这个机制确实需要存在，它运行得是否足够高效？**

包括 algorithmic cost、CPU、memory、I/O、network、batching、lock contention、resource lifecycle、external API/storage/model cost 和 long-running stability。

权威规则见 [`references/optimization-review.md`](references/optimization-review.md)。

## Business Logic 不默认相信代码和测试

Business Review 会先建立当前项目自己的 **Business Authority Map**，判断本次业务真相主要来自哪些证据：外部协议/服务契约、正式 spec / ADR、用户承诺、测试、现有实现等。

这个权威顺序不是 Core 写死的，因为不同领域并不相同。

如果业务意图无法可靠确定，Reviewer 应把它写入 **Open Questions for the Maintainer**，而不是伪装成一个 P1/P2 finding。

详见 [`references/business-logic-review.md`](references/business-logic-review.md)。

# Domain Packs

这是 Full-Spectrum Review 的另一个核心设计。

Core Skill 只负责**怎么审**；Domain Pack 负责**这个领域有哪些不能靠通用软件知识可靠推导的真实规则**。

```text
Core Audit Method
        +
0..N Domain Packs
```

一个真实项目可以同时加载多个领域包，例如：

```text
trading
+ distributed-systems
+ accounting
```

Core 不硬编码 pack 名称。Reviewer 检查可用 `domains/`，根据 `applies-when` 加载全部适用包，并把 pack 名称/版本记录进 Audit Metadata。

### Domain Pack 负责

- Domain Glossary；
- Domain Invariants；
- External Semantics；
- Domain-specific Scenario Sweep；
- Severity Context。

### Core 负责

- Audit Orchestration；
- First-Principles 方法；
- finding 验证与反证门槛；
- P0/P1/P2/P3 与 Confidence；
- root-cause dedup；
- report / coverage / stable-ID lifecycle。

Pack 可以用领域语言**实例化** Core 原则，但不能复制一套自己的 finding bar 或 report schema。

统一 contract 见 [`domains/_CONTRACT.md`](domains/_CONTRACT.md)。该文件是 pack authoring contract，普通 audit 不需要加载。

## Trading Domain Pack

当前内置：[`domains/trading/DOMAIN.md`](domains/trading/DOMAIN.md) `v2`。

它用于量化交易、交易所/券商执行、模拟盘与真实资金系统，额外关注：

- K 线/行情时间语义与未来函数；
- backtest / simulation / live parity；
- signal / intent / order / fill / position 的概念分离；
- partial fill、cancel/fill race、UNKNOWN order outcome；
- position truth、restart reconciliation、manual takeover；
- precision / minimum order / rounding；
- PnL、fee、funding 与数量守恒；
- protection order；
- rate limits / throttling / bans；
- server time / signing window；
- reduce-only / close-position / post-only / TIF / trigger-price semantics；
- hedge vs one-way、margin mode、liquidation/ADL；
- symbol lifecycle / maintenance / delisting；
- multi-instance account ownership；
- API credential permission scope。

这些内容保持 **provider-neutral**：pack 要求 Reviewer 去核实目标交易所真实 contract，而不是把 Binance/OKX/Bybit 任意一家当前参数写成通用真理。

未来可以按同一 contract 增加 payments、accounting、distributed-systems、security、database、AI-agent 等 Domain Packs，而**不修改 `SKILL.md` 来注册新包**。

## Finding 不再是一次性编号

审计报告不是一次性快照。

Finding 使用 stable ID，并通过轻量状态持续复审：

```text
OPEN
FIXED
ACCEPTED
SUPERSEDED
REOPENED
```

优先级变化不会改变 ID；ID 也不会因为报告重新排序而重排。

如果目标仓库没有自己的审计体系，默认使用：

```text
docs/reviews/
├── INDEX.md
├── 2026-09-02-full-spectrum-review.md
└── pr-123-a1b2c3d-full-spectrum-review.md
```

`INDEX.md` 只是轻量 finding ledger，不是再造一个 Jira。

权威规则见 [`references/reporting-protocol.md`](references/reporting-protocol.md)。

## 报告里有什么

一次完整审计通常包括：

- Audit Metadata / exact revision；
- **Core Skill version + Skill revision**；
- Execution Mode（single / sequential-units / parallel-units）；
- Loaded Domain Packs + versions；
- Coverage Ledger；
- Executive Summary；
- Priority Overview；
- Recommended Execution Order；
- P0 → P1 → P2 → P3 findings；
- Open Questions for the Maintainer；
- Positive Findings / Keep As-Is；
- Evidence / Verification Gaps。

多 Audit Unit 审计可以在 Appendix 留一个紧凑 orchestration summary，但不会把内部 worker transcript 全部塞进最终报告。

Finding 的 canonical schema、Priority、Confidence、Status 只有一个权威来源：[`references/finding-protocol.md`](references/finding-protocol.md)。README 只做解释，不复制另一套规范。

## 审计默认只读

即使 Agent 有 repository write 权限，**审计过程也不会顺手修改业务代码或配置**。

审计授权下的写入范围只包括 report / INDEX 等审计资产。真正修复必须成为用户另行明确授权的任务。

这对生产系统、真实资金系统尤其重要。

## 版本控制

Core Skill 使用 Semantic Versioning，当前版本由根目录 [`VERSION`](VERSION) 唯一确定；用户可见协议变化记录在 [`CHANGELOG.md`](CHANGELOG.md)。

当前仍处于 `0.x`：

- `MINOR`：新增能力、重要 audit/report contract 变化；在 1.0 之前，不兼容协议调整也允许提升 MINOR；
- `PATCH`：不改变主要审计 contract 的修正、澄清和小型兼容改进；
- `MAJOR`：1.0 之后用于不兼容的核心协议变化。

Domain Pack **独立版本化**。例如 Core 可以是 `0.3.0`，同时 Trading Pack 是 `v2`；审计报告会同时记录二者。

Git tag / GitHub Release 后续正式发布时可以与 `VERSION` 对齐，但 Skill 的运行不依赖 release infrastructure。

## 目录

```text
full-spectrum-review/
├── SKILL.md
├── VERSION
├── CHANGELOG.md
├── README.md
├── README.en.md
├── LICENSE
├── ACKNOWLEDGEMENTS.md
├── references/
│   ├── orchestration-protocol.md
│   ├── first-principles-review.md
│   ├── engineering-review.md
│   ├── business-logic-review.md
│   ├── optimization-review.md
│   ├── finding-protocol.md
│   ├── reporting-protocol.md
│   └── example-finding.md
└── domains/
    ├── _CONTRACT.md
    └── trading/
        └── DOMAIN.md
```

`SKILL.md` 保持流程与 contract 精简；详细规则、示例和领域知识按需读取，避免固定巨型 Prompt 挤占源码上下文。`CHANGELOG.md` 和 `domains/_CONTRACT.md` 也不会在普通 audit 中无条件加载。

## 安装

本仓库遵循 `SKILL.md` Agent Skills 目录格式。

如果客户端支持厂商中立的 `.agents/skills/`，推荐优先使用它：

```bash
git clone https://github.com/liuyejinghong/full-spectrum-review.git .agents/skills/full-spectrum-review
```

目前已核实的常见位置/方式包括：

| Client | Project / workspace | User / global |
|---|---|---|
| Cursor | `.agents/skills/` 或 `.cursor/skills/` | `~/.agents/skills/` 或 `~/.cursor/skills/` |
| Gemini CLI | `.agents/skills/` 或 `.gemini/skills/` | `~/.agents/skills/` 或 `~/.gemini/skills/` |
| GitHub Copilot | `.agents/skills/` / `.github/skills/` / `.claude/skills/` | `~/.agents/skills/` / `~/.copilot/skills/` |
| Codex | `.codex/skills/` | `$CODEX_HOME/skills/`（通常为 `~/.codex/skills/`） |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |

不同客户端的发现/激活机制会变化；以对应客户端当前官方文档为准。Skill 本身不依赖某个 harness 的工具名、subagent 或 GitHub API。

## 使用

Repository-wide audit：

```text
使用 full-spectrum-review 对这个项目进行一次全面审计。
理解业务和架构，从第一性原理重建关键机制，加载所有适用 Domain Packs；如果目标较大且当前 harness 支持 worker/subagent，按 Audit Units 并发执行，否则同边界串行执行；诚实记录 coverage，统一验证/去重/排序 findings，最终沉淀 report + audit ledger。
```

PR audit：

```text
使用 full-spectrum-review 全面审查 PR #123。
绑定 exact head，覆盖所有重要受影响链路，最终生成 compact canonical report；blocking finding 存在时给出 REQUEST_CHANGES。
```

## 设计原则

- 全面审计是默认；专项审查是显式例外。
- 全面意味着 coverage 可证明，不意味着每个文件同深度扫描。
- 大型目标优先按 subsystem/flow 拆成有界 Audit Units；并发是能力优化，不是协议依赖。
- 有 subagent 就并发，没有就同边界串行，最终报告 contract 不变。
- worker 只产 candidate evidence；Lead 才拥有 final finding / stable ID / verdict authority。
- 先重建问题，再接受现有解决方案。
- Necessity 与 Cost 分离。
- 找 accidental complexity 必须主动寻找反证。
- 测试是证据，不是真理。
- changed lines 是起点，不是 reasoning 边界。
- finding 按 root cause 去重，不按症状堆数量。
- severity 与 confidence 分开。
- Domain knowledge 可插拔，Core method 不随领域增长。
- 审计对被审实现默认只读。
- 最终交付必须让维护者知道：**审到了什么、没审到什么、先修什么、为什么、如何证明修好了，以及什么不要乱改。**

## 参考标准与客户端文档

- Agent Skills open standard: https://agentskills.io/
- Cursor Agent Skills: https://cursor.com/docs/skills
- Gemini CLI Agent Skills: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md
- GitHub Copilot Agent Skills: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
- OpenAI Codex skills examples/docs: https://github.com/openai/codex/tree/main/.codex/skills
- Claude Agent Skills authoring guidance: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices

## License

MIT
