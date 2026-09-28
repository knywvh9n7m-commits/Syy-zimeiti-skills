# Syy-zimeiti-skills

个人维护的社交媒体研究 Skill，标识为 `syy-zimeiti-skills`。基于 [Pongfi-Skills](https://github.com/s15039733700-cpu/Pongfi-Skills) 的 `pongfi-research` 改编，保留 MIT 许可与原作者版权声明。

支持赛道发现、趋势扫描、对标账号、账号审计、异常高表现内容拆解、评论需求、内容空白、跨平台比较、品牌研究、选题生成与市场地图。平台和赛道由任务指定，不限定为 AI 内容。

## 在 Codex 中使用

将 `skills/syy-zimeiti-skills` 整个文件夹复制到个人 Codex skills 目录，安装后从下一轮对话开始使用：

```text
$syy-zimeiti-skills
研究最近 30 天抖音上的 AI 教程内容。
先用小样本找对标账号和评论需求，再给出适合我的 5 个选题。
每个选题附原始链接、采集时间、证据和局限。只研究抖音。
```

也可直接指定本仓库中的 `skills/syy-zimeiti-skills/SKILL.md`，按其中指令执行。Skill 文件夹自带 LICENSE，单独复制时也应一并保留。

## 数据方式

- 已连接的公开数据工具：优先使用用户指定或当前可用的工具。
- 用户提供的 JSON/JSONL、CSV、截图或原始口播稿：在可核实范围内分析，注明覆盖范围。
- TikHub：可选的远程数据连接，需要用户自己的 `TIKHUB_API_KEY`；服务可能收费。本次改编和离线测试没有调用付费接口。
- 没有平台数据：提供采样方案或探索性假设，不编造实时热度、点赞数、评论或爆款表现。

## Windows / PowerShell

配套脚本只需 Python 3.9 或更高版本，无第三方 Python 包。进入 Skill 文件夹后执行；如果 `python` 不在 PATH，可用本机已有 Python 可执行文件的完整路径替代。

```powershell
Set-Location .\skills\syy-zimeiti-skills
python scripts\estimate_cost.py --requests 20
python scripts\tikhub_mcp.py --help
python -m unittest discover -s tests -v
```

TikHub 工具发现和调用需要在本地设置环境变量。不要在聊天中发送真实密钥，也不要将其写入仓库。

```powershell
$env:TIKHUB_API_KEY = 'YOUR_API_KEY'
python scripts\tikhub_mcp.py discover --platform douyin --query 'search video keyword'
```

具体工具名和参数必须以当前服务返回的 schema 为准。Windows JSON 参数建议写入本地文件，再使用 `--args-file`，避免多层引号转义。

## 本次改编

- 使用个人名称、触发说明及 Codex 界面元数据。
- 增加 Windows 使用示例和创作者研究约束。
- 明确保留指定平台、区分趋势线索与实际表现、保留缺失数据、尊重账号定位。
- 修正互动字段缺失时仍计算完整互动率的问题。
- 费用规划默认只给请求数；只有提供单价假设时才计算金额，不冒充实时 TikHub 报价。
- 保留上游四个辅助脚本、研究模式、参考资料、模板及第三方说明。

来源版本和改动记录见 [来源与改编说明](skills/syy-zimeiti-skills/ATTRIBUTION.md)。后续可将此仓库上传到自己的 GitHub，并在 README 中保留来源说明。当前仅完成本地制作与安装，没有创建远程仓库。

## 许可

[MIT](LICENSE)，保留 `Copyright (c) 2026 Pongfi`。个人名称表示本地改编版本，不表示取得上游内容的独占版权。TikHub 的服务、商标、价格和条款独立于本 Skill。
