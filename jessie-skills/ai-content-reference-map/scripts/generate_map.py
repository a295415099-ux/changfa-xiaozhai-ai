#!/usr/bin/env python3
"""
生成《全域内容AI可引用地图》的辅助脚本。
接收各阶段输出的JSON数据，自动拼接成完整的地图Markdown表格。
"""

import json
import sys
import os
from datetime import datetime


def generate_map(data: dict) -> str:
    """根据输入数据生成完整的全域内容AI可引用地图。"""
    
    brand_name = data.get("brand_name", "未指定品牌")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    lines = []
    lines.append(f"# 全域内容AI可引用地图")
    lines.append(f"")
    lines.append(f"**品牌**：{brand_name}")
    lines.append(f"**生成日期**：{date_str}")
    lines.append(f"")
    
    # 表头
    lines.append("| 用户问题 | 内容主题 | 平台分布 | 内容形式 | 关键词布局 | 引用证据 | 承接入口 | 备注 |")
    lines.append("|---------|---------|---------|---------|-----------|---------|---------|------|")
    
    # 数据行
    items = data.get("content_items", [])
    for item in items:
        row = "| {} | {} | {} | {} | {} | {} | {} | {} |".format(
            item.get("user_question", ""),
            item.get("content_topic", ""),
            item.get("platform_distribution", ""),
            item.get("content_format", ""),
            item.get("keyword_layout", ""),
            item.get("reference_evidence", ""),
            item.get("conversion_entry", ""),
            item.get("notes", "")
        )
        lines.append(row)
    
    # 如果没有数据项，添加空行
    if not items:
        for _ in range(5):
            lines.append("| | | | | | | | |")
    
    # 统计信息
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"**总计内容主题数**：{len(items)}")
    
    # 平台覆盖统计
    all_platforms = set()
    for item in items:
        platforms = item.get("platform_distribution", "")
        for p in platforms.replace("、", ",").replace("，", ",").split(","):
            p = p.strip()
            if p:
                all_platforms.add(p)
    
    if all_platforms:
        lines.append(f"**覆盖平台**：{'、'.join(sorted(all_platforms))}")
    
    lines.append("")
    lines.append("> 全域内容越统一，AI越容易理解品牌。")
    
    return "\n".join(lines)


def generate_top10_topics(data: dict) -> str:
    """生成10个AI高频问答内容选题。"""
    
    items = data.get("content_items", [])
    # 取前10条
    top10 = items[:10] if len(items) >= 10 else items
    
    lines = []
    lines.append("## 10个AI高频问答内容选题")
    lines.append("")
    lines.append("| 序号 | 用户问题 | 内容主题 | 平台 | 形式 | 核心关键词 | 引用证据 | 承接入口 |")
    lines.append("|------|---------|---------|------|------|-----------|---------|---------|")
    
    for i, item in enumerate(top10, 1):
        row = "| {} | {} | {} | {} | {} | {} | {} | {} |".format(
            i,
            item.get("user_question", ""),
            item.get("content_topic", ""),
            item.get("platform_distribution", ""),
            item.get("content_format", ""),
            item.get("keyword_layout", ""),
            item.get("reference_evidence", ""),
            item.get("conversion_entry", "")
        )
        lines.append(row)
    
    # 补足到10行
    remaining = 10 - len(top10)
    for i in range(len(top10) + 1, 11):
        lines.append(f"| {i} | | | | | | | |")
    
    return "\n".join(lines)


def generate_boss_summary(data: dict) -> str:
    """生成老板版摘要。"""
    
    brand_name = data.get("brand_name", "未指定品牌")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    summary = data.get("boss_summary", {})
    
    lines = []
    lines.append("## 全域内容AI可引用地图 — 老板版摘要")
    lines.append("")
    lines.append(f"**品牌名称**：{brand_name}")
    lines.append(f"**执行日期**：{date_str}")
    lines.append("")
    lines.append("### 一句话结论")
    lines.append("")
    lines.append("> 全域内容越统一，AI越容易理解品牌。")
    lines.append("")
    lines.append("### 当前最需要统一的3个高频问题")
    lines.append("")
    for i, q in enumerate(summary.get("top_questions", ["待补充"] * 3)[:3], 1):
        lines.append(f"{i}. {q}")
    lines.append("")
    lines.append("### 当前最需要先补的内容平台")
    lines.append("")
    for p in summary.get("priority_platforms", ["待补充"]):
        lines.append(f"- {p}")
    lines.append("")
    lines.append(f"### 当前最关键的承接入口")
    lines.append("")
    lines.append(summary.get("key_entry", "待补充"))
    lines.append("")
    lines.append("### 最适合优先做成AI可引用语料的内容类型")
    lines.append("")
    lines.append(summary.get("priority_content_type", "待补充"))
    lines.append("")
    lines.append("### 谁来推进这张地图落地")
    lines.append("")
    lines.append("| 角色 | 负责人 | 核心职责 |")
    lines.append("|------|--------|---------|")
    for role in summary.get("team_roles", []):
        lines.append(f"| {role.get('role', '')} | {role.get('person', '')} | {role.get('duty', '')} |")
    if not summary.get("team_roles"):
        lines.append("| 内容负责人 | 待定 | 地图维护、内容生产协调 |")
        lines.append("| 电商负责人 | 待定 | 商品详情页、客服问答同步 |")
        lines.append("| 平台运营 | 待定 | 各平台内容执行 |")
    lines.append("")
    lines.append("### 下一步行动")
    lines.append("")
    for i, action in enumerate(summary.get("next_actions", ["待补充"]), 1):
        lines.append(f"{i}. {action}")
    
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 generate_map.py <input.json> [output_prefix]", file=sys.stderr)
        print("")
        print("input.json 格式：", file=sys.stderr)
        print("""
{
  "brand_name": "品牌名",
  "content_items": [
    {
      "user_question": "用户问题",
      "content_topic": "内容主题",
      "platform_distribution": "平台分布",
      "content_format": "内容形式",
      "keyword_layout": "关键词布局",
      "reference_evidence": "引用证据",
      "conversion_entry": "承接入口",
      "notes": "备注"
    }
  ],
  "boss_summary": {
    "top_questions": ["问题1", "问题2", "问题3"],
    "priority_platforms": ["平台1", "平台2"],
    "key_entry": "关键入口",
    "priority_content_type": "内容类型",
    "team_roles": [
      {"role": "角色", "person": "负责人", "duty": "职责"}
    ],
    "next_actions": ["行动1", "行动2"]
  }
}
""", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_prefix = sys.argv[2] if len(sys.argv) > 2 else "output"
    
    if not os.path.exists(input_file):
        print(f"错误: 输入文件 {input_file} 不存在", file=sys.stderr)
        sys.exit(1)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 生成3个输出文件
    outputs = {
        f"{output_prefix}_map.md": generate_map(data),
        f"{output_prefix}_top10.md": generate_top10_topics(data),
        f"{output_prefix}_boss_summary.md": generate_boss_summary(data),
    }
    
    for filename, content in outputs.items():
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] 已生成: {filename}")
    
    # 合并到一个文件
    combined = f"{output_prefix}_complete.md"
    with open(combined, 'w', encoding='utf-8') as f:
        f.write(outputs[f"{output_prefix}_map.md"])
        f.write("\n\n---\n\n")
        f.write(outputs[f"{output_prefix}_top10.md"])
        f.write("\n\n---\n\n")
        f.write(outputs[f"{output_prefix}_boss_summary.md"])
    print(f"[OK] 已生成合并文件: {combined}")


if __name__ == "__main__":
    main()
