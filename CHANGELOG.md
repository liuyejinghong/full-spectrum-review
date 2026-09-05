# Changelog

本文件记录 `full-spectrum-review` Core Skill 的用户可见协议变化。

项目采用 Semantic Versioning。当前仍处于 `0.x` 阶段，因此在 1.0 之前，重要的协议重构也可能通过 MINOR 版本发布。`VERSION` 是当前 Core Skill 版本的权威来源。

Domain Pack 独立版本化；例如 Trading Pack 的版本记录在 `domains/trading/DOMAIN.md` frontmatter 中，不与 Core Skill 版本绑定。

> 说明：下面的早期版本根据仓库实际演进整理。当前仓库尚不要求每个版本都必须已有 Git tag 或 GitHub Release；后续正式发布时可以让 tag/release 与 `VERSION` 对齐。

## [0.12.0] - 2026-09-05

小优化（additive only，core 三处加段 + schema 两可选字段 + trading 包两条 invariant + 1 个回归 case + 自检两项）。来源：2026-09-05 AItrading 全量审计的独立复核（10/10 CONFIRMED，但发现三类协议漏：行号引用漂移、默认关闭/暂停路径的 P 级通胀、收据时间声明与真实 wire 语义脱节）。

### Added

- **Exposure / Frequency 纪律**（`finding-protocol.md`）：conditional header 加 `Blast`（live-active / tool-active / research-default-on / research-default-off / paused / unknown）与 `Frequency`（measured / inferred）；P1 需同时满足 active exposure + 可达生产/资金/状态路径 + 真实触发，默认关闭/暂停/无现场量测封顶 P2；Reachability 必须声明 measured 还是 inferred。
- **证据钉死**（`reporting-protocol.md`）：P0/P1 必须带原文 mechanism 片段 + 在 bound revision 上重开源码重钉 `path:line`，漂移显式注明；Skill 经 git 安装时用 `git rev-parse HEAD` 取 revision，取不到记 `revision: unavailable` + 原因。
- **Schema 两可选字段**（`schemas/finding.schema.json`）：`blast` / `frequency` 枚举，JSON 导出与工具可用，prose 仍是唯一权威。
- **Trading 包 v4→v5**：Backtest parity 加 bar 时间口径端到端可追溯（ingest→wire→engine→receipt 四时区分，signal 腿 validator 不能证明 execution 腿）；Notification 加调度双向独立与 wake 合并显式化。
- **evals case-07**（stale-evidence-default-off guard）：陈旧行号复述与默认关闭 P1 通胀双陷阱；`REGRESSION.md` 通过线 6/6→7/7。
- **自检两项**（`scripts/validate_fsr.py`，仅 stdlib）：`domains/*/DOMAIN.md` frontmatter 必带 version + last-verified；evals 夹具数必须等于 REGRESSION 期望数。

## [0.11.0] - 2026-09-04

小优化（additive only，两条协议各加几行 + 1 个回归 case）。来源：freqtrade 首审的 #13529 教训（parity 缺口是已知权衡，却被当 fresh finding 发布）。

### Added

- **Stated-rationale 检查**（`finding-protocol.md`）：提议新机制/测试/契约的 finding，发布前先查 maintainer 在先立场（docs limitations、ADR、issue 记录）；有明确拒绝或接受理由 → ACCEPTED-with-rationale 或 Open Question。反证从"为什么这层存在"推广到"为什么这个东西不存在"。
- **测试环境探针**（`orchestration-protocol.md` Phase 0）：开工先探测试执行能力；跑不起来记一次 wave 级证据缺口（全波置信封顶），不再逐 finding 重复。
- **evals case-06**（accepted-tradeoff guard）：有文档化权衡在先时，不断言修复、必须引用权衡；无引用发布 parity 诉求即挂。

## [deploy-pack v3] - 2026-09-04

Domain Pack 独立版本化，本条目不影响 Core `0.10.0`。来源：独立渐进交付实现的收敛验证（Argo Rollouts canary/pause/abort 语义、Flagger 度量门禁自动 promotion/rollback、SRE Workbook canarying 六原则）。

### Added

- Domain Invariants +1：前一 artifact 在回滚窗口内必须可用（retention 短于窗口 = 回滚路径作废）。
- Scenario Sweep +3：canary 只看聚合健康而分群服务指标分化（评估先天失明，要求按群拆分）；重叠并发 rollout（信号污染，一次只跑一个 canary）；单 artifact 打包多个可独立回退变更而无分离机制（回滚粒度丢失）。
- 口音裁决：`Generation` 一词保留——glossary 内明确定义即脱口音，与 trading 包删除未解释用法不冲突；若真实用户产生混淆再改名。

### Changed

- 包头来源声明扩为三管线（事故复盘 / runbook 事实链 / 独立参考收敛），点名三家外部源。

## [deploy-pack v2] - 2026-09-04

Domain Pack 独立版本化，本条目不影响 Core `0.10.0`。来源：`docs/releases/` 收据层的逐事务事实（canary→rollback→永不重发链、QUALIFICATION BLOCKED 队列、second-failure 停线、平台/产品分离）。

### Added

- Domain Invariants +2：失败候选永久退役（下一 attempt 必须是新 source + 新身份 + 新授权，失败收据只作不可变证据）；terminal receipt 顶层必须携带决定性拒绝原因（通用 code + 原因埋 side log = 不可诊断终态，不得据此提交下一目标）。
- Scenario Sweep +2：验收 gate 耦合无关验证导致 fail-closed 僵局（gate 按动作自身前置条件定界）；产品发版夹带部署工具升级而无独立平台验收（tooling 与产品独立版本，先验 tooling 身份再当冻结输入消费）。

## [0.10.0] - 2026-09-04

无规范性协议变更（additive only）。新增：deploy pack v1（独立版本化）、finding/INDEX JSON schema、自检脚本、回归网。

### Added

- **Deploy Domain Pack v1**（`domains/deploy/`，独立版本）。来源：AItrading 生产发版事故复盘（08-17/18 跨代 rollback 拼接、08-07 price-basis 迁移自报成功、08-21 preflight 语义身份锁死、08-03/04 与 08-20/21 发版失败链）+ 发版 runbook 的单一事实链（exact source → 一次构建 → 冻结 manifest → 单目标单事务 → terminal receipt）+ 参考实现收敛（rollback 演练、smoke 与 health 区分、digest pinning、expand/contract 迁移、flag 生命周期）。核心条款：单一不可变事实链、manifest 唯一权威、rollback generation 安全、preflight 只读、恢复复用发版路径、terminal 闭环绑定、发版不改 access/mode、canary 首败停、迁移精确性、old-running≠recovered、禁 artifact 外 live 修改。Pack 只裁决发版机制，不宣布远程现场一致性（机制 vs 现场，见 pack 内 Out of Scope）。
- **`schemas/finding.schema.json` + `schemas/index.schema.json`**：canonical finding header 与 INDEX.json 的机校验形式。Markdown 报告仍是唯一权威产物；schema 只约束 JSON 导出与工具，不约束 prose。
- **`scripts/validate_fsr.py`**（仅 stdlib）：版本号三处一致（VERSION/CHANGELOG/README）、markdown 围栏配平、必需文件存在、`fsr-reports/**/INDEX.json` 枚举校验。
- **`evals/` 回归网**：召回网而非排行榜。5 个 must-catch/must-not-publish case（gate key 穷举、跨代 rollback、匿名动作、proof 缺失急救单、无历史复杂度反证下限）+ 跑法与发版门（core MINOR 前必跑，红灯挡发版）。

> 动因：market 对标（Nordic hygiene 可学：schema、validator、范例；tiers/edit-mode/lens-workers 与 FSR 立场冲突不学，见讨论备忘）+ 发版面审计需求（交易系统下次审计 Deployment/operations 正式 Unit）。回归网回答"协议改动是否悄悄致盲"，不定 prose 质量分。

## [0.9.0] - 2026-09-04

评审讨论驱动的硬化（issue-style 备忘见 `.omo/FSR-OPTIMIZATION-NOTES.md`，共识"不做的"两项未入：硬预算上限、通用检查单）：

### Added

- **计划枚举三清单**（`orchestration-protocol.md` Phase 0）：入口点 / 重要可变事实 / 外部边界，机械枚举自消费源码，每项必有归属 Unit 或显式 `none`+原因；Coverage Ledger 防"说了没做"，本规则防"没想到"。枚举出的有界集合自动落入 v0.8.0 穷举规则。
- **多波次收敛**（`reporting-protocol.md`）：audit wave 声明本波覆盖的 Unit；推迟项记 `NOT_COVERED`（`deferred to next wave`）为计划内状态；同一台账跨会话收敛。大库不再需要单次 heroic pass。
- **INDEX 双轨**（`reporting-protocol.md`）：`INDEX.json` 为机器真相源，`INDEX.md` 由其渲染；禁止只手改 markdown 单边。
- **Pack 不适用声明**（`reporting-protocol.md` Audit Metadata）：看过但判定不适用的 pack 记一行原因。
- **报告阅读契约**（`reporting-protocol.md`）：1–5 节为决策层（可独立定级），6 节之后为修复层。
- **Lead 复述标准**（`orchestration-protocol.md` Phase 3）：每条 P0/P1 Lead 必须用自己的话复述 mechanism（一句），写不出则降为 observation/evidence gap。卡出口，不加作业步骤。
- **Keep-As-Is 前置引用**（`finding-protocol.md`）：Accidental Complexity 证明须引用或推翻一条 Keep-As-Is 条目（含理由），批评与保护清单挂钩。
- **协议变更迁移规则**（`finding-protocol.md` Stable identity）：protocol 变化导致的结论变化保留 ID，记录双版本+理由；禁止发新 ID 洗白重分类。
- **无历史替代取证下限**（`first-principles-review.md`）：无 git 历史时至少用 caller/consumer/config/test 中两源做反证基；做不到则保持 observation。"没历史"永不升级为 finding。
- **Pack 贡献接口**（`CONTRIBUTING_PACKS.md` 新文件 + README 声明）：外部 pack 提交路径与评审门；README 明示目前唯一 verified pack 是 trading。

> 动因：连续评审发现协议缺的三类东西——计划层防遗漏的机械动作（ledger 管不住"没想到"）、Lead 核验的出口标准（弱 Lead 会 rubber-stamp）、跨版本/跨会话的台账连续性（JSON 真相源、多波次收敛、ID 迁移规则）。全部按"卡出口、禁单边、不断账"收敛，未增加任何作业步骤清单。

## [0.8.0] - 2026-09-04

### Added

- **可枚举集合穷举规则（Enumerable-set completeness）**：gate / allowlist / key 表 / 参数注册表 / 枚举 / phase 清单 / 路由×鉴权矩阵 / 业务操作清单 / 生命周期 state×event 矩阵这类有界集合，默认 `deep + 穷举`，禁用 `sampled`——成员必须从消费该集合的源码/契约（而非描述它的注释/文档）逐个列出，并逐个定性为 `must-govern` / `covered-elsewhere`（注明兜底机制）/ `remove-or-fix`；无法定性的成员记为 evidence gap，不得隐式放行。Reviewer Packet 携带成员清单（含分类）；Coverage Ledger 行必须标注成员数与真相源（如 `gate keys 52/52, source: run_config producer`），`sampled` 对这类集合永远不能标 `COMPLETE`。
- Maintainability bar 下明确：必须相互一致的映射表复本（同一份 key 表抄多份、gate 表 vs 生产侧字段表）本身就是具体维护机制；finding 须出示复本、漂移（或缺失的漂移检测）与可致分歧的改动。优先单一真相源；复本保留时 gate 必须 diff 它们。
- Lead 职责 +1（第 13 条）：对 correctness / money-state / safety 路径上的有界集合强制穷举；Phase 3 核验深度豁免这类集合——不因影响分级降为引用核验。

> 动因：一次仓库级审计中，研究门禁的 key 表（`PARAM_KEYS` 32 个）以 `sampled` 合规交差，漏掉生产侧约 20 个经济字段；复审以穷举法逐字段定性才挖出核心问题。根因是协议只给了 publish 精度 bar，没有 discovery 召回 bar，且 `sampled` 的定义（representative, not exhaustive）为漏检提供了合法外衣。

## [trading-pack v4] - 2026-09-02

Domain Pack 独立版本化，本条目不影响 Core `0.7.0`。来源：市场监管框架（EU RTS 6、US SEC 15c3-5）与成熟开源参考实现（NautilusTrader / Hummingbot / Freqtrade / QuantConnect Lean / Jane Street 确定性仿真实践）的调研蒸馏。

### Added

- **新增 "Pre-Trade Controls & Kill Functionality" 一节**（监管蒸馏，控制类别非法条）：独立于策略代码的 pre-trade 护栏层、数值护栏（价格护圈/最大订单量值/每执行边界消息速率上限）、重复单与胖手指在入场前拦截、kill functionality（单操作撤全部挂单、降级态可达、独立于策略进程、须被测试而非仅存在）、护栏配置与策略部署分权、保护机制定期在压力形态下演练；明确标注"控制类别是领域真理，合规义务因辖区而异"。
- Backtest/Live Parity +5 条（参考实现收敛证据）：回测必须显式声明 bar 内排序假设（保守默认止损优先）、回测/实盘共享单一执行解释器（双引擎需显式 parity 契约 + 共享 fixtures）、实盘异步 vs 回测同步订单、同限价单因排队位置 fill 不同（分歧归因纪律）、组合测试运行在确定性模拟 venue 上（可注入时钟/网络 + 对抗性成交，持续随机化测试）。
- External Semantics +2：限频预算按 endpoint 权重共享单一加权池（参考收敛；按调用点计数/按实例退避是已知失败形态）、启动时先拉取 venue 已有挂单与仓位再做任何决策。
- Order/Execution Sweep +1：交易所侧保护单被手工撤销时系统须对照 venue 真实性检测缺席并重挂（保护在场性 enforced）。

### Changed

- 包头来源声明扩为三类（事故复盘 / 监管控制类别 / 参考实现收敛），"经验非定律"框定不变。
- `domains/_CONTRACT.md` 新增 **"Distilling pack content"** 一节：三条蒸馏管线（事故复盘→不变量、监管框架→控制类别、参考实现→收敛证据）+ 共同策展门五条（换系统通用性检验 / 去源系统口音 / 经验非定律 / 按 contract 归类 / 代价证据三选一：事故、监管强制、独立参考收敛）。供所有未来 pack 复用。

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

### Revised（同日修订，仍为 v3）

- 新增包级**"经验非定律"声明**：pack 内容是蒸馏自真实系统的审查经验（高基率 verify/challenge 问题），不是金科玉律——目标有证据的理由可以不同（记录理由而非强制合规），venue 实际契约与业务证据永远优先于 pack 假设，目标没有的特性条款自动不适用。同一原则写入 `domains/_CONTRACT.md`，由所有 pack 继承。
- 去源系统口音：匿名动作条款 "cycle-bound identity" → "绑定所服务仓位/交易的持久身份"；rollback 条款从 "generation" 改为朴素表述（venue 侧世界已前进则禁止盲恢复、只能前向对账）；新鲜度条款去掉 "processed generation" 术语；启动分类条款去掉 "canonical projection" 术语。
- Notification & Alerting 每条补交易后果锚点：误标止损在实盘中误导风险决策与事故分级、provider 故障不得永久吞掉终态成交通知、事故中例行通知不得挤占关键交易告警预算、接管期间自动动作不得被误读为人工指令、健康检查不触决策链时仓位可数小时无人管理。

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
