from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from .core import (
    append_jsonl,
    connect,
    ensure_dir,
    ensure_project,
    fetch_one,
    job_dir,
    next_id,
    read_json,
    rel,
    root_path,
    sha256_file,
    utc_now,
    write_human_text,
    write_json,
)

PRIMARY_PLATFORMS = ["bilibili", "douyin", "xiaohongshu", "youtube_shorts"]
PLATFORM_STUBS = ["tiktok", "kuaishou", "instagram_reels"]
PLATFORMS = PRIMARY_PLATFORMS
SUPPORTED_INTAKE_MODES = {"text", "url", "local_file", "reference_folder", "manual_format"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm", ".avi"}
REGENT = "kairove_regent"
P0B_SCORE_WEIGHTS = {
    "popularity": 0.2,
    "growth_speed": 0.2,
    "reproduction_clarity": 0.14,
    "production_feasibility": 0.14,
    "asset_availability": 0.1,
    "platform_fit": 0.1,
    "comment_sentiment": 0.08,
    "fatigue_or_overused_risk": -0.12,
}


def _loads(value: str | None, fallback: Any) -> Any:
    if not value:
        return fallback
    return json.loads(value)


def _job_path(root: Path, job_id: str, *parts: str) -> Path:
    return job_dir(root, job_id).joinpath(*parts)


def write_decision(
    root: str | Path,
    run_id: str | None,
    job_id: str | None,
    stage: str,
    decision: str,
    reason: str,
    inputs: dict[str, Any] | None = None,
    actor: str = REGENT,
) -> str:
    base = root_path(root)
    created_at = utc_now()
    with connect(base) as conn:
        decision_id = next_id(conn, "decision")
        row = {
            "decision_id": decision_id,
            "run_id": run_id,
            "job_id": job_id,
            "stage": stage,
            "actor": actor,
            "decision": decision,
            "inputs_json": json.dumps(inputs or {}, ensure_ascii=False),
            "reason": reason,
            "created_at": created_at,
        }
        conn.execute(
            "INSERT INTO decision_logs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            tuple(row.values()),
        )
        conn.commit()
    log_path = _job_path(base, job_id, "decision_log.jsonl") if job_id else base / "logs" / "decision_log.jsonl"
    append_jsonl(log_path, row)
    return decision_id


def create_review_item(
    root: str | Path,
    review_type: str,
    run_id: str | None,
    job_id: str | None,
    summary: str,
    priority: str = "medium",
    blocking: bool = False,
    details_path: str | None = None,
    recommendation: str | None = None,
    options: list[str] | None = None,
) -> str:
    base = root_path(root)
    created_at = utc_now()
    with connect(base) as conn:
        review_id = next_id(conn, "review")
        row = {
            "review_id": review_id,
            "type": review_type,
            "run_id": run_id,
            "job_id": job_id,
            "blocking": 1 if blocking else 0,
            "priority": priority,
            "summary": summary,
            "details_path": details_path,
            "system_recommendation": recommendation,
            "options_json": json.dumps(options or [], ensure_ascii=False),
            "status": "pending",
            "created_at": created_at,
            "resolved_at": None,
            "user_response": None,
        }
        conn.execute(
            "INSERT INTO review_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            tuple(row.values()),
        )
        conn.commit()
    append_jsonl(_job_path(base, job_id, "review_items.jsonl") if job_id else base / "logs" / "review_items.jsonl", row)
    return review_id


def create_tool_setup_item(
    root: str | Path,
    tool_id: str,
    missing: list[str],
    impact: str,
    priority: str = "medium",
    notes: str | None = None,
) -> str:
    base = root_path(root)
    now = utc_now()
    with connect(base) as conn:
        setup_id = next_id(conn, "toolsetup")
        row = {
            "setup_id": setup_id,
            "tool_id": tool_id,
            "missing_json": json.dumps(missing, ensure_ascii=False),
            "impact": impact,
            "user_action_required": 1,
            "priority": priority,
            "status": "open",
            "test_steps_json": json.dumps(["configure tool", "run p0b-demo again", "confirm output manifest"], ensure_ascii=False),
            "notes": notes,
            "created_at": now,
            "updated_at": now,
        }
        conn.execute("INSERT INTO tool_setup_items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(row.values()))
        conn.commit()
    append_jsonl(base / "reports" / "implementation_logs" / "tool_setup_items.jsonl", row)
    return setup_id


def create_run(root: str | Path, input_summary: str, run_type: str = "production", trigger_type: str = "manual") -> str:
    base = ensure_project(root)
    started_at = utc_now()
    with connect(base) as conn:
        run_id = next_id(conn, "run")
        conn.execute(
            "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (run_id, run_type, trigger_type, input_summary, "created", started_at, None, "user", "P0-B chain"),
        )
        conn.commit()
    ensure_dir(base / "runs" / run_id)
    write_json(base / "runs" / run_id / "run.json", {"run_id": run_id, "input_summary": input_summary, "status": "created", "started_at": started_at})
    write_decision(base, run_id, None, "run", "create_run", "Manual trigger accepted for P0-B chain.")
    return run_id


def create_job(
    root: str | Path,
    run_id: str,
    title: str,
    job_type: str = "ordinary_ai_format_video",
    target_platforms: list[str] | None = None,
) -> str:
    base = root_path(root)
    platforms = target_platforms or PLATFORMS
    now = utc_now()
    with connect(base) as conn:
        job_id = next_id(conn, "job")
        directory = _job_path(base, job_id)
        conn.execute(
            "INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (job_id, run_id, job_type, title, "created", "normal", json.dumps(platforms), rel(base, directory), None, now, now, None),
        )
        conn.commit()
    for part in ["sources", "planning", "prompts", "generation", "candidates", "quality", "publish", "reports", "manual_slots"]:
        ensure_dir(_job_path(base, job_id, part))
    write_json(_job_path(base, job_id, "job_config.json"), {"job_id": job_id, "run_id": run_id, "job_type": job_type, "title_working": title, "target_platforms": platforms, "created_at": now})
    write_decision(base, run_id, job_id, "job", "create_job", "Created P0-B ordinary AI video job.", {"target_platforms": platforms})
    return job_id


def _policy_for_source(source_type: str) -> tuple[str, str]:
    if source_type in {"official", "user_provided", "generated"}:
        return "direct_use", "not_required"
    if source_type in {"personal_creator", "unknown"}:
        return "reference_only", "pending"
    return "style_analysis_only", "pending"


def intake_manual_source(
    root: str | Path,
    run_id: str,
    job_id: str,
    mode: str,
    value: str,
    title: str = "Manual seed",
    source_type: str = "unknown",
    content_type: str = "text",
    author: str = "user",
    provenance: dict[str, Any] | None = None,
) -> str:
    base = root_path(root)
    if mode not in SUPPORTED_INTAKE_MODES:
        raise ValueError(f"unsupported P0-B intake mode: {mode}")
    usage_policy, review_status = _policy_for_source(source_type)
    now = utc_now()
    platform = "manual"
    url = value if mode == "url" else None
    local_path = value if mode in {"local_file", "reference_folder"} else None
    provenance_data = {
        "source_url": url,
        "local_path": local_path,
        "work_title": title,
        "character_or_asset_name": provenance.get("character_or_asset_name") if provenance else None,
        "official_owner_or_account": provenance.get("official_owner_or_account") if provenance else (author if source_type == "official" else None),
        "usage": provenance.get("usage") if provenance else "format_reference",
        "download_or_record_date": now,
        "linked_job": job_id,
        "usage_mode": provenance.get("usage_mode") if provenance else ("direct_use" if usage_policy == "direct_use" else "reference"),
    }
    with connect(base) as conn:
        candidate_source_id = next_id(conn, "sourcecand")
        source_id = next_id(conn, "source")
        manifest_path = base / "research_assets" / "manifests" / f"{source_id}.json"
        conn.execute(
            "INSERT INTO source_candidates VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (candidate_source_id, run_id, platform, url, title, author, content_type, "{}", json.dumps({"mode": mode, "manual_value": value}, ensure_ascii=False), "accepted", now),
        )
        conn.execute(
            "INSERT INTO sources VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (source_id, candidate_source_id, run_id, platform, url, source_type, content_type, usage_policy, review_status, "manifest_only", rel(base, manifest_path), None, now, now),
        )
        conn.commit()
    manifest = {
        "source_id": source_id,
        "candidate_source_id": candidate_source_id,
        "run_id": run_id,
        "job_id": job_id,
        "mode": mode,
        "value": value,
        "title": title,
        "author": author,
        "source_type": source_type,
        "content_type": content_type,
        "provenance": provenance_data,
        "usage_policy": usage_policy,
        "review_status": review_status,
        "used_for": ["format observation", "semantic transfer brief", "prompt package"],
        "created_at": now,
    }
    write_json(manifest_path, manifest)
    write_json(_job_path(base, job_id, "sources", "source_refs.json"), {"primary_source": manifest})
    if review_status == "pending":
        create_review_item(base, "source_usage", run_id, job_id, f"Source {source_id} needs user review before direct use.", details_path=rel(base, manifest_path), recommendation="Prefer official/substitute assets first; use this source only as reference/style analysis until approved.", options=["approve direct use", "reference only", "find official substitute", "reject"])
    write_decision(base, run_id, job_id, "source_intake", "accept_manual_source", "Manual seed/source registered for P0-B.", {"source_id": source_id, "usage_policy": usage_policy, "review_status": review_status})
    return source_id

def build_planning_artifacts(
    root: str | Path,
    run_id: str,
    job_id: str,
    source_id: str,
    job_goal: str,
    target_style: str = "ordinary AI format adaptation",
) -> dict[str, str]:
    base = root_path(root)
    planning_dir = _job_path(base, job_id, "planning")
    with connect(base) as conn:
        source = fetch_one(conn, "sources", "source_id", source_id)
    source_manifest = read_json(base / source["manifest_path"])
    score_profile = read_json(base / "config" / "score_profiles" / "trend_video_v1.json")
    score_weights = score_profile.get("weights", {})
    if not set(P0B_SCORE_WEIGHTS).issubset(score_weights):
        score_weights = P0B_SCORE_WEIGHTS
    review_pending = source_manifest["review_status"] == "pending"
    format_observation = {
        "format_label": "p0b_text_seed_format_transfer",
        "source_id": source_id,
        "job_id": job_id,
        "source_summary": source_manifest.get("value", ""),
        "core_hook": "Manual P0-B placeholder: identify the audience-recognizable hook from the text seed/source.",
        "scene_structure": ["opening recognition beat", "format-function development", "payoff or reversal beat"],
        "character_roles": ["source role function", "target substituted role function"],
        "audio_role": "Manual/local/official audio may be attached later; no automatic music/SFX selection in P0-B.",
        "text_or_subtitle_role": "Keep readable copy/subtitle intent if the format depends on text.",
        "visual_style_notes": "Ordinary AI video adaptation; not MMD/3D or longform in P0-B.",
        "estimated_duration_policy": "fit_format",
        "why_this_can_be_reproduced": "P0-B only needs enough structure to create a prompt/manual slot and traceable candidate.",
        "known_uncertainties": ["No autonomous trend proof in P0-B", "No full Format Miner confidence", "Human should review subjective mapping"],
        "created_at": utc_now(),
    }
    scores = {
        "popularity": 0.5,
        "growth_speed": 0.5,
        "reproduction_clarity": 0.55,
        "production_feasibility": 0.6,
        "asset_availability": 0.45,
        "platform_fit": 0.5,
        "comment_sentiment": 0.5,
        "fatigue_or_overused_risk": 0.2 if review_pending else 0.15,
    }
    weighted_total = round(sum(scores[key] * score_weights.get(key, 0.0) for key in scores), 4)
    score_stub = {
        "score_profile": "trend_video_v1",
        "score_profile_version": score_profile.get("version"),
        "visible_weights": score_weights,
        "scores": scores,
        "weighted_total": weighted_total,
        "dimensions": list(scores),
        "adjustable_by_config_or_ui_later": True,
        "major_weight_changes_require_user_approval": True,
        "fatigue_policy": "Fatigue is not volume-only; later phases consider comments, recent growth, and interaction quality.",
    }
    semantic_md = f"""# 语义迁移简报 / Semantic Transfer Brief\n\n- Job: `{job_id}`\n- Source: `{source_id}`\n- 目标: {job_goal}\n- 目标风格: {target_style}\n\n## 必须保留的格式功能\n\n- 保留核心笑点、爽点、恐怖点或情绪曲线。\n- 保留角色关系功能、节奏、反转机制和观众识别点。\n- 保留平台原生的节奏感，但不把时长锁死成固定数字。\n\n## P0-B 允许改变的部分\n\n- 角色、世界观、画风、具体台词和场景细节都可以换。\n- 当前输出只要求链路完整、人工能接着做，不要求已经接近可发布或爆款。\n\n## 素材和审核\n\n- 不直接使用个人画师或未知素材，除非用户审核通过。\n- 来源政策不确定时，优先寻找官方素材或替代素材。\n- 官方、本地、生成素材都必须按来源和用途记录。\n\n## P0-B 限制\n\n这是一份可见的生产骨架。Format Miner、Trend Analyst、Script Council、Asset Resolver、Route Planner 和多层 QA 会在后续阶段扩展它。\n"""
    asset_report = {
        "job_id": job_id,
        "source_id": source_id,
        "required_assets": [
            {"slot": "main_video_candidate", "type": "video", "provider": "manual_generation_slot", "required": True},
            {"slot": "reference_material", "type": source_manifest["content_type"], "provider": "registered_source", "required": True},
            {"slot": "music_or_sfx", "type": "audio", "provider": "local_or_manual", "required": False},
            {"slot": "cover_material", "type": "image", "provider": "generated_or_frame_capture_later", "required": False},
        ],
        "optional_assets": ["official music/SFX with platform-risk note", "cover frame or generated cover"],
        "available_assets": [source_manifest["source_id"]],
        "missing_assets": ["generated video candidate"],
        "searchable_assets": ["official/substitute visual reference", "official music/SFX"],
        "needs_user_provided_assets": ["manual generated video candidate"],
        "policy_review_needed": review_pending,
        "user_needed_when_missing": ["generation tool/account", "local voice/music asset", "official display asset if required"],
    }
    recipe = {
        "job_id": job_id,
        "route": "ordinary_ai_format_video/manual_generation_slot",
        "steps": [
            "understand source format",
            "write semantic transfer brief",
            "prepare prompt package",
            "user or external tool generates candidate",
            "register candidate",
            "run basic QA",
            "build manual publish package",
        ],
        "non_goals": ["autonomous crawling", "auto publishing", "MMD/3D", "longform"],
    }
    route_plan = {
        "job_id": job_id,
        "selected_route": "manual_generation_slot",
        "reason": "P0-B must close a complete chain without requiring a configured paid generation API.",
        "fallback_routes": ["configured_ai_video_generation_api_later", "local_generation_tool_later"],
        "requires_user_action": True,
    }
    files = {
        "format_observation": planning_dir / "format_observation.json",
        "score_stub": planning_dir / "score_stub.json",
        "semantic_transfer_brief": planning_dir / "semantic_transfer_brief.md",
        "asset_requirement_report": planning_dir / "asset_requirement_report.json",
        "production_recipe_draft": planning_dir / "production_recipe_draft.json",
        "route_plan": planning_dir / "route_plan.json",
    }
    write_json(files["format_observation"], format_observation)
    write_json(files["score_stub"], score_stub)
    files["semantic_transfer_brief"].write_text(semantic_md, encoding="utf-8")
    write_json(files["asset_requirement_report"], asset_report)
    write_json(files["production_recipe_draft"], recipe)
    write_json(files["route_plan"], route_plan)
    write_decision(base, run_id, job_id, "planning", "build_p0b_planning_artifacts", "Created visible planning scaffold for P0-B.", {"source_id": source_id})
    return {name: rel(base, path) for name, path in files.items()}


def _load_job_config(root: Path, job_id: str) -> dict[str, Any]:
    return read_json(_job_path(root, job_id, "job_config.json"))


def build_manual_generation_slot(root: str | Path, run_id: str, job_id: str) -> dict[str, str]:
    base = root_path(root)
    job_config = _load_job_config(base, job_id)
    planning_dir = _job_path(base, job_id, "planning")
    prompt_dir = _job_path(base, job_id, "prompts", "prompt_package_000001")
    slot_dir = _job_path(base, job_id, "manual_slots", "manual_slot_000001")
    ensure_dir(prompt_dir)
    ensure_dir(slot_dir / "inbox")
    source_refs = read_json(_job_path(base, job_id, "sources", "source_refs.json"))
    semantic_brief = (planning_dir / "semantic_transfer_brief.md").read_text(encoding="utf-8")
    positive_prompt = f"""# 中文说明\n\n为 `{job_config['title_working']}` 生成一个普通 AI 短视频候选。当前是 P0-B 手动生成槽，只要求链路完整、可追踪、人工能继续处理，不要求成片已经接近发布或爆款。\n\n必须保留：格式功能、观众识别点、核心笑点/爽点/情绪曲线、关系功能、节奏和反转机制。\n\n可以改变：角色、世界观、画风、具体台词和场景。\n\n# English Generation Prompt\n\nCreate one ordinary AI short-video candidate for: {job_config['title_working']}.\n\nPreserve the recognizable format function, audience recognition point, core joke/payoff/emotion curve, relationship function, rhythm, and reversal mechanism. Change the concrete characters, world setting, visual style, exact lines, and scene details as needed. The output should be traceable and suitable for human continuation; viral quality is not required for this P0-B test.\n\n# Source / Semantic Notes\n\n{semantic_brief}\n"""
    negative_prompt = "Avoid unreadable text, broken anatomy, duplicated faces, flicker, accidental watermark-like marks, direct personal-creator asset copying, and platform-hostile pacing."
    tool_parameters = {
        "generation_mode": "manual_generation_slot",
        "duration_policy": "fit_format",
        "aspect_ratio": "platform dependent; user/tool may choose",
        "candidate_count": 1,
        "platforms": job_config["target_platforms"],
        "language_policy": "Chinese explanation plus English generation prompt by default.",
    }
    context = {
        "prompt_package_id": "prompt_package_000001",
        "job_id": job_id,
        "run_id": run_id,
        "source_refs": source_refs,
        "planning_files": {
            "semantic_transfer_brief": rel(base, planning_dir / "semantic_transfer_brief.md"),
            "route_plan": rel(base, planning_dir / "route_plan.json"),
        },
        "expected_output": {
            "type": "video",
            "place_file_in": rel(base, slot_dir / "inbox"),
            "or_import_with_cli": "python -m kairove --root <root> import-candidate --job-id <job_id> --file <video>",
        },
        "next_quality_checks": ["file exists", "size > 0", "supported video extension", "basic semantic review scaffold"],
    }
    (prompt_dir / "positive_prompt.txt").write_text(positive_prompt, encoding="utf-8")
    (prompt_dir / "negative_prompt.txt").write_text(negative_prompt, encoding="utf-8")
    write_json(prompt_dir / "tool_parameters.json", tool_parameters)
    write_json(prompt_dir / "prompt_context.json", context)
    write_json(prompt_dir / "source_links.json", source_refs)
    (prompt_dir / "human_summary.md").write_text(f"# 手动生成槽说明 / Manual Generation Slot\n\n用这个 prompt package 为 `{job_id}` 生成一个视频候选。\n\n- Prompt package: `prompt_package_000001`\n- 输入来源: `{source_refs['primary_source']['source_id']}`\n- 生成后，把视频放进 `{rel(base, slot_dir / 'inbox')}`，或者用 CLI import。\n- 下一步检查: 文件存在、非空、视频扩展名可接受、基础语义 QA 骨架。\n\nP0-B 不假装自动生成 API 已经配置好；这里是诚实的 manual slot。\n", encoding="utf-8")
    slot_manifest = {
        "slot_id": "manual_slot_000001",
        "job_id": job_id,
        "generation_step_type": "manual_generation_slot",
        "status": "waiting_for_candidate",
        "prompt_package": rel(base, prompt_dir),
        "input_assets": [source_refs["primary_source"]],
        "positive_prompt": rel(base, prompt_dir / "positive_prompt.txt"),
        "negative_prompt": rel(base, prompt_dir / "negative_prompt.txt"),
        "parameters": rel(base, prompt_dir / "tool_parameters.json"),
        "expected_output_type": "video",
        "quality_checks_after_import": context["next_quality_checks"],
        "inbox": rel(base, slot_dir / "inbox"),
        "created_at": utc_now(),
    }
    write_json(slot_dir / "slot_manifest.json", slot_manifest)
    write_json(_job_path(base, job_id, "generation", "manual_generation_slot.json"), slot_manifest)
    with connect(base) as conn:
        step_id = next_id(conn, "genstep")
        conn.execute(
            "INSERT INTO generation_steps VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (step_id, job_id, None, "manual_generation_slot", "manual_generation_slot", json.dumps([source_refs], ensure_ascii=False), "[]", rel(base, prompt_dir), json.dumps(tool_parameters, ensure_ascii=False), "pending", None, utc_now(), None),
        )
        conn.commit()
    append_jsonl(_job_path(base, job_id, "generation", "generation_steps.jsonl"), {"step_id": step_id, "status": "pending", "tool_id": "manual_generation_slot"})
    tools = read_json(base / "config" / "tools.json").get("tools", {})
    if tools.get("ai_video_generation_api", {}).get("status") != "available":
        create_tool_setup_item(base, "ai_video_generation_api", ["provider/account/API or local tool binding"], "Automatic generation is unavailable, so P0-B uses a manual generation slot.", priority="high")
    write_decision(base, run_id, job_id, "generation", "open_manual_generation_slot", "Manual slot created because P0-B must work before generation APIs are configured.", {"step_id": step_id})
    return {"step_id": step_id, "prompt_package": rel(base, prompt_dir), "manual_slot": rel(base, slot_dir)}

def import_candidate(root: str | Path, job_id: str, candidate_file: str | Path, run_id: str | None = None, fixture: bool = False) -> str:
    base = root_path(root)
    src = Path(candidate_file).expanduser().resolve()
    if not src.exists() or not src.is_file():
        raise FileNotFoundError(f"candidate file not found: {src}")
    with connect(base) as conn:
        candidate_id = next_id(conn, "candidate")
        asset_id = next_id(conn, "asset")
    candidate_dir = _job_path(base, job_id, "candidates", candidate_id)
    ensure_dir(candidate_dir)
    dest = candidate_dir / f"video{src.suffix.lower() or '.mp4'}"
    shutil.copy2(src, dest)
    file_hash = sha256_file(dest)
    now = utc_now()
    asset_manifest = {
        "asset_id": asset_id,
        "candidate_id": candidate_id,
        "job_id": job_id,
        "asset_class": "generated",
        "asset_type": "video",
        "storage_path": rel(base, dest),
        "hash": file_hash,
        "source_type": "generated" if not fixture else "fixture",
        "usage_policy": "direct_use",
        "review_status": "not_required",
        "metadata": {"imported_from": str(src), "fixture": fixture, "size_bytes": dest.stat().st_size},
        "created_at": now,
    }
    source_refs_path = _job_path(base, job_id, "sources", "source_refs.json")
    source_refs = read_json(source_refs_path) if source_refs_path.exists() else {}
    write_json(candidate_dir / "asset_manifest.json", asset_manifest)
    write_json(base / "generated_assets" / "manifests" / f"{asset_id}.json", asset_manifest)
    with connect(base) as conn:
        conn.execute(
            "INSERT INTO assets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (asset_id, "generated", "video", None, job_id, rel(base, dest), file_hash, asset_manifest["source_type"], "direct_use", "not_required", json.dumps(asset_manifest["metadata"], ensure_ascii=False), now, now),
        )
        step = conn.execute(
            "SELECT * FROM generation_steps WHERE job_id = ? AND status = 'pending' ORDER BY started_at DESC LIMIT 1",
            (job_id,),
        ).fetchone()
        if step is None:
            step_id = next_id(conn, "genstep")
            conn.execute(
                "INSERT INTO generation_steps VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (step_id, job_id, candidate_id, "manual_import", "manual_generation_slot", "[]", json.dumps([asset_id]), None, "{}", "succeeded", None, now, now),
            )
        else:
            step_id = step["step_id"]
            conn.execute(
                "UPDATE generation_steps SET candidate_id = ?, output_assets_json = ?, status = 'succeeded', completed_at = ? WHERE step_id = ?",
                (candidate_id, json.dumps([asset_id]), now, step_id),
            )
        conn.execute(
            "INSERT INTO candidates VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (candidate_id, job_id, "video", "imported", rel(base, dest), json.dumps([step_id]), None, None, None, now),
        )
        conn.commit()
    candidate_manifest = {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "status": "imported",
        "output_path": rel(base, dest),
        "generation_steps": [step_id],
        "asset_id": asset_id,
        "prompt_package_id": "prompt_package_000001",
        "prompt_package_path": rel(base, _job_path(base, job_id, "prompts", "prompt_package_000001")),
        "source_chain": source_refs,
        "file_metadata": {
            "hash_sha256": file_hash,
            "size_bytes": dest.stat().st_size,
            "extension": dest.suffix.lower(),
            "fixture": fixture,
        },
        "created_at": now,
    }
    write_json(_job_path(base, job_id, "generation", "candidate_manifest.json"), candidate_manifest)
    write_json(candidate_dir / "candidate_manifest.json", candidate_manifest)
    append_jsonl(_job_path(base, job_id, "generation", "generation_steps.jsonl"), {"step_id": step_id, "candidate_id": candidate_id, "status": "succeeded", "asset_id": asset_id})
    write_decision(base, run_id, job_id, "candidate", "register_candidate", "Generated/imported candidate registered with manifest and hash.", {"candidate_id": candidate_id, "asset_id": asset_id, "fixture": fixture})
    return candidate_id


def run_basic_qa(root: str | Path, job_id: str, candidate_id: str) -> str:
    base = root_path(root)
    with connect(base) as conn:
        candidate = fetch_one(conn, "candidates", "candidate_id", candidate_id)
    output_path = base / candidate["output_path"]
    candidate_manifest_path = _job_path(base, job_id, "candidates", candidate_id, "candidate_manifest.json")
    candidate_manifest = read_json(candidate_manifest_path) if candidate_manifest_path.exists() else {}
    is_fixture = bool(candidate_manifest.get("file_metadata", {}).get("fixture"))
    exists = output_path.exists()
    size = output_path.stat().st_size if exists else 0
    ext = output_path.suffix.lower()
    failure_tags: list[str] = []
    warnings: list[str] = []
    if not exists:
        failure_tags.append("missing_file")
    if size <= 0:
        failure_tags.append("empty_file")
    if ext not in VIDEO_EXTENSIONS:
        failure_tags.append("unsupported_extension")
    if exists and size > 0 and ext in VIDEO_EXTENSIONS:
        warnings.append("container_not_deep_verified_in_p0b")
    if is_fixture:
        warnings.append("test_fixture_not_real_generated_video")
    publish_ready = not failure_tags
    decision = "pass_to_packaging" if publish_ready else "retry_or_user_fix_required"
    score = 0.65 if publish_ready else 0.0
    qa_dir = _job_path(base, job_id, "quality", candidate_id)
    ensure_dir(qa_dir)
    technical_report = {
        "candidate_id": candidate_id,
        "file_exists": exists,
        "size_bytes": size,
        "extension": ext,
        "extension_supported": ext in VIDEO_EXTENSIONS,
        "container_verified": False,
        "resolution": None,
        "fps": None,
        "duration_seconds": None,
        "is_test_fixture": is_fixture,
        "warnings": warnings,
        "failure_tags": failure_tags,
    }
    fixture_note = "\n\n注意：这个 candidate 是测试 fixture，只证明链路能走通，不是真生成视频，不能按真实成片发布。\n" if is_fixture else ""
    semantic_md = f"""# 基础语义 QA / Basic Semantic QA\n\nCandidate: `{candidate_id}`\n{fixture_note}\nP0-B semantic QA 是浅层检查，只确认链路完整、可追踪、人工能接着做。P0-B QA 通过不代表视频接近可发布，也不代表它会成为爆款。\n\nChecklist:\n\n- Candidate file is registered.\n- Candidate links to a generation step and prompt package.\n- Candidate links back to source/provenance chain.\n- Later P5/P6 work will handle deep visual QA, role accuracy, format fidelity, multi-agent judgment, and retry optimization.\n\nDecision: `{decision}`\n"""
    retry_decision = {
        "candidate_id": candidate_id,
        "decision": decision,
        "publish_ready": publish_ready,
        "failure_tags": failure_tags,
        "allowed_values": ["pass_to_packaging", "retry_same_prompt", "revise_prompt", "replace_asset", "switch_route", "ask_user", "abandon_job"],
        "next_action": "build_manual_publish_package" if publish_ready else "ask_user",
    }
    technical_path = qa_dir / "technical_quality_report.json"
    semantic_path = qa_dir / "semantic_quality_report.md"
    write_json(technical_path, technical_report)
    semantic_path.write_text(semantic_md, encoding="utf-8")
    write_json(qa_dir / "failure_tags.json", {"failure_tags": failure_tags})
    write_json(qa_dir / "retry_decision.json", retry_decision)
    with connect(base) as conn:
        quality_report_id = next_id(conn, "quality")
        conn.execute(
            "INSERT INTO quality_reports VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (quality_report_id, candidate_id, job_id, rel(base, technical_path), rel(base, semantic_path), json.dumps(failure_tags), 1 if publish_ready else 0, decision, utc_now()),
        )
        conn.execute(
            "UPDATE candidates SET quality_report_id = ?, score = ?, status = ? WHERE candidate_id = ?",
            (quality_report_id, score, "qa_passed" if publish_ready else "qa_failed", candidate_id),
        )
        conn.commit()
    write_decision(base, None, job_id, "quality", decision, "Basic P0-B QA completed.", {"candidate_id": candidate_id, "quality_report_id": quality_report_id, "failure_tags": failure_tags})
    return quality_report_id

def _legacy_build_manual_publish_package(root: str | Path, job_id: str, candidate_id: str) -> str:
    base = root_path(root)
    with connect(base) as conn:
        candidate = fetch_one(conn, "candidates", "candidate_id", candidate_id)
        job = fetch_one(conn, "jobs", "job_id", job_id)
    output_path = base / candidate["output_path"]
    if not output_path.exists():
        raise FileNotFoundError(f"candidate output not found: {output_path}")
    publish_dir = _job_path(base, job_id, "publish")
    package_dir = publish_dir / "manual_publish_package"
    ensure_dir(package_dir)
    final_video = package_dir / f"final_video{output_path.suffix.lower()}"
    shutil.copy2(output_path, final_video)
    title_working = job["title_working"]
    target_platforms = _loads(job["target_platforms_json"], PLATFORMS)
    title_options = [
        title_working,
        f"{title_working} | AI adaptation",
        f"{title_working} - format transfer test",
    ]
    descriptions = {
        "short": f"AI video format adaptation test for {title_working}.",
        "long": f"This package was prepared by Kairove P0-B. It contains the final candidate, title options, tags, platform payload drafts, and manual publish checklist for {job_id}.",
    }
    tags = ["AI视频", "短视频", "二创", "format-transfer", "Kairove"]
    cover_notes = {
        "cover_strategy": "P0-B placeholder: choose a clear frame or generate a cover later.",
        "must_check": ["text readability", "platform crop", "character/world consistency"],
    }
    payloads: dict[str, Any] = {}
    for platform in target_platforms:
        payloads[platform] = {
            "platform": platform,
            "status": "ready_manual",
            "title": title_options[0],
            "description": descriptions["short"],
            "tags": tags,
            "video_path": rel(base, final_video),
            "cover_notes": cover_notes,
            "upload_mode": "manual_package_only",
        }
        write_json(publish_dir / f"payload_{platform}.json", payloads[platform])
    readiness_report = {
        "job_id": job_id,
        "candidate_id": candidate_id,
        "status": "manual_ready",
        "auto_upload": False,
        "platforms": target_platforms,
        "checks": {
            "candidate_file_exists": True,
            "qa_report_present": bool(candidate["quality_report_id"]),
            "metadata_present": True,
            "cover_finalized": False,
        },
        "manual_before_publish": ["watch final video", "choose title", "choose cover", "review platform payload", "upload manually"],
        "created_at": utc_now(),
    }
    write_json(publish_dir / "title_options.json", {"title_options": title_options})
    write_json(publish_dir / "selected_title.json", {"title": title_options[0], "selected_by": "system_default"})
    write_json(publish_dir / "description.json", descriptions)
    write_json(publish_dir / "tags.json", {"tags": tags})
    write_json(publish_dir / "cover_notes.json", cover_notes)
    write_json(publish_dir / "platform_payloads.json", payloads)
    write_json(publish_dir / "readiness_report.json", readiness_report)
    write_json(package_dir / "manifest.json", {"job_id": job_id, "candidate_id": candidate_id, "final_video": rel(base, final_video), "payloads": rel(base, publish_dir / "platform_payloads.json"), "readiness_report": rel(base, publish_dir / "readiness_report.json")})
    now = utc_now()
    with connect(base) as conn:
        package_id = next_id(conn, "publishpkg")
        conn.execute(
            "INSERT INTO publish_packages VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (package_id, job_id, rel(base, final_video), "[]", rel(base, publish_dir / "platform_payloads.json"), rel(base, publish_dir / "readiness_report.json"), "manual_ready", now),
        )
        for platform in target_platforms:
            record_id = next_id(conn, "publishrec")
            conn.execute(
                "INSERT INTO publish_records VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (record_id, job_id, platform, "manual", "package_ready", None, None, rel(base, publish_dir / f"payload_{platform}.json"), None, now, now),
            )
        conn.execute("UPDATE jobs SET status = ?, updated_at = ? WHERE job_id = ?", ("packaged", now, job_id))
        conn.commit()
    write_decision(base, None, job_id, "publish", "build_manual_publish_package", "Built all-platform manual publish package; auto upload remains disabled in P0-B.", {"publish_package_id": package_id, "platforms": target_platforms})
    return package_id


def build_manual_publish_package(root: str | Path, job_id: str, candidate_id: str) -> str:
    base = root_path(root)
    with connect(base) as conn:
        candidate = fetch_one(conn, "candidates", "candidate_id", candidate_id)
        job = fetch_one(conn, "jobs", "job_id", job_id)

    output_path = base / candidate["output_path"]
    if not output_path.exists():
        raise FileNotFoundError(f"candidate output not found: {output_path}")
    if not candidate["quality_report_id"]:
        raise ValueError(f"candidate {candidate_id} has no QA report; P0-B packaging is blocked")
    with connect(base) as conn:
        quality_report = fetch_one(conn, "quality_reports", "quality_report_id", candidate["quality_report_id"])
    if not quality_report["publish_ready"]:
        raise ValueError(f"candidate {candidate_id} did not pass QA; P0-B packaging is blocked")

    publish_dir = _job_path(base, job_id, "publish")
    package_dir = publish_dir / "manual_publish_package"
    ensure_dir(package_dir)
    for part in ["cover", "titles", "descriptions", "tags", "platform_payloads"]:
        ensure_dir(package_dir / part)

    final_video = package_dir / f"final_video{output_path.suffix.lower()}"
    shutil.copy2(output_path, final_video)

    title_working = job["title_working"]
    target_platforms = _loads(job["target_platforms_json"], PLATFORMS)
    primary_platforms = [platform for platform in target_platforms if platform in PRIMARY_PLATFORMS]
    if not primary_platforms:
        primary_platforms = list(PRIMARY_PLATFORMS)
    stub_platforms = [platform for platform in PLATFORM_STUBS if platform not in primary_platforms]

    title_options = [
        title_working,
        f"{title_working} | AI adaptation",
        f"{title_working} - format transfer test",
    ]
    youtube_auxiliary = {
        "title_en": f"{title_working} | AI format transfer test",
        "description_en": "Manual package prepared by Kairove P0-B. This is a traceable chain test, not an automatic upload.",
        "tags_en": ["AI video", "shorts", "format transfer", "Kairove"],
    }
    descriptions = {
        "short": f"AI video format adaptation test for {title_working}.",
        "long": f"This package was prepared by Kairove P0-B. It contains the final candidate, title options, tags, platform payload drafts, and manual publish checklist for {job_id}.",
        "youtube_shorts_auxiliary_en": youtube_auxiliary["description_en"],
    }
    tags = ["AI-video", "short-video", "format-transfer", "manual-package", "Kairove"]
    cover_notes = {
        "cover_strategy": "P0-B placeholder: choose a clear frame or generate a cover later.",
        "must_check": ["text readability", "platform crop", "character/world consistency"],
    }

    source_refs_path = _job_path(base, job_id, "sources", "source_refs.json")
    candidate_manifest_path = _job_path(base, job_id, "candidates", candidate_id, "candidate_manifest.json")
    candidate_manifest = read_json(candidate_manifest_path) if candidate_manifest_path.exists() else {}
    is_fixture = bool(candidate_manifest.get("file_metadata", {}).get("fixture"))
    provenance_md = "# Source And Asset Provenance\n\n"
    if source_refs_path.exists():
        provenance_md += json.dumps(read_json(source_refs_path), ensure_ascii=False, indent=2)
    provenance_md += f"\n\nCandidate asset: `{candidate['output_path']}`\nQA report: `{candidate['quality_report_id']}`\n"

    payloads: dict[str, Any] = {}
    for platform in primary_platforms:
        payloads[platform] = {
            "platform": platform,
            "status": "ready_manual",
            "title": title_options[0],
            "description": descriptions["short"],
            "tags": tags,
            "video_path": rel(base, final_video),
            "cover_notes": cover_notes,
            "upload_mode": "manual_package_only",
        }
        if platform == "youtube_shorts":
            payloads[platform]["auxiliary_metadata_en"] = youtube_auxiliary
        write_json(publish_dir / f"payload_{platform}.json", payloads[platform])
        write_json(package_dir / "platform_payloads" / f"{platform}.json", payloads[platform])

    for platform in stub_platforms:
        payloads[platform] = {
            "platform": platform,
            "status": "blocked_tool_setup",
            "reason": "P0-B platform stub only; full support is not required for P0-B.",
            "upload_mode": "manual_package_stub",
        }
        write_json(publish_dir / f"payload_{platform}.json", payloads[platform])
        write_json(package_dir / "platform_payloads" / f"{platform}.json", payloads[platform])

    readiness_report = {
        "job_id": job_id,
        "candidate_id": candidate_id,
        "status": "manual_package_ready",
        "auto_upload": False,
        "is_test_fixture": is_fixture,
        "real_publish_ready": not is_fixture,
        "p0b_pass_meaning": "chain_complete_traceable_human_continuable",
        "primary_platforms": primary_platforms,
        "platform_stubs": stub_platforms,
        "platforms": primary_platforms + stub_platforms,
        "checks": {
            "candidate_file_exists": True,
            "qa_report_present": bool(candidate["quality_report_id"]),
            "metadata_present": True,
            "cover_finalized": False,
        },
        "manual_before_publish": ["watch final video", "choose title", "choose cover", "review platform payload", "upload manually"],
        "created_at": utc_now(),
    }
    review_summary = f"""# P0-B 输出检查摘要\n\nJob: `{job_id}`\nCandidate: `{candidate_id}`\n\n## 当前结论\n\n- P0-B 链路已跑通：文字 seed -> planning -> prompt package -> manual slot -> candidate import -> QA -> manual publish package。\n- 这是 manual package，不会自动发布。\n- 主平台 payload 已准备：Bilibili、Douyin、Xiaohongshu、YouTube Shorts。\n- TikTok、Kuaishou、Instagram Reels 只是 P0-B stub，状态应为 blocked/tool setup。\n\n## 重要提醒\n\n- `final_video.mp4` 是测试 fixture: `{is_fixture}`。\n- 如果 `is_test_fixture` 为 true，它不能当真实生成视频发布，只证明链路能管理视频文件。\n- `cover_finalized` 仍为 false，发布前需要人工选封面或后续生成封面。\n- P0-B QA 通过只代表链路完整、记录完整、人工能继续，不代表成片质量达标。\n\n## 你最该先看的文件\n\n- `manifest.json`\n- `platform_payloads/platform_payloads.json`\n- `source_and_asset_provenance.md`\n- `titles/selected_title.txt`\n- `cover/cover_notes.md`\n"""

    write_json(publish_dir / "title_options.json", {"title_options": title_options})
    write_json(publish_dir / "selected_title.json", {"title": title_options[0], "selected_by": "system_default"})
    write_json(publish_dir / "description.json", descriptions)
    write_json(publish_dir / "tags.json", {"tags": tags})
    write_json(publish_dir / "cover_notes.json", cover_notes)
    write_json(publish_dir / "platform_payloads.json", payloads)
    write_json(publish_dir / "readiness_report.json", readiness_report)

    write_json(package_dir / "titles" / "title_options.json", {"title_options": title_options, "youtube_shorts_auxiliary": youtube_auxiliary})
    write_human_text(package_dir / "titles" / "selected_title.txt", title_options[0] + "\n")
    write_json(package_dir / "descriptions" / "description.json", descriptions)
    write_json(package_dir / "tags" / "tags.json", {"tags": tags})
    write_json(package_dir / "cover" / "cover_notes.json", cover_notes)
    write_human_text(package_dir / "cover" / "cover_notes.md", "# Cover Notes\n\n- Choose a clear frame or generate a cover later.\n- Check text readability, platform crop, and character/world consistency.\n")
    write_json(package_dir / "platform_payloads" / "platform_payloads.json", payloads)
    write_human_text(package_dir / "source_and_asset_provenance.md", provenance_md)
    write_human_text(package_dir / "review_summary.md", review_summary)
    write_json(package_dir / "publish_record_placeholder.json", {"job_id": job_id, "candidate_id": candidate_id, "status": "not_uploaded", "auto_publish": False})
    write_json(package_dir / "manifest.json", {"job_id": job_id, "candidate_id": candidate_id, "final_video": rel(base, final_video), "payloads": rel(base, package_dir / "platform_payloads" / "platform_payloads.json"), "readiness_report": rel(base, publish_dir / "readiness_report.json"), "auto_publish": False})

    now = utc_now()
    with connect(base) as conn:
        package_id = next_id(conn, "publishpkg")
        conn.execute(
            "INSERT INTO publish_packages VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (package_id, job_id, rel(base, final_video), "[]", rel(base, package_dir / "platform_payloads" / "platform_payloads.json"), rel(base, publish_dir / "readiness_report.json"), "manual_ready", now),
        )
        for platform in primary_platforms + stub_platforms:
            record_id = next_id(conn, "publishrec")
            record_status = "package_ready" if platform in primary_platforms else "stub_blocked"
            conn.execute(
                "INSERT INTO publish_records VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (record_id, job_id, platform, "manual", record_status, None, None, rel(base, publish_dir / f"payload_{platform}.json"), None, now, now),
            )
        conn.execute("UPDATE jobs SET status = ?, updated_at = ? WHERE job_id = ?", ("packaged", now, job_id))
        conn.commit()

    write_decision(base, None, job_id, "publish", "build_manual_publish_package", "Built manual publish package for primary platforms and explicit stubs; auto upload remains disabled in P0-B.", {"publish_package_id": package_id, "primary_platforms": primary_platforms, "platform_stubs": stub_platforms})
    run_p0b_self_check(base, job_id, candidate_id)
    return package_id


def _check_json_file(path: Path) -> tuple[bool, str | None]:
    try:
        read_json(path)
    except Exception as exc:  # noqa: BLE001 - report exact parse/open failure in self-check.
        return False, str(exc)
    return True, None


def run_p0b_self_check(root: str | Path, job_id: str, candidate_id: str) -> dict[str, Any]:
    base = root_path(root)
    job_root = _job_path(base, job_id)
    package_dir = job_root / "publish" / "manual_publish_package"
    quality_dir = job_root / "quality" / candidate_id
    required_files = {
        "job_config": job_root / "job_config.json",
        "source_refs": job_root / "sources" / "source_refs.json",
        "format_observation": job_root / "planning" / "format_observation.json",
        "score_stub": job_root / "planning" / "score_stub.json",
        "semantic_transfer_brief": job_root / "planning" / "semantic_transfer_brief.md",
        "asset_requirement_report": job_root / "planning" / "asset_requirement_report.json",
        "route_plan": job_root / "planning" / "route_plan.json",
        "positive_prompt": job_root / "prompts" / "prompt_package_000001" / "positive_prompt.txt",
        "manual_slot": job_root / "manual_slots" / "manual_slot_000001" / "slot_manifest.json",
        "candidate_manifest": job_root / "candidates" / candidate_id / "candidate_manifest.json",
        "technical_qa": quality_dir / "technical_quality_report.json",
        "semantic_qa": quality_dir / "semantic_quality_report.md",
        "retry_decision": quality_dir / "retry_decision.json",
        "readiness_report": job_root / "publish" / "readiness_report.json",
        "platform_payloads": job_root / "publish" / "platform_payloads.json",
        "manual_package_manifest": package_dir / "manifest.json",
        "review_summary": package_dir / "review_summary.md",
        "provenance_summary": package_dir / "source_and_asset_provenance.md",
        "final_video": package_dir / "final_video.mp4",
    }

    checks: list[dict[str, Any]] = []
    for name, path in required_files.items():
        item = {
            "name": name,
            "path": rel(base, path),
            "exists": path.exists(),
            "ok": path.exists(),
            "message": "exists" if path.exists() else "missing",
        }
        if path.suffix == ".json" and path.exists():
            ok, error = _check_json_file(path)
            item["ok"] = ok
            item["message"] = "json_ok" if ok else f"json_error: {error}"
        checks.append(item)

    readiness_path = job_root / "publish" / "readiness_report.json"
    readiness = read_json(readiness_path) if readiness_path.exists() else {}
    payloads_path = job_root / "publish" / "platform_payloads.json"
    payloads = read_json(payloads_path) if payloads_path.exists() else {}
    technical_path = quality_dir / "technical_quality_report.json"
    technical = read_json(technical_path) if technical_path.exists() else {}

    policy_checks = [
        {
            "name": "auto_publish_disabled",
            "ok": readiness.get("auto_upload") is False,
            "message": "auto_upload must remain false in P0-B",
        },
        {
            "name": "fixture_not_real_publish_ready",
            "ok": not readiness.get("is_test_fixture") or readiness.get("real_publish_ready") is False,
            "message": "test fixtures must not be marked as real publish-ready",
        },
        {
            "name": "primary_platforms_ready_manual",
            "ok": all(payloads.get(platform, {}).get("status") == "ready_manual" for platform in PRIMARY_PLATFORMS),
            "message": "P0-B primary platforms should be ready_manual",
        },
        {
            "name": "stub_platforms_blocked",
            "ok": all(payloads.get(platform, {}).get("status") == "blocked_tool_setup" for platform in PLATFORM_STUBS),
            "message": "P0-B stub platforms should be blocked_tool_setup",
        },
        {
            "name": "fixture_warning_present",
            "ok": not technical.get("is_test_fixture") or "test_fixture_not_real_generated_video" in technical.get("warnings", []),
            "message": "fixture candidates must carry an explicit warning",
        },
    ]
    checks.extend(policy_checks)

    failed = [item for item in checks if not item["ok"]]
    status = "pass" if not failed else "fail"
    report = {
        "job_id": job_id,
        "candidate_id": candidate_id,
        "status": status,
        "failed_count": len(failed),
        "checked_at": utc_now(),
        "checks": checks,
        "human_first_files": [
            rel(base, package_dir / "review_summary.md"),
            rel(base, package_dir / "manifest.json"),
            rel(base, package_dir / "platform_payloads" / "platform_payloads.json"),
            rel(base, package_dir / "source_and_asset_provenance.md"),
            rel(base, job_root / "planning" / "semantic_transfer_brief.md"),
        ],
    }

    report_path = job_root / "reports" / "self_check_report.json"
    md_path = job_root / "reports" / "self_check_report.md"
    package_md_path = package_dir / "self_check_report.md"
    write_json(report_path, report)

    failed_lines = "\n".join(f"- `{item['name']}`: {item['message']} ({item.get('path', '')})" for item in failed) or "- None"
    md = f"""# P0-B Self-Check Report\n\nJob: `{job_id}`\nCandidate: `{candidate_id}`\nStatus: `{status}`\nFailed checks: `{len(failed)}`\n\n## Human First Files\n\n- `manual_publish_package/review_summary.md`\n- `manual_publish_package/manifest.json`\n- `manual_publish_package/platform_payloads/platform_payloads.json`\n- `manual_publish_package/source_and_asset_provenance.md`\n- `planning/semantic_transfer_brief.md`\n\n## Failed Checks\n\n{failed_lines}\n\n## Meaning\n\nThis self-check only verifies that the P0-B output is complete, traceable, and not misleading. It does not judge real video quality, trend value, or publish performance.\n"""
    write_human_text(md_path, md)
    write_human_text(package_md_path, md)
    write_decision(base, None, job_id, "self_check", f"p0b_self_check_{status}", "Self-check report written after P0-B output generation.", {"failed_count": len(failed)})
    return report


def write_phase0_report(root: str | Path, run_id: str, job_id: str) -> dict[str, str]:
    base = root_path(root)
    phase_dir = base / "reports" / "phase_reports"
    job_report_dir = _job_path(base, job_id, "reports")
    artifact_index = {
        "phase": "P0-B",
        "run_id": run_id,
        "job_id": job_id,
        "chain": [
            "manual source",
            "source manifest",
            "format observation",
            "semantic transfer brief",
            "route plan",
            "asset requirement report",
            "prompt package",
            "manual generation slot",
            "candidate registration",
            "basic QA",
            "manual publish package",
            "self-check report",
        ],
        "job_dir": rel(base, _job_path(base, job_id)),
        "created_at": utc_now(),
    }
    test_report = {
        "status": "implemented_offline_chain",
        "covered": ["sqlite schema", "config bootstrap", "manual source intake", "prompt package", "candidate import", "basic QA", "manual publish package", "self-check report"],
        "not_covered_yet": ["web scouting", "real generation API", "deep media probe", "visual semantic multi-agent QA", "auto publish"],
    }
    gaps_md = """# Known P0-B Gaps\n\n- P0-B has no autonomous web scouting.\n- P0-B uses JSON config equivalents instead of YAML to remain standard-library only.\n- P0-B does not call paid generation tools; it creates manual slots.\n- Technical QA does not inspect codec, resolution, duration, or FPS yet.\n- Semantic QA is a review scaffold, not visual understanding.\n"""
    next_md = """# Next Discussion Notes\n\nConfirmed next work should refine P1/P2 execution boundaries before implementing autonomous scouting and Format Miner evolution. MMD/3D and longform remain separate large discussions.\n"""
    completion_md = f"""# Phase 0-B Completion\n\nRun: `{run_id}`\nJob: `{job_id}`\n\nP0-B now has a complete offline production skeleton: manual seed/source intake, visible planning artifacts, manual generation slot, candidate registration, basic QA, manual publish package, and phase report.\n"""
    files = {
        "artifact_index": phase_dir / "phase0_artifact_index.json",
        "test_report": phase_dir / "p0b_test_report.json",
        "known_gaps": phase_dir / "known_gaps.md",
        "next_notes": phase_dir / "next_discussion_notes.md",
        "completion": phase_dir / "phase0_completion.md",
    }
    write_json(files["artifact_index"], artifact_index)
    write_json(files["test_report"], test_report)
    files["known_gaps"].write_text(gaps_md, encoding="utf-8")
    files["next_notes"].write_text(next_md, encoding="utf-8")
    files["completion"].write_text(completion_md, encoding="utf-8")
    for name, path in files.items():
        target = job_report_dir / path.name
        if path.suffix == ".json":
            write_json(target, read_json(path))
        else:
            target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    now = utc_now()
    with connect(base) as conn:
        conn.execute("UPDATE runs SET status = ?, completed_at = ? WHERE run_id = ?", ("completed", now, run_id))
        conn.execute("UPDATE jobs SET status = ?, updated_at = ?, completed_at = ? WHERE job_id = ?", ("completed_p0b", now, now, job_id))
        conn.commit()
    write_decision(base, run_id, job_id, "phase_report", "complete_p0b", "P0-B offline chain report written.")
    return {name: rel(base, path) for name, path in files.items()}


def run_p0b_demo(root: str | Path, seed_text: str, title: str, target_style: str = "ordinary AI format adaptation") -> dict[str, Any]:
    base = root_path(root)
    run_id = create_run(base, seed_text, run_type="production", trigger_type="manual")
    job_id = create_job(base, run_id, title)
    source_id = intake_manual_source(base, run_id, job_id, "text", seed_text, title=title, source_type="user_provided", content_type="text")
    planning = build_planning_artifacts(base, run_id, job_id, source_id, seed_text, target_style=target_style)
    manual_slot = build_manual_generation_slot(base, run_id, job_id)
    fixture = base / "tests" / "fixtures" / "p0b_fixture_candidate.mp4"
    fixture.write_bytes(b"KAIROVE P0-B TEST FIXTURE - NOT AN AI GENERATED VIDEO\n")
    candidate_id = import_candidate(base, job_id, fixture, run_id=run_id, fixture=True)
    quality_report_id = run_basic_qa(base, job_id, candidate_id)
    publish_package_id = build_manual_publish_package(base, job_id, candidate_id)
    phase_report = write_phase0_report(base, run_id, job_id)
    return {
        "root": str(base),
        "run_id": run_id,
        "job_id": job_id,
        "source_id": source_id,
        "planning": planning,
        "manual_slot": manual_slot,
        "candidate_id": candidate_id,
        "quality_report_id": quality_report_id,
        "publish_package_id": publish_package_id,
        "phase_report": phase_report,
    }
