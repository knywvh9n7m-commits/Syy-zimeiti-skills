---
name: syy-zimeiti-skills
description: 研究指定社交平台的趋势、对标账号、异常高表现内容、评论需求和选题机会，并输出可追溯的证据报告。适用于公开社媒数据研究；纯文案润色和视频剪辑不启用。
license: MIT
metadata:
  brand: Syy-zimeiti-skills
  version: 0.2.0
  language: zh-CN
  runtime: Codex or WorkBuddy; Python optional
---

# Syy-zimeiti-skills

把公开社媒样本转成可追溯的趋势、竞品、用户需求与内容机会。主题可以是任意赛道、品牌、产品、人物、账号或话题。支持单个平台研究，也支持用户指定的跨平台比较。

本 Skill 基于 Pongfi Research 改编，来源提交及改动见 [ATTRIBUTION.md](ATTRIBUTION.md)，原作者版权与许可见 [LICENSE](LICENSE)，第三方说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## 任务输入与研究模式

先从请求中确定主题、目标、平台、地区或语言、时间窗、样本规模、预算和输出要求。未指定时间窗时先按最近 30 天规划，实际覆盖范围按数据报告。主题缺失且无法从对话确定时，先询问主题。

保留用户指定的平台和范围；若平台无数据，说明缺口。用户要求全平台时先按研究价值选择 3–5 个平台做样本验证，再决定是否扩展。未指定平台时参考 [平台选择](references/platforms.md)（WorkBuddy：`@references/platforms.md`）。

按任务选取模式，可组合使用：

| 模式 | 解决的问题 |
|---|---|
| niche-discovery | 赛道与子赛道发现 |
| trend-scan | 近期主题、热词和变化 |
| competitor-discovery | 对标账号、品牌与代表创作者 |
| account-audit | 内容结构、发布节奏、近期基线 |
| viral-breakdown | 异常高表现内容及可能原因 |
| comment-mining | 高频问题、顾虑、反对点和教程需求 |
| content-gap | 样本中的未满足需求与供给情况 |
| cross-platform | 同一主题在指定平台的差异 |
| brand-product | 产品认知、反馈与竞品比较 |
| idea-generation | 有证据且适合用户的选题 |
| market-map | 参与者、主题、内容形态与需求地图 |

具体研究步骤见 [研究方法](references/research-playbooks.md)（WorkBuddy：`@references/research-playbooks.md`）。涉及创作者、对标或选题时，同时读取 [创作者研究补充](references/creator-research.md)（WorkBuddy：`@references/creator-research.md`）。

## 数据与工具选择

**默认走宿主自带能力，不调用付费数据接口。** 在 Codex 或 WorkBuddy 中使用当前可用的网页搜索、浏览器或公开页面读取工具，以及用户提供的链接、文件和截图。模型的研究与分析使用当前宿主的额度；这些额度不能购买第三方平台数据。不要因为环境里已有 TikHub Key、API Key 或付费连接就自动调用。只有用户明确要求使用某个外部收费来源、了解其费用并授权该来源后，才读取 [可选付费数据连接](references/paid-data.md)。

按 [公开网页采样](references/public-web.md) 搜索、验证 1–3 个页面、记录查询与覆盖范围，再继续。WorkBuddy 可通过 `@references/public-web.md` 读取同一资源。网页搜索结果只证明搜索索引返回了这些页面；打开来源并核对发布日期和可见字段，不能把索引时间当发布日期。单条视频、单个主页和平台热榜各有不同覆盖范围，不互相冒充。截图只支持画面可见的内容和指标。无可访问网页或原始资料时交付采样计划，明确不能验证的结论。

该入口保持 Codex/WorkBuddy 通用：不要写死宿主专有工具名、命令或额度。WorkBuddy 没有可用网页搜索时，先查看其当前可用的公开搜索或浏览器能力；不能访问则报告缺口，不自行安装收费插件或改用付费 API。

## 采样与分析

1. 使用 [研究简报模板](templates/research_brief.md) 固定范围、取样计划和数据限制。
2. 规划各平台查询词、排序/时间筛选、页数与评论样本。先验证 1–3 个来源的发布日期、字段、时区和内容是否匹配任务；记录无法访问的来源。
3. 公开网页采样可以在已有宿主能力范围内继续；若工具、连接器或外部 API 可能单独收费，先核实费用与授权，未获授权就停止该路径。
4. 保存可访问的页面链接、页面摘录或用户提供的原始资料；需要时另存标准化数据、分析和报告。记录采集时间、查询词、搜索页数、实际打开的页面数和去重后的内容数。不要把搜索结果总数当成已检查样本数。
5. 依据实际 schema 建立字段映射。缺失字段保留 null，不用其他指标推算缺失播放、完播、转化或粉丝数。
6. 只有同平台、同账号、可比时间窗和足够的可见指标时，才计算相对表现；有播放量时用播放量基线，缺播放量但有公开点赞数时可单独使用点赞基线，并标明 `relative_performance_basis=likes`。两种基线不能混排。没有基线时只说“该样本公开播放/点赞较高”，不要称为账号爆款。
7. 评论提炼聚焦问题、使用障碍、购买顾虑、比较需求与未回答的问题，保留样本量和可核实例子。热门评论不能代表全部观众。
8. 为内容空白和选题补充用户受众、经验、可展示素材和制作能力的匹配判断。缺少信息时标注暂定判断。

辅助命令：

~~~powershell
python scripts\normalize.py --input raw-posts.jsonl --mapping mapping.json --constants '{"platform":"douyin"}' --out research-output\normalized\posts.jsonl
python scripts\score_posts.py research-output\normalized\posts.jsonl --out research-output\analysis\posts-scored.jsonl
~~~

这些脚本仅在有结构化原始数据且当前环境有 Python 时使用；普通公开网页研究不需要 Python。标准化与指标计算详见 [评分方法](references/scoring.md)。脚本只接受明确映射，不保证直接识别所有页面结构。

互动率只有点赞、评论、分享和有效播放字段都存在时计算；实际返回的 0 是有效观测值。相对表现采用同平台账号样本中位数，报告说明它是样本基线，并写明基于播放还是点赞。点赞相对表现不能解释成播放或互动率。不同平台的原始播放量、浏览、曝光、收藏与分享定义可能不同，不直接混排。

## 结论与交付

按任务规模使用 [报告模板](templates/report.md)，小任务可省略无关章节。中文结论优先，再给证据、覆盖范围与方法。

主要结论区分直接观测、计算结果、分析推断和探索性假设，遵循 [证据规则](references/evidence.md)（WorkBuddy：`@references/evidence.md`）。没有可比时段时不要断言增长；搜索结果供给少不等于整个赛道无人做。

每个推荐选题给出具体问题、样本依据、原始来源、取样时间、用户需求、供给判断、账号适配理由、素材需求、推荐平台和证据置信度。有充分依据时按 references/scoring.md 给机会分数，否则保留定性判断。分数是研究优先级，不是播放或收益预测。

遇到原始口播稿缺失时标记 script_lost，不从标题、封面和数据还原原稿。创作建议使用用户自己的经验、素材和表达。

## 故障与边界

仅处理公开或用户有权提供的数据，遵循 [数据使用边界](references/safety.md)。不采集私信或私密账号，不推断个人敏感属性，不绕过访问控制。

- 页面要求登录或返回 401/403：记录不可访问；不绕过访问控制。
- 工具返回 402、付费墙或额外购买提示：停止该来源；宿主 AI 额度不能抵扣第三方费用。
- 429：降低请求频率，遵守 Retry-After；仍失败则记录。
- 5xx 或网络故障：有限次数重试，持续失败时报告数据缺口。
- 参数变化：重新读取工具 schema；缺字段时保留 null。
- 平台失败：已有授权覆盖的其他指定平台可以继续，报告中说明覆盖不完整。
