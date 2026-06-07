# Kairove MMD / 3D Route Plan

## 0. Purpose

This document defines Kairove's future MMD / VRM / 3D production route.

MMD / 3D is not the core identity of Kairove. It is one specialized production route among many. It should be integrated into the same system:

```text
trend -> format -> semantic transfer -> route selection -> assets -> generation/render -> QA -> retry -> package -> publish -> learn
```

This route is difficult because it involves model compatibility, motion data, rigging, rendering, camera, physics, and AI post-processing.

---

## 1. Route ID

```text
route_mmd_3d_assisted_video
```

Human name:

```text
MMD / VRM / 3D 辅助视频线
```

---

## 2. When to Use This Route

Use when the format requires:

- stable character identity;
- dance or repeatable motion;
- 3D model-based character video;
- predictable camera;
- model showcase;
- character performance where AI video alone is unstable;
- using MMD/VRM assets the user prepared;
- base render for AI enhancement.

Do not use first when:

- simple meme edit is enough;
- pure image-to-video can solve it;
- 3D assets are missing;
- motion is too hard to retarget;
- user has not approved model/asset usage.

---

## 3. Supported Asset Types

Future support:

```text
Models:
  PMX / PMD / VRM / FBX / GLB / GLTF

Motion:
  VMD / BVH / FBX / motion capture

Camera:
  VMD / JSON / generated camera plan

Stage:
  blend / FBX / GLB / image background

Audio:
  music / voice / sfx
```

First practical target:

```text
PMX + VMD + Blender/MMD Tools + vertical render
```

Do not try to support every format at once.

---

## 4. 3D Council

Agents:

- `ModelAssetInspector`
- `MotionAssetInspector`
- `RigCompatibilityAgent`
- `CameraPlanAgent`
- `StagePlanAgent`
- `RenderFeasibilityAgent`
- `MMDRouteAgent`
- `BlenderRouteAgent`
- `AIPostProcessAgent`
- `3DQualityRiskAgent`

Ordered flow:

```text
1. Check if 3D route is needed
2. Inspect model assets
3. Inspect motion assets
4. Check rig/motion compatibility
5. Build camera/stage plan
6. Choose MMD / Blender / hybrid route
7. Render base candidate
8. Optionally AI enhance
9. Run 3D-specific QA
```

---

## 5. Production Variants

### 5.1 Pure 3D Render

```text
model + motion + camera + stage -> render -> edit -> publish
```

### 5.2 3D Base + AI Enhancement

```text
3D render or keyframes -> AI video enhancement -> QC -> edit
```

### 5.3 3D Keyframes + Image-to-Video

```text
render keyframes -> image-to-video per shot -> edit
```

### 5.4 MMD Dance

```text
PMX + VMD dance + music + camera -> vertical dance video
```

### 5.5 Character Showcase

```text
model poses + camera orbit + closeups -> showcase video
```

---

## 6. Technical Risks

Major risks:

- PMX import failure;
- missing textures;
- Japanese/Chinese path encoding;
- VMD motion incompatible with model bones;
- morph/expression mismatch;
- physics instability;
- skirt/hair clipping;
- camera framing bad in vertical ratio;
- Blender plugin version mismatch;
- rendering too slow;
- FFmpeg output failure.

Each risk should produce specific failure tags:

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
```

---

## 7. 3D-Specific QA

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
- audio sync if music/dance.

Agent-assisted checks:

- does the character look correct?
- is the dance/watchability acceptable?
- is camera composition good?
- does AI enhancement damage identity?

---

## 8. Integration with Existing System

MMD/3D route must reuse:

- Asset Resolver;
- Tool Registry;
- Generation Manager;
- Quality Council;
- Retry Engine;
- Packaging Council;
- Publish Council;
- Learning Memory.

It should not become a separate disconnected tool.

---

## 9. First 3D Implementation Boundary

When this route is implemented, first target:

```text
one verified PMX
one verified VMD
one default vertical camera
one short render
one output mp4
first/last frame export
clear error messages
```

Do not start with generic support for all 3D formats.

---

## 10. Acceptance Criteria

3D route is usable when it can:

1. Register 3D assets.
2. Inspect model/motion existence.
3. Check basic compatibility.
4. Render a vertical base video.
5. Export frames.
6. Run technical and visual QA.
7. Save render logs.
8. Feed result into normal Packaging and Publish pipeline.

