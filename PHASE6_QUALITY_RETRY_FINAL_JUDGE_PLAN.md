# Kairove Phase 6: Quality Council, Retry Engine, and Final Judge Plan

## 0. Status

Current status:

```text
Phase 6: detailed planning draft, not yet confirmed for implementation
Depends on: P5 CandidateManifest and HandoffToQuality
Primary output: selected final candidate or targeted RetryPlan
Related capability doc: QUALITY_AND_RETRY_PLAN.md
```

---

## 1. Purpose

Phase 6 decides whether generated candidates are good enough, what failed, what should be preserved, and what should be retried.

It answers:

```text
Does this candidate technically work, does it preserve the intended format and semantic transfer, is it worth publishing, and if not, what exact next action should happen?
```

Quality is not one judge. It is a layered council.

---

## 2. One-Line Scope

```text
CandidateManifest + ProductionRecipe + Prompt/Asset/Source Context -> QualityReports + RetryPlan or FinalCandidateSelection
```

---

## 3. Must Include

```text
Program-First Technical QA:
  File, codec, resolution, fps, duration, audio, subtitles, cover, black/frozen frame checks.

Layered Semantic QA:
  Cheap first, medium next, strong only when needed.

Specialist QA:
  Run only relevant specialists such as meme, horror, music sync, character/CP, visual style, MMD/3D, longform, platform.

Failure Tags:
  Stable structured tags mapped to retry actions.

Retry Engine:
  Preserve what worked and change only what failed when possible.

Route Mutation:
  Switch route when prompt-level fixes cannot solve the issue.

Final Judge:
  Select final candidate, ask user, retry more, switch route, or abandon.
```

---

## 4. Must Not Include

```text
candidate generation itself
silent publish approval
untracked retries
hidden strong-model decisions
learning rule changes without review
ignoring blocking failures because total score is high
```

---

## 5. Inputs

```text
CandidateManifest
Candidate assets
GenerationPlan
GenerationSteps
PromptPackages
ProductionRecipeDraft or ProductionRecipe
ReproductionPlan
SemanticTransferPlan
FormatGenome
AssetResolutionReport
QualityExpectationDraft
ToolPerformanceRecords
Permission profile
Budget/retry profile
```

---

## 6. Outputs

```text
TechnicalQualityReport
CheapVisualQualityReport
SemanticQualityReport
SpecialistQualityReport
StrongJudgeReport
FinalQualityReport
FailureTags
RetryPlan
RevisionRequest
RouteChangeRequest
FinalCandidateSelection
ReviewItems
DecisionLogs
Phase6QualityReport
```

---

## 7. Workstreams

```text
P6-A Candidate Intake and Context Loader
P6-B Technical QA
P6-C Cheap Visual QA
P6-D Semantic QA Layers
P6-E Specialist QA
P6-F Strong Judge and Disagreement Resolution
P6-G Failure Tagging and Root Cause Analysis
P6-H Retry Planner
P6-I Final Candidate Selection
P6-J Quality Report and Tests
```

---

## 8. QA Execution Order

```text
1. Candidate Intake
2. Technical QA: deterministic program checks
3. Technical QA Assist: cheap agent only if ambiguous
4. Cheap Visual QA: obvious visual failures
5. Semantic QA Level 1: cheap plan-adherence pass
6. Semantic QA Level 2: medium format/transfer pass
7. Specialist QA: route-specific checks
8. Strong Judge: high-value, near-threshold, disputed, or repeated-failure cases
9. Regent Final Decision
10. Retry Planner or Packaging handoff
```

Skip rules:

```text
if file cannot decode -> skip semantic QA and return technical fix
if severe visual garbage -> skip expensive semantic QA unless diagnosis needs it
if all lower layers pass and risk is low -> Strong Judge can be skipped
if agents disagree on publish-level decision -> Strong Judge required
```

Skipped layers must still write a skipped record.

---

## 9. Technical QA

Program checks:

```text
file exists
can decode
container readable
codec readable
resolution
aspect ratio
frame rate
duration
bitrate if available
frame count
black frame ratio
frozen frame ratio
corrupt frames
flicker heuristic
audio track presence
audio loudness/clipping/silence
subtitle timing and bounds
cover validity
platform format constraints
```

Technical QA output:

```json
{
  "technical_quality_report_id": "techqa_000001",
  "candidate_id": "candidate_001",
  "status": "pass | warning | fail | skipped",
  "checks": {},
  "warnings": [],
  "failure_tags": [],
  "needs_agent_assist": false
}
```

Technical QA is program-first, not program-only. Use a cheap visual/audio agent only for ambiguous cases like dark horror vs black screen.

---

## 10. Visual QA

Cheap visual checks:

```text
subject present
wrong character count
face collapse
hand failure
identity drift
severe blur
generation garbage
random text
watermark issue
style mismatch
composition failure
```

Visual QA should save evidence frames:

```json
{
  "frame_id": "frame_000123",
  "candidate_id": "candidate_001",
  "timestamp": 4.21,
  "reason_saved": "identity_drift_evidence",
  "local_path": "..."
}
```

---

## 11. Semantic QA Layers

Semantic QA compares the candidate against:

```text
FormatGenome
ReproductionPlan
SemanticTransferPlan
ScriptPackage
ShotPlan
ProductionRecipe
PromptPackages
AssetResolutionReport
representative source examples
```

Level 1 cheap pass:

```text
PlanChecklistJudge
BeatOrderJudge
BasicRoleLogicJudge
BasicCaptionAudioJudge
```

Level 2 medium pass:

```text
FormatCoreJudge
SemanticTransferJudge
RelationshipLogicJudge
CharacterFitJudge
PacingAndPayoffJudge
```

Level 3 strong pass only when triggered:

```text
StrongSemanticJudge
AudienceAppealJudge
FinalPublishRiskJudge
```

Semantic QA asks:

```text
Did the format core survive?
Did the role/relationship/emotion mapping make sense?
Did the viewer hook survive?
Did the candidate become generic AI content?
Did subtitles/audio/visual beats support the intended structure?
```

---

## 12. Specialist QA

Run only relevant specialists:

```text
MemeSpecialistQA
AbstractShortDramaSpecialistQA
HorrorSpecialistQA
MusicSyncSpecialistQA
CharacterReenactmentSpecialistQA
CPRelationshipSpecialistQA
VisualStyleSpecialistQA
PlatformPackagingSpecialistQA
MMD3DSpecialistQA
LongformSpecialistQA
```

Specialist examples:

```text
horror -> atmosphere, reveal timing, darkness intent, audio dread
meme -> joke clarity, chaos control, subtitle timing
music_sync -> beat alignment, drop impact, loop points
character/CP -> identity, OOC risk, relationship dynamic
abstract short -> intentional absurd logic, escalation, payoff
```

---

## 13. Failure Tags

Failure tags should be stable and mapped to retry actions.

Core groups:

```text
technical
visual
semantic_format
script_pacing
audio_music
route_tool
risk_platform
specialist
```

Tag record:

```json
{
  "tag": "semantic_transfer_failed",
  "severity": "low | medium | high | blocking",
  "confidence": 0.0,
  "evidence": [],
  "recommended_retry_action": "revise_role_mapping",
  "owner_layer": "semantic_qa"
}
```

Blocking failures override total score.

---

## 14. Strong Judge and Regent Final Decision

Strong Judge triggers:

```text
near threshold
agent disagreement
high-value job
repeated retries failed
semantic transfer subtle
user taste likely decisive
publish decision needs confidence
```

Strong Judge recommends. Regent decides.

Final decision values:

```text
select_candidate
package
retry
ask_user
switch_route
abandon
```

Final decision schema:

```json
{
  "final_qc_decision_id": "final_qc_decision_000001",
  "candidate_id": "candidate_001",
  "decision": "package",
  "reason": "...",
  "quality_report_path": "...",
  "retry_plan_id": null,
  "review_item_id": null,
  "decision_log_id": "decision_000001"
}
```

---

## 15. Retry Planner

RetryPlanner maps failure to the smallest useful change.

Retry scope values:

```text
file_reexport
subtitle_only
audio_only
single_segment
multiple_segments
prompt_only
asset_resolution
script_revision
semantic_transfer_revision
route_change
full_regeneration
ask_user
abandon
```

RetryPlan schema:

```json
{
  "retry_plan_id": "retry_000001",
  "candidate_id": "candidate_001",
  "retry_round": 2,
  "decision": "retry_with_route_change",
  "root_causes": [],
  "preserve": [],
  "changes": [],
  "expected_improvements": [],
  "risks": [],
  "needs_user_review": false
}
```

Preserve policy:

```text
preserve assets that passed QA
preserve generated shots that passed semantic/visual checks
preserve timing that passed music/pacing checks
do not preserve anything linked to blocking failure unless justified
```

---

## 16. Route Mutation

Route mutation is required when the current route cannot satisfy the task.

Examples:

```text
continuous two-character scene fails -> reaction-cut dialogue edit
text-to-video identity fails -> reference image + image-to-video
AI dance fails -> beat-synced edit or MMD/3D route
horror too explicit -> shadow/audio partial reveal
longform scene weak -> regenerate scene only, not whole episode
```

Route changes must return a structured request to P5 and may also request P3/P4 revisions.

---

## 17. Quality Thresholds

Default thresholds:

```yaml
package_ready: 7.5
select_with_warnings: 6.8
retry: 5.0
reject_below: 5.0
strong_judge_band:
  min: 6.5
  max: 7.7
```

Blocking failures override score:

```text
technical_decode_failed
format_core_lost
source_policy_unresolved
identity_drift_severe
missing_required_audio
platform_export_invalid
```

---

## 18. Handoff Outcomes

Possible handoffs:

```text
package_ready -> P7
retry_generation -> P5
revise_assets -> P4
revise_semantic_transfer_or_script -> P3
ask_user -> Review Queue / P9
abandon -> phase report and learning
```

---

## 19. Storage Layout

```text
generated_assets/jobs/job_000001/quality/
  candidate_001/
    technical_qa.json
    cheap_visual_qa.json
    semantic_qa_level1.json
    semantic_qa_level2.json
    specialist_qa.json
    strong_judge.json
    final_quality_report.json
    final_quality_report.md
    evidence_frames/
    retry_plan_round_01.json
```

---

## 20. Tests

Fixture groups:

```text
corrupt video
wrong aspect ratio
black screen vs intentional dark horror
identity drift
format core lost
semantic transfer failed
weak punchline
beat mismatch
near-threshold candidate
specialist disagreement
route mutation needed
pass-to-package candidate
```

Required tests:

```text
technical QA runs before semantic QA
skips expensive QA on decode failure
saves evidence frames
creates stable failure tags
runs relevant specialist only
triggers Strong Judge on near-threshold/disagreement
creates RetryPlan with preserve/change fields
creates route-change request when needed
selects final candidate only with DecisionLog
passes package-ready candidate to P7
```

---

## 21. Acceptance Criteria

P6 is ready when Kairove can:

```text
run layered QA on registered candidates
separate technical, visual, semantic, specialist, and strong-judge checks
produce final quality reports
assign failure tags
create targeted retry plans
mutate route when needed
select final candidate or abandon with reason
handoff to P7 only after final decision
pass fixture-based tests
```

---

## 22. Non-Acceptance

P6 is not acceptable if:

```text
one agent decides everything
technical failures continue into expensive QA without reason
failure tags are vague free text
retries regenerate everything blindly
Strong Judge is used for every trivial candidate
Regent decisions are not logged
candidates pass despite blocking failures
```

---

## 23. Confirmation Checklist

Before P6 implementation, confirm or revise:

```text
initial QA thresholds
which strong model tier is used for final judge
cost limits for repeated semantic QA
failure tag taxonomy
retry limits
when human review should override Regent
```

---

## Cross-Phase Policy Alignment - 2026-06-06

P6 strong-judge aesthetic defaults:

```text
Default preference order:
  first: resembles the hot format, has a hook, has sharing potential
  second: character accuracy, visual stability, completion quality

Type-specific weight switching:
  character-focused video: higher character accuracy weight
  abstract short drama: higher joke/rhythm weight
  MMD/3D: higher motion, clipping, and stability weight
```

Retry policy:

```text
Retry patience is configurable, not hardcoded.
Default recommendation: 3-5 normal retries per job.
If cost/time limits are exceeded or repeated same-type failures occur, create ReviewItem.
High-cost route retries ask before each round.
```
