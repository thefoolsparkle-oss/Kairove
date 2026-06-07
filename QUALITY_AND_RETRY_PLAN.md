# Kairove Quality and Retry Plan

## 0. Purpose

This document defines Kairove's quality inspection and retry system.

Kairove should not simply generate a video and hope it is good. Every candidate should be checked in layers, scored, tagged with failure reasons, and either:

- accepted;
- retried with targeted changes;
- routed to another production strategy;
- sent to human review;
- abandoned with a clear reason.

Quality and retry are one loop:

```text
candidate -> quality report -> failure classification -> retry plan -> generation -> candidate
```

---

## 1. Core Principles

### 1.1 Program-First, Agent-Assisted Technical QA

Technical QA should use deterministic program checks first:

- file exists;
- can decode;
- resolution;
- frame rate;
- duration;
- audio track;
- black frames;
- frozen frames;
- corrupt frames;
- subtitle bounds;
- platform format.

But it is not program-only.

Lightweight agents can assist when program checks are not enough:

- dark horror scene vs black screen;
- subtitle inside bounds but covering faces;
- cover technically valid but visually messy;
- audio technically aligned but feels wrong.

### 1.2 Multi-Layer, Not One Judge

Quality should be layered:

1. Technical QA;
2. Cheap Visual QA;
3. Semantic QA;
4. Specialist QA;
5. Strong Judge;
6. Regent Final Decision.

### 1.3 Failure Tags Matter More Than Total Score

A total score is useful, but failure tags drive retries.

Examples:

- `semantic_transfer_failed`
- `format_core_lost`
- `identity_drift`
- `bad_pacing`
- `audio_mismatch`
- `subtitle_overflow`
- `tool_not_suitable`

### 1.4 Preserve What Worked

Retry must protect successful parts. Kairove should not blindly regenerate everything.

Each retry plan must include:

```text
preserve:
  what should stay

change:
  what should be modified
```

### 1.5 Route Mutation Is Allowed

Some failures cannot be fixed by prompt changes.

Example:

```text
continuous two-character interaction fails
```

Possible route mutation:

```text
split into alternating reaction shots
```

---

## 2. Quality Council Layers

## 2.1 Technical QA

### Purpose

Check whether the candidate is technically valid and platform-ready at the file level.

### Inputs

- candidate file;
- platform requirements;
- subtitle files;
- cover files;
- audio files.

### Program Checks

Video:

- file exists;
- file can be opened;
- codec readable;
- resolution;
- aspect ratio;
- frame rate;
- duration;
- bitrate if available;
- frame count;
- black frame ratio;
- frozen frame ratio;
- corrupt frame detection;
- flicker heuristic;
- no unintended empty video.

Audio:

- audio track exists if required;
- sample rate;
- loudness range;
- clipping;
- silence ratio;
- audio duration matches video duration;
- no missing dialogue if voice is expected.

Subtitles:

- file exists if expected;
- subtitle timing within video duration;
- subtitle text length;
- safe area bounds;
- overlap detection;
- unreadable duration detection.

Cover:

- file exists;
- resolution;
- aspect ratio;
- size;
- readable image.

### Agent-Assisted Checks

Use lightweight visual or multimodal agents for:

- dark scene vs black screen;
- subtitle blocks covering important faces;
- cover visual clutter;
- visible platform UI obstruction risk;
- obvious audio/visual mismatch not caught by timestamps.

### Output

```json
{
  "layer": "technical_qa",
  "status": "pass | fail | warning",
  "checks": {},
  "warnings": [],
  "failure_tags": [],
  "needs_agent_assist": false
}
```

### Failure Handling

Technical failure usually returns directly to Generation Manager or Edit step.

No expensive semantic QA should run if the file is technically unusable, unless diagnosis requires it.

---

## 2.2 Cheap Visual QA

### Purpose

Catch obvious visual failures cheaply.

### Checks

- subject disappeared;
- wrong number of characters;
- severe face collapse;
- severe hand collapse;
- identity drift;
- bad watermarks or random text;
- extremely blurry image;
- wrong style;
- obvious generation garbage;
- unexpected explicit or unsafe content;
- video does not match basic prompt at all.

### Output

```json
{
  "layer": "cheap_visual_qa",
  "status": "pass | fail | warning",
  "scores": {
    "basic_visual_quality": 0,
    "subject_presence": 0,
    "identity_stability": 0
  },
  "failure_tags": [],
  "evidence_frames": []
}
```

### Failure Handling

If severe, skip deeper QA and retry or reject.

If uncertain, pass to Semantic QA.

---

## 2.3 Semantic QA

### Purpose

Check whether the candidate follows the plan.

Inputs:

- candidate;
- source format;
- reproduction plan;
- semantic transfer plan;
- production recipe;
- script or visual plan;
- generation prompts.

Checks:

- did it preserve the format core?
- did it preserve the relationship/emotion pattern?
- did semantic transfer make sense?
- does visual content match planned beats?
- do subtitles/audio/scene match the intended story?
- does it feel like the intended adaptation?

Example judgment:

```text
The original format is intimate teasing denial. The candidate preserves denial and evidence reveal, but lacks familiar teasing between characters, so semantic transfer is weakened.
```

Output:

```json
{
  "layer": "semantic_qa",
  "status": "pass | fail | warning",
  "scores": {
    "format_reproduction": 0,
    "semantic_transfer": 0,
    "plan_adherence": 0
  },
  "failure_tags": [],
  "reasoning": [],
  "retry_recommendations": []
}
```

---

## 2.4 Specialist QA

### Purpose

Run checks specific to the route.

Specialist QA should only run relevant checks.

### Meme QA

Checks:

- is the joke understandable?
- is the rhythm too slow?
- is the punchline strong?
- is the chaos funny or just confusing?
- does subtitle timing support the meme?

Failure tags:

- `weak_punchline`
- `too_confusing`
- `bad_meme_timing`
- `too_generic`

### Horror QA

Checks:

- is the atmosphere effective?
- is there enough tension?
- is the reveal too early?
- is it over-explained?
- is it too graphic or platform-risky?

Failure tags:

- `weak_atmosphere`
- `over_explained`
- `bad_reveal_timing`
- `horror_platform_risk`

### Music Sync QA

Checks:

- beat alignment;
- lyric timing;
- visual cut timing;
- motion on beat;
- chorus/drop reveal;
- audio quality.

Failure tags:

- `beat_mismatch`
- `lyric_mismatch`
- `weak_drop`
- `audio_mismatch`

### Character QA

Checks:

- character identity;
- character visual features;
- personality;
- speech style;
- relationship fit;
- OOC risk;
- CP/fandom risk.

Failure tags:

- `ooc_character`
- `relationship_not_clear`
- `bad_cp_mapping`
- `identity_drift`

### Visual Style QA

Checks:

- style consistency;
- visual reference adherence;
- not too copied from personal creator;
- lighting/color/composition;
- AI artifact level.

Failure tags:

- `style_mismatch`
- `visual_inconsistency`
- `ai_artifact`
- `overcopied_style`

### Platform QA

Checks:

- platform formatting;
- title/cover risk;
- tag mismatch;
- likely UI obstruction;
- platform-specific content risk.

Failure tags:

- `platform_packaging_issue`
- `cover_not_readable`
- `bad_platform_fit`

---

## 2.5 Strong Judge

### Purpose

Use a stronger model for final judgment when needed.

Triggered by:

- near-threshold candidate;
- agent disagreement;
- high-value job;
- repeated failures;
- publish decision;
- high semantic uncertainty;
- high user preference uncertainty.

Checks:

- would a real viewer watch it?
- does it feel low-quality AI?
- does it preserve the source format's appeal?
- is it worth retrying?
- should it be shown to user?
- should it be published?

Output:

```json
{
  "layer": "strong_judge",
  "decision": "publish_ready | retry | ask_user | reject",
  "confidence": 0.0,
  "reason": "...",
  "recommended_next_actions": []
}
```

---

## 2.6 Regent Final Decision

Regent combines all QA layers and decides:

```text
select_candidate
retry
ask_user
switch_route
abandon
publish_package
```

Regent must write a decision log.

---

## 3. Quality Score Profiles

Quality scoring should be route-specific.

### 3.1 Ordinary AI Format Video

Suggested dimensions:

```yaml
technical_validity: 0.12
visual_quality: 0.14
format_reproduction: 0.18
semantic_transfer: 0.16
character_consistency: 0.12
audio_sync: 0.08
script_or_text_quality: 0.08
platform_fit: 0.06
viewer_retention_potential: 0.12
safety_or_risk: -0.10
```

### 3.2 Music Sync Video

```yaml
technical_validity: 0.10
visual_quality: 0.12
audio_sync: 0.24
format_reproduction: 0.18
motion_or_cut_timing: 0.16
viewer_retention_potential: 0.12
platform_fit: 0.08
safety_or_risk: -0.10
```

### 3.3 Script / Short Drama

```yaml
technical_validity: 0.10
visual_quality: 0.12
script_quality: 0.18
semantic_transfer: 0.18
character_consistency: 0.14
pacing: 0.14
format_reproduction: 0.14
safety_or_risk: -0.10
```

### 3.4 Horror

```yaml
technical_validity: 0.10
visual_quality: 0.14
atmosphere: 0.22
pacing: 0.16
reveal_strategy: 0.12
audio_design: 0.12
viewer_retention_potential: 0.10
platform_fit: 0.04
safety_or_risk: -0.12
```

All weights must be configurable and versioned.

---

## 4. Failure Tag Taxonomy

### 4.1 Technical

```text
file_missing
decode_failed
wrong_resolution
wrong_aspect_ratio
wrong_duration
bad_frame_rate
black_screen
frozen_video
corrupt_frames
audio_missing
audio_clipping
audio_too_quiet
subtitle_overflow
subtitle_overlap
cover_invalid
```

### 4.2 Visual

```text
face_collapse
hand_failure
identity_drift
wrong_character_count
subject_disappeared
blurry_output
random_text
watermark_issue
style_mismatch
visual_inconsistency
ai_artifact
```

### 4.3 Semantic / Format

```text
format_core_lost
semantic_transfer_failed
relationship_not_clear
world_adaptation_failed
plan_adherence_failed
wrong_emotional_tone
weak_format_signal
```

### 4.4 Script / Pacing

```text
weak_hook
weak_punchline
bad_pacing
too_explanatory
too_generic
ai_text_feel
dialogue_not_characterized
```

### 4.5 Audio / Music

```text
audio_mismatch
beat_mismatch
lyric_mismatch
voice_mismatch
bad_voice_quality
bgm_too_loud
sfx_mistimed
```

### 4.6 Route / Tool

```text
tool_not_suitable
tool_missing
api_failed
prompt_rejected
route_failure
too_expensive_to_retry
model_capability_gap
```

### 4.7 Risk / Platform

```text
personal_creator_asset_unapproved
unknown_source_unapproved
platform_packaging_issue
platform_policy_risk
ooc_character
bad_cp_mapping
```

---

## 5. Retry Engine

## 5.1 Retry Inputs

Retry Engine receives:

- quality report;
- failure tags;
- candidate metadata;
- generation steps;
- prompt history;
- resolved assets;
- reproduction plan;
- production recipe;
- tool capability records;
- budget state;
- retry policy.

## 5.2 Failure Classification

Classify into:

```text
technical_failure
prompt_failure
asset_failure
model_failure
route_failure
script_failure
semantic_transfer_failure
format_mismatch
platform_risk
cost_failure
unknown_failure
```

Output:

```json
{
  "failure_classification": [
    {
      "type": "semantic_transfer_failure",
      "confidence": 0.82,
      "evidence": "Target characters do not preserve intimate teasing relationship."
    }
  ]
}
```

---

## 5.3 Fix Strategy Selection

Common mappings:

### Face or Identity Drift

Actions:

- stronger reference image;
- shorter video segments;
- closer crop;
- different image-to-video tool;
- reduce camera movement;
- add negative prompt;
- split scene.

### Hand Failure

Actions:

- remove complex hand gesture;
- crop hands out;
- replace with face reaction;
- use cuts instead of continuous action;
- add negative prompt.

### Semantic Transfer Failure

Actions:

- rerun RelationshipMapper;
- choose another CP/relationship;
- adjust dialogue;
- add relationship cues;
- ask user.

### Format Core Lost

Actions:

- return to Reproduction Council;
- strengthen must-preserve elements;
- change route;
- rebuild script/visual plan.

### Bad Pacing

Actions:

- shorten lines;
- adjust subtitle timing;
- add cuts;
- move punchline earlier;
- change music/sfx timing.

### Tool Not Suitable

Actions:

- switch tool;
- switch route;
- reduce complexity;
- use multi-shot edit;
- ask user to configure tool.

### Asset Missing

Actions:

- search official web;
- use generated substitute;
- create human task;
- pause job.

---

## 5.4 Preservation Guard

Each retry plan must list:

```json
{
  "preserve": [
    "character visual design",
    "subtitle rhythm",
    "BGM choice"
  ],
  "change": [
    "shot_02 hand gesture",
    "relationship cue",
    "ending punchline"
  ]
}
```

If no successful elements exist, full regeneration is allowed.

---

## 5.5 Retry Actions

Possible retry actions:

```text
retry_same_prompt
retry_revised_prompt
retry_negative_prompt
retry_with_new_asset
retry_with_new_tool
retry_with_route_change
retry_with_script_change
retry_with_edit_change
ask_user
abandon
select_best_available
```

---

## 5.6 Retry Plan Output

```json
{
  "retry_plan_id": "retry_000001",
  "retry_round": 2,
  "decision": "retry_with_route_change",
  "root_causes": [
    "continuous two-character interaction unstable",
    "semantic relationship cue too weak"
  ],
  "preserve": [
    "character visual design",
    "subtitle rhythm"
  ],
  "changes": [
    {
      "type": "route_change",
      "from": "continuous_two_character_scene",
      "to": "reaction_cut_dialogue_scene"
    },
    {
      "type": "prompt_revision",
      "target": "shot_02",
      "instruction": "replace hand touch with eye contact and embarrassed pause"
    }
  ],
  "expected_improvements": [],
  "risks": [],
  "needs_user_review": false
}
```

---

## 6. Retry Policies

Retry policy should be configurable.

Example:

```yaml
default:
  max_rounds: 5
  max_cost_per_job: null
  escalate_after_failed_rounds: 2
  abandon_below_score_after_round: 3

critical_candidate:
  max_rounds: 8

cheap_draft:
  max_rounds: 2

high_cost_generation:
  ask_user_above_cost: true
```

Stop conditions:

- retry limit reached;
- cost limit reached;
- tool gap cannot be solved;
- route failure repeated;
- user rejects;
- no meaningful improvement after several rounds.

---

## 7. Route Mutation

Route mutation is required when prompt-level fixes cannot solve the issue.

Examples:

### Two-Character Continuous Scene Fails

Original:

```text
one continuous two-character AI video
```

Mutated:

```text
alternating reaction shots + subtitle dialogue + edit rhythm
```

### Text-to-Video Fails Character Consistency

Original:

```text
text_to_video
```

Mutated:

```text
character reference image -> image_to_video -> edit
```

### Music Sync Fails Motion

Original:

```text
AI generated dance
```

Mutated:

```text
beat-synced visual cuts + pose loops + effects
```

### Horror Too Explicit

Original:

```text
visible monster reveal
```

Mutated:

```text
sound + shadow + partial reveal
```

---

## 8. Human Review Triggers

Create review items when:

1. high-cost retry exceeds threshold;
2. semantic transfer uncertain;
3. character / CP risk medium or high;
4. personal creator asset needed for direct use;
5. unknown source needed for direct use;
6. tool setup required;
7. repeated retries fail;
8. final candidate is near threshold and decision is subjective;
9. publish permission requires approval.

---

## 9. Quality Reports File Layout

Per candidate:

```text
candidates/candidate_001/qc_reports/
  technical_qa.json
  cheap_visual_qa.json
  semantic_qa.json
  specialist_qa.json
  strong_judge.json
  final_quality_report.json
  agent_votes.json
  retry_recommendations.json
```

Retry:

```text
candidates/candidate_001/retry/
  retry_plan_round_01.json
  revised_prompts/
  revised_assets/
```

---

## 10. Decision Flow

Candidate decision:

```text
Technical fail
  -> fix technical/edit issue

Severe cheap visual fail
  -> retry or reject

Semantic fail
  -> retry or route back to reproduction/semantic transfer

Specialist fail
  -> route-specific fix

Near threshold
  -> Strong Judge

Pass
  -> Final Judge / Packaging
```

---

## 11. Memory Writeback

Quality and retry should write memory entries:

### Tool Memory

```text
This tool fails on continuous two-character interaction.
Workaround: split into reaction shots.
```

### Format Memory

```text
This format requires relationship cue; narration-only version failed.
```

### Asset Memory

```text
This character reference image gave stable identity.
```

### Prompt Memory

```text
This negative prompt reduced hand artifacts.
```

### User Preference

```text
User rejected this style as too AI-like.
```

---

## 12. Acceptance Criteria

Quality and Retry system is ready when it can:

1. Run program-first Technical QA on a candidate.
2. Use agent-assisted checks for ambiguous visual issues.
3. Run at least one cheap visual QA pass.
4. Run semantic QA against reproduction plan.
5. Run route-specific specialist QA when applicable.
6. Produce a final quality report.
7. Assign failure tags.
8. Generate a retry plan.
9. Preserve successful parts in retry plan.
10. Trigger route mutation when needed.
11. Stop retrying according to policy.
12. Create review items for uncertain or high-cost decisions.
13. Write learning memory after success or failure.

---

## 13. Implementation Notes

1. Start with deterministic Technical QA and structured reports.
2. Add agent-assisted Technical QA only for ambiguous cases.
3. Do not call strong models for every candidate.
4. Save frames used as evidence for visual QA.
5. Make failure tags stable and searchable.
6. Score profiles must be configurable and versioned.
7. Retry should be local and targeted whenever possible.
8. Every retry must link to original candidate and failed generation steps.
---

## 14. Detailed Operating Contract

This section tightens the Quality and Retry system into an operating contract.

It does not create a new phase. It supplements this existing plan.

Core rule:

```text
Quality is not one judge. Quality is an ordered council where cheap checks, deterministic checks, specialist checks, and stronger judges each do different work.
```

---

## 15. QA Execution Order

Default order:

```text
1. Candidate Intake
2. Technical QA: deterministic program checks
3. Technical QA Assist: cheap agent only if ambiguous
4. Cheap Visual QA: obvious visual failures
5. Semantic QA Level 1: cheap plan-adherence pass
6. Semantic QA Level 2: medium model format/transfer pass
7. Specialist QA: route-specific checks
8. Strong Judge: high-value, near-threshold, or disputed candidates
9. Regent Final Decision
10. Retry Planner or Packaging handoff
```

Skip rules:

- if the file cannot decode, skip visual/semantic QA and return to technical fix;
- if cheap visual QA finds severe garbage, skip expensive semantic QA unless diagnosis needs it;
- if semantic QA says the format core is lost, Specialist QA may still run only to identify fix type;
- if all lower layers pass cleanly and risk is low, Strong Judge can be skipped;
- if agents disagree on a publish-level decision, Strong Judge is required.

Every skipped layer must record:

```json
{
  "layer": "semantic_qa_level_2",
  "status": "skipped",
  "skip_reason": "technical_decode_failed",
  "skipped_by": "regent_quality_router"
}
```

---

## 16. QA Agent Passes

### 16.1 Technical QA Agents

```text
FileInspector
MediaProbe
FrameAnomalyDetector
AudioProbe
SubtitleBoundsChecker
CoverProbe
PlatformFormatChecker
TechnicalQAAssistAgent
```

Order:

```text
FileInspector -> MediaProbe -> FrameAnomalyDetector -> AudioProbe -> SubtitleBoundsChecker -> CoverProbe -> PlatformFormatChecker -> TechnicalQAAssistAgent if needed
```

TechnicalQAAssistAgent should be cheap and only used when deterministic checks are ambiguous.

Examples:

- dark horror frame vs unintended black frame;
- visible subtitle within bounds but covering face;
- cover technically valid but visually unreadable.

### 16.2 Visual QA Agents

```text
FrameSampler
SubjectPresenceJudge
IdentityStabilityJudge
ArtifactJudge
StyleMatchJudge
CompositionJudge
WatermarkTextJudge
CheapVisualAggregator
```

Order:

```text
FrameSampler -> SubjectPresenceJudge -> IdentityStabilityJudge -> ArtifactJudge -> StyleMatchJudge -> CompositionJudge -> WatermarkTextJudge -> CheapVisualAggregator
```

Visual QA must save evidence frames.

Evidence frame manifest:

```json
{
  "frame_id": "frame_000123",
  "candidate_id": "cand_000001",
  "timestamp": 4.21,
  "reason_saved": "identity_drift_evidence",
  "local_path": "..."
}
```

### 16.3 Semantic QA Agents

Semantic QA should run in levels.

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

Level 3 strong pass, only when needed:

```text
StrongSemanticJudge
AudienceAppealJudge
FinalPublishRiskJudge
```

Semantic QA should compare candidate against:

- FormatCard;
- FormatGenome;
- ReproductionPlan;
- SemanticTransfer notes;
- ProductionRecipe;
- prompts and selected assets;
- source examples where available.

Semantic QA must answer:

```text
Did the candidate preserve the format core?
Did the transfer target make sense?
Did the emotional/relationship logic survive?
Did the audience hook survive?
Did the candidate become generic AI content?
```

### 16.4 Specialist QA Agents

Specialist QA is selected by route and format type.

Specialists:

```text
MemeSpecialistQA
HorrorSpecialistQA
AbstractShortDramaSpecialistQA
MusicSyncSpecialistQA
CharacterReenactmentSpecialistQA
CPRelationshipSpecialistQA
VisualStyleSpecialistQA
PlatformPackagingSpecialistQA
MMD3DSpecialistQA
LongformSpecialistQA
```

Only relevant specialists should run.

---

## 17. Specialist QA Requirements

### 17.1 Abstract Short Drama QA

Checks:

- abstract logic is intentional, not random incoherence;
- escalation is readable;
- punchline or final image has force;
- subtitles support the absurdity;
- pacing does not flatten the joke;
- the result does not become generic surreal AI noise.

Failure tags:

```text
abstract_logic_unclear
absurdity_without_payoff
random_not_funny
escalation_flat
abstract_short_too_generic
```

### 17.2 Horror QA

Checks:

- atmosphere builds before reveal;
- threat is readable but not overexplained;
- darkness is intentional, not technical failure;
- audio supports dread;
- final beat lands;
- visual artifact does not accidentally ruin fear.

Failure tags:

```text
weak_atmosphere
cheap_jump_scare
horror_reveal_too_clear
horror_reveal_too_unclear
unintentional_comedy
fear_pacing_failed
```

### 17.3 Music Sync QA

Checks:

- key cuts match beats;
- motion or visual change lands on audio cue;
- subtitles do not fight rhythm;
- loop points are clean;
- audio is not clipped or delayed.

Failure tags:

```text
beat_mismatch
audio_visual_offset
weak_drop_moment
loop_point_bad
music_energy_mismatch
```

### 17.4 Character / CP QA

Checks:

- character identity is recognizable;
- relationship dynamic matches target CP or fandom logic;
- dialogue is not out of character;
- emotional beats fit the characters;
- visual references are used consistently;
- replacement characters preserve the source format's role logic.

Failure tags:

```text
identity_drift
ooc_character
cp_dynamic_wrong
relationship_not_clear
role_mapping_failed
character_reference_underused
```

### 17.5 Meme QA

Checks:

- viewer can understand the joke quickly;
- rhythm supports the punchline;
- format recognition is preserved;
- captions are readable and timed;
- chaos is controlled.

Failure tags:

```text
weak_punchline
meme_timing_failed
format_recognition_failed
caption_joke_mismatch
chaos_without_structure
```

---

## 18. Failure Tag Standard Table

Failure tags should be stable, searchable, and mapped to retry actions.

```text
technical_decode_failed -> fix_encode_or_regenerate_file
wrong_resolution -> reexport_or_resize
wrong_aspect_ratio -> reframe_or_reexport
fps_mismatch -> reexport
black_screen -> inspect_dark_scene_or_regenerate
frozen_frames -> regenerate_segment_or_reencode
missing_audio -> regenerate_audio_or_edit
subtitle_overflow -> subtitle_layout_fix
subtitle_timing_bad -> retime_subtitles
cover_unreadable -> rebuild_cover

subject_missing -> regenerate_visual
wrong_character_count -> revise_prompt_or_route
face_collapse -> regenerate_frame_or_reduce_complexity
hand_failure -> crop_hide_hands_or_regenerate
identity_drift -> stronger_reference_or_shorter_segments
style_mismatch -> adjust_style_prompt_or_reference
visual_noise -> regenerate_or_denoise
unwanted_text -> negative_prompt_or_inpaint
watermark_artifact -> regenerate_or_remove

format_core_lost -> return_to_reproduction_plan
beat_order_wrong -> revise_script_or_edit_order
semantic_transfer_failed -> revise_role_mapping
relationship_not_clear -> strengthen_dialogue_or_visual_cue
role_mapping_failed -> redo_semantic_transfer
pacing_failed -> edit_timing_or_reduce_beats
payoff_weak -> rewrite_final_beat
ai_genericness -> add_specific_format_constraints

weak_atmosphere -> adjust_audio_lighting_pacing
weak_punchline -> rewrite_joke_or_timing
beat_mismatch -> retime_edit
cp_dynamic_wrong -> revise_character_mapping
ooc_character -> rewrite_lines_or_action
abstract_logic_unclear -> strengthen_escalation

model_capability_gap -> switch_tool_or_route
tool_failure -> retry_tool_or_create_setup_item
asset_missing -> resolve_asset_or_ask_user
source_policy_unresolved -> create_review_item
too_expensive_to_retry -> ask_user_or_abandon
repeated_no_improvement -> switch_route_or_abandon
```

Every failure tag should include:

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

---

## 19. Retry Decision Matrix

Retry Planner should map failures to the smallest useful change.

```text
technical export issue -> reexport only
subtitle issue -> subtitle/edit step only
single bad shot -> regenerate shot only
identity drift across video -> stronger refs + shorter segments
format core lost -> return to ReproductionPlan
semantic transfer wrong -> redo SemanticTransfer, preserve source FormatCard
weak punchline -> rewrite script/payoff, preserve visual assets
music sync failed -> retime edit, preserve generated visuals if good
asset missing -> AssetResolver or ask user
tool cannot do task -> switch tool or route
too many retries -> Strong Judge or abandon
```

Default preserve policy:

```text
Preserve assets that passed QA.
Preserve prompts that produced stable identity.
Preserve generated shots that passed semantic and visual checks.
Preserve edit timing that passed music/pacing checks.
Do not preserve anything linked to a blocking failure unless explicitly justified.
```

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

---

## 20. Strong Judge and Final Judge Contract

Strong Judge should run when:

- candidate is near publish threshold;
- lower agents disagree;
- job is high-value;
- repeated retries failed;
- semantic transfer is subtle;
- user taste is likely decisive;
- final publish decision needs confidence.

Strong Judge output:

```json
{
  "layer": "strong_judge",
  "candidate_id": "cand_000001",
  "decision": "publish_ready | select_with_warnings | retry | ask_user | reject",
  "confidence": 0.0,
  "summary": "...",
  "best_parts": [],
  "blocking_issues": [],
  "non_blocking_issues": [],
  "format_preservation_score": 0.0,
  "audience_appeal_score": 0.0,
  "retry_worthiness_score": 0.0,
  "recommended_action": "..."
}
```

Regent Final Decision output:

```json
{
  "final_decision_id": "final_qc_decision_000001",
  "candidate_id": "cand_000001",
  "decision": "select_candidate | retry | ask_user | switch_route | abandon | package",
  "reason": "...",
  "quality_report_path": "...",
  "retry_plan_id": null,
  "review_item_id": null,
  "decision_log_id": "decision_000001"
}
```

Rule:

```text
Strong Judge recommends. Regent decides and records the decision.
```

---

## 21. Final Quality Report Template

Final report path:

```text
candidates/candidate_001/qc_reports/final_quality_report.json
candidates/candidate_001/qc_reports/final_quality_report.md
```

Minimum JSON shape:

```json
{
  "quality_report_id": "quality_000001",
  "candidate_id": "cand_000001",
  "job_id": "job_000001",
  "overall_status": "pass | warning | fail | needs_review",
  "overall_score": 0.0,
  "layer_results": {
    "technical_qa": "pass",
    "cheap_visual_qa": "warning",
    "semantic_qa": "pass",
    "specialist_qa": "pass",
    "strong_judge": "skipped"
  },
  "blocking_failure_tags": [],
  "non_blocking_failure_tags": [],
  "evidence_files": [],
  "preserve_recommendations": [],
  "retry_recommendations": [],
  "final_decision_recommendation": "package | retry | ask_user | reject",
  "created_at": "..."
}
```

Markdown report should show:

```text
Summary
Decision recommendation
Scores by layer
Blocking failures
Warnings
Evidence frames
What worked
What should be preserved
What should be retried
Whether Strong Judge was used
Next action
```

---

## 22. Quality Threshold Defaults

Default quality thresholds:

```yaml
quality_thresholds:
  package_ready: 7.5
  select_with_warnings: 6.8
  retry: 5.0
  reject_below: 5.0
  strong_judge_band:
    min: 6.5
    max: 7.7
```

Blocking failures override score.

Blocking examples:

```text
technical_decode_failed
format_core_lost
source_policy_unresolved
identity_drift_severe
missing_required_audio
platform_export_invalid
```

A high score with a blocking failure is not package-ready.

---

## 23. Integration Points

Quality and Retry integrates with:

```text
Generation Manager:
  receives retry plans and step-level redo instructions.

Asset Resolver:
  receives asset_missing, weak_reference, source_policy_unresolved.

Format Reproduction Council:
  receives format_core_lost, beat_order_wrong, payoff_weak.

Semantic Transfer:
  receives semantic_transfer_failed, role_mapping_failed, relationship_not_clear.

Packaging Council:
  receives package_ready candidates and packaging warnings.

Knowledge Base:
  receives tool, format, asset, prompt, and user preference memories.

Human Review Console:
  receives near-threshold, high-cost, subjective, policy, and repeated-failure review items.
```

---

## 24. Updated Ready-To-Implement Checklist

Before implementation, confirm:

- deterministic Technical QA comes first;
- agent QA uses cheap-to-strong ordering;
- Strong Judge is conditional, not default for everything;
- failure tags are stable and mapped to retry actions;
- retry plans preserve successful parts;
- route mutation is allowed;
- final decisions are made by Regent with DecisionLog;
- reports exist in both JSON and Markdown;
- thresholds and weights are configurable;
- QA can create ReviewItems and ToolSetupItems;
- QA memory writeback never silently changes core rules.

---

## Cross-Phase Policy Alignment - 2026-06-06

QA aesthetic defaults:

```text
Default strong-judge preference order:
  first: resembles the hot format, has a hook, has sharing potential
  second: character accuracy, visual stability, completion quality

Type-specific weights:
  character-focused video: higher character accuracy
  abstract short drama: higher joke/rhythm
  MMD/3D: higher motion, clipping, and stability
```

Retry:

```text
Retry patience is configurable, not hardcoded.
Default recommendation: 3-5 normal retries per job.
Repeated same-type failure or cost/time overrun creates ReviewItem.
High-cost route retries ask before each round.
```
