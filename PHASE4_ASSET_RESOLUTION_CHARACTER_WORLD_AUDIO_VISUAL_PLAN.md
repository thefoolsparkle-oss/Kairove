# Kairove Phase 4: Asset Resolution, Character/World Knowledge, Audio/Visual Material System Plan

## 0. Status

Current status:

```text
Phase 4: detailed planning draft, not yet confirmed for implementation
Depends on: P3 ProductionRecipeDraft and AssetRequirementDraft
Primary output: AssetResolutionReport and knowledge/reference packs for generation
Related capability docs: AUDIO_VISUAL_ASSET_SYSTEM_PLAN.md, SOURCE_SCOUT_AND_HARVEST_PLAN.md
```

---

## 1. Purpose

Phase 4 resolves the materials needed for production.

It answers:

```text
What assets, references, voices, audio, styles, characters, world knowledge, and source materials are available, usable, missing, generated, or waiting for the user?
```

It is the bridge between creative planning and generation execution.

---

## 2. One-Line Scope

```text
ProductionRecipeDraft + AssetRequirementDraft -> AssetResolutionReport + ReferencePacks + updated AssetManifests
```

---

## 3. Must Include

```text
Typed Asset Resolution:
  Every requirement ends as resolved, generated, substituted, waiting_for_user, blocked, or deferred.

Local Asset Search:
  User-curated local assets and trained voices are checked first.

Research Asset Search:
  P1/P2 collected research evidence can be reused as references.

Official/Wiki/Web Search:
  Find official and wiki references when allowed and technically available.

Audio and Voice Handling:
  Identify, locate, request, train, or substitute music, SFX, BGM, voice, and TTS requirements.

Visual Reference Handling:
  Build character, world, style, subtitle, cover, and scene reference packs.

Policy Handling:
  Official assets can be direct-use under current user policy; personal creator and unknown assets require review before direct use.

Provenance:
  Every file/reference needs source, policy, review state, and usage link.
```

---

## 4. Must Not Include

```text
final video generation
untracked downloads
mixing research/local/generated asset folders
unreviewed personal creator direct-use
fake asset availability
silent voice training
MMD/3D compatibility implementation beyond asset metadata
publishing
```

---

## 5. Inputs

```text
ProductionRecipeDraft
AssetRequirementDraft
ReproductionPlan
SemanticTransferPlan
ScriptPackage
ShotPlan
local asset inventory
research asset manifests
Source records and SourceManifests
Tool registry snapshot
Permission snapshot
UserPreference
Character/World/Relationship memory
```

Optional:

```text
user-provided folders
user-trained voice profiles
official model/material folders
manual asset notes
```

---

## 6. Outputs

```text
AssetResolutionReport
CharacterReferencePack
WorldReferencePack
RelationshipReferencePack
AudioRequirementReport
VoiceProfileResolutionReport
VisualReferencePack
StyleReferencePack
SubtitleStylePack
CoverReferencePack
SceneReferencePack
ToolSetupItems
ReviewItems
updated AssetManifests
Phase4AssetReport
```

Primary handoff:

```text
AssetResolutionReport -> P5 Generation Route and Candidate Generation
```

---

## 7. Workstreams

```text
P4-A Requirement Normalization
P4-B Local Asset Inventory Search
P4-C Research Asset Reuse
P4-D Official/Wiki/Web Reference Search
P4-E Character/World/Relationship Knowledge Builder
P4-F Audio/Music/SFX/Voice Resolver
P4-G Visual/Style/Subtitle/Cover Resolver
P4-H Policy and Review Handling
P4-I Generated/Substitute Asset Planning
P4-J Asset Manifest and Report Writer
```

---

## 8. Resolution Order

Default order:

```text
1. Existing local assets
2. User-curated official assets
3. User-trained voices and local trained assets
4. Official pages and official platform accounts
5. Wiki/reference pages
6. Research assets collected by P1/P2
7. Broader web references when allowed
8. Generated substitutes
9. Ask user
10. Defer or block
```

Reason:

```text
local and official assets are usually more stable and easier to reuse;
research assets preserve trend provenance;
generated substitutes keep production moving;
human tasks are used when automation cannot honestly resolve the need.
```

---

## 9. Asset Requirement Record

```json
{
  "requirement_id": "asset_req_000001",
  "job_or_recipe_id": "recipe_draft_000001",
  "asset_type": "character_reference",
  "target": "target_character_a",
  "required": true,
  "usage_needed": "direct_use | reference_only | style_analysis | generation_input",
  "preferred_source_types": ["official", "wiki", "local"],
  "quality_bar": "draft | normal | high | critical",
  "fallback_policy": "generate | substitute | ask_user | defer | block",
  "source_reason": "needed for character identity stability",
  "status": "unresolved"
}
```

---

## 10. AssetResolutionReport

```json
{
  "asset_resolution_report_id": "asset_res_000001",
  "production_recipe_draft_id": "recipe_draft_000001",
  "requirements_total": 0,
  "resolved": [],
  "generated_planned": [],
  "substituted": [],
  "waiting_for_user": [],
  "blocked": [],
  "review_items": [],
  "tool_setup_items": [],
  "overall_status": "ready | ready_with_warnings | waiting_for_user | blocked"
}
```

The Markdown report must show:

```text
requirement
chosen asset/reference
source/provenance
usage policy
review state
quality notes
fallback if rejected
what P5 may use it for
```

---

## 11. Character and World Knowledge

P4 should build reference packs, not final scripts.

CharacterReferencePack:

```json
{
  "character_pack_id": "char_pack_000001",
  "character_name": "...",
  "source_refs": [],
  "visual_profile": {
    "hair": [],
    "eyes": [],
    "outfit": [],
    "colors": [],
    "signature_props": [],
    "must_preserve": []
  },
  "personality_notes": [],
  "speech_style_notes": [],
  "relationship_notes": [],
  "ooc_risks": [],
  "confidence": 0.0
}
```

WorldReferencePack:

```text
locations
props
UI elements
visual motifs
setting rules
common scenes
what would feel wrong in this world
```

RelationshipReferencePack:

```text
relationship type
canonical / fanon / user-preferred status
dynamic
format fit
risk notes
user verification state
```

---

## 12. Audio and Voice Resolution

AudioRequirementReport should cover:

```text
music/song identity
sound meme source
BGM need
SFX need
voice/TTS need
beat/timing requirement
whether original audio is needed or only timing/reference
policy state
fallbacks
```

Voice outcomes:

```text
local_voice_profile_available
TTS_voice_available
voice_training_needed
user_audio_needed
voice_not_required
subtitles_only_fallback
```

Rules:

```text
voice training never happens silently
if the program can train a voice, it should create and register the training material path and review state
if it cannot train, it should tell the user exactly what material/tool is needed
```

---

## 13. Visual and Style Resolution

VisualReferencePack should include:

```text
character references
style references
scene/background references
subtitle style references
cover style references
AI-method/style clues
negative references: what to avoid
```

Style extraction should describe:

```text
composition
lighting
color palette
camera language
texture/render look
subtitle layout
cover composition
editing rhythm where visually inferable
```

Style references from personal creators may be `style_analysis` or `reference_only` until approved.

---

## 14. Generated and Substitute Assets

P4 may plan generated/substitute assets, but P5 performs generation.

GeneratedAssetPlan fields:

```json
{
  "generated_asset_plan_id": "gen_asset_plan_000001",
  "requirement_id": "asset_req_000001",
  "reason": "official scene reference missing",
  "asset_type": "background_reference",
  "prompt_intent": "generate a classroom-like equivalent matching target world mood",
  "input_refs": [],
  "tool_needs": ["image_generation"],
  "quality_requirements": [],
  "fallback_if_failed": "ask_user"
}
```

---

## 15. Policy and Review

Policy defaults:

```text
official game/anime/PV/image/music/SFX assets -> direct_use allowed with provenance
personal creator assets -> review required before direct_use
unknown assets -> review required
official-like misleading risk -> not blocking under current user policy
```

ReviewItems should be created for:

```text
personal creator direct-use
unknown source direct-use
uncertain official status
voice training permission
missing local model/material
asset quality below required bar
manual file request
high-impact substitution
```

---

## 16. Storage Layout

```text
runs/run_000001/phase4/
  normalized_requirements/
  local_asset_search/
  official_reference_search/
  character_packs/
  world_packs/
  relationship_packs/
  audio_reports/
  voice_reports/
  visual_reference_packs/
  style_packs/
  generated_asset_plans/
  asset_resolution_report.json
  asset_resolution_report.md

local_assets/
  user_curated/
  voices/
  models/
  official_materials/

research_assets/
  references/
  snapshots/
  source_downloads/

generated_assets/
  planned/
```

Generated outputs do not enter `generated_assets` until P5 actually generates or imports them.

---

## 17. Tests

Fixture groups:

```text
official character reference found
wiki reference only
local trained voice available
voice missing and training unavailable
personal creator image direct-use requested
unknown music source
hot audio timing reference only
generated substitute needed
required asset blocked
```

Required tests:

```text
normalizes P3 asset requirements
searches local assets first
classifies official/personal/unknown policy
creates ReviewItem for personal/unknown direct-use
creates ToolSetupItem for missing training/search capability
writes CharacterReferencePack
writes AudioRequirementReport
writes VisualReferencePack
writes AssetResolutionReport
blocks job when required asset is unresolved
never mixes research/local/generated asset folders
```

---

## 18. Acceptance Criteria

P4 is ready when Kairove can:

```text
read typed requirements from P3
resolve local/research/official/wiki assets where available
build character/world/audio/visual reference packs
track provenance and policy for every asset/reference
create review items for uncertain or personal assets
create setup items for unavailable capabilities
plan generated substitutes without generating them silently
write asset manifests and AssetResolutionReport
handoff ready assets and blockers to P5
pass fixture-based tests
```

---

## 19. Non-Acceptance

P4 is not acceptable if:

```text
it says an asset exists when it only guessed
it downloads or uses personal creator assets directly without review
it mixes asset folders
it trains voices without review
it hides missing materials
it generates final assets without P5 tracking
it drops source provenance
it blocks every missing asset instead of proposing useful fallbacks
```

---

## 20. Confirmation Checklist

Before P4 implementation, confirm or revise:

```text
asset resolution order
current official/personal/unknown policy
voice training behavior
whether broader web search is enabled for references
which local asset folders the user will maintain
whether generated substitutes are allowed by default
```

---

## Cross-Phase Policy Alignment - 2026-06-06

P4 asset and knowledge handling must follow:

```text
Maintain all three knowledge pack types:
  work pack
  character pack
  relationship/CP pack

Relationship packs are important because many transfers depend on relationship function, not only single-character facts.
```

Asset policy:

```text
Official assets can be direct-use with provenance under current user policy.
Personal creator or unknown assets:
  first search for official or substitute assets
  ask the user before direct use

Reference/style analysis can be more permissive than direct use, but direct use requires review.
```

Music and SFX:

```text
Official music/SFX can be direct-use with provenance.
Music requires extra platform-risk notes.
Minimum music/SFX fields: source, work/song title, official owner/account, usage, platform risk note.
Personal or unknown music/SFX sources default to review.
```
