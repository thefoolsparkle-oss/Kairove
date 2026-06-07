# Kairove Packaging and Publishing Plan

## 0. Purpose

This document defines how Kairove creates titles, descriptions, tags, covers, first frames, platform payloads, publish packages, and publishing records.

Packaging is not a minor final step. It is part of video performance.

---

## 1. Packaging Council

Inputs:

- final video;
- format card;
- trend scorecard;
- reproduction plan;
- quality report;
- target platforms;
- platform profiles;
- packaging feedback memory.

Outputs:

- title options;
- selected title;
- description;
- tags;
- cover candidates;
- selected cover;
- first-frame notes;
- pinned comment;
- platform payloads.

---

## 2. Packaging Agents

```text
TitleAgent
TitleCriticAgent
DescriptionAgent
TagAgent
CoverConceptAgent
CoverGeneratorAgent
CoverCriticAgent
FirstFrameAgent
PinnedCommentAgent
SeriesAgent
PlatformPayloadAssembler
```

These agents should work in passes:

```text
1. Load video context
2. Generate options
3. Critique options
4. Select or combine
5. Create per-platform payloads
6. Write packaging report
```

---

## 3. Title Strategy

Title options can include:

- trend hook;
- character hook;
- suspense hook;
- meme hook;
- search-friendly title;
- platform-native style.

Title critique checks:

- too AI-like;
- too flat;
- too long;
- too misleading;
- wrong platform tone;
- risk tags.

---

## 4. Cover Strategy

Cover candidates:

- character close-up;
- conflict moment;
- subtitle big-text cover;
- horror atmosphere cover;
- meme punchline cover;
- platform-specific crop.

Cover QA:

- readable at small size;
- face not blocked;
- text not too dense;
- no bad crop;
- platform ratio;
- no unexpected watermark;
- visual appeal.

---

## 5. Tags and Description

TagAgent should generate:

- platform tags;
- topic tags;
- fandom tags;
- format tags;
- music tags if relevant;
- AI/video style tags.

It should avoid:

- irrelevant tags;
- misleading tags;
- tags that increase unwanted risk.

---

## 6. Default All-Platform Policy

Kairove should prepare all platform payloads by default.

It should only skip or pause a platform when:

- packaging missing;
- platform API missing and manual package disabled;
- platform-specific risk high;
- language/package not available;
- user permission requires confirmation.

---

## 7. Platform Payload

```json
{
  "platform": "bilibili",
  "decision": "publish | skip | needs_packaging_change | ask_user",
  "video_path": "...",
  "cover_path": "...",
  "title": "...",
  "description": "...",
  "tags": [],
  "category": "...",
  "publish_mode": "manual | draft | scheduled | auto",
  "adaptations": [],
  "risk_notes": []
}
```

---

## 8. Publish Package Layout

```text
publish_package/
  final_video.mp4
  cover_master.png
  title_options.json
  selected_title.txt
  description.txt
  tags.json
  platform_payloads/
    bilibili.json
    douyin.json
    xiaohongshu.json
    youtube.json
  publish_readiness_report.json
  risk_review.json
  upload_log.json
```

---

## 9. Publisher Integrations

Methods:

```text
official_api
browser_automation
manual_package
```

Each platform should support:

- capability check;
- auth check;
- prepare payload;
- upload draft;
- publish;
- schedule;
- fetch status;
- fetch metrics;
- fetch comments.

If a platform is not configured, Kairove creates a tool setup item and still writes a manual publish package.

---

## 10. Publish Records

```json
{
  "publish_record_id": "pub_000001",
  "job_id": "job_000001",
  "platform": "douyin",
  "method": "official_api",
  "status": "uploaded_draft",
  "platform_item_id": "...",
  "url": "...",
  "error_message": null
}
```

---

## 11. Feedback Collection

After publishing, collect:

- views;
- likes;
- comments;
- shares;
- favorites;
- completion rate if available;
- follower gain;
- audit status;
- comment sentiment.

Feedback writes to:

- Platform Feedback Memory;
- Format Knowledge;
- Packaging Learning;
- Trend Analyst;
- Scoring Engine.

---

## 12. Acceptance Criteria

Packaging and publishing is ready when it can:

1. Generate title options.
2. Generate descriptions and tags.
3. Generate or select cover candidates.
4. Produce per-platform payloads.
5. Create manual publish package.
6. Record platform capability gaps.
7. Create publish records.
8. Fetch or manually record metrics.
9. Write packaging learning entries.
---

## 13. Packaging Operating Contract

Packaging Council starts after a candidate is selected by Quality Council or manually approved by the user. It should package for all configured target platforms by default, then mark only unsuitable or blocked platforms as paused.

Inputs:

```text
final_candidate_id
final_video_path
format_card_id
trend_scorecard_id
semantic_transfer_plan_id
quality_report_id
asset_manifest_id
platform_profiles
packaging_memory
permission_profile
```

Outputs:

```text
packaging_report.md
title_options.json
selected_title.json
description_options.json
selected_description.json
tag_sets.json
cover_candidates.json
selected_cover.json
platform_payloads/
publish_readiness_report.json
manual_publish_package/
```

Packaging is allowed to reject a candidate for publishing if the title/cover/first-frame cannot honestly represent the video, if required platform fields cannot be created, or if the selected video quality is too weak for public release.

---

## 14. Packaging Execution Order

```text
1. Load final video and all upstream reports.
2. Extract usable moments for title, cover, and first frame.
3. Generate title option pools.
4. Critique title option pools.
5. Generate description and tag sets.
6. Generate or select cover candidates.
7. QA cover readability and crop.
8. Assemble per-platform payloads.
9. Run platform unsuitability checks.
10. Write publish readiness report.
11. If allowed, upload draft or publish.
12. Register publish records.
```

The council should not decide `which platform fits best` as a replacement for publishing strategy. The default is all platforms. Its real job is to detect what is unsuitable, missing, or blocked per platform.

---

## 15. Title Agent Passes

Title creation should run in several passes:

```text
TitleSeedAgent:
  Generates many raw titles from format, trend, character, and punchline.

TitleStyleAgent:
  Produces platform-native variants without changing the video meaning.

TitleSearchAgent:
  Adds searchable terms when useful.

TitleCriticAgent:
  Removes AI-flavored, flat, misleading, overlong, or wrong-tone titles.

TitleSelectorAgent:
  Selects final title and keeps backups.
```

Title records:

```json
{
  "title_id": "title_000001",
  "text": "...",
  "style": "trend_hook | character_hook | suspense | search | meme",
  "platform_fit": {
    "bilibili": 8.2,
    "douyin": 7.6
  },
  "risks": [],
  "reason": "Connects character hook with source format punchline."
}
```

The final title must connect to the actual video content and should not require viewers to already know internal production notes.

---

## 16. Cover and First-Frame Pipeline

Cover pipeline:

```text
1. Extract candidate frames from final video.
2. Ask CoverConceptAgent for cover concepts.
3. Choose frame-based, generated, or hybrid cover route.
4. Produce cover candidates.
5. Run cover QA.
6. Crop per platform.
7. Store master and platform variants.
```

Cover candidate record:

```json
{
  "cover_id": "cover_000001",
  "source": "video_frame | generated | hybrid",
  "source_frame_timestamp": 3.42,
  "text_overlay": "...",
  "platform_variants": {
    "bilibili": "cover_bilibili.png",
    "douyin": "cover_douyin.png"
  },
  "qa": {
    "small_size_readability": 8.0,
    "face_visibility": 9.0,
    "crop_safety": 8.5,
    "visual_hook": 7.8
  }
}
```

FirstFrameAgent checks the first visible second of the video. If the first frame is weak, black, visually confusing, or mismatched with the cover, it should request an edit before packaging finishes.

---

## 17. Platform Unsuitability Checks

Default decision is `publish`. A platform becomes paused only for a specific reason.

Unsuitability reasons:

```text
missing_required_payload
cover_ratio_unavailable
video_ratio_unusable
manual_or_api_upload_unavailable
platform_audit_risk_high
metadata_language_mismatch
file_size_or_duration_blocked
title_or_tag_policy_problem
user_permission_required
```

Decision schema:

```json
{
  "platform": "douyin",
  "decision": "publish",
  "blocked_reasons": [],
  "warnings": ["manual upload required until account integration exists"],
  "required_user_actions": [],
  "payload_path": "platform_payloads/douyin.json"
}
```

Even when automatic upload is unavailable, Kairove should create a complete manual package.

---

## 18. Upload Modes

Publishing methods:

```text
manual_package:
  Always supported. Kairove writes files and instructions for the user.

draft_upload:
  Upload but do not publish. Useful when account/API allows draft creation.

scheduled_publish:
  Upload and schedule if platform supports it and permission allows.

auto_publish:
  Direct publish only when explicit permission allows it.
```

Each platform integration must declare its supported modes.

```json
{
  "platform": "bilibili",
  "supports": {
    "manual_package": true,
    "draft_upload": true,
    "scheduled_publish": false,
    "auto_publish": false,
    "metrics_fetch": true,
    "comment_fetch": true
  },
  "status": "requires_account_login"
}
```

---

## 19. Publish Readiness Report

```json
{
  "job_id": "job_000001",
  "final_candidate_id": "candidate_003",
  "overall_status": "ready_manual | ready_auto | needs_review | blocked",
  "platforms": [],
  "title_selected": true,
  "description_selected": true,
  "cover_selected": true,
  "tags_selected": true,
  "quality_report_passed": true,
  "asset_policy_review_complete": true,
  "missing_items": [],
  "warnings": [],
  "created_at": "..."
}
```

The report should be readable in the local console and saved inside the publish package.

---

## 20. Feedback Loop Contract

After publishing, Packaging Council and Knowledge System should receive feedback in stages:

```text
T+1h early pulse if available
T+24h first useful result
T+72h short-term result
T+7d stable result
```

Collected feedback should be linked to:

```text
format_card
trend_scorecard
semantic_transfer_plan
title_id
cover_id
tag_set_id
platform_payload
quality_report
publish_record
```

The system should not conclude too much from one video. Strong learning suggestions require sample size, confidence, and comparison against similar past jobs.

---

## 21. Phase 0 Publishing Scope

Phase 0 should support manual publishing packages before platform automation.

Minimum real chain:

```text
final candidate -> title/description/tag options -> selected packaging -> cover candidate -> per-platform payload json -> manual publish folder -> publish record placeholder
```

API upload, browser automation, scheduling, and metric fetching can be added after the manual package path works.

---

## Cross-Phase Policy Alignment - 2026-06-06

Platform and language defaults:

```text
P0-B primary platforms: Bilibili, Douyin, Xiaohongshu, YouTube Shorts.
Long-term expandable stubs: TikTok, Kuaishou, Instagram Reels.
Titles/descriptions/tags: Chinese primary.
YouTube Shorts may receive English auxiliary metadata.
```

Publishing:

```text
Manual publish package remains default.
Auto-publish may be enabled later only after user approval.
Auto-publish must be enabled separately per platform, account, and permission switch.
No global default auto-publish.
```
