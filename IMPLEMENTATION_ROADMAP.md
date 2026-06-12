# Kairove Implementation Roadmap

## 0. Correction

Latest P1 status correction - 2026-06-12:

| Scope | Skeleton | Live capability | Acceptance |
| --- | --- | --- | --- |
| confirmed | implemented and verified | public metadata/evidence live scouts connected for Search/Bilibili/YouTube/Wiki; Douyin/XHS probe-only | public metadata P1 acceptance complete with declared gaps |

This status overrides older shorthand. "P1 implemented and verified" previously meant the offline-safe skeleton only. As of `run_000034`, P1 is accepted for the public metadata/evidence Trend and Source Intelligence foundation, not for deep platform automation.

This roadmap is **not** a fixed Phase 0 -> Phase 20 implementation plan.

Earlier wording incorrectly made future capability areas look like agreed implementation phases. That was wrong.

Current rule:

```text
Only phases that have been discussed and accepted should be numbered as phases.
Future modules are capability areas, not scheduled phases.
```

Current status:

```text
Phase 0 discussed boundary: P0-B Lowest Complete Production Chain; implementation is not authorized.
P0-A Foundation Skeleton is included inside P0-B as a proposed foundation subset, not a separate competing phase.
Phase 1 public metadata/evidence implementation is accepted with declared gaps.
Phase 2 through Phase 11 detailed planning docs exist; none of P2-P11 are confirmed for implementation.
```

---

## 1. Roadmap Philosophy

Kairove is too large to plan as a simple linear list of twenty phases.

Implementation planning should use three labels:

```text
Phase:
  A committed implementation stage that has been discussed and accepted.

Workstream:
  A large area inside a phase that may need its own breakdown.

Future Capability Area:
  A planned capability that is not yet scheduled as a phase.
```

No new numbered phase should be added without explicit discussion.

---

## 2. Discussed Phase 0 Shape: P0-B Lowest Complete Production Chain

P0-B is the currently discussed Phase 0 boundary, pending final re-confirmation before coding.

The purpose of P0-B is to prove that Kairove can honestly move one ordinary AI video project through a complete recorded chain, even when some automation is still manual.

P0-B is not a toy MVP and not the full system. It is the smallest real production spine.

One-line scope:

```text
approved source/format -> route plan -> prompt package -> manual generation slot -> candidate registration -> basic QA -> retry decision -> packaging -> manual publish package
```

Automation gaps are handled by:

```text
manual slots
setup items
explicit missing capability reports
```

They must not be hidden behind fake API output.

---

## 3. Why P0 Is Not Foundation-Only

A foundation-only P0 would create folders, database tables, and manifests, but it would not prove that the system can produce anything.

The user explicitly objected to this kind of useless MVP. Therefore P0 must include one narrow but complete production chain.

P0-A still matters, but only as the foundation subset inside P0-B.

---

## 4. P0-B Chain

```text
approved source or manual seed
-> source manifest
-> simple format observation
-> semantic transfer brief
-> route plan
-> asset requirement report
-> prompt package
-> manual generation slot or configured tool call
-> candidate registration
-> basic technical QA
-> basic semantic QA report
-> retry decision
-> packaging options
-> manual publish package
-> phase report
```

This chain is for ordinary AI video first. It does not prioritize MMD/3D or longform.

---

## 5. P0-B Includes

```text
foundation:
  folder skeleton
  config skeletons
  permission capability matrix
  budget/risk policy config
  SQLite base
  Run / Job / DecisionLog / ReviewItem / ToolSetupItem
  source and asset manifest stubs

intake and provenance:
  manual seed / approved source intake
  source manifest
  source provenance
  source usage policy
  ReviewItem when source or asset policy is uncertain
  autonomous-source interfaces only as capability/setup placeholders if unconfigured

planning:
  simple Format Observation, not full Format Miner
  visible score stub with editable weights
  semantic transfer brief
  route plan
  Asset Resolver report shape
  asset requirement report

generation handoff:
  Generation Manager manual slot
  prompt package
  missing tool/capability ToolSetupItem

candidate and QA:
  user-provided generated candidate import
  candidate manifest
  generated asset manifest update
  basic technical QA report
  basic semantic QA report
  structured failure tags
  retry/pass decision

packaging and reporting:
  all-platform manual publish package by default
  platform payload status per platform
  source and asset provenance summary
  self-check report after output generation
  phase0_completion.md
  offline and manual-slot tests
```

---

## 6. P0-B Excludes

```text
full autonomous platform crawling
large-scale trend database
full Format Miner evolution
full Trend Analyst scoring
full multi-agent ecosystem
paid or automatic AI video API requirement
real auto-publish requirement
MMD/3D route implementation
longform route implementation
voice training automation
platform feedback learning loop
self-applying learning rules
full local web console
automatic source downloading unless explicitly supported
automatic asset search or asset repair
automatic cover generation requirement
platform metrics fetching
strong judge / final judge automation
multi-candidate optimization loop
```

Excluded does not mean forgotten. These are future capability areas or candidate Phase 1+ discussion topics.

---

## 7. P0-B Acceptance Criteria

P0-B is complete when Kairove can:

```text
foundation:
  initialize required folders
  initialize SQLite database
  load and validate config
  load permission capability switches
  create a Run
  create a Job attached to that Run

intake:
  intake one approved source or manual seed
  record source provenance
  record usage policy
  create ReviewItem for unknown/personal/uncertain source or asset policy
  keep research assets, local assets, and generated assets separate

planning:
  produce a simple format observation
  create a visible weighted score stub
  allow score weights to be inspected and changed by config/data, not hidden logic
  create a semantic transfer brief
  create a route plan
  create an asset requirement report before generation planning
  create DecisionLog entries for meaningful choices

generation handoff:
  create prompt package
  create manual generation slot
  create ToolSetupItem when automation is unavailable
  explain where the user-provided generated output should be placed or imported

candidate:
  import one user-provided generated video into the manual slot
  register candidate asset under generated assets
  link candidate to job, source, prompt package, and generation step
  record candidate provenance and hash/file metadata where possible

QA and retry:
  run basic technical QA checks and write report
  run basic semantic QA checks and write report
  produce structured failure tags
  create explicit retry/pass decision
  block packaging if no QA report exists

packaging:
  create title/description/tag/cover package data
  create platform payloads for all planned platforms by default
  mark each platform as ready, needs review, blocked, or skipped with reason
  write manual publish package
  avoid auto-publish
  write self-check report that verifies key files, JSON parseability, QA/package honesty, platform payload states, fixture warnings, and human-first entry files

reporting and tests:
  write complete phase0_completion.md
  pass tests that do not require external APIs, network crawling, video generation, or real publishing
```

---

## 7A. P0-B Locked Operating Defaults - 2026-06-06

These defaults are locked for P0-B only. P1/P2 will separately discuss real trend samples, Trend Analyst weights, Format Miner growth, and hot-versus-overused judgment.

P0-B tone and format range:

```text
Do not lock one specific topic or fandom.
Default direction is ordinary AI video reproduction/transfer of recent popular formats.
Supported format taste includes short jokes, abstract short drama, character substitution, plot reversal, spoken/copywriting adaptation, and AI animation skits.
P0-B does not judge whether something is a real hit format.
P0-B only proves the chain can carry these format types.
```

P0-B default start:

```text
Main acceptance chain starts from text seed.
URL intake remains structurally reserved.
Local reference folder intake remains structurally reserved.
Manual format selection remains structurally reserved.
P0-B acceptance requires the text-seed chain to run through.
```

P0-B platform defaults:

```text
Primary P0-B package platforms:
  Bilibili
  Douyin
  Xiaohongshu
  YouTube Shorts

Platform stubs, not full P0-B support:
  TikTok
  Kuaishou
  Instagram Reels
```

P0-B pass standard:

```text
Pass means the chain is complete, traceable, and usable for a human to continue.
Source, asset, candidate, QA, retry/pass decision, and publish package must be connected.
Pass does not mean the video is close to publishable or likely to become a hit.
Deep semantic QA, multi-agent judgment, and generation quality optimization belong to P5/P6.
```

Minimum official-asset provenance:

```text
source_url
local_path
work_title
character_or_asset_name
official_owner_or_account
usage
download_or_record_date
linked_job
usage_mode: direct_use / reference / derivative_clip
```

Default permission switches:

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

P0-B visible score dimensions:

```text
popularity
growth_speed
reproduction_clarity
production_feasibility
asset_availability
fatigue_or_overused_risk
comment_sentiment
platform_fit
```

Weight policy:

```text
popularity and growth_speed start with higher weights.
fatigue_or_overused_risk is not based only on volume.
fatigue_or_overused_risk must consider comment_sentiment, recent growth, and interaction quality.
Weights must remain visible, configurable, versioned, and recalculable.
Major weight changes require user approval.
```

Must ask the user before:

```text
direct use of personal creator or unknown assets
auto-publishing
turning learning suggestions into rules
high-cost API calls
large-scale downloads
major weight changes
main route switches
deleting local assets
```

P0-B automation posture:

```text
P0-B should be controllable before it is autonomous.
It must honestly run one complete chain.
It must not pretend it can already fully automate hotspot discovery, generation, quality judgment, or publishing.
```

---

## 8. P0-B Failure Rules

```text
no fake crawler output
no fake AI generation result
no unrecorded source/asset usage
no mixed asset folders
no unknown permission silently allowed
no job without run reference
no meaningful action without DecisionLog
no hidden weight changes
no auto-publish
no treating manual slot as final automation
no network/API/video generation requirement for tests
```

---

## 9. P0-A Foundation Subset Inside P0-B

P0-A is no longer a competing Phase 0 option. It is the first subset that P0-B must build.

P0-A subset includes:

```text
folder skeleton
config loading
permission capability matrix base
SQLite database base
Run object
Job object
DecisionLog
ReviewItem
ToolSetupItem
basic manifest helpers
basic tests
```

P0-A subset acceptance:

```text
initialize folders
create default configs
validate config shape
initialize SQLite
create Run and Job
write DecisionLog
create/resolve ReviewItem
create/update ToolSetupItem
write source/asset manifest stubs
create run/job directories
```

---

## 10. Discussed Phase 1 Direction: Trend and Source Intelligence Foundation

Phase 1 broad direction has been discussed. Implementation is not authorized.

The discussed purpose of Phase 1:

```text
Teach Kairove to find, save, understand, and preliminarily organize trending source material.
```

Internal P1 workstreams:

```text
P1-A Source Scout design and first usable scouts
P1-B Harvester and source manifests
P1-C Video Understanding reports
P1-D Format observation and early grouping
P1-E Trend scoring draft
P1-F Review/reporting for collected material
```

These are internal P1 workstreams, not separate phases.

Accepted P1 defaults:

1. Platform order: broad web search -> Bilibili -> YouTube -> wiki/official pages -> Douyin/XHS capability probes.
2. Autonomous search is the core route; ManualSeedScout is auxiliary.
3. Evidence must be enough to create weak/promising/strong Format Observations without claiming full Format Miner confidence.
4. Understanding Report v1 is required before Format Observation v1.
5. Opportunity Scoring v1 belongs in P1, but full Trend Analyst does not.
6. Research Review Report is the first review surface; full Web UI remains future work.
7. Missing platform/API/login capability creates ToolSetupItems instead of fake outputs.

---

## 11. Detailed Draft Capability Areas

The capability areas that were previously future-only have now been mapped and detailed as P2-P11 planning drafts.

Important rule:

```text
Detailed planning draft does not mean implementation approval.
```

Current detailed draft phase areas:

```text
P2: Format Intelligence and Opportunity Decision
P3: Reproduction Planning, Semantic Transfer, Script and Direction
P4: Asset Resolution, Character/World Knowledge, Audio/Visual Material System
P5: Generation Tool Registry, Production Routes, Candidate Generation
P6: Quality Council, Retry Engine, Final Judge
P7: Packaging, Publishing, Platform Payloads
P8: Feedback Learning, Long-Term Memory, Weight Optimization
P9: Local Web Console and Human Review Center
P10: MMD/3D Specialized Route
P11: Longform Specialized Route
```

They should be implemented only after the user explicitly confirms or schedules the relevant phase.

---

## 12. Planning Rule Going Forward

Before each implementation phase:

1. Discuss the phase scope.
2. Decide what is included.
3. Decide what is excluded.
4. Write or update the phase brief.
5. Then implement only that phase.

Phase completion report should include:

```text
Completed
How to run
Tests
Outputs
Not implemented yet
Next discussion target
```

---

## 13. Current Next Target

P0-B is the confirmed Phase 0 shape. Implementation was explicitly authorized and completed for the current offline chain.

P0-B1 through P0-B7 are internal implementation order, not separate user approval gates.

Current no-code planning target:

```text
P0-B final include/exclude list and acceptance criteria are locked. Phase 1 public metadata/evidence foundation is implemented and accepted with declared gaps. Do not move to P2 until the user explicitly says to start P2.
```

P0-B internal workstream order:

```text
P0-B1 Foundation subset
P0-B2 Source/manual seed intake and provenance
P0-B3 Simple format observation, semantic transfer brief, and asset requirement report
P0-B4 Prompt package, manual generation slot, and candidate import
P0-B5 Basic QA and retry/pass decision
P0-B6 Packaging and manual publish package
P0-B7 Phase report and tests
```

This workstream list is not a new phase list. It is the proposed internal build order for P0-B if implementation is later approved, now detailed in sections 14-22.
---

## 14. P0-B Workstream Operating Rules

P0-B workstreams are internal build order, not new phases.

Rules:

```text
1. Each workstream must leave runnable, inspectable state behind.
2. Each workstream must write DecisionLog entries for meaningful choices.
3. Each workstream must avoid fake external results.
4. Each workstream must be testable without paid APIs, crawling, or public publishing.
5. Each workstream may create setup items for missing tools instead of blocking silently.
6. Each workstream must preserve source/asset provenance.
7. Each workstream must keep research assets, local assets, and generated assets separate.
```

P0-B implementation should prefer boring, durable interfaces over clever agent behavior. Agents can be simulated by deterministic modules or structured manual reports in P0-B, as long as the future agent interfaces are not blocked.

---

## 15. P0-B1 Foundation Subset

Purpose:

```text
Create the project skeleton, database, config, permission system, IDs, object lifecycle, and report/log foundations that every later step depends on.
```

Inputs:

```text
project root
P0-B planning scope
config defaults
permission defaults
schema plan
```

Deliverables:

```text
folder skeleton
config files
SQLite database
schema migration base
Run model
Job model
DecisionLog model
ReviewItem model
ToolSetupItem model
SourceManifest stub
AssetManifest stub
ID generator
path resolver
phase report writer base
offline test harness
```

Minimum folders:

```text
config/
data/
runs/
research_assets/
local_assets/
generated_assets/
reports/phase_reports/
tests/fixtures/
logs/
```

Acceptance:

```text
kairove can initialize the project
config loads and validates
permissions return allow/ask/deny
SQLite initializes
Run can be created and resumed
Job can be created under a Run
DecisionLog can be written
ReviewItem can be created/resolved
ToolSetupItem can be created/updated
source/asset manifest stubs can be written
all P0-B1 tests pass offline
```

Non-goals:

```text
real source search
real generation
real QA agents
real publishing
full UI
```

Exit gate:

```text
A fresh project root can be initialized and a dummy Run/Job can be created with valid logs and manifests.
```

---

## 16. P0-B2 Source / Manual Seed Intake And Provenance

Purpose:

```text
Allow P0-B to start from one approved source or manual seed while preserving provenance and review state.
```

Inputs:

```text
manual URL
manual local file
manual text seed
optional source metadata
user approval state
```

Deliverables:

```text
SourceCandidate record
Source record
source_manifest.json
source_snapshot folder when available
source approval ReviewItem when needed
DecisionLog for intake choice
basic source report
```

Supported P0-B intake modes:

```text
manual_url
manual_local_file
manual_text_seed
manual_reference_folder
```

Autonomous scouting interfaces may exist, but they should only produce setup items or empty capability reports unless actually implemented.

Acceptance:

```text
user can register one source or seed
source has stable id
source has provenance fields
source has usage policy fields
source can link to a Job
unknown/personal creator source creates ReviewItem
official source can be marked direct-use under current user policy
no downloaded asset is mixed into local or generated folders
```

Non-goals:

```text
broad web search
platform crawling
comment harvesting
trend ranking
large source clustering
```

Exit gate:

```text
One approved source can be attached to a production job with complete provenance.
```

---

## 17. P0-B3 Simple Format Observation, Semantic Transfer Brief, And Asset Requirement Report

Purpose:

```text
Convert the source into a small structured production understanding without pretending the full Format Miner exists.
```

Inputs:

```text
Source record
source manifest
manual notes if provided
job goal
optional target character/style idea
```

Deliverables:

```text
format_observation.json
score_stub.json
semantic_transfer_brief.md
asset_requirement_report.json
production_recipe_draft.json
DecisionLog entries
ReviewItems for unclear mapping or risky assets
```

P0-B simple format observation fields:

```text
format_label
source_summary
core_hook
scene_structure
character_roles
audio_role
text/subtitle_role
visual_style_notes
estimated_duration_policy
why_this_can_be_reproduced
known_uncertainties
```

Score stub fields:

```text
interest_guess
production_feasibility
asset_readiness
format_clarity
risk_or_review_need
weights_visible
```

Semantic transfer brief fields:

```text
what_to_preserve
what_to_change
role_mapping
style_mapping
setting_mapping
joke/conflict/emotion mapping
what_must_not_change
what_needs_user_review
```

Asset requirement report fields:

```text
required_assets
optional_assets
available_assets
missing_assets
searchable_assets
needs_user_provided_assets
policy_review_needed
```

Acceptance:

```text
job has a readable format observation
job has a semantic transfer brief
job has visible score components and weights
job has asset requirements before generation planning
uncertainty is recorded instead of hidden
full Format Miner is not claimed
```

Non-goals:

```text
full format genome
trend lifecycle scoring
multi-agent Format Miner
automatic character wiki resolution unless separately implemented
```

Exit gate:

```text
A human can read the brief and understand what the generated video is trying to imitate, transform, and avoid.
```

---

## 18. P0-B4 Prompt Package, Manual Generation Slot, And Candidate Import

Purpose:

```text
Prepare exact generation instructions and support manual external generation without pretending automation exists.
```

Inputs:

```text
production_recipe_draft
semantic_transfer_brief
asset_requirement_report
available assets
configured tool registry
permission profile
```

Deliverables:

```text
generation_plan.json
prompt_package/
manual_generation_slot.json
generation_steps.jsonl
candidate_import_folder
candidate_manifest.json
asset manifest update for imported output
ToolSetupItem for unavailable automation
DecisionLog entries
```

Prompt package layout:

```text
prompt_package/
  positive_prompt.txt
  negative_prompt.txt
  prompt_context.json
  tool_parameters.json
  human_summary.md
  source_links.json
```

Manual generation slot must show:

```text
which external tool or capability to use
input assets
positive prompt
negative prompt
parameters
expected output type
where to place output
what quality checks will run next
```

Candidate import rules:

```text
imported file must receive candidate_id
candidate must link to generation_step_id
candidate must link to prompt_package_id
candidate must link to source and asset chain
import must not overwrite existing candidate
hash should be recorded if possible
```

Acceptance:

```text
prompt package is complete
manual slot is understandable
missing automation creates ToolSetupItem
user-provided output can be imported
candidate record is created
candidate asset is registered under generated_assets
candidate links to source, prompt, generation step, and job
```

Non-goals:

```text
automatic paid API integration
multi-candidate generation strategy
advanced route switching
MMD/3D generation
```

Exit gate:

```text
One generated video file can be manually dropped in, imported, and treated as a registered candidate.
```

---

## 19. P0-B5 Basic QA And Retry / Pass Decision

Purpose:

```text
Check the imported candidate enough to decide whether to pass, retry, revise prompt, replace asset, or ask user.
```

Inputs:

```text
candidate record
candidate video file
prompt package
semantic transfer brief
format observation
asset manifest
```

Deliverables:

```text
technical_quality_report.json
semantic_quality_report.md
failure_tags.json
retry_decision.json
ReviewItems for subjective or blocking issues
DecisionLog entries
```

P0-B technical QA checks:

```text
file exists
readable media container
duration extracted if possible
resolution extracted if possible
fps extracted if possible
basic audio presence check if possible
file size recorded
```

P0-B semantic QA checks:

```text
matches intended format roughly
preserves core hook roughly
target role/style mapping is understandable
major visual failure noted
subtitle/text issue noted
asset/source mismatch noted
obvious low-quality issue noted
```

Retry decision values:

```text
pass_to_packaging
retry_same_prompt
revise_prompt
replace_asset
switch_route
ask_user
abandon_job
```

Acceptance:

```text
candidate cannot pass without a QA report
QA report links to candidate and job
failure tags are structured
retry/pass decision is explicit
DecisionLog explains why
manual user judgment can override with record
```

Non-goals:

```text
full multi-layer QA council
expensive visual-language judging by default
strong judge / final judge automation
frame-perfect semantic validation
```

Exit gate:

```text
One candidate is either passed to packaging or given a concrete retry/revision reason.
```

---

## 20. P0-B6 Packaging And Manual Publish Package

Purpose:

```text
Turn the passed candidate into a practical all-platform manual publish package.
```

Inputs:

```text
passed candidate
QA report
format observation
semantic transfer brief
source manifest
asset manifest
platform profile defaults
```

Deliverables:

```text
title_options.json
selected_title.txt
description.txt
tags.json
cover_notes.md or cover file
platform_payloads/
publish_readiness_report.json
manual_publish_package/
publish_record_placeholder.json
DecisionLog entries
```

P0-B platform payloads should default to all planned platforms, but mark each as:

```text
ready_manual
needs_cover
needs_user_review
blocked_missing_data
blocked_tool_setup
skipped_with_reason
```

Manual publish package layout:

```text
manual_publish_package/
  final_video.mp4
  cover/
  titles/
  descriptions/
  tags/
  platform_payloads/
  source_and_asset_provenance.md
  publish_readiness_report.json
```

Acceptance:

```text
final video is copied or referenced safely
at least one title option exists
selected title exists
basic description exists
tags exist
cover file or cover instruction exists
platform payload json exists
publish readiness report exists
manual package is usable by the user
no auto-publish occurs
```

Non-goals:

```text
automatic platform upload
scheduled publishing
metrics fetching
advanced cover generation
platform-specific growth optimization
```

Exit gate:

```text
The user can open the manual publish package and have the files/text needed to post the video manually.
```

---

## 21. P0-B7 Phase Report And Tests

Purpose:

```text
Prove P0-B works, record what is complete, and leave a clean handoff for the next implementation discussion.
```

Inputs:

```text
all P0-B artifacts
all P0-B test results
known setup items
known failures
manual notes
```

Deliverables:

```text
phase0_completion.md
phase0_artifact_index.json
p0b_test_report.json
known_gaps.md
next_discussion_notes.md
```

Phase report must include:

```text
what was built
how to run it
what files are produced
what tests passed
what external tools are not automated
what manual steps remain
what was intentionally excluded
which candidate Phase 1 questions are still open
```

Required test groups:

```text
P0-A foundation subset tests
source intake/provenance tests
format observation and semantic transfer fixture tests
asset requirement report tests
prompt package/manual slot tests
candidate import tests
basic QA and retry decision tests
manual publish package tests
end-to-end manual production-chain dry run
```

Acceptance:

```text
all required tests pass without paid API or public publishing
phase0_completion.md exists
known gaps are explicit
P0-B artifacts can be inspected from the job directory
next implementation target is stated without inventing unscheduled phases
```

Non-goals:

```text
claiming the whole product is usable
claiming P1 is implemented
hiding missing API/tool setup
```

Exit gate:

```text
A new chat or future coder can read the phase report and understand exactly what P0-B can and cannot do.
```

---

## 22. P0-B Implementation Dependency Order

Hard dependency order:

```text
P0-B1 -> P0-B2 -> P0-B3 -> P0-B4 -> P0-B5 -> P0-B6 -> P0-B7
```

Why:

```text
P0-B2 needs Run/Job/manifest foundations.
P0-B3 needs an approved source.
P0-B4 needs a transfer brief and asset requirements.
P0-B5 needs an imported candidate.
P0-B6 needs a passed candidate.
P0-B7 needs artifacts and tests from all previous workstreams.
```

Parallel-friendly work:

```text
P0-B1 config/schema/tests can be designed together.
P0-B3 schema fields can be drafted while P0-B2 is being implemented.
P0-B6 package layout can be prepared before QA exists, but cannot be accepted until QA passes a candidate.
```

Implementation should still merge in dependency order to avoid half-connected objects.
---

## 23. P0-B Batch Record

P0-B implementation was explicitly authorized and implemented as one continuous Phase 0 batch for the current offline chain.

Meaning:

```text
P0-B1 through P0-B7 are internal implementation order.
They are not separate phases.
They are not separate planning approval gates.
They should be built together only after explicit implementation approval, until the full P0-B acceptance criteria can pass.
```

During approved implementation, the system should still preserve internal checkpoints, tests, and reports for each workstream. The phase-level implementation approval covers the batch, while scope changes still require user direction.

P0-B completion is judged only by the full P0-B acceptance criteria:

```text
source/seed intake
provenance
format observation
semantic transfer brief
asset requirement report
prompt package
manual generation slot
candidate import
basic QA
retry/pass decision
manual publish package
phase report
offline/manual-slot tests
```

P1 public metadata/evidence foundation is implemented and accepted with declared gaps. No P2+ coding order is active until the user explicitly authorizes implementation of a named phase.
---

## 24. Documentation During Coding Policy

When coding begins, do not create a new root Markdown file for every change.

Default policy:

```text
Code and tests are the implementation source of truth.
Canonical planning docs are the contract source of truth.
Git history is the detailed change history once the project is initialized as a repository.
Phase reports are the human-readable completion records.
```

Update docs in place when:

```text
scope changes
accepted behavior changes
data contracts change
folder layout changes
permissions/risk policy changes
test acceptance changes
external tool setup expectations change
```

Do not update planning docs for:

```text
small refactors that do not change behavior
internal renames that do not affect contracts
formatting-only changes
routine bug fixes already covered by tests
```

Implementation logging should live outside the root doc set:

```text
reports/phase_reports/phase0_completion.md
reports/phase_reports/phase1_completion.md
reports/implementation_logs/...
```

The root planning docs should remain canonical and low-count. If a new document is needed, prefer placing it under `reports/`, `runs/`, or another generated-output folder instead of adding another root `.md`.

Coding batch workflow:

```text
1. Read the relevant canonical docs.
2. Implement code and tests.
3. If code changes the plan/contract, update the canonical doc in the same batch.
4. Record generated outputs in reports or run folders.
5. Summarize changed code, changed docs, and tests in the final response.
```
---

## 25. Phase 2 Planning: Format Intelligence And Opportunity Decision

Phase 2 is the next numbered planning document after the discussed Phase 1 direction.

Status:

```text
Phase 2 detailed planning doc exists.
Phase 2 scope is not yet confirmed for implementation.
P3-P11 detailed planning docs now exist, but are not confirmed for implementation.
```

Canonical document:

```text
PHASE2_FORMAT_INTELLIGENCE_AND_OPPORTUNITY_DECISION_PLAN.md
```

One-line scope:

```text
TrendOpportunityPacket + FormatObservation -> Format + FormatGenome + TrendScorecard -> ProductionStartPacket for P0-B
```

Do not keep Phase 2's full contract in this roadmap. Edit the canonical P2 document instead.
---

## 26. Global Phase Map

This map assigns major capability areas to rough phases so planning does not sprawl or overlap.

Status rules:

```text
discussed_boundary:
  The phase can be discussed as a named boundary, but coding is not authorized.

implementation_authorized:
  The user has explicitly approved coding for this named phase. No phase currently has this status.

detailed_planning_doc_exists:
  Canonical detailed phase document exists, but scope is not confirmed for implementation.

```

The map is allowed to change before implementation of each phase. P3-P11 have now been detailed as planning drafts; do not create P12+ phase docs unless the user asks.

---

## 27. Phase Map Summary

```text
P0: Lowest Complete Production Chain
P1: Trend and Source Intelligence
P2: Format Intelligence and Opportunity Decision
P3: Reproduction Planning, Semantic Transfer, Script and Direction
P4: Asset Resolution, Character/World Knowledge, Audio/Visual Material System
P5: Generation Tool Registry, Production Routes, Candidate Generation
P6: Quality Council, Retry Engine, Final Judge
P7: Packaging, Publishing, Platform Payloads
P8: Feedback Learning, Long-Term Memory, Weight Optimization
P9: Local Web Console and Human Review Center
P10: MMD/3D Specialized Route
P11: Longform Specialized Route
```

---

## 28. P0 Map: Lowest Complete Production Chain

Status:

```text
discussed_boundary
detailed in this roadmap sections 2-9 and 13-24
implementation_not_authorized
```

Goal:

```text
Prove Kairove can move one ordinary AI video project through a complete recorded chain, even when generation is manual-slot based.
```

Inputs:

```text
approved source
manual seed
local asset/reference
```

Outputs:

```text
job
source manifest
simple format observation
semantic transfer brief
asset requirement report
prompt package
manual generation slot
candidate import
basic QA report
retry/pass decision
manual publish package
phase0_completion.md
```

Must include:

```text
foundation objects
folder/config/database skeleton
DecisionLog and ReviewItem
manual generation slot
manual publish package
P0-B tests
```

Must not include:

```text
full autonomous scouting
full Format Miner
full Trend Analyst
real auto-publish
MMD/3D
longform
```

---

## 29. P1 Map: Trend and Source Intelligence

Status:

```text
discussed scope
canonical doc: PHASE1_TREND_SOURCE_INTELLIGENCE_PLAN.md
implementation_not_authorized
```

Goal:

```text
Let Kairove autonomously discover current video/source opportunities and prepare evidence-backed TrendOpportunityPackets.
```

Inputs:

```text
research goal
current date/time
platform/search configuration
optional target fandom/character/audio
```

Outputs:

```text
QueryPlan
ScoutResult
SourceCandidate
Source
SourceManifest
UnderstandingReport
FormatObservation v1
TrendOpportunityPacket
ResearchReviewReport
ToolSetupItem
```

Must include:

```text
autonomous search first
SearchEngineScout
BilibiliScout v1
YouTubeScout v1
Wiki/Official Source Scout
Douyin/XHS capability probe
ManualSeedScout auxiliary only
Harvester v1
Opportunity Scoring v1
```

Must not include:

```text
video generation
full Format Miner
full Trend Analyst
production execution
platform publishing
```

---

## 30. P2 Map: Format Intelligence and Opportunity Decision

Status:

```text
detailed_planning_doc_exists
canonical doc: PHASE2_FORMAT_INTELLIGENCE_AND_OPPORTUNITY_DECISION_PLAN.md
scope not yet confirmed for implementation
```

Goal:

```text
Convert P1 opportunities into stable formats, scorecards, and production decisions.
```

Inputs:

```text
TrendOpportunityPacket
FormatObservation
UnderstandingReport
SourceManifest
source clusters
comment sentiment summaries
AI method guesses
ScoreProfile
```

Outputs:

```text
Format
FormatGenome v1
FormatClusterReport
TrendScorecard v1
ScoreExplanationReport
ProductionOpportunityDecision
ProductionStartPacket for P0-B
ReviewItem
DecisionLog
```

Must include:

```text
format promotion
format genome v1
cluster/variant analysis
fatigue interpretation
visible score weights
Regent Gate 1
ProductionStartPacket
```

Must not include:

```text
new broad crawling beyond P1
video generation
full script council
full asset resolver
publishing
fake evidence
hidden score changes
```

---

## 31. P3 Map: Reproduction Planning, Semantic Transfer, Script and Direction

Status:

```text
detailed_planning_doc_exists
canonical doc: PHASE3_REPRODUCTION_PLANNING_SEMANTIC_TRANSFER_SCRIPT_DIRECTION_PLAN.md
scope not yet confirmed for implementation
```

Goal:

```text
Turn selected ProductionStartPackets into reproduction strategies, semantic transfer plans, scripts, storyboards, and direction packages.
```

Inputs:

```text
ProductionStartPacket
FormatGenome
TrendScorecard
representative sources
user preferences
character/world target
```

Outputs:

```text
ReproductionPlan
SemanticTransferPlan
ScriptPackage
Storyboard / ShotPlan
DirectorBrief
ProductionRecipe draft
ReviewItems for subjective choices
```

Must include:

```text
format preservation rules
role/character/world mapping
anti-AI-flavor script checks
platform-neutral production intent
clear handoff to Asset Resolver and Generation Manager
```

Must not include:

```text
final generation execution
full asset downloading/training
auto-publish
MMD/3D-specific implementation
longform-specific implementation
```

---

## 32. P4 Map: Asset Resolution, Character/World Knowledge, Audio/Visual Material System

Status:

```text
detailed_planning_doc_exists
canonical doc: PHASE4_ASSET_RESOLUTION_CHARACTER_WORLD_AUDIO_VISUAL_PLAN.md
scope not yet confirmed for implementation
```

Goal:

```text
Resolve what materials the production needs, locate or request assets, manage provenance, and build character/world/audio/visual knowledge required for generation.
```

Inputs:

```text
ProductionRecipe
SemanticTransferPlan
ScriptPackage
asset requirements
local asset inventory
official/wiki references
```

Outputs:

```text
AssetResolutionReport
CharacterReferencePack
WorldReferencePack
AudioRequirementReport
Voice/tts/training setup items
VisualReferencePack
AssetReviewItems
updated asset manifests
```

Must include:

```text
web asset search where allowed
local asset use
official/personal/unknown policy handling
missing asset escalation
reference provenance
separate research/local/generated asset folders
```

Must not include:

```text
unreviewed personal creator direct-use
fake asset availability
final video generation
platform publishing
```

---

## 33. P5 Map: Generation Tool Registry, Production Routes, Candidate Generation

Status:

```text
detailed_planning_doc_exists
canonical doc: PHASE5_GENERATION_ROUTES_AND_CANDIDATE_PLAN.md
scope not yet confirmed for implementation
```

Goal:

```text
Choose production routes, build generation plans, call configured tools or manual slots, and register candidates.
```

Inputs:

```text
ProductionRecipe
AssetResolutionReport
Tool registry
PromptPackage
permission profile
budget profile
```

Outputs:

```text
GenerationPlan
ToolSelectionReport
PromptPackages
GenerationSteps
Candidate videos/images/audio
CandidateManifest
ToolSetupItems
failure reports
```

Must include:

```text
route selection
fallback route planning
tool capability registry
manual slot support
candidate registration
output asset provenance
```

Must not include:

```text
unconfigured API pretending to work
untracked generated files
QA final approval
publishing
```

---

## 34. P6 Map: Quality Council, Retry Engine, Final Judge

Status:

```text
detailed_planning_doc_exists
canonical doc: PHASE6_QUALITY_RETRY_FINAL_JUDGE_PLAN.md
scope not yet confirmed for implementation
```

Goal:

```text
Evaluate candidates, detect failures, run retry decisions, and select final publishable outputs.
```

Inputs:

```text
CandidateManifest
GenerationSteps
PromptPackages
ProductionRecipe
source/reference evidence
quality profiles
```

Outputs:

```text
TechnicalQualityReport
SemanticQualityReport
FailureTags
RetryPlan
RevisionRequest
FinalJudgeReport
selected final candidate
ReviewItems
```

Must include:

```text
technical checks
multi-agent semantic QA layers
failure tag taxonomy
retry decision matrix
strong judge / final judge path
human override with DecisionLog
```

Must not include:

```text
silent candidate approval
untracked retries
publishing
learning rule changes without approval
```

---

## 35. P7 Map: Packaging, Publishing, Platform Payloads

Status:

```text
detailed_planning_doc_exists
canonical doc: PHASE7_PACKAGING_PUBLISHING_PLATFORM_PAYLOADS_PLAN.md
scope not yet confirmed for implementation
```

Goal:

```text
Create titles, descriptions, tags, covers, first-frame checks, platform payloads, and upload/manual publishing packages.
```

Inputs:

```text
final candidate
quality report
format/trend context
asset provenance
platform profiles
```

Outputs:

```text
TitleOptions
Description
Tags
CoverCandidates
SelectedCover
PlatformPayloads
PublishReadinessReport
ManualPublishPackage
PublishRecords
```

Must include:

```text
all-platform default packaging
platform unsuitability detection
manual package fallback
publish record creation
metadata provenance
```

Must not include:

```text
auto-publish without explicit permission
fake upload status
unreviewed risky platform payloads
```

---

## 36. P8 Map: Feedback Learning, Long-Term Memory, Weight Optimization

Status:

```text
detailed_planning_doc_exists
canonical doc: PHASE8_FEEDBACK_LEARNING_MEMORY_WEIGHT_OPTIMIZATION_PLAN.md
scope not yet confirmed for implementation
```

Goal:

```text
Collect performance feedback, summarize lessons, propose weight/rule changes, and grow long-term knowledge without silent self-modification.
```

Inputs:

```text
PublishRecords
platform metrics
comments
quality reports
retry history
user decisions
ToolPerformanceRecords
```

Outputs:

```text
FeedbackReport
MemoryEntries
LearningObservations
LearningSuggestions
WeightChangeSuggestions
ToolPerformanceUpdates
approved rules after user review
```

Must include:

```text
observations vs suggestions vs approved rules
sample size/confidence tracking
weight change review
format/tool/platform learning
rollback/supersede rule history
```

Must not include:

```text
silent rule changes
silent weight changes
overfitting from one weak result
auto-deleting old knowledge
```

---

## 37. P9 Map: Local Web Console and Human Review Center

Status:

```text
detailed_planning_doc_exists
canonical doc: PHASE9_LOCAL_WEB_CONSOLE_REVIEW_CENTER_PLAN.md
scope not yet confirmed for implementation
```

Goal:

```text
Build the local control room for jobs, reviews, candidates, assets, tools, permissions, publishing, and learning reports.
```

Inputs:

```text
all core objects
ReviewItems
DecisionLogs
reports
asset manifests
tool setup items
publish packages
learning suggestions
```

Outputs:

```text
local dashboard
review queue
candidate compare view
asset provenance view
tool setup view
permission matrix UI
publish center
learning reports
```

Must include:

```text
dense operational UI
fast approve/reject/edit actions
weight editing UI
manual generation slot UI
source/asset traceability
```

Must not include:

```text
marketing landing page
remote multi-user assumptions by default
hidden agent decisions
```

---

## 38. P10 Map: MMD/3D Specialized Route

Status:

```text
detailed_planning_doc_exists
canonical doc: MMD_3D_DETAILED_PLAN.md
scope not yet confirmed for implementation
```

Goal:

```text
Support model-based 3D/MMD-style productions as one specialized route among many, especially for repeatable motion, dance, camera, and character staging.
```

Inputs:

```text
ProductionRecipe
CharacterReferencePack
3D/MMD model assets
motion/camera/audio requirements
route constraints
```

Outputs:

```text
MMD/3D RoutePlan
model compatibility report
motion/camera plan
render/import outputs
3D-specific QA report
candidate video assets
```

Must include:

```text
model format compatibility
motion/camera handling
asset provenance
route-specific QA
fallback to non-3D routes when needed
```

Must not include:

```text
treating MMD as the main project identity
blocking ordinary AI video routes
untracked model usage
```

---

## 39. P11 Map: Longform Specialized Route

Status:

```text
detailed_planning_doc_exists
canonical doc: LONGFORM_DETAILED_PLAN.md
scope not yet confirmed for implementation
```

Goal:

```text
Support longer videos with segment planning, continuity, pacing, source management, and longform packaging.
```

Inputs:

```text
longform production goal
source corpus
outline
segment plans
voice/audio requirements
platform duration requirements
```

Outputs:

```text
LongformPlan
segment scripts
chapter/scene structure
continuity report
longform generation/edit plan
longform QA report
longform publish package
```

Must include:

```text
segment-level planning
continuity checks
long duration asset management
longform-specific QA
chapter/title/description strategy
```

Must not include:

```text
forcing short-video assumptions onto longform
unbounded source crawling
unreviewed long video publishing
```

---

## 40. Phase Map Rules

1. P0-B is implemented and verified for its current offline acceptance chain; P1 public metadata/evidence foundation is implemented and accepted with declared gaps.
2. P2-P11 now have canonical detailed planning drafts.
3. P2-P11 are not confirmed for implementation until explicitly accepted or scheduled.
4. Do not create P12+ canonical docs unless the user chooses to extend the roadmap.
5. Do not implement phases out of order unless the user explicitly redirects.
6. Specialized routes such as MMD/3D and longform are phases/routes later in the map, not the identity of the whole project.
7. When a phase status changes, update this roadmap, `PROJECT_INDEX.md`, `KAIROVE_COMPACT_CONTEXT.md`, and `READING_GUIDE.md`.

---

## 41. P0-B Implementation Status - 2026-06-06

P0-B implementation is now active for the current offline lowest complete production chain under:

```text
src/kairove/
```

Implemented runtime pieces:

```text
core.py:
  folder bootstrap
  JSON config bootstrap
  SQLite schema
  Run / Job / DecisionLog / ReviewItem / ToolSetupItem helpers
  manifest helpers

p0b.py:
  manual source intake
  source manifest
  simple format observation
  visible score stub
  semantic transfer brief
  asset requirement report
  route plan
  prompt package
  manual generation slot
  candidate import
  generated asset manifest
  basic technical QA
  basic semantic QA scaffold
  retry/pass decision
  manual all-platform publish package
  post-output self-check report
  phase0 reports

cli.py:
  init
  p0b-demo
  import-candidate
  qa
  package
```

Actual verification performed:

```text
$env:PYTHONPATH='src'; python -m unittest discover -s tests -v
5 tests passed.

python -m kairove --root E:\影潮枢_Kairove p0b-demo ...
created run_000003 / job_000003 successfully.
```

P0-B remains intentionally honest about missing automation: it uses manual generation slots and tool setup items instead of pretending that autonomous crawling, paid AI generation, deep visual QA, or platform auto-publishing already exist.
---

## 42. Latest Phase Boundary Authority - Planning Reset 2026-06-06

This section overrides any ambiguous earlier wording about whether coding should begin.

Current mode:

```text
P0-B implementation was explicitly authorized and completed for the current offline chain.
P1 implementation was explicitly authorized and completed for the public metadata/evidence acceptance chain; deep-content platform automation remains outside accepted P1.
Do not write P2+ code until the user explicitly says to start implementing another named phase.
```

Important distinction:

```text
Phase boundary discussed:
  The phase can be named and discussed as a possible implementation unit.

Phase confirmed for implementation:
  The user has explicitly approved starting code for that phase.
```

Current implementation permission:

```text
P0-B is implemented for the current offline chain.
No P1+ phase is currently authorized for further coding.
Do not treat detailed planning drafts as permission to implement later phases.
```

Phase status table:

| Phase | Boundary Name | Boundary Status | Implementation Status | What Must Happen Next |
| --- | --- | --- | --- | --- |
| P0 | P0-B Lowest Complete Production Chain | Final include/exclude list and acceptance criteria locked | Implemented and verified for current offline chain | Re-check P1 exact boundary next |
| P0-A | Foundation Skeleton | Not an independent phase; subset inside P0-B | Not separate | Keep as internal P0-B foundation workstream |
| P1 | Trend and Source Intelligence Foundation | Scope confirmed | Public metadata/evidence foundation accepted with declared gaps | Do not move to P2 until explicitly authorized |
| P2 | Format Intelligence and Opportunity Decision | Detailed draft exists | Not authorized | Discuss because Format Miner / Trend Analyst are core and need careful confirmation |
| P3 | Reproduction Planning, Semantic Transfer, Script, Direction | Detailed draft exists | Not authorized | Confirm ordinary imitation/adaptation workflow versus short-drama-only workflow |
| P4 | Asset Resolution, Character/World Knowledge, Audio/Visual Material | Detailed draft exists | Not authorized | Confirm asset search, official/wiki/reference/local-asset policy and folder contracts |
| P5 | Generation Routes and Candidate Management | Detailed draft exists | Not authorized | Confirm production routes, tool registry, prompt packages, manual slots, candidate model |
| P6 | Quality, Retry, Strong Judge | Detailed draft exists | Not authorized | Confirm layered QA order, model tiers, failure tags, retry mutation rules |
| P7 | Packaging, Publishing, Platform Payloads | Detailed draft exists | Not authorized | Confirm title/description/tag/cover agents and platform upload boundaries |
| P8 | Feedback, Learning, Memory, Weight Optimization | Detailed draft exists | Not authorized | Confirm which learning suggestions can be automatic and which require approval |
| P9 | Local Web Console and Review Center | Detailed draft exists | Not authorized | Confirm UI/review center role after core chain is stable |
| P10 | MMD/3D Specialized Route | Specialized draft exists | Not authorized | Discuss separately; MMD/3D is one route, not the project identity |
| P11 | Longform Specialized Route | Specialized draft exists | Not authorized | Discuss separately; longform has different pacing, storage, QA, and publishing needs |

Practical rule for future turns:

```text
If the user says “继续计划 / 继续讨论 / 整理 / 补完”, edit planning docs only.
If the user says “开始实现 Pn” or “写代码实现 Pn”, then code may begin for that named phase only.
If ambiguous, ask once instead of assuming implementation permission.
```
---

## Phase Boundary Confirmation Update - 2026-06-06

User accepted the P0-P9 boundary overview.

Meaning:

```text
P0-P9 planning boundaries are confirmed as the current roadmap shape.
This is not implementation authorization.
No code should be written until the user explicitly authorizes implementation of a named phase.
```

Confirmed planning boundaries:

```text
P0-B: Lowest Complete Production Chain
P1: Trend and Source Intelligence Foundation
P2: Format Intelligence and Opportunity Decision
P3: Reproduction Planning, Semantic Transfer, Script, Direction
P4: Asset Resolution, Character/World Knowledge, Audio/Visual Material
P5: Generation Routes and Candidate Management
P6: Quality, Retry, Strong Judge
P7: Packaging, Publishing, Platform Payloads
P8: Feedback, Learning, Memory, Weight Optimization
P9: Local Web Console and Review Center
```

Still pending separate boundary discussion:

```text
P10: MMD/3D Specialized Route
P11: Longform Specialized Route
P12+: not defined
```
---

## P10-P11 Boundary Confirmation Update - 2026-06-06

User accepted the P10/P11 continuation with one correction: P10 must treat 3D compatibility and repair as core requirements, not optional or out of scope.

Meaning:

```text
P0-P11 planning boundaries are now confirmed as the current roadmap shape.
This is not implementation authorization.
No phase should be coded until the user explicitly authorizes implementation of that named phase.
P12+ remains undefined.
```

P10 confirmed correction:

```text
MMD/3D compatibility is required.
Kairove should attempt direct use, compatibility mapping, and automatic repair before marking a model/motion combo unusable.
Model assets are treated as usable by default for the user's local production flow, while provenance, usage, repair history, and warnings are still recorded.
Bone, morph, physics, material, texture, camera, scale, clipping, and render issues should enter a repair/preview/QA loop, not simply become early non-goals.
```

P11 confirmed boundary:

```text
Longform remains a specialized route with project/episode/chapter/scene hierarchy, checkpointed generation, longform QA, source tracking, continuity, longform publishing, and derived shorts.
```

Current full planning boundary map:

```text
P0-B: Lowest Complete Production Chain
P1: Trend and Source Intelligence Foundation
P2: Format Intelligence and Opportunity Decision
P3: Reproduction Planning, Semantic Transfer, Script, Direction
P4: Asset Resolution, Character/World Knowledge, Audio/Visual Material
P5: Generation Routes and Candidate Management
P6: Quality, Retry, Strong Judge
P7: Packaging, Publishing, Platform Payloads
P8: Feedback, Learning, Memory, Weight Optimization
P9: Local Web Console and Review Center
P10: MMD/3D Specialized Route with compatibility and repair core
P11: Longform Specialized Route
P12+: not defined
```

---

## Cross-Phase Final Policy Sync - 2026-06-06

This section is the latest cross-phase policy authority. If older documents conflict with this section, this section wins. It is planning authority only and is not implementation authorization.

Documentation authority:

```text
Current project documents remain the source of truth, but user-provided cross-phase final policy updates override older conflicting text.
When a cross-phase policy update is accepted, sync root docs and relevant phase docs before implementation.
```

Language policy:

```text
Default user-facing language: Chinese.
Titles/descriptions/tags: Chinese primary version.
YouTube Shorts may also receive English auxiliary title/description/tags.
Prompts: tool-effectiveness based; default keeps Chinese explanation plus English generation prompt.
Reports/plans/review items: Chinese primary.
Internal object IDs, schema fields, and config keys: English.
```

Platform policy:

```text
P0-B primary platforms:
  Bilibili
  Douyin
  Xiaohongshu
  YouTube Shorts

Long-term expandable platforms:
  TikTok
  Kuaishou
  Instagram Reels

TikTok, Kuaishou, and Instagram Reels remain platform stubs until their support is explicitly expanded.
```

Publish policy:

```text
Default output is still manual publish package.
Auto-publish may be enabled later only after user approval.
Auto-publish must be enabled separately per platform, account, and permission switch.
No global default auto-publish.
```

Search and collection policy:

```text
Preferred automatic search/collection directions:
  general web search
  official sites
  wiki sources
  Bilibili
  YouTube

Douyin and Xiaohongshu may use capability probes and semi-automatic entry points.
If API/login/cookie/download capability is missing, create ToolSetupItem.
Do not bypass platform restrictions.
Do not pretend unstable or unavailable data was collected.
Metadata collection may be automatic.
Large-scale downloads, comment crawling, and asset downloads default to ask.
```

Hot-but-overused policy:

```text
Do not automatically avoid overused formats.
Default strategy is to reduce exact-copy weight and prefer variant entry points.
If comment sentiment is good, growth remains active, and interaction quality is high, the system may still ride the trend.
If comment fatigue is visible, negativity is high, or growth is declining, reduce score or abandon the opportunity.
```

Format Miner priority:

```text
Primary extracted structure:
  hook
  rhythm
  shot/scene structure
  role relationship
  reversal point
  copywriting template
  audio/subtitle function
  visual style

Additional useful structure:
  audience expectation
  interaction trigger
  production difficulty
  asset requirements
  platform fit
```

Semantic transfer policy:

```text
The invariant is format function.
Do not change the core joke/payoff/scare/emotion curve, relationship function, rhythm, reversal mechanism, or audience recognition point.
Characters, world, art style, exact lines, and scenes may change if the audience can still recognize the same transferred format.
```

Character and world knowledge policy:

```text
Maintain all three pack types:
  work pack
  character pack
  relationship/CP pack

Relationship packs are important because many transfers depend on relationship function, not only single-character facts.
```

Music and SFX policy:

```text
Official music and SFX follow the official-asset direct-use policy with provenance.
Music requires extra platform-risk notes because it is more likely to trigger platform restrictions.
Minimum music/SFX fields: source, work/song title, official owner/account, usage, platform risk note.
Personal or unknown music/SFX sources default to review.
```

Personal creator / unknown asset policy:

```text
Default first action is to search for official or substitute assets.
Ask the user before direct use of personal creator or unknown assets.
Reference/style analysis can be more permissive than direct use, but direct use requires review.
```

Generation tool policy:

```text
Do not lock one specific generation tool.
Use Tool Registry.
Allowed tool categories include text-to-video, image-to-video, video-to-video, image generation, TTS/voice, editing, subtitles, covers, inpainting/repair, and MMD/Blender/3D tools.
Forbidden tool behavior: black-box high-cost batch runs, untraceable outputs, inability to export files/metadata, or obvious platform/account rule violations.
Missing API/key/account/local install creates ToolSetupItem.
```

Budget policy:

```text
Low-cost generation is a capability switch first, not a fixed number in P0-B.
Future budgets should support daily, per-job, per-run, and high-cost-threshold layers.
P0-B does not require real paid APIs.
High-cost routes ask before each round.
```

QA aesthetic policy:

```text
Default strong-judge preference order:
  first: resembles the hot format, has a hook, has sharing potential
  second: character accuracy, visual stability, completion quality

P6 must support type-specific weight switching:
  character-focused video: higher character accuracy weight
  abstract short drama: higher joke/rhythm weight
  MMD/3D: higher motion, clipping, and stability weight
```

Retry policy:

```text
Retry patience should be configurable, not hardcoded.
Default recommendation: 3-5 normal retries per job.
If cost/time limits are exceeded or repeated same-type failures occur, create ReviewItem.
High-cost route retries ask before each round.
```

Learning policy:

```text
Observations may automatically become memory.
Learning suggestions may be generated automatically.
Rule changes, weight changes, permission changes, and auto-publish strategy changes require user approval before becoming active.
Suggestions must not silently become rules.
```

Local Web Console policy:

```text
Long-term console shape is production board + review desk + creation/material/control console.
P9 first version prioritizes production board and review desk.
Do not build decorative or marketing-style UI first.
```

MMD/3D policy:

```text
No single required toolchain.
Design as compatibility layer.
Long-term support should include MMD, Blender, PMX, VMD, VRM, and optionally Unity/other tools when useful.
3D compatibility, skeleton, morph, physics, clipping, material, texture, camera, scale, and render issues must enter detect -> repair attempt -> preview -> QA.
```

Longform policy:

```text
Do not lock one longform content type.
Supported longform categories remain long drama, commentary/explainer, remix/compilation, tutorial, and fan-series.
P11 focuses on longform structure: Project -> Episode -> Chapter -> Scene -> Shot.
P11 is not short video stretched longer.
```

Local data retention policy:

```text
Default retention is long-term.
Failed generations, old candidates, downloaded assets, QA reports, and publish packages keep source and usage records.
Cleanup is allowed only with manifest and traceable records.
Deleting generated assets: ask.
Deleting local assets: deny by default.
```
