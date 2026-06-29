#!/usr/bin/env python3
"""
AI三维洞察SOP — 分析流程辅助脚本

用于按阶段生成结构化输出，辅助执行19步SOP。
用法：python analysis_runner.py <阶段> [参数]
"""

import json
import sys
from datetime import datetime

# 阶段定义
PHASES = {
    "scope": {
        "name": "阶段一：定义范围",
        "steps": [1, 2, 3, 4, 5, 6],
        "description": "明确对象 → 拆解问题 → 补充背景 → 确认竞品 → 确认同行 → 确定趋势范围"
    },
    "competitor": {
        "name": "阶段二：竞品分析",
        "steps": [7, 8, 9, 10],
        "description": "抓取竞品内容 → 竞品归类 → 策略分析 → 话术提炼"
    },
    "peer": {
        "name": "阶段三：同行分析",
        "steps": [11, 12, 13],
        "description": "抓取同行内容 → 同行场景分析 → 爆款因子分析"
    },
    "trend": {
        "name": "阶段四：趋势分析",
        "steps": [14, 15],
        "description": "趋势信号收集 → 兴趣点变化分析"
    },
    "strategy": {
        "name": "阶段五：综合判断与行动",
        "steps": [16, 17, 18, 19],
        "description": "三维对比 → 提炼机会点 → 转成策略 → 生成行动表"
    }
}

DELIVERABLES = [
    {"name": "竞品传播分析表", "fields": ["品牌", "平台", "主推产品", "核心卖点",
                                          "标题风格", "正文结构", "高频话术", "情绪调性",
                                          "互动数据", "可借鉴点"]},
    {"name": "同行场景机会表", "fields": ["品牌", "场景类型", "表达方式", "互动情况",
                                          "可借鉴点", "差异化机会"]},
    {"name": "趋势变化观察表", "fields": ["趋势信号", "热词", "用户评论", "高频问题",
                                          "变化判断", "对本品牌的影响"]},
    {"name": "三维对比矩阵", "fields": ["交集", "差异", "空白机会", "潜在风险", "建议动作"]},
    {"name": "7天/30天行动表", "fields": ["天数/周次", "目标", "具体动作", "内容形式",
                                          "发布平台", "观察指标", "负责人"]}
]


def list_phases():
    """列出所有阶段"""
    print("AI三维洞察SOP — 五阶段流程\n")
    for key, phase in PHASES.items():
        print(f"  [{key}] {phase['name']}")
        print(f"       步骤 {phase['steps']}")
        print(f"       {phase['description']}\n")


def list_deliverables():
    """列出交付物模板"""
    print("交付物清单\n")
    for i, d in enumerate(DELIVERABLES, 1):
        print(f"  {i}. {d['name']}")
        print(f"     字段：{', '.join(d['fields'])}\n")


def generate_checklist():
    """生成执行检查清单"""
    steps = [
        (1, "明确对象", "定义本次洞察范围"),
        (2, "拆解问题", "把大问题拆成三维问题"),
        (3, "补充背景", "给AI喂业务上下文"),
        (4, "确认竞品", "锁定直接竞品与替代型竞品"),
        (5, "确认同行", "建立同行参考池"),
        (6, "确定趋势范围", "明确趋势观察口径"),
        (7, "抓取竞品内容", "收集竞品样本"),
        (8, "竞品归类", "看清竞品内容结构"),
        (9, "竞品策略分析", "提炼竞品传播打法"),
        (10, "竞品话术提炼", "找出可学习的话术规律"),
        (11, "抓取同行内容", "看行业主流都在打什么"),
        (12, "同行场景分析", "识别行业常见场景"),
        (13, "爆款因子分析", "找出更容易出圈的内容结构"),
        (14, "趋势信号收集", "收集行业与用户变化"),
        (15, "兴趣点变化分析", "看用户偏好正在怎么变化"),
        (16, "三维对比", "把三类信息放在一起判断"),
        (17, "提炼机会点", "识别品牌可切入的位置"),
        (18, "转成策略", "从洞察反推内容策略"),
        (19, "生成行动表", "形成下一步测试动作"),
    ]

    print("AI三维洞察SOP 执行检查清单\n")
    print(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    phase_names = {1: "阶段一：定义范围", 7: "阶段二：竞品分析",
                   11: "阶段三：同行分析", 14: "阶段四：趋势分析",
                   16: "阶段五：综合判断与行动"}

    current_phase = ""
    for num, task, goal in steps:
        if num in phase_names:
            current_phase = phase_names[num]
            print(f"\n{'='*50}")
            print(f"  {current_phase}")
            print(f"{'='*50}")

        print(f"  [ ] 步骤{num}: {task} — {goal}")

    print(f"\n{'='*50}")
    print("  输出交付物")
    print(f"{'='*50}")
    for i, d in enumerate(DELIVERABLES, 1):
        print(f"  [ ] {i}. {d['name']}")


def main():
    if len(sys.argv) < 2:
        print("AI三维洞察SOP 分析流程辅助脚本\n")
        print("用法:")
        print("  python analysis_runner.py phases        — 列出所有阶段")
        print("  python analysis_runner.py deliverables  — 列出交付物模板")
        print("  python analysis_runner.py checklist     — 生成执行检查清单")
        print("  python analysis_runner.py step <N>      — 查看第N步详情")
        return

    cmd = sys.argv[1]

    if cmd == "phases":
        list_phases()
    elif cmd == "deliverables":
        list_deliverables()
    elif cmd == "checklist":
        generate_checklist()
    elif cmd == "step" and len(sys.argv) > 2:
        step_num = int(sys.argv[2])
        print(f"查看步骤 {step_num} 详情\n")
        print("请参考 SKILL.md 中对应的步骤描述和 references/prompts.md 中的提示词模板。")
    else:
        print(f"未知命令: {cmd}")
        print("可用命令: phases, deliverables, checklist, step")


if __name__ == "__main__":
    main()
