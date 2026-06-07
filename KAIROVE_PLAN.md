# 影潮枢 / Kairove 项目总计划

## 0. 项目定位

**影潮枢 / Kairove** 是一个面向个人本地使用的 AI 短视频趋势挖掘、格式复现、生成、质检、发布与学习系统。

它不是单一的 MMD 工具，也不是简单的“输入一句 prompt 生成视频”。它的核心目标是：

1. 联网广泛搜索当前热门视频、热文案、热音乐、热剧情、热门 AI 视频风格；
2. 分析大量热视频背后的可复现格式；
3. 判断哪些格式正在上升、哪些已经疲劳、哪些适合蹭热度；
4. 将热视频格式语义等价迁移到其他角色、圈层、画风或世界观中；
5. 主动寻找、采集、生成、管理生产所需素材；
6. 调用多种 AI 工具生成图片、视频、音频、字幕、封面；
7. 用多层 Agent 和程序质检生成结果；
8. 根据质检结果多轮修正、重试、换路线；
9. 生成标题、简介、tag、封面、平台发布包；
10. 自动或半自动发布到 B站、抖音、小红书、YouTube 等平台；
11. 回收平台反馈、人工审查反馈、生成失败经验，让系统长期成长。

MMD / VRM / 3D 只是 Kairove 可以输出的视频类型之一，不是系统主线。普通 AI 视频格式复现是第一条主要生产线。

---

## 1. 核心原则

### 1.1 格式复现，不是随机换皮

Kairove 要做的是 **语义等价迁移**。

例如真人情侣嘴硬短剧，不应随机变成任意两个人，而应先识别原格式里的关系与情绪：

- A：质问者、清醒者、熟悉对方弱点；
- B：嘴硬者、心虚者、被戳穿者；
- 关系：亲密、熟悉、能互相吐槽；
- 情绪：暧昧、嘴硬、心虚、破防。

然后迁移到目标圈层里的等价关系：

- 游戏内 CP；
- 动漫 CP；
- 队友、宿敌、师徒、搭档；
- 玩家与角色；
- 指挥官与角色。

核心不是“换名字”，而是保留观众买账的关系、节奏、情绪和爽点。

### 1.2 默认全平台发布，只排除不适合的平台

Kairove 不以“哪个平台最适合”为默认问题，而是：

- 默认 B站、抖音、小红书、YouTube 等全部准备发布；
- 判断哪些平台不适合；
- 对不同平台调整标题、封面、tag、简介、发布时间；
- 风险过高的平台可跳过、改包装或请求人工确认。

### 1.3 可解释、可配置、可复盘

所有判断都必须能解释：

- 为什么选择这个格式；
- 为什么这个趋势分高；
- 为什么这条 production route 可行；
- 为什么某个候选视频失败；
- 为什么要重试；
- 为什么建议发布或不发布；
- 为什么建议调权重。

所有评分权重必须可配置，不写死。所有结果必须保存日志与报告。

### 1.4 学习，但不偷偷改核心规则

系统可以自动记录事实、观察趋势、总结经验、提出建议，但不能偷偷改变核心权重、发布权限、素材策略。

学习结果分为：

- `observation`：观察到的事实；
- `suggestion`：系统建议；
- `approved_rule`：用户确认后生效的规则。

### 1.5 权限不是等级制，而是能力矩阵

不是 Level 6 自动拥有 Level 1-5，而是每项能力独立开关。

例如用户可以允许：

- 联网搜索；
- 下载参考素材；
- 自动发布；

但禁止：

- 高成本生成；
- 声音训练；
- 直接使用个人画师素材。

权限状态：

- `allow`
- `ask`
- `deny`
- `allow_with_limits`

### 1.6 素材策略

当前用户策略：

- 官方素材默认可直接使用，包括游戏官方、动漫官方、官方 PV、官方展示图、官方音乐、官方音效等；
- 官方素材需要记录来源，但不强制人工审查；
- 个人画师、个人创作者、来源不明素材必须进入人工审查；
- 冒充官方或像官方 PV 的风险不作为阻止条件；
- Kairove 自己生成的素材可直接用于生产，但要记录 prompt、模型、参考来源。

---

## 2. 总体架构

Kairove 由以下主要模块组成：

1. **Kairove Regent**
2. **Trend & Format Mining Engine**
3. **Source Scout**
4. **Harvester**
5. **Video Understanding Engine**
6. **Format Miner**
7. **Trend Analyst**
8. **Scoring & Feedback Engine**
9. **Knowledge Base**
10. **Asset Resolver & Acquisition Planner**
11. **Format Reproduction Council**
12. **Semantic Format Transfer**
13. **Route Selector**
14. **Specialized Councils**
15. **Generation Manager**
16. **Quality Council**
17. **Revision & Retry Engine**
18. **Packaging Council**
19. **Publish Council**
20. **Platform Publisher Integrations**
21. **Human Review Console**
22. **Learning Memory System**
23. **Tool Capability Registry**
24. **Config & Permission System**
25. **Storage Layout**
26. **Security / Compliance / Risk Policy**

---

## 3. Kairove Regent

Kairove Regent 是系统主 Agent，负责代替用户在日常运行中调度各模块、做低风险判断、发现缺口、生成审查任务。

职责：

1. 启动自动巡航、关键词任务、指定链接任务；
2. 调度 Source Scout、Harvester、Format Miner 等模块；
3. 按权限能力矩阵判断某一步是否能自动执行；
4. 遇到不确定素材、成本、平台、角色风险时生成 review item；
5. 根据 Quality Council 报告判断重试、换路线、放弃或交给用户；
6. 记录所有关键决策到 `decision_log.json`；
7. 定期进行复盘，生成学习建议。

Regent 不是无限代理用户。所有高风险、高成本、用户偏好未确认的动作都必须根据权限矩阵停下来。

---

## 4. Trend & Format Mining Engine

这是 Kairove 的核心输入端。它不是简单热点总结器，而是热门视频格式挖掘系统。

它要识别：

- 很多视频都在拍同一段文案；
- 很多视频都在用同一首歌；
- 很多视频都在演同一段剧情；
- 某类恐怖视频突然流行；
- 某类抽象剪辑正在扩散；
- 某种 AI 画风或工具风格在流行；
- 某个格式适合换角色、换圈层、换画风重演。

输出不是单个热点，而是：

- `format_card`
- `format_genome`
- `trend_scorecard`
- `reproduction_opportunity`

---

## 5. Source Scout

Source Scout 负责发现候选素材，不负责深度理解。

输入方式：

- 自动巡航；
- 关键词；
- 指定平台；
- 指定视频链接；
- 指定角色或圈层；
- 指定热门音乐；
- 指定创作者；
- 指定视频类型。

平台 Scout：

- `BilibiliScout`
- `DouyinScout`
- `XiaohongshuScout`
- `YouTubeScout`
- `TikTokScout`
- `WeiboScout`
- `SearchEngineScout`
- `WikiScout`
- `ManualSeedScout`

输出候选：

```json
{
  "candidate_source_id": "cand_src_0001",
  "platform": "bilibili",
  "url": "...",
  "title": "...",
  "author": "...",
  "content_type": "video",
  "observed_metrics": {
    "views": 123000,
    "likes": 8800,
    "comments": 900
  },
  "discovery_reason": [
    "keyword_match",
    "rising_search_result",
    "similar_script_cluster"
  ],
  "collected_at": "..."
}
```

Source Scout 要寻找三类候选：

1. 已经爆了的；
2. 刚起势的；
3. 单个不大火但大量重复出现的格式。

---

## 6. Harvester

Harvester 负责采集、下载、截图、转写、保存来源和 manifest。

保存内容：

- 网页快照；
- 视频文件或可访问引用；
- 封面图；
- 关键截图；
- 字幕、描述、tag；
- 评论区样本；
- 音频信息；
- 作者信息；
- 发布时间；
- 平台指标；
- 来源链接；
- 采集方式；
- 用途标记。

素材用途：

- `analysis_only`
- `reference_only`
- `style_analysis`
- `direct_use`
- `generated`
- `user_provided`
- `blocked`
- `unknown`

下载失败也要记录：

- `download_failed`
- `requires_login`
- `requires_api`
- `manual_needed`
- `browser_capture_only`
- `metadata_only`

---

## 7. Video Understanding Engine

视频理解层把单个热视频变成结构化理解报告。

### 7.1 文本理解

- 标题；
- 简介；
- tag；
- 字幕 OCR；
- 语音 ASR；
- 评论高频词；
- 评论情绪；
- 置顶评论；
- 弹幕。

Agent：

- `OCRAgent`
- `ASRAgent`
- `CommentMinerAgent`
- `SentimentAgent`
- `KeywordExtractor`
- `TranscriptCleaner`

### 7.2 画面理解

- 主体是谁；
- 真人、动漫、AI、游戏画面、3D、MMD；
- 镜头数量；
- 镜头节奏；
- 主要动作；
- 字幕样式；
- 封面样式；
- 画面比例；
- 是否像 AI 生成；
- 是否有水印；
- 是否有模板痕迹。

Agent：

- `SceneSegmentAgent`
- `VisualStyleAgent`
- `SubjectAgent`
- `ShotRhythmAgent`
- `SubtitleStyleAgent`
- `CoverStyleAgent`
- `WatermarkAgent`
- `AIArtifactAgent`

### 7.3 音频理解

- 是否有人声；
- 是否是热门歌曲；
- 是否是同款音频；
- BPM；
- 节奏点；
- 爆点位置；
- 沉默点；
- 音效类型；
- 是否适合复现。

Agent：

- `MusicIdentifierAgent`
- `BeatMapAgent`
- `VoiceDetectorAgent`
- `SFXDetectorAgent`
- `AudioMoodAgent`
- `LyricExtractorAgent`

### 7.4 剧情与格式理解

- 开头钩子；
- 角色关系；
- 剧情节拍；
- 冲突点；
- 反转点；
- 笑点或恐怖点；
- 可替换槽位；
- 观众期待；
- 是否适合换角色演绎。

输出：

```json
{
  "source_id": "src_000132",
  "content_summary": "A short dialogue meme where one person denies buying gacha pulls while evidence appears.",
  "content_type_guess": ["dialogue_meme", "short_drama", "gacha_meme"],
  "visual": {
    "style": "real-person vertical short video",
    "shot_count": 5,
    "subtitle_style": "large white text with black stroke",
    "ai_generated_likelihood": 0.21
  },
  "audio": {
    "has_music": true,
    "music_role": "comedic tension"
  },
  "story": {
    "roles": [
      { "role": "A", "function": "questioner" },
      { "role": "B", "function": "denier" }
    ],
    "beats": ["question", "denial", "evidence", "panic", "punchline"]
  },
  "comments": {
    "sentiment": "positive",
    "common_reactions": ["太真实了", "又是我", "钱包没了"]
  },
  "format_clues": [
    "same denial structure appears in similar videos",
    "dialogue can be transferred to game/anime CP"
  ]
}
```

每个判断必须带置信度和证据。

---

## 8. Format Miner

Format Miner 是格式挖掘层，是系统最重要的成长模块之一。

它不是总结单个视频，而是从多个理解报告中聚类，找出可复现格式。

它要提取：

- 剧情骨架；
- 角色槽位；
- 情绪曲线；
- 镜头语法；
- 音频语法；
- 字幕语法；
- 可替换元素；
- 不可替换核心；
- 生成难度；
- 风险点；
- 生命周期。

输出 `format_card`：

```json
{
  "format_id": "fmt_000042",
  "name": "嘴硬不抽卡",
  "category": "dialogue_meme",
  "format_genome": {
    "relationship": "熟人互怼 / 亲密戳穿",
    "beats": ["否认", "证据", "嘴硬", "破防"],
    "visual_style": "fast subtitles + reaction closeups",
    "audio_style": "comedic tension"
  },
  "lifecycle": {
    "stage": "rising",
    "last_seen_at": "...",
    "fatigue_score": 2.1
  },
  "recommended_routes": ["script_council", "character_reenactment_council"]
}
```

Format Miner 必须成长：

1. 判断新视频像不像已有格式；
2. 像则更新已有格式的证据、变体、热度、疲劳度；
3. 不像则创建新 format；
4. 生产视频后回写成功和失败经验；
5. 下次遇到类似格式时减少错误。

辅助 Agent：

- `SimilarityAgent`
- `NoveltyAgent`
- `SlotExtractor`
- `BeatMapper`
- `VisualGrammarAgent`
- `AudioGrammarAgent`
- `MemeLifecycleAgent`
- `AdaptationAgent`
- `FeasibilityAgent`
- `FailureAnalyst`
- `LibrarianAgent`

---

## 9. Trend Analyst

Trend Analyst 负责趋势评分。

它要分清：

- 类似视频多且点赞高、评论积极：加分；
- 类似视频多但评论说烂梗、点赞下滑：扣分；
- 类似视频少但增长快：大机会；
- 类似视频多且二创多：格式生命力强；
- 类似视频多但完播低、吐槽多：疲劳。

评分分正向和惩罚：

正向：

- `heat_score`
- `velocity_score`
- `engagement_quality`
- `remixability`
- `format_strength`
- `production_feasibility`
- `audience_fit`
- `freshness`

惩罚：

- `fatigue_penalty`
- `risk_penalty`
- `complexity_penalty`
- `tool_gap_penalty`

初始权重建议：

```yaml
positive:
  heat_score: 0.22
  velocity_score: 0.22
  engagement_quality: 0.16
  remixability: 0.14
  format_strength: 0.12
  production_feasibility: 0.08
  freshness: 0.06

penalties:
  fatigue_penalty: -0.18
  risk_penalty: -0.20
  tool_gap_penalty: -0.10
  complexity_penalty: -0.08
```

权重必须可配置、可重算、可记录版本。

---

## 10. Scoring & Feedback Engine

评分系统必须输出 `scorecard`。

每个 scorecard 包含：

- 每个评分项；
- 当前权重；
- 加权贡献；
- 扣分项；
- Agent 理由；
- 最终分；
- 决策；
- 后续建议。

示例：

```json
{
  "score_profile": "trend_video_v1",
  "positive_scores": {
    "heat_score": { "score": 8.7, "weight": 0.22, "weighted": 1.914 },
    "velocity_score": { "score": 9.1, "weight": 0.22, "weighted": 2.002 }
  },
  "penalties": {
    "fatigue_penalty": { "score": 2.0, "weight": -0.18, "weighted": -0.36 }
  },
  "final_score": 7.29,
  "decision": "make_video"
}
```

发布后要对比：

- 生成前预测分；
- 生成后质检分；
- 人工审查分；
- 平台反馈分。

系统可以提出权重调整建议，但必须用户确认后生效。

---

## 11. Knowledge Base

Kairove 的长期知识库分为七类。

### 11.1 Research Knowledge

保存联网研究内容：

- 热榜；
- 视频链接；
- 标题；
- 评论；
- 字幕；
- 截图；
- 网页快照；
- 热歌信息；
- 同款视频集合；
- 平台指标。

### 11.2 Format Knowledge

保存：

- format_card；
- format_genome；
- 生命周期；
- 成功迁移；
- 失败迁移；
- 适合平台；
- 适合 production route。

### 11.3 Fandom / Character Knowledge

保存：

- 作品；
- 角色；
- 角色性格；
- 角色说话风格；
- 角色关系；
- 常见 CP；
- 粉丝认可度；
- 雷点；
- 世界观场景；
- 适合演的梗。

### 11.4 Local Asset Knowledge

保存：

- 用户训练的声音；
- 角色参考；
- 本地模型；
- 音乐；
- 音效；
- 字幕模板；
- 封面模板；
- 用户收集素材。

### 11.5 Tool Capability Knowledge

保存当前可用工具及能力：

- 文生图；
- 图生视频；
- 文生视频；
- 视频转视频；
- TTS；
- 声音训练；
- 剪辑；
- 上传平台。

### 11.6 Job Memory

保存每次任务：

- 输入；
- 参考；
- 生产配方；
- prompt；
- 候选；
- 质检；
- 人工反馈；
- 发布结果；
- 失败原因。

### 11.7 User Preference

保存用户偏好：

- 喜欢的视频方向；
- 不喜欢的 AI 味；
- 常用角色；
- 常用平台；
- 风险边界；
- 批准或否决过的风格。

所有知识都要有：

- 来源；
- 置信度；
- 是否用户确认；
- 更新时间。

---

## 12. Asset Resolver & Acquisition Planner

该模块负责主动找素材、查素材、生成替代、发现缺口。

顺序：

1. 查本地资产；
2. 查研究库；
3. 联网搜索；
4. 生成原创替代；
5. 尝试构建能力；
6. 做不到则生成 human_task。

素材决策示例：

```json
{
  "asset_need": "character_reference_for_target_cp",
  "resolution": "web_research_and_generated_reference",
  "selected_assets": [
    {
      "asset_id": "research_img_0012",
      "role": "visual_reference_only",
      "source": "official wiki",
      "usage": "reference for character description",
      "review_status": "pending_user_review"
    }
  ],
  "human_tasks": []
}
```

当前素材策略：

- 官方来源素材默认可直接使用；
- 个人画师和个人创作者素材需要人工审查；
- 来源不明素材需要人工审查；
- 网络素材都要保存 manifest。

---

## 13. Format Reproduction Council

格式复现委员会负责判断：

- 原视频应该模仿哪里；
- 哪些必须保留；
- 哪些可以替换；
- 哪些不要管；
- 怎么用现有工具复现。

它输出 `reproduction_plan.json`。

核心子 Agent：

- `CoreExtractor`
- `PreservationAgent`
- `ReplacementAgent`
- `BoundaryAgent`
- `AudienceExpectationAgent`
- `ToolMatchAgent`
- `FeasibilityAgent`
- `VariationAgent`
- `StrategyRanker`
- `ReproductionPlanner`

---

## 14. Semantic Format Transfer

语义等价迁移负责把原视频的角色关系、情绪关系、剧情功能迁移到目标圈层。

关键 Agent：

- `SemanticRoleExtractor`
- `RelationshipMapper`
- `FandomFitAgent`
- `WorldAdaptationAgent`
- `TonePreservationAgent`
- `CharacterBehaviorAgent`
- `CanonRiskAgent`

示例输出：

```json
{
  "semantic_transfer": {
    "source_relationship": "intimate teasing couple",
    "target_relationship": "popular anime/game CP with teasing dynamic",
    "preserved_emotion": ["嘴硬", "心虚", "被熟人戳穿", "暧昧吐槽"],
    "world_adaptation": {
      "source_scene": "couple home conversation",
      "target_scene": "game character dorm room near gacha interface",
      "equivalent_function": "private space where one character can expose the other's secret"
    },
    "evidence_object_mapping": {
      "source": "phone purchase record",
      "target": "gacha history / stamina purchase log"
    }
  }
}
```

---

## 15. Specialized Councils

不同视频类型由专门委员会处理。它们不是互斥的，一个视频可以有一个 primary council 和多个 supporting councils。

### 15.1 Script Council

处理：

- 抽象短剧；
- 对白梗；
- 旁白故事；
- 恐怖小故事；
- 剧情反转。

### 15.2 Music Sync Council

处理：

- 热歌；
- 卡点；
- 舞蹈；
- 歌词梗；
- 同款 BGM。

### 15.3 Character Reenactment Council

处理：

- 二游角色演绎；
- 动漫角色演绎；
- CP 迁移；
- 角色反应视频。

### 15.4 Visual Style Council

处理：

- AI 视觉风格；
- 二游建模感；
- 动漫画风；
- 恐怖风格；
- 伪纪录感；
- 字幕与封面视觉规律。

### 15.5 Horror Atmosphere Council

处理：

- 恐怖短剧；
- 怪谈；
- 梦核、怪核；
- 灵异监控风；
- 氛围恐怖。

### 15.6 Meme Edit Council

处理：

- 抽象剪辑；
- 字幕梗；
- 音效堆叠；
- 鬼畜感；
- 评论区梗。

### 15.7 Dance / Motion Council

处理：

- 舞蹈；
- 动作模仿；
- MMD；
- 3D 动作；
- 角色跳同款。

### 15.8 Longform Council

处理：

- 5 分钟以上；
- 10 分钟以上；
- 几十分钟；
- 几小时；
- 解说；
- 合集；
- 系列。

### 15.9 AI Tool Imitation Council

处理：

- 判断原视频可能用了什么 AI；
- 查 Kairove 是否有同类工具；
- 输出 tool_gap 或 fallback。

### 15.10 MMD / 3D Council

处理：

- MMD；
- VRM；
- PMX / VMD；
- Blender；
- 3D 角色动作。

该模块后续单独细拆。

### 15.11 Hybrid Council

处理多路线组合和冲突。

---

## 16. Generation Manager

生成调度层负责将生产计划变成实际图、视频、声音、字幕、封面。

职责：

- 选择 production route；
- 选择工具；
- 生成 prompt；
- 生成 negative prompt；
- 调用 AI 工具；
- 批量生成候选；
- 记录 generation_step；
- 失败后给 fallback。

支持 routes：

- `text_to_video`
- `image_to_video`
- `multi_image_to_video`
- `video_to_video`
- `reference_video_reenactment`
- `character_reenactment`
- `music_sync_video`
- `short_drama_multi_scene`
- `horror_atmosphere_video`
- `meme_edit_video`
- `mmd_3d_assisted_video`
- `longform_video`
- `hybrid_pipeline`

每个生成动作记录：

```json
{
  "step_id": "gen_step_0004",
  "job_id": "job_0012",
  "step_type": "image_to_video",
  "tool": "kling",
  "input_assets": ["image_0007"],
  "prompt_path": "...",
  "output_assets": ["video_candidate_0004"],
  "status": "success",
  "created_at": "..."
}
```

---

## 17. Quality Council

质检分层：

1. `Technical QA`：程序优先，Agent 辅助；
2. `Cheap Visual QA`：便宜视觉模型筛明显问题；
3. `Semantic QA`：检查是否符合计划和语义迁移；
4. `Specialist QA`：按视频类型检查；
5. `Strong Judge`：高级模型终审；
6. `Kairove Regent`：综合运营判断。

Technical QA 不是不用 Agent，而是程序优先：

- 分辨率；
- 帧率；
- 时长；
- 音轨；
- 黑屏；
- 坏帧；
- 字幕越界。

Agent 辅助：

- 暗场是否被误判黑屏；
- 字幕是否压脸；
- 封面是否技术合规但观感混乱；
- 音画是否观感不同步。

失败标签：

- `format_core_lost`
- `semantic_transfer_failed`
- `ooc_character`
- `weak_hook`
- `bad_pacing`
- `ai_artifact`
- `face_collapse`
- `hand_failure`
- `audio_mismatch`
- `subtitle_overflow`
- `too_generic`
- `tool_not_suitable`
- `asset_missing`
- `platform_risk`

---

## 18. Revision & Retry Engine

多轮修正系统负责把质检报告变成下一轮可执行修改。

流程：

1. `FailureClassifier`
2. `FixStrategySelector`
3. `PreservationGuard`
4. `PromptRevisionAgent`
5. `NegativePromptRevisionAgent`
6. `AssetRevisionAgent`
7. `RouteRevisionAgent`
8. `BudgetGuard`
9. `RegressionRiskAgent`
10. `RetryPlanner`
11. `MemoryWriter`

失败归因：

- technical failure；
- prompt failure；
- asset failure；
- model failure；
- route failure；
- script failure；
- semantic transfer failure；
- format mismatch；
- platform risk；
- cost failure；
- unknown failure。

重试必须保护成功部分：

```json
{
  "preserve": [
    "same character design",
    "same subtitle pacing",
    "same final camera angle"
  ],
  "revise": [
    "replace hand gesture with face reaction",
    "increase teasing relationship cue"
  ]
}
```

---

## 19. Packaging Council

包装委员会负责：

- 标题；
- 简介；
- tag；
- 封面；
- 首帧；
- 合集或系列名；
- 置顶评论；
- 平台 payload。

子 Agent：

- `TitleAgent`
- `TitleCriticAgent`
- `DescriptionAgent`
- `TagAgent`
- `CoverConceptAgent`
- `CoverGeneratorAgent`
- `CoverCriticAgent`
- `FirstFrameAgent`
- `PinnedCommentAgent`
- `SeriesAgent`

包装必须与前面内容连携：

- format_card；
- trend_scorecard；
- reproduction_plan；
- script / visual / audio plan；
- quality_report；
- platform profile；
- publish feedback memory。

---

## 20. Publish Council

发布委员会负责：

- 发布包整理；
- 平台排除与适配；
- 发布前风险复查；
- 上传、排程、草稿；
- 发布后数据回收。

默认全平台发布，只排除不适合项。

输出：

```json
{
  "publish_targets": {
    "bilibili": {
      "decision": "publish",
      "adaptations": ["longer title", "add description"]
    },
    "douyin": {
      "decision": "publish",
      "adaptations": ["shorter title", "hot topic tags"]
    },
    "xiaohongshu": {
      "decision": "needs_packaging_change",
      "adaptations": ["make cover more note-like"]
    },
    "youtube_shorts": {
      "decision": "skip",
      "reason": "no English subtitle/package generated"
    }
  }
}
```

---

## 21. Platform Publisher Integrations

执行平台发布。

支持方式：

1. 官方 API；
2. 浏览器自动化；
3. 手动发布包。

平台目录：

```text
publishers/
  bilibili/
  douyin/
  xiaohongshu/
  youtube/
  manual/
```

统一接口：

- `check_capability()`
- `check_auth()`
- `prepare_payload()`
- `upload_draft()`
- `publish()`
- `schedule_publish()`
- `fetch_publish_status()`
- `fetch_metrics()`
- `fetch_comments()`

做平台模块时，需要什么 API、权限、OAuth、账号配置，系统会列给用户。

---

## 22. Audio & Voice System

底层音频能力层，服务 Music Sync Council、Script Council、Generation Manager、Quality Council。

能力：

- 音频发现；
- 音频识别；
- beat 分析；
- voice profile 管理；
- 声音训练流水线；
- TTS 生成；
- 音效与 BGM；
- 混音；
- 音频质检。

声音策略：

- 用户训练或提供的声音可用；
- 原创生成声音可用；
- 官方角色声音克隆默认不自动做；
- 可提取声音风格描述，生成原创相似风格声音；
- 做不到则生成 human_task。

---

## 23. Visual Asset & Style System

底层视觉资产与风格能力。

能力：

- 视觉参考发现；
- 角色视觉理解；
- 风格提取；
- 字幕风格系统；
- 封面风格系统；
- 场景与背景资产；
- 生成视觉资产；
- 视觉 QA；
- 来源和用途标记。

官方角色图、官方 wiki 图可按当前策略 direct use，但仍记录来源。

个人画师和来源不明图需要审查。

---

## 24. Tool Capability Registry

工具能力注册表记录：

- 有哪些工具；
- 每个工具能做什么；
- 支持输入输出；
- 优势和弱点；
- 状态；
- API 或本地安装要求；
- 成本；
- 速度；
- route 兼容性；
- 历史表现；
- 常见失败；
- 成功 workaround。

工具状态：

- `available`
- `not_configured`
- `requires_api_key`
- `requires_account`
- `requires_permission`
- `requires_local_install`
- `temporarily_failed`
- `deprecated`
- `blocked`
- `unknown`

---

## 25. Config & Permission System

配置包括：

- system config；
- agent config；
- tool config；
- permission config；
- score profiles；
- platform profiles；
- user preferences；
- route profiles。

权限是能力矩阵，不是等级制。

示例：

```yaml
permissions:
  research.web_search: allow
  research.download_reference_assets: allow
  generation.generate_high_cost_candidates: ask
  asset.train_voice: ask
  publish.auto_publish: allow
  publish.upload_draft: allow
  asset.use_web_assets_directly: ask
```

每一步行动都检查：

- 所需 capability；
- 当前是否 allow / ask / deny；
- 是否超预算；
- 是否触发风险；
- 是否需要人工审查。

---

## 26. Human Review Console

人工审查控制台是用户与 Kairove Regent 的交接界面。

功能：

- review queue；
- decision card；
- 候选视频对比；
- 素材出处查看；
- agent 分歧查看；
- 权重编辑；
- tool setup queue；
- 发布确认；
- API 缺口清单。

早期可用：

```text
review_queue/*.json
reports/review_dashboard.html
scripts/review.py
```

后期做本地 Web UI。

---

## 27. Learning Memory System

学习记忆系统记录：

- format learning；
- trend prediction learning；
- generation learning；
- quality learning；
- user preference learning；
- platform learning；
- packaging learning；
- asset learning。

每次视频生命周期都保存：

- 预测分；
- 生成路线；
- prompt；
- 成本；
- 重试轮次；
- 质量分；
- 用户人工反馈；
- 平台数据；
- 评论情绪；
- 复盘结论。

学习输出分为：

- observation；
- suggestion；
- approved_rule。

---

## 28. Storage Layout

顶层目录：

```text
Kairove/
  config/
  kairove/
  scripts/
  data/
  research_assets/
  local_assets/
  generated_assets/
  knowledge_base/
  outputs/
  review_queue/
  reports/
  logs/
```

三类素材目录：

```text
research_assets/
  raw_pages/
  raw_videos/
  raw_audio_refs/
  screenshots/
  covers/
  comments/
  transcripts/
  manifests/

local_assets/
  voices/
  characters/
  models/
  music/
  sfx/
  style_refs/
  user_collected/
  licenses/
  manifests/

generated_assets/
  jobs/
  images/
  videos/
  audio/
  covers/
  subtitles/
  prompts/
  manifests/
```

Job 目录：

```text
generated_assets/jobs/job_000001/
  job_config.json
  decision_log.json
  source_refs.json
  format_card.json
  trend_scorecard.json
  reproduction_plan.json
  production_recipe.json

  councils/
  assets/
  prompts/
  candidates/
  final/
  publish_package/
  feedback/
```

数据库存索引和状态，大文件存在文件夹。所有素材都要有 manifest。

---

## 29. Security / Compliance / Risk Policy

风险系统的职责是识别风险、标记风险、给替代方案、必要时请求人工确认。

当前用户策略：

- 冒充官方或像官方 PV 的风险不用管；
- 官方素材默认可 direct use；
- 个人画师、个人创作者、来源不明素材需要审查；
- 音乐、音效如果是官方素材也可直接用；
- 所有素材仍要记录来源和用途。

风险等级：

- `none`
- `low`
- `medium`
- `high`
- `blocked`
- `unknown`

动作：

- `allow`
- `allow_with_manifest`
- `allow_with_warning`
- `ask_user`
- `rewrite_or_replace`
- `use_as_reference_only`
- `block`

---

## 30. First Production Line

第一条生产线：

```text
route_ordinary_ai_format_video
普通 AI 格式复现视频线
```

覆盖：

- 热视频文案复现；
- 角色换皮演绎；
- 抽象短视频；
- 恐怖氛围短视频；
- 音乐 / 音效梗；
- AI 视觉风格复现；
- 多镜头 AI 拼接短视频。

完整流程：

1. Run Intake；
2. Source Scout；
3. Harvester；
4. Video Understanding；
5. Format Miner；
6. Trend Analyst；
7. Regent Gate；
8. Format Reproduction Council；
9. Semantic Format Transfer；
10. Route Selector；
11. Specialized Councils；
12. Asset Resolver；
13. Generation Manager；
14. Quality Council；
15. Revision & Retry；
16. Final Judge；
17. Packaging Council；
18. Publish Council；
19. Publisher Integrations；
20. Feedback Collector；
21. Learning Memory。

验收标准：

1. 输入一个热视频链接或关键词；
2. Kairove 能采集并理解素材；
3. 能提取至少一个 format_card；
4. 能给出 trend_scorecard 和权重解释；
5. 能生成 reproduction_plan；
6. 能找/生成所需素材，并标明来源；
7. 能生成多个候选视频；
8. 能多层质检并给失败标签；
9. 能至少一轮自动修正；
10. 能输出 final_video 和 publish_package；
11. 能保存完整日志和学习记录。

---

## 31. Legacy Capability Sequence (Not Current Phase Plan)

Important correction:

```text
This section is an old capability sequence draft.
It is not the current implementation roadmap.
Phase 0 is confirmed as P0-B Lowest Complete Production Chain. Phase 1 scope is confirmed but implementation is not started.
Do not treat Legacy Step 1-19 as accepted phases.
```

### Legacy Step 0：项目地基与记忆落盘（early draft of current Phase 0）

目标：

- 创建 Kairove 项目结构；
- 建立配置系统；
- 建立日志；
- 建立数据库；
- 建立 run / job / review 基础对象；
- 把当前架构共识写入项目文档。

验收：

- 能创建 run；
- 能创建 job；
- 能写 decision_log；
- 能写 review_item；
- 能读取权限配置。

### Legacy Step 1：权限矩阵与主 Agent 骨架（not an accepted phase）

目标：

- 实现 Permission Capability Matrix；
- 实现 Kairove Regent skeleton；
- 实现 decision logging；
- 实现 review queue；
- 实现 tool setup queue。

验收：

- 输入一个操作请求；
- 系统能判断 allow / ask / deny；
- 能生成 review item；
- 能记录原因。

### Legacy Step 2：Source Scout 基础版（not an accepted phase）

目标：

- 实现 ManualSeedScout；
- 实现 SearchEngineScout；
- 实现 BilibiliScout 基础；
- 实现 YouTubeScout 基础；
- 记录平台能力状态。

验收：

- 输入关键词；
- 输出 candidate_sources.json。

### Legacy Step 3：Harvester 与素材 manifest（not an accepted phase）

目标：

- 建立 research_assets；
- 建立 source manifest；
- 建立 asset manifest；
- 保存网页、截图、评论、元数据；
- 标记官方、个人、未知来源。

验收：

- 采集一个视频链接；
- 生成 source manifest；
- 标记素材用途。

### Legacy Step 4：Video Understanding 基础版（not an accepted phase）

目标：

- title / description / tag parser；
- OCR 接口预留；
- ASR 接口预留；
- comment miner 基础；
- visual summary 接口；
- audio summary 接口；
- understanding_report.json。

验收：

- 输入 source；
- 输出 understanding_report。

### Legacy Step 5：Format Miner v1（not an accepted phase）

目标：

- format clustering；
- format genome schema；
- format_card；
- similarity detection；
- new / variant 判断；
- format memory 写入。

验收：

- 输入一组相似视频；
- 输出 format_card。

### Legacy Step 6：Trend Analyst + Scoring Engine（not an accepted phase）

目标：

- score_profiles；
- trend_scorecard；
- positive / penalty scoring；
- weight display；
- decision explanation。

验收：

- 每个 format 都有分数；
- 能看到每项权重和贡献；
- 能修改权重后重算。

### Legacy Step 7：Knowledge Base 基础版（not an accepted phase）

目标：

- format knowledge；
- tool registry；
- user preference；
- local asset registry；
- fandom / character knowledge skeleton；
- memory entries。

验收：

- Format Miner 能读取历史 format；
- Trend Analyst 能读取历史表现；
- ToolSelector 能读取工具能力。

### Legacy Step 8：Format Reproduction + Semantic Transfer（not an accepted phase）

目标：

- reproduction_plan；
- semantic role extraction；
- relationship mapping skeleton；
- 官方素材策略；
- 角色 / CP 风险标记；
- production_recipe。

验收：

- 输入真人热视频格式；
- 输出二游 / 动漫 / 角色版本复现计划。

### Legacy Step 9：Specialized Councils v1（not an accepted phase）

目标：

- Script Council；
- Visual Style Council；
- Character Reenactment Council；
- Meme Edit Council；
- Horror Atmosphere Council 基础；
- Music Sync Council 基础。

验收：

- 根据 reproduction_plan 输出 production plan；
- 支持多 council 协作。

### Legacy Step 10：Asset Resolver & Acquisition v1（not an accepted phase）

目标：

- local asset lookup；
- research asset lookup；
- web visual / audio reference lookup；
- official direct-use policy；
- personal creator review policy；
- human_task generation。

验收：

- 给定 production plan；
- 输出 resolved_assets.json；
- 缺素材时生成 review item。

### Legacy Step 11：Tool Capability Registry + Generation Manager v1（not an accepted phase）

目标：

- tool registry；
- tool status；
- route compatibility；
- generation_step；
- prompt builder；
- candidate registrar；
- fallback planner。

验收：

- 输入 production_recipe；
- 至少生成图片 / 视频 / 音频候选之一；
- 记录工具、参数、prompt、输出和失败原因。

### Legacy Step 12：Quality Council v1（not an accepted phase）

目标：

- Technical QA；
- Cheap Visual QA；
- Semantic QA；
- Specialist QA hooks；
- scorecard；
- failure tags。

验收：

- 输入 candidate；
- 输出完整 quality_report。

### Legacy Step 13：Revision & Retry v1（not an accepted phase）

目标：

- failure classifier；
- retry planner；
- prompt revision；
- preservation guard；
- route mutation；
- memory writeback。

验收：

- 候选失败后能生成 retry_plan；
- 至少完成一轮修正重试。

### Legacy Step 14：Packaging Council v1（not an accepted phase）

目标：

- title agent；
- description agent；
- tag agent；
- cover concept / generation / critic；
- platform payloads。

验收：

- 输出各平台 payload；
- 默认全平台，标记不适合或需调整的平台。

### Legacy Step 15：Publish Council + Manual Package（not an accepted phase）

目标：

- publish_package；
- manual publisher；
- platform payload schema；
- publish readiness report；
- tool setup queue for APIs。

验收：

- 输出 final_video、cover、title、description、tags、per-platform payload。

### Legacy Step 16：Platform API / Browser Publisher（not an accepted phase）

目标：

- 逐个平台接上传与反馈。

建议顺序：

1. B站；
2. 抖音；
3. YouTube；
4. 小红书；
5. 其他。

每个平台实现：

- auth；
- upload draft；
- publish / schedule；
- fetch metrics；
- fetch comments。

### Legacy Step 17：Feedback Learning（not an accepted phase）

目标：

- user feedback；
- platform metrics；
- format learning update；
- tool performance update；
- score weight suggestions；
- packaging learning。

验收：

- 发布后生成 learning_update；
- 提出可解释权重或策略建议。

### Legacy Step 18：Local Web Console（not an accepted phase）

目标：

做本地控制台。

页面：

- Dashboard；
- Trend Explorer；
- Format Library；
- Review Queue；
- Job Detail；
- Candidate Compare；
- Asset Provenance；
- Tool Setup；
- Permission Matrix；
- Publish Center；
- Learning Reports。

### Legacy Step 19：3D / MMD 专项路线（not an accepted phase）

目标：

单独攻克：

- PMX / VMD；
- VRM；
- Blender；
- MMD；
- 动作、镜头、渲染；
- AI + 3D 混合路线。

---

## Cross-Phase Policy Pointer - 2026-06-06

The latest cross-phase policy authority is:

```text
IMPLEMENTATION_ROADMAP.md Cross-Phase Final Policy Sync - 2026-06-06
```

If this legacy plan conflicts with that accepted policy, the accepted cross-phase policy wins. This pointer is planning authority only and does not authorize implementation.

---

## 32. 下一步建议

在真正写代码前，建议先执行：

1. 确认项目根目录；
2. 创建上述目录骨架；
3. 创建 `config/permissions.yaml`；
4. 创建 `config/score_profiles/trend_video_v1.yaml`；
5. 创建数据库基础 schema；
6. 创建 `scripts/create_run.py`；
7. 创建 `scripts/create_job.py`；
8. 实现 review queue 和 decision log；
9. 只做当前确认的 Phase 0，不跳到生成、MMD、平台发布。

Phase 0 完成后，Kairove 应该能保存系统记忆、创建任务、记录决策，并为后续 Source Scout 做准备。
