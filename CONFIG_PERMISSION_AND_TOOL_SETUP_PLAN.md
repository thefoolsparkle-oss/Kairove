# Kairove Config, Permission, and Tool Setup Plan

## 0. Purpose

This document defines Kairove's configuration system, permission capability matrix, budget rules, tool setup queue, and API readiness workflow.

Kairove must be able to run automatically, but every action must be bounded by explicit permissions.

---

## 1. Configuration Layout

Suggested config tree:

```text
config/
  system.yaml
  permissions.yaml
  agents.yaml
  tools.yaml
  budgets.yaml
  risk_policy.yaml
  user_preferences.yaml

  platforms/
    bilibili.yaml
    douyin.yaml
    xiaohongshu.yaml
    youtube.yaml

  score_profiles/
    trend_video_v1.yaml
    quality_ordinary_ai_v1.yaml
    quality_music_sync_v1.yaml
    packaging_v1.yaml

  route_profiles/
    ordinary_ai_format_video.yaml
    music_sync.yaml
    character_reenactment.yaml
    horror_atmosphere.yaml
    longform.yaml
    mmd_3d.yaml
```

Config must be versioned. Important changes should create config history entries.

---

## 2. Permission Capability Matrix

Permissions are not a linear level system. They are independent capability switches.

Allowed states:

```text
allow
ask
deny
allow_with_limits
```

Example:

```yaml
permissions:
  research.web_search: allow
  research.collect_metadata: allow
  research.download_reference_assets: allow_with_limits
  research.fetch_comments: allow

  asset.use_official_assets_directly: allow
  asset.use_personal_creator_assets_directly: ask
  asset.use_unknown_assets_directly: ask
  asset.generate_visual_assets: allow
  asset.generate_audio_assets: allow
  asset.train_voice: ask

  generation.generate_low_cost_drafts: allow
  generation.generate_high_cost_candidates: ask
  generation.batch_generation: allow_with_limits
  generation.retry_generation: allow_with_limits

  publish.create_package: allow
  publish.upload_draft: ask
  publish.schedule_publish: ask
  publish.auto_publish: ask
  publish.fetch_metrics: allow
  publish.fetch_comments: allow

  system.modify_config: ask
  system.delete_generated_assets: ask
  system.delete_local_assets: deny
  system.run_background_tasks: allow
```

---

## 3. Permission Check Flow

Every meaningful action should pass:

```text
1. Required capability lookup
2. Permission state check
3. Budget check
4. Risk policy check
5. User review check if needed
6. Decision log write
```

Output:

```json
{
  "action": "generate_high_cost_candidates",
  "required_capabilities": ["generation.generate_high_cost_candidates"],
  "permission_result": "ask",
  "budget_result": "within_limit",
  "risk_result": "low",
  "decision": "create_review_item"
}
```

---

## 4. Budget Rules

Budget configuration:

```yaml
budget:
  daily_max_cost: null
  per_run_max_cost: null
  per_job_max_cost: null
  high_cost_confirmation_threshold: null
  max_parallel_generations: 4
  default_retry_rounds: 5
```

Budget can be disabled by setting values to null, but Kairove should still record estimated and actual cost when available.

Budget triggers:

- high-cost model;
- batch generation;
- retry rounds;
- video length expansion;
- platform API costs;
- voice training;
- local GPU-heavy processing.

---

## 5. Risk Policy Config

Current user policy:

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

  voice:
    user_trained: allow
    generated_original: allow
    official_character_clone: ask
    real_person_clone: ask
```

Risk policy should be configurable per platform and per route.

---

## 6. Tool Setup Queue

When Kairove cannot perform an action because a tool, API, account, permission, or local install is missing, it should create a setup item.

Fields:

```json
{
  "setup_id": "setup_000001",
  "tool_id": "douyin_publisher",
  "missing": [
    "developer app",
    "publish permission",
    "oauth token"
  ],
  "impact": "Can create manual publish package but cannot auto publish to Douyin.",
  "user_action_required": true,
  "priority": "high",
  "status": "pending | configured | tested | failed | skipped",
  "test_steps": [],
  "notes": ""
}
```

---

## 7. Tool Setup Lifecycle

```text
not_configured
  -> setup_item_created
  -> waiting_for_user
  -> configured
  -> test_pending
  -> tested_available / failed
```

After the user configures a tool, Kairove should run a safe test:

- auth test;
- minimal request;
- dry-run upload if platform publisher;
- no real publish unless permission allows.

---

## 8. Tool Config Example

```yaml
tools:
  kling_image_to_video:
    status: requires_api_key
    env_keys:
      - KLING_API_KEY
    cost_level: medium
    permission_required:
      - generation.generate_high_cost_candidates

  bilibili_publisher:
    status: requires_permission
    setup_requirements:
      - developer_account
      - app_credentials
      - oauth_token
    permission_required:
      - publish.upload_draft
      - publish.auto_publish
```

---

## 9. Agent Config

Agent config should define:

- enabled/disabled;
- model tier;
- max rounds;
- escalation triggers;
- output paths;
- fallback.

Example:

```yaml
agents:
  trend_analyst:
    enabled: true
    default_tier: medium
    escalate_on_low_confidence: true

  strong_judge:
    enabled: true
    default_tier: strong
    use_only_when_triggered: true
```

---

## 10. Acceptance Criteria

This system is ready when it can:

1. Load config files.
2. Check permissions for an action.
3. Produce allow/ask/deny decisions.
4. Create review items for ask decisions.
5. Track budget estimates.
6. Create tool setup items.
7. Update tool status after configuration.
8. Write decision logs for permission decisions.


---

## P0-B JSON Implementation Note

The planning layout uses YAML examples because YAML is comfortable for human editing.

The P0-B runtime currently writes JSON equivalents:

```text
config/system.json
config/permissions.json
config/tools.json
config/budgets.json
config/risk_policy.json
config/user_preferences.json
config/platforms/*.json
config/score_profiles/*.json
config/route_profiles/*.json
```

Reason:

```text
P0-B must run offline with the Python standard library only. JSON avoids adding a YAML dependency before the basic chain is proven.
```

This does not change the config contract. Later phases may add YAML support, import/export, config history, and a local UI editor while preserving the same logical fields.

---

## Cross-Phase Policy Alignment - 2026-06-06

Permission defaults from the accepted cross-phase policy:

```text
web_search: ask or allow_with_limits
metadata_collection: allow
asset_download: ask
official_asset_direct_use: allow
personal_creator_or_unknown_asset_direct_use: ask
low_cost_generation: allow_with_limits
high_cost_api: ask
auto_publish: ask
write_learning_rule: ask
delete_generated_assets: ask
delete_local_assets: deny
```

Budget defaults:

```text
Low-cost generation is a capability switch first.
Do not hardcode numeric P0-B paid-generation budgets.
Future budget layers: daily, per-job, per-run, high-cost-threshold.
High-cost routes ask before each round.
```

Auto-publish:

```text
Manual publish package remains default.
Auto-publish requires explicit user approval per platform, account, and permission switch.
No global default auto-publish.
```
