# Kairove Audio, Voice, Visual Asset, and Style System Plan

## 0. Purpose

This document defines Kairove's asset capability layer for audio, voice, visual references, style extraction, subtitles, covers, scenes, and generated assets.

Councils decide what is needed. This system finds, creates, manages, and checks the assets.

---

## 1. Audio and Voice System

### 1.1 Audio Discovery

Find:

- hot songs;
- sound memes;
- common BGM;
- punchline SFX;
- platform-native audio;
- user-provided audio.

### 1.2 Audio Identification

Identify:

- song name;
- artist;
- audio role;
- whether modified;
- whether platform-native;
- whether direct embedding is allowed by user policy.

### 1.3 Beat and Timing Analysis

Produce:

- BPM;
- beat points;
- drop points;
- silence points;
- lyric timestamps;
- recommended cut points.

### 1.4 Voice Profile Management

Store:

- user-trained voices;
- generated original voices;
- narrator voices;
- character-style voices;
- singing voices;
- unavailable or blocked voices.

### 1.5 Voice Training Pipeline

If enabled:

```text
collect audio -> check source -> clean -> slice -> transcribe -> train -> test -> user review -> register voice profile
```

If unavailable, create human task.

### 1.6 TTS

Generate:

- narration;
- dialogue;
- emotional takes;
- multiple candidates;
- alignment data.

### 1.7 SFX and BGM

Find or generate:

- punchline sting;
- horror drone;
- transition sounds;
- ambience;
- loopable BGM.

### 1.8 Audio QA

Check:

- clipping;
- low volume;
- noise;
- BGM masking voice;
- sync;
- subtitle alignment;
- audio source policy.

---

## 2. Visual Asset and Style System

### 2.1 Visual Reference Discovery

Find:

- official character images;
- wiki references;
- official PV screenshots;
- visual style references;
- subtitle/cover references;
- scene references.

Current policy:

- official visual assets can be direct-use;
- personal creator assets need review for direct use.

### 2.2 Character Visual Understanding

Extract:

- hair;
- eyes;
- outfit;
- color palette;
- accessories;
- body silhouette;
- signature props;
- must-preserve features.

### 2.3 Style Extraction

Extract:

- composition;
- lighting;
- color;
- camera;
- texture;
- subtitle layout;
- cover layout;
- AI artifact style.

### 2.4 Subtitle Style System

Manage:

- fast meme subtitles;
- horror subtitles;
- lyric subtitles;
- large cover-like captions;
- keyword highlights;
- safe areas.

### 2.5 Cover Style System

Generate and evaluate:

- character close-up cover;
- conflict cover;
- horror cover;
- meme big-text cover;
- platform-specific crop.

### 2.6 Scene and Background Assets

Find or generate equivalent scenes:

- dorm room;
- command room;
- classroom;
- cafe;
- horror hallway;
- game UI;
- gacha screen;
- livestream room.

Scene choice should support semantic transfer, not random decoration.

### 2.7 Generated Visual Assets

Generated assets must record:

- prompt;
- model;
- input references;
- source references;
- usage;
- quality report.

### 2.8 Visual QA

Check:

- character similarity;
- style consistency;
- watermarks;
- random text;
- face/hand problems;
- cover readability;
- subtitle obstruction;
- source policy.

---

## 3. Asset Manifest Requirements

Every asset must record:

- asset id;
- source id;
- source type;
- usage policy;
- local path;
- hash;
- review status;
- used jobs;
- generation step if generated.

---

## 4. Acceptance Criteria

This system is ready when it can:

1. Register local voice and visual assets.
2. Record official/reference/personal source policy.
3. Find official visual references.
4. Produce character visual profiles.
5. Produce subtitle style and cover style records.
6. Generate or register audio assets.
7. Create human tasks for missing voice/model/tool capability.
8. Feed resolved assets to Generation Manager.
---

## 5. Asset Resolver Operating Contract

Asset Resolver turns production needs into actual usable assets or clear human tasks.

It should not simply search randomly. It should resolve a typed requirement with provenance, usage policy, review status, and fallback options.

Core rule:

```text
Every required asset ends as resolved, generated, substituted, waiting_for_user, blocked, or deferred.
```

---

## 6. Asset Requirement Types

Supported requirement types:

```text
character_reference
character_voice
world_or_scene_reference
style_reference
source_video_reference
audio_reference
music_or_bgm
sound_effect
subtitle_style
cover_style
logo_or_ui_element
mmd_model
mmd_motion
mmd_stage
platform_package_asset
```

Minimum requirement record:

```json
{
  "requirement_id": "asset_req_000001",
  "job_id": "job_000001",
  "asset_type": "character_reference",
  "target": "character_a",
  "required": true,
  "preferred_source_types": ["official", "wiki", "local"],
  "usage_needed": "direct_use | reference_only | style_analysis | generation_input",
  "quality_bar": "draft | normal | high | critical",
  "fallback_policy": "generate | substitute | ask_user | defer",
  "status": "unresolved"
}
```

---

## 7. Resolution Order

Default resolution order:

```text
1. Existing local assets
2. User-curated official assets
3. User-trained voices / local trained assets
4. Official pages and official platform accounts
5. Wiki/reference pages
6. Research assets collected by Source Scout
7. Generated assets
8. Ask user
9. Defer or block
```

Rules:

- local_assets are preferred when they already satisfy quality and policy;
- official assets can be direct-use under current user policy but still need provenance;
- personal creator and unknown assets require review before direct use;
- generated assets must record prompt/model/input references;
- if a required asset cannot be found, create ReviewItem or ToolSetupItem.

---

## 8. Asset Resolver Agents

Suggested ordered agents:

```text
AssetRequirementNormalizer
LocalAssetSearchAgent
OfficialSourceAssetFinder
WikiReferenceFinder
ResearchAssetMatcher
AudioAssetResolver
VoiceAssetResolver
VisualStyleResolver
GeneratedAssetPlanner
PolicyClassifier
AssetQualityChecker
AssetManifestWriter
MissingAssetReporter
```

Order:

```text
normalize requirement -> search local -> search official/wiki/research -> classify policy -> quality check -> write manifest -> report resolved/missing
```

For audio/voice requirements, use:

```text
AudioIdentifier -> AudioPolicyClassifier -> BeatAnalyzer -> VoiceProfileMatcher -> VoiceTrainingTaskPlanner if needed
```

For character visuals, use:

```text
OfficialReferenceFinder -> WikiReferenceFinder -> VisualProfileExtractor -> ReferenceSetBuilder -> SimilarityChecker
```

---

## 9. Asset Resolution Report

Each job should produce:

```text
generated_assets/jobs/job_000001/assets/asset_resolution_report.json
generated_assets/jobs/job_000001/assets/asset_resolution_report.md
```

Minimum JSON:

```json
{
  "asset_resolution_report_id": "asset_res_000001",
  "job_id": "job_000001",
  "requirements_total": 0,
  "resolved": [],
  "generated": [],
  "substituted": [],
  "waiting_for_user": [],
  "blocked": [],
  "tool_setup_items": [],
  "review_items": [],
  "overall_status": "ready | ready_with_warnings | waiting_for_user | blocked"
}
```

Markdown report should show:

```text
Requirement
Resolved asset
Source/provenance
Usage policy
Review status
Quality notes
Fallback if failed
```

---

## 10. Asset Manifest Fields

Every resolved asset must have a manifest.

Minimum fields:

```json
{
  "asset_id": "asset_000001",
  "asset_type": "character_reference",
  "asset_origin": "local | official | wiki | research | generated | user_provided | unknown",
  "source_id": "src_000001",
  "source_url": "...",
  "local_path": "...",
  "hash": "...",
  "usage_policy": "direct_use | reference_only | style_analysis | generation_input | blocked | unknown",
  "review_status": "not_required | pending | approved | rejected",
  "used_for": ["job_000001"],
  "quality_status": "pass | warning | fail | unchecked",
  "created_by": "asset_resolver | user | generation_manager",
  "created_at": "..."
}
```

---

## 11. Missing Asset Handling

Missing asset outcomes:

```text
ask_user_for_file
ask_user_for_approval
create_tool_setup_item
generate_replacement
use_reference_only
change_route
defer_job
block_job
```

Examples:

```text
character voice missing -> use narrator/TTS, train voice if user provides material, or ask user
specific official model missing -> ask user to place it in local_assets, or use 2D reference route
hot audio unavailable -> use timing reference only, generate similar BGM/SFX, or ask user
personal creator image needed for direct use -> create review item
```

---

## 12. Asset Quality Checks

Asset quality checks should happen before generation.

Visual reference checks:

- readable resolution;
- character unobstructed;
- consistent identity;
- no unwanted watermark/text if direct-use;
- source policy known;
- enough angles if needed.

Audio checks:

- usable duration;
- clipping/noise;
- beat detectability;
- voice clarity;
- source policy known;
- loop/cut points usable.

MMD/3D checks:

- file exists;
- format recognized;
- dependencies known;
- license/policy status;
- compatibility metadata where possible.

---

## 13. Asset Resolver Acceptance Criteria

Asset Resolver is ready when it can:

1. Read typed asset requirements from a job.
2. Search local assets first.
3. Search official/wiki/research references when allowed.
4. Classify usage policy.
5. Create review items for personal/unknown direct-use assets.
6. Create tool setup items for missing search/download/generation capability.
7. Generate or plan replacement assets when allowed.
8. Write asset manifests.
9. Produce asset resolution reports.
10. Block or defer jobs when required assets are unresolved.
11. Feed resolved assets to Generation Manager.

---

## Cross-Phase Policy Alignment - 2026-06-06

Asset policy:

```text
Official assets can be direct-use with provenance under current user policy.
Personal creator or unknown assets:
  first search for official or substitute assets
  ask before direct use
Reference/style analysis can be more permissive than direct use.
```

Music and SFX:

```text
Official music/SFX can be direct-use with provenance.
Music needs extra platform-risk notes.
Minimum fields: source, work/song title, official owner/account, usage, platform risk note.
Personal or unknown music/SFX sources default to review.
```

Knowledge packs:

```text
Maintain work packs, character packs, and relationship/CP packs.
Relationship packs are first-class because many transfers depend on relationship function.
```
