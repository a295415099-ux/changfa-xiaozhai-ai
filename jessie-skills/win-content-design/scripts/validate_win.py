#!/usr/bin/env python3
"""
W+I→N内容设计框架 - 执行辅助脚本
用于检查WIN三层设计的基本结构和链路完整性。
"""

import json
import sys
from pathlib import Path


def validate_win_structure(data: dict) -> dict:
    """验证W+I→N三层结构是否完整"""
    results = {
        "passed": [],
        "warnings": [],
        "errors": [],
    }

    # 检查三层是否都存在
    for layer in ["W", "I", "N"]:
        if layer not in data or not data[layer]:
            results["errors"].append(f"{layer}层缺少内容设计")
        else:
            if not isinstance(data[layer], list) or len(data[layer]) == 0:
                results["errors"].append(f"{layer}层内容为空")
            else:
                results["passed"].append(f"{layer}层内容已设计（{len(data[layer])}条）")

    # 检查链路连接
    if "W" in data and "I" in data and data.get("W") and data.get("I"):
        has_W_to_I = any(
            item.get("next_step", "").upper() in ["I", "→I", "→ I"]
            or item.get("导向", "").upper() in ["I", "→I", "→ I"]
            for item in data["W"]
        )
        if not has_W_to_I:
            results["warnings"].append("W层内容缺少到I层的导向链接")
        else:
            results["passed"].append("W→I链路已确认")

    if "I" in data and "N" in data and data.get("I") and data.get("N"):
        has_I_to_N = any(
            item.get("next_step", "").upper() in ["N", "→N", "→ N"]
            or item.get("导向", "").upper() in ["N", "→N", "→ N"]
            for item in data["I"]
        )
        if not has_I_to_N:
            results["warnings"].append("I层内容缺少到N层的导向链接")
        else:
            results["passed"].append("I→N链路已确认")

    # 检查N层是否有明确承接动作
    if "N" in data and data.get("N"):
        has_cta = any(
            item.get("承接动作") or item.get("action") or item.get("cta")
            for item in data["N"]
        )
        if not has_cta:
            results["errors"].append("N层内容缺少明确承接动作（导店/导商品/导直播等）")
        else:
            results["passed"].append("N层承接动作已确认")

    # 检查SKU是否定义
    if not data.get("core_sku"):
        results["errors"].append("缺少核心SKU定义")
    else:
        results["passed"].append(f"核心SKU已定义：{data['core_sku']}")

    return results


def print_result(results: dict):
    """格式化输出检查结果"""
    print("\n" + "=" * 60)
    print("  W+I→N 内容设计框架 - 结构检查报告")
    print("=" * 60)

    if results["errors"]:
        print(f"\n❌ 错误 ({len(results['errors'])}项)：")
        for e in results["errors"]:
            print(f"   - {e}")

    if results["warnings"]:
        print(f"\n⚠️  警告 ({len(results['warnings'])}项)：")
        for w in results["warnings"]:
            print(f"   - {w}")

    if results["passed"]:
        print(f"\n✅ 通过 ({len(results['passed'])}项)：")
        for p in results["passed"]:
            print(f"   - {p}")

    total = len(results["errors"]) + len(results["warnings"])
    if results["errors"]:
        print(f"\n🔴 整体结论：不通过（{total}个问题待解决）")
    elif results["warnings"]:
        print(f"\n🟡 整体结论：通过（有{len(results['warnings'])}个优化建议）")
    else:
        print(f"\n🟢 整体结论：全部通过！")
    print()


def main():
    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])
    else:
        input_file = Path(sys.stdin.read().strip()) if not sys.stdin.isatty() else None

    if not input_file or not input_file.exists():
        print("用法：python validate_win.py <json文件>")
        print("或从stdin传入JSON数据")
        sys.exit(1)

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = validate_win_structure(data)
    print_result(results)

    # 输出可被程序解析的结果码
    if results["errors"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
