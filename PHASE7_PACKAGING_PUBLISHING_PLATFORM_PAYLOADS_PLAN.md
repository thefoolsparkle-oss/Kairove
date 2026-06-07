# Kairove Phase 7: Packaging, Publishing, and Platform Payloads Plan

## 0. Status

Current status:

```text
Phase 7: detailed planning draft, not yet confirmed for implementation
Depends on: P6 selected final candidate
Primary output: publish packages, platform payloads, publish records
Related capability doc: PACKAGING_AND_PUBLISHING_PLAN.md
```

---

## 1. Purpose

Phase 7 turns a selected final candidate into platform-ready packaging and publish records.

It answers:

```text
What title, description, tags, cover, first frame, platform payload, upload method, and publish readiness state should this final video use?
```

Packaging is part of performance. It is not decoration at the end.

---

## 2. One-Line Scope

```text
FinalCandidate + QualityReport + Format/Trend Context -> PackagingReport + PlatformPayloads + PublishPackage + PublishRecords
```

---

## 3. Must Include

```text
Title/Description/Tag Agents:
  Generate and critique platform-aware metadata.

Cover and First-Frame Pipeline:
  Create/select covers, crop variants, and check first visible frame.

All-Platform Default:
  Prepare payloads for all configured platforms unless specifically blocked or unsuitable.

Platform Unsuitability Detection:
  Mark what is missing, blocked, risky, or unavailable per platform.

Publish Modes:
  manual package, draft upload, scheduled publish, auto publish if explicitly allowed.

Publish Records:
  Every upload/manual/skipped platform gets a record.

Feedback Hook:
  Prepare objects P8 can later use for metrics and learning.
```

---

## 4. Must Not Include

```text
silent auto-publish
fake upload status
publishing without package records
ignoring missing cover/title/tag requirements
platform selection as an excuse not to package broadly
learning weight changes
```

---

## 5. Inputs

```text
selected final candidate
final video asset
FinalQualityReport
FormatGenome
TrendScorecard
ReproductionPlan
SemanticTransferPlan
AssetResolutionReport
source/asset provenance
platform profiles
permission profile
packaging memory
user preferences
```

---

## 6. Outputs

```text
PackagingReport
TitleOptions
SelectedTitle
DescriptionOptions
SelectedDescription
TagSets
CoverCandidates
SelectedCover
FirstFrameReport
PlatformPayloads
PublishReadinessReport
ManualPublishPackage
PublishRecords
UploadLogs when applicable
ReviewItems
DecisionLogs
Phase7PublishReport
```

---

## 7. Workstreams

```text
P7-A Packaging Context Loader
P7-B Title/Description/Tag Council
P7-C Cover and First-Frame Council
P7-D Platform Payload Assembler
P7-E Platform Unsuitability Checker
P7-F Publish Readiness Gate
P7-G Manual Package Builder
P7-H Publisher Integration Runner
P7-I Publish Record Writer
P7-J Packaging Report and Tests
```

---

## 8. Packaging Execution Order

```text
1. Load final candidate and upstream reports.
2. Extract title/cover/first-frame hooks.
3. Generate title option pools.
4. Critique title options.
5. Generate descriptions and tags.
6. Generate or select cover candidates.
7. QA cover readability and platform crops.
8. Check first frame.
9. Assemble platform payloads for all target platforms.
10. Run unsuitability/blocker checks.
11. Write publish readiness report.
12. Build manual publish package.
13. If permission/tooling allows, upload draft/schedule/publish.
14. Register publish records.
```

---

## 9. Title, Description, and Tag Council

Agents:

```text
TitleSeedAgent
TitleStyleAgent
TitleSearchAgent
TitleCriticAgent
TitleSelectorAgent
DescriptionAgent
TagAgent
PlatformToneAgent
MetadataRiskAgent
```

Title record:

```json
{
  "title_id": "title_000001",
  "text": "...",
  "style": "trend_hook | character_hook | suspense | search | meme",
  "platform_fit": {},
  "risks": [],
  "reason": "Connects character hook with source format punchline."
}
```

Metadata must reflect the actual video. It should not describe a better video than the one selected.

---

## 10. Cover and First Frame

Cover sources:

```text
video_frame
generated
hybrid
manual_user_file
```

Cover candidate schema:

```json
{
  "cover_id": "cover_000001",
  "source": "video_frame | generated | hybrid | manual_user_file",
  "source_frame_timestamp": 3.42,
  "text_overlay": "...",
  "platform_variants": {},
  "qa": {
    "small_size_readability": 0.0,
    "face_visibility": 0.0,
    "crop_safety": 0.0,
    "visual_hook": 0.0
  }
}
```

FirstFrameReport checks:

```text
not black or confusing
consistent with cover/title
contains early hook or readable setup
no unwanted UI/watermark/text
safe for platform crop
```

If first frame is weak, P7 can request a light edit or P6/P5 revision.

---

## 11. Platform Payloads

Default platforms:

```text
bilibili
douyin
xiaohongshu
youtube
manual
```

PlatformPayload:

```json
{
  "platform": "bilibili",
  "decision": "publish | ready_manual | upload_draft | needs_review | blocked | skipped",
  "video_path": "...",
  "cover_path": "...",
  "title": "...",
  "description": "...",
  "tags": [],
  "category": "...",
  "publish_mode": "manual | draft | scheduled | auto",
  "adaptations": [],
  "risk_notes": [],
  "blocked_reasons": [],
  "required_user_actions": []
}
```

The default is to create payloads for all platforms. A platform is skipped only with a reason.

---

## 12. Platform Unsuitability Checks

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
quality_warning_platform_specific
```

This layer decides what is not suitable, blocked, or incomplete; it does not replace all-platform strategy.

---

## 13. Publish Modes

```text
manual_package:
  Always supported. Files and instructions are written for user upload.

draft_upload:
  Upload but do not publish.

scheduled_publish:
  Upload and schedule if platform supports it and permission allows.

auto_publish:
  Direct publish only when explicit permission allows it.
```

Auto-publish must check:

```text
platform integration configured
permission allows
publish package complete
risk/review blockers resolved
asset policy complete
quality pass exists
```

---

## 14. PublishReadinessReport

```json
{
  "publish_readiness_report_id": "pub_ready_000001",
  "job_id": "job_000001",
  "final_candidate_id": "candidate_003",
  "overall_status": "ready_manual | ready_draft | ready_auto | needs_review | blocked",
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

---

## 15. Publish Records

PublishRecord:

```json
{
  "publish_record_id": "pub_000001",
  "job_id": "job_000001",
  "platform": "douyin",
  "method": "manual | official_api | browser_automation",
  "status": "not_started | ready_manual | uploading | uploaded_draft | scheduled | published | failed | needs_user_action | skipped",
  "platform_item_id": null,
  "url": null,
  "payload_path": "...",
  "error_message": null,
  "created_at": "..."
}
```

Manual publishing still creates records so P8 can receive manually entered metrics later.

---

## 16. Manual Publish Package

Layout:

```text
manual_publish_package/
  final_video.mp4
  cover/
    cover_master.png
    bilibili.png
    douyin.png
    xiaohongshu.png
    youtube.png
  titles/
  descriptions/
  tags/
  platform_payloads/
  source_and_asset_provenance.md
  publish_readiness_report.json
  upload_instructions.md
```

This package should be usable even with no platform API configured.

---

## 17. Review Triggers

Create ReviewItems for:

```text
publish permission required
platform payload incomplete
cover/title disagreement
asset policy unresolved
quality selected with warnings
high audit risk
manual platform login/setup needed
auto-publish requested but permission missing
```

---

## 18. Storage Layout

```text
generated_assets/jobs/job_000001/publish/
  packaging_report.md
  titles/
  descriptions/
  tags/
  covers/
  platform_payloads/
  publish_readiness_report.json
  manual_publish_package/
  publish_records.jsonl
  upload_logs/
```

---

## 19. Tests

Fixture groups:

```text
candidate ready for all platforms
missing cover
weak first frame
manual package only
Bilibili upload configured
Douyin upload missing auth
platform-specific ratio issue
auto-publish permission denied
quality selected with warnings
```

Required tests:

```text
loads selected final candidate
creates title/description/tag options
selects title and tags
creates or selects cover
checks first frame
creates payloads for all configured platforms
marks unsuitable platforms with reason
builds manual publish package
creates publish records
never fakes upload status
blocks auto-publish without permission
```

---

## 20. Acceptance Criteria

P7 is ready when Kairove can:

```text
package a selected candidate for platforms
create titles/descriptions/tags/covers
assemble all-platform payloads
identify blocked/unsuitable platforms
create manual publish package
upload draft/publish only when configured and permitted
write publish records
handoff publish records to P8
pass fixture-based tests
```

---

## 21. Non-Acceptance

P7 is not acceptable if:

```text
it only packages for one platform without reason
it auto-publishes silently
it claims upload success without platform confirmation
it omits publish records for manual packages
it hides missing cover/title/tag issues
it changes final video content without QA handoff
```

---

## 22. Confirmation Checklist

Before P7 implementation, confirm or revise:

```text
initial target platforms
which platforms can use API/browser/manual mode
whether draft upload is allowed
whether auto-publish is allowed
cover generation behavior
manual package folder shape
metrics collection handoff to P8
```

---

## Cross-Phase Policy Alignment - 2026-06-06

P7 platform and language defaults:

```text
P0-B primary platforms:
  Bilibili
  Douyin
  Xiaohongshu
  YouTube Shorts

Long-term expandable stubs:
  TikTok
  Kuaishou
  Instagram Reels

Titles/descriptions/tags:
  Chinese primary version.
  YouTube Shorts may receive English auxiliary metadata.
```

Publishing policy:

```text
Default output remains manual publish package.
Auto-publish may be enabled later only after user approval.
Auto-publish must be enabled separately per platform, account, and permission switch.
No global default auto-publish.
```
