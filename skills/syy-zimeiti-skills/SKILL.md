---
name: syy-zimeiti-skills
description: 研究指定社交平台的趋势、对标账号、异常高表现内容、评论需求和选题机会，并输出可追溯的证据报告。适用于公开社媒数据研究；纯文案润色和视频剪辑不启用。
license: MIT
metadata:
  brand: Syy-zimeiti-skills
  version: 0.1.0
  language: zh-CN
  runtime: python>=3.9
---

# Syy-zimeiti-skills

把公开社媒样本转成可追溯的趋势、竞品、用户需求与内容机会。主题可以是任意赛道、品牌、产品、人物、账号或话题。支持单个平台研究，也支持用户指定的跨平台比较。

本 Skill 基于 Pongfi Research 改编，来源提交及改动见 [ATTRIBUTION.md](ATTRIBUTION.md)，原作者版权与许可见 [LICENSE](LICENSE)，第三方说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## 任务输入与研究模式

先从请求中确定主题、目标、平台、地区或语言、时间窗、样本规模、预算和输出要求。未指定时间窗时先按最近 30 天规划，实际覆盖范围按数据报告。主题缺失且无法从对话确定时，先询问主题。

保留用户指定的平台和范围；若平台无数据，说明缺口。用户要求全平台时先按研究价值选择 3–5 个平台做样本验证，再决定是否扩展。未指定平台时参考 [平台选择](references/platforms.md)。

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

具体研究步骤见 [研究方法](references/research-playbooks.md)。涉及创作者、对标或选题时，同时读取 [创作者研究补充](references/creator-research.md)。

## 数据与工具选择

优先使用用户指定或当前已连接的公开数据工具。用户提供的原始文件也可作为数据源；截图只支持画面可见的内容和指标。无实时数据工具时可交付采样计划或现有资料分析，明确证据截止时间，不伪造平台查询结果。

TikHub 辅助客户端是可选连接方式，需要用户自己的账户、网络和 TIKHUB_API_KEY。按需要运行：

~~~powershell
python scripts\tikhub_mcp.py health
python scripts\tikhub_mcp.py platforms
python scripts\tikhub_mcp.py discover --platform douyin --query 'search video keyword'
python scripts\tikhub_mcp.py list-tools --platform xiaohongshu
python scripts\tikhub_mcp.py call --platform douyin --tool CURRENT_TOOL_NAME --args-file args.json --out research-output\raw\douyin\search.json
~~~

命令以本 Skill 文件夹为工作目录，先定位已有 Python；不在 PATH 时用可执行文件的完整路径。上例工具名是占位示例，实际工具名及参数必须从当前 tools/list 返回的 schema 中选择。远程客户端的协议行为沿用上游，真实账户连接未经本次离线测试验证。

密钥只从环境变量读取，不写进报告或仓库。Windows 可在本地设置：

~~~powershell
$env:TIKHUB_API_KEY = 'YOUR_API_KEY'
~~~

初始化 MCP → tools/list → 选择真实工具 → tools/call → 保存响应。工具目录变化时重新发现，不猜端点。优先寻找搜索、榜单、账号、帖子详情、评论、字幕等与目标相符的工具。

## 采样与分析

1. 使用 [研究简报模板](templates/research_brief.md) 固定范围、取样计划和数据限制。
2. 规划搜索、分页、账号、帖子详情、评论和字幕等请求量。先验证 1–3 个样本，检查字段、时间及时区、分页和内容是否匹配任务。
3. 明显扩大采样前说明预计请求量和用户预算；只有账户或当前价目表能支持实际费用。已有授权覆盖的采集继续执行；需要新增付费授权时先取得授权。
4. 原始响应按平台保存到 research-output/raw，另存标准化数据、分析和报告；记录来源链接或帖子 ID、采集时间、查询词、时间窗和覆盖量，保留原始证据。
5. 依据实际 schema 建立字段映射。缺失字段保留 null，不用其他指标推算缺失播放、完播、转化或粉丝数。
6. 在同平台、同账号和可比时间窗内计算表现，再解释差异；样本偏差、缺字段和过小基线都要说明。
7. 评论提炼聚焦问题、使用障碍、购买顾虑、比较需求与未回答的问题，保留样本量和可核实例子。热门评论不能代表全部观众。
8. 为内容空白和选题补充用户受众、经验、可展示素材和制作能力的匹配判断。缺少信息时标注暂定判断。

辅助命令：

~~~powershell
python scripts\estimate_cost.py --requests 20
python scripts\estimate_cost.py --requests 20 --low 0.001 --high 0.01
python scripts\normalize.py --input raw-posts.jsonl --mapping mapping.json --constants '{"platform":"douyin"}' --out research-output\normalized\posts.jsonl
python scripts\score_posts.py research-output\normalized\posts.jsonl --out research-output\analysis\posts-scored.jsonl
~~~

第二条命令的单价只是调用者明确输入的假设，不表示 TikHub 当前报价。未提供单价时报告价格未知。标准化与指标计算详见 [评分方法](references/scoring.md)。脚本只接受明确映射，不保证直接识别所有 API 包装结构。

互动率只有点赞、评论、分享和有效播放字段都存在时计算；实际返回的 0 是有效观测值。相对表现采用同平台账号样本中位数，报告说明它是样本基线。不同平台的原始播放量、浏览、曝光、收藏与分享定义可能不同，不直接混排。

## 结论与交付

按任务规模使用 [报告模板](templates/report.md)，小任务可省略无关章节。中文结论优先，再给证据、覆盖范围与方法。

主要结论区分直接观测、计算结果、分析推断和探索性假设，遵循 [证据规则](references/evidence.md)。没有可比时段时不要断言增长；搜索结果供给少不等于整个赛道无人做。

每个推荐选题给出具体问题、样本依据、原始来源、取样时间、用户需求、供给判断、账号适配理由、素材需求、推荐平台和证据置信度。有充分依据时按 references/scoring.md 给机会分数，否则保留定性判断。分数是研究优先级，不是播放或收益预测。

遇到原始口播稿缺失时标记 script_lost，不从标题、封面和数据还原原稿。创作建议使用用户自己的经验、素材和表达。

## 故障与边界

仅处理公开或用户有权提供的数据，遵循 [数据使用边界](references/safety.md)。不采集私信或私密账号，不推断个人敏感属性，不绕过访问控制。

- 401/403：报告密钥或权限问题，不反复重试。
- 402：说明余额或付费要求，停止扩大采样。
- 429：降低请求频率，遵守 Retry-After；仍失败则记录。
- 5xx 或网络故障：有限次数重试，持续失败时报告数据缺口。
- 参数变化：重新读取工具 schema；缺字段时保留 null。
- 平台失败：已有授权覆盖的其他指定平台可以继续，报告中说明覆盖不完整。
