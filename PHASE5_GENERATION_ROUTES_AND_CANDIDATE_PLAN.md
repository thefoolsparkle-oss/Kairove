# Kairove Phase 5: Generation Routes, Tool Registry, and Candidate Generation Plan

## 0. Status

Current status:

```text
Phase 5: detailed planning draft, not yet confirmed for implementation
Depends on: P3 ProductionRecipeDraft and P4 AssetResolutionReport
Primary output: registered candidates and generation records for P6 Quality Council
Related capability doc: GENERATION_AND_TOOL_REGISTRY_PLAN.md
```

---

## 1. Purpose

Phase 5 turns a resolved production plan into actual candidate outputs.

It answers:

```text
Which route should produce this video, which tools or manual slots should be used, what prompts/parameters are needed, what candidates were created, and how are all outputs traced?
```

Phase 5 is where automatic APIs, local tools, browser/manual slots, and fallback routes meet the production plan.

---

## 2. One-Line Scope

```text
ProductionRecipeDraft + AssetResolutionReport + ToolRegistry -> GenerationPlan + PromptPackages + GenerationSteps + CandidateManifest
```

---

## 3. Must Include

```text
Tool Registry Snapshot:
  Know what tools are available, missing, not configured, or unsuitable.

Route Selection:
  Choose primary, backup, and diagnostic routes based on creative fit, asset readiness, tool readiness, cost, and risk.

Prompt Package Building:
  Build structured prompts and parameters for each tool or manual slot.

Manual Slot Support:
  If automation is missing, write exact instructions and import slots rather than faking API output.

Candidate Generation / Import:
  Register every output file, generated asset, generation step, prompt, input asset, and failure.

Fallback Handling:
  Switch tool/route or reduce complexity when needed.

Handoff to QA:
  Send only registered candidates to P6.
```

---

## 4. Must Not Include

```text
trend selection
creative rewrite without P3/P6 request
asset policy override
untracked generated files
fake tool calls
silent paid generation
final QA approval
publishing
learning rule changes
```

---

## 5. Inputs

```text
ProductionRecipeDraft
AssetResolutionReport
resolved AssetManifests
GeneratedAssetPlans
Tool registry snapshot
Permission profile
Budget profile
QualityExpectationDraft
UserPreference
previous ToolPerformanceRecords
```

Optional:

```text
manual external tool output
user-provided candidate files
API credentials if configured
local service status
```

---

## 6. Outputs

```text
GenerationPlan
ToolSelectionReport
RouteDecisionReport
PromptPackages
ManualGenerationSlots
GenerationSteps
GeneratedAssets
CandidateManifest
FailureReport
ToolSetupItems
HandoffToQuality
DecisionLogs
Phase5GenerationReport
```

---

## 7. Workstreams

```text
P5-A Tool Registry and Capability Snapshot
P5-B Route Planner
P5-C Permission and Budget Gate
P5-D Prompt Package Builder
P5-E Manual Generation Slot Builder
P5-F Generation Step Executor / Importer
P5-G Candidate Registrar
P5-H Failure and Fallback Planner
P5-I Handoff to Quality Council
P5-J Generation Report and Tests
```

---

## 8. Route Selection Order

```text
1. Load production intent and quality expectations.
2. Read asset readiness and blockers.
3. Identify output form: text-to-video, image-to-video, edit, music sync, MMD/3D, longform segment, hybrid.
4. Remove tools blocked by permission, missing setup, or budget.
5. Score routes.
6. Select primary route.
7. Select backup route.
8. Select diagnostic route for expensive or fragile jobs.
9. Write route decision and reasons.
```

Route score dimensions:

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

---

## 9. Route Profiles

Initial route profiles:

```text
plain_text_to_video
reference_image_to_video
multi_image_to_video
video_to_video_style_transfer
reference_video_reenactment
multi_shot_ai_edit
character_reenactment_image_to_video
music_sync_edit
short_drama_scene_split
horror_atmosphere_scene_split
abstract_meme_caption_edit
manual_asset_assisted_route
mmd_3d_assisted_route
longform_segmented_route
hybrid_pipeline
```

Route profile schema:

```json
{
  "route_id": "character_reenactment_image_to_video",
  "route_type": "character_reenactment",
  "required_assets": ["character_reference", "style_reference"],
  "optional_assets": ["voice_reference", "music_reference"],
  "required_tools": ["image_generation", "image_to_video", "video_editing"],
  "optional_tools": ["tts", "subtitle_rendering"],
  "best_for": [],
  "weak_for": [],
  "default_candidate_count": 3,
  "default_retry_limit": 2
}
```

MMD/3D and longform are route profiles here, but their specialized implementation is handled in P10/P11.

---

## 10. Tool Registry

Tool status values:

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

Tool card:

```json
{
  "tool_id": "tool_000001",
  "display_name": "...",
  "tool_type": "image_to_video",
  "provider": "...",
  "status": "available | requires_api_key | unknown",
  "supported_inputs": [],
  "outputs": [],
  "supported_ratios": [],
  "strengths": [],
  "weaknesses": [],
  "route_compatibility": {},
  "cost_level": "free | low | medium | high | unknown",
  "speed_level": "fast | medium | slow | unknown"
}
```

Missing tools create ToolSetupItems. They do not block the whole system if a manual or fallback route exists.

---

## 11. GenerationPlan

```json
{
  "generation_plan_id": "genplan_000001",
  "production_recipe_draft_id": "recipe_draft_000001",
  "asset_resolution_report_id": "asset_res_000001",
  "primary_route": "character_reenactment_image_to_video",
  "backup_route": "multi_shot_ai_edit",
  "diagnostic_route": "single_keyframe_test",
  "target_output": {
    "duration_policy": "fit_format",
    "aspect_ratio": "platform_default",
    "platforms": [],
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

Duration must stay `fit_format` by default. Do not force fixed buckets such as 8/15/30 seconds when the source format requires a different length.

---

## 12. Prompt Package Contract

PromptBuilder should assemble prompts from structured context:

```text
production intent
format core to preserve
semantic transfer target
character/style references
scene action
camera/composition
timing/motion
audio/subtitle requirements
tool-specific syntax
negative constraints
provenance and prompt version
```

Prompt package layout:

```text
prompt_package/
  positive_prompt.txt
  negative_prompt.txt
  prompt_context.json
  tool_parameters.json
  human_summary.md
  source_links.json
```

Rules:

```text
prompts must link to source and asset references
negative prompts should target known failure risks
human summary must be understandable enough for manual generation
prompt versions must be tracked
```

---

## 13. Manual Generation Slots

Manual slots are first-class outputs.

Manual slot record:

```json
{
  "manual_slot_id": "manual_slot_000001",
  "generation_plan_id": "genplan_000001",
  "intended_tool": "external_image_to_video_tool",
  "input_assets": [],
  "prompt_package_id": "prompt_pkg_000001",
  "parameters": {},
  "expected_output": "video",
  "drop_folder": "generated_assets/jobs/job_000001/manual_slots/manual_slot_000001/inbox",
  "status": "waiting_for_user | imported | skipped | failed"
}
```

Manual slot rules:

```text
show exactly what user should run externally
show where to place output
imported output becomes generated asset
imported output links to prompt package and slot id
```

---

## 14. Candidate Strategy

Candidate count should be adaptive:

```text
low_cost_scene: 2 candidates
normal_scene: 3 candidates
key_scene: 4 candidates
high_cost_scene: 1 diagnostic candidate first
fragile_route: 1 diagnostic candidate, then expand after QA passes
```

Candidate diversity should vary controlled factors:

```text
camera framing
motion strength
expression intensity
subtitle style
background style
cut rhythm
voice take
```

Avoid generating many near-identical outputs.

---

## 15. GenerationStep and Output Registration

GenerationStep:

```json
{
  "step_id": "gen_step_000001",
  "job_id": "job_000001",
  "candidate_id": "candidate_001",
  "step_type": "image_to_video | text_to_video | tts | edit | subtitle_render | manual_import",
  "tool_id": "tool_000001",
  "input_assets": [],
  "output_assets": [],
  "prompt_package_id": "prompt_pkg_000001",
  "parameters": {},
  "status": "pending | running | success | failed | skipped | retrying",
  "error_message": null
}
```

Every generated file becomes an asset:

```json
{
  "asset_id": "asset_gen_000001",
  "asset_origin": "generated",
  "generated_by_step_id": "gen_step_000001",
  "tool_id": "tool_000001",
  "prompt_package_id": "prompt_pkg_000001",
  "source_asset_ids": [],
  "usage": ["candidate_video"],
  "job_id": "job_000001",
  "review_status": "pending_quality",
  "path": "..."
}
```

---

## 16. CandidateManifest

```json
{
  "candidate_manifest_id": "cand_manifest_000001",
  "job_id": "job_000001",
  "generation_plan_id": "genplan_000001",
  "candidates": [
    {
      "candidate_id": "candidate_001",
      "candidate_type": "video | scene | cover | audio | package",
      "status": "generated | imported | failed | awaiting_qa",
      "output_asset_ids": [],
      "generation_step_ids": [],
      "variation_notes": [],
      "known_risks": []
    }
  ],
  "handoff_to_quality_id": "qa_handoff_000001"
}
```

Candidates without generation steps or import records are invalid.

---

## 17. Failure and Fallback

Failure groups:

```text
retry_same_tool
adjust_prompt
switch_tool_or_route
ask_user_or_setup
abandon_step
```

Repeated failure rules:

```text
same step fails 2 times with same cause -> request prompt/route change
same route fails 3 times on key requirement -> route downgrade or switch
same tool fails across 3 jobs -> mark tool health degraded
```

Fallback examples:

```text
continuous two-character scene fails -> split into reaction shots
text-to-video fails identity -> image reference then image-to-video
dance AI generation fails -> MMD/3D route or beat-synced edit
same AI method unavailable -> try closest available route and report gap
```

---

## 18. Handoff To Quality

```json
{
  "handoff_id": "qa_handoff_000001",
  "job_id": "job_000001",
  "candidate_ids": [],
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

P6 should reject unregistered candidates.

---

## 19. Storage Layout

```text
generated_assets/jobs/job_000001/generation/
  generation_plan.json
  route_decision_report.json
  tool_selection_report.json
  prompt_packages/
  manual_slots/
  generation_steps.jsonl
  candidate_manifest.json
  failures/
  handoff_to_quality.json
```

Generated assets stay under `generated_assets`; research downloads and local assets remain separate.

---

## 20. Tests

Fixture groups:

```text
automated tool available
missing API key but manual slot possible
route with backup available
route with no fallback
manual import candidate
prompt rejection
repeated tool failure
same AI method unavailable
```

Required tests:

```text
loads ProductionRecipeDraft and AssetResolutionReport
creates GenerationPlan
selects primary/backup/diagnostic routes
creates prompt package
creates manual slot when tool missing
imports manual output
registers generated asset
writes GenerationStep
writes CandidateManifest
creates ToolSetupItem for missing tool
hands off registered candidates to P6
never fakes tool output
```

---

## 21. Acceptance Criteria

P5 is ready when Kairove can:

```text
snapshot tool capabilities
select route and fallback
build prompt packages
create manual slots
execute or import generation steps
register generated assets
register candidates
record failures and fallback decisions
handoff candidates to P6
pass fixture-based tests
```

---

## 22. Non-Acceptance

P5 is not acceptable if:

```text
it pretends unavailable tools worked
it generates files without manifests
it creates candidates without generation steps
it silently spends money
it changes creative target without logged upstream request
it sends unregistered outputs to QA
it mixes generated assets with local or research assets
```

---

## 23. Confirmation Checklist

Before P5 implementation, confirm or revise:

```text
initial tool registry fields
manual slot behavior
default candidate count policy
paid generation permission thresholds
first supported automated tools
fallback route priorities
```

---

## Cross-Phase Policy Alignment - 2026-06-06

P5 generation must remain tool-registry based:

```text
Do not lock one specific generation tool.
Allowed tool categories:
  text-to-video
  image-to-video
  video-to-video
  image generation
  TTS/voice
  editing
  subtitles
  covers
  inpainting/repair
  MMD/Blender/3D tools

Missing API/key/account/local install:
  create ToolSetupItem.
```

Forbidden tool behavior:

```text
black-box high-cost batch runs
untraceable outputs
outputs that cannot export files/metadata
obvious platform/account rule violations
```

Budget policy:

```text
Low-cost generation is a capability switch first, not a fixed number in P0-B.
Future budgets should support daily, per-job, per-run, and high-cost-threshold layers.
High-cost routes ask before each round.
```
