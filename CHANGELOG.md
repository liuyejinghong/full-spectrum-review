# Changelog

本文件记录 `full-spectrum-review` Core Skill 的用户可见协议变化。

项目采用 Semantic Versioning。当前仍处于 `0.x` 阶段，因此在 1.0 之前，重要的协议重构也可能通过 MINOR 版本发布。`VERSION` 是当前 Core Skill 版本的权威来源。

Domain Pack 独立版本化；例如 Trading Pack 的版本记录在 `domains/trading/DOMAIN.md` frontmatter 中，不与 Core Skill 版本绑定。

> 说明：下面的早期版本根据仓库实际演进整理。当前仓库尚不要求每个版本都必须已有 Git tag 或 GitHub Release；后续正式发布时可以让 tag/release 与 `VERSION` 对齐。

## [trading-pack v3] - 2026-09-02

Domain Pack 独立版本化，本条目不影响 Core `0.7.0`。

### Added

- **源自真实生产事故复盘的领域条款**（30 篇实盘事故复盘 + 跨事故系统性审查的泛化蒸馏，不引用任何具体部署）：
  - Glossary 新增四个概念：Business obligation / Mechanism / Canonical proof / Runner（经济身份非小残仓）；
  - Domain Invariants 新增 11 条：退出/入场意图独立、禁止匿名不可逆动作（POST 前 mint cycle-bound identity）、可计算义务在触发前必有 durable intent、proof 缺失≠保护缺失、"风险已处置"≠"交易成功"（typed 结果）、degraded 态保护与 reduce-only 必须继续（按动作能力集建模）、信号被消费未执行必须可见可修、blocker 必须有清除路径、rollback 的 generation 安全、空恢复计划≠期望零保护、阈值穿越状态可从历史重建；
  - External Semantics 新增：限频执行边界（出口 IP）与实例边界错位、429 是升级封禁前的停止信号、closePosition 同向唯一性与 bridge-cancel-place、读回表示语义（quantity=0=全仓/省略字段归一/200 信封带失败码）、跨 endpoint 价格比较须精度归一、签名字节=发送字节、拒绝必须记录 venue 响应体；
  - Scenario Sweep 扩充：同 K 激活屏障（聚合 OHLC 无 bar 内顺序）、完成事件与数据可见性竞态、新鲜度归 last-processed generation、跨标的价基、失败下单须持久退避记录、提交时点重证仓位、重启瞬态窗口、canonical 先于外部分类、单 fill 不阻塞后续 ingest、事故闩锁跨重启、健康/修复路径同一 proof 合同、迁移窗口内真实 venue 事件；
  - 新增 **Notification & Alerting Semantics** 一节：机器码语义跨边界保留、稳定 typed 事故身份、durable intent 先于远端可用、优先级容量保留、进程健康≠业务链路活性；
  - Severity Context 新增"成对概念区分"清单（protected≠healthy、risk-handled≠succeeded、sent≠delivered、access=full≠能开仓、未核算损益保持 unknown 等十余对）；
  - Backtest parity 新增：历史复盘须分段回放当时生效配置并标注 provenance mode、未知枚举值在每个引擎 fail-closed、内部表示不得当语义标签。

### Changed

- Out of Scope 显式排除事故修复流程纪律（停止规则/attempt 预算/发版治理）——真实事故源，但属流程规则非领域真相。

## [0.7.0] - 2026-09-02

### Changed

- 审计产物落点重构：从"写入被审仓库 `docs/reviews/`"改为**当前工作区固定根** `<workspace>/fsr-reports/<target>/`（INDEX.md 台账 + 日期/PR 命名的报告）。一切路径相对工作区——不使用绝对路径、OS 特定位置或临时目录，跨 harness/平台行为一致；复审从同一位置读取先前状态。写入被审仓库降级为**显式授权的发布动作**（跟随仓库既有惯例，否则 `docs/reviews/`），并在工作区 INDEX 记录发布位置，不维护第二份可变台账。harness 完全无可写工作区时，完整交还报告与 index 增量。
- 动因：双路径试跑中报告被即兴放在仓库之外的临时目录，暴露协议对"审计产物的家"缺少唯一、平台无关的答案——工作区根是所有 harness 共有的锚点，统一了"在被审仓库内审计"与"从外部审计他人仓库"两种场景。

## [0.6.0] - 2026-09-02

### Changed

- Read-only 纪律语义澄清（`SKILL.md`）：只读约束的是**修改被审实现**，不是证据获取——运行被审仓库的测试、执行 benchmark/可复现实验（仓外沙箱或事后清理临时产物）、联网核实外部契约都是预期的证据工作，用尽 harness 与用户实际授予的一切能力。禁止自我加码（离线、只 read/grep、不跑测试）再当作纪律呈现："能跑测试却选择不跑的审计是在猜，不是在审"。环境真不具备的能力记为 evidence gap 并如实影响置信度。
- `references/orchestration-protocol.md` 新增 **Worker capability floor**：Lead 不得对 worker 施加比 harness/用户授权更窄的能力限制；常设约束只有三条（对被审实现只读、candidate-only、exact-revision 绑定）；worker 预期以测试/benchmark/实验为证据；harness 自身缺乏能力时记录为证据缺口，不当作自己的选择。

> 动因：v0.5.0 双路径试跑中 Lead 派工时自我施加了 no-network / read-grep-only 约束，导致部分 finding 只能静态推演并降档置信。限制应来自环境与用户授权，不应来自审计协议自身。

## [0.5.0] - 2026-09-02

外部复审（issues #1–#5）修正：

### Changed

- Core workflow 顺序修正（#1）：Select Domain Packs 提前到 First Principles 之前——领域 invariants / external semantics 是最小充分机制推导的输入，先推导后加载会把 essential domain complexity 误判为 accidental complexity；single-unit 与 multi-unit 模式的领域知识加载顺序就此一致，FP 步骤明确把 pack 语义作为约束输入。
- exclusive territory 改为 **primary ownership**（#2）：每个模块仍只有一个 primary owner 负责完整 local review，禁止同问题、同深度的重复审查；但允许其他单元带着明确声明的横切问题（ownership/source-of-truth 边界、端到端 invariant、domain lifecycle、跨模块资源路径）复查同一代码——distinct-question verification 不算重复，undifferentiated rescanning 才算。
- 串行回退的 packet 从"落盘"改为 harness-neutral 的 **recoverable coordination artifact**（#3）：真正的 invariant 是 packet / brief 在上下文压缩后可恢复，filesystem 只是实现之一（session scratch、harness artifact store 均可）；harness 无任何可恢复机制时诚实降级——记录 compaction risk、收窄审计波次或如实标注覆盖/结论限制，不假装等价执行。
- description 正向触发条件与正文对齐（#4）：去掉 "persisted findings" 前置（那是交付能力不是触发条件），改为"点名本 skill 或明确要求 comprehensive 审计"即触发；负面触发（ordinary / quick / diff-only review 不自动加载）保持不变。
- README 中英的 Coverage Ledger 表述区分 Depth（deep / sampled / none）与 Status（COMPLETE / PARTIAL / NOT_COVERED / INSUFFICIENT_EVIDENCE）两个维度（#5），与 `reporting-protocol.md` 权威定义一致。

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
