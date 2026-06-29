#!/usr/bin/env python3
"""
AI内容协同流程草图生成器

根据品牌信息和流程诊断结果，自动生成一份结构化的AI内容协同流程草图。
输出格式为Markdown，可直接用于汇报或粘贴到文档中。
"""

import json
import sys
from datetime import datetime


def generate_flow_diagram(brand_name: str, flow_data: dict) -> str:
    """根据输入数据生成协同流程草图"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = []
    lines.append(f"# {brand_name} · AI内容协同流程表")
    lines.append(f"")
    lines.append(f"> 生成时间：{now}")
    lines.append(f"> 核心原则：AI只有进入流程，才会变成企业能力；否则它永远只是个人技巧")
    lines.append(f"")
    lines.append(f"## 一、五阶段协同流程")
    lines.append(f"")

    stages = flow_data.get("stages", [
        {
            "name": "内容需求进入",
            "issue": "(待确认)内容为什么要做、由谁提出",
            "owner": "(待确认)",
            "ai_role": "(待确认)AI可帮助整理和归类需求",
            "review_point": "需求方向是否正确、是否与经营目标一致",
            "next": "统一语言系统"
        },
        {
            "name": "统一语言系统",
            "issue": "(待确认)内容到底按什么标准说",
            "owner": "(待确认)",
            "ai_role": "(待确认)AI可辅助维护和更新词库",
            "review_point": "搜索词/卖点词/场景词是否统一",
            "next": "AI辅助生成"
        },
        {
            "name": "AI辅助生成",
            "issue": "(待确认)哪些环节适合AI先做",
            "owner": "(待确认)",
            "ai_role": "(待确认)AI负责初稿、多版本生成、平台适配改写",
            "review_point": "内容是否偏离品牌调性、是否需人工深加工",
            "next": "人工审核"
        },
        {
            "name": "人工审核",
            "issue": "(待确认)谁来保证内容不跑偏",
            "owner": "(待确认)",
            "ai_role": "AI可辅助检查品牌表达一致性",
            "review_point": "品牌表达标准、平台要求、承接目标",
            "next": "上线与复盘"
        },
        {
            "name": "上线与复盘",
            "issue": "(待确认)内容上线后谁来负责后续判断",
            "owner": "(待确认)",
            "ai_role": "(待确认)AI可辅助数据整理和复盘分析",
            "review_point": "搜索回流、内容效果、下一轮优化方向",
            "next": "→ 回到需求进入（形成闭环）"
        }
    ])

    lines.append(f"| 流程节点 | 核心问题 | 由谁负责 | AI参与方式 | 人工判断/审核点 | 交给谁 |")
    lines.append(f"|---------|---------|---------|-----------|--------------|-------|")
    for s in stages:
        lines.append(f"| {s['name']} | {s['issue']} | {s['owner']} | {s['ai_role']} | {s['review_point']} | {s['next']} |")

    lines.append(f"")
    lines.append(f"## 二、协同角色分工")
    lines.append(f"")

    roles = flow_data.get("roles", [
        {"role": "老板/经营负责人", "duty": "(待确认)", "standard": "品牌经营方向与目标", "partner": "品牌负责人", "note": ""},
        {"role": "品牌负责人", "duty": "(待确认)", "standard": "品牌表达标准、统一语言系统", "partner": "内容团队", "note": ""},
        {"role": "内容团队", "duty": "(待确认)", "standard": "内容质量与效率", "partner": "电商团队、品牌负责人", "note": ""},
        {"role": "电商团队", "duty": "(待确认)", "standard": "搜索承接、转化目标", "partner": "内容团队", "note": ""},
        {"role": "直播团队", "duty": "(待确认)", "standard": "直播内容与话术一致性", "partner": "内容团队、电商团队", "note": ""},
        {"role": "运营/投放团队", "duty": "(待确认)", "standard": "投放素材有效性", "partner": "内容团队", "note": ""},
    ])

    lines.append(f"| 角色/团队 | 负责什么 | 维护什么标准 | 和谁协同 | 备注 |")
    lines.append(f"|----------|---------|------------|---------|------|")
    for r in roles:
        lines.append(f"| {r['role']} | {r['duty']} | {r['standard']} | {r['partner']} | {r['note']} |")

    lines.append(f"")
    lines.append(f"## 三、首轮推进动作")
    lines.append(f"")

    action = flow_data.get("first_action", {
        "what": "(待确认)今晚最值得先推进的1个动作",
        "stage": "(待确认)属于哪个流程节点",
        "lead": "(待确认)先由谁牵头",
        "output": "(待确认)预期产出",
        "note": "不追求一口气搭完整流程，但必须推进一版"
    })

    lines.append(f"| 今晚先推进什么 | 属于哪个流程节点 | 先由谁牵头 | 预期输出 | 备注 |")
    lines.append(f"|-------------|---------------|----------|---------|------|")
    lines.append(f"| {action['what']} | {action['stage']} | {action['lead']} | {action['output']} | {action['note']} |")

    lines.append(f"")
    lines.append(f"## 四、流程风险点")
    lines.append(f"")

    risks = flow_data.get("risks", [
        "需求来源不清 → 后面所有动作都会乱",
        "语言系统未统一 → AI产出无法形成合力",
        "审核节点缺失 → 内容质量不可控",
        "复盘环节被跳过 → 流程无法自我优化",
        "责任人不明确 → 流程形同虚设"
    ])

    for risk in risks:
        lines.append(f"- ⚠️ {risk}")

    lines.append(f"")
    lines.append(f"## 五、迭代机制")
    lines.append(f"")
    lines.append(f"- **执行周期**：首轮推进后，每周复盘一次流程运行情况")
    lines.append(f"- **优化触发**：当出现新的内容类型、新平台需求、或团队反馈流程卡顿")
    lines.append(f"- **责任人**：(待指定)负责定期审视和更新本流程表")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        brand_name = input("请输入品牌名称：")
    else:
        brand_name = sys.argv[1]

    # Try to read data from stdin if piped
    flow_data = {}
    if not sys.stdin.isatty():
        try:
            raw = sys.stdin.read()
            if raw.strip():
                flow_data = json.loads(raw)
        except json.JSONDecodeError:
            print("⚠️ 无法解析输入数据，使用默认模板", file=sys.stderr)

    result = generate_flow_diagram(brand_name, flow_data)
    print(result)


if __name__ == "__main__":
    main()
