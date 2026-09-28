# Syy-zimeiti-skills

个人维护的公开社媒研究 Skill，名称为 `syy-zimeiti-skills`。基于 Pongfi Research 改编，保留趋势、竞品、账号、评论需求、内容空白、品牌研究和选题能力。来源及修改见 [ATTRIBUTION.md](ATTRIBUTION.md)。

## 使用

在 Codex 中输入：

~~~text
$syy-zimeiti-skills
研究最近 30 天抖音上的 AI 教程内容。
先找对标账号与评论问题，推荐 5 个符合我账号定位的选题。
仅使用抖音数据，并给出原始链接、采集时间、样本规模与证据局限。
~~~

从 [SKILL.md](SKILL.md) 读取完整流程。主题不限于 AI，平台按用户请求指定；其他示例见 [examples/prompts.md](examples/prompts.md)。

## 数据准备

可使用当前已连接的公开数据工具，或用户提供的原始数据。没有平台数据时提供采样计划和探索性假设，不编造实时热度。

TikHub 是可选的远程连接，需要用户自己的密钥及可能收费的账户；本次只验证离线脚本，尚未验证真实账户连接。配套脚本只需 Python 3.9 或更高版本和标准库。

在 Windows PowerShell 中，从本文件夹运行：

~~~powershell
python scripts\estimate_cost.py --requests 20
python scripts\tikhub_mcp.py --help
python -m unittest discover -s tests -v
~~~

如果已有 Python 不在 PATH，使用它的完整路径替代命令中的 python。远程调用前，仅在本地设置 TIKHUB_API_KEY 环境变量，再按 SKILL.md 动态发现当前工具。不要将密钥写入仓库或聊天。

费用规划默认报告请求量和价格未知。只有显式提供单价范围时才输出假设性金额，不能代替服务商当前报价。

## 许可

MIT，完整许可见 [LICENSE](LICENSE)。保留原作者 Pongfi 的版权声明。上游第三方声明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
