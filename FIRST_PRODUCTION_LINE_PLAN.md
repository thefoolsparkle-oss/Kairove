# Kairove First Production Line Plan

## 0. Purpose

This document defines Kairove's first usable production line:

```text
route_ordinary_ai_format_video
普通 AI 格式复现视频线
```

This is not a toy MVP. It is the first complete production route that should eventually produce usable AI videos from real trends.

It focuses on:

- discovering hot video formats;
- extracting reusable format structure;
- reproducing the format through semantic transfer;
- generating ordinary AI videos;
- quality checking;
- retrying;
- packaging;
- publishing;
- learning from feedback.

It does not prioritize MMD / VRM / 3D in the first route. Those will be handled later as specialized production routes.

---

## 1. Route Definition

Route ID:

```text
route_ordinary_ai_format_video
```

Human name:

```text
普通 AI 格式复现视频线
```

Primary goal:

```text
Turn a trending video format into a new AI-generated version using available tools and assets.
```

Typical outputs:

- short AI video;
- AI short drama;
- meme video;
- horror atmosphere short;
- character reenactment;
- music / sound meme adaptation;
- AI visual style imitation;
- multi-shot edited short video.

Not first-priority:

- complex MMD dance;
- complex 3D motion;
- long continuous character performance;
- high-complexity multi-person continuous scenes;
- multi-hour longform.

---

## 2. Supported Input Modes

### 2.1 Auto Scout

User intent:

```text
Find currently hot ordinary AI video formats and produce the best candidates.
```

Inputs:

```json
{
  "mode": "auto_scout",
  "platforms": ["bilibili", "douyin", "xiaohongshu", "youtube"],
  "topics": [],
  "video_categories": ["ai_video", "meme", "horror", "character_reenactment"],
  "max_formats_to_plan": 3
}
```

### 2.2 Keyword Search

User intent:

```text
Find trends around a specific keyword or category.
```

Example:

```text
找最近抽象短剧方向
```

Inputs:

```json
{
  "mode": "keyword",
  "keywords": ["抽象短剧"],
  "platforms": ["bilibili", "douyin"]
}
```

### 2.3 Source Link

User intent:

```text
Analyze this video and make a new version.
```

Inputs:

```json
{
  "mode": "source_link",
  "urls": ["..."],
  "target_style": "anime_game_character_version"
}
```

### 2.4 Character / Fandom Target

User intent:

```text
Find formats suitable for specific characters or fandoms.
```

Inputs:

```json
{
  "mode": "character_target",
  "characters": ["char_000001", "char_000002"],
  "world": "world_000001",
  "preferred_formats": ["dialogue_meme", "music_sync", "horror"]
}
```

### 2.5 Audio / Music Target

User intent:

```text
Find or produce videos using a specific song, audio, or sound meme.
```

Inputs:

```json
{
  "mode": "audio_target",
  "audio_ref": "audio_ref_000001",
  "platforms": ["douyin", "bilibili"]
}
```

---

## 3. Full Pipeline

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
12. Specialized Councils
13. Asset Resolver
14. Regent Gate 2: Production Feasibility
15. Generation Manager
16. Quality Council
17. Revision & Retry
18. Final Judge
19. Packaging Council
20. Publish Council
21. Publisher Integrations
22. Feedback Collection
23. Learning Memory Update
```

---

## 4. Step Details

## 4.1 Run Intake

Purpose:

Create a `Run` and normalize the user's intent.

Inputs:

- user message;
- schedule trigger;
- manual link;
- keyword;
- character target;
- audio target.

Outputs:

- `run_id`
- normalized run config;
- permission snapshot;
- decision log entry.

Artifacts:

```text
data/runs/run_000001.json
logs/run_000001.log
```

Failure cases:

- unclear intent;
- missing required target;
- permission denied for requested action.

If unclear but low risk, Regent can create a planning run and ask later.

---

## 4.2 Source Scout

Purpose:

Find candidate sources.

Agents:

- `QueryPlanner`
- platform scouts;
- `CandidateNormalizer`
- `CandidateDeduplicator`
- `InitialRelevanceRanker`
- `ScoutReporter`

Outputs:

- `candidate_sources.json`
- source candidate rows in database.

Artifacts:

```text
research_assets/manifests/candidate_sources_run_000001.json
```

Failure cases:

- platform access blocked;
- API missing;
- no results;
- too many noisy results.

Fallbacks:

- use search engine;
- switch platform;
- ask user for seed links;
- metadata-only scouting.

---

## 4.3 Harvester

Purpose:

Save evidence and create source manifests.

Outputs:

- `Source` records;
- `Asset` records;
- raw files or metadata;
- source manifests.

Artifacts:

```text
research_assets/raw_pages/
research_assets/raw_videos/
research_assets/screenshots/
research_assets/comments/
research_assets/transcripts/
research_assets/manifests/
```

Policy:

- official sources can be direct-use by default;
- personal creator / unknown sources need review before final direct use;
- all sources need provenance.

Failure cases:

- download failed;
- login required;
- rate limit;
- comments unavailable;
- video unavailable.

Fallbacks:

- save metadata only;
- save screenshots;
- browser-assisted capture;
- create tool setup review item.

---

## 4.4 Video Understanding

Purpose:

Convert sources into understanding reports.

Inputs:

- source manifests;
- raw video or screenshots;
- title/description/comments;
- audio reference.

Outputs:

- `understanding_report.json`

Report includes:

- text summary;
- visual style;
- audio role;
- story beats;
- relationship pattern;
- format clues;
- AI tool clues;
- confidence and evidence.

Artifacts:

```text
research_assets/understanding/src_000001_understanding.json
```

Failure cases:

- no video file;
- ASR unavailable;
- OCR unavailable;
- comments unavailable;
- visual model unavailable.

Fallbacks:

- metadata-only understanding;
- screenshot-only understanding;
- user-provided transcript;
- run later after tool setup.

---

## 4.5 Format Miner

Purpose:

Find reusable formats from one or more understanding reports.

Inputs:

- understanding reports;
- existing format knowledge;
- source clusters.

Outputs:

- `format_card`
- `format_genome`
- `format_observations`

Artifacts:

```text
knowledge_base/formats/format_cards/fmt_000001.json
knowledge_base/formats/format_genomes/fmt_000001.json
```

Failure cases:

- only one weak source;
- no clear format;
- format too broad;
- format looks like old variant.

Fallbacks:

- mark as observation-only;
- watchlist instead of production;
- ask user if manual link is important.

---

## 4.6 Trend Analyst

Purpose:

Score whether the format is worth producing.

Inputs:

- format card;
- observations;
- metrics;
- comments;
- lifecycle data;
- tool feasibility notes.

Outputs:

- `trend_scorecard.json`
- decision suggestion.

Scoring:

Positive:

- heat;
- velocity;
- engagement quality;
- remixability;
- format strength;
- production feasibility;
- freshness.

Penalties:

- fatigue;
- risk;
- tool gap;
- complexity.

Artifacts:

```text
knowledge_base/scoring/trend_scorecards/trend_score_000001.json
```

Failure cases:

- insufficient metrics;
- platform metrics unavailable;
- comment sentiment unclear.

Fallbacks:

- use confidence penalty;
- ask user;
- observe instead of production.

---

## 4.7 Regent Gate 1: Format Selection

Purpose:

Decide whether to create a job.

Inputs:

- trend scorecard;
- permission matrix;
- risk notes;
- user preferences;
- current budget.

Possible decisions:

```text
create_job
observe
reject
ask_user
wait_for_more_data
```

Writes:

- decision log;
- review item if needed.

---

## 4.8 Job Creation

Purpose:

Create a `Job` and job directory.

Outputs:

```text
generated_assets/jobs/job_000001/
  job_config.json
  decision_log.json
  source_refs.json
  format_card.json
  trend_scorecard.json
```

Job status:

```text
created -> planning
```

---

## 4.9 Format Reproduction Council

Purpose:

Decide what to reproduce.

Outputs:

- `reproduction_plan.json`

Must define:

- primary reproduction target;
- must preserve;
- should preserve;
- optional;
- avoid;
- adaptation strategy;
- needed target world or characters;
- human review needs.

Failure cases:

- source format unclear;
- reproduction would require unavailable tools;
- too high risk;
- no meaningful adaptation.

Fallbacks:

- observe format;
- ask user;
- choose weaker adaptation;
- route to another council.

---

## 4.10 Semantic Format Transfer

Purpose:

Map source roles, relationships, scenes, and emotional functions to a target world or character set.

Examples:

```text
real couple teasing dialogue
  -> anime/game CP teasing dynamic
```

Outputs:

- semantic transfer section in reproduction plan;
- relationship mapping;
- world adaptation;
- OOC or fandom risk notes.

Failure cases:

- no target character knowledge;
- CP mapping uncertain;
- high OOC risk;
- target world lacks equivalent scene.

Fallbacks:

- use original-like generic characters;
- ask user to choose characters;
- create character research task;
- skip character transfer.

---

## 4.11 Route Selector

Purpose:

Choose production route combination.

Outputs:

```json
{
  "primary_route": "character_reenactment_council",
  "supporting_routes": ["script_council", "meme_edit_council"],
  "route_conflicts": [],
  "reason": "format depends on character relationship and dialogue punchline"
}
```

Failure cases:

- multiple routes conflict;
- no feasible route;
- tool gap.

Fallbacks:

- choose hybrid route;
- simplify production goal;
- create tool setup request.

---

## 4.12 Specialized Councils

Purpose:

Produce route-specific plans.

Possible councils:

- Script Council;
- Music Sync Council;
- Character Reenactment Council;
- Visual Style Council;
- Horror Atmosphere Council;
- Meme Edit Council;
- AI Tool Imitation Council.

Outputs:

- `councils/<council_name>/plan.json`
- needed assets;
- recommended tools;
- quality checks needed.

Failure cases:

- plan too complex;
- style unclear;
- script weak;
- audio timing missing;
- character behavior uncertain.

Fallbacks:

- create alternatives;
- ask user;
- simplify route.

---

## 4.13 Asset Resolver

Purpose:

Find or create required assets.

Search order:

1. local assets;
2. research assets;
3. official web sources;
4. broader web references;
5. generated alternatives;
6. human task.

Outputs:

- `resolved_assets.json`
- asset manifests;
- review items for uncertain assets.

Artifacts:

```text
generated_assets/jobs/job_000001/assets/resolved_assets.json
```

Failure cases:

- missing character reference;
- missing voice;
- missing music;
- ambiguous source;
- source needs review.

Fallbacks:

- generate substitute;
- use official source;
- ask user;
- mark as blocking.

---

## 4.14 Regent Gate 2: Production Feasibility

Purpose:

Before spending generation cost, confirm feasibility.

Checks:

- required assets resolved;
- tool route available;
- budget allowed;
- risk policy satisfied;
- user review items resolved if blocking.

Decisions:

```text
proceed_generation
ask_user
change_route
wait_for_asset
abandon
```

---

## 4.15 Generation Manager

Purpose:

Generate assets and candidates.

Outputs:

- generated images;
- generated video clips;
- generated audio;
- subtitles;
- edited candidate videos;
- generation steps;
- candidates.

Artifacts:

```text
generated_assets/jobs/job_000001/prompts/
generated_assets/jobs/job_000001/candidates/candidate_001/
```

Generation strategy:

- multiple candidates;
- lower-cost draft when useful;
- high-cost generation only when allowed;
- register all outputs.

Failure cases:

- API missing;
- API failed;
- model unsuitable;
- prompt rejected;
- output unusable;
- cost limit exceeded.

Fallbacks:

- retry;
- switch tool;
- switch route;
- reduce complexity;
- ask user for tool setup.

---

## 4.16 Quality Council

Purpose:

Evaluate each candidate.

Layers:

1. Technical QA;
2. Cheap Visual QA;
3. Semantic QA;
4. Specialist QA;
5. Strong Judge if needed;
6. Regent final decision.

Outputs:

- `quality_report.json`
- failure tags;
- retry recommendations;
- publish readiness.

Artifacts:

```text
generated_assets/jobs/job_000001/candidates/candidate_001/qc_reports/
```

Failure cases:

- technical invalid;
- format core lost;
- semantic transfer failed;
- bad AI artifacts;
- weak pacing;
- tool mismatch.

---

## 4.17 Revision & Retry

Purpose:

Turn failures into targeted fixes.

Outputs:

- `retry_plan.json`
- revised prompts;
- revised assets;
- route change requests;
- human tasks.

Rules:

- preserve what worked;
- do not blindly regenerate everything;
- stop when cost or retry policy says stop;
- route mutation is allowed.

Possible decisions:

```text
retry_prompt
retry_asset
retry_route
ask_user
abandon
select_best_available
```

---

## 4.18 Final Judge

Purpose:

Select final candidate or abandon job.

Inputs:

- all candidates;
- QC reports;
- retry history;
- budget state;
- user preferences.

Decisions:

```text
select_candidate
needs_user_review
retry_more
abandon
```

Outputs:

```text
generated_assets/jobs/job_000001/final/
```

---

## 4.19 Packaging Council

Purpose:

Generate per-platform packaging.

Outputs:

- titles;
- descriptions;
- tags;
- covers;
- first-frame notes;
- pinned comments;
- platform payloads.

Artifacts:

```text
generated_assets/jobs/job_000001/publish_package/
  bilibili/
  douyin/
  xiaohongshu/
  youtube/
  manual/
```

Policy:

- default all platforms;
- skip only if blocked, unsuitable, or missing platform package.

---

## 4.20 Publish Council

Purpose:

Prepare for publishing.

Checks:

- package complete;
- platform payloads valid;
- permissions allow upload or publish;
- risk policy satisfied;
- tool setup available.

Decisions:

```text
manual_package_only
upload_draft
schedule_publish
auto_publish
ask_user
skip_platform
```

---

## 4.21 Publisher Integrations

Purpose:

Upload, publish, schedule, and fetch metrics.

Methods:

- official API;
- browser automation;
- manual package.

If API missing, create Tool Setup Queue item.

---

## 4.22 Feedback Collection

Purpose:

Collect platform performance.

Metrics:

- views;
- likes;
- comments;
- shares;
- favorites;
- completion rate if available;
- follower gain;
- review status;
- comment sentiment.

Outputs:

- `platform_metrics`
- feedback reports.

---

## 4.23 Learning Memory Update

Purpose:

Write learning from production and publishing.

Updates:

- format learning;
- trend prediction learning;
- tool performance;
- packaging performance;
- user preference;
- platform profile.

Outputs:

- memory entries;
- suggestions;
- learning update report.

---

## 5. Output Package for a Completed Job

Minimum completed job package:

```text
generated_assets/jobs/job_000001/
  job_config.json
  decision_log.json
  source_refs.json
  format_card.json
  trend_scorecard.json
  reproduction_plan.json
  production_recipe.json
  resolved_assets.json

  councils/
  prompts/
  candidates/
  final/
    final_video.mp4
    cover.png
    subtitles.srt
    final_metadata.json

  publish_package/
    bilibili/
    douyin/
    xiaohongshu/
    youtube/
    manual/

  feedback/
    user_review.json
    publish_metrics.json
    learning_update.json
```

---

## 6. Review Gates

Review gates in this route:

1. unclear user intent;
2. high-value format selection if confidence is low;
3. uncertain character / CP mapping;
4. personal creator or unknown assets;
5. missing API or tool setup;
6. high-cost generation;
7. repeated retry failure;
8. publish approval if permission requires;
9. weight or rule changes.

Current user policy reduces some review needs:

- official assets can be direct use;
- official-like / PV-like misleading risk is not blocking.

---

## 7. Failure Branches

### 7.1 No Useful Trend Found

Action:

- save scout report;
- create observation memory;
- optionally ask user for seed links.

### 7.2 Trend Found but Format Weak

Action:

- observe;
- add to watchlist;
- do not create job.

### 7.3 Format Strong but Tool Missing

Action:

- create tool setup item;
- propose fallback route;
- ask user if fallback is acceptable.

### 7.4 Semantic Transfer Fails

Action:

- try alternative target relationship;
- ask user to pick characters;
- switch to generic characters;
- abandon if format depends on impossible mapping.

### 7.5 Asset Missing

Action:

- search official web;
- search wider web;
- generate substitute;
- create human task.

### 7.6 Generation Fails

Action:

- classify failure;
- retry prompt;
- switch tool;
- switch route;
- reduce complexity;
- ask user if high-cost retry is needed.

### 7.7 Candidate Fails Quality

Action:

- use retry engine;
- preserve successful parts;
- generate new candidate;
- abandon if repeated route failure.

### 7.8 Packaging Not Good Enough

Action:

- generate more titles/covers;
- use platform-specific packaging;
- ask user if uncertain.

### 7.9 Platform Publishing Blocked

Action:

- create manual package;
- create tool setup item;
- skip platform only if needed.

---

## 8. Quality Targets

A completed video should satisfy:

- technically valid file;
- platform-compatible video and audio;
- source format core preserved;
- semantic transfer makes sense if used;
- visual quality acceptable;
- AI artifacts not too distracting;
- packaging complete;
- publish package complete;
- provenance recorded;
- quality report available;
- learning update written.

---

## 9. First Implementation Boundaries

This route should be complete, but it can start with limited integrations.

Allowed initial simplifications:

- manual seed links before full platform crawling;
- metadata-only harvest for hard platforms;
- manual publish package before official upload API;
- placeholder tool interfaces when API is not configured;
- deterministic checks before expensive agents;
- generated reports before full Web UI.

Not allowed:

- fake external APIs;
- untracked assets;
- unlogged decisions;
- unversioned score weights;
- candidates without generation steps;
- publishing without package records;
- losing source provenance.

---

## 10. Acceptance Criteria

The first production line is considered structurally ready when it can:

1. Create a run from keyword or source link.
2. Collect candidate sources.
3. Harvest at least metadata and source manifest.
4. Produce understanding reports.
5. Produce at least one format card.
6. Produce trend scorecards with visible weights.
7. Create a job.
8. Produce reproduction plan and production recipe.
9. Resolve assets or create review items.
10. Generate at least one candidate through a real configured tool or a clearly marked local/manual generation step.
11. Run multi-layer QC.
12. Produce retry plan when candidate fails.
13. Produce final package when candidate passes.
14. Produce per-platform packaging.
15. Create manual publish package at minimum.
16. Record feedback if available.
17. Write learning memory entries.

---

## 11. Relationship to Later Routes

This first production line will later call or share infrastructure with:

- MMD / 3D route;
- longform route;
- advanced music/dance route;
- automated platform publishing;
- local Web Console.

It should not hard-code assumptions that only apply to short videos or only apply to one platform.

---

## 11. Execution Contract (Merged)

Merged from `FIRST_PRODUCTION_LINE_EXECUTION_BRIEF.md`.

This is a route execution contract, not a numbered phase.

Full intended route gates:

```text
Gate 1: Is this format worth making?
Gate 2: Can Kairove produce it with current tools/assets?
Gate 3: Are generated candidates good enough?
Gate 4: Is the publish package acceptable?
Gate 5: What did feedback teach Kairove?
```

Execution pipeline:

```text
Run Intake
Source Scout
Harvester
Video Understanding
Format Miner
Trend Analyst
Regent Gate 1
Job Creation
Format Reproduction Council
Semantic Format Transfer
Route Selector
Asset Requirement Planning
Asset Resolver
Regent Gate 2
Production Recipe Builder
Generation Manager
Candidate Assembly
Quality Council
Revision and Retry
Final Judge
Packaging Council
Publish Council
Publisher Integrations or Manual Publish Package
Feedback Collection
Learning Memory Update
```

Required job package:

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

Key rule:

```text
Job creation means Kairove committed to planning one production attempt. It does not mean generation has started.
```

---

## 12. Format Miner and Trend Analyst Contract (Merged)

Merged from `FORMAT_MINER_TREND_ANALYST_BRIEF.md`.

Format Miner turns understanding reports into reusable structures.
Trend Analyst scores whether those structures are worth producing.

Format Miner outputs:

```text
FormatCandidate
FormatCluster
FormatCard
FormatGenome
FormatMemoryUpdate
```

Trend Analyst outputs:

```text
TrendScorecard
ScoreExplanationReport
ReviewItem when confidence/policy is uncertain
```

Format signal groups:

```text
script
visual
audio
structure
production
```

Decision values for new vs existing:

```text
new_format
variant_of_existing
weak_observation
not_a_format
needs_more_sources
```

Default trend score dimensions:

```text
heat_score
velocity_score
engagement_quality
remixability
format_strength
transfer_potential
production_feasibility
audience_fit
freshness
fatigue_penalty
overdone_penalty
negative_sentiment_penalty
production_risk_penalty
tool_gap_penalty
source_confidence_penalty
platform_unsuitability_penalty
```

Default weight principle:

```text
heat_score and velocity_score are high-weight by default.
Every scorecard must expose raw score, weight, weighted contribution, and evidence.
Weights are configurable and versioned.
Weight changes require user approval before becoming rules.
```

Heat vs overdone rule:

```text
Many similar videos are positive when engagement, comments, remixing, and newer examples remain strong.
Many similar videos are negative when comments call it tired, engagement declines, and variants stop adding value.
```

Default thresholds:

```yaml
make_video: 7.2
observe: 5.5
collect_more: 4.0
reject_below: 4.0
```
---

## 13. Phase 2 Format Intelligence Link

Format Intelligence and Opportunity Decision is now tracked as Phase 2 planning, not as an embedded candidate section inside this file.

Canonical document:

```text
PHASE2_FORMAT_INTELLIGENCE_AND_OPPORTUNITY_DECISION_PLAN.md
```

Relationship to this production line:

```text
P1 discovers TrendOpportunityPackets.
Phase 2 converts strong opportunities into Format, FormatGenome, TrendScorecard, and ProductionStartPacket.
P0-B can start a production job from ProductionStartPacket.
```

This file keeps the first production line context. Edit the Phase 2 canonical document for Phase 2 scope changes.

---

## Cross-Phase Policy Alignment - 2026-06-06

First production line taste:

```text
Default direction is ordinary AI video reproduction/transfer of recent popular formats.
Do not lock one specific topic or fandom.
Supported taste includes short jokes, abstract short drama, character substitution, plot reversal, spoken/copywriting adaptation, and AI animation skits.
P0-B only proves the chain can carry these types; it does not judge real hit potential.
```

P0-B start:

```text
Main acceptance chain starts from text seed.
URL, local reference folder, and manual format selection remain structurally reserved.
```
