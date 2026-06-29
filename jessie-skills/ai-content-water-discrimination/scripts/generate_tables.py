#!/usr/bin/env python3
"""
内容蓄水判断表生成脚本
根据输入的内容数据，生成标准化的内容蓄水判断表（CSV格式）和老板版摘要。
"""
import csv
import json
import sys
from datetime import datetime

def generate_judgment_table(content_data, output_path):
    """生成内容蓄水判断表CSV"""
    headers = [
        "内容名称/编号", "平台", "所属WIN层", "有没有种购买理由",
        "有没有种搜索心智", "最终导向目标", "发布时间是否合适",
        "是否是真蓄水内容", "理由说明", "优先级", "备注"
    ]
    
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for item in content_data:
            writer.writerow([
                item.get("name", ""),
                item.get("platform", ""),
                item.get("win_layer", ""),
                item.get("has_purchase_reason", ""),
                item.get("has_search_mindset", ""),
                item.get("target_goal", ""),
                item.get("time_suitable", ""),
                item.get("is_real_water", ""),
                item.get("reason", ""),
                item.get("priority", ""),
                item.get("notes", "")
            ])
    
    print(f"✅ 内容蓄水判断表已生成：{output_path}")
    return output_path


def generate_boss_summary(judgment_results, output_path):
    """生成老板版摘要"""
    real_waters = [r for r in judgment_results if r.get("is_real_water") == "是"]
    noise_contents = [r for r in judgment_results if r.get("is_real_water") == "否"]
    
    summary = f"""# 内容蓄水判断 · 老板版摘要
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 一句话结论
当前共判断 {len(judgment_results)} 条内容动作，其中 {len(real_waters)} 条为真蓄水内容，{len(noise_contents)} 条为热闹内容（伪忙碌）。

## 当前最值得优先做的蓄水内容
"""
    for r in real_waters:
        summary += f"- **{r.get('name', 'N/A')}**：{r.get('reason', '')}，优先导向{r.get('target_goal', '')}\n"
    
    summary += "\n## 哪些内容只是热闹内容\n"
    for r in noise_contents:
        summary += f"- **{r.get('name', 'N/A')}**：{r.get('reason', '')}\n"
    
    summary += "\n## 本周最该先做的动作\n"
    for i, r in enumerate(real_waters[:3] if len(real_waters) >= 3 else real_waters, 1):
        summary += f"{i}. {r.get('name', 'N/A')} — {r.get('target_goal', '')}\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"✅ 老板版摘要已生成：{output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 generate_tables.py <input_json_file>")
        print("JSON格式：[{'name':'...', 'platform':'...', ...}, ...]")
        sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    generate_judgment_table(data, f"content_water_judgment_{timestamp}.csv")
    generate_boss_summary(data, f"boss_summary_{timestamp}.md")
