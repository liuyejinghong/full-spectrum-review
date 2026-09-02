# Full-Spectrum Review

一个**模型无关**的开源 Agent Skill，用于独立的软件工程审查。

它不把所有审查要求塞进一份巨型 Prompt，而是拆成三个彼此独立的审查轴：

| 审查轴 | 核心问题 |
|---|---|
| **Engineering Review** | 实现本身是否正确、可靠、安全，并且和上下游正确集成？ |
| **Business Logic Audit** | 系统实际执行的行为，是否真正符合业务/领域现实？ |
| **Optimization & Simplification Review** | 在保持必要行为不变的前提下，能否用更少代码、状态、成本、复杂度和故障面完成同样目标？ |

三个方向先独立生成候选 finding，再通过统一的证据协议验证，并按根因去重。

## 为什么拆成三个方向？

不同 reviewer 应该被允许从不同角度得出相反建议。

Engineering reviewer 可能认为“这里应该再加一个保护”；Optimization reviewer 应该可以反问：“这个保护是不是在补偿一个错误的 ownership 或重复状态模型？”；Business reviewer 则负责确定无论怎么实现，都必须保持哪些业务 invariant。

这种结构比让所有模型吃同一张超长 checklist 更能保持第三方审查的独立性。

## 目录

```text
full-spectrum-review/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── LICENSE
├── ACKNOWLEDGEMENTS.md
└── references/
    ├── engineering-review.md
    ├── business-logic-review.md
    ├── optimization-review.md
    ├── finding-protocol.md
    └── trading-domain.md
```

`SKILL.md` 故意保持精简；详细检查项放进 `references/`，只有对应审查轴需要时才加载，避免浪费上下文和稀释注意力。

## 安装

本仓库遵循开放的 Agent Skills `SKILL.md` 格式。把整个仓库 clone/copy 到你的 AI 客户端 Skill 目录即可。

例如：

```bash
# Claude Code，用户级
git clone https://github.com/liuyejinghong/full-spectrum-review.git ~/.claude/skills/full-spectrum-review

# Codex，用户级
git clone https://github.com/liuyejinghong/full-spectrum-review.git ~/.codex/skills/full-spectrum-review
```

不同客户端的项目级目录可能不同，常见位置包括：

```text
.claude/skills/
.codex/skills/
.cursor/skills/
.gemini/skills/
.github/skills/
```

如果你的 Agent 支持 Agent Skills 但使用其他发现路径，按该客户端文档把此目录放进去即可。

## 使用示例

### 全方位审查

```text
Use the full-spectrum-review skill to review PR #123.
Run Engineering, Business Logic, and Optimization/Simplification as independent passes, then verify and deduplicate findings. Bind the verdict to the exact PR head.
```

### 只审业务逻辑

```text
Use full-spectrum-review in Business Logic mode.
Reconstruct the domain rules and invariants before judging the implementation. Focus on business-semantic mismatches rather than code style.
```

### 只做优化/精简审查

```text
Use full-spectrum-review in Optimization & Simplification mode.
Preserve required behavior. Prioritize deleting duplicated state, responsibility, recovery machinery, and redundant work over adding new abstractions or micro-optimizations.
```

### 真实资金交易系统

```text
Use full-spectrum-review with the trading-domain pack.
Review the exact commit for engineering correctness, business semantics, and behavior-preserving simplification. Treat unknown exchange/order state as something that requires reconciliation rather than an implicit success/failure.
```

## 核心设计原则

- 专项独立审查优于一份巨型 checklist。
- 先还原 specification / domain，再判断代码。
- 候选发现阶段追求高召回；真正发布 finding 时追求高证据门槛。
- 测试是证据，不是真理。
- changed lines 是审查起点，不是 reasoning 边界。
- 真实可达的失败场景值得审；仅理论上可构造的不算。
- 优化必须保持业务行为，并解释被删除责任由谁承担。
- 减少重复状态和 ownership 模糊，往往比继续加 guard 更能提高稳定性。
- PR verdict 应尽可能绑定 exact head SHA。
- finding 数量不是审查质量指标。

## Domain Pack

核心 Skill 保持领域无关。需要时再加载额外领域包。

当前包含：

- `references/trading-domain.md`：行情时间语义、未来函数、回测/模拟/实盘一致性、订单生命周期、部分成交、未知订单结果、幂等、仓位 truth、重启 reconciliation、精度、PnL/费用、保护单、人工接管等。

后续可以继续增加支付、电商、金融账务、工作流等领域包，而不改变三轴 Review 架构。

## License

MIT
