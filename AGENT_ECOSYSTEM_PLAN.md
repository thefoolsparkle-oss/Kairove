# Kairove Agent Ecosystem Plan

## 0. Purpose

This document defines how Kairove's agent ecosystem should work.

Kairove should not be a pile of agent names. It needs:

- clear orchestration;
- ordered collaboration;
- non-mutually-exclusive councils;
- explainable decisions;
- model tier escalation;
- review gates;
- stable input and output contracts.

Agents should behave like a production studio:

```text
scout -> understand -> mine format -> score -> plan reproduction -> produce -> inspect -> revise -> package -> publish -> learn
```

---

## 1. Agent Design Principles

### 1.1 Councils Are Not Mutually Exclusive

Most videos combine multiple format cores:

- hot script + character reenactment;
- hot song + dance + subtitles;
- horror atmosphere + AI visual style;
- meme edit + official character material;
- longform explanation + short clips.

Therefore, a job can have:

```text
primary_council: one
supporting_councils: many
```

Example:

```json
{
  "primary_council": "music_sync_council",
  "supporting_councils": [
    "character_reenactment_council",
    "meme_edit_council",
    "visual_style_council"
  ]
}
```

### 1.2 Agents Should Work in Ordered Passes

Agents should not randomly debate forever.

Most councils should use ordered passes:

```text
interpret -> generate options -> evaluate -> refine -> risk check -> final assemble
```

Some tasks can run in parallel, but every council should have a clear final assembler.

### 1.3 Agents Do Not Hide Disagreement

If agents disagree, Kairove must record:

- topic;
- who disagreed;
- evidence;
- confidence;
- whether escalation happened;
- final resolution.

Disagreement should not be smoothed into a fake consensus.

### 1.4 Cheap First, Strong Later

Use cheaper agents for:

- broad search summaries;
- initial filtering;
- obvious failures;
- low-risk formatting;
- candidate expansion.

Use stronger agents for:

- semantic transfer;
- final publish judgment;
- hard disagreements;
- repeated retry failures;
- high-risk decisions;
- user-facing recommendations.

### 1.5 Agents Produce Structured Outputs

Every agent should output structured data:

```json
{
  "agent": "agent_name",
  "task": "...",
  "recommendation": "...",
  "confidence": 0.0,
  "reasons": [],
  "concerns": [],
  "evidence": [],
  "next_actions": [],
  "needs_user_review": false
}
```

Free-form text is allowed for explanation, but structured fields are required.

---

## 2. Model Tiers

Kairove should support model tiers rather than fixed model names.

### 2.1 Tier Types

```text
cheap:
  Used for initial screening, extraction, simple summaries, obvious QA.

medium:
  Used for semantic analysis, format extraction, council planning, normal critique.

strong:
  Used for final judgment, high-risk review, hard disagreements, repeated failures.

specialized:
  Used for domain tasks such as OCR, ASR, music ID, visual QA, embeddings.
```

### 2.2 Escalation Triggers

Escalate to stronger models when:

1. agents disagree strongly;
2. confidence is low but decision impact is high;
3. high-cost generation is about to happen;
4. publishing is about to happen;
5. retry failed more than configured rounds;
6. semantic transfer is uncertain;
7. character / CP / fandom risk is medium or higher;
8. user preference is unclear;
9. platform risk is unclear;
10. a result is near threshold and worth saving.

### 2.3 Escalation Output

Escalation should write:

```json
{
  "escalation_id": "esc_000001",
  "reason": "agent_disagreement",
  "from_tier": "medium",
  "to_tier": "strong",
  "question": "...",
  "inputs": [],
  "result": {},
  "decision_log_id": "decision_000001"
}
```

---

## 3. Kairove Regent

### 3.1 Role

Kairove Regent is the main orchestrator.

It does not replace every specialist. It decides:

- what module to run;
- when to continue;
- when to pause;
- when to ask the user;
- when to spend money;
- when to abandon;
- when to publish;
- when to write memory.

### 3.2 Regent Responsibilities

1. Start and resume runs.
2. Enforce permission capability matrix.
3. Select candidate formats for planning.
4. Decide primary and supporting councils.
5. Create jobs.
6. Generate review items.
7. Resolve agent disagreements or escalate them.
8. Approve low-risk automated steps.
9. Pause for high-risk or unknown steps.
10. Write decision logs.
11. Trigger learning updates.

### 3.3 Regent Must Not

Regent must not:

- silently change score weights;
- silently change permissions;
- silently use personal creator assets in final output;
- silently train sensitive voices;
- silently exceed cost limits;
- silently publish if publish permission is not enabled;
- delete local assets automatically.

### 3.4 Regent Output

```json
{
  "stage": "trend_selection",
  "decision": "create_job",
  "selected_format_id": "fmt_000001",
  "confidence": 0.84,
  "reason": "...",
  "permission_checks": [],
  "risk_checks": [],
  "next_stage": "format_reproduction_council",
  "review_items_created": []
}
```

---

## 4. Global Pipeline Agents

These agents operate across the whole system.

### 4.1 PermissionAgent

Checks whether an action is allowed, denied, or requires user review.

Inputs:

- action type;
- required capabilities;
- cost estimate;
- risk report;
- current permission config.

Output:

```json
{
  "action": "generate_high_cost_candidates",
  "permission_result": "allow | ask | deny | allow_with_limits",
  "required_capabilities": [],
  "triggered_limits": [],
  "review_item_needed": false
}
```

### 4.2 RiskAgent

Evaluates risk across assets, platform, content, character, voice, and cost.

Current user policy:

- official assets may be direct use;
- personal creator assets require review;
- unknown assets require review;
- official-like / PV-like misleading risk is not blocking.

### 4.3 DecisionLoggerAgent

Writes decision logs for gates and important actions.

### 4.4 ReviewItemAgent

Turns uncertain decisions into short, actionable review cards.

### 4.5 MemoryWriterAgent

Writes observations, suggestions, and approved rules after major outcomes.

---

## 5. Source Scout Agent Group

### 5.1 Purpose

Find candidate sources from platforms and the web.

### 5.2 Agents

- `BilibiliScout`
- `DouyinScout`
- `XiaohongshuScout`
- `YouTubeScout`
- `TikTokScout`
- `WeiboScout`
- `SearchEngineScout`
- `WikiScout`
- `ManualSeedScout`
- `CreatorProfileScout`
- `MusicTrendScout`

### 5.3 Ordered Flow

```text
1. QueryPlanner
2. Platform Scouts
3. CandidateNormalizer
4. CandidateDeduplicator
5. InitialRelevanceRanker
6. ScoutReporter
```

### 5.4 Output

```json
{
  "candidate_sources": [],
  "platform_capability_notes": [],
  "query_used": [],
  "recommend_harvest": []
}
```

---

## 6. Harvester Agent Group

### 6.1 Purpose

Save evidence and create source manifests.

### 6.2 Agents

- `MetadataHarvester`
- `PageSnapshotHarvester`
- `VideoHarvester`
- `ScreenshotHarvester`
- `CommentHarvester`
- `TranscriptHarvester`
- `AudioReferenceHarvester`
- `ManifestWriter`
- `HarvestFailureReporter`

### 6.3 Ordered Flow

```text
1. CapabilityCheck
2. HarvestPlan
3. FetchMetadata
4. FetchFilesOrSnapshots
5. SaveManifest
6. UsagePolicyTagging
7. FailureReport if needed
```

### 6.4 Output

```json
{
  "source_id": "src_000001",
  "harvest_status": "complete | partial | metadata_only | failed",
  "manifest_path": "...",
  "assets_created": [],
  "failures": []
}
```

---

## 7. Video Understanding Agent Group

### 7.1 Purpose

Convert raw sources into structured understanding reports.

### 7.2 Text Agents

- `TitleDescriptionParser`
- `OCRAgent`
- `ASRAgent`
- `TranscriptCleaner`
- `CommentMinerAgent`
- `SentimentAgent`
- `KeywordExtractor`

### 7.3 Visual Agents

- `SceneSegmentAgent`
- `VisualStyleAgent`
- `SubjectAgent`
- `ShotRhythmAgent`
- `SubtitleStyleAgent`
- `CoverStyleAgent`
- `WatermarkAgent`
- `AIArtifactAgent`

### 7.4 Audio Agents

- `MusicIdentifierAgent`
- `BeatMapAgent`
- `VoiceDetectorAgent`
- `SFXDetectorAgent`
- `AudioMoodAgent`
- `LyricExtractorAgent`

### 7.5 Story and Format Clue Agents

- `HookExtractor`
- `BeatStructureAgent`
- `RelationshipExtractor`
- `ConflictExtractor`
- `PunchlineExtractor`
- `FormatClueAgent`

### 7.6 Ordered Flow

```text
1. Basic metadata parsing
2. Text/audio/visual understanding in parallel
3. Story and relationship extraction
4. Format clue extraction
5. Confidence and evidence annotation
6. UnderstandingReportAssembler
```

---

## 8. Format Miner Agent Group

### 8.1 Purpose

Extract reusable formats from many sources.

### 8.2 Agents

- `SimilarityAgent`
- `NoveltyAgent`
- `ClusterAgent`
- `SlotExtractor`
- `BeatMapper`
- `VisualGrammarAgent`
- `AudioGrammarAgent`
- `MemeLifecycleAgent`
- `AdaptationAgent`
- `FeasibilityAgent`
- `FailureAnalyst`
- `LibrarianAgent`

### 8.3 Ordered Flow

```text
1. Load understanding reports
2. Compare with known formats
3. Cluster similar sources
4. Decide new format vs variant
5. Extract format genome
6. Estimate lifecycle
7. Write or update format card
8. Record format observations
```

### 8.4 Output

```json
{
  "format_id": "fmt_000001",
  "is_new_format": true,
  "format_card_path": "...",
  "format_genome_path": "...",
  "observations": [],
  "confidence": 0.82
}
```

---

## 9. Trend Analyst Agent Group

### 9.1 Purpose

Score whether a format is worth producing.

### 9.2 Agents

- `HeatScoreAgent`
- `VelocityScoreAgent`
- `EngagementQualityAgent`
- `CommentDirectionAgent`
- `FatigueDetector`
- `RemixabilityAgent`
- `FormatStrengthAgent`
- `ProductionFeasibilityAgent`
- `ToolGapAgent`
- `RiskPenaltyAgent`
- `ScorecardAssembler`

### 9.3 Ordered Flow

```text
1. Gather metrics and observations
2. Score positive factors
3. Score penalties
4. Apply score profile weights
5. Produce scorecard
6. Recommend make / observe / reject / ask user
```

### 9.4 Output

```json
{
  "trend_scorecard_id": "trend_score_000001",
  "final_score": 7.29,
  "decision": "make_video",
  "reason": "...",
  "weight_profile": "trend_video_v1"
}
```

---

## 10. Format Reproduction Council

### 10.1 Purpose

Decide how to reproduce a hot format.

### 10.2 Agents

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

### 10.3 Ordered Flow

```text
1. Extract source format core
2. Identify must-preserve elements
3. Identify replaceable elements
4. Apply user asset policy and boundaries
5. Generate reproduction strategies
6. Rank strategies
7. Assemble reproduction plan
```

---

## 11. Semantic Format Transfer Council

### 11.1 Purpose

Perform semantic equivalent transfer.

Example:

```text
real couple denial dialogue
  -> anime/game CP with similar teasing dynamic
```

### 11.2 Agents

- `SemanticRoleExtractor`
- `RelationshipMapper`
- `FandomFitAgent`
- `WorldAdaptationAgent`
- `TonePreservationAgent`
- `CharacterBehaviorAgent`
- `CanonRiskAgent`

### 11.3 Ordered Flow

```text
1. Extract source roles and relationship functions
2. Search target world and character knowledge
3. Generate relationship mapping options
4. Check fandom fit and OOC risk
5. Map scenes, props, evidence objects
6. Preserve emotional tone
7. Assemble semantic transfer plan
```

### 11.4 Output

```json
{
  "source_relationship": "...",
  "target_relationship": "...",
  "mapping_confidence": 0.76,
  "ooc_risk": "medium",
  "needs_user_review": true,
  "world_adaptation": {}
}
```

---

## 12. Route Selector and Hybrid Council

### 12.1 Purpose

Choose primary and supporting production routes.

### 12.2 Agents

- `RouteClassifier`
- `PrimaryRouteSelector`
- `SupportingRouteSelector`
- `RouteConflictDetector`
- `HybridPlanner`
- `RouteFeasibilityAgent`

### 12.3 Route Candidates

- `script_council`
- `music_sync_council`
- `visual_style_council`
- `character_reenactment_council`
- `horror_atmosphere_council`
- `meme_edit_council`
- `dance_motion_council`
- `longform_council`
- `ai_tool_imitation_council`
- `mmd_3d_council`
- `hybrid_council`

### 12.4 Output

```json
{
  "primary_route": "character_reenactment_council",
  "supporting_routes": ["script_council", "meme_edit_council"],
  "route_conflicts": [],
  "reason": "format depends on character relationship and dialogue punchline"
}
```

---

## 13. Specialized Councils

### 13.1 Script Council

Used when script, dialogue, narration, or story is central.

Ordered passes:

```text
1. BriefInterpreter
2. AngleGenerator
3. AngleEvaluator
4. StructureBuilder
5. HookWriter
6. DialogueOrNarrationWriter
7. CharacterVoicePass
8. MemePlatformLanguagePass
9. PacingPass
10. AntiAITextPass
11. RiskPass
12. ProductionFeasibilityPass
13. ScriptCriticPass
14. RewritePass
15. FinalAssembler
```

Rules are style guidelines, not universal hard laws. Different video types have different writing modes.

### 13.2 Music Sync Council

Used when music, lyrics, beat, dance, or audio meme is central.

Agents:

- `AudioCoreDetector`
- `BeatUsePlanner`
- `LyricHookAgent`
- `VisualBeatMapper`
- `DanceNeedAgent`
- `MusicUsageRiskAgent`
- `SyncPlanAssembler`

### 13.3 Character Reenactment Council

Used when character or CP replacement is central.

Agents:

- `CastingAgent`
- `CharacterVoiceAgent`
- `CharacterBehaviorAgent`
- `RelationshipFitAgent`
- `OOCGuard`
- `SceneEquivalenceAgent`
- `CharacterPlanAssembler`

### 13.4 Visual Style Council

Used when visual style is central.

Agents:

- `StyleReferenceAnalyzer`
- `ColorLightingAgent`
- `CompositionAgent`
- `CameraLanguageAgent`
- `SubtitleVisualAgent`
- `StyleRiskAgent`
- `StyleGuideAssembler`

### 13.5 Horror Atmosphere Council

Used for horror, weirdcore, dreamcore, found-footage, and suspense.

Agents:

- `FearTypeClassifier`
- `PacingAndSilenceAgent`
- `RevealStrategyAgent`
- `SoundFearAgent`
- `OverExplanationGuard`
- `PlatformHorrorRiskAgent`
- `HorrorPlanAssembler`

### 13.6 Meme Edit Council

Used for abstract, fast-cut, chaotic, subtitle-heavy videos.

Agents:

- `ChaosLevelAgent`
- `SubtitleMemeAgent`
- `SFXPlacementAgent`
- `ReactionTimingAgent`
- `ComprehensionGuard`
- `MemeEditAssembler`

### 13.7 Dance / Motion Council

Used for dance, action imitation, MMD, motion-heavy routes.

Agents:

- `MotionComplexityAgent`
- `DanceBeatAgent`
- `BodyConsistencyRiskAgent`
- `MMDRouteAgent`
- `AIMotionRouteAgent`
- `MotionPlanAssembler`

### 13.8 Longform Council

Used for videos from several minutes to hours.

Agents:

- `ChapterPlanner`
- `InformationDensityAgent`
- `NarrationStructureAgent`
- `SegmentReuseAgent`
- `LongformContinuityAgent`
- `LongformPlanAssembler`

---

## 14. Asset Resolver Agent Group

### 14.1 Purpose

Find or create required assets.

### 14.2 Agents

- `LocalAssetLookupAgent`
- `ResearchAssetLookupAgent`
- `OfficialSourceFinder`
- `PersonalCreatorReviewDetector`
- `WebReferenceSearchAgent`
- `GeneratedAssetProposalAgent`
- `CapabilityBuildRequestAgent`
- `HumanTaskAgent`
- `ResolvedAssetAssembler`

### 14.3 Ordered Flow

```text
1. Normalize asset requirements
2. Search local assets
3. Search research assets
4. Search official web sources
5. Search broader web references
6. Mark official/personal/unknown source policy
7. Propose generated alternatives
8. Create human tasks for gaps
9. Assemble resolved assets
```

---

## 15. Generation Manager Agent Group

### 15.1 Purpose

Turn production plans into generated assets.

### 15.2 Agents

- `RequirementNormalizer`
- `RoutePlanner`
- `ToolSelector`
- `PromptBuilder`
- `NegativePromptBuilder`
- `CostPlanner`
- `BatchGenerator`
- `FailureHandler`
- `FallbackPlanner`
- `CandidateRegistrar`
- `HandoffManager`

### 15.3 Ordered Flow

```text
1. Normalize requirements
2. Resolve tool options
3. Check permission and budget
4. Build prompts per tool
5. Generate draft candidates
6. Register outputs
7. Hand off to Quality Council
```

---

## 16. Quality Council

### 16.1 Purpose

Evaluate candidates in layers.

### 16.2 Layers

```text
1. TechnicalQA
2. CheapVisualQA
3. SemanticQA
4. SpecialistQA
5. StrongJudge
6. RegentFinalDecision
```

TechnicalQA is program-first, agent-assisted.

### 16.3 Specialist QA Agents

- `MemeQA`
- `HorrorQA`
- `MusicSyncQA`
- `CharacterQA`
- `VisualStyleQA`
- `LongformQA`
- `PlatformQA`

### 16.4 Output

```json
{
  "candidate_id": "candidate_001",
  "publish_ready": false,
  "decision": "retry",
  "failure_tags": ["semantic_transfer_failed"],
  "scores": {},
  "retry_recommendations": []
}
```

---

## 17. Revision and Retry Agent Group

### 17.1 Purpose

Turn quality failures into targeted next actions.

### 17.2 Agents

- `FailureClassifier`
- `FixStrategySelector`
- `PreservationGuard`
- `PromptRevisionAgent`
- `NegativePromptRevisionAgent`
- `AssetRevisionAgent`
- `RouteRevisionAgent`
- `BudgetGuard`
- `RegressionRiskAgent`
- `RetryPlanner`
- `MemoryWriter`

### 17.3 Ordered Flow

```text
1. Classify failure
2. Preserve successful parts
3. Select fix strategy
4. Revise prompt/assets/route
5. Check budget and regression risk
6. Create retry plan
7. Write memory
```

---

## 18. Packaging Council

### 18.1 Purpose

Create platform packaging.

### 18.2 Agents

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
- `PlatformPayloadAssembler`

### 18.3 Ordered Flow

```text
1. Load final video and format context
2. Generate title options
3. Generate description and tags
4. Generate or choose covers
5. Critique packaging
6. Create per-platform payloads
```

---

## 19. Publish Council and Publisher Agents

### 19.1 Purpose

Prepare, upload, publish, and collect feedback.

### 19.2 Agents

- `PublishReadinessAgent`
- `PlatformExclusionAndAdaptationAgent`
- `PublishRiskReviewAgent`
- `ScheduleAgent`
- `UploadAgent`
- `PublishLogger`
- `FeedbackCollector`
- `FeedbackAnalyst`

### 19.3 Platform Publisher Agents

- `BilibiliPublisher`
- `DouyinPublisher`
- `XiaohongshuPublisher`
- `YouTubePublisher`
- `ManualPublisher`

### 19.4 Default Policy

Default is all-platform publishing unless a platform is skipped, blocked, or needs packaging changes.

---

## 20. Learning Agents

### 20.1 Purpose

Convert production and publish outcomes into memory.

### 20.2 Agents

- `FormatLearningAgent`
- `TrendPredictionLearningAgent`
- `ToolPerformanceLearningAgent`
- `QualityLearningAgent`
- `UserPreferenceLearningAgent`
- `PlatformLearningAgent`
- `PackagingLearningAgent`
- `AssetLearningAgent`
- `WeightSuggestionAgent`
- `ReflectionReporter`

### 20.3 Output Types

- `observation`
- `suggestion`
- `approved_rule`

Only observations can be written automatically. Suggestions need user approval to become rules.

---

## 21. Agent Disagreement Handling

### 21.1 Disagreement Types

- score disagreement;
- semantic interpretation disagreement;
- character fit disagreement;
- risk disagreement;
- tool feasibility disagreement;
- publish readiness disagreement.

### 21.2 Resolution Flow

```text
1. Record disagreement
2. Ask relevant specialist
3. If still unresolved, escalate model tier
4. If high risk or user preference unclear, create ReviewItem
5. Regent makes final decision if permission allows
```

### 21.3 Disagreement Record

```json
{
  "topic": "character_fit",
  "positions": [
    {
      "agent": "RelationshipFitAgent",
      "position": "fit",
      "confidence": 0.72
    },
    {
      "agent": "OOCGuard",
      "position": "risky",
      "confidence": 0.81
    }
  ],
  "resolution": "ask_user",
  "review_item_id": "review_000001"
}
```

---

## 22. Agent Output Contract

Every agent output should include:

```json
{
  "agent": "...",
  "stage": "...",
  "input_refs": [],
  "summary": "...",
  "recommendation": "...",
  "confidence": 0.0,
  "scores": {},
  "reasons": [],
  "concerns": [],
  "evidence": [],
  "risks": [],
  "next_actions": [],
  "needs_user_review": false,
  "created_review_items": [],
  "memory_entries": []
}
```

---

## 23. Gate Points

Important gates:

1. Trend selection gate.
2. Reproduction strategy gate.
3. Semantic transfer gate.
4. Asset availability gate.
5. Generation cost gate.
6. Candidate quality gate.
7. Retry continuation gate.
8. Publish readiness gate.
9. Auto publish gate.
10. Learning rule application gate.

Each gate should:

- check permissions;
- check risk;
- collect agent votes;
- write decision log;
- create review item if needed.

---

## 24. First Production Line Agent Flow

For `route_ordinary_ai_format_video`:

```text
Run Intake
  -> Source Scout Agent Group
  -> Harvester Agent Group
  -> Video Understanding Agent Group
  -> Format Miner Agent Group
  -> Trend Analyst Agent Group
  -> Regent Gate
  -> Format Reproduction Council
  -> Semantic Format Transfer Council if needed
  -> Route Selector
  -> Specialized Councils
  -> Asset Resolver Agent Group
  -> Generation Manager Agent Group
  -> Quality Council
  -> Revision and Retry Agent Group if needed
  -> Final Judge / Regent
  -> Packaging Council
  -> Publish Council
  -> Publisher Agents
  -> Feedback Collector
  -> Learning Agents
```

---

## 25. Implementation Notes

1. Do not implement all agents as separate expensive LLM calls at first.
2. Many early agents can be deterministic functions, templates, or cheap model calls.
3. Keep agent names in outputs even if implementation is simple at first.
4. The important part is stable inputs, outputs, logs, and responsibilities.
5. Add stronger models only where value is clear.
6. Every agent group should be testable with saved JSON inputs.
7. Never write fake external APIs. Use interfaces and TODO setup reports.

