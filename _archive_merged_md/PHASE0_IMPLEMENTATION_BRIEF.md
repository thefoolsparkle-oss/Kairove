# Kairove Phase 0 Implementation Brief

## 0. Status

This is a planning document, not implementation code.

Current status:

```text
Phase 0: confirmed
Phase 0 implementation: not started
Code writing: not allowed until the user explicitly asks
```

Purpose:

```text
Make Phase 0 concrete enough to implement without accidentally building P1, generation, publishing, MMD/3D, or longform features.
```

---

## 1. Phase 0 Objective

Phase 0 builds Kairove's foundation layer.

In plain language:

```text
Kairove should be able to remember, record, resume, and explain future work.
```

P0 does not try to make a usable video pipeline.

P0 should only create the project skeleton and core data flow needed by later phases.

---

## 2. P0 Includes

P0 includes:

- project directory skeleton;
- config file skeletons;
- config loading and validation plan;
- permission capability matrix base;
- budget config base;
- risk policy config base;
- SQLite database base;
- Run object;
- Job object;
- DecisionLog object;
- ReviewItem object;
- ToolSetupItem object;
- source manifest stub;
- asset manifest stub;
- basic file path helpers;
- basic ID generation rules;
- basic tests;
- a Phase 0 completion report.

---

## 3. P0 Excludes

P0 must not implement:

- real web search;
- real platform crawling;
- source downloading;
- AI model calls;
- full agent ecosystem;
- full Regent behavior;
- Format Miner;
- Trend Analyst;
- generation tools;
- quality judging;
- packaging;
- publishing;
- browser automation;
- MMD/3D;
- longform;
- local web console.

P0 may create placeholders, config files, and setup items for later features, but it must not fake those features.

---

## 4. P0 Folder Layout

Recommended root layout after P0:

```text
E:\影潮枢_Kairove\
  config\
    system.yaml
    permissions.yaml
    budgets.yaml
    risk_policy.yaml
    tools.yaml
    agents.yaml
    user_preferences.yaml

    platforms\
      bilibili.yaml
      douyin.yaml
      xiaohongshu.yaml
      youtube.yaml

    route_profiles\
      ordinary_ai_format_video.yaml
      music_sync.yaml
      character_reenactment.yaml
      horror_atmosphere.yaml
      mmd_3d.yaml
      longform.yaml

    score_profiles\
      trend_video_v1.yaml
      quality_ordinary_ai_v1.yaml
      packaging_v1.yaml

  data\
    kairove.sqlite3
    migrations\
    schema_snapshots\

  runs\

  research_assets\
    sources\
    manifests\
    snapshots\
    covers\
    screenshots\
    comments\

  local_assets\
    user_provided\
    trained_voice\
    official_assets_curated_by_user\
    mmd_models\
    mmd_motions\
    mmd_stages\

  generated_assets\
    jobs\
    temp\
    final\

  reports\
    phase_reports\

  tests\
    fixtures\
    phase0\

  logs\
```

Important separation rule:

```text
research_assets = collected or referenced from outside
local_assets = user-owned/user-curated/user-trained material
generated_assets = produced by Kairove
```

P0 only creates these folders. It does not fill them with real production material.

---

## 5. P0 Config Files

P0 should create config files with safe defaults.

### 5.1 system.yaml

Purpose:

```text
Project identity, storage locations, default timezone, and run behavior.
```

Minimum fields:

```yaml
project:
  name_cn: "影潮枢"
  name_en: "Kairove"
  root: "E:/影潮枢_Kairove"

storage:
  database_path: "data/kairove.sqlite3"
  runs_dir: "runs"
  research_assets_dir: "research_assets"
  local_assets_dir: "local_assets"
  generated_assets_dir: "generated_assets"
  reports_dir: "reports"

defaults:
  timezone: "Australia/Sydney"
  language: "zh-CN"
  create_decision_logs: true
```

### 5.2 permissions.yaml

Purpose:

```text
Capability switches. Not linear levels.
```

Minimum capability groups:

```yaml
research:
  web_search: ask
  collect_metadata: allow
  download_reference_assets: ask
  fetch_comments: ask

asset:
  use_official_assets_directly: allow
  use_personal_creator_assets_directly: ask
  use_unknown_assets_directly: ask
  generate_visual_assets: ask
  generate_audio_assets: ask
  train_voice: ask

generation:
  generate_low_cost_drafts: ask
  generate_high_cost_candidates: ask
  batch_generation: ask
  retry_generation: ask

publish:
  create_package: ask
  upload_draft: ask
  schedule_publish: ask
  auto_publish: ask
  fetch_metrics: ask

system:
  modify_config: ask
  delete_generated_assets: ask
  delete_local_assets: deny
  run_background_tasks: ask
```

### 5.3 budgets.yaml

Purpose:

```text
Record budget limits even if the user leaves them unlimited.
```

Minimum fields:

```yaml
budget:
  daily_max_cost: null
  per_run_max_cost: null
  per_job_max_cost: null
  high_cost_confirmation_threshold: null
  max_parallel_generations: 1
  default_retry_rounds: 0
```

P0 does not enforce real API costs. It only loads and records these values.

### 5.4 risk_policy.yaml

Purpose:

```text
Encode current user policy in machine-readable form.
```

Minimum fields:

```yaml
risk_policy:
  official_misleading_risk:
    enabled: false

  official_assets:
    images: direct_use
    videos: direct_use
    music: direct_use
    sfx: direct_use
    require_review: false

  personal_creator_assets:
    direct_use: ask
    reference_use: allow
    style_analysis: allow

  unknown_source_assets:
    direct_use: ask
    reference_use: ask
    style_analysis: allow

  generated_assets:
    direct_use: allow
```

### 5.5 tools.yaml

Purpose:

```text
Record configured tools, missing tools, and setup status.
```

P0 only needs a skeleton:

```yaml
tools:
  search_engine:
    status: not_configured
  bilibili:
    status: not_configured
  youtube:
    status: not_configured
  douyin:
    status: not_configured
  xiaohongshu:
    status: not_configured
  video_generation:
    status: not_configured
  publishing:
    status: not_configured
```

---

## 6. P0 Database Scope

P0 should use SQLite first.

Minimum tables:

```text
runs
jobs
decision_logs
review_items
tool_setup_items
source_manifests
asset_manifests
config_snapshots
permission_snapshots
```

P0 can add migration tracking:

```text
schema_migrations
```

P0 should not create every future table if it makes implementation noisy. It can keep future objects in planning docs until needed.

---

## 7. P0 Core Objects

### 7.1 Run

P0 Run fields:

```json
{
  "run_id": "run_000001",
  "run_type": "planning | review | phase0_test",
  "trigger_type": "manual",
  "input_summary": "...",
  "status": "pending | running | waiting_for_user | failed | completed | abandoned",
  "created_by": "user | kairove_regent",
  "permission_snapshot_id": "perm_snap_000001",
  "config_snapshot_id": "cfg_snap_000001",
  "started_at": "...",
  "completed_at": null,
  "notes": ""
}
```

P0 rule:

```text
Every meaningful operation belongs to a Run.
```

### 7.2 Job

P0 Job fields:

```json
{
  "job_id": "job_000001",
  "run_id": "run_000001",
  "job_type": "ordinary_ai_format_video | music_sync | character_reenactment | horror | longform | mmd_3d | hybrid | placeholder",
  "title_working": "...",
  "status": "created | waiting_for_user | abandoned | failed | completed",
  "priority": "low | normal | high | urgent",
  "target_platforms": [],
  "job_dir": "generated_assets/jobs/job_000001",
  "created_at": "...",
  "updated_at": "...",
  "user_notes": ""
}
```

P0 does not process a Job into production. It only proves jobs can be created and recorded.

### 7.3 DecisionLog

P0 DecisionLog fields:

```json
{
  "decision_id": "dec_000001",
  "run_id": "run_000001",
  "job_id": null,
  "decision_type": "permission_check | config_load | object_created | user_review | setup_needed | error",
  "summary": "...",
  "reason": "...",
  "inputs": {},
  "outputs": {},
  "created_at": "..."
}
```

Rule:

```text
No silent important decisions.
```

### 7.4 ReviewItem

P0 ReviewItem fields:

```json
{
  "review_item_id": "review_000001",
  "run_id": "run_000001",
  "job_id": null,
  "review_type": "permission | source_policy | config_change | missing_info | manual_choice",
  "title": "...",
  "body": "...",
  "status": "pending | approved | rejected | resolved | cancelled",
  "options": [],
  "created_at": "...",
  "resolved_at": null
}
```

### 7.5 ToolSetupItem

P0 ToolSetupItem fields:

```json
{
  "setup_id": "setup_000001",
  "tool_id": "bilibili_scout",
  "missing": ["api_key_or_cookie"],
  "impact": "Cannot collect Bilibili metadata automatically yet.",
  "user_action_required": true,
  "priority": "low | normal | high | urgent",
  "status": "needed | requested | configured | tested | failed | deferred",
  "test_steps": [],
  "notes": ""
}
```

### 7.6 Manifest Stub

Source manifest stub:

```json
{
  "manifest_id": "manifest_src_stub_000001",
  "source_id": null,
  "original_url": null,
  "source_type": "unknown",
  "usage_policy": "unknown",
  "review_status": "pending",
  "local_files": [],
  "used_for": [],
  "created_at": "..."
}
```

Asset manifest stub:

```json
{
  "manifest_id": "manifest_asset_stub_000001",
  "asset_id": null,
  "asset_origin": "research | local | generated | unknown",
  "usage_policy": "unknown",
  "review_status": "pending",
  "local_path": null,
  "created_at": "..."
}
```

---

## 8. P0 Conceptual Command Shape

These are not final CLI commands. They describe future behavior.

Initialize project:

```text
kairove init
```

Validate config:

```text
kairove config validate
```

Create a test run:

```text
kairove run create --type phase0_test --summary "Phase 0 smoke test"
```

Create a placeholder job:

```text
kairove job create --run run_000001 --type ordinary_ai_format_video --title "placeholder"
```

Create a review item:

```text
kairove review create --run run_000001 --type permission --title "Example permission check"
```

Create a tool setup item:

```text
kairove setup create --tool bilibili_scout --missing api_key_or_cookie
```

Write manifest stubs:

```text
kairove manifest create-source-stub --run run_000001
kairove manifest create-asset-stub --run run_000001
```

Generate Phase 0 report:

```text
kairove phase0 report
```

---

## 9. P0 Run Directory Example

A Phase 0 smoke run should create:

```text
runs/run_000001/
  run.json
  config_snapshot.json
  permission_snapshot.json
  decision_log.jsonl
  review_items.jsonl
  tool_setup_items.jsonl
  manifest_stubs/
    source_manifest_stub.json
    asset_manifest_stub.json
  report.md
```

A placeholder job should create:

```text
generated_assets/jobs/job_000001/
  job.json
  decision_log.jsonl
  source_refs.json
  notes.md
```

`source_refs.json` can be empty in P0.

---

## 10. P0 Permission Behavior

P0 should implement permission lookup behavior but does not need advanced policy intelligence.

Permission result values:

```text
allow
ask
deny
allow_with_limits
missing
```

Example check output:

```json
{
  "capability": "research.web_search",
  "configured_value": "ask",
  "result": "ask",
  "decision": "create_review_item",
  "review_item_id": "review_000001"
}
```

Rules:

- `allow` permits the action and writes a DecisionLog.
- `ask` creates a ReviewItem.
- `deny` blocks the action and writes a DecisionLog.
- `allow_with_limits` requires checking relevant config limits.
- missing capability config should not silently allow.

---

## 11. P0 Test Plan

Required P0 tests:

```text
config loads
required config files exist
permission lookup returns allow/ask/deny/allow_with_limits/missing
SQLite initializes
Run can be created
Job can be created
DecisionLog can be written
ReviewItem can be created and resolved
ToolSetupItem can be created and updated
source manifest stub can be written
asset manifest stub can be written
run directory is created
job directory is created
Phase 0 report can be generated
```

P0 tests should not need network access.

P0 tests should not call paid APIs.

P0 tests should not create real videos.

---

## 12. P0 Acceptance Criteria

P0 is accepted when Kairove can:

1. initialize the folder skeleton;
2. create safe default configs;
3. validate config shape;
4. initialize SQLite;
5. create a Run;
6. create a Job;
7. write DecisionLog entries;
8. create and resolve ReviewItems;
9. create and update ToolSetupItems;
10. write source and asset manifest stubs;
11. create run and job directories;
12. generate a Phase 0 report;
13. pass all P0 tests.

---

## 13. P0 Failure Rules

P0 is not acceptable if:

- it writes generated assets into research_assets;
- it writes research downloads into local_assets;
- it allows unknown permissions by default;
- it creates jobs without run references;
- it creates meaningful actions without DecisionLog;
- it claims any real crawling/generation/publishing feature works;
- it requires network access to pass tests;
- it cannot resume or inspect a prior Run.

---

## 14. P0 Completion Report

P0 completion report should be written to:

```text
reports/phase_reports/phase0_completion.md
```

Report sections:

```text
1. Summary
2. Created directories
3. Config files created
4. Database tables created
5. Smoke run ID
6. Placeholder job ID
7. Decision logs written
8. Review item test
9. Tool setup item test
10. Manifest stub test
11. Test results
12. Known limitations
13. Next planning target
```

Known limitations should explicitly say:

```text
No real crawling, generation, QA, packaging, publishing, MMD/3D, or longform features are implemented in Phase 0.
```

---

## 15. P0 Ready-To-Code Checklist

P0 should not start coding until these are accepted:

- folder skeleton above is acceptable;
- config skeleton above is acceptable;
- SQLite is acceptable as first database;
- Run/Job/DecisionLog/ReviewItem/ToolSetupItem are the only required active objects;
- manifest stubs are enough for P0;
- P0 tests are offline only;
- P0 completion report is required;
- P0 does not include any real crawling or generation.

---

## 16. Next After P0

After P0 is complete, the next discussion target is still P1:

```text
Trend and Source Intelligence Foundation
```

But P1 should not start just because P0 is done. P1 should start only after the user confirms the P1 implementation brief.