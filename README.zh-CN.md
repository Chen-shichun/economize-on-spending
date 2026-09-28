# 🪙 节流（Economize on Spending）· 跨模型极简通信层

> ✨ 让**任意大模型 / AI Agent** 用极简中文回复，砍掉 60–89% 输出 token，**技术信息零丢失**。

节流 是一个**模型无关（model-agnostic）**的极简通信 skill：把冗余的中文表达压缩掉、把信息密度提上来——结果又短又准、人能直接读懂。

---

## 🌱 缘起

在 WorkBuddy 上用「蓝色大肥鱼」（DeepSeek 的戏称）时，一长串回复把 token 哗哗烧光，看着用量很心痛。于是动手做了这个 skill。开发过程中，刚好在 B 站刷到「原始人」（genshijin）超压缩通信的推广视频，受其「删冗余、留信息」思路启发，参考并迭代优化出这套更贴合中文、可跨任意大模型 / Agent 的规则——砍掉 60–89% 输出 token，**技术信息零丢失**。省下的 token，就是省下的钱和耐心。

---

## 🤖 适用的大模型与 Agent

节流 的规则是纯文本，因此**任何能读 system prompt / 规则文件 / SKILL.md 的 Agent 都能用**：

| Agent / 平台 | 接入方式 |
|---|---|
| **WorkBuddy** | 直接安装本 skill（`~/.workbuddy/skills/economize-on-spending/`） |
| **Claude Code / Claude.ai** | 规则贴进 `CLAUDE.md`，或建 `/compress` 类 slash command |
| **OpenAI Codex CLI** | 写入 `codex.md` / 项目 AGENTS 规则 |
| **Cursor / Windsurf** | 写入 `.cursorrules` / 项目 rules |
| **Gemini CLI** | 写入 `GEMINI.md` |
| **Aider** | 写入 `CONVENTIONS.md` 或 `.aider.conf.yml` |
| **任意 Chat / API** | 把 `SKILL.md` 正文作为 system prompt 片段注入 |

> 🔗 各平台迁移模板见 [`references/port-guide.md`](references/port-guide.md)。

---

## 📊 效果实测（非估算）

同一题「2026 主流 AI 论文方向」，用 Qwen BPE 离线 tokenizer 实测：

| 版本 | token | 占比 |
|---|---|---|
| 正常中文 | 817 | 100% |
| 旧版节流 | 214 | 26% |
| **新版（结构规则）** | **87** | **11%（省 89%）** |

9 个关键事实（量化 / MoE / 57% / 水印 / AI4Science…）全部存活，无语义丢失。

---

## 🎚️ 三档强度

| 档 | 做法 | 场景 |
|---|---|---|
| 温和 | 删客套/模糊/铺垫，留完整句 | 对外沟通 |
| 标准（默认） | 敬语全删、短句、符号表+结构规则 | 自己用 |
| 极限 | 仅关键词+箭头，缩写泛滥 | 内部速记 |

- 🎯 触发：`简短点` / `简洁` / `省点 token` / `压缩一下` / `别啰嗦` / `节流` / `节源`
- 🚪 解除：`恢复正常` / `别节流了` / `正常模式`
- 🔁 切档：`节流 温和|标准|极限`

---

## 🛡️ 安全护栏（自动恢复为正常中文）

遇以下情况，临时切回正常中文讲清楚，再回到节流：

- 💥 破坏性操作确认（`rm -rf` / `DROP TABLE` / `force push` / 格式化）
- ⚠️ 安全警告 / 漏洞提示
- 🧩 LaTeX / 复杂 SQL / 正则边界等技术歧义
- ❓ 用户困惑或追问

**绝不改写的**：代码、命令、术语、路径、错误原文、数值、否定/例外词。

---

## ✅ 本地验证

```bash
cd ~/.workbuddy/skills/economize-on-spending/scripts
python throttle_test.py        # 17 项确定性用例，全过即健康
python ab_measure.py           # A/B token 实测（需 Qwen tokenizer）
```

---

## 📄 License

MIT — 见 [LICENSE](LICENSE)。
