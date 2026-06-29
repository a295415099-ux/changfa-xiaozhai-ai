#!/usr/bin/env python3
"""
优质素材筛选 - 评分表生成工具
生成《素材筛选评分表》的表格模板和汇总工具
"""

import json
import sys

SCORING_DIMENSIONS = [
    {
        "id": "seeding_power",
        "name": "种草力",
        "question": "用户是否产生代入和需求？",
        "max_score": 5
    },
    {
        "id": "keyword_power", 
        "name": "关键词力",
        "question": "是否强化搜索词/卖点词/场景词？",
        "max_score": 5
    },
    {
        "id": "conversion_power",
        "name": "转化力",
        "question": "是否带来点击、进店、加购、咨询？",
        "max_score": 5
    },
    {
        "id": "interaction_quality",
        "name": "互动质量",
        "question": "评论区是否出现真实购买问题？",
        "max_score": 5
    },
    {
        "id": "landing_match",
        "name": "承接匹配",
        "question": "店铺页面是否能接住这条内容？",
        "max_score": 5
    },
    {
        "id": "reuse_value",
        "name": "复用价值",
        "question": "是否能被改写、二创、投放、沉淀？",
        "max_score": 5
    }
]


def classify_material(total_score: int) -> dict:
    """根据总分进行A/B/C/D分级"""
    if total_score >= 25:
        return {"grade": "A级", "action": "优先放大", "desc": "直接纳入投放计划，加大预算，多平台分发"}
    elif total_score >= 20:
        return {"grade": "B级", "action": "优化后放大", "desc": "针对性补短板后纳入投放计划"}
    elif total_score >= 15:
        return {"grade": "C级", "action": "观察/待定", "desc": "保留但不优先投放，等待验证或优化"}
    else:
        return {"grade": "D级", "action": "淘汰/不再放大", "desc": "不建议继续投放，但可保留作为反面样本"}


def generate_scoring_table(materials: list) -> str:
    """生成素材筛选评分表"""
    lines = []
    lines.append("# 素材筛选评分表")
    lines.append("")
    lines.append("| 素材名称 | 种草力 | 关键词力 | 转化力 | 互动质量 | 承接匹配 | 复用价值 | 总分 | 等级 | 处理方式 |")
    lines.append("|----------|--------|----------|--------|----------|----------|----------|------|------|----------|")
    
    for m in materials:
        scores = m.get("scores", {})
        total = sum(scores.values())
        classification = classify_material(total)
        lines.append(
            f"| {m['name']} | "
            f"{scores.get('seeding_power', 0)} | "
            f"{scores.get('keyword_power', 0)} | "
            f"{scores.get('conversion_power', 0)} | "
            f"{scores.get('interaction_quality', 0)} | "
            f"{scores.get('landing_match', 0)} | "
            f"{scores.get('reuse_value', 0)} | "
            f"**{total}** | {classification['grade']} | {classification['action']} |"
        )
    
    lines.append("")
    return "\n".join(lines)


def generate_priority_list(materials: list) -> str:
    """生成优先放大素材清单"""
    # 按总分降序排列
    sorted_materials = sorted(
        materials, 
        key=lambda m: sum(m.get("scores", {}).values()), 
        reverse=True
    )
    
    # 筛选A级和B级
    priority = [m for m in sorted_materials if sum(m.get("scores", {}).values()) >= 20]
    
    lines = []
    lines.append("# 优先放大素材清单")
    lines.append("")
    
    if not priority:
        lines.append("暂无A级/B级素材，建议先优化素材再筛选。")
        return "\n".join(lines)
    
    for i, m in enumerate(priority[:3], 1):
        total = sum(m.get("scores", {}).values())
        classification = classify_material(total)
        lines.append(f"## 优先级 #{i}：{m['name']}")
        lines.append(f"- **等级**：{classification['grade']}（{total}分）")
        lines.append(f"- **处理方式**：{classification['desc']}")
        lines.append(f"- **建议动作**：")
        if total >= 25:
            lines.append(f"  1. 投放团队：加大预算投放，多平台分发")
            lines.append(f"  2. 内容团队：拆解结构，二创多版本")
            lines.append(f"  3. 电商团队：优化承接页，确保首屏一致性")
            lines.append(f"  4. 客服团队：准备FAQ话术")
        else:
            # B级素材：找出短板
            scores = m.get("scores", {})
            dim_names = {d["id"]: d["name"] for d in SCORING_DIMENSIONS}
            weak = [(dim_names[k], v) for k, v in scores.items() if v <= 3]
            weak.sort(key=lambda x: x[1])
            if weak:
                lines.append(f"  1. 优先优化短板维度：{'、'.join([w[0] for w in weak[:2]])}")
            lines.append(f"  2. 小预算测试验证优化效果")
        lines.append("")
    
    return "\n".join(lines)


def generate_checklist(material_name: str, scores: dict) -> str:
    """生成单条素材的放大前检查清单"""
    total = sum(scores.values())
    classification = classify_material(total)
    
    lines = []
    lines.append(f"# 素材放大前检查清单：{material_name}")
    lines.append(f"素材等级：{classification['grade']}（{total}分）")
    lines.append("")
    lines.append("投放放大前请逐项确认：")
    lines.append("")
    
    checklist = [
        ("关键词统一", "素材关键词 = 搜索词 = 商品标题词"),
        ("商品标题承接", "商品标题包含素材中的核心关键词"),
        ("详情页首屏承接", "首屏信息与素材种草理由一致"),
        ("客服准备", "客服话术覆盖素材评论区常见问题"),
        ("评论区问题整理", "整理评论区高频提问供客服/直播使用"),
        ("投放指标确认", "CTR/进店率/加购率等指标达到投放基准"),
        ("二次剪辑可能", "素材可拆解为多版本用于不同渠道"),
        ("直播间承接", "直播间话术已准备对应素材引流场景"),
    ]
    
    for i, (item, standard) in enumerate(checklist, 1):
        lines.append(f"- [ ] {i}. {item}：{standard}")
    
    lines.append("")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 scoring_tool.py <materials.json>")
        print("或者: python3 scoring_tool.py --dimensions  (查看评分维度)")
        print("或者: python3 scoring_tool.py --classify <score>  (查看分级)")
        sys.exit(1)

    if sys.argv[1] == "--dimensions":
        print(json.dumps(SCORING_DIMENSIONS, ensure_ascii=False, indent=2))
        return
    
    if sys.argv[1] == "--classify":
        score = int(sys.argv[2])
        result = classify_material(score)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)

    materials = data.get("materials", [])
    
    print(generate_scoring_table(materials))
    print("---\n")
    
    if data.get("priority_list", True):
        print(generate_priority_list(materials))
    
    if data.get("checklists", False):
        for m in materials:
            total = sum(m.get("scores", {}).values())
            if total >= 20:  # A级或B级才生成检查清单
                print(generate_checklist(m["name"], m.get("scores", {})))
                print("---\n")


if __name__ == "__main__":
    main()
