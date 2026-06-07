# Kairove Planning Completion Map

## 0. Purpose

This document tracks planning completeness.

It is not a new roadmap and it does not create new phases.

Use it to answer:

- what has already been planned;
- what is implementation-ready;
- what is still only a future capability area;
- which documents should be updated when planning changes.

---

## 1. Current Phase Status

Strict phase count:

```text
Confirmed implementation phases: 1
Confirmed phase: Phase 0
Current drafted candidate phase: Phase 1
Total future phase count: unknown
```

Important rule:

```text
Only discussed and accepted implementation stages become numbered phases.
Legacy Step lists and route stages are not global phases.
```

---

## 2. Implementation-Ready Planning

### Phase 0: Foundation

Status:

```text
Confirmed and implementation-brief drafted.
```

Primary docs:

```text
IMPLEMENTATION_ROADMAP.md
PHASE0_IMPLEMENTATION_BRIEF.md
CORE_OBJECTS_AND_SCHEMA_PLAN.md
CONFIG_PERMISSION_AND_TOOL_SETUP_PLAN.md
TESTING_STRATEGY_PLAN.md
```

P0 is ready for final user review before coding.

P0 still needs explicit user approval before implementation begins.

### Candidate Phase 1: Trend and Source Intelligence Foundation

Status:

```text
Candidate scope drafted, default decisions drafted, not implementation-started.
```

Primary docs:

```text
PHASE1_TREND_SOURCE_INTELLIGENCE_PLAN.md
PHASE1_IMPLEMENTATION_BRIEF.md
SOURCE_SCOUT_AND_HARVEST_PLAN.md
CORE_OBJECTS_AND_SCHEMA_PLAN.md
```

P1 is not confirmed as an implementation phase yet.

P1 still needs review of:

- platform priority;
- candidate and harvest limits;
- snapshot policy;
- fixture examples;
- report format;
- external tool/API setup expectations.

---

## 3. Core Architecture Plans

These are foundational plans and should stay synchronized with phase briefs.

```text
KAIROVE_PLAN.md:
  Main system vision. Section 31 is legacy capability sequencing, not the current roadmap.

CORE_OBJECTS_AND_SCHEMA_PLAN.md:
  Core object vocabulary and schema concepts.

AGENT_ECOSYSTEM_PLAN.md:
  Regent, councils, sub-agent sequencing, escalation, and disagreement handling.

CONFIG_PERMISSION_AND_TOOL_SETUP_PLAN.md:
  Capability permissions, budgets, risk policy, tool setup queue.

TESTING_STRATEGY_PLAN.md:
  Test levels, fixture strategy, Phase 0 tests, safe external tests.
```

Update rule:

```text
If a phase brief changes object fields, permissions, status values, or tests, update the relevant core architecture plan or mark the difference explicitly.
```

---

## 4. First Production Line Plans

Prepared capability brief:

```text
FORMAT_MINER_TREND_ANALYST_BRIEF.md:
  Defines Format Miner and Trend Analyst capability planning: format clustering, format cards/genomes, trend scorecards, visible weights, fatigue vs heat logic, and fixture tests.
```

These describe the intended first complete usable video-making line.

```text
FIRST_PRODUCTION_LINE_PLAN.md:
  Ordinary AI format reproduction route.

SOURCE_SCOUT_AND_HARVEST_PLAN.md:
  Discovery and harvesting layer.

QUALITY_AND_RETRY_PLAN.md:
  Technical QA, visual/semantic QA, specialist QA, strong judges, retry.

GENERATION_AND_TOOL_REGISTRY_PLAN.md:
  Tool registry and generation manager.

PACKAGING_AND_PUBLISHING_PLAN.md:
  Titles, descriptions, tags, covers, publish packages, platform publishing.
```

Status:

```text
Planned as capability areas. Not all are scheduled as phases.
```

Important:

```text
A complete first production line will need multiple future phases, but those phases have not been numbered or accepted yet.
```

---

## 5. Asset and Source Plans

```text
AUDIO_VISUAL_ASSET_SYSTEM_PLAN.md:
  Audio, voice, visual references, subtitles, cover-related assets.

SOURCE_SCOUT_AND_HARVEST_PLAN.md:
  External source discovery and provenance.

CONFIG_PERMISSION_AND_TOOL_SETUP_PLAN.md:
  Source usage policy and review rules.
```

Status:

```text
Broad planning drafted. Implementation scheduling depends on P1 and later production phases.
```

Current user policy captured:

- official assets can be direct-use under current user policy;
- personal creator assets require review before direct use;
- unknown assets require review;
- official-like misleading risk is not blocking;
- all assets still require provenance.

---

## 6. Specialized Route Plans

### MMD / 3D

Docs:

```text
MMD_3D_ROUTE_PLAN.md
MMD_3D_DETAILED_PLAN.md
```

Status:

```text
Specialized route planned, not scheduled as a global phase.
```

Important:

```text
3D Route Stages are internal route stages, not global phases.
```

### Longform

Docs:

```text
LONGFORM_VIDEO_ROUTE_PLAN.md
LONGFORM_DETAILED_PLAN.md
```

Status:

```text
Specialized route planned, not scheduled as a global phase.
```

---

## 7. Review, UI, Learning, and Handoff Plans

```text
HUMAN_REVIEW_CONSOLE_PLAN.md:
  Review queues and future control console behavior.

LOCAL_WEB_CONSOLE_UI_PLAN.md:
  Future local UI layout and interaction plan.

KNOWLEDGE_AND_LEARNING_PLAN.md:
  Memory, learning suggestions, feedback loops.

ROADMAP_AND_HANDOFF_PLAN.md:
  Handoff and continuity rules.
```

Status:

```text
Important long-term plans drafted. Not scheduled as implementation phases yet.
```

---

## 8. Always Update These When Planning Changes

The user explicitly requested these to stay current:

```text
KAIROVE_COMPACT_CONTEXT.md
READING_GUIDE.md
```

Also update when relevant:

```text
PROJECT_INDEX.md
IMPLEMENTATION_ROADMAP.md
PLANNING_COMPLETION_MAP.md
```

Rule:

```text
When a new planning document is added, update PROJECT_INDEX.md, READING_GUIDE.md, KAIROVE_COMPACT_CONTEXT.md, and this file.
```

---

## 9. Current Planning Gaps

These are not blockers for P0.

Open planning gaps before later implementation:

```text
P1 final user confirmation
Reproduction/Semantic Transfer implementation brief
Asset Resolver implementation brief
Generation Manager implementation brief
Quality/Retry implementation brief
Packaging/Publishing implementation brief
Feedback Learning implementation brief
Local Web Console implementation brief
MMD/3D implementation scheduling decision
Longform implementation scheduling decision
```

Already drafted but not scheduled as phases:

```text
PHASE0_IMPLEMENTATION_BRIEF.md
PHASE1_IMPLEMENTATION_BRIEF.md
FORMAT_MINER_TREND_ANALYST_BRIEF.md
FIRST_PRODUCTION_LINE_EXECUTION_BRIEF.md
```

Do not turn open gaps into numbered phases until discussed.

---

## 10. Recommended Next Planning Flow

Recommended order from here:

```text
1. Review PHASE0_IMPLEMENTATION_BRIEF.md.
2. If acceptable, implement Phase 0 later when the user asks for code.
3. Review PHASE1_IMPLEMENTATION_BRIEF.md sections 13-16.
4. Adjust P1 defaults if needed.
5. Only then decide whether P1 becomes the next confirmed phase.
```

If the user says "继续写计划" again, choose the highest-value missing implementation brief rather than inventing future phase numbers.

Recommended next non-code planning targets:

```text
A. Quality/Retry implementation brief
B. Asset Resolver implementation brief
C. Packaging/Publishing implementation brief
D. Generation Manager implementation brief
E. Local Web Console implementation brief
```