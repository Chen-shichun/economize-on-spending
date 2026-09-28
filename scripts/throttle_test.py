#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
节流 自测脚本（确定性不变量校验）。

仅覆盖 SKILL.md 里"可机械判定"的规则：
  - 否定/限定/例外词（不/禁止/不可/未/无/仅/只/除…外）必须保留
  - 代码块 ```...``` 与内联代码 `...` 必须原样保留
  - 数值/版本号/日期必须保留
  - 客套话（您/请/您好/感谢/辛苦了）必须被删
  - 铺垫词（首先/然后/接下来/需要注意的是）必须被删
  - 符号表（因此/所以/导致→→；并且→+；或者→/；例如→如）保护区间外生效
  - 压缩率冒烟：冗余段落压缩率必须达标
  - SKILL.md 结构完整性：关键章节（符号表/结论前置/复合词保护/极限档铁律）必须存在

这是一个"参照实现 + 断言测试"，不是完整压缩器；完整压缩由模型按 SKILL.md 执行。
用法：python throttle_test.py
"""
import os
import re
import sys

# ---- 确定性规则（保守版，仅用于测试断言）----
DELETE_PHRASES = [
    "您", "请", "您好", "感谢", "辛苦了", "不好意思", "方便的话",
    "首先", "然后", "接下来", "需要注意的是", "值得一提的是", "换句话说",
    "简单来说", "也就是说", "总的来说", "个人认为", "我觉得",
    "可能", "也许", "大概", "似乎", "应该", "一般来说", "某种程度上", "非常",
    "其实", "基本上", "确实", "当然", "显然", "众所周知",
    "即可", "就行", "就可以了",
    "适当的", "正确的", "合适的", "基本的", "一般的", "相关的",
    "进行", "加以", "予以",
]
# 按长度降序处理：长复合词先删，避免单字先删破坏复合词（如 您好→好）
DELETE_PHRASES.sort(key=len, reverse=True)
# 仅当孤立助词且不在受保护复合词内时删除（「与」表并列连接，SKILL.md 已移出删除表）
DELETE_CHARS = ["的", "了", "是", "在", "于", "对"]
# 受保护复合词：含上面字符但不能拆（删了会断义）——与 SKILL.md 复合词保护铁律对齐
# 高危：是否→否（语义反转）/ 不对→不（悬空否定）/ 请求·了解·目的（不成词）
PROTECT_COMPOUNDS = [
    "但是", "对于", "关于", "于是", "在于", "由于", "等于", "属于", "以及",
    "以为", "认为", "就是", "还是", "也是", "总是", "才是", "要是", "或是",
    "的话", "的确", "的士", "除了", "为了", "参与", "与其", "对比",
    "面对", "绝对", "对齐", "对称", "核对", "存在", "现在", "在线", "所在",
    "可能性", "都是", "只是", "更是", "凡是", "正是", "终于", "至于", "鉴于",
    "请求", "申请", "邀请", "请假", "了解", "目的", "标的", "事实", "现实",
    "不是", "而是", "是否", "不对", "对象", "对方", "相对", "对话",
    "正在", "潜在", "内在", "处于", "位于", "善于", "别的", "不得了", "了不起",
]
NEGATIVES = ["不", "禁止", "不可", "未", "无", "仅", "只", "除", "外", "没有", "没"]

# 符号表（标准档起）：整词替换，仅代码保护区间外；复合词保护不参与符号阶段
#（否则 所以/因此 会被复合词保护挡住无法替换）。与 SKILL.md「结构规则·符号表」对齐。
SYMBOL_MAP = [
    ("因此", "→"), ("所以", "→"), ("导致", "→"), ("变成", "→"), ("结果是", "→"),
    ("是由于", "←"),
    ("并且", "+"), ("而且", "+"),
    ("或者", "/"),
    ("例如", "如"),
    ("大约", "≈"),
]
PUNCT = "，。、；：！？"

CODE_BLOCK_RE = re.compile(r"```[\s\S]*?```")
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def protect_spans(text, compounds=True):
    """返回需保护的区间列表。compounds=False 时仅保护代码（供符号替换阶段用）。"""
    spans = []
    for m in CODE_BLOCK_RE.finditer(text):
        spans.append((m.start(), m.end()))
    for m in INLINE_CODE_RE.finditer(text):
        spans.append((m.start(), m.end()))
    if compounds:
        for comp in PROTECT_COMPOUNDS:
            for m in re.finditer(re.escape(comp), text):
                spans.append((m.start(), m.end()))
    return spans


def in_spans(i, spans):
    return any(s <= i < e for s, e in spans)


def apply_symbols(text):
    """符号替换（标准档）：整词匹配，仅代码保护区间外。每轮重算保护区间。"""
    result = text
    for src, dst in SYMBOL_MAP:
        spans = protect_spans(result, compounds=False)  # 随文本变化重算，避免 stale span
        new = []
        idx = 0
        while True:
            j = result.find(src, idx)
            if j == -1:
                break
            end = j + len(src)
            if in_spans(j, spans):
                new.append(result[idx:end])
            else:
                new.append(result[idx:j])
                new.append(dst)
            idx = end
        result = "".join(new) + result[idx:]
    return result


def conservative_compress(text):
    """保守压缩：删确定性可删词 + 符号替换，保护代码与复合词。返回压缩后文本。"""
    # 先删短语（受保护区间外）。每轮重算保护区间，避免删词导致区间漂移（stale span）。
    result = text
    for ph in DELETE_PHRASES:
        spans = protect_spans(result)  # 关键：随文本变化重算
        new = []
        idx = 0
        while True:
            j = result.find(ph, idx)
            if j == -1:
                break
            end = j + len(ph)
            if in_spans(j, spans):
                new.append(result[idx:end])
            else:
                new.append(result[idx:j])
            idx = end
        result = "".join(new) + result[idx:]
    # 符号替换（同样逐轮重算保护区间）
    result = apply_symbols(result)
    # 单字符删除 + 标点折叠（仅保护区间外；spans 必须对最终文本重算）
    spans = protect_spans(result)
    final = []
    prev_punct = False
    for k, ch in enumerate(result):
        if not in_spans(k, spans):
            if ch in DELETE_CHARS:
                continue
            if ch in PUNCT:
                if prev_punct:
                    continue  # 重复标点折叠：删词留下的 "。。""，," 等
                prev_punct = True
            else:
                prev_punct = False
        else:
            prev_punct = False
        final.append(ch)
    return "".join(final).lstrip(PUNCT)


SKILL_MD = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "SKILL.md"))


def run_tests():
    cases = [
        {
            "name": "否定词保留",
            "text": "这个配置不可以删除，仅管理员可改，除 root 外无权限。",
            "must_keep": ["不", "仅", "除", "外", "无"],
            "must_drop": [],
        },
        {
            "name": "代码块原样",
            "text": "运行 `npm install` 然后 `rm -rf node_modules` 即可。",
            "must_keep": ["npm install", "rm -rf node_modules"],
            "must_drop": ["即可"],
        },
        {
            "name": "符号不进内联代码",
            "text": "跑 `npm install || npm run build`，因此分两步。",
            "must_keep": ["npm install || npm run build", "→"],
            "must_drop": ["因此"],
        },
        {
            "name": "符号替换（保护区间外）",
            "text": "因此内存溢出，例如 OOM。并且高并发，或者配置错误。",
            "must_keep": ["→", "如", "+", "/", "OOM"],
            "must_drop": ["因此", "例如", "并且", "或者"],
        },
        {
            "name": "客套话删除",
            "text": "您好，感谢您的提问。首先，这个问题需要您请仔细查看日志。",
            "must_drop": ["您好", "感谢", "首先", "您", "请"],
            "must_keep": ["日志"],
        },
        {
            "name": "数值/版本保留",
            "text": "版本 1.2.3 在 2026-09-27 发布了，耗时 42 秒。",
            "must_keep": ["1.2.3", "2026-09-27", "42"],
        },
        {
            "name": "复合词'但是'不被拆",
            "text": "该方法很快，但是内存占用高。",
            "must_keep": ["但是"],
        },
        {
            "name": "复合词'对于'不被拆",
            "text": "对于这种情况，建议重试。",
            "must_keep": ["对于"],
        },
        {
            "name": "复合词'参与/对齐/存在/为了'不被拆",
            "text": "为了排查，用户参与了校验，确认镜像对齐，缓存存在过期风险。",
            "must_keep": ["为了", "参与", "对齐", "存在"],
        },
        {
            "name": "高危单字入词（请求/了解/是否/目的/对话/不对）",
            "text": "发送请求前先了解配置，检查是否对齐，目的是找出不对的对话记录。",
            "must_keep": ["请求", "了解", "是否", "目的", "对话", "不对"],
            "must_drop": [],
        },
        {
            "name": "全量复合词系统性存活扫描",
            "text": "",
            "compound_sweep": True,
        },
        {
            "name": "可能性'整体保留",
            "text": "存在内存泄漏的可能性。",
            "must_keep": ["可能性"],
        },
        {
            "name": "空串安全",
            "text": "",
            "expect_out": "",
        },
        {
            "name": "纯代码块原样",
            "text": "```\nx = 1  # 的了是\n```",
            "must_keep": ["x = 1  # 的了是", "```"],
            "must_drop": [],
        },
        {
            "name": "幂等性（二次压缩不变）",
            "text": "您好，感谢您的提问。首先，经过仔细检查日志，发现根本原因是由于认证中间件令牌过期检查 `<` 误写 `<=` 所导致的，建议您修改比较运算符应该就能解决问题了。",
            "idempotent": True,
            "must_keep": ["认证"],
        },
        {
            "name": "压缩率冒烟（冗余段落）",
            "text": "您好，感谢您的提问。首先，经过我仔细检查日志和代码，发现根本原因是由于认证中间件的令牌过期检查 `<` 误写 `<=` 所导致的，建议您修改比较运算符应该就能解决问题了。",
            "must_keep": ["认证", "<=", "`"],
            # 0.85 = 仅机械删词+符号的保守实现下限；结构改写（结论前置/去重/列表）由模型执行，
            # 实际回复在此之上再省 20-40%（见 SKILL.md 结构规则）。
            "max_ratio": 0.85,
        },
        {
            "name": "SKILL.md 结构完整",
            "skill_check": True,
            "text": "",
            "must_keep": ["结论前置", "符号表", "复合词保护（铁律）", "极限档铁律",
                          "去重铁律", "尾问省略", "自动恢复", "数字紧凑",
                          "「与」表并列连接", "节源",
                          # 触发词抽查
                          "简短点", "节流", "恢复正常",
                          # 高危警示句必须在
                          "语义反转", "悬空否定"],
            "symbol_consistency": True,
            "compound_consistency": True,
        },
    ]
    passed = 0
    total = len(cases)
    for c in cases:
        problems = []
        if c.get("skill_check"):
            out = ""
            txt = open(SKILL_MD, encoding="utf-8").read()
            if txt.startswith("﻿"):
                problems.append("SKILL.md 带 BOM，frontmatter 解析可能失败")
            if "\r\n" in txt:
                problems.append("SKILL.md 含 CRLF，建议统一 LF")
            for k in c.get("must_keep", []):
                if k not in txt:
                    problems.append(f"SKILL.md 缺章节/规则: {k!r}")
            if c.get("symbol_consistency"):
                for src, dst in SYMBOL_MAP:
                    if src not in txt:
                        problems.append(f"SYMBOL_MAP 的 {src!r} 未在 SKILL.md 符号表声明（两处漂移）")
            if c.get("compound_consistency"):
                for comp in PROTECT_COMPOUNDS:
                    if comp not in txt:
                        problems.append(f"PROTECT_COMPOUNDS 的 {comp!r} 未在 SKILL.md 复合词表声明（两处漂移）")
        else:
            out = conservative_compress(c["text"])
            if c.get("compound_sweep"):
                for comp in PROTECT_COMPOUNDS:
                    probe = f"甲{comp}乙测试"
                    o = conservative_compress(probe)
                    if comp not in o:
                        problems.append(f"复合词被拆: {comp!r} → {o!r}")
                if not problems:
                    out = f"(已扫描 {len(PROTECT_COMPOUNDS)} 个复合词)"
            if "expect_out" in c and out != c["expect_out"]:
                problems.append(f"期望输出不符: {out!r} != {c['expect_out']!r}")
            if c.get("idempotent"):
                out2 = conservative_compress(out)
                if out2 != out:
                    problems.append(f"不幂等: 二次压缩结果不同\n          一次: {out!r}\n          二次: {out2!r}")
            for k in c.get("must_keep", []):
                if k not in out:
                    problems.append(f"应保留却丢失: {k!r}")
            for d in c.get("must_drop", []):
                if d in out:
                    problems.append(f"应删除却残留: {d!r}")
            if "max_ratio" in c:
                ratio = len(out) / max(1, len(c["text"]))
                if ratio > c["max_ratio"]:
                    problems.append(f"压缩率不达标: {ratio:.0%} > {c['max_ratio']:.0%}")
        ok = not problems
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        extra = ""
        if "max_ratio" in c and not c.get("skill_check"):
            extra = f"（压缩率 {len(out)/max(1,len(c['text'])):.0%}）"
        print(f"[{status}] {c['name']}{extra}")
        if problems:
            for p in problems:
                print(f"        - {p}")
        if not c.get("skill_check"):
            print(f"        原文: {c['text']}")
            print(f"        压缩: {out}")
        print()
    print(f"=== 结果: {passed}/{total} 通过 ===")
    return passed == total


if __name__ == "__main__":
    ok = run_tests()
    sys.exit(0 if ok else 1)
