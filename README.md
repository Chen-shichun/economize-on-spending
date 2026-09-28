# 🪙 节流 (Economize on Spending) · Cross-Model Minimal-Communication Layer

> ✨ Make **any LLM / AI agent** reply in minimal Chinese — cut 60–89% of output tokens with **zero loss of technical information**.

Economize on Spending is a **model-agnostic** compression skill. It strips redundant Chinese phrasing and raises information density, so replies stay short, accurate, and human-readable.

---

## 🌱 Background

This skill was born from token pain: while using "Blue Fat Fish" (a playful nickname for DeepSeek) on WorkBuddy, long-winded replies burned through tokens fast and it hurt to watch the usage climb. So I started building Economize on Spending. While working on it, I happened to see a Bilibili promo video about "原始人" (genshijin), an ultra-compression communication skill. Inspired by its "drop fluff, keep info" idea, I studied it and iterated into this Chinese-first, model-agnostic rule set — making any LLM / agent reply in minimal Chinese, cutting 60–89% of output tokens with **zero loss of technical information**. Every token saved is money and patience saved.

---

## 🤖 Supported LLMs & Agents

The rules are plain text, so **any agent that can read a system prompt / rules file / SKILL.md can use it**:

| Agent / Platform | How to enable |
|---|---|
| **WorkBuddy** | Install this skill directly (`~/.workbuddy/skills/economize-on-spending/`) |
| **Claude Code / Claude.ai** | Paste rules into `CLAUDE.md`, or make a `/compress` slash command |
| **OpenAI Codex CLI** | Write into `codex.md` / project AGENTS rules |
| **Cursor / Windsurf** | Write into `.cursorrules` / project rules |
| **Gemini CLI** | Write into `GEMINI.md` |
| **Aider** | Write into `CONVENTIONS.md` or `.aider.conf.yml` |
| **Any Chat / API** | Inject `SKILL.md` body as a system-prompt fragment |

> 🔗 Per-platform migration templates: [`references/port-guide.md`](references/port-guide.md).

---

## 📊 Measured effect (not an estimate)

Same prompt "2026 mainstream AI paper directions", measured with an offline Qwen BPE tokenizer:

| Version | tokens | share |
|---|---|---|
| Normal Chinese | 817 | 100% |
| Old throttle | 214 | 26% |
| **New (structural rules)** | **87** | **11% (89% saved)** |

All 9 key facts (quantization / MoE / 57% / watermark / AI4Science…) survived with no semantic loss.

---

## 🎚️ Three intensity levels

| Level | Behavior | Use case |
|---|---|---|
| Gentle | Drop pleasantries/vagueness/lead-ins, keep full sentences | External communication |
| Standard (default) | Drop honorifics, short sentences, symbols + structure rules | Personal use |
| Extreme | Keywords + arrows only, heavy abbreviations | Internal notes |

- 🎯 Trigger: `简短点` / `简洁` / `省点 token` / `压缩一下` / `别啰嗦` / `节流` / `节源`
- 🚪 Exit: `恢复正常` / `正常模式`
- 🔁 Switch: `节流 温和|标准|极限`

---

## 🛡️ Safety guardrails (auto-revert to normal Chinese)

Temporarily revert to normal Chinese, then resume throttling, when:

- 💥 Destructive-operation confirmation (`rm -rf` / `DROP TABLE` / `force push` / format)
- ⚠️ Security warning / vulnerability notice
- 🧩 Technical ambiguity (LaTeX / complex SQL / regex boundaries)
- ❓ User looks confused or asks again

**Never altered**: code, commands, terms, paths, raw errors, numbers, negation/exception words.

---

## ✅ Local verification

```bash
cd ~/.workbuddy/skills/economize-on-spending/scripts
python throttle_test.py        # 17 deterministic cases; all-pass = healthy
python ab_measure.py           # A/B token measurement (needs Qwen tokenizer)
```

---

## 📄 License

MIT — see [LICENSE](LICENSE).
