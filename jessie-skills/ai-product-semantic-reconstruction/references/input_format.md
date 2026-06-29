# generate_outputs.py 输入JSON格式说明

步骤3-9的盘点结果需按以下JSON结构组织，作为脚本输入：

```json
{
  "product": {
    "name": "商品名称",
    "identity": "一句话身份定义（用户价值身份）",
    "one_liner": "一句话推荐理由"
  },
  "target_audience": [
    {
      "label": "人群标签",
      "fit_reason": "转化理由"
    }
  ],
  "use_scenarios": [
    {
      "category": "场景分类",
      "situation": "具体情境描述",
      "keywords": "检索关键词(逗号分隔)",
      "solution": "商品在此场景的角色"
    }
  ],
  "core_pain_points": [
    {
      "label": "痛点标签",
      "description": "痛点描述(用户语言)",
      "context": "发生场景",
      "keywords": "检索关键词",
      "user_question": "用户会怎么问",
      "solution_description": "本商品如何解决"
    }
  ],
  "functional_features": [
    {
      "user_problem": "用户遇到什么问题",
      "function": "对应功能",
      "principle": "解决原理",
      "user_benefit": "用户感知收益"
    }
  ],
  "emotional_values": [
    {
      "type": "情绪类型(生活感/身份感/审美感/陪伴感/安心感)",
      "description": "用户感受描述",
      "trigger": "触发情境"
    }
  ],
  "trust_evidence": [
    {
      "type": "证据类型(评价/案例/销量/达人/资质)",
      "content": "具体内容",
      "source": "来源"
    }
  ],
  "comparative_advantages": [
    {
      "dimension": "对比维度",
      "common_situation": "同类常见情况",
      "difference": "本商品差异点"
    }
  ],
  "complementary_products": [
    {
      "name": "搭配商品名",
      "scene": "搭配场景",
      "keywords": "检索关键词"
    }
  ],
  "comparison_summary": "对比总体总结",
  "trigger_keywords": ["触发词1", "触发词2", "触发词3"]
}
```
