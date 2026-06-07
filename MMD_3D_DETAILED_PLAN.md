# Kairove MMD / 3D Detailed Plan

## 0. Purpose

This document expands the MMD / VRM / 3D route in detail.

MMD / 3D is a specialized Kairove production route. It is not the core identity of the project, but it is important because it can provide stable characters, stable motion, and controllable camera work that pure AI video often struggles with.

The main goal is not to pretend 3D is easy. The goal is:

```text
diagnose clearly
prefer verified combinations
preview before final render
explain failures in human language
feed results into the normal AI/video/QA/publish pipeline
```

---

## 1. Plain-Language 3D Concepts

Kairove should explain 3D to the user in production terms.

```text
Model:
  The character body, face, clothes, bones, materials, and textures.

Motion:
  How the character moves. In MMD this is often VMD.

Camera:
  How the virtual camera films the character.

Stage:
  The background or location.

Lighting:
  The lights that make the model readable and attractive.

Physics:
  Simulated hair, skirt, accessories, and cloth movement.

Render:
  Turning the 3D scene into image frames or video.

AI Enhancement:
  Using AI to improve, stylize, extend, or transform rendered output.
```

Kairove should translate technical errors into human-readable explanations.

Example:

```text
Technical:
  bone mismatch / missing morph / broken material texture path

User-facing:
  This motion does not fit this model well. Some body parts, fingers, or expressions may not move correctly.
```

---

## 2. Why This Route Is Hard

Common problems:

- model cannot import;
- textures missing;
- Japanese/Chinese path encoding issues;
- VMD motion does not match model bones;
- finger motion breaks;
- face morphs do not work;
- hair/skirt physics explode;
- clothing clips through body;
- camera does not frame well vertically;
- Blender plugin version mismatch;
- render is too slow;
- AI enhancement changes the character.

Kairove must detect these problems early and tell the user what is missing.

---

## 3. 3D Asset Metadata

### 3.1 Model Metadata

```json
{
  "asset_id": "asset_model_0001",
  "model_format": "pmx",
  "character_name": "...",
  "source_type": "official | user_provided | unknown",
  "usage_policy": "direct_use",
  "has_textures": true,
  "texture_paths_valid": true,
  "bone_profile": {
    "has_standard_mmd_bones": true,
    "has_finger_bones": true,
    "has_ik": true
  },
  "morph_profile": {
    "has_eye_morphs": true,
    "has_mouth_morphs": true,
    "has_expression_morphs": true
  },
  "physics_profile": {
    "has_rigid_bodies": true,
    "has_joints": true,
    "risk": "low | medium | high"
  },
  "known_issues": []
}
```

### 3.2 Motion Metadata

```json
{
  "asset_id": "asset_motion_0001",
  "motion_format": "vmd",
  "motion_type": "dance | reaction | walk | pose | camera | unknown",
  "estimated_duration": null,
  "requires_standard_bones": true,
  "uses_finger_motion": true,
  "uses_expression_morphs": true,
  "complexity": "low | medium | high",
  "known_good_models": [],
  "known_bad_models": []
}
```

### 3.3 Camera Metadata

```json
{
  "asset_id": "asset_camera_0001",
  "camera_format": "vmd | json | generated",
  "orientation": "horizontal | vertical | unknown",
  "shot_type": "full_body | closeup | medium | mixed",
  "vertical_safe": false,
  "known_issues": []
}
```

---

## 4. Verified Combo System

Arbitrary model + motion combinations are risky. Kairove should maintain verified combos.

```json
{
  "combo_id": "mmd_combo_0001",
  "model_asset_id": "asset_model_0001",
  "motion_asset_id": "asset_motion_0001",
  "camera_asset_id": "asset_camera_0001",
  "stage_asset_id": "asset_stage_0001",
  "render_profile": "vertical_1080x1920_30fps",
  "status": "verified | usable_with_warnings | failed | unknown",
  "best_use": ["dance_short", "character_showcase"],
  "known_issues": ["minor hair clipping around frame 120"],
  "last_tested_at": "..."
}
```

Status meanings:

```text
unknown:
  Not tested.

testing:
  Test render in progress.

verified:
  Works well enough for production.

usable_with_warnings:
  Works, but has known issues.

failed:
  Not suitable unless repaired.
```

Generation Manager should prefer verified combos.

---

## 5. 3D Readiness Check

Before rendering, run a readiness check.

### 5.1 Environment Readiness

Check:

- Blender executable exists;
- Blender version known;
- MMD Tools installed if needed;
- Python environment compatible;
- FFmpeg available;
- output directory writable;
- GPU/render device info if available.

Output:

```json
{
  "environment_ready": false,
  "missing": ["mmd_tools_plugin"],
  "human_message": "Blender is installed, but the MMD Tools plugin is not detected."
}
```

### 5.2 Model Readiness

Check:

- file exists;
- format supported;
- can import;
- textures found;
- materials readable;
- bones present;
- morphs present;
- physics data present;
- scale reasonable.

### 5.3 Motion Readiness

Check:

- motion file exists;
- duration readable;
- bone names compatible;
- unsupported bones/morphs;
- high-complexity hand/finger movement;
- known compatibility history.

### 5.4 Camera Readiness

Check:

- camera exists or can be generated;
- vertical framing;
- subject visible;
- full-body vs close-up suitability;
- no extreme movement unless intended.

### 5.5 Render Readiness

Check:

- resolution;
- fps;
- frame range;
- output path;
- disk space if possible;
- expected render time estimate if possible.

---

## 6. Human-Friendly Failure Diagnosis

Every failure should include:

1. technical error;
2. likely cause;
3. user-facing explanation;
4. suggested fixes;
5. whether it blocks production.

Example:

```json
{
  "failure_tag": "bone_mismatch",
  "technical_detail": "Motion references bones not found on model.",
  "human_message": "This motion does not fit the current model. Some body parts may not move or may twist.",
  "suggested_fixes": [
    "Use a motion known to work with this model.",
    "Try a simpler pose or reaction motion.",
    "Ask Kairove to search for a compatible motion.",
    "Manually repair or retarget the motion."
  ],
  "blocking": true
}
```

---

## 7. 3D Production Workflows

### 7.1 Character Showcase

Goal:

```text
Show character appearance, outfit, face, and pose.
```

Route:

```text
model -> simple pose/motion -> generated camera -> render key shots -> optional AI enhancement
```

This is a good first 3D workflow because it requires less complex motion.

### 7.2 Short Dance / Motion Clip

Goal:

```text
Use a verified model + motion combo to produce a short vertical dance or action clip.
```

Route:

```text
model + motion + camera + music -> render -> QA -> optional AI enhance -> package
```

### 7.3 3D Reference for AI Video

Goal:

```text
Use 3D to create stable pose/composition references, while final video may be AI-generated.
```

Route:

```text
3D keyframes -> image prompts/reference -> image/video generation -> edit
```

### 7.4 AI Enhanced 3D

Goal:

```text
Keep 3D motion stable while improving atmosphere or style with AI.
```

Risks:

- AI changes face;
- outfit changes;
- identity drift;
- motion distortion.

Needs strong identity QA.

---

## 8. Render Profiles

Render profiles should be config-driven.

```yaml
vertical_short:
  width: 1080
  height: 1920
  fps: 30
  max_duration_seconds: 20
  camera_safe_area: true

vertical_preview:
  width: 540
  height: 960
  fps: 15
  purpose: "fast QA preview"

keyframe_export:
  output: "png_sequence"
  frames: ["first", "middle", "last", "important_beats"]
```

Kairove should use preview renders before expensive final renders.

---

## 9. 3D-Specific QA

Checks:

- model imported correctly;
- textures visible;
- motion applied;
- camera follows subject;
- no severe clipping;
- no physics explosion;
- face/expression acceptable;
- vertical framing correct;
- render duration/fps correct;
- audio sync if music/dance;
- AI enhancement does not damage identity.

Failure tags:

```text
model_import_failed
missing_textures
motion_retarget_failed
bone_mismatch
physics_explosion
clipping_issue
camera_off_subject
render_failed
plugin_missing
identity_changed_by_ai
```

---

## 10. 3D Retry Strategies

```text
model_import_failed:
  check plugin, file path, format, encoding, missing dependencies.

missing_textures:
  search texture folder, ask user, render with fallback material.

motion_retarget_failed:
  choose compatible motion, simplify motion, use pose-only route.

camera_off_subject:
  generate default vertical camera, use subject tracking, crop in edit.

physics_explosion:
  disable physics for preview, reduce physics, use shorter clip.

clipping_issue:
  change camera angle, crop, choose different pose/motion.

render_too_slow:
  lower preview settings, render keyframes only, use Eevee-style preview route.
```

---

## 11. 3D Human Tasks

Create human tasks when:

- Blender not installed;
- plugin missing;
- model file broken;
- motion incompatible and no alternative found;
- texture missing and cannot be located;
- user must approve model source;
- manual retargeting needed;
- render result is visually wrong but technically valid.

Task example:

```json
{
  "task_type": "mmd_setup_needed",
  "summary": "MMD Tools plugin is missing in Blender.",
  "impact": "PMX/VMD route cannot run.",
  "user_action_needed": [
    "Install MMD Tools plugin",
    "Run environment check again"
  ]
}
```

---

## 12. 3D Route Stages (Not Global Phases)

These are internal 3D route stages. They are not global Kairove implementation phases and should not be counted in the main Phase 0 / Phase 1 roadmap.

### 3D Route Stage 0: Environment Detection

- Blender path config;
- FFmpeg path config;
- plugin detection;
- environment report.

### 3D Route Stage 1: Asset Registry

- model registry;
- motion registry;
- camera/stage registry;
- metadata extraction where possible.

### 3D Route Stage 2: Readiness Check

- model file exists;
- motion file exists;
- combo readiness report;
- human-friendly failure messages.

### 3D Route Stage 3: Preview Render

- one verified PMX;
- one verified VMD;
- default camera;
- low-res preview render;
- frame export.

### 3D Route Stage 4: Full Render

- vertical 1080x1920 render;
- audio sync if needed;
- FFmpeg output;
- technical QA.

### 3D Route Stage 5: AI Enhancement

- keyframe export;
- AI enhancement interface;
- identity QA.

---

## 13. P10 Compatibility and Repair Policy

Earlier drafts were too conservative about 3D compatibility. The current P10 boundary treats compatibility and repair as core requirements, not optional extras.

Default assumptions:

```text
Models are treated as usable by default for the user's local production flow.
Kairove should attempt direct use, compatibility mapping, and repair before marking a model/motion combo as unusable.
Source, terms, repair history, and usage must still be recorded.
Risk warnings can create ReviewItems, but they should not silently block the user's personal workflow unless the user config says so.
```

P10 must try to handle:

```text
import failures
texture path repair
Japanese/Chinese filename and path encoding issues
missing texture relinking
material/shader cleanup
scale/origin/axis normalization
standard MMD bone detection
non-standard bone mapping
bone rename/mapping profiles
IK chain issues
finger bone mismatch
face/mouth/eye morph mismatch
VMD motion retargeting where possible
camera framing repair
vertical framing conversion
stage/camera scale mismatch
physics instability
rigid body / joint sanity checks
hair/skirt/accessory physics tuning
cloth/body clipping detection
basic clipping mitigation
render failure recovery
AI enhancement identity drift checks
```

Repair approach:

```text
1. Detect issue.
2. Choose repair recipe.
3. Save repaired derivative as generated/local working asset, never overwrite the original silently.
4. Record before/after metadata.
5. Run preview render.
6. Run 3D QA.
7. Mark combo as verified, usable_with_warnings, needs_manual_fix, or failed.
```

Important nuance:

```text
P10 should aim for broad model/motion compatibility and automatic repair.
P10 must not pretend repair succeeded without preview and QA.
```

Candidate helper tools to support later:

```text
Blender
MMD Tools
PMX Editor / PMXE style workflows
VMD retargeting utilities
VRM import/export tools
FFmpeg
future local scripts for bone/morph/physics repair
```

This means P10 is not merely a route registry. It is a 3D compatibility, repair, preview, and QA route.

---

## 14. Final Principle

Kairove should not treat MMD/3D as magic.

It should treat it as a high-control but high-friction route:

```text
inspect -> verify combo -> preview -> QA -> render -> optional AI enhance -> normal package/publish pipeline
```

---

## 14. Route Summary (Merged)

Merged from `MMD_3D_ROUTE_PLAN.md`.

Route ID:

```text
route_mmd_3d
```

Use this route when the production requires PMX/VRM/FBX/Blender/MMD-style motion, camera, stage, or render workflows.

Main variants:

```text
pure 3D render
3D base + AI enhancement
3D keyframes + image-to-video
MMD dance
character showcase
```

This is a specialized route, not the project identity. In the global roadmap it is also the canonical detailed plan for Phase 10 when that phase is scheduled.

---

## 15. Phase 10 Canonical Contract

Phase 10 identity:

```text
MMD/3D Specialized Route
```

Status:

```text
P10 planning boundary confirmed with compatibility and repair as core requirements.
Implementation is not authorized until the user explicitly schedules P10.
```

Purpose:

```text
Support model-based 3D/MMD-style productions as one specialized route among many, especially for stable character motion, dance, camera, staging, and 3D reference generation.
```

Primary inputs:

```text
ProductionRecipe
CharacterReferencePack
3D/MMD model assets
motion/camera/stage/audio requirements
Tool registry snapshot
Asset policy snapshot
route constraints
```

Primary outputs:

```text
MMD3DRoutePlan
EnvironmentReadinessReport
ModelCompatibilityReport
MotionCompatibilityReport
CameraAndStagePlan
PreviewRender
FullRender or keyframe exports
AIEnhancementPlan when needed
MMD3DQualityReport
candidate video assets
ToolSetupItems
ReviewItems
```

P10 workstreams:

```text
P10-A 3D Environment Detection
P10-B 3D Asset Registry
P10-C Model/Motion/Camera/Stage Metadata Extraction
P10-D Compatibility, Readiness Check, and Repair Planning
P10-E Automatic Repair Attempts and Verified Combo System
P10-F Preview Render
P10-G Full Render or Keyframe Export
P10-H AI Enhancement Bridge
P10-I 3D-Specific QA and Retry
P10-J Normal Candidate Handoff to P6/P7
```

P10 must include:

```text
human-readable 3D error explanations
verified model/motion/camera combos
preview before final render
asset provenance
model/motion/camera compatibility and repair reports
automatic repair attempts before fallback to non-3D routes when 3D remains not viable
```

P10 must not include:

```text
treating MMD/3D as the whole Kairove identity
blocking ordinary AI video routes
untracked model or motion usage
pretending retargeting/repair succeeded without preview and QA
silently overwriting original models or repaired derivatives without provenance
publishing without normal QA/package phases
```

P10 acceptance criteria:

```text
can detect Blender/FFmpeg/plugin readiness
can register model/motion/camera/stage assets
can write compatibility and repair reports
can identify and attempt repair for common import, texture, bone, morph, physics, clipping, and camera issues
can create repaired derivative records and verified combo records
can produce preview render or explain why not
can hand rendered output/keyframes into normal candidate pipeline
can run 3D-specific QA
can create user tasks for missing setup or incompatible assets
```

P10 confirmation checklist:

```text
first supported 3D toolchain
first model formats
first motion formats
preview render resolution/fps
where user stores official/local models
whether AI enhancement is allowed by default
whether repaired derivatives should be kept forever or garbage-collected
which local 3D repair tools are installed
what counts as a verified combo
```

---

## Cross-Phase Policy Alignment - 2026-06-06

P10 toolchain policy:

```text
No single required toolchain.
Design as compatibility layer.
Long-term support should include MMD, Blender, PMX, VMD, VRM.
Unity and other tools can be added when useful.
```

P10 compatibility and repair flow:

```text
3D compatibility, skeleton, morph, physics, clipping, material, texture, camera, scale, and render issues must enter:
  detect
  repair attempt
  preview
  QA
```

P10 remains one specialized route and must not become the whole Kairove identity.
