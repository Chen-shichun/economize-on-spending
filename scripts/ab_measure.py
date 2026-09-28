# -*- coding: utf-8 -*-
"""A/B 实测：同题三版回复的真实 token 数（Qwen2.5 BPE 离线 tokenizer，中文代表性好）。"""
import os
import sys

from tokenizers import Tokenizer

TOK_PATH = r"C:\tools\tmp-tok\qwen_tok.json"
if not os.path.exists(TOK_PATH):
    print(f"[错误] 缺少 tokenizer 词表: {TOK_PATH}")
    print("获取方式（bash）:")
    print('  mkdir -p /c/tools/tmp-tok && curl -sL \\')
    print('    "https://hf-mirror.com/Qwen/Qwen2.5-0.5B/resolve/main/tokenizer.json" \\')
    print("    > /c/tools/tmp-tok/qwen_tok.json")
    sys.exit(2)

tok = Tokenizer.from_file(TOK_PATH)

def n_tokens(t):
    return len(tok.encode(t).ids)

NORMAL = """基于 2026 年几大顶会（ICML / ICLR / AAAI / ACL / CVPR）和 arXiv 的论文数据透视，当前 AI 研究已经明显从「堆参数」转向「实用落地」，主流方向可以归纳为五大核心 + 几个新兴热点：

## 五大核心方向（2026 共识）

**1. 效率优先（Efficiency）** —— 论文占比最高（arXiv 上约 31%）。方向包括：
- 量化压缩（2–3 bit 量化）、剪枝、知识蒸馏
- MoE（混合专家）稀疏化、投机解码（speculative decoding）
- 线性注意力、状态空间模型（SSM）、Transformer 之外的混合架构（如 TransMamba）
- 目标：让前沿级模型跑在消费级显卡/手机上

**2. 推理能力（Reasoning）** —— ICLR 2026 热度第二。从「更长思维链」转向「更准、更高效」：
- Test-time compute（推理时多算、搜索、自校验）
- 强化学习引入后训练（RLHF/DPO 变体、RLP 预训练注入推理）
- 解决「过度思考 / 思考不足」的平衡推理
- 形式化验证（verifiable reasoning）

**3. 智能体崛起（Agentic AI）** —— 2026 最大爆发点。ICLR 2026 有 162 篇 agent 论文：
- 工具调用 / 函数调用（Tool Use）、多步规划
- 多智能体协作（自组织涌现、预算感知优化）
- 上下文工程（Context Engineering，替代简单历史堆叠）
- Agent 驱动科学发现（Agentic Science 在 Science/Nature 密集发表）

**4. 评估引领（Evaluation）** —— arXiv 上占比 57% 居首。核心驱动力从「造模型」转向「量模型」：
- 推理链路质量、长程任务规划、多模态深度的精细化评测
- 传统跑分范式已不适配新兴能力，评测体系本身成了前沿研究方向

**5. 安全筑基（Safety & Alignment）** —— 从「可选项」变「全生命周期标配」：
- 越狱攻击可迁移性、机器遗忘（Unlearning，如 BS 框架精准删有害知识）
- 用户级水印溯源（治深度伪造）
- 对齐、红队、合规治理框架

## 几个新兴热点

- **多模态统一**：单一模型原生处理文本+图像+视频+音频（取代流水线拼接）
- **世界模型 + 具身智能**：视频预测/物理感知生成 → 仿真训练策略迁移真实机器人（如 SP-VLA 准确率 66%→84.6%）
- **AI for Science**：蛋白设计、药物发现、材料、气象预测进入实用部署
- **时序/预测基础模型**：时间序列的 foundation model

## 一句话总结

2026 年 AI 论文的主旋律是：以高效推理为引擎、具身智能为载具、体系安全为边界，从「比跑分」迈入「比落地、比可信、比能干活」的高质量发展阶段。

如果你在做竞赛/科研方向选择，我会建议优先考虑 Agent + 推理 或 效率/量化 这两个交叉度高、资源门槛相对低、且中文机构（复旦、北大、上交）贡献突出的方向。"""

OLD_THROTTLE = """2026 主流 AI 论文 5 大方向：

1. **效率** → 量化/剪枝/MoE/线性注意力。让大模型 跑消费级硬件
2. **推理** → test-time compute、RL 后训练、可验证推理
3. **智能体** → 工具调用、多智能体协作、上下文工程（ICLR 162篇）
4. **评测** → arXiv 占 57%，从「造模型」转「量模型」
5. **安全** → 越狱防御、机器遗忘、水印溯源

新兴：多模态统一 / 世界模型+具身 / AI4Science / 时序基础模型。

主旋律：**高效推理为引擎、具身为载具、安全为边界**，比落地比可信。

竞赛向 建议：**Agent+推理** 或 **效率/量化**（中文机构贡献突出、门槛低）。"""

NEW_THROTTLE = """2026 主流 5 方向：
效率→量化/MoE/线性注意力；推理→test-time compute+RL；agent→工具调用/多体协作；
评测（arXiv 57%）；安全→遗忘/水印。
新兴：多模态统一/具身/AI4Science。
竞赛向：Agent+推理 或 效率量化（门槛低）。"""

rows = [("正常中文", NORMAL), ("旧节流(标准档)", OLD_THROTTLE), ("新节流(+结构规则)", NEW_THROTTLE)]
base_n = n_tokens(NORMAL)
base_c = len(NORMAL)
print(f"{'版本':<20}{'字符':>7}{'token':>8}{'vs正常':>9}")
for name, t in rows:
    n = n_tokens(t)
    print(f"{name:<20}{len(t):>7}{n:>8}{n/base_n:>8.0%}")

# 语义保真 spot-check：关键事实必须存活
KEY_FACTS = ["量化", "MoE", "test-time compute", "RL", "57%", "水印", "agent", "AI4Science", "竞赛"]
missing = [k for k in KEY_FACTS if k not in NEW_THROTTLE]
print()
print("关键事实存活检查:", "全部保留 ✅" if not missing else f"丢失: {missing}")
