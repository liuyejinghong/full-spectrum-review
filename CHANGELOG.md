# Changelog

本文件记录 `full-spectrum-review` Core Skill 的用户可见协议变化。

项目采用 Semantic Versioning。当前仍处于 `0.x` 阶段，因此在 1.0 之前，重要的协议重构也可能通过 MINOR 版本发布。`VERSION` 是当前 Core Skill 版本的权威来源。

Domain Pack 独立版本化；例如 Trading Pack 的版本记录在 `domains/trading/DOMAIN.md` frontmatter 中，不与 Core Skill 版本绑定。

> 说明：下面的早期版本根据仓库实际演进整理。当前仓库尚不要求每个版本都必须已有 Git tag 或 GitHub Release；后续正式发布时可以让 tag/release 与 `VERSION` 对齐。

## [0.4.0] - 2026-09-02

### Added

- `references/orchestration-protocol.md` 新增上下文节省纪律（全部通过方法/结构控制重复阅读，不设字数预算，不因长度截断信息）：
  - Shared Audit Brief 逐行准入测试（能否改变某 worker 的检查范围或解读方式），以筛选控制体积而非截断；
  - 单元独占文件管辖（exclusive territory）：每个模块只归一个单元审，跨边界只读记 concern，防止隐性重读；
  - Reviewer Packet 内容选择：候选证据完整保留（packet 漏掉的候选随 worker 上下文消失），排除的只有过程叙事与源码预消化，不设长度上限；
  - Lead 按影响分配核验深度：P0/P1 与跨单元争议候选直接重开源码核验，轻量候选经引用与一致性核验——力度重新分配但不降低 evidence bar，不因省力丢弃候选；
  - Phase 2 跟进单元必须先说出要解决的"活性问题"（仍未解决且现有 packet 未回答）；
  - 串行回退的 Packet 落盘到会话暂存（不入被审仓库），synthesis 时重载，抗上下文压缩；
  - 单元数量由架构边界决定，合并会重叠的单元、仅在单单元过大时拆分，不设目标数量。
- `SKILL.md` 新增显式执行分级（Execution sizing）：single-unit / sequential-units / parallel-units 三档，小目标单单元模式为一等公民。

### Changed

- `SKILL.md` description 改为显式调用语义：仅当用户点名本 skill 或明确要求全面审计时触发，普通/快速/diff-only review 请求不自动加载（重协议不劫持日常 review）。
- Terminal result 拆分为 merge verdicts（APPROVE / APPROVE_WITH_NON_BLOCKING_FINDINGS / REQUEST_CHANGES）与终止状态（HEAD_DRIFT / INSUFFICIENT_EVIDENCE）两组。
- Coverage 状态统一为大写（COMPLETE / PARTIAL / NOT_COVERED / INSUFFICIENT_EVIDENCE），与 `reporting-protocol.md` 权威定义一致。
- `SKILL.md` Versioning 一节瘦身，版本政策细节移至 CHANGELOG 开头。
- README 中英双语重写：价值前置、术语中文化、新增真实 finding 缩略示例与"何时用/何时别用"。

## [0.3.0] - 2026-09-02

### Added

- 新增模型无关的 `references/orchestration-protocol.md`：
  - 大型审计可拆成有界 Audit Units；
  - harness 支持 worker/subagent 时可并发执行；
  - 不支持时按相同边界串行退化；
  - Shared Audit Brief；
  - Reviewer Packet；
  - 独立 first pass；
  - cross-boundary verification；
  - Lead/Coordinator 统一核验、根因去重和最终裁决。
- 新增正式 Domain Pack 架构：`domains/_CONTRACT.md` + `domains/<domain>/DOMAIN.md`。
- Trading Domain Pack v2，补充交易所机制、账户级安全、多实例 ownership、触发语义、持仓/保证金模式和长期 instrument lifecycle。
- 新增 Coverage Ledger、稳定 Finding ID、Finding lifecycle status 和 re-review audit ledger。
- 新增 `references/example-finding.md` 作为完整 finding 范例。
- 新增 `VERSION` 与本 `CHANGELOG.md`。

### Changed

- First Principles 与 Optimization 职责边界重构为：
  - First Principles = **Necessity**（机制是否应该存在）；
  - Optimization = **Cost**（已证明必要后，实现成本是否合理）。
- Accidental Complexity finding 强制进行 disconfirmation：必须主动调查“该层为什么存在”，否则只能作为 observation/hypothesis。
- Business Logic Review 改为动态建立 `Business Authority Map`；无法确认业务意图时进入 `Open Questions for the Maintainer`。
- 报告从一次性快照升级为可复审的持久审计记录。
- Core 不再 hard-code Trading Pack；一个项目允许加载 0..N 个 Domain Packs。
- 审计授权明确为默认只读；报告写权限不等于业务代码修改授权。
- Repository write access 与 review-platform API access 明确分离。

### Removed

- 删除旧 `references/trading-domain.md`，迁移到 `domains/trading/DOMAIN.md`。
- 删除 First-Principles 与 Optimization 之间大量重复的 necessity/simplification 规则。

## [0.2.0] - 2026-09-02

### Added

- 默认行为从“多轴 review”升级为完整 Full-Spectrum Audit。
- 强制第一性原理重建：Required Outcome、Irreducible Constraints、Required Invariants、Minimum Sufficient Mechanism。
- Accidental Complexity 作为正式审计 finding 类型。
- 持久化 canonical Markdown 审计报告。
- P0 / P1 / P2 / P3 统一优先级与 Recommended Execution Order。
- Positive Findings / Keep-As-Is 与 Evidence / Verification Gaps。

### Changed

- Engineering / Business Logic / Optimization 从独立最终报告改为内部 reasoning lenses；最终只输出一份统一审计结论。
- 仓库默认 README 切换为中文，英文说明迁移到 `README.en.md`。

## [0.1.0] - 2026-09-02

### Added

- 初始模型无关 Agent Skill。
- `SKILL.md` + progressive-disclosure `references/` 结构。
- Engineering Review、Business Logic Audit、Optimization & Simplification 三个独立 reasoning axes。
- Finding verification、exact-head discipline、root-cause deduplication 与 Trading domain reference。
- 中文/英文 README、MIT License 与 acknowledgements。
