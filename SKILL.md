---
name: economize-on-spending
description: 'Language-selectable concise-response rules. Load SKILL.zh-CN.md for Chinese, SKILL.en.md for English, or both when bilingual output is needed.'
agent_created: true
---

# Economize on Spending

Choose one language pack to minimize retrieval and prompt tokens:

- Chinese only: load [SKILL.zh-CN.md](SKILL.zh-CN.md)
- English only: load [SKILL.en.md](SKILL.en.md)
- Bilingual: load both files
- Unsure: load only the pack matching the user's requested response language

Shared contract: preserve facts, uncertainty, conditions, scope, negation, exceptions, safety warnings, technical tokens, numbers, and operation order. Compression is secondary to semantic fidelity.

Activation examples:
- Chinese: “简短点”, “精简”, “节流”, “省点 token”
- English: “be brief”, “shorter”, “less verbose”, “save tokens”

Language packs are standalone and intentionally avoid duplicating the other language's rules.