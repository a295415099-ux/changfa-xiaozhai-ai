#!/usr/bin/env python3
"""
AI内容断链检查表 - 综合生成脚本
读取用户提供的品牌/SKU/内容信息，生成完整的内容断链检查报告。
"""
import json, sys, os

def generate_check_report(brand_name, core_sku, content_info, search_words, page_info, schedule_info):
    """生成完整的断链检查报告"""
    lines = []
    lines.append(f"# {brand_name} - {core_sku} 内容断链检查报告")
    lines.append("")
    lines.append("## 一、断链检查任务定义")
    lines.append(f"- 品牌：{brand_name}")
    lines.append(f"- 核心SKU：{core_sku}")
    lines.append(f"- 检查目标：诊断从内容被看见到回站内主战场的过程中链路是否断裂")
    lines.append("")
    lines.append("## 二、断链类型判定框架")
    lines.append("| 断链类型 | 典型表现 | 本质问题 |")
    lines.append("|----------|----------|----------|")
    lines.append("| 关键词断链 | 内容有热度但用户不知道搜什么 | 内容没有种下明确关键词 |")
    lines.append("| 搜索承接断链 | 用户搜了但搜出来的页接不住 | 站内页面没有准备好 |")
    lines.append("| 利益点断链 | 用户进来但没有明确购买理由 | 承接页没讲透为什么买 |")
    lines.append("| 节奏错位断链 | 内容先做但搜索/直播/活动没跟上 | 节奏不同步 |")
    lines.append("")
    lines.append("## 三、内容断链检查表")
    lines.append("")
    lines.append("| 检查项 | 当前现象 | 是否断链 | 断链类型 | 影响程度 | 修复建议 | 责任团队 | 优先级 |")
    lines.append("|--------|---------|---------|---------|---------|---------|---------|------|")
    checks = [
        "内容有没有种下清晰关键词",
        "用户看完后会不会知道下一步搜什么",
        "搜索出来的页是不是接得住",
        "页面表达是否和内容一致",
        "承接页有没有明确利益点",
        "承接页有没有清晰转化动作",
        "内容节奏和站内承接节奏是否同步"
    ]
    for c in checks:
        lines.append(f"| {c} | 待分析 | 待判定 | 待归类 | 待评估 | 待建议 | 待分配 | 待定 |")
    lines.append("")
    lines.append("## 四、课堂核心金句")
    lines.append("> 不是内容没价值，而是内容后的动作没接住。")
    lines.append("")
    lines.append("## 五、下一步动作")
    lines.append("请基于以上框架，逐项填入实际分析结果。")
    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python generate_report.py <config.json>")
        print("config.json 需包含: brand_name, core_sku, content_info, search_words, page_info, schedule_info")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        config = json.load(f)

    report = generate_check_report(
        config.get("brand_name", "品牌名"),
        config.get("core_sku", "核心SKU"),
        config.get("content_info", {}),
        config.get("search_words", []),
        config.get("page_info", {}),
        config.get("schedule_info", {})
    )
    output_file = config.get("output", "断链检查报告.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"报告已生成: {output_file}")
