# Kairove Phase 3: Reproduction Planning, Semantic Transfer, Script and Direction Plan

## 0. Status

Current status:

```text
Phase 3: detailed planning draft, not yet confirmed for implementation
Depends on: P0-B, P1, P2 planning contracts
Primary input: ProductionStartPacket
Primary output: ProductionRecipeDraft and direction package for P4/P5
```

Phase 3 is detailed because the user chose to detail all remaining phases. It should still be confirmed before coding begins.

---

## 1. Purpose

Phase 3 turns a selected opportunity into a production-intent package.

P2 says:

```text
This format is worth making.
```

P3 says:

```text
What exactly are we reproducing, what are we changing, who/what replaces the original roles, what should the script/shot/direction be, and what must later phases preserve?
```

This phase is not only for short drama. It covers imitation and transformation across many video types:

```text
short drama imitation
character or CP reenactment
music/sound meme adaptation
horror short planning
abstract short planning
meme edit planning
visual style imitation planning
AI-method imitation planning
ordinary AI video production planning
```

---

## 2. One-Line Scope

```text
ProductionStartPacket -> ReproductionPlan + SemanticTransferPlan + Script/Shot/Direction Package + ProductionRecipeDraft
```

---

## 3. Must Include

```text
Reproduction Strategy:
  Decide what part of the source format is the actual reusable core.

Semantic Transfer:
  Map source roles, relationships, emotion, joke, conflict, setting, and symbols to a target world, character set, style, or generic AI version.

Script and Text Planning:
  Produce scripts, captions, subtitle beats, narration, or text overlays only when the format needs them.

Direction Planning:
  Produce shot plan, pacing, audio cues, edit rhythm, visual instructions, and coverable moments.

Council Selection:
  Choose primary and supporting councils without making them mutually exclusive.

Production Recipe Draft:
  Hand P4/P5 a structured plan with asset requirements, route needs, and quality expectations.

Review Items:
  Ask for user review when subjective mapping, CP/character fit, high-cost route, or risky source use is unclear.
```

---

## 4. Must Not Include

```text
full asset search/download
final asset resolution
actual generation calls
candidate QA
publishing
post-publish learning
MMD/3D implementation
longform implementation
silent character/CP assumptions when confidence is low
```

P3 can request assets and tools, but it does not resolve or run them.

---

## 5. Inputs

```text
ProductionStartPacket
Format
FormatGenome
TrendScorecard
ScoreExplanationReport
representative Source records
UnderstandingReports
UserPreference
known Character / Relationship / World memory
Tool registry snapshot
Permission snapshot
existing asset inventory summary
```

Optional inputs:

```text
user-chosen character / fandom / CP
user-provided target style
user-provided target script idea
platform emphasis
local asset hints
```

---

## 6. Outputs

```text
ReproductionPlan
SemanticTransferPlan
ScriptPackage
ShotPlan
DirectorBrief
CouncilSelectionReport
ProductionRecipeDraft
AssetRequirementDraft
QualityExpectationDraft
ReviewItems
DecisionLogs
Phase3PlanningReport
```

Primary handoff:

```text
ProductionRecipeDraft -> P4 Asset Resolution and P5 Generation Route Planning
```

---

## 7. Workstreams

```text
P3-A Input and Format Core Loader
P3-B Reproduction Strategy Council
P3-C Semantic Transfer Council
P3-D Target Casting and World Mapping
P3-E Script/Text/Caption Council
P3-F Shot, Timing, Audio, and Direction Council
P3-G Route Intent and Council Selection
P3-H ProductionRecipeDraft Builder
P3-I Review Report and Tests
```

These are internal workstreams, not separate phases.

---

## 8. Operating Flow

```text
1. Load ProductionStartPacket and evidence.
2. Identify source format core from FormatGenome.
3. Separate must-preserve, should-preserve, can-change, and avoid elements.
4. Decide target adaptation strategy.
5. Generate semantic role mappings.
6. If character/world target exists, evaluate fit and OOC/relationship risks.
7. If no target exists, propose generic, original, official-IP, or user-review options.
8. Select primary and supporting councils.
9. Build script/caption/narration only where required.
10. Build shot plan and direction notes.
11. Derive typed asset requirements.
12. Derive generation route intent and quality expectations.
13. Create ReviewItems for uncertain subjective decisions.
14. Write ProductionRecipeDraft and Phase3PlanningReport.
```

---

## 9. Agent Order

Default agent order:

```text
1. FormatCoreInterpreter
2. MustPreserveExtractor
3. ReplaceableSlotExtractor
4. AdaptationStrategyGenerator
5. SemanticRoleExtractor
6. RelationshipMapper
7. WorldAdaptationAgent
8. CharacterFitAgent
9. TonePreservationAgent
10. ScriptNeedClassifier
11. ScriptCouncil or CaptionCouncil if needed
12. ShotPlanner
13. AudioCuePlanner
14. EditRhythmPlanner
15. RouteIntentClassifier
16. CouncilSelectionAgent
17. ProductionRecipeAssembler
18. ReviewItemAgent
19. Phase3ReportWriter
```

Escalate to stronger models when:

```text
semantic transfer is subtle
character/CP mapping is disputed
script feels generic or AI-like
format core and target world conflict
production route is expensive
P3 decision would strongly affect generation cost
```

---

## 10. ReproductionPlan

Purpose:

```text
Define what Kairove is trying to reproduce before it writes scripts or asks for assets.
```

Schema:

```json
{
  "reproduction_plan_id": "repro_000001",
  "production_start_packet_id": "psp_000001",
  "format_id": "fmt_000001",
  "primary_reproduction_target": "relationship rhythm and evidence-reveal punchline",
  "must_preserve": [],
  "should_preserve": [],
  "can_change": [],
  "must_avoid": [],
  "adaptation_strategy": "character_reenactment | style_transfer | meme_edit | horror_remix | music_sync | generic_remake | hybrid",
  "confidence": 0.0,
  "evidence_refs": [],
  "review_items": []
}
```

Rules:

```text
must_preserve should be small and strict
can_change should be explicit so later phases do not overfit the source
must_avoid includes unapproved personal creator lines/assets and route-specific failure risks
```

---

## 11. Semantic Transfer

Semantic transfer is not keyword replacement.

It maps functions:

```text
source role -> target role
source desire/conflict -> target desire/conflict
source evidence object -> target equivalent object
source emotional turn -> target emotional turn
source setting logic -> target setting logic
source audience recognition cue -> target audience recognition cue
```

Example:

```text
real couple mouth-hard denial short drama
-> anime/game CP teasing dynamic
-> one character denies wanting a gacha item / attention / victory / snack / praise
-> the other reveals evidence in a way that fits that world
```

SemanticTransferPlan schema:

```json
{
  "semantic_transfer_plan_id": "sem_transfer_000001",
  "reproduction_plan_id": "repro_000001",
  "source_roles": [],
  "target_roles": [],
  "role_mappings": [],
  "relationship_mapping": {},
  "setting_mapping": {},
  "object_symbol_mapping": {},
  "emotion_mapping": {},
  "joke_or_conflict_mapping": {},
  "what_breaks_if_changed": [],
  "fit_score": 0.0,
  "ooc_risk": "low | medium | high | unknown",
  "needs_user_review": false
}
```

---

## 12. Target Selection Modes

P3 supports multiple target modes:

```text
user_selected_character_or_cp
program_suggested_character_or_cp
official_ip_character_adaptation
generic_ai_character_adaptation
original_character_adaptation
style_only_adaptation
music_or_dance_adaptation
horror_or_abstract_adaptation
```

If target selection is uncertain:

```text
create ranked options
show why each works or fails
create ReviewItem instead of silently picking a high-impact target
```

---

## 13. Script and Text Package

Script Council runs only when script/text is central.

ScriptPackage may contain:

```text
spoken_dialogue
narration
subtitle_lines
on-screen text
cover text hooks
pinned comment idea
beat-by-beat text timing
```

Schema:

```json
{
  "script_package_id": "script_000001",
  "job_id": null,
  "format_id": "fmt_000001",
  "mode": "dialogue | narration | subtitles_only | text_overlay | none",
  "beats": [
    {
      "beat_id": "beat_01",
      "function": "setup_denial",
      "line": "...",
      "duration_hint": "fit_format",
      "visual_need": "close reaction",
      "audio_need": "short silence before reveal"
    }
  ],
  "anti_ai_text_notes": [],
  "character_voice_notes": [],
  "review_items": []
}
```

Anti-AI-text checks are guidelines, not hard universal rules. Different video types can require stiff narration, chaotic meme text, horror understatement, or direct platform-native captions.

---

## 14. ShotPlan and DirectorBrief

ShotPlan describes how the video should be seen, not how to generate it yet.

ShotPlan fields:

```json
{
  "shot_plan_id": "shotplan_000001",
  "duration_policy": "fit_format",
  "aspect_ratio_intent": "platform_default | vertical | horizontal | flexible",
  "beats": [],
  "shots": [
    {
      "shot_id": "shot_01",
      "beat_id": "beat_01",
      "shot_type": "closeup | medium | wide | insert | reaction | montage | text_card",
      "visual_intent": "...",
      "camera_notes": "...",
      "audio_notes": "...",
      "subtitle_notes": "...",
      "required_assets": []
    }
  ],
  "edit_rhythm": "fast_meme | slow_horror | dialogue_reaction | music_sync | narrative",
  "coverable_moments": []
}
```

DirectorBrief is the human-readable summary:

```text
what the video should feel like
what viewers should understand in the first seconds
what the payoff is
what not to over-explain
what must be checked in QA
```

---

## 15. Council Selection

P3 chooses councils without making them mutually exclusive.

Possible councils:

```text
script_council
caption_council
character_reenactment_council
semantic_transfer_council
music_sync_council
visual_style_council
horror_atmosphere_council
abstract_short_council
meme_edit_council
dance_motion_council
ai_tool_imitation_council
hybrid_council
```

CouncilSelectionReport:

```json
{
  "primary_council": "character_reenactment_council",
  "supporting_councils": ["script_council", "meme_edit_council"],
  "not_used": [
    {"council": "music_sync_council", "reason": "audio is supporting, not structural"}
  ],
  "route_intent": "ordinary_ai_format_video",
  "confidence": 0.0
}
```

---

## 16. AssetRequirementDraft

P3 outputs requirements, not resolved assets.

Requirement categories:

```text
character_reference
relationship_reference
world_reference
scene_reference
style_reference
audio_reference
music_or_bgm
sound_effect
voice_or_tts
subtitle_style
cover_style
source_video_reference
special_tool_or_method
```

Each requirement should include:

```text
why needed
required vs optional
preferred source policy
quality bar
fallback policy
whether user-provided material may be needed
```

---

## 17. ProductionRecipeDraft

ProductionRecipeDraft is the main P3 handoff object.

```json
{
  "production_recipe_draft_id": "recipe_draft_000001",
  "production_start_packet_id": "psp_000001",
  "reproduction_plan_id": "repro_000001",
  "semantic_transfer_plan_id": "sem_transfer_000001",
  "script_package_id": "script_000001",
  "shot_plan_id": "shotplan_000001",
  "council_selection_report_id": "council_select_000001",
  "recommended_job_type": "ordinary_ai_format_video",
  "route_intents": [],
  "asset_requirements": [],
  "quality_expectations": [],
  "review_items": [],
  "created_at": "..."
}
```

It becomes a full `ProductionRecipe` only after P4 resolves assets and P5 confirms generation route feasibility.

---

## 18. Review Triggers

Create ReviewItems for:

```text
uncertain CP or relationship mapping
uncertain character fit
high OOC risk
unclear target world
source format core disputed
script direction subjective
style transfer may overcopy personal creator
AI-method imitation unavailable
expensive route likely required
user preference conflict
```

Official-like misleading risk is not blocking under current user policy.

---

## 19. Storage Layout

```text
runs/run_000001/phase3/
  input_refs.json
  reproduction_plans/
  semantic_transfer_plans/
  script_packages/
  shot_plans/
  director_briefs/
  council_selection/
  production_recipe_drafts/
  phase3_planning_report.md
```

P3 should reference research assets and P2 evidence instead of copying large files.

---

## 20. Tests

Fixture groups:

```text
real couple dialogue -> anime/game CP transfer
music trend -> character visual adaptation
horror source -> original horror adaptation
abstract short -> meme edit adaptation
same format with no target character
character target with weak fit
script-free visual format
AI-method imitation unavailable
```

Required tests:

```text
loads ProductionStartPacket
creates ReproductionPlan
extracts must-preserve/can-change fields
creates SemanticTransferPlan
creates ScriptPackage only when needed
creates ShotPlan
creates AssetRequirementDraft
creates ProductionRecipeDraft
creates ReviewItems for uncertainty
does not resolve assets or generate candidates
```

---

## 21. Acceptance Criteria

P3 is ready when Kairove can:

```text
turn selected P2 opportunity into a clear reproduction strategy
perform semantic transfer into target or generic context
create script/caption/shot packages when needed
choose primary and supporting councils
write typed asset requirements
write quality expectations
write ProductionRecipeDraft
record subjective uncertainty as ReviewItems
hand off cleanly to P4/P5
pass fixture-based tests
```

---

## 22. Non-Acceptance

P3 is not acceptable if:

```text
it assumes every video is a short drama
it treats semantic transfer as text replacement
it silently chooses risky character/CP mapping
it writes generic AI scripts without format-specific constraints
it starts generation
it claims assets are resolved
it ignores P2 must-preserve fields
it makes councils mutually exclusive when hybrid planning is needed
```

---

## 23. Confirmation Checklist

Before P3 implementation, confirm or revise:

```text
primary output is ProductionRecipeDraft
script council is conditional, not always central
semantic transfer supports character, style, generic, horror, music, meme, and abstract adaptations
P3 does not resolve assets or generate video
P4 receives asset requirements
P5 receives route intent and production draft
```

---

## Cross-Phase Policy Alignment - 2026-06-06

P3 semantic transfer must preserve format function:

```text
Must not change:
  core joke/payoff/scare/emotion curve
  role relationship function
  rhythm
  reversal mechanism
  audience recognition point

May change:
  characters
  world setting
  art style
  exact lines
  scene details

Acceptance principle:
  the audience can still recognize the same transferred format.
```

Language defaults:

```text
Reports/plans/review items: Chinese primary.
Internal object IDs and schema/config keys: English.
Prompts may keep Chinese explanation plus English generation prompt for tool effectiveness.
```
