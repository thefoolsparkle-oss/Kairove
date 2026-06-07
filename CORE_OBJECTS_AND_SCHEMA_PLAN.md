# Kairove Core Objects and Schema Plan

## 0. Purpose

This document defines the core objects, database entities, status flows, and storage rules for Kairove.

The goal is not to lock implementation details too early, but to make sure future code has stable concepts:

- what a run is;
- what a job is;
- what a source is;
- what an asset is;
- what a format is;
- how decisions are logged;
- how review items are created;
- how candidates, quality reports, publish records, and learning memories connect.

Kairove should be explainable and recoverable. Every generated video must be traceable from:

```text
source trend -> format -> reproduction plan -> assets -> generation steps -> candidates -> QC -> final package -> publish result -> learning update
```

---

## 1. Storage Strategy

Kairove should use a hybrid storage model:

```text
Database:
  indexes, metadata, object status, relationships, hashes, timestamps, scores.

Filesystem:
  large files, raw videos, screenshots, generated videos, prompts, reports, publish packages.

Manifests:
  per-file provenance, usage policy, review status, and relation to jobs.
```

Early implementation can use SQLite. Later implementation can move to Postgres without changing the conceptual model.

Large binary assets should not be stored directly in the database.

---

## 2. Core Object List

Core objects:

1. `Run`
2. `Job`
3. `SourceCandidate`
4. `Source`
5. `Asset`
6. `Format`
7. `FormatObservation`
8. `TrendScorecard`
9. `DecisionLog`
10. `ReviewItem`
11. `ProductionRecipe`
12. `ReproductionPlan`
13. `CouncilOutput`
14. `GenerationStep`
15. `Candidate`
16. `QualityReport`
17. `RetryPlan`
18. `PublishPackage`
19. `PublishRecord`
20. `PlatformMetric`
21. `MemoryEntry`
22. `Tool`
23. `ToolPerformanceRecord`
24. `Character`
25. `Relationship`
26. `UserPreference`
27. `ScoreProfile`

---

## 3. Run

### 3.1 Meaning

A `Run` is one execution session of Kairove.

Examples:

- daily trend scouting;
- manual keyword search;
- analysis of one video link;
- production of a selected format;
- review-only session;
- publish feedback collection.

A run may create many source candidates, sources, formats, and jobs.

### 3.2 Fields

```json
{
  "run_id": "run_000001",
  "run_type": "scout | planning | production | review | publish_feedback | learning",
  "trigger_type": "manual | scheduled | regent_auto | user_link | keyword",
  "input_summary": "...",
  "status": "pending | running | waiting_for_user | failed | completed | abandoned",
  "started_at": "...",
  "completed_at": null,
  "created_by": "user | kairove_regent",
  "permission_snapshot_id": "...",
  "config_snapshot_id": "...",
  "notes": ""
}
```

### 3.3 Rules

- Every automated action should belong to a run.
- A run can be resumed.
- A run must keep a decision log.
- A run can produce zero jobs if no format is worth making.

---

## 4. Job

### 4.1 Meaning

A `Job` is one actual video production task.

It starts after Kairove decides a trend or format is worth producing.

### 4.2 Fields

```json
{
  "job_id": "job_000001",
  "run_id": "run_000001",
  "job_type": "ordinary_ai_format_video | music_sync | character_reenactment | horror | longform | mmd_3d | hybrid",
  "title_working": "...",
  "format_id": "fmt_000001",
  "status": "created | planning | resolving_assets | generating | quality_checking | retrying | packaging | publishing | waiting_for_user | completed | abandoned | failed",
  "priority": "low | normal | high | urgent",
  "target_platforms": ["bilibili", "douyin", "xiaohongshu", "youtube"],
  "created_at": "...",
  "updated_at": "...",
  "completed_at": null,
  "job_dir": "generated_assets/jobs/job_000001",
  "user_notes": ""
}
```

### 4.3 Job Directory

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

### 4.4 Rules

- A job must have a job directory.
- A job must record all source references.
- A job may have multiple candidates.
- A job may be abandoned with a reason.
- A job cannot be considered complete without a final report, even if no video is published.

---

## 5. SourceCandidate

### 5.1 Meaning

A `SourceCandidate` is a candidate discovered by Source Scout before full harvesting.

It may be a video, article, music page, wiki page, search result, creator profile, topic page, or manual link.

### 5.2 Fields

```json
{
  "candidate_source_id": "cand_src_000001",
  "run_id": "run_000001",
  "platform": "bilibili | douyin | xiaohongshu | youtube | tiktok | weibo | search | wiki | manual",
  "url": "...",
  "title": "...",
  "author": "...",
  "content_type": "video | audio | article | wiki_page | topic_page | profile | unknown",
  "observed_metrics": {
    "views": null,
    "likes": null,
    "comments": null,
    "shares": null,
    "favorites": null
  },
  "discovery_reason": ["keyword_match", "hot_rank", "similar_script_cluster"],
  "status": "new | selected_for_harvest | ignored | failed",
  "collected_at": "..."
}
```

### 5.3 Rules

- SourceCandidate is lightweight.
- It should not require complete downloads.
- Many candidates may be discarded before harvesting.

---

## 6. Source

### 6.1 Meaning

A `Source` is a harvested research object.

It has provenance, local files, usage policy, and understanding reports.

### 6.2 Fields

```json
{
  "source_id": "src_000001",
  "candidate_source_id": "cand_src_000001",
  "run_id": "run_000001",
  "platform": "douyin",
  "url": "...",
  "source_type": "official | personal_creator | platform_user | unknown | generated | user_provided",
  "content_type": "video | image | audio | page | comment_thread",
  "usage_policy": "analysis_only | reference_only | style_analysis | direct_use | blocked | unknown",
  "review_status": "not_required | pending | approved | rejected",
  "harvest_status": "metadata_only | partial | complete | failed",
  "manifest_path": "research_assets/manifests/src_000001.json",
  "understanding_report_path": "...",
  "created_at": "...",
  "updated_at": "..."
}
```

### 6.3 Rules

- Official sources can default to `direct_use` under current user policy.
- Personal creator and unknown sources default to `ask_user` / `reference_only` until reviewed.
- Every source must have a manifest.
- Failed harvests should still be recorded.

---

## 7. Asset

### 7.1 Meaning

An `Asset` is any usable or referenceable file or capability.

Examples:

- harvested video;
- official image;
- generated keyframe;
- local voice profile;
- local character model;
- BGM;
- subtitle style template;
- cover image;
- prompt file.

### 7.2 Fields

```json
{
  "asset_id": "asset_000001",
  "asset_class": "research | local | generated",
  "asset_type": "video | image | audio | voice_profile | model | motion | subtitle_style | cover | prompt | text | other",
  "source_id": "src_000001",
  "job_id": "job_000001",
  "storage_path": "...",
  "hash": "...",
  "source_type": "official | personal_creator | unknown | generated | user_provided",
  "usage_policy": "analysis_only | reference_only | style_analysis | direct_use | generated | user_provided | blocked",
  "review_status": "not_required | pending | approved | rejected",
  "used_in_jobs": ["job_000001"],
  "metadata": {},
  "created_at": "...",
  "updated_at": "..."
}
```

### 7.3 Rules

- Assets from official sources may default to direct use.
- Assets from personal creators or unknown sources require review for final use.
- Generated assets must record model, prompt, input references, and generation step.
- Local assets must never be auto-deleted.

---

## 8. Format

### 8.1 Meaning

A `Format` is a reusable video pattern discovered by Format Miner.

It may be:

- a dialogue meme;
- a music sync pattern;
- a horror atmosphere pattern;
- an AI visual style;
- a subtitle/editing template;
- a role relationship structure;
- a longform narrative structure.

### 8.2 Fields

```json
{
  "format_id": "fmt_000001",
  "name": "嘴硬不抽卡",
  "category": "dialogue_meme",
  "format_genome_path": "knowledge_base/formats/format_genomes/fmt_000001.json",
  "current_lifecycle_stage": "emerging | rising | peak | fatigue | dead | unknown",
  "fatigue_score": 2.1,
  "remixability_score": 8.4,
  "recommended_routes": ["script_council", "character_reenactment_council"],
  "created_at": "...",
  "updated_at": "...",
  "confidence": 0.82
}
```

### 8.3 Format Genome

The genome file should include:

```json
{
  "format_id": "fmt_000001",
  "core_structure": ["denial", "evidence", "defense", "collapse"],
  "relationship_pattern": "intimate teasing / familiar exposure",
  "visual_grammar": ["reaction closeups", "fast subtitles"],
  "audio_grammar": ["comedic sting", "short silence before punchline"],
  "must_preserve": ["role contrast", "evidence reveal", "final collapse"],
  "replaceable_slots": ["characters", "object_of_desire", "world_context"],
  "avoid": ["exact personal creator lines if not approved"],
  "successful_transfers": [],
  "failed_transfers": []
}
```

### 8.4 Rules

- Format is long-lived.
- It should be updated by learning feedback.
- It should distinguish new formats from variants.

---

## 9. FormatObservation

### 9.1 Meaning

A `FormatObservation` links a source to a format.

It records evidence that a source belongs to a format.

### 9.2 Fields

```json
{
  "observation_id": "fmt_obs_000001",
  "format_id": "fmt_000001",
  "source_id": "src_000001",
  "similarity_score": 0.87,
  "evidence": [
    "same denial -> exposure -> collapse structure",
    "similar subtitle rhythm"
  ],
  "created_at": "..."
}
```

---

## 10. TrendScorecard

### 10.1 Meaning

A `TrendScorecard` records trend and production opportunity scoring for a format.

### 10.2 Fields

```json
{
  "scorecard_id": "trend_score_000001",
  "format_id": "fmt_000001",
  "run_id": "run_000001",
  "score_profile_id": "trend_video_v1",
  "positive_scores": {},
  "penalties": {},
  "final_score": 7.29,
  "decision": "make_video | observe | reject | ask_user",
  "reason": "...",
  "scorecard_path": "...",
  "created_at": "..."
}
```

### 10.3 Rules

- Every score must expose weight and weighted contribution.
- Score profiles must be versioned.
- Scores must be recalculable when weights change.

---

## 11. DecisionLog

### 11.1 Meaning

A `DecisionLog` records why Kairove did something.

It is essential for explainability.

### 11.2 Fields

```json
{
  "decision_id": "decision_000001",
  "run_id": "run_000001",
  "job_id": "job_000001",
  "stage": "trend_selection | asset_resolution | generation | quality | publish | learning",
  "actor": "kairove_regent | user | council | system",
  "decision": "selected_format_for_production",
  "inputs": {},
  "agent_votes": [],
  "permission_checks": [],
  "risk_checks": [],
  "reason": "...",
  "created_at": "..."
}
```

### 11.3 Rules

- Every gate must write a decision log.
- If Kairove asks the user, the answer should be linked back to the decision log.

---

## 12. ReviewItem

### 12.1 Meaning

A `ReviewItem` is a task requiring user judgment.

Examples:

- approve personal creator asset;
- confirm CP mapping;
- configure API;
- approve high-cost retry;
- approve publish;
- accept weight adjustment suggestion.

### 12.2 Fields

```json
{
  "review_id": "review_000001",
  "type": "asset_review | risk_review | tool_setup | publish_approval | weight_change | character_mapping | user_decision",
  "run_id": "run_000001",
  "job_id": "job_000001",
  "blocking": true,
  "priority": "low | normal | high | urgent",
  "summary": "...",
  "details_path": "...",
  "system_recommendation": "...",
  "options": ["approve", "reject", "ask_more", "replace"],
  "status": "pending | approved | rejected | deferred | resolved",
  "created_at": "...",
  "resolved_at": null,
  "user_response": null
}
```

### 12.3 Rules

- Review items should be short and decision-focused.
- They should link to evidence, not dump raw logs.
- Blocking review items pause the related job or run.

---

## 13. ProductionRecipe

### 13.1 Meaning

A `ProductionRecipe` is the executable plan before actual generation.

It is produced after trend scoring, format reproduction, and route selection.

### 13.2 Fields

```json
{
  "recipe_id": "recipe_000001",
  "job_id": "job_000001",
  "format_id": "fmt_000001",
  "video_project_type": "ordinary_ai_format_video",
  "primary_route": "character_reenactment",
  "supporting_routes": ["script_council", "meme_edit_council"],
  "duration_strategy": "short_punchline | mini_drama | longform | unknown",
  "target_platforms": ["bilibili", "douyin", "xiaohongshu", "youtube"],
  "required_assets": [],
  "tool_plan": [],
  "quality_requirements": [],
  "risk_notes": [],
  "recipe_path": "...",
  "created_at": "..."
}
```

---

## 14. ReproductionPlan

### 14.1 Meaning

A `ReproductionPlan` says how Kairove will reproduce a source format.

It is not a script or prompt. It is a strategy.

### 14.2 Fields

```json
{
  "reproduction_plan_id": "repro_000001",
  "job_id": "job_000001",
  "format_id": "fmt_000001",
  "primary_reproduction_target": "relationship rhythm and punchline structure",
  "must_preserve": [],
  "should_preserve": [],
  "optional": [],
  "avoid": [],
  "semantic_transfer": {},
  "adaptation_strategy": "...",
  "confidence": 0.81,
  "human_review_needed": false,
  "plan_path": "...",
  "created_at": "..."
}
```

---

## 15. CouncilOutput

### 15.1 Meaning

Each Specialized Council produces a `CouncilOutput`.

### 15.2 Fields

```json
{
  "council_output_id": "council_out_000001",
  "job_id": "job_000001",
  "council": "script_council | music_sync_council | visual_style_council | character_reenactment_council | horror_atmosphere_council | meme_edit_council | hybrid_council",
  "role": "primary | supporting",
  "plan_path": "...",
  "needed_assets": [],
  "recommended_tools": [],
  "quality_checks_needed": [],
  "risks": [],
  "status": "draft | accepted | rejected | revised",
  "created_at": "..."
}
```

---

## 16. GenerationStep

### 16.1 Meaning

A `GenerationStep` is one tool call or generation action.

Examples:

- generate image;
- image-to-video;
- TTS;
- subtitle render;
- cover generation;
- video edit;
- audio mix.

### 16.2 Fields

```json
{
  "step_id": "gen_step_000001",
  "job_id": "job_000001",
  "candidate_id": "candidate_001",
  "step_type": "image_generation | image_to_video | text_to_video | tts | audio_mix | subtitle_render | cover_generation | edit",
  "tool_id": "kling_image_to_video",
  "input_assets": [],
  "output_assets": [],
  "prompt_path": "...",
  "parameters": {},
  "status": "pending | running | success | failed | skipped | retrying",
  "cost_estimate": null,
  "actual_cost": null,
  "error_message": null,
  "started_at": "...",
  "completed_at": null
}
```

### 16.3 Rules

- Every generated asset should be linked to a generation step.
- Failed steps should be recorded with reason.
- Retried steps should link to previous failed steps.

---

## 17. Candidate

### 17.1 Meaning

A `Candidate` is one generated video or package version competing for final selection.

### 17.2 Fields

```json
{
  "candidate_id": "candidate_001",
  "job_id": "job_000001",
  "candidate_type": "video | scene | cover | audio | package",
  "status": "generated | quality_checking | rejected | selected | archived | failed",
  "output_path": "generated_assets/jobs/job_000001/candidates/candidate_001/video.mp4",
  "generation_steps": ["gen_step_000001"],
  "quality_report_id": "quality_000001",
  "score": null,
  "selected_reason": null,
  "created_at": "..."
}
```

---

## 18. QualityReport

### 18.1 Meaning

A `QualityReport` records multi-layer QC results for a candidate.

### 18.2 Fields

```json
{
  "quality_report_id": "quality_000001",
  "candidate_id": "candidate_001",
  "job_id": "job_000001",
  "technical_qa_path": "...",
  "cheap_visual_qa_path": "...",
  "semantic_qa_path": "...",
  "specialist_qa_path": "...",
  "strong_judge_path": "...",
  "final_scorecard_path": "...",
  "failure_tags": ["semantic_transfer_failed"],
  "publish_ready": false,
  "decision": "retry | reject | select | ask_user",
  "created_at": "..."
}
```

---

## 19. RetryPlan

### 19.1 Meaning

A `RetryPlan` turns quality failures into next actions.

### 19.2 Fields

```json
{
  "retry_plan_id": "retry_000001",
  "job_id": "job_000001",
  "candidate_id": "candidate_001",
  "retry_round": 2,
  "decision": "retry_with_prompt_change | retry_with_asset_change | retry_with_route_change | abandon | ask_user",
  "root_causes": [],
  "preserve": [],
  "changes": [],
  "expected_improvements": [],
  "risks": [],
  "plan_path": "...",
  "created_at": "..."
}
```

---

## 20. PublishPackage

### 20.1 Meaning

A `PublishPackage` is the final bundle prepared for platforms.

### 20.2 Fields

```json
{
  "publish_package_id": "pkg_000001",
  "job_id": "job_000001",
  "final_video_path": "...",
  "cover_paths": {},
  "platform_payloads_path": "...",
  "readiness_report_path": "...",
  "status": "draft | ready | published | failed",
  "created_at": "..."
}
```

---

## 21. PublishRecord

### 21.1 Meaning

A `PublishRecord` records an upload or publication attempt.

### 21.2 Fields

```json
{
  "publish_record_id": "pub_000001",
  "job_id": "job_000001",
  "platform": "bilibili | douyin | xiaohongshu | youtube",
  "method": "official_api | browser_automation | manual",
  "status": "not_started | preparing | auth_failed | uploading | uploaded_draft | scheduled | published | failed | needs_user_action | skipped",
  "platform_item_id": null,
  "url": null,
  "payload_path": "...",
  "error_message": null,
  "created_at": "...",
  "updated_at": "..."
}
```

---

## 22. PlatformMetric

### 22.1 Meaning

Platform metrics record post-publish performance.

### 22.2 Fields

```json
{
  "metric_id": "metric_000001",
  "publish_record_id": "pub_000001",
  "platform": "douyin",
  "collected_at": "...",
  "views": null,
  "likes": null,
  "comments": null,
  "shares": null,
  "favorites": null,
  "completion_rate": null,
  "follower_gain": null,
  "comment_sentiment_path": null,
  "raw_metrics": {}
}
```

---

## 23. MemoryEntry

### 23.1 Meaning

A `MemoryEntry` stores learning observations, suggestions, and approved rules.

### 23.2 Fields

```json
{
  "memory_id": "mem_000001",
  "memory_type": "observation | suggestion | approved_rule",
  "scope": "format | tool | user_preference | platform | packaging | quality | asset",
  "related_object_type": "format | tool | job | candidate | platform | score_profile",
  "related_object_id": "fmt_000001",
  "content": {},
  "confidence": 0.78,
  "requires_user_approval": true,
  "status": "active | pending_approval | rejected | archived",
  "created_at": "...",
  "updated_at": "..."
}
```

### 23.3 Rules

- Observations can be written automatically.
- Suggestions require user approval to become rules.
- Approved rules should be versioned.

---

## 24. Tool

### 24.1 Meaning

A `Tool` is any AI model, API, local service, scraper, publisher, or helper capability.

### 24.2 Fields

```json
{
  "tool_id": "tool_000001",
  "display_name": "Kling Image-to-Video",
  "tool_type": "image_to_video",
  "provider": "kling",
  "status": "available | not_configured | requires_api_key | requires_account | requires_permission | requires_local_install | temporarily_failed | deprecated | blocked | unknown",
  "auth_status": "configured | missing | expired | not_required",
  "supported_inputs": ["image", "prompt"],
  "outputs": ["video"],
  "strengths": [],
  "weaknesses": [],
  "cost_level": "free | low | medium | high | unknown",
  "route_compatibility": {},
  "setup_requirements": [],
  "created_at": "...",
  "updated_at": "..."
}
```

---

## 25. ToolPerformanceRecord

### 25.1 Meaning

Records historical performance of a tool in a context.

### 25.2 Fields

```json
{
  "record_id": "tool_perf_000001",
  "tool_id": "tool_000001",
  "context": {
    "route": "character_reenactment",
    "scene_type": "two_character_dialogue"
  },
  "runs": 28,
  "avg_quality_score": 6.4,
  "common_failures": ["identity_drift", "hand_failure"],
  "successful_workarounds": ["split into reaction shots"],
  "updated_at": "..."
}
```

---

## 26. Character

### 26.1 Meaning

A `Character` represents a real or fictional role known to Kairove.

It can come from official material, wiki research, user notes, or generated original settings.

### 26.2 Fields

```json
{
  "character_id": "char_000001",
  "world_id": "world_000001",
  "name": "...",
  "source_type": "official | wiki | user_note | generated | unknown",
  "visual_profile_path": "...",
  "personality": [],
  "speech_style": "...",
  "risk_notes": [],
  "review_status": "pending | approved | rejected | not_required",
  "created_at": "...",
  "updated_at": "..."
}
```

---

## 27. Relationship

### 27.1 Meaning

A `Relationship` stores character relationships, CP dynamics, rivalry, partnership, or other semantic relations.

### 27.2 Fields

```json
{
  "relationship_id": "rel_000001",
  "source_character_id": "char_000001",
  "target_character_id": "char_000002",
  "relationship_type": "popular_cp | canon_pair | rival | partner | mentor_student | player_character | unknown",
  "dynamic": "互怼但信任",
  "fit_for_formats": ["denial_dialogue", "jealousy_meme"],
  "risk_notes": [],
  "confidence": 0.74,
  "verified_by_user": false,
  "created_at": "...",
  "updated_at": "..."
}
```

---

## 28. UserPreference

### 28.1 Meaning

Stores user preferences learned or manually set.

### 28.2 Fields

```json
{
  "preference_id": "pref_000001",
  "scope": "global | platform | format | character | route | packaging",
  "key": "...",
  "value": {},
  "source": "manual | inferred | approved_suggestion",
  "confidence": 1.0,
  "created_at": "...",
  "updated_at": "..."
}
```

---

## 29. ScoreProfile

### 29.1 Meaning

A score profile stores weights for trend scoring or quality scoring.

### 29.2 Fields

```json
{
  "score_profile_id": "trend_video_v1",
  "profile_type": "trend | quality | packaging | platform",
  "version": "1.0",
  "weights": {},
  "created_at": "...",
  "updated_at": "...",
  "change_note": ""
}
```

### 29.3 Rules

- Score profiles must be versioned.
- Changes should not silently affect old scorecards unless explicitly recalculated.

---

## 30. State Flow Summary

### 30.1 Source Flow

```text
SourceCandidate
  -> Source
  -> UnderstandingReport
  -> FormatObservation
  -> Format
```

### 30.2 Production Flow

```text
Format
  -> TrendScorecard
  -> Job
  -> ReproductionPlan
  -> ProductionRecipe
  -> CouncilOutputs
  -> GenerationSteps
  -> Candidates
  -> QualityReports
  -> RetryPlans
  -> Final Candidate
  -> PublishPackage
  -> PublishRecords
  -> PlatformMetrics
  -> MemoryEntries
```

### 30.3 Review Flow

```text
Risk / Permission / Unknown / Cost / Tool Gap
  -> ReviewItem
  -> User Decision
  -> DecisionLog
  -> Continue / Change / Stop
```

---

## 31. Minimal Database Tables

Initial tables:

```text
runs
jobs
source_candidates
sources
assets
formats
format_observations
trend_scorecards
decision_logs
review_items
production_recipes
reproduction_plans
council_outputs
generation_steps
candidates
quality_reports
retry_plans
publish_packages
publish_records
platform_metrics
memory_entries
tools
tool_performance_records
characters
relationships
user_preferences
score_profiles
```

This is enough to support the first production line without locking future 3D/MMD or longform extensions.

---

## 32. Status Vocabulary

Use consistent statuses.

### 32.1 Generic

```text
pending
running
waiting_for_user
waiting_for_api
failed
retrying
completed
skipped
abandoned
```

### 32.2 Review

```text
pending
approved
rejected
deferred
resolved
archived
```

### 32.3 Publish

```text
not_started
preparing
auth_failed
uploading
uploaded_draft
scheduled
published
failed
needs_user_action
skipped
```

---

## 33. ID Rules

Suggested IDs:

```text
run_000001
job_000001
cand_src_000001
src_000001
asset_000001
fmt_000001
fmt_obs_000001
trend_score_000001
decision_000001
review_000001
recipe_000001
repro_000001
council_out_000001
gen_step_000001
candidate_001
quality_000001
retry_000001
pkg_000001
pub_000001
metric_000001
mem_000001
tool_000001
char_000001
rel_000001
pref_000001
```

IDs should be stable and human-readable.

---

## 34. Important Design Rules

1. Every significant action belongs to a run.
2. Every production task belongs to a job.
3. Every file-like object should be an asset or linked to an asset.
4. Every source and asset needs provenance.
5. Every gate writes a decision log.
6. Every user decision should resolve a review item.
7. Every generated candidate must link to generation steps.
8. Every quality failure should have failure tags.
9. Every retry should preserve what worked when possible.
10. Every publish attempt should create a publish record.
11. Every feedback loop should write memory entries.
12. Old scorecards should remain reproducible even after weight changes.

---

## Cross-Phase Policy Alignment - 2026-06-06

Language and identifier policy:

```text
User-facing titles/descriptions/tags/reports/review items are Chinese primary.
YouTube Shorts may receive English auxiliary metadata.
Prompts may keep Chinese explanation plus English generation prompt.
Internal object IDs, schema fields, and config keys stay English.
```

Retention and deletion:

```text
Default retention is long-term.
Failed generations, old candidates, downloaded assets, QA reports, and publish packages keep source and usage records.
Cleanup requires manifest and traceable records.
Deleting generated assets asks.
Deleting local assets defaults deny.
```
