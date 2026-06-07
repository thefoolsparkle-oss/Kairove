# Kairove Longform Video Route Plan

## 0. Purpose

This document defines Kairove's longform route for videos from several minutes to hours.

Longform is not just a longer short video. It needs different planning, storage, generation, QA, editing, and feedback loops.

---

## 1. Route ID

```text
route_longform_video
```

---

## 2. Use Cases

Longform can include:

- 5-10 minute explanation videos;
- AI story episodes;
- horror story compilations;
- trend analysis videos;
- character/fandom deep dives;
- documentary-style videos;
- multi-hour compilations;
- serialized content.

---

## 3. Object Hierarchy

Longform should use:

```text
Project
  -> Episode
    -> Chapter
      -> Scene
        -> Shot
          -> GenerationStep
```

Do not manage longform as one giant video job.

---

## 4. Longform Council

Agents:

- `TopicDepthAgent`
- `ChapterPlanner`
- `InformationDensityAgent`
- `NarrationStructureAgent`
- `SegmentPlanner`
- `ContinuityAgent`
- `RetentionCurveAgent`
- `AssetReuseAgent`
- `LongformEditAgent`
- `LongformQAAgent`

Flow:

```text
1. Define longform goal
2. Build outline
3. Split chapters
4. Split scenes
5. Plan narration and visuals
6. Resolve reusable assets
7. Generate segments
8. QA per segment
9. Assemble full video
10. QA full video
```

---

## 5. Duration Strategy

Longform should not use fixed durations blindly.

Duration is determined by:

- topic complexity;
- number of chapters;
- audience retention expectations;
- platform;
- generation cost;
- available materials;
- narrative pacing.

Strategies:

```text
mini_longform: 3-8 minutes
standard_longform: 8-20 minutes
deep_dive: 20-60 minutes
compilation: 60+ minutes
```

---

## 6. Generation Strategy

Longform should use:

- reusable narration voices;
- reusable visual styles;
- segment-level generation;
- cached assets;
- batch subtitle rendering;
- checkpointed editing;
- resumable jobs.

Avoid:

- one huge generation call;
- untracked segment files;
- inconsistent style across chapters;
- no checkpoint recovery.

---

## 7. Longform QA

Checks:

- chapter order;
- repeated information;
- narration continuity;
- subtitle sync;
- visual consistency;
- audio loudness consistency;
- pacing;
- retention drops;
- chapter transition quality;
- final video technical validity.

QA should happen at:

```text
scene level
chapter level
full video level
```

---

## 8. Longform Publishing

Packaging differs:

- stronger title and thumbnail;
- chapters/timestamps;
- longer description;
- more tags;
- platform-specific category;
- possible series/playlist.

---

## 9. Acceptance Criteria

Longform route is ready when it can:

1. Create project/episode/chapter/scene hierarchy.
2. Generate outline.
3. Generate narration plan.
4. Generate or resolve repeated assets.
5. Produce segment candidates.
6. Assemble segments.
7. Run segment and full-video QA.
8. Produce longform publish package.

