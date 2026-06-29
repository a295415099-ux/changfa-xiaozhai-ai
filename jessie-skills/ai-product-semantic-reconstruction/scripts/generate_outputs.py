#!/usr/bin/env python3
"""
AI商品语义重构表 - 输出生成脚本

基于前面步骤的盘点结果，批量生成步骤10-14的输出内容。
在步骤3-9的盘点数据收集完成后调用。

用法：
  python3 generate_outputs.py <input_json_path> <output_dir>
"""

import json
import sys
import os
from pathlib import Path


def load_input(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_purchase_reasons(data):
    """步骤10：生成购买理由"""
    lines = []
    lines.append("# 购买理由表\n")
    lines.append("| 理由编号 | 适配人群 | 适用场景 | 核心购买理由 | 证据支撑 |")
    lines.append("|---------|---------|---------|------------|---------|")

    persona = data.get("target_audience", [])
    scenarios = data.get("use_scenarios", [])
    pains = data.get("core_pain_points", [])
    features = data.get("functional_features", [])
    evidence = data.get("trust_evidence", [])

    idx = 1
    # 人群×场景 组合生成理由
    for p in persona[:3]:
        for s in scenarios[:2]:
            reason = f"作为{p.get('label', '')}，当你在{s.get('situation', '')}时，"
            pain_desc = pains[0].get("description", "") if pains else ""
            feature_desc = features[0].get("user_benefit", "") if features else ""
            reason += f"经常遇到{pain_desc}的问题。本商品通过{feature_desc}"
            evidence_text = evidence[0].get("content", "") if evidence else "见详情"
            lines.append(f"| R{idx:03d} | {p.get('label', '')} | {s.get('situation', '')} | {reason} | {evidence_text} |")
            idx += 1

    return "\n".join(lines)


def generate_scene_tags(data):
    """步骤11：生成场景标签"""
    lines = []
    lines.append("# 商品场景标签表\n")
    lines.append("| 标签类型 | 标签名称 | 关联场景 | 检索关键词 | 适用推荐逻辑 |")
    lines.append("|---------|---------|---------|-----------|------------|")

    scenarios = data.get("use_scenarios", [])
    pains = data.get("core_pain_points", [])

    # 场景标签
    for s in scenarios:
        lines.append(f"| 场景标签 | {s.get('category', '')} | {s.get('situation', '')} | {s.get('keywords', '')} | 场景匹配推荐 |")

    # 需求标签（基于痛点）
    for p in pains:
        lines.append(f"| 需求标签 | {p.get('label', '')} | {p.get('context', '')} | {p.get('keywords', '')} | 需求匹配推荐 |")

    # 搭配标签
    complements = data.get("complementary_products", [])
    for c in complements:
        lines.append(f"| 搭配标签 | 搭配{c.get('name', '')} | {c.get('scene', '')} | {c.get('keywords', '')} | 关联推荐 |")

    return "\n".join(lines)


def generate_qa_corpus(data):
    """步骤12：生成商品问答语料"""
    lines = []
    lines.append("# 商品问答语料库\n")
    lines.append("| 问题分类 | 用户问法 | 标准回答 | 可追问方向 |")
    lines.append("|---------|---------|---------|----------|")

    qa_items = []

    # 基于商品身份
    product = data.get("product", {})
    qa_items.append({
        "category": "商品基础",
        "question": f"这个{product.get('name', '商品')}是什么？",
        "answer": f"这是{product.get('identity', '一款优质商品')}，{product.get('one_liner', '')}",
        "follow_up": "适用场景、使用方式"
    })

    # 基于人群
    for p in data.get("target_audience", [])[:2]:
        qa_items.append({
            "category": "适合人群",
            "question": f"{p.get('label', '')}适合用吗？",
            "answer": f"非常适合。{p.get('fit_reason', '')}",
            "follow_up": "具体用法、搭配建议"
        })

    # 基于痛点
    for p in data.get("core_pain_points", [])[:3]:
        qa_items.append({
            "category": "解决问题",
            "question": p.get("user_question", f"能解决{p.get('description', 'XX')}的问题吗？"),
            "answer": p.get("solution_description", "可以，具体来说..."),
            "follow_up": "使用效果、对比同类"
        })

    # 基于对比
    qa_items.append({
        "category": "商品对比",
        "question": "和XX比有什么不同？",
        "answer": data.get("comparison_summary", "本商品在XX方面更适合XX需求的用户"),
        "follow_up": "具体差异点、性价比分析"
    })

    for qa in qa_items:
        lines.append(f"| {qa['category']} | {qa['question']} | {qa['answer']} | {qa['follow_up']} |")

    return "\n".join(lines)


def generate_recommendation_scripts(data):
    """步骤13：生成AI推荐话术"""
    lines = []
    lines.append("# AI推荐话术库\n")
    lines.append("| 触发条件 | 推荐话术模板 | 推荐逻辑 | 适用渠道 |")
    lines.append("|---------|------------|---------|---------|")

    persona = data.get("target_audience", [])
    scenarios = data.get("use_scenarios", [])
    product = data.get("product", {})
    advantages = data.get("comparative_advantages", [])

    product_name = product.get("name", "这款商品")

    # 人群触发版本
    for p in persona[:3]:
        trigger = f"用户提到自己是{p.get('label', 'XX人群')}"
        script = f"看到你是{p.get('label', '')}，{product_name}可能特别适合你。因为{p.get('fit_reason', '它针对性地解决了你的核心需求')}。"
        lines.append(f"| {trigger} | {script} | 人群精准匹配 | 客服/私域/直播间 |")

    # 场景触发版本
    for s in scenarios[:2]:
        trigger = f"用户提到{s.get('situation', 'XX场景')}需求"
        script = f"在{s.get('situation', '')}时，很多人都会遇到XX问题。{product_name}专门为此设计，{s.get('solution', '能帮你有效解决')}。"
        lines.append(f"| {trigger} | {script} | 场景需求匹配 | 内容种草/详情页 |")

    # 对比触发版本
    if advantages:
        adv = advantages[0]
        trigger = f"用户在对比同类商品"
        script = f"如果你更看重{adv.get('dimension', 'XX方面')}，{product_name}会比同类更适合。{adv.get('difference', '')}"
        lines.append(f"| {trigger} | {script} | 对比差异化推荐 | 详情页/直播间 |")

    return "\n".join(lines)


def generate_recommendation_card(data):
    """步骤14：生成单品AI推荐理由卡"""
    product = data.get("product", {})
    persona = data.get("target_audience", [])
    scenarios = data.get("use_scenarios", [])
    pains = data.get("core_pain_points", [])
    features = data.get("functional_features", [])
    emotions = data.get("emotional_values", [])
    evidence = data.get("trust_evidence", [])
    advantages = data.get("comparative_advantages", [])

    lines = []
    lines.append("# 单品AI推荐理由卡\n")
    lines.append(f"**商品名称：** {product.get('name', '待填写')}")
    lines.append(f"**商品身份（一句话）：** {product.get('identity', '待填写')}")
    lines.append("")
    lines.append(f"**适合人群（3类）：**")
    for p in persona[:3]:
        lines.append(f"- {p.get('label', '')}：{p.get('fit_reason', '')}")
    lines.append("")
    lines.append(f"**核心场景（3-5个）：**")
    for s in scenarios[:5]:
        lines.append(f"- {s.get('situation', '')}")
    lines.append("")
    lines.append(f"**核心痛点（3个）：**")
    for p in pains[:3]:
        lines.append(f"- {p.get('description', '')}")
    lines.append("")
    lines.append(f"**核心卖点（3个）：**")
    for f in features[:3]:
        lines.append(f"- {f.get('user_benefit', '')}")
    lines.append("")
    lines.append(f"**情绪价值（2-3个）：**")
    for e in emotions[:3]:
        lines.append(f"- {e.get('type', '')}：{e.get('description', '')}")
    lines.append("")
    lines.append(f"**信任证据（3-5条）：**")
    for ev in evidence[:5]:
        lines.append(f"- [{ev.get('type', '')}] {ev.get('content', '')}")
    lines.append("")
    lines.append(f"**对比优势（3条）：**")
    for a in advantages[:3]:
        lines.append(f"- {a.get('dimension', '')}：{a.get('difference', '')}")
    lines.append("")
    lines.append(f"**一句话推荐理由：** {product.get('one_liner', '待填写')}")
    lines.append(f"**AI推荐触发词：** {', '.join(data.get('trigger_keywords', ['待填写']))}")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print("用法: python3 generate_outputs.py <input_json> <output_dir>")
        print("input_json 格式见 references/input_format.md")
        sys.exit(1)

    json_path = sys.argv[1]
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)

    data = load_input(json_path)

    outputs = {
        "10_purchase_reasons.md": generate_purchase_reasons(data),
        "11_scene_tags.md": generate_scene_tags(data),
        "12_qa_corpus.md": generate_qa_corpus(data),
        "13_recommendation_scripts.md": generate_recommendation_scripts(data),
        "14_recommendation_card.md": generate_recommendation_card(data),
    }

    for filename, content in outputs.items():
        path = output_dir / filename
        path.write_text(content, encoding="utf-8")
        print(f"✅ 已生成: {path}")

    print(f"\n共生成 {len(outputs)} 个文件，输出目录: {output_dir}")


if __name__ == "__main__":
    main()
