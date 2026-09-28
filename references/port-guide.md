# 迁移到其它大模型 / Agent

节流 的规则是**纯文本**，因此任何能读 system prompt、规则文件或 SKILL.md 的 Agent 都能用。下面给出各平台的接入片段。核心规则只有一段，复制即用。

## 通用最小规则（可直接粘贴到任意 Agent）

> 用极简中文回复，砍掉冗余表达但保留全部技术信息：删除客套/铺垫/模糊词，结论前置，列表/表格优先；启用符号表（因此/所以/导致→`→`；并且/而且→`+`；或者→`/`；例如→如；大约→`≈`；成功→`✅`；失败→`❌`；增→`↑`；减→`↓`）。保留代码、命令、术语、路径、错误原文、数值、否定/例外词。遇破坏性操作或安全风险自动切回正常中文。分 温和 / 标准 / 极限 三档，默认标准。

---

## WorkBuddy（本仓库默认）

把本目录放到用户级 skills 即可：

```
~/.workbuddy/skills/economize-on-spending/
```

## Claude Code / Claude.ai

- 项目级：把上面「通用最小规则」追加到项目 `CLAUDE.md`
- 命令级：在 `~/.claude/commands/compress.md` 建 slash command，正文引用本 SKILL.md

## OpenAI Codex CLI

写入项目 `codex.md` 或 AGENTS 规则文件，首行注入规则。

## Cursor / Windsurf

- Cursor：写入项目 `.cursorrules` 或 `.cursor/rules/*.md`
- Windsurf：写入 `.windsurf/rules/*.md`

## Gemini CLI

写入项目 `GEMINI.md`。

## Aider

写入 `CONVENTIONS.md`，并在 `.aider.conf.yml` 里引用；或启动加 `--read CONVENTIONS.md`。

## 任意 Chat / API

将 `SKILL.md` 正文作为 system prompt 片段注入即可，无需任何插件。

---

## 触发词（可随平台改名）

- 中文：`简短点` / `简洁` / `省点 token` / `压缩一下` / `别啰嗦` / `节流` / `节源`
- 解除：`恢复正常` / `正常模式`
- 切档：`节流 温和|标准|极限`

> 不同模型对触发词的敏感度不同；若某模型不响应，可在其规则文件里把触发词写得更直白，例如「回复一律用极简中文」。
