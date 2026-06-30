from pathlib import Path
import html


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/diagrams/sop-swimlanes"


PALETTE = {
    "bg": "#f6f4ef",
    "paper": "#fffdf8",
    "text": "#1f2933",
    "muted": "#687383",
    "line": "#d7d1c6",
    "green": "#146c5c",
    "green_dark": "#0f5148",
    "green_soft": "#dcefe8",
    "gold": "#c99a3e",
    "gold_soft": "#f4e8c8",
    "rose": "#b46a55",
    "rose_soft": "#f1d9cf",
    "blue": "#4f7f9f",
    "blue_soft": "#dce9ef",
    "purple": "#7566a5",
    "purple_soft": "#e4e0f0",
}


def wrap(text, max_chars=9):
    chunks = []
    current = ""
    for char in text:
        current += char
        if len(current) >= max_chars:
            chunks.append(current)
            current = ""
    if current:
        chunks.append(current)
    return chunks


def node(x, y, w, h, label, fill, stroke, title=False):
    lines = wrap(label, 9 if w < 130 else 12)
    font_size = 18 if title else 15
    line_height = 22 if title else 19
    start_y = y + h / 2 - (len(lines) - 1) * line_height / 2 + 5
    text_lines = "\n".join(
        f'<text x="{x + w / 2}" y="{start_y + i * line_height}" text-anchor="middle" '
        f'font-size="{font_size}" font-weight="{"700" if title else "600"}" fill="{PALETTE["text"]}">{html.escape(line)}</text>'
        for i, line in enumerate(lines)
    )
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="1.5"/>\n{text_lines}'
    )


def arrow(x1, y1, x2, y2, color=None):
    color = color or PALETTE["muted"]
    return (
        f'<path d="M{x1} {y1} C {(x1 + x2) / 2} {y1}, {(x1 + x2) / 2} {y2}, {x2} {y2}" '
        f'fill="none" stroke="{color}" stroke-width="2" marker-end="url(#arrow)"/>'
    )


def swimlane_svg(title, subtitle, lanes, filename):
    width = 1680
    margin = 44
    header_h = 104
    lane_h = 108
    step_w = 132
    step_gap = 28
    lane_label_w = 156
    max_steps = max(len(lane["steps"]) for lane in lanes)
    content_w = lane_label_w + max_steps * step_w + (max_steps - 1) * step_gap
    height = header_h + len(lanes) * lane_h + 52
    start_x = margin + lane_label_w + 24

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<defs>",
        '<marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">',
        f'<path d="M0,0 L0,6 L9,3 z" fill="{PALETTE["muted"]}"/>',
        "</marker>",
        "</defs>",
        f'<rect width="{width}" height="{height}" fill="{PALETTE["bg"]}"/>',
        f'<rect x="20" y="20" width="{width - 40}" height="{height - 40}" rx="20" fill="{PALETTE["paper"]}" stroke="{PALETTE["line"]}"/>',
        f'<text x="{margin}" y="62" font-size="34" font-weight="800" fill="{PALETTE["green_dark"]}">{html.escape(title)}</text>',
        f'<text x="{margin}" y="92" font-size="16" fill="{PALETTE["muted"]}">{html.escape(subtitle)}</text>',
    ]

    for lane_index, lane in enumerate(lanes):
        y = header_h + lane_index * lane_h
        fill = "#fbfaf6" if lane_index % 2 == 0 else "#f1ede4"
        svg.append(f'<rect x="32" y="{y}" width="{width - 64}" height="{lane_h}" fill="{fill}"/>')
        svg.append(f'<line x1="32" y1="{y}" x2="{width - 32}" y2="{y}" stroke="{PALETTE["line"]}" stroke-width="1"/>')
        svg.append(
            node(
                margin,
                y + 20,
                lane_label_w,
                lane_h - 40,
                lane["name"],
                lane["label_fill"],
                lane["label_stroke"],
                True,
            )
        )
        last = None
        for step_index, step in enumerate(lane["steps"]):
            x = start_x + step_index * (step_w + step_gap)
            if step is None:
                continue
            svg.append(node(x, y + 23, step_w, lane_h - 46, step, lane["fill"], lane["stroke"]))
            if last is not None:
                svg.append(arrow(last[0] + step_w, last[1], x, y + lane_h / 2))
            last = (x, y + lane_h / 2)

    svg.append(f'<text x="{width - margin}" y="{height - 24}" text-anchor="end" font-size="14" fill="{PALETTE["muted"]}">长发小寨 AI 总控工作台 / SOP 泳道图</text>')
    svg.append("</svg>")
    (OUT / filename).write_text("\n".join(svg), encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    swimlane_svg(
        "品牌设计部总泳道图",
        "把电商设计、社媒推广、包装设计统一放进需求、语义、设计、上线、复盘、沉淀的总控链路",
        [
            {"name": "需求方/业务", "label_fill": PALETTE["gold_soft"], "label_stroke": PALETTE["gold"], "fill": "#fff7df", "stroke": PALETTE["gold"], "steps": ["提出需求", "补齐资料", "确认目标", "确认上线", "接收复盘"]},
            {"name": "品牌负责人", "label_fill": PALETTE["green_soft"], "label_stroke": PALETTE["green"], "fill": "#eef7f2", "stroke": PALETTE["green"], "steps": [None, "语义校准", "审核 brief", "终稿确认", "资产沉淀"]},
            {"name": "Codex 总控", "label_fill": PALETTE["purple_soft"], "label_stroke": PALETTE["purple"], "fill": "#f0edf8", "stroke": PALETTE["purple"], "steps": ["需求归类", "资料检查", "调度 Skill", "上线检查", "复盘判断"]},
            {"name": "设计部", "label_fill": PALETTE["blue_soft"], "label_stroke": PALETTE["blue"], "fill": "#eef6fa", "stroke": PALETTE["blue"], "steps": [None, "方向探索", "设计深化", "交付文件", "模板沉淀"]},
            {"name": "渠道/数据", "label_fill": PALETTE["rose_soft"], "label_stroke": PALETTE["rose"], "fill": "#fbefeb", "stroke": PALETTE["rose"], "steps": [None, "提供规则", "上线执行", "数据回收", "指标复盘"]},
        ],
        "00-品牌设计部总泳道图.svg",
    )

    swimlane_svg(
        "品牌设计全流程 SOP 泳道图",
        "从需求进入到资产沉淀，明确业务、品牌、AI、设计和数据各自负责的动作",
        [
            {"name": "需求方", "label_fill": PALETTE["gold_soft"], "label_stroke": PALETTE["gold"], "fill": "#fff7df", "stroke": PALETTE["gold"], "steps": ["需求进入", "资料提供", "目标确认", "上线接收", "结果反馈"]},
            {"name": "品牌负责人", "label_fill": PALETTE["green_soft"], "label_stroke": PALETTE["green"], "fill": "#eef7f2", "stroke": PALETTE["green"], "steps": [None, "品牌语义", "策略审核", "终稿确认", "资产归档"]},
            {"name": "Codex/AI", "label_fill": PALETTE["purple_soft"], "label_stroke": PALETTE["purple"], "fill": "#f0edf8", "stroke": PALETTE["purple"], "steps": ["任务归类", "资料检查", "AI方向探索", "审核清单", "复盘建议"]},
            {"name": "设计部", "label_fill": PALETTE["blue_soft"], "label_stroke": PALETTE["blue"], "fill": "#eef6fa", "stroke": PALETTE["blue"], "steps": [None, "设计 brief", "设计深化", "上线交付", "模板沉淀"]},
            {"name": "数据/渠道", "label_fill": PALETTE["rose_soft"], "label_stroke": PALETTE["rose"], "fill": "#fbefeb", "stroke": PALETTE["rose"], "steps": [None, "渠道规则", "上线排期", "数据复盘", "指标沉淀"]},
        ],
        "01-品牌设计全流程SOP泳道图.svg",
    )

    swimlane_svg(
        "电商设计 SOP 泳道图",
        "围绕商品、搜索、页面、上线和成交数据，把电商设计变成可复盘的转化链路",
        [
            {"name": "电商运营", "label_fill": PALETTE["gold_soft"], "label_stroke": PALETTE["gold"], "fill": "#fff7df", "stroke": PALETTE["gold"], "steps": ["提出需求", "商品资料", "活动机制", "上线排期", "回收数据"]},
            {"name": "品牌/内容", "label_fill": PALETTE["green_soft"], "label_stroke": PALETTE["green"], "fill": "#eef7f2", "stroke": PALETTE["green"], "steps": [None, "卖点统一", "搜索词统一", "承接检查", "内容复用"]},
            {"name": "Codex/悟空", "label_fill": PALETTE["purple_soft"], "label_stroke": PALETTE["purple"], "fill": "#f0edf8", "stroke": PALETTE["purple"], "steps": ["需求判断", "资料检查", "结构建议", "上线检查", "经营判断"]},
            {"name": "电商设计", "label_fill": PALETTE["blue_soft"], "label_stroke": PALETTE["blue"], "fill": "#eef6fa", "stroke": PALETTE["blue"], "steps": [None, "转化路径", "设计初稿", "切图交付", "素材沉淀"]},
            {"name": "数据/投放", "label_fill": PALETTE["rose_soft"], "label_stroke": PALETTE["rose"], "fill": "#fbefeb", "stroke": PALETTE["rose"], "steps": [None, "历史数据", "投放适配", "上线观察", "7天复盘"]},
        ],
        "02-电商设计SOP泳道图.svg",
    )

    swimlane_svg(
        "品牌社媒推广设计 SOP 泳道图",
        "从传播目标到互动和搜索回流，确保社媒内容不是单条素材，而是可沉淀的内容资产",
        [
            {"name": "品牌/业务", "label_fill": PALETTE["gold_soft"], "label_stroke": PALETTE["gold"], "fill": "#fff7df", "stroke": PALETTE["gold"], "steps": ["传播目标", "人群场景", "主题确认", "发布确认", "反馈输入"]},
            {"name": "内容团队", "label_fill": PALETTE["green_soft"], "label_stroke": PALETTE["green"], "fill": "#eef7f2", "stroke": PALETTE["green"], "steps": [None, "栏目规划", "标题脚本", "发布执行", "评论复盘"]},
            {"name": "Codex/AI", "label_fill": PALETTE["purple_soft"], "label_stroke": PALETTE["purple"], "fill": "#f0edf8", "stroke": PALETTE["purple"], "steps": ["需求拆解", "选题生成", "画面探索", "发布检查", "回流观察"]},
            {"name": "社媒设计", "label_fill": PALETTE["blue_soft"], "label_stroke": PALETTE["blue"], "fill": "#eef6fa", "stroke": PALETTE["blue"], "steps": [None, "平台适配", "视觉生产", "版本交付", "模板沉淀"]},
            {"name": "平台/数据", "label_fill": PALETTE["rose_soft"], "label_stroke": PALETTE["rose"], "fill": "#fbefeb", "stroke": PALETTE["rose"], "steps": [None, "平台规则", "上线发布", "互动搜索", "内容资产"]},
        ],
        "03-社媒推广SOP泳道图.svg",
    )

    swimlane_svg(
        "包装设计 SOP 泳道图",
        "把包装策略、结构工艺、打样量产和上市联动统一管理，避免包装和电商社媒各说各话",
        [
            {"name": "产品/业务", "label_fill": PALETTE["gold_soft"], "label_stroke": PALETTE["gold"], "fill": "#fff7df", "stroke": PALETTE["gold"], "steps": ["上市需求", "产品资料", "成本边界", "量产确认", "上市反馈"]},
            {"name": "品牌负责人", "label_fill": PALETTE["green_soft"], "label_stroke": PALETTE["green"], "fill": "#eef7f2", "stroke": PALETTE["green"], "steps": [None, "商品语义", "包装 brief", "打样评审", "系列规范"]},
            {"name": "Codex/AI", "label_fill": PALETTE["purple_soft"], "label_stroke": PALETTE["purple"], "fill": "#f0edf8", "stroke": PALETTE["purple"], "steps": ["需求归类", "品类研究", "方向探索", "联动清单", "复盘沉淀"]},
            {"name": "包装设计", "label_fill": PALETTE["blue_soft"], "label_stroke": PALETTE["blue"], "fill": "#eef6fa", "stroke": PALETTE["blue"], "steps": [None, "视觉方向", "设计深化", "量产文件", "资产沉淀"]},
            {"name": "供应链/渠道", "label_fill": PALETTE["rose_soft"], "label_stroke": PALETTE["rose"], "fill": "#fbefeb", "stroke": PALETTE["rose"], "steps": [None, "工艺合规", "打样量产", "上市素材", "问题反馈"]},
        ],
        "04-包装设计SOP泳道图.svg",
    )


if __name__ == "__main__":
    main()
