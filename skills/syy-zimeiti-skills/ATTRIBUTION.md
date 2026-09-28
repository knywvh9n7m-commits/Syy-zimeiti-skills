# 来源与改编说明

- 上游项目：https://github.com/s15039733700-cpu/Pongfi-Skills
- 上游 Skill：`skills/pongfi-research`
- 上游作者声明：`Copyright (c) 2026 Pongfi`
- 来源提交：`ed51f7cf503bcf8cd4cb42fbfc59b0be705ee025`
- 检查与改编日期：2026-09-28
- 许可：MIT，全文见本文件夹的 [LICENSE](LICENSE)。

## 个人版本 0.1.0

本版本以 `syy-zimeiti-skills` 发布本地 Skill，显示名称为“Syy-zimeiti-skills”。使用新的入口说明和 Codex 元数据，增加创作者研究约束、Windows 命令和离线使用说明；保留上游研究模式、标准化、相对表现分析、MCP 辅助代码、参考资料和模板。

修改 `score_posts.py`：缺失的点赞、评论、分享数据不再视为零，完整互动率只有在所需字段均有效时才计算；拒绝负数、非有限数字和布尔值作为计数。

修改 `estimate_cost.py`：删除未经验证的默认单价。调用者可显式提供单价范围用于假设性规划；未给单价时只报告请求量和价格未知。

修改 `tikhub_mcp.py`：更新客户端名称与版本；远程协议行为沿用上游，尚未通过真实 TikHub 账户验证。

上游关于 TikHub 和架构参考项目的声明原样保留在 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。本版本是公开注明来源的改编作品。
