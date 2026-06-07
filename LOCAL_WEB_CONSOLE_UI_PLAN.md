# Kairove Local Web Console UI Plan

## 0. Purpose

This document defines the future local Web Console for Kairove.

The console is not required for Phase 0, but Kairove will need it because the system has many review items, candidates, tools, permissions, and learning reports.

---

## 1. Design Principles

- Dense, utilitarian, operational interface.
- No marketing landing page.
- Prioritize review, comparison, status, and control.
- Everything should link back to source, manifest, decision log, or report.
- User should be able to approve/reject quickly.

---

## 2. Main Pages

### 2.1 Dashboard

Shows:

- active runs;
- active jobs;
- pending reviews;
- tool setup needs;
- best trend opportunities;
- recently generated candidates;
- publish status;
- learning suggestions.

### 2.2 Trend Explorer

Shows:

- discovered formats;
- trend scorecards;
- source clusters;
- similar videos;
- comments summary;
- fatigue indicators.

### 2.3 Format Library

Shows:

- format cards;
- format genomes;
- lifecycle;
- successful transfers;
- failed transfers;
- recommended routes.

### 2.4 Job Detail

Shows:

- job status;
- source references;
- reproduction plan;
- production recipe;
- council outputs;
- candidates;
- quality reports;
- retry history;
- publish package.

### 2.5 Candidate Compare

Side-by-side:

- video preview;
- keyframes;
- score;
- failure tags;
- prompts;
- generation steps;
- cost;
- agent notes.

Actions:

- select;
- reject;
- retry;
- ask Regent;
- send to review.

### 2.6 Review Queue

Decision cards for:

- assets;
- risk;
- tool setup;
- publish approval;
- weight changes;
- character mapping;
- high-cost generation.

### 2.7 Asset Provenance

Shows:

- asset preview;
- source URL;
- source type;
- usage policy;
- review status;
- jobs used in;
- manifest.

### 2.8 Tool Setup

Shows:

- available tools;
- missing API keys;
- missing permissions;
- auth status;
- test buttons;
- impact of missing tools.

### 2.9 Permission Matrix

Allows editing:

- research permissions;
- asset permissions;
- generation permissions;
- publish permissions;
- system permissions.

### 2.10 Publish Center

Shows:

- publish packages;
- platform payloads;
- upload status;
- published links;
- metrics;
- comments.

### 2.11 Learning Reports

Shows:

- observations;
- suggestions;
- approved rules;
- weight suggestions;
- tool performance;
- platform performance.

---

## 3. UI Objects

Reusable components:

- decision card;
- scorecard panel;
- failure tag list;
- source provenance panel;
- video comparison grid;
- timeline/step viewer;
- permission toggle matrix;
- tool status badge;
- review action buttons.

---

## 4. Acceptance Criteria

Console is useful when user can:

1. See what Kairove is doing.
2. Review blocking items quickly.
3. Compare candidates.
4. Inspect asset provenance.
5. Edit permissions and score weights.
6. See tool setup gaps.
7. Approve publish packages.
8. Read learning suggestions.

---

## 5. Human Review Console Contract (Merged)

Merged from `HUMAN_REVIEW_CONSOLE_PLAN.md`.

The local web console should include a review queue for:

```text
permissions
source policy
asset usage
score/weight changes
tool setup gaps
candidate selection
publish confirmation
learning suggestions
```

Decision cards should show:

```text
what is being asked
why Kairove is asking
available options
risk/impact
related source/job/asset
DecisionLog link
```

The review console is part of the local web console plan, not a separate root planning document.
---

## 6. Console Operating Contract

The local web console is the user's control room. It should expose the system's decisions instead of hiding them behind agent summaries.

Core requirements:

```text
show current state
show why the system made a decision
show source/provenance for every important item
allow approve/reject/edit/escalate actions
allow score weight inspection and adjustment
allow permission switches by independent capability
allow retry and route-change decisions
allow manual file drop for external tools
```

The console should be local-first. It can later support remote access, but the first design should assume one personal operator using the machine directly.

---

## 7. Navigation Model

Primary navigation:

```text
Dashboard
Discovery
Formats
Jobs
Assets
Generation
Quality
Publish
Tools
Permissions
Learning
Settings
```

Every object page should link sideways:

```text
source -> format -> job -> assets -> generation steps -> candidate -> quality report -> publish package -> feedback -> learning entries
```

No page should be a dead end. If a user sees a score, asset, failure tag, or agent claim, they should be able to click into evidence.

---

## 8. Dashboard Detail

Dashboard sections:

```text
Active Jobs:
  status, current agent/layer, blocker, next action.

Pending Reviews:
  asset policy, tool setup, weight change, expensive generation, publish approval.

Trend Opportunities:
  top formats with visible score components and freshness.

Generation Queue:
  currently running steps, waiting manual slots, failed steps.

Quality Queue:
  candidates awaiting QA, retry requested, final judge waiting.

Publish Queue:
  ready manual packages, uploaded drafts, failed platform payloads.

Learning Suggestions:
  pending suggestions, affected rules, confidence.
```

Dashboard actions should be fast:

```text
open
approve
reject
pause
retry
mark reviewed
```

---

## 9. Review Queue Contract

Each review card must include:

```json
{
  "review_item_id": "review_000001",
  "review_type": "asset_policy | tool_setup | weight_change | candidate_selection | publish | learning_suggestion",
  "title": "...",
  "why_needed": "...",
  "recommended_action": "...",
  "options": [],
  "impact": "...",
  "risk_notes": [],
  "related_objects": [],
  "created_by_agent": "...",
  "deadline_or_priority": "normal"
}
```

Review options should be explicit:

```text
approve
reject
approve_once
always_allow_similar
send_back_to_agent
request_more_evidence
manual_override
pause_job
```

`always_allow_similar` must create a learning suggestion or permission update record. It should not silently become a broad rule.

---

## 10. Weight Control UI

Trend and quality weights must be visible and adjustable.

Weight panel should show:

```text
current weight profile
score components
raw component scores
weighted total
agent explanations
sample source evidence
last modified time
who/what suggested changes
```

User actions:

```text
edit weight
save as profile
restore default
compare profiles
recalculate existing scorecards
approve suggested change
reject suggested change
```

Weight edits should create a versioned record:

```json
{
  "weight_profile_id": "trend_default_v3",
  "changed_fields": {
    "heat": {"from": 0.24, "to": 0.30},
    "growth": {"from": 0.22, "to": 0.28}
  },
  "reason": "User approved stronger emphasis on heat and growth.",
  "applies_to": "future_and_recalculate_on_request"
}
```

---

## 11. Manual Generation Slot UI

Some tools may not be automated at first. The console should support manual generation slots so Phase 0 can still complete the production chain.

Slot UI shows:

```text
tool to use
account/API/setup needed if any
input assets
positive prompt
negative prompt
parameters
expected output type
where to drop output
what QA will check next
```

Actions:

```text
copy prompt
open asset folder
mark external generation started
import output file
rerun registration
skip this slot
switch route
```

Manual slots are not a failure. They are a bridge until the corresponding API or local automation exists.

---

## 12. Candidate Compare Detail

Candidate comparison should support:

```text
sync playback
frame stepping
side-by-side stills
score overlay toggle
failure tag overlay
prompt diff
asset diff
generation parameter diff
cost/time diff
agent notes
user notes
```

Decision actions:

```text
select as final
reject
request retry same route
request retry different route
request prompt revision
request asset replacement
send to higher QA
```

The chosen candidate should write a decision log entry with the reason. Rejected candidates remain useful for learning and failure clustering.

---

## 13. Asset Provenance Detail

Asset page should show:

```text
preview
asset type
folder class: research/local/generated
source URL or local origin
source platform
source author/official status
license/policy state
review status
used in jobs
derived assets
hash
manifest path
```

Review actions:

```text
approve direct use
approve reference only
reject
mark official
mark personal creator
mark unknown
request replacement
```

The user policy currently allows direct use of official game/anime/PV/music/SFX assets, while personal creator and unknown assets require review.

---

## 14. Tool Setup Detail

Tool setup page should separate capabilities from specific providers.

```text
Capability: image_to_video
  Providers:
    kling: requires_api_key
    runway: not_configured
    local_comfyui: requires_local_install
```

Each provider card should show:

```text
status
what it enables
routes affected
required user action
test connection button
last failure
historical quality
cost/speed notes
```

When the user completes setup, the console should run a small capability test and update Tool Registry.

---

## 15. Permission Matrix Detail

Permissions are independent switches, not linear levels.

Example capabilities:

```text
autonomous_web_search
autonomous_download_research_assets
autonomous_download_official_assets
use_official_assets_directly
use_personal_creator_assets_after_review
train_voice_from_local_material
run_paid_generation
run_high_cost_generation
auto_upload_draft
auto_publish
fetch_platform_metrics
apply_learning_suggestions
```

The user can enable any combination, such as `1,2,6`, without enabling everything below or above it.

---

## 16. UI Acceptance for Phase 0

Phase 0 does not require the full console, but it should define the data shape so a console can be built without redesigning the backend.

Phase 0 UI substitute can be:

```text
static job report pages
JSON manifests
manual review markdown files
folder-based manual generation slots
simple local dashboard later
```

The important part is that every decision is already recorded in a way the future UI can display.

---

## Cross-Phase Policy Alignment - 2026-06-06

Long-term console shape:

```text
production board
review desk
creation/material/control console
```

Initial P9 priority:

```text
production board first
review desk first
avoid decorative or marketing-style UI first
show suggestions separately from approved rules
show permission and weight changes with logs
support review for direct-use assets, high-cost routes, auto-publish, and deletion decisions
```
