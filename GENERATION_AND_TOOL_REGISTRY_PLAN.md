# Kairove Generation and Tool Registry Plan

## 0. Purpose

This document defines how Kairove stores tool capabilities and how Generation Manager selects tools, builds prompts, generates candidates, handles failures, and registers outputs.

---

## 1. Tool Capability Registry

The registry records what Kairove can use.

Tool categories:

```text
text_generation
vision_language_model
image_generation
image_to_video
text_to_video
video_to_video
audio_generation
tts
voice_training
music_identification
audio_analysis
video_editing
subtitle_rendering
cover_generation
platform_upload
metrics_fetch
web_search
web_browser
scraper
database
```

Tool status:

```text
available
not_configured
requires_api_key
requires_account
requires_permission
requires_local_install
temporarily_failed
deprecated
blocked
unknown
```

---

## 2. Tool Card

```json
{
  "tool_id": "kling_image_to_video",
  "display_name": "Kling Image-to-Video",
  "tool_type": "image_to_video",
  "provider": "kling",
  "status": "requires_api_key",
  "supported_inputs": ["image", "prompt"],
  "outputs": ["video"],
  "supported_ratios": ["9:16", "16:9", "1:1"],
  "strengths": ["short character reaction", "cinematic motion"],
  "weaknesses": ["long consistency", "complex two-character interaction"],
  "route_compatibility": {
    "character_reenactment": 8.0,
    "two_character_dialogue": 4.0,
    "horror_atmosphere": 8.5
  },
  "cost_level": "medium",
  "speed_level": "medium"
}
```

---

## 3. Generation Manager Flow

```text
1. RequirementNormalizer
2. RoutePlanner
3. ToolSelector
4. Permission and Budget Check
5. PromptBuilder
6. NegativePromptBuilder
7. GenerationStep Builder
8. BatchGenerator
9. CandidateRegistrar
10. FailureHandler
11. HandoffManager
```

---

## 4. Production Routes

Supported route types:

```text
text_to_video
image_to_video
multi_image_to_video
video_to_video
reference_video_reenactment
character_reenactment
music_sync_video
short_drama_multi_scene
horror_atmosphere_video
meme_edit_video
mmd_3d_assisted_video
longform_video
hybrid_pipeline
```

Routes should not assume one model can do everything.

---

## 5. Tool Selection

ToolSelector considers:

- availability;
- input/output support;
- route compatibility;
- character consistency;
- long duration support;
- multi-character support;
- cost;
- speed;
- historical quality;
- recent failure rate;
- user permission;
- platform requirements.

Output:

```json
{
  "selected_tool": "kling_image_to_video",
  "reason": "Best available image-to-video tool for short character reaction.",
  "alternatives": [
    {
      "tool_id": "local_comfyui_pipeline",
      "reason": "Cheaper but weaker motion."
    }
  ],
  "confidence": 0.78
}
```

---

## 6. Prompt Packages

Prompts should be per-step and per-tool.

Prompt package:

```json
{
  "prompt_package_id": "prompt_pkg_000001",
  "job_id": "job_000001",
  "step_id": "gen_step_000001",
  "tool_id": "kling_image_to_video",
  "positive_prompt_path": "...",
  "negative_prompt_path": "...",
  "prompt_metadata": {
    "source_format_id": "fmt_000001",
    "candidate_strategy": "reaction_shot",
    "preserve": [],
    "avoid": []
  }
}
```

---

## 7. GenerationStep

Every generation call is recorded as a step:

```json
{
  "step_id": "gen_step_000001",
  "job_id": "job_000001",
  "candidate_id": "candidate_001",
  "step_type": "image_to_video",
  "tool_id": "kling_image_to_video",
  "input_assets": ["asset_000001"],
  "output_assets": [],
  "prompt_path": "...",
  "parameters": {},
  "status": "pending | running | success | failed | skipped",
  "error_message": null
}
```

---

## 8. Candidate Strategy

Generation should usually create multiple candidates:

```yaml
candidate_strategy:
  draft_candidates_per_key_scene: 3
  final_candidates_per_key_scene: 2
  critical_scene_extra_candidates: true
  stop_when_quality_above: 8.2
```

Candidate count should depend on:

- scene importance;
- generation cost;
- tool reliability;
- retry policy;
- user permission.

---

## 9. Failure Handling

Failure types:

```text
api_error
auth_error
rate_limit
prompt_rejected
bad_output
timeout
tool_capability_gap
cost_limit
unknown_error
```

Generation Manager should:

- record the failure;
- mark tool health if needed;
- create setup item if auth/config missing;
- request retry if recoverable;
- ask Revision Engine for strategy if output bad.

---

## 10. Fallback Planning

Examples:

```text
text_to_video fails character consistency
  -> use generated key image + image_to_video

continuous two-character scene fails
  -> split into reaction shots

complex dance fails
  -> use beat-synced cuts or MMD route

tool unavailable
  -> manual package / ask user / alternate model
```

---

## 11. Tool Performance Learning

After each generation:

- record success/failure;
- quality score;
- failure tags;
- cost;
- duration;
- prompt style;
- workaround.

This updates Tool Performance Records.

---

## 12. Acceptance Criteria

Generation system is ready when it can:

1. Register tools.
2. Mark missing tool setup.
3. Select a tool for a route.
4. Build step-specific prompts.
5. Create generation steps.
6. Register outputs as assets.
7. Create candidates.
8. Record failures and fallbacks.
9. Feed candidates to Quality Council.
---

## 13. Generation Manager Operating Contract

Generation Manager is the production executor for one approved production recipe. It does not decide what is trendy by itself and does not silently rewrite the creative target. Its job is to translate the approved recipe into concrete generation steps, choose usable tools, create candidates, register every output, and hand candidates to Quality Council.

Inputs:

```text
job_id
format_card_id
trend_scorecard_id
semantic_transfer_plan_id
production_recipe_id
asset_resolution_report_id
quality_profile_id
permission_profile_id
budget_profile_id
tool_registry_snapshot_id
```

Required outputs:

```text
generation_plan.json
generation_steps.jsonl
prompt_packages/
candidate_manifest.json
asset_manifest_updates.jsonl
tool_gap_report.json
failure_report.json
handoff_to_quality.json
```

Generation Manager must be deterministic enough to resume. If the process stops midway, it should reload the job state and continue from the last completed step instead of regenerating everything blindly.

---

## 14. Route Planner Decision Order

RoutePlanner chooses a production route in this order:

```text
1. Load production recipe and semantic transfer target.
2. Identify required output form: short video, long video, image sequence, edit, MMD/3D, hybrid.
3. Identify hard constraints: duration, ratio, character count, dialogue, dance, music sync, scene count, platform constraints.
4. Load available assets and missing asset notes from Asset Resolver.
5. Load tool registry snapshot and remove tools blocked by permission, setup, or cost.
6. Score possible routes.
7. Pick primary route.
8. Pick backup route.
9. Pick lowest-cost diagnostic route if the job is uncertain.
10. Write route decision with reasons.
```

Route scores should include:

```text
creative_fit
format_fidelity
semantic_transfer_fit
asset_readiness
tool_readiness
expected_quality
expected_cost
expected_speed
retry_flexibility
known_failure_risk
```

The selected route must always include a fallback. If no fallback exists, Generation Manager should mark the job as fragile and require higher review before expensive generation.

---

## 15. Route Profiles

Each route profile defines what must exist before generation starts.

```json
{
  "route_id": "character_reenactment_image_to_video",
  "route_type": "character_reenactment",
  "required_assets": ["character_reference", "style_reference"],
  "optional_assets": ["voice_reference", "music_reference", "background_reference"],
  "required_tools": ["image_generation", "image_to_video", "video_editing"],
  "optional_tools": ["tts", "subtitle_rendering"],
  "best_for": ["short reaction", "role transfer", "meme reenactment"],
  "weak_for": ["long continuous dialogue", "precise choreography"],
  "default_candidate_count": 3,
  "default_retry_limit": 2
}
```

Initial route profiles:

```text
plain_text_to_video
reference_image_to_video
reference_video_reenactment
multi_shot_ai_edit
character_reenactment_image_to_video
style_transfer_video_to_video
music_sync_edit
short_drama_scene_split
horror_atmosphere_scene_split
meme_caption_edit
mmd_3d_assisted_route
longform_segmented_route
manual_asset_assisted_route
```

MMD/3D is just one route profile. It should be selected when the format requires repeatable character motion, dance, model-based staging, or camera control that ordinary AI video tools cannot handle well.

---

## 16. Generation Plan Schema

```json
{
  "generation_plan_id": "genplan_000001",
  "job_id": "job_000001",
  "primary_route": "character_reenactment_image_to_video",
  "backup_route": "multi_shot_ai_edit",
  "diagnostic_route": "single_keyframe_test",
  "target_output": {
    "duration_policy": "fit_format",
    "aspect_ratio": "9:16",
    "platforms": ["bilibili", "douyin"],
    "language": "zh-CN"
  },
  "steps": [],
  "candidate_strategy": {},
  "budget_guard": {},
  "permission_checks": [],
  "known_risks": [],
  "created_at": "..."
}
```

The duration field must not force fixed buckets like 8, 15, or 30 seconds. It should store `fit_format` by default and derive actual duration from the source format, script, music, platform constraints, and route capability.

---

## 17. Prompt Build Order

PromptBuilder should build prompts from structured context instead of one giant free-form paragraph.

Order:

```text
1. Production intent
2. Format structure to preserve
3. Semantic transfer target
4. Character/style requirements
5. Scene action
6. Camera and composition
7. Timing and motion
8. Audio/subtitle requirements if relevant
9. Tool-specific syntax
10. Negative constraints
11. Provenance note and prompt version
```

Prompt packages should include both machine prompts and human-readable summaries.

```text
prompt_package/
  positive_prompt.txt
  negative_prompt.txt
  prompt_context.json
  tool_parameters.json
  human_summary.md
  source_links.json
```

No prompt package should hide source material. If a generated output is based on a trending video, reference image, official asset, local trained voice, or user-provided material, the link must be preserved in `source_links.json`.

---

## 18. Batch and Candidate Policy

Candidate count should be adaptive.

Default policy:

```text
low_cost_scene: 2 candidates
normal_scene: 3 candidates
key_scene: 4 candidates
high_cost_scene: 1 diagnostic candidate first
fragile_route: 1 diagnostic candidate, then expand only after QA passes
```

Candidate diversity should be intentional. For the same scene, candidates should vary one or two controlled factors only:

```text
camera framing
motion strength
expression intensity
subtitle style
background style
cut rhythm
voice take
```

Generation Manager should avoid making many nearly identical outputs. Candidate manifests must record what changed between candidates.

---

## 19. Tool Gap and Setup Items

When a needed tool is unavailable, Generation Manager writes a setup item instead of treating the whole project as impossible.

```json
{
  "setup_item_id": "setup_000001",
  "missing_capability": "voice_training",
  "needed_for": "character_voice_reenactment",
  "blocking_level": "route_blocking | quality_limiting | optional_upgrade",
  "suggested_tools": ["local_voice_training_tool", "cloud_tts_provider"],
  "user_action_needed": "install local tool or provide API key",
  "fallback_available": true,
  "fallback_route": "subtitle_only_version"
}
```

Tool gaps are important planning outputs. They tell the user what accounts, APIs, local installs, or training materials are needed.

---

## 20. Generation Failure Triage

FailureHandler classifies failures into four action groups:

```text
retry_same_tool:
  transient API error, timeout, minor bad output.

adjust_prompt:
  prompt rejection, bad motion, weak expression, wrong style.

switch_tool_or_route:
  tool capability gap, repeated bad output, poor consistency.

ask_user_or_setup:
  missing account, missing API key, missing local asset, expensive route approval.
```

Repeated failure rule:

```text
same step fails 2 times with same cause -> ask Revision Engine for change
same route fails 3 times on key requirement -> route downgrade or switch
same tool fails across 3 jobs -> mark tool health degraded
```

Every failure should be visible in the job detail page and connected to Quality Council failure tags when the failure is output-quality related.

---

## 21. Output Registration Contract

Every generated file becomes an asset record.

```json
{
  "asset_id": "asset_gen_000001",
  "asset_origin": "generated",
  "generated_by_step_id": "gen_step_000001",
  "tool_id": "kling_image_to_video",
  "prompt_package_id": "prompt_pkg_000001",
  "source_asset_ids": ["asset_ref_000001"],
  "usage": ["candidate_video"],
  "job_id": "job_000001",
  "review_status": "pending_quality",
  "path": "..."
}
```

Generated assets must stay separate from research downloads and local user assets. They can be reused only if their source chain and quality status allow it.

---

## 22. Handoff to Quality Council

Generation Manager hands off only registered candidates.

```json
{
  "handoff_id": "qa_handoff_000001",
  "job_id": "job_000001",
  "candidate_ids": ["candidate_001", "candidate_002"],
  "route_id": "character_reenactment_image_to_video",
  "quality_profile_id": "qa_profile_short_reenactment",
  "must_check": [
    "format_fidelity",
    "semantic_transfer",
    "character_consistency",
    "visual_artifacts",
    "audio_sync",
    "subtitle_readability"
  ],
  "known_risks": [],
  "retry_budget_remaining": 2
}
```

Quality Council can request retry, route change, prompt adjustment, asset replacement, or human review. Generation Manager executes those requests but must write a new generation plan version when the route changes.

---

## 23. Implementation Notes for Phase 0

Phase 0 should implement a narrow but real generation path:

```text
approved source/format -> semantic transfer target -> route plan -> prompt package -> external/manual generation slot -> candidate registration -> QA handoff
```

If automated AI video APIs are not configured yet, Phase 0 can still be real by supporting `manual_generation_slot`:

```text
Kairove writes exact prompts, assets, parameters, and expected output slots.
User runs the external tool manually.
User drops output into the slot.
Kairove registers the output and continues QA, retry, package, and publish planning.
```

This keeps Phase 0 as a lowest complete production chain without pretending all APIs already exist.

---

## Cross-Phase Policy Alignment - 2026-06-06

Generation tool policy:

```text
Use Tool Registry; do not lock one specific generation tool.
Allowed categories: text-to-video, image-to-video, video-to-video, image generation, TTS/voice, editing, subtitles, covers, inpainting/repair, MMD/Blender/3D tools.
Missing API/key/account/local install creates ToolSetupItem.
```

Forbidden behavior:

```text
black-box high-cost batch runs
untraceable outputs
outputs that cannot export files/metadata
obvious platform/account rule violations
```

Budget:

```text
Low-cost generation is a capability switch first.
Future budgets should support daily, per-job, per-run, and high-cost-threshold layers.
P0-B does not require real paid APIs.
High-cost routes ask before each round.
```
