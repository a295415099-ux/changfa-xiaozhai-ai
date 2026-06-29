#!/usr/bin/env python3
"""
检查断链类型归类脚本
输入检查结果JSON，自动归类到四种断链类型并给出优先级建议。
"""
import json, sys
from collections import defaultdict

BREAK_TYPES = {
    "keyword": {
        "name": "关键词断链",
        "keywords": ["关键词", "搜索词", "不知道搜什么", "没种词", "种词", "品牌词", "品类词", "卖点词", "场景词", "搜索导向"],
        "description": "内容有热度但用户不知道下一步搜什么"
    },
    "search": {
        "name": "搜索承接断链",
        "keywords": ["搜索承接", "搜不到", "接不住", "商品标题", "详情页", "店铺页", "搜出来", "承接", "搜索页"],
        "description": "用户搜了但搜出来的页接不住"
    },
    "benefit": {
        "name": "利益点断链",
        "keywords": ["利益点", "购买理由", "为什么买", "优惠", "促销", "限时", "转化", "CTA", "加购", "领券"],
        "description": "用户进来但没有明确购买理由"
    },
    "rhythm": {
        "name": "节奏错位断链",
        "keywords": ["节奏", "时间", "排期", "同步", "上线", "发布", "直播时间", "活动页上线", "时间错位"],
        "description": "内容先做但搜索/直播/活动没跟上"
    }
}

def classify_breaks(check_results):
    """根据检查结果关键词归类断链类型"""
    classified = defaultdict(list)
    for item in check_results:
        check_name = item.get("check_name", "")
        finding = item.get("finding", "")
        combined = check_name + finding
        for btype, binfo in BREAK_TYPES.items():
            for kw in binfo["keywords"]:
                if kw in combined:
                    classified[btype].append(item)
                    break
    return classified

if __name__ == "__main__":
    if len(sys.argv) < 2:
        results = json.load(sys.stdin)
    else:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            results = json.load(f)

    classified = classify_breaks(results)
    print("# 断链类型归类结果\n")
    for btype in ["keyword", "search", "benefit", "rhythm"]:
        items = classified.get(btype, [])
        info = BREAK_TYPES[btype]
        print(f"## {info['name']}")
        print(f"本质：{info['description']}")
        print(f"发现断点数量：{len(items)}")
        if items:
            for item in items:
                print(f"  - {item.get('check_name', 'N/A')}: {item.get('finding', 'N/A')[:80]}")
        print()
    print("## 优先级建议")
    by_count = sorted(classified.items(), key=lambda x: len(x[1]), reverse=True)
    for i, (btype, items) in enumerate(by_count):
        if items:
            print(f"{i+1}. {BREAK_TYPES[btype]['name']} — {len(items)}个断点 — {'P0立即修复' if i == 0 else 'P1本周修复' if i == 1 else 'P2本月修复'}")
