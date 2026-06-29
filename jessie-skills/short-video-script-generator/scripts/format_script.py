#!/usr/bin/env python3
"""
短视频脚本表格式化输出脚本。
读取 JSON 格式的脚本数据，输出格式化的 Markdown 表格。
"""

import json
import sys


def format_script_table(data: dict) -> str:
    """将脚本JSON数据格式化为Markdown表格"""
    title = data.get("title", "短视频脚本表")
    shots = data.get("shots", [])

    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append("| 镜头 | 画面 | 口播 | 字幕 | 对应卖点 | 拍摄提示 |")
    lines.append("|------|------|------|------|----------|----------|")

    for shot in shots:
        idx = shot.get("index", "")
        scene = shot.get("scene", "").replace("|", "\\|")
        voice = shot.get("voice", "").replace("|", "\\|")
        subtitle = shot.get("subtitle", "").replace("|", "\\|")
        selling_point = shot.get("selling_point", "").replace("|", "\\|")
        tip = shot.get("tip", "").replace("|", "\\|")
        lines.append(f"| {idx} | {scene} | {voice} | {subtitle} | {selling_point} | {tip} |")

    # 附加信息
    if "hook" in data:
        lines.append(f"\n## 开头钩子\n{data['hook']}")
    if "cta" in data:
        lines.append(f"\n## 行动引导\n{data['cta']}")
    if "taobao_guide" in data:
        lines.append(f"\n## 淘内承接建议\n{data['taobao_guide']}")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: format_script.py <script.json>")
        print("Or pipe JSON: cat script.json | python3 format_script.py -")
        sys.exit(1)

    if sys.argv[1] == "-":
        raw = sys.stdin.read()
    else:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            raw = f.read()

    data = json.loads(raw)
    output = format_script_table(data)
    print(output)


if __name__ == "__main__":
    main()
