# Full-Spectrum Review

> 面向 AI Coding Agent 的**全方位代码库审计 Skill**：从第一性原理重建需求，再统一审查工程正确性、业务逻辑、架构、稳定性、性能与复杂度，并沉淀为按优先级排序的审计报告。

**简体中文** · [English](README.en.md)

## 它解决什么问题

普通 AI Code Review 往往有三个问题：

1. 只盯 diff 找 bug；
2. 拿着一张很长的 checklist 逐项打勾；
3. 默认接受现有架构，只检查“这套复杂实现有没有 bug”，却很少追问“这个功能本来是否根本不需要这么复杂”。

`full-spectrum-review` 的目标不是制造更多 finding，而是完成一次真正可落地的综合审计：

```text
理解真实需求 / 业务 / 外部约束
      ↓
第一性原理重建最小充分机制
      ↓
与现有架构 / 状态 / 补丁层比较
      ↓
全面检查工程 + 业务 + 稳定性 + 性能 + 复杂度
      ↓
高召回生成候选问题
      ↓
证据验证 + 根因去重
      ↓
统一 P0 / P1 / P2 / P3 排序
      ↓
生成并沉淀完整审计报告
```

## 第一性原理：先审“为什么需要这么复杂”

这是全面审计里的强制阶段，不是普通 Optimization 的附属项。

Reviewer 在深入接受现有实现前，要先独立回答：

1. 这个功能真正必须完成什么结果？
2. 哪些约束是业务、外部系统、并发、恢复、性能或兼容性带来的真实约束？
3. 哪些 invariant 无论如何都必须保持？
4. 满足这些要求的**最小充分机制**是什么？
5. 现有实现额外增加了哪些 state、owner、worker、queue、cache、retry、fallback、watchdog、wrapper、状态机或配置分支？
6. 每一层额外复杂度到底承载哪个当前仍然存在的独立 requirement？
7. 如果今天从零实现同样的当前需求，还会选择这套设计吗？

比较方式是：

```text
Required outcome
+ Irreducible constraints
+ Required invariants
        ↓
Minimum sufficient mechanism
        VS
Current implementation
        ↓
Accidental complexity delta
```

因此，即使一段实现：

- 当前没有复现 bug；
- 测试全部通过；
- 最终业务结果也正确；

只要可以证明它通过不必要的重复状态、补丁层、互相修复的 recovery、无真实消费者的 abstraction 等方式完成了一个本可显著更简单完成的功能，仍然可以成为正式的 **Accidental Complexity** finding。

这不等于“代码越少越好”。真实的业务状态、并发、失败恢复、兼容性和性能约束可能天然复杂。只有当 reviewer 能证明某层没有独立责任，或责任可以安全收敛到更简单机制，并保持所有必要行为时，才可以判为 accidental complexity。

详细规则见 [`references/first-principles-review.md`](references/first-principles-review.md)。

## 默认会审什么

正常调用这个 Skill 时，默认就是**全面审计**，不需要用户再选择模式。

它会根据项目实际情况覆盖：

- 第一性原理、最小充分机制与 accidental complexity；
- 工程正确性、调用链与契约传播；
- 业务规则、Domain Model、业务 invariant 与生命周期；
- 架构边界、ownership、source of truth、跨模块耦合；
- timeout、retry、restart、reconciliation、并发与状态一致性；
- 数据完整性、兼容性、配置、迁移与外部系统语义；
- CPU、内存、I/O、网络、算法复杂度和长时间运行稳定性；
- 冗余代码、重复状态、过度抽象、dead code、依赖与配置膨胀；
- 测试质量、可观测性、部署、回滚与运维风险；
- 存在真实 trust boundary 时的安全问题；
- 对应 Domain Pack 中的领域特有风险。

First Principles / Engineering / Business Logic / Optimization 是不同的内部 reasoning lens，目的是减少思维盲区；**最终不会输出几份割裂报告，而会合并成一份按风险和根因优先级排序的审计结论。**

## 最终产物

一次完整审计必须形成可长期保存的 Markdown 报告。

默认结构大致为：

```text
Full-Spectrum Review Report
├── 审计元数据 / exact revision
├── Executive Summary
├── P0/P1/P2/P3 总览
├── 建议修复执行顺序
├── P0 Critical Findings
├── P1 High Findings
├── P2 Medium Findings
├── P3 Low Findings
├── Positive Findings / Keep As-Is
├── Test / Verification Gaps
└── Evidence / Appendix
```

正式 finding 可以包括：

- `Defect`：实现或行为错误；
- `Business`：业务语义错误或不完整；
- `Reliability`：恢复、并发、状态等风险；
- `Performance`：有实际 workload 的性能/资源问题；
- `Accidental Complexity`：现有需求可以由显著更简单的充分机制完成，但当前额外层没有独立 requirement；
- `Optimization`：行为正确但成本明显不必要；
- `Maintainability` / `Security` / `Test Gap` 等。

其中 First-Principles finding 需要额外说明：

```text
Required outcome
Irreducible constraints / invariants
Minimum sufficient mechanism
Current mechanism
Accidental complexity delta
Simplification direction
Behavior-preservation plan
```

所以不能只写一句“这里太复杂了”。

如果 AI 对目标仓库有写权限并且用户授权写入，优先遵循项目已有审计文档规范；没有现成规范时默认沉淀到：

```text
docs/reviews/<YYYY-MM-DD>-full-spectrum-review.md
```

PR 审查则可使用：

```text
docs/reviews/pr-<number>-<short-head>-full-spectrum-review.md
```

这样审查结果不会只存在于一次聊天里，而会成为项目本身可以继续跟踪、复审和修复的工程资产。

## 优先级

| 优先级 | 含义 |
|---|---|
| **P0 Critical** | 灾难性资金/数据损失、系统性 compromise、不可恢复生产状态 |
| **P1 High** | 现实条件下的重大 correctness、业务、状态、恢复、安全、性能或生产风险；核心路径上严重模糊 ownership/safety 的 accidental complexity 也可能达到 P1 |
| **P2 Medium** | 真实 defect、重要弱点、显著优化机会，或明显增加状态空间/失败面/运维与维护成本的 accidental complexity |
| **P3 Low** | 具体但非阻塞的低影响改进 |

没有当前 bug，不代表复杂度问题只能是 P3；但纯审美上的“我更喜欢这样写”也不能被拔高成 P1/P2。

最终报告严格按照 **P0 → P1 → P2 → P3** 排序，而不是按照文件顺序或者 AI 发现问题的先后顺序。

另外还会给出一个 **Recommended Execution Order**：如果先修一个错误 ownership / source-of-truth / responsibility boundary，就能让多层 guard、retry、state 或 recovery 一起消失，会优先建议修根因，而不是继续逐条打补丁。

## 为什么不做成一份巨型 Prompt

核心 `SKILL.md` 只负责审计流程、范围纪律和最终交付要求；具体审查知识放在 `references/` 中按需读取：

```text
full-spectrum-review/
├── SKILL.md
├── README.md
├── README.en.md
├── LICENSE
├── ACKNOWLEDGEMENTS.md
└── references/
    ├── first-principles-review.md
    ├── engineering-review.md
    ├── business-logic-review.md
    ├── optimization-review.md
    ├── finding-protocol.md
    ├── reporting-protocol.md
    └── trading-domain.md
```

这样既能做到全面，又不会让一份十几 k token 的固定 Prompt 挤占代码上下文并稀释注意力。

## Domain Pack

核心 Skill 保持领域无关。

当前包含 `references/trading-domain.md`，用于交易、量化和真实资金系统，额外检查：

- 行情/K 线时间语义和未来函数；
- backtest / simulation / live parity；
- order lifecycle 与 partial fill；
- UNKNOWN order outcome 和重复下单；
- position truth 与 restart reconciliation；
- tick / step / minimum notional / rounding；
- PnL、fee、funding 与数量守恒；
- 止损止盈等保护单；
- 自动交易与人工接管之间的 ownership。

后续可以继续增加支付、电商、账务、分布式系统、AI Agent 等 Domain Pack，而不需要改变核心审计流程。

## 安装

本仓库遵循 Agent Skills 的 `SKILL.md` 目录格式。把整个仓库 clone/copy 到对应客户端 Skill 目录即可。

```bash
# Claude Code，用户级
git clone https://github.com/liuyejinghong/full-spectrum-review.git ~/.claude/skills/full-spectrum-review

# Codex，用户级
git clone https://github.com/liuyejinghong/full-spectrum-review.git ~/.codex/skills/full-spectrum-review
```

常见项目级目录还包括：

```text
.claude/skills/
.codex/skills/
.cursor/skills/
.gemini/skills/
.github/skills/
```

## 使用方式

最简单的调用方式就是：

```text
使用 full-spectrum-review 对这个项目进行一次全面审计。
从第一性原理重新推导关键功能的最小充分机制，不要默认接受现有架构；同时审查代码、业务逻辑、架构、性能、稳定性和可精简项。验证并按 P0/P1/P2/P3 排序，最终把完整报告沉淀到仓库。
```

审 PR：

```text
使用 full-spectrum-review 全面审查 PR #123。
绑定 exact head，从第一性原理检查这次实现是否存在不必要复杂度，并全面检查受影响链路；最终按优先级生成并沉淀审查报告，存在 blocking finding 时给出 REQUEST_CHANGES。
```

## 设计原则

- 全面审计是默认行为；专项审查是显式例外。
- **先问最小充分机制，再接受现有实现。**
- 先理解系统和业务，再判断代码。
- 正确但无必要复杂的实现也可以是正式 finding。
- 第一性原理不是“越少越好”；真实 requirement / invariant 优先于简洁。
- 候选问题阶段追求高召回，正式 finding 追求高证据门槛。
- 测试是证据，不是真理，也不能证明现有架构有存在必要。
- changed lines 是审查起点，不是 reasoning 边界。
- finding 按根因去重，不按症状堆数量。
- 优化不仅是“跑得快”，还包括减少状态、责任、抽象和失败路径。
- 删除错误复杂度往往比继续增加 guard 更能提高长期稳定性。
- 最终交付必须让维护者清楚知道：**先修什么、为什么、哪些复杂度可以消失、如何证明改完仍然正确。**

## License

MIT
