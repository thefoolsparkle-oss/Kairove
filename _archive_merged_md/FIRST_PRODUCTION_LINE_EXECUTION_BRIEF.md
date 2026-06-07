# Kairove First Production Line Execution Brief

## 0. Status

This is a capability execution brief, not a confirmed numbered phase.

Current status:

```text
Route: ordinary AI format reproduction video line
Execution brief: drafted
Implementation: not started
Global phase number: not assigned
```

Purpose:

```text
Define how Kairove's first complete production line should eventually connect discovery, format mining, planning, asset resolution, generation, QA, packaging, publishing, and learning.
```

This is not an MVP plan.

It describes the first usable route Kairove should eventually support.

---

## 1. Route Identity

Route ID:

```text
route_ordinary_ai_format_video
```

Route meaning:

```text
Take a real external video format or trend, extract its reusable structure, semantically transfer it into a new context, generate ordinary AI video candidates, quality-check them, package them for platforms, and learn from feedback.
```

This route is not MMD/3D-specific.

MMD/3D can later become one production route among many.

---

## 2. Route Input Types

Supported future inputs:

```text
auto_trend_patrol
keyword_search
manual_seed_link
character_or_fandom_target
audio_or_music_target
user_selected_format
```

Examples:

```text
Find currently hot AI short video formats.
Find abstract short-drama formats.
Take this couple skit and make an anime/game CP version.
Use this hot audio structure with different characters.
Find horror short formats that can be made with available tools.
```

---

## 3. Route Outputs

Final route outputs:

```text
final_video
cover
title
description
tags
platform payloads
publish package
quality report
source/asset provenance
publish records
feedback records
learning update
```

Intermediate outputs:

```text
ResearchReviewReport
FormatCard
FormatGenome
TrendScorecard
ReproductionPlan
AssetRequirementList
AssetResolutionReport
ProductionRecipe
GenerationSteps
CandidateVideos
QualityReports
RetryPlans
PublishPackage
```

---

## 4. Route Pipeline

Full intended pipeline:

```text
1. Run Intake
2. Source Scout
3. Harvester
4. Video Understanding
5. Format Miner
6. Trend Analyst
7. Regent Gate 1: Format Selection
8. Job Creation
9. Format Reproduction Council
10. Semantic Format Transfer
11. Route Selector
12. Asset Requirement Planning
13. Asset Resolver
14. Regent Gate 2: Production Feasibility
15. Production Recipe Builder
16. Generation Manager
17. Candidate Assembly
18. Quality Council
19. Revision and Retry
20. Final Judge
21. Packaging Council
22. Publish Council
23. Publisher Integrations or Manual Publish Package
24. Feedback Collection
25. Learning Memory Update
```

This is an execution route, not a phase list.

---

## 5. Gate Overview

The route should have explicit gates.

```text
Gate 1: Is this format worth making?
Gate 2: Can Kairove produce it with current tools/assets?
Gate 3: Are generated candidates good enough?
Gate 4: Is the publish package acceptable?
Gate 5: What did feedback teach Kairove?
```

Every gate writes a DecisionLog.

If a gate cannot decide, it creates a ReviewItem.

---

## 6. Gate 1: Format Selection

Inputs:

- FormatCard;
- FormatGenome;
- TrendScorecard;
- source evidence;
- user preferences;
- available route profiles;
- policy constraints.

Decision values:

```text
make_now
observe
collect_more
reject
ask_user
```

Gate 1 should select a format only if:

- evidence is strong enough;
- trend score is good enough or user explicitly wants it;
- format has a plausible transfer route;
- source/asset policy does not block planning;
- Kairove can explain why it is choosing this format.

Gate 1 must show:

- final score;
- score weights;
- heat vs fatigue explanation;
- confidence;
- source examples;
- recommended production route.

---

## 7. Job Creation

Once Gate 1 selects a format, Kairove creates a Job.

Minimum job package:

```text
generated_assets/jobs/job_000001/
  job_config.json
  decision_log.jsonl
  source_refs.json
  format_card.json
  format_genome.json
  trend_scorecard.json
  reproduction_plan.json
  asset_requirements.json
  production_recipe.json
  candidates/
  quality/
  final/
  publish_package/
  feedback/
```

Job creation does not mean generation has started.

It means Kairove has committed to planning one production attempt.

---

## 8. Format Reproduction Council

Purpose:

```text
Turn FormatCard and FormatGenome into a concrete reproduction strategy.
```

It should decide:

- what must be preserved;
- what can be changed;
- what target context to use;
- which characters or roles fit;
- whether the result should be short drama, meme, horror, music sync, character reenactment, or hybrid;
- which elements are risky or likely to fail.

Outputs:

```text
ReproductionPlan
semantic_transfer_notes
route_candidate_list
risk_notes
review_items_if_needed
```

---

## 9. Semantic Format Transfer

Semantic transfer means preserving the reusable structure while changing surface content.

Example:

```text
真人情侣嘴硬短剧
-> 二游/动漫 CP 角色版本
```

Transfer should preserve:

- relationship logic;
- joke or reveal structure;
- emotional beat order;
- timing and escalation;
- audience-recognizable hook.

Transfer can change:

- characters;
- world/background;
- art style;
- spoken lines;
- props;
- visual route;
- platform packaging.

Transfer should fail or ask user if:

- the new characters do not fit the relationship logic;
- the format depends on real-person context that cannot transfer;
- the source format is too weak;
- required audio/voice/material is unavailable;
- production tools cannot express the core beat.

---

## 10. Route Selector

Route Selector chooses a production route.

Possible routes:

```text
scripted_ai_video
image_to_video_sequence
text_to_video_sequence
character_reenactment
music_sync_short
horror_atmosphere_short
abstract_short_drama
hybrid_edit
manual_assisted
```

MMD/3D is not the default route here.

Route selection uses:

- FormatGenome;
- available tools;
- required assets;
- target style;
- difficulty;
- cost/budget;
- expected QA risks;
- user preferences.

Output:

```json
{
  "selected_route": "character_reenactment",
  "backup_routes": ["scripted_ai_video", "hybrid_edit"],
  "selection_reason": "...",
  "known_risks": [],
  "tool_gaps": []
}
```

---

## 11. Asset Requirement Planning

Before resolving assets, Kairove should describe what it needs.

Asset requirements can include:

- character reference images;
- official art or wiki references;
- style references;
- background references;
- music/audio references;
- SFX;
- voice model or voice material;
- subtitle/caption style;
- cover style;
- platform-specific package assets.

Output:

```json
{
  "asset_requirement_id": "asset_req_000001",
  "job_id": "job_000001",
  "requirements": [
    {
      "requirement_id": "req_000001",
      "asset_type": "character_reference",
      "target": "character_a",
      "required": true,
      "preferred_source_type": ["official", "wiki"],
      "usage_policy_needed": "direct_use | reference_only | style_analysis",
      "fallback": "ask_user"
    }
  ]
}
```

---

## 12. Asset Resolver

Asset Resolver attempts to satisfy requirements.

Resolution order:

```text
1. existing local assets
2. user-curated official assets
3. official/wiki/web references
4. platform source material if allowed
5. generated assets
6. ask user
```

It must keep folders separate:

```text
research_assets
local_assets
generated_assets
```

It must mark:

- source;
- usage policy;
- review status;
- used_for;
- local path;
- missing items;
- fallback plan.

If it cannot resolve something, it creates ReviewItem or ToolSetupItem.

---

## 13. Gate 2: Production Feasibility

Before generation, Regent checks whether the job is feasible.

Inputs:

- ReproductionPlan;
- selected route;
- asset resolution report;
- tool capability registry;
- permissions;
- budget;
- known QA risks.

Decision values:

```text
proceed
proceed_with_warnings
ask_user
collect_assets
change_route
abandon
```

Gate 2 should block or ask user when:

- required asset is missing;
- permission is ask/deny;
- high-cost generation needs approval;
- selected tool is unavailable;
- source policy is unresolved;
- likely output cannot preserve the core format.

---

## 14. Production Recipe

A `ProductionRecipe` turns plan into ordered generation/editing steps.

Minimum fields:

```json
{
  "recipe_id": "recipe_000001",
  "job_id": "job_000001",
  "route": "character_reenactment",
  "steps": [
    {
      "step_id": "step_01",
      "step_type": "prompt_generation | image_generation | video_generation | audio_generation | edit | upscale | subtitle | package",
      "tool_id": "...",
      "inputs": [],
      "outputs_expected": [],
      "permission_required": [],
      "fallback_steps": []
    }
  ],
  "qa_checkpoints": [],
  "created_at": "..."
}
```

Recipe should preserve traceability from source format to final candidate.

---

## 15. Generation Manager

Generation Manager executes recipe steps later.

This route brief does not define every tool call.

It requires Generation Manager to record:

- model/tool used;
- parameters;
- prompts;
- input assets;
- output files;
- cost estimate if available;
- errors;
- retry lineage.

Outputs:

```text
GenerationStep records
Candidate files
Prompt files
Tool logs
```

---

## 16. Candidate Assembly

A candidate video may be built from multiple generated parts.

Candidate metadata should include:

```json
{
  "candidate_id": "cand_000001",
  "job_id": "job_000001",
  "recipe_id": "recipe_000001",
  "generation_steps": [],
  "video_path": "...",
  "duration_seconds": null,
  "resolution": null,
  "fps": null,
  "source_format_id": "fmt_000001",
  "candidate_notes": "..."
}
```

P0/P1 do not create candidates. This is future route behavior.

---

## 17. Quality Council

Quality Council checks candidates.

Required QA layers:

```text
Technical QA
Visual QA
Semantic QA
Specialist QA where relevant
Strong Judge / final judge
```

Technical QA can check simple facts:

- resolution;
- fps;
- duration;
- file validity;
- audio presence;
- aspect ratio.

Semantic QA checks whether the candidate preserved the format:

- correct beat order;
- correct role logic;
- target characters fit;
- joke/reveal still works;
- no obvious AI drift;
- no major missing element.

Semantic QA should use multiple agent levels when needed.

---

## 18. Revision and Retry

Retry should be targeted, not blind.

RetryPlan fields:

```json
{
  "retry_plan_id": "retry_000001",
  "candidate_id": "cand_000001",
  "failure_tags": [],
  "preserve_steps": [],
  "redo_steps": [],
  "changed_prompts": [],
  "reason": "...",
  "max_retry_rounds": 0
}
```

Failure tags examples:

```text
identity_drift
format_structure_lost
audio_sync_failed
subtitle_bad
visual_artifact
wrong_relationship_logic
too_ai_generic
tool_failure
missing_asset
```

---

## 19. Final Judge

Final Judge decides:

```text
select
retry
reject
ask_user
```

It should consider:

- QA reports;
- trend score;
- reproduction success;
- publish suitability;
- user preferences;
- cost and retry history.

No video should be marked final without a final report.

---

## 20. Packaging Council

Packaging Council prepares:

- title;
- description;
- tags;
- cover;
- platform-specific payloads;
- publish notes;
- unsuitable-platform flags.

Default platform strategy:

```text
Prepare for all configured platforms unless a platform is blocked, unsuitable, or missing required tooling/package data.
```

Packaging must use:

- FormatCard;
- TrendScorecard;
- ReproductionPlan;
- QualityReport;
- platform profile;
- user preferences.

---

## 21. Publish Council

Publish Council decides whether to:

```text
create_manual_package
upload_draft
schedule_publish
auto_publish
ask_user
skip_platform
```

Auto-publish requires explicit permission and platform setup.

If API/browser publisher is missing, create ToolSetupItem and still create manual package if possible.

---

## 22. Feedback and Learning

After publishing or manual review, Kairove should collect:

- platform metrics;
- comments;
- user rating;
- quality outcomes;
- publish result;
- failed tool route notes.

Learning updates can be:

```text
observation
suggestion
approved_rule
```

No core score weight, permission, or source policy changes silently.

---

## 23. Required Reports

Per job reports:

```text
job_summary.md
format_selection_report.md
reproduction_plan.md
asset_resolution_report.md
generation_report.md
quality_report.md
retry_report.md
publish_package_report.md
feedback_report.md
learning_update.md
```

A user should be able to inspect why the job happened and how the final output was made.

---

## 24. Non-Goals

This brief does not schedule implementation.

It does not implement:

- crawling;
- generation;
- QA agents;
- publishing;
- MMD/3D;
- longform;
- UI.

It defines the intended route shape for the first complete usable production line.

---

## 25. Acceptance Criteria

The route is fully usable only when Kairove can:

1. discover or accept a source format;
2. harvest and understand evidence;
3. mine a FormatCard and FormatGenome;
4. score the trend with visible weights;
5. choose a format through Gate 1;
6. create a Job;
7. make a ReproductionPlan;
8. perform semantic transfer;
9. select a production route;
10. resolve assets with provenance;
11. pass Gate 2 feasibility;
12. build and execute a ProductionRecipe;
13. generate multiple candidates;
14. perform multi-layer QA;
15. create targeted RetryPlans;
16. select or reject final output;
17. package title/description/tags/cover;
18. publish or create manual publish package;
19. collect feedback;
20. write learning updates.

This is the future complete route target, not a current phase acceptance list.

---

## 26. Ready-To-Schedule Questions

Before this route is scheduled into implementation phases, decide:

- which capability comes immediately after P1;
- whether Format Miner and Trend Analyst are implemented before any generation;
- what minimal generation route is acceptable for the first complete route;
- which platforms are required for first publishing support;
- whether manual publishing package is enough before platform automation;
- how much UI is needed before the route becomes usable;
- how many QA layers are required before first public posting.