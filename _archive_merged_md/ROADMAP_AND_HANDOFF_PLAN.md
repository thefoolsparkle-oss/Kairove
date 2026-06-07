# Kairove Roadmap and Handoff Plan

## 0. Purpose

This document summarizes what should happen before implementation, how to hand work to another AI or developer, and how to avoid losing project intent.

---

## 1. Current Planning Documents

Core documents:

```text
KAIROVE_PLAN.md
CORE_OBJECTS_AND_SCHEMA_PLAN.md
AGENT_ECOSYSTEM_PLAN.md
FIRST_PRODUCTION_LINE_PLAN.md
SOURCE_SCOUT_AND_HARVEST_PLAN.md
QUALITY_AND_RETRY_PLAN.md
CONFIG_PERMISSION_AND_TOOL_SETUP_PLAN.md
GENERATION_AND_TOOL_REGISTRY_PLAN.md
KNOWLEDGE_AND_LEARNING_PLAN.md
PACKAGING_AND_PUBLISHING_PLAN.md
HUMAN_REVIEW_CONSOLE_PLAN.md
AUDIO_VISUAL_ASSET_SYSTEM_PLAN.md
ROADMAP_AND_HANDOFF_PLAN.md
```

Any new chat or coding agent should read these before coding.

---

## 2. No-Code Planning Remaining

Optional future planning docs:

```text
MMD_3D_ROUTE_PLAN.md
LONGFORM_VIDEO_ROUTE_PLAN.md
PLATFORM_SPECIFIC_API_NOTES.md
LOCAL_WEB_CONSOLE_UI_PLAN.md
TESTING_STRATEGY_PLAN.md
```

These can be written later when those areas become urgent.

---

## 3. Phase 0 Implementation Goal

Phase 0 should not implement generation, crawling, MMD, or platform upload.

It should implement:

- project directories;
- config loading;
- permissions loading;
- SQLite database;
- run creation;
- job creation;
- decision log;
- review item;
- tool setup item;
- basic manifests;
- CLI scripts to create run/job/review.

---

## 4. What Another AI May Do

If using another AI to generate base code, require it to:

1. Read all planning docs.
2. Implement only the requested phase.
3. Avoid fake APIs.
4. Use TODO interfaces for unavailable external tools.
5. Preserve directory layout.
6. Store decisions and review items.
7. Keep score weights configurable.
8. Write tests for core objects and permission checks.
9. Never jump to MMD or video generation unless asked.

---

## 5. What Another AI Must Not Do

Do not allow another AI to:

- invent external API responses;
- mix research/local/generated assets;
- hard-code paths;
- hard-code score weights;
- skip manifests;
- skip decision logs;
- delete local assets;
- silently auto-publish;
- implement all agents as expensive calls;
- ignore permission matrix;
- rewrite the project into an unrelated simple video generator.

---

## 6. Review Checklist for Generated Code

When code is generated, review:

- does it match object schema?
- does every action belong to a run?
- does every job have a directory?
- does every source/asset have manifest support?
- do permissions return allow/ask/deny?
- are review items written?
- are decision logs written?
- are score profiles config-driven?
- are external APIs interfaces/TODOs when not configured?
- are tests present?

---

## 7. Suggested Implementation Order

```text
1. Directory skeleton
2. Config loader
3. Permission matrix
4. Database schema
5. Run manager
6. Job manager
7. Decision logger
8. Review queue
9. Tool setup queue
10. Manifest helpers
11. CLI scripts
12. Tests
```

Only after this should Source Scout begin.

---

## 8. Handoff Prompt for New Chat

Use this prompt in a new chat:

```text
Read all planning documents in E:\影潮枢_Kairove before doing anything:
KAIROVE_PLAN.md,
CORE_OBJECTS_AND_SCHEMA_PLAN.md,
AGENT_ECOSYSTEM_PLAN.md,
FIRST_PRODUCTION_LINE_PLAN.md,
SOURCE_SCOUT_AND_HARVEST_PLAN.md,
QUALITY_AND_RETRY_PLAN.md,
CONFIG_PERMISSION_AND_TOOL_SETUP_PLAN.md,
GENERATION_AND_TOOL_REGISTRY_PLAN.md,
KNOWLEDGE_AND_LEARNING_PLAN.md,
PACKAGING_AND_PUBLISHING_PLAN.md,
HUMAN_REVIEW_CONSOLE_PLAN.md,
AUDIO_VISUAL_ASSET_SYSTEM_PLAN.md,
ROADMAP_AND_HANDOFF_PLAN.md.

Do not write code until I explicitly ask. If I ask for implementation, start only with Phase 0.
```

---

## 9. Project North Star

Kairove is not a prompt toy.

It is:

```text
trend-aware + format-aware + asset-aware + tool-aware + quality-aware + platform-aware + learning video production system
```

The first usable route is ordinary AI format reproduction. MMD/3D is a later specialized route.

