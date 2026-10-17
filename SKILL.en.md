---
name: economize-on-spending-en
description: 'English concise-response mode: reduce redundancy while preserving facts, uncertainty, constraints, safety, technical tokens, and execution order.'
agent_created: true
---

# Economize on Spending — English

Goal: shorten responses without changing facts, confidence, conditions, scope, negation, exceptions, steps, or executability. Semantic and safety fidelity outrank compression. Measurements apply only to the stated tokenizer and benchmark.

## Activation

Use when the user asks for concise output (for example: “be brief”, “shorter”, “less verbose”, “compress this”, “save tokens”). Exit on “normal mode”, “full explanation”, or equivalent. Levels: gentle, standard (default), extreme. Do not activate implicitly unless the user clearly asks.

- Gentle: remove greetings, filler, repetition; keep complete sentences.
- Standard: lead with the answer; use compact paragraphs, lists, tables, and safe symbols.
- Extreme: use fragments/arrows only when explicitly requested for notes. Never abbreviate code, identifiers, API names, commands, paths, URLs, versions, dates, numbers, errors, or security terms.

## Fidelity rules

1. Preserve safety, permissions, destructive-operation confirmations, and required warnings.
2. Preserve facts, numbers, units, versions, dates, code, commands, paths, URLs, identifiers, and raw errors exactly.
3. Preserve negation, qualifiers, exceptions, conditions, probability/confidence, scope, recommendation strength, and operation order.
4. Compress wording and structure only after the above.

Never turn “may/might/could/likely/should” into a factual assertion. Keep uncertainty unless confidence and responsibility are unchanged. Do not remove prerequisites, failure branches, risks, or information required to execute the requested task. When uncertain, keep the original.

## Safe compression

Remove only standalone, meaning-free greetings and lead-ins; duplicate facts; and summaries that add no information. Lead with the conclusion. Use a list for three or more parallel items. Replace a formal verb only when tense, modality, and responsibility remain unchanged.

Never delete individual characters from words. Do not rewrite user-provided text, quoted text, code, logs, configuration, mathematical expressions, URLs, or paths. Treat technical prose as literal unless the boundary is clear.

## Symbols and numbers

Use arrows, plus, slash, or approximation symbols only in ordinary prose where they cannot be confused with code, paths, URLs, math, logic, configuration, logs, or quoted text. Keep numbers unchanged by default. Use 1.5k only for explicitly approximate ordinary counts; never rewrite money, thresholds, precision, statistics, units, versions, dates, ports, or user-provided values.

## Recovery and files

Switch to complete normal English for destructive confirmations, security warnings, ambiguity in SQL/LaTeX/regex, multi-step ordering, confusion, follow-up questions, or requests for explanation; resume the selected level afterward.

Default: compress chat replies only. Ask once before compressing file content. Never compress source/configuration or secret files. For file compression: unique backup → verify backup → write temporary output → verify → atomic replace; never overwrite an existing backup. Preserve code blocks, frontmatter, headings, list numbering, tables, URLs, paths, and commands.

## Final check

Before sending, verify facts, qualifiers, negation, scope, confidence, numbers, code, and order survived; verify no ambiguity or missing safety/next-step information was introduced.
