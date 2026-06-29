# AI 与 Skill 调度手册

## 总控原则

Codex 是总控，不是单个工具。所有 AI 工具都要被放进业务流程里使用：

- Codex 负责判断、拆解、调度、整合、校验和沉淀。
- Jessie Skill 负责电商内容流量和经营 SOP。
- 外部 AI 负责图像、视频、语义扩写、素材生成等专项能力。
- 悟空这类平台 Agent 负责特定平台任务，例如淘宝/天猫域内的搜索、承接、投放和成交。
- 设计师负责审美判断、品牌把关、落地文件和最终质量。

## 品牌设计部任务分类

| 任务类型 | 典型需求 | 主调度 |
|---|---|---|
| 品牌表达统一 | 品牌定位、卖点、关键词、语义资产 | Codex + `brand-semantic-asset-sop` |
| 电商设计 | 主图、详情页、活动页、投放素材 | Codex + 电商承接类 Skill |
| 社媒推广 | 小红书、抖音、视频号、私域海报 | Codex + 内容生产类 Skill |
| 包装设计 | 包装 brief、视觉方向、上市联动 | Codex + 商品语义/信任证据 Skill |
| 数据复盘 | 素材评分、搜索回流、转化判断 | Codex + 复盘/经营判断 Skill |
| 团队推进 | 分工、排期、甘特图、7/60天计划 | Codex + 执行复盘类 Skill |

## Jessie Skill 调度地图

### 1. 品牌与商品语义

适用于品牌定位、SKU 卖点、包装语言、详情页语言、社媒语言统一。

优先调用：

- `brand-semantic-asset-sop`
- `ai-product-semantic-reconstruction`
- `ai-trust-evidence-chain`
- `keyword-unified-sop`

输出：

- 品牌语义资产表。
- 商品推荐理由语料。
- 信任证据链。
- 三类关键词表。

### 2. 电商设计与承接

适用于主图、详情页、活动页、店铺页、投放素材。

优先调用：

- `ai-store-reception-optimization`
- `ai-content-reception-checklist`
- `ai-external-content-internal-receiving`
- `ai-content-search-connect`

输出：

- 店铺承接优化动作清单。
- 内容到承接检查表。
- 外种内收路径图。
- 内容-搜索-承接连接表。

### 3. 社媒推广与内容生产

适用于小红书、抖音、视频号、私域内容。

优先调用：

- `win-content-design`
- `short-video-script-generator`
- `xiaohongshu-note-generator`
- `ai-content-standard-template`
- `private-domain-content`

输出：

- 内容分层设计。
- 短视频脚本。
- 小红书笔记。
- 内容表达标准。
- 私域触达内容。

### 4. 包装设计与上市联动

Jessie Skill 里没有独立包装设计 Skill，但可以由以下能力组合：

- `brand-semantic-asset-sop`：包装品牌表达。
- `ai-product-semantic-reconstruction`：包装卖点与购买理由。
- `ai-trust-evidence-chain`：包装信任证据。
- `ai-content-reference-map`：包装上市后的内容可引用地图。
- `short-video-script-generator`：包装开箱/新品视频。
- `xiaohongshu-note-generator`：包装上新种草笔记。

输出：

- 包装设计 brief。
- 包装信息层级表。
- 包装上市联动清单。
- 包装社媒内容脚本。

### 5. 素材筛选与复盘

适用于判断哪些设计、内容、素材值得继续放大。

优先调用：

- `quality-material-screening`
- `ai-search-reflow-observation-sop`
- `post-promo-content-review`
- `ai-business-judgment`

输出：

- 素材评分表。
- 搜索回流观察表。
- 内容资产复盘表。
- AI 辅助经营判断表。

### 6. 团队执行与排期

适用于设计部跨电商、社媒、包装推进。

优先调用：

- `ai-roles-division`
- `team-leader-promotion-sop`
- `ai-back-to-store-7day-sop`
- `ai-post-training-gantt-chart`
- `ai-60day-training-camp`

输出：

- 三角色分工表。
- 负责人推进表。
- 7天行动清单。
- 甘特图。
- 60天任务表。

## 外部 AI 调度边界

| 工具类型 | 适合做 | 不适合做 |
|---|---|---|
| 千问/豆包/通义 | 商品识别、卖点扩写、内容初稿、资料整理 | 最终经营判断、品牌拍板 |
| 生图工具 | 视觉方向、场景图、详情图概念、产品摄影探索 | 最终印刷文件、合规包装终稿 |
| 视频工具 | 产品展示、口播、开箱、使用场景视频初稿 | 最终无审校发布 |
| 阿里生态数据 | 搜索、投放、成交、承接复盘 | 替代品牌策略判断 |
| 悟空类平台 Agent | 淘宝/天猫平台内的商品、搜索、店铺、投放、成交建议 | 跨平台品牌总控、包装策略、社媒传播总判断 |
| Codex | 调度、写 SOP、生成文档/表格、整理知识库 | 代替老板最终拍板 |

## 悟空的接入方式

悟空应被定位为淘宝/天猫专项 Agent。它可以参与淘内经营判断，但不能替代长发小寨 Codex 的总控角色。

推荐分工：

| 事项 | 悟空负责 | Codex负责 |
|---|---|---|
| 淘内搜索 | 分析搜索词、商品标题、搜索承接 | 判断这些词是否与品牌社媒和包装语言一致 |
| 店铺承接 | 检查商品页、活动页、店铺页 | 判断是否接住外部种草和品牌表达 |
| 投放建议 | 给出阿里生态投放优化方向 | 判断素材是否值得放大、是否沉淀为资产 |
| 成交复盘 | 看淘内成交与转化 | 合并社媒、包装、私域和品牌资产复盘 |
| 页面优化 | 给出淘内页面建议 | 生成设计 brief 并交给设计部执行 |

接入原则：

1. Codex 给悟空分配任务。
2. 悟空返回淘内建议。
3. Codex 做跨平台验证。
4. 设计部按 SOP 执行。
5. 结果回到品牌资产库和复盘库。

## 标准调用流程

1. 先判断任务归属：电商、社媒、包装、品牌资产、复盘、团队执行。
2. 读取对应 SOP。
3. 判断所需资料是否齐全。
4. 调用对应 Jessie Skill 或外部 AI。
5. 输出初稿。
6. 按品牌、渠道、转化、合规四个维度校验。
7. 形成交付物。
8. 上线后复盘并沉淀进资产库。

## 品牌设计部 AI 工作台建议

建议建立 6 个固定资料区：

1. 品牌资料库：定位、VI、字体、色彩、品牌故事。
2. SKU 资料库：产品信息、卖点、规格、价格、证据。
3. 视觉资产库：主图、详情页、包装、社媒模板、投放素材。
4. 内容资产库：脚本、笔记、标题、私域话术。
5. 数据复盘库：搜索、点击、转化、ROI、用户反馈。
6. SOP 与模板库：本文件包、Jessie Skill、表格模板。

## 当前优先级

第一优先级：先把品牌语义资产和 SKU 资料补齐。

第二优先级：选 1 个核心 SKU 跑通电商设计、社媒推广、包装联动。

第三优先级：建立周度复盘和资产沉淀机制。
