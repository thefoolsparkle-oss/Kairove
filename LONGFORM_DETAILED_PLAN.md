# Kairove Longform Detailed Plan

## 0. Purpose

This document expands the longform video route in detail.

Longform is not a stretched short video. It needs stronger structure, chapter planning, source handling, narration continuity, asset reuse, checkpointing, and multi-level QA.

---

## 1. Longform Is Not Shortform

Short videos are optimized around:

```text
hook -> fast payoff -> repeat/share
```

Longform is optimized around:

```text
promise -> structure -> sustained attention -> payoff -> memory
```

Kairove must not use short-video logic unchanged.

Longform needs:

- outline;
- chapter-level planning;
- information density control;
- repetition control;
- narration continuity;
- asset reuse;
- checkpointing;
- scene-level QA;
- chapter-level QA;
- full-video QA.

---

## 2. Longform Content Types

### 2.1 Explanation / Commentary

Examples:

- trend analysis;
- AI tool analysis;
- fandom explanation;
- character/story analysis;
- platform trend recap.

Needs:

- accurate structure;
- source citations;
- clear narration;
- visual support;
- pacing.

### 2.2 Story / Episode

Examples:

- AI horror episode;
- serialized short drama;
- character story;
- fictional documentary.

Needs:

- narrative arc;
- scene continuity;
- character consistency;
- mood control.

### 2.3 Compilation

Examples:

- many short AI horror clips;
- meme format compilation;
- character reaction合集;
- weekly trend recap.

Needs:

- selection quality;
- ordering;
- transitions;
- no fatigue;
- consistent packaging.

### 2.4 Deep Dive

Examples:

- one topic 20-60 minutes;
- long fandom/world explanation;
- multi-format comparison.

Needs:

- research;
- chapter hierarchy;
- evidence management;
- retention curve.

---

## 3. Longform Object Hierarchy

Longform should use:

```text
Project
  -> Episode
    -> Chapter
      -> Scene
        -> Shot
          -> GenerationStep
```

### 3.1 Project

```json
{
  "project_id": "long_project_0001",
  "topic": "...",
  "project_type": "explanation | story | compilation | deep_dive",
  "target_platforms": ["bilibili", "youtube"],
  "style": "...",
  "status": "planning | producing | paused | completed"
}
```

### 3.2 Episode

```json
{
  "episode_id": "episode_0001",
  "project_id": "long_project_0001",
  "episode_title_working": "...",
  "duration_strategy": "mini_longform | standard_longform | deep_dive | compilation",
  "chapter_ids": []
}
```

### 3.3 Chapter

```json
{
  "chapter_id": "chapter_0001",
  "episode_id": "episode_0001",
  "title": "...",
  "purpose": "setup | evidence | analysis | story_turn | conclusion",
  "estimated_duration": null,
  "scene_ids": []
}
```

### 3.4 Scene

```json
{
  "scene_id": "scene_0001",
  "chapter_id": "chapter_0001",
  "scene_type": "narration | generated_clip | source_analysis | transition | montage",
  "script_path": "...",
  "shot_ids": []
}
```

---

## 4. Longform Council Flow

Ordered flow:

```text
1. Intent Interpreter
2. Topic Scope Agent
3. Research Planner
4. Outline Builder
5. Chapter Planner
6. Retention Curve Planner
7. Narration Planner
8. Visual Support Planner
9. Asset Reuse Planner
10. Segment Production Planner
11. Longform Risk and Fatigue Check
12. Longform Plan Assembler
```

### 4.1 Topic Scope Agent

Decides:

- what the video covers;
- what it does not cover;
- target audience knowledge level;
- how much context is needed.

### 4.2 Retention Curve Planner

Plans:

- opening promise;
- early payoff;
- chapter hooks;
- mid-video re-engagement;
- final payoff.

### 4.3 Asset Reuse Planner

Determines:

- repeated character visuals;
- reusable backgrounds;
- repeated subtitle style;
- recurring music bed;
- recurring lower-thirds or diagrams.

---

## 5. Longform Script Strategy

Longform script should be layered:

```text
outline
  -> chapter brief
    -> scene brief
      -> narration draft
        -> pacing pass
          -> source/evidence check
```

Script modes:

```text
commentary:
  clear, structured, evidence-driven.

horror_story:
  atmosphere, suspense, controlled reveal.

compilation:
  short intros, transitions, minimal repetition.

deep_dive:
  strong chapter logic and recap.
```

Anti-AI checks:

- repetitive phrasing;
- generic summaries;
- too many mechanical transitions;
- over-explaining;
- lack of concrete evidence;
- same sentence rhythm for too long.

---

## 6. Research and Source Handling

Longform often needs stronger research than shortform.

Research requirements:

- source list;
- citation notes;
- screenshots;
- transcripts;
- claim confidence;
- unknown claims marked.

Each claim should ideally link to:

```text
source_id
timestamp if video
quote/summary
confidence
```

Kairove should distinguish:

- factual claims;
- interpretation;
- speculation;
- user preference;
- generated fiction.

---

## 7. Generation Strategy

Longform should use segmented generation.

Segment types:

```text
narration_segment
visual_broll_segment
generated_scene_segment
source_reference_segment
transition_segment
title_card_segment
chapter_card_segment
compilation_item
```

Cache:

- narration audio;
- subtitle files;
- generated images;
- reusable background video;
- character reference images;
- music beds;
- chapter cards.

Every scene/chapter should have:

- status;
- output files;
- QA report;
- retry history.

Do not wait until final assembly to know a chapter failed.

---

## 8. Editing Strategy

Longform editing should support:

- chapter cards;
- lower thirds;
- source screenshots;
- generated B-roll;
- subtitles;
- music ducking;
- transitions;
- recap moments;
- progress structure.

For B站/YouTube:

- chapters/timestamps matter;
- title/thumbnail are critical;
- description can hold sources and context.

---

## 9. QA Levels

### 9.1 Scene QA

Checks:

- technical validity;
- narration sync;
- visual support;
- local pacing;
- no missing assets.

### 9.2 Chapter QA

Checks:

- chapter purpose fulfilled;
- no major repetition;
- transition from previous chapter;
- information density;
- mood consistency.

### 9.3 Full Episode QA

Checks:

- outline coherence;
- chapter order;
- audio loudness consistency;
- subtitle consistency;
- style consistency;
- retention curve;
- total duration appropriateness;
- final publish readiness.

---

## 10. Retry Strategy

Retry should be localized.

Examples:

```text
bad scene narration:
  rewrite only scene narration.

weak chapter transition:
  rewrite transition and chapter card.

visual style inconsistency:
  regenerate affected B-roll, not entire episode.

audio loudness mismatch:
  remix chapter audio.

too long:
  trim low-value scenes or split into episodes.
```

Avoid full regeneration unless the whole structure is wrong.

---

## 11. Longform Publish Package

Package:

```text
final_video.mp4
thumbnail.png
title_options.json
description.txt
tags.json
chapters.json
source_notes.json
platform_payloads/
```

For B站/YouTube:

- chapter timestamps;
- longer description;
- source notes if useful;
- playlist/series info.

For short-video platforms:

- consider cutting longform into highlights;
- publish trailer clips;
- link or series-tag main episode.

---

## 12. Derived Shorts

Longform should be able to create derivative short clips:

```text
long episode -> highlight segments -> short clips -> platform short package
```

Derived shorts should preserve links to the parent episode.

---

## 13. Human Review Points

Ask user when:

- topic scope unclear;
- factual claim confidence low;
- source interpretation risky;
- long script direction uncertain;
- total duration too high;
- chapter order disputed;
- high-cost batch generation required;
- publish package differs greatly by platform.

---

## 14. Implementation Phases

### Phase Long-0: Object Model

- project;
- episode;
- chapter;
- scene;
- shot references.

### Phase Long-1: Outline and Chapter Planning

- outline builder;
- chapter planner;
- chapter JSON output.

### Phase Long-2: Narration and Subtitle Pipeline

- narration script per scene;
- TTS or voice output;
- subtitles;
- audio alignment.

### Phase Long-3: Segment Generation

- scene-level visual generation;
- reusable assets;
- segment QA.

### Phase Long-4: Assembly

- chapter assembly;
- full episode assembly;
- chapter timestamps;
- full QA.

### Phase Long-5: Derived Shorts

- highlight extraction;
- short clip packaging;
- link to parent episode.

---

## 15. Early Non-Goals

Do not start with:

- multi-hour fully automatic production;
- no-source factual claims;
- huge uncheckpointed generation;
- automatic public publishing without review;
- complex documentary editing UI.

---

## 16. Final Principle

Longform should be:

```text
structured
checkpointed
source-aware
segment-based
locally retryable
platform-packaged
able to generate derivative shorts
```

---

## 16. Route Summary (Merged)

Merged from `LONGFORM_VIDEO_ROUTE_PLAN.md`.

Route ID:

```text
route_longform_video
```

Use this route for videos where structure, retention, chapters, source management, and editing continuity matter more than short trend replication.

Core hierarchy:

```text
Project -> Episode -> Chapter -> Scene
```

This is a specialized route. In the global roadmap it is also the canonical detailed plan for Phase 11 when that phase is scheduled.

---

## 17. Phase 11 Canonical Contract

Phase 11 identity:

```text
Longform Specialized Route
```

Status:

```text
P11 planning boundary confirmed as the longform specialized route.
Implementation is not authorized until the user explicitly schedules P11.
```

Purpose:

```text
Support videos where structure, retention, chapters, source handling, continuity, and checkpointed production matter more than short trend replication.
```

Primary inputs:

```text
longform production goal
source corpus
Format/Trend context when relevant
research notes
outline goals
voice/audio requirements
visual style requirements
platform duration requirements
```

Primary outputs:

```text
LongformProject
EpisodePlan
ChapterPlans
ScenePlans
ShotPlans
NarrationScripts
SourceNotes
SegmentGenerationPlans
ContinuityReports
LongformQualityReports
LongformPublishPackage
DerivedShortsPlan
```

P11 workstreams:

```text
P11-A Longform Object Model
P11-B Topic Scope and Research Plan
P11-C Outline and Chapter Planning
P11-D Retention Curve Planning
P11-E Narration and Script Pipeline
P11-F Source/Citation Handling
P11-G Segment Generation Planning
P11-H Assembly and Continuity
P11-I Scene/Chapter/Episode QA
P11-J Longform Publish Package
P11-K Derived Shorts Extraction
```

P11 must include:

```text
Project -> Episode -> Chapter -> Scene -> Shot hierarchy
source-aware claim tracking
chapter-level checkpoints
localized retry
continuity checks
longform-specific publish metadata
option to create derived shorts
```

P11 must not include:

```text
forcing short-video assumptions onto long videos
multi-hour uncheckpointed generation
no-source factual claims
unreviewed long video publishing
rebuilding every scene when one scene fails
```

P11 acceptance criteria:

```text
can create longform project hierarchy
can write outline, chapter, scene, and shot plans
can manage source notes and claim confidence
can produce narration/visual segment plans
can QA scene, chapter, and full episode levels
can retry localized segments
can build longform publish package with chapters/source notes
can create derived shorts linked to parent episode
```

P11 confirmation checklist:

```text
first longform type: explanation, story, compilation, or deep dive
initial target duration range policy
first supported platforms
source citation strictness
voice/narration strategy
whether derived shorts are default
```

---

## Cross-Phase Policy Alignment - 2026-06-06

P11 longform type policy:

```text
Do not lock one longform content type.
Supported categories remain:
  long drama
  commentary/explainer
  remix/compilation
  tutorial
  fan-series
```

P11 structure policy:

```text
Focus on longform hierarchy:
  Project -> Episode -> Chapter -> Scene -> Shot

P11 is not short video stretched longer.
```
