# Kairove Phase 9: Local Web Console and Human Review Center Plan

## 0. Status

Current status:

```text
Phase 9: detailed planning draft, not yet confirmed for implementation
Depends on: core objects, ReviewItems, DecisionLogs, reports, manifests, jobs, candidates, publish records, learning suggestions
Primary output: local operational console and review center
Related capability doc: LOCAL_WEB_CONSOLE_UI_PLAN.md
```

---

## 1. Purpose

Phase 9 builds the local control room for Kairove.

It answers:

```text
How does the user inspect what Kairove is doing, review uncertain decisions, compare candidates, adjust weights, manage tools, approve assets, control publishing, and inspect learning?
```

This is an operational interface, not a marketing site.

---

## 2. One-Line Scope

```text
Core objects + reports + review queue -> local dashboard, review center, candidate compare, asset/tool/permission/publish/learning UI
```

---

## 3. Must Include

```text
Dashboard:
  Active runs/jobs, blockers, pending reviews, setup gaps, candidates, publishing, learning suggestions.

Review Queue:
  Short actionable decision cards with evidence and options.

Candidate Compare:
  Side-by-side video/keyframe/score/prompt/asset/failure-tag comparison.

Trend and Format Views:
  Trend scorecards, source clusters, Format genomes, fatigue indicators.

Asset Provenance View:
  Source, policy, review status, usage, derived assets, manifests.

Tool Setup View:
  Capabilities, providers, auth/setup status, impact, tests.

Permission Matrix:
  Independent capability switches, not linear levels.

Weight Control:
  Inspect, edit, compare, version, and recalculate score profiles.

Publish Center:
  Payloads, manual packages, upload status, links, metrics.

Learning Center:
  Observations, suggestions, approved rules, pending weight changes.
```

---

## 4. Must Not Include

```text
marketing landing page
remote multi-user assumptions by default
hidden agent decisions
unlogged user overrides
irreversible permission changes without record
silent auto-publish controls
```

---

## 5. Inputs

```text
Run records
Job records
Source and Asset manifests
Format records
TrendScorecards
ProductionRecipe drafts
GenerationPlans
CandidateManifests
QualityReports
RetryPlans
PublishPackages
PublishRecords
ReviewItems
DecisionLogs
ToolSetupItems
ScoreProfiles
MemoryEntries
LearningSuggestions
```

---

## 6. Outputs

```text
local web app
review decisions
weight profile edits
permission updates
manual generation imports
candidate selection decisions
asset policy approvals
publish approvals
learning approvals
DecisionLogs
updated ReviewItems
Phase9UIReport
```

---

## 7. Workstreams

```text
P9-A Backend Read API for Core Objects
P9-B Review Queue and Decision Actions
P9-C Dashboard and Job Status
P9-D Candidate Compare
P9-E Source/Format/Trend Explorer
P9-F Asset Provenance and Policy UI
P9-G Tool Setup and Permission Matrix UI
P9-H Weight Control and Recalculation UI
P9-I Publish Center
P9-J Learning Center
P9-K Manual Generation Slot UI
P9-L UI Test and Accessibility Pass
```

---

## 8. Navigation Model

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

No page should be a dead end.

---

## 9. Dashboard

Dashboard sections:

```text
Active Jobs:
  status, current layer, blocker, next action.

Pending Reviews:
  asset policy, tool setup, weight change, expensive generation, publish approval.

Trend Opportunities:
  top formats with visible score components and freshness.

Generation Queue:
  running steps, waiting manual slots, failed steps.

Quality Queue:
  candidates awaiting QA, retry requested, final judge waiting.

Publish Queue:
  ready manual packages, uploaded drafts, failed payloads.

Learning Suggestions:
  pending suggestions, affected rules, confidence.
```

Fast actions:

```text
open
approve
reject
pause
retry
mark reviewed
send back
```

---

## 10. Review Queue

ReviewItem card schema:

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
  "priority": "normal"
}
```

Review actions:

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

`always_allow_similar` creates a permission/rule suggestion. It should not silently become broad policy.

---

## 11. Candidate Compare

Candidate Compare should support:

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

The chosen candidate writes a DecisionLog entry. Rejected candidates remain useful for P8 learning.

---

## 12. Trend and Format Explorer

Views:

```text
TrendOpportunityPacket list
Format cluster view
FormatGenome detail
TrendScorecard detail
ScoreExplanation detail
fatigue/lifecycle view
source evidence viewer
comment sentiment summary
```

Score panels must show:

```text
raw score
weight
weighted contribution
evidence
confidence
missing evidence
```

The user should be able to compare weight profiles and request recalculation.

---

## 13. Job Detail

Job detail sections:

```text
status and next action
source/provenance
P2 decision summary
P3 reproduction/semantic transfer/script/shot plan
P4 assets and blockers
P5 generation steps and prompt packages
P6 quality reports and retry history
P7 publish package
P8 learning entries
DecisionLog timeline
```

Job detail should show what is blocking progress and what action will unblock it.

---

## 14. Asset Provenance UI

Asset page fields:

```text
preview
asset type
folder class: research/local/generated
source URL or local origin
platform/source author
official/personal/unknown status
usage policy
review status
jobs used in
derived assets
hash
manifest path
```

Actions:

```text
approve direct use
approve reference only
reject
mark official
mark personal creator
mark unknown
request replacement
```

---

## 15. Tool Setup UI

Tool setup separates capability from provider:

```text
Capability: image_to_video
  Providers:
    kling: requires_api_key
    runway: not_configured
    local_comfyui: requires_local_install
```

Provider card shows:

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

After setup, Kairove should run a small capability test and update Tool Registry.

---

## 16. Permission Matrix UI

Permissions are independent switches.

Examples:

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

The user can enable any combination, such as `1,2,6`, without enabling intermediate capabilities.

---

## 17. Weight Control UI

Weight panel shows:

```text
current score profile
score components
raw component scores
weighted total
agent explanations
sample source evidence
last modified time
suggested changes
```

Actions:

```text
edit weight
save as profile
restore default
compare profiles
recalculate existing scorecards
approve suggested change
reject suggested change
```

Edits create versioned records and DecisionLogs.

---

## 18. Manual Generation Slot UI

Manual slot page shows:

```text
tool to use
setup needed
input assets
positive prompt
negative prompt
parameters
expected output type
drop folder
what QA checks next
```

Actions:

```text
copy prompt
open asset folder
mark external generation started
import output file
rerun registration
skip slot
switch route
```

Manual slots are a bridge, not a failure.

---

## 19. Publish Center

Publish Center shows:

```text
manual packages
platform payloads
cover variants
titles/descriptions/tags
readiness reports
upload/draft/publish status
published links
metrics
comments
```

Actions:

```text
open manual package
approve publish
upload draft
retry upload
mark manually published
enter manual metrics
fetch metrics if configured
```

---

## 20. Learning Center

Learning Center shows:

```text
observations
analysis
suggestions
approved rules
weight suggestions
tool performance
platform performance
format memory
user preference memory
```

Actions:

```text
approve suggestion
reject suggestion
edit and approve
request more samples
supersede rule
rollback rule
```

Learning UI must clearly distinguish suggestions from active rules.

---

## 21. Design Requirements

UI style:

```text
dense
operational
fast to scan
not card-heavy marketing
not decorative
not a landing page
```

Use appropriate controls:

```text
icons for tool buttons
segmented controls for modes
toggles/checkboxes for permission switches
sliders or numeric inputs for weights
menus for option sets
tabs for job subviews
tables for dense object lists
```

Text must fit on mobile and desktop. No overlapping panels.

---

## 22. Local-First Architecture

Initial assumptions:

```text
single personal operator
local machine
local database/files
browser at localhost
no remote multi-user auth by default
```

Later remote access can be added, but P9 should not redesign the whole backend around multi-user SaaS assumptions.

---

## 23. Storage and API

Suggested backend endpoints should expose:

```text
runs
jobs
sources
assets
formats
scorecards
reviews
tools
permissions
candidates
quality_reports
publish_records
learning_entries
```

Every write action must create a DecisionLog or ReviewItem update.

---

## 24. Tests

Required UI test areas:

```text
dashboard loads active jobs
review card approve/reject updates ReviewItem
candidate compare loads videos and reports
asset policy action updates manifest/review
weight edit creates new score profile version
tool setup status displays missing action
manual generation import registers candidate
publish center marks manual publish
learning suggestion approval creates approved_rule
```

Visual QA:

```text
desktop and mobile screenshots
no text overlap
video preview visible
tables usable
buttons fit labels
permission matrix not confusing
```

---

## 25. Acceptance Criteria

P9 is ready when the user can:

```text
see current Kairove state
review blocking items quickly
compare candidates
inspect source and asset provenance
edit permissions independently
inspect and adjust score weights
manage manual generation slots
approve or reject publish packages
inspect learning suggestions
see DecisionLogs behind major actions
```

---

## 26. Non-Acceptance

P9 is not acceptable if:

```text
it looks like a marketing landing page
it hides evidence behind summaries
it cannot resolve review items
it edits permissions without logs
it cannot compare candidates
it cannot show asset provenance
it cannot distinguish suggestions from approved rules
```

---

## 27. Confirmation Checklist

Before P9 implementation, confirm or revise:

```text
initial frontend stack
local server port policy
first pages to implement
whether browser automation is needed
how manual file import should work
which permissions are editable first
which score profiles are editable first
```

---

## Cross-Phase Policy Alignment - 2026-06-06

P9 long-term console shape:

```text
production board
review desk
creation/material/control console
```

P9 first version priority:

```text
prioritize production board
prioritize review desk
avoid decorative or marketing-style UI first
show suggestions separately from approved rules
show permission and weight changes with logs
support review for asset direct-use, high-cost routes, auto-publish, and deletion decisions
```
