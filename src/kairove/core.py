from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

APP_NAME = "Kairove"
DB_FILE = "data/kairove.sqlite3"

ROOT_DIRS = [
    "config",
    "config/platforms",
    "config/score_profiles",
    "config/route_profiles",
    "data",
    "runs",
    "research_assets",
    "research_assets/manifests",
    "local_assets",
    "generated_assets",
    "generated_assets/jobs",
    "generated_assets/manifests",
    "reports",
    "reports/phase_reports",
    "reports/implementation_logs",
    "tests/fixtures",
    "logs",
]

DEFAULT_PERMISSIONS = {
    "research.web_search": "ask",
    "research.collect_metadata": "allow",
    "research.download_reference_assets": "ask",
    "research.download_assets": "ask",
    "research.large_scale_downloads": "ask",
    "research.fetch_comments": "ask",
    "research.crawl_comments": "ask",
    "asset.use_official_assets_directly": "allow",
    "asset.use_personal_creator_assets_directly": "ask",
    "asset.use_unknown_assets_directly": "ask",
    "asset.generate_visual_assets": "allow",
    "asset.generate_audio_assets": "allow",
    "asset.train_voice": "ask",
    "generation.generate_low_cost_drafts": "allow_with_limits",
    "generation.low_cost_generation": "allow_with_limits",
    "generation.generate_high_cost_candidates": "ask",
    "generation.high_cost_api": "ask",
    "generation.batch_generation": "allow_with_limits",
    "generation.retry_generation": "allow_with_limits",
    "publish.create_package": "allow",
    "publish.upload_draft": "ask",
    "publish.schedule_publish": "ask",
    "publish.auto_publish": "ask",
    "publish.fetch_metrics": "allow",
    "publish.fetch_comments": "allow",
    "system.modify_config": "ask",
    "system.delete_generated_assets": "ask",
    "system.delete_local_assets": "deny",
    "system.run_background_tasks": "allow",
}

DEFAULT_RISK_POLICY = {
    "official_misleading_risk": {"enabled": False},
    "official_assets": {
        "images": "direct_use",
        "videos": "direct_use",
        "music": "direct_use",
        "sfx": "direct_use",
        "require_review": False,
        "music_requires_platform_risk_note": True,
    },
    "personal_creator_assets": {
        "direct_use": "ask",
        "reference_use": "allow",
        "style_analysis": "allow",
    },
    "unknown_source_assets": {
        "direct_use": "ask",
        "reference_use": "ask",
        "style_analysis": "allow",
    },
    "generated_assets": {"direct_use": "allow"},
    "voice": {
        "user_trained": "allow",
        "generated_original": "allow",
        "official_character_clone": "ask",
        "real_person_clone": "ask",
    },
}

DEFAULT_BUDGETS = {
    "daily_max_cost": None,
    "per_run_max_cost": None,
    "per_job_max_cost": None,
    "high_cost_confirmation_threshold": None,
    "max_parallel_generations": 4,
    "default_retry_rounds": 5,
}

DEFAULT_TOOLS = {
    "manual_generation_slot": {
        "status": "available",
        "tool_type": "manual_bridge",
        "outputs": ["video", "image", "audio"],
    },
    "ai_video_generation_api": {
        "status": "not_configured",
        "tool_type": "image_to_video | text_to_video | video_to_video",
        "outputs": ["video"],
        "setup_requirements": ["choose provider", "configure account/API/local tool"],
    },
    "local_generation_tool": {
        "status": "not_configured",
        "tool_type": "text_to_video | image_to_video | video_to_video",
        "outputs": ["video"],
        "setup_requirements": ["install local tool", "configure export path", "confirm metadata/export support"],
    },
    "ffprobe": {
        "status": "unknown",
        "tool_type": "media_probe",
        "outputs": ["technical_metadata"],
    },
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS id_counters (
  prefix TEXT PRIMARY KEY,
  value INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS runs (
  run_id TEXT PRIMARY KEY,
  run_type TEXT NOT NULL,
  trigger_type TEXT NOT NULL,
  input_summary TEXT NOT NULL,
  status TEXT NOT NULL,
  started_at TEXT NOT NULL,
  completed_at TEXT,
  created_by TEXT NOT NULL,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS jobs (
  job_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  job_type TEXT NOT NULL,
  title_working TEXT NOT NULL,
  status TEXT NOT NULL,
  priority TEXT NOT NULL,
  target_platforms_json TEXT NOT NULL,
  job_dir TEXT NOT NULL,
  user_notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  completed_at TEXT,
  FOREIGN KEY(run_id) REFERENCES runs(run_id)
);

CREATE TABLE IF NOT EXISTS decision_logs (
  decision_id TEXT PRIMARY KEY,
  run_id TEXT,
  job_id TEXT,
  stage TEXT NOT NULL,
  actor TEXT NOT NULL,
  decision TEXT NOT NULL,
  inputs_json TEXT NOT NULL,
  reason TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS review_items (
  review_id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  run_id TEXT,
  job_id TEXT,
  blocking INTEGER NOT NULL,
  priority TEXT NOT NULL,
  summary TEXT NOT NULL,
  details_path TEXT,
  system_recommendation TEXT,
  options_json TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  resolved_at TEXT,
  user_response TEXT
);

CREATE TABLE IF NOT EXISTS tool_setup_items (
  setup_id TEXT PRIMARY KEY,
  tool_id TEXT NOT NULL,
  missing_json TEXT NOT NULL,
  impact TEXT NOT NULL,
  user_action_required INTEGER NOT NULL,
  priority TEXT NOT NULL,
  status TEXT NOT NULL,
  test_steps_json TEXT NOT NULL,
  notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS source_candidates (
  candidate_source_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  platform TEXT NOT NULL,
  url TEXT,
  title TEXT NOT NULL,
  author TEXT,
  content_type TEXT NOT NULL,
  observed_metrics_json TEXT NOT NULL,
  discovery_reason_json TEXT NOT NULL,
  status TEXT NOT NULL,
  collected_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sources (
  source_id TEXT PRIMARY KEY,
  candidate_source_id TEXT NOT NULL,
  run_id TEXT NOT NULL,
  platform TEXT NOT NULL,
  url TEXT,
  source_type TEXT NOT NULL,
  content_type TEXT NOT NULL,
  usage_policy TEXT NOT NULL,
  review_status TEXT NOT NULL,
  harvest_status TEXT NOT NULL,
  manifest_path TEXT NOT NULL,
  understanding_report_path TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS assets (
  asset_id TEXT PRIMARY KEY,
  asset_class TEXT NOT NULL,
  asset_type TEXT NOT NULL,
  source_id TEXT,
  job_id TEXT,
  storage_path TEXT NOT NULL,
  hash TEXT,
  source_type TEXT NOT NULL,
  usage_policy TEXT NOT NULL,
  review_status TEXT NOT NULL,
  metadata_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS generation_steps (
  step_id TEXT PRIMARY KEY,
  job_id TEXT NOT NULL,
  candidate_id TEXT,
  step_type TEXT NOT NULL,
  tool_id TEXT NOT NULL,
  input_assets_json TEXT NOT NULL,
  output_assets_json TEXT NOT NULL,
  prompt_path TEXT,
  parameters_json TEXT NOT NULL,
  status TEXT NOT NULL,
  error_message TEXT,
  started_at TEXT,
  completed_at TEXT
);

CREATE TABLE IF NOT EXISTS candidates (
  candidate_id TEXT PRIMARY KEY,
  job_id TEXT NOT NULL,
  candidate_type TEXT NOT NULL,
  status TEXT NOT NULL,
  output_path TEXT NOT NULL,
  generation_steps_json TEXT NOT NULL,
  quality_report_id TEXT,
  score REAL,
  selected_reason TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quality_reports (
  quality_report_id TEXT PRIMARY KEY,
  candidate_id TEXT NOT NULL,
  job_id TEXT NOT NULL,
  technical_qa_path TEXT,
  semantic_qa_path TEXT,
  failure_tags_json TEXT NOT NULL,
  publish_ready INTEGER NOT NULL,
  decision TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS publish_packages (
  publish_package_id TEXT PRIMARY KEY,
  job_id TEXT NOT NULL,
  final_video_path TEXT NOT NULL,
  cover_paths_json TEXT NOT NULL,
  platform_payloads_path TEXT NOT NULL,
  readiness_report_path TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS publish_records (
  publish_record_id TEXT PRIMARY KEY,
  job_id TEXT NOT NULL,
  platform TEXT NOT NULL,
  method TEXT NOT NULL,
  status TEXT NOT NULL,
  platform_item_id TEXT,
  url TEXT,
  payload_path TEXT,
  error_message TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
"""


class ClosingConnection(sqlite3.Connection):
    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> bool:
        result = super().__exit__(exc_type, exc_value, traceback)
        self.close()
        return bool(result)

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def root_path(root: str | Path) -> Path:
    return Path(root).expanduser().resolve()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_human_text(path: Path, text: str) -> None:
    ensure_dir(path.parent)
    # UTF-8 with BOM makes Chinese Markdown easier to open in legacy Windows tools.
    path.write_text(text, encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def append_jsonl(path: Path, item: Any) -> None:
    ensure_dir(path.parent)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(item, ensure_ascii=False) + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")
    except ValueError:
        return str(path.resolve())


def connect(root: str | Path) -> sqlite3.Connection:
    base = root_path(root)
    db_path = base / DB_FILE
    ensure_dir(db_path.parent)
    conn = sqlite3.connect(db_path, factory=ClosingConnection)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(root: str | Path) -> None:
    with connect(root) as conn:
        conn.executescript(SCHEMA)
        conn.commit()


def next_id(conn: sqlite3.Connection, prefix: str, width: int = 6) -> str:
    row = conn.execute("SELECT value FROM id_counters WHERE prefix = ?", (prefix,)).fetchone()
    value = 1 if row is None else int(row["value"]) + 1
    if row is None:
        conn.execute("INSERT INTO id_counters(prefix, value) VALUES (?, ?)", (prefix, value))
    else:
        conn.execute("UPDATE id_counters SET value = ? WHERE prefix = ?", (value, prefix))
    return f"{prefix}_{value:0{width}d}"


def deep_merge_defaults(existing: Any, defaults: Any) -> Any:
    if isinstance(existing, dict) and isinstance(defaults, dict):
        merged = dict(existing)
        for key, value in defaults.items():
            if key in merged:
                merged[key] = deep_merge_defaults(merged[key], value)
            else:
                merged[key] = value
        return merged
    return existing


def apply_policy_migrations(relative_path: str, data: Any) -> Any:
    if not isinstance(data, dict):
        return data
    if relative_path == "config/user_preferences.json":
        if data.get("target_platforms") in (["bilibili", "douyin", "xiaohongshu", "youtube"], None):
            data["target_platforms"] = ["bilibili", "douyin", "xiaohongshu", "youtube_shorts"]
        data.setdefault("platform_stubs", ["tiktok", "kuaishou", "instagram_reels"])
        data["manual_seed_role"] = "p0b_primary_acceptance_chain"
    if relative_path == "config/permissions.json":
        permissions = data.setdefault("permissions", {})
        permissions["generation.generate_low_cost_drafts"] = "allow_with_limits"
        permissions["generation.low_cost_generation"] = "allow_with_limits"
        permissions.setdefault("research.large_scale_downloads", "ask")
        permissions.setdefault("research.crawl_comments", "ask")
        permissions.setdefault("research.download_assets", "ask")
        permissions["publish.auto_publish"] = "ask"
        permissions["system.delete_local_assets"] = "deny"
        permissions.setdefault("system.delete_generated_assets", "ask")
    if relative_path == "config/score_profiles/trend_video_v1.json":
        weights = data.setdefault("weights", {})
        old_keys = {"interest_guess", "risk_or_review_need"}
        if old_keys.intersection(weights):
            data["version"] = "p0b_locked_2026_06_06"
            data["weights"] = {
                "popularity": 0.2,
                "growth_speed": 0.2,
                "reproduction_clarity": 0.14,
                "production_feasibility": 0.14,
                "asset_availability": 0.1,
                "platform_fit": 0.1,
                "comment_sentiment": 0.08,
                "fatigue_or_overused_risk": -0.12,
            }
    return data


def init_config(root: str | Path) -> None:
    base = root_path(root)
    defaults = {
        "config/system.json": {
            "project": APP_NAME,
            "config_version": "p0b_json_v1",
            "created_for_phase": "P0-B",
        },
        "config/permissions.json": {"permissions": DEFAULT_PERMISSIONS},
        "config/budgets.json": {"budget": DEFAULT_BUDGETS},
        "config/risk_policy.json": {"risk_policy": DEFAULT_RISK_POLICY},
        "config/tools.json": {"tools": DEFAULT_TOOLS},
        "config/user_preferences.json": {
            "language_policy": {
                "default_user_facing": "zh",
                "metadata_primary": "zh",
                "youtube_shorts_auxiliary_metadata": "en",
                "prompt_default": "zh_explanation_plus_en_generation_prompt",
                "internal_keys": "en",
            },
            "target_platforms": ["bilibili", "douyin", "xiaohongshu", "youtube_shorts"],
            "platform_stubs": ["tiktok", "kuaishou", "instagram_reels"],
            "duration_policy": "fit_format",
            "manual_seed_role": "p0b_primary_acceptance_chain",
            "p0b_format_taste": [
                "short_joke",
                "abstract_short_drama",
                "character_substitution",
                "plot_reversal",
                "spoken_copywriting_adaptation",
                "ai_animation_skit",
            ],
        },
        "config/platforms/bilibili.json": {"platform": "bilibili", "status": "p0b_primary", "publish_modes": ["manual_package"]},
        "config/platforms/douyin.json": {"platform": "douyin", "status": "p0b_primary", "publish_modes": ["manual_package"]},
        "config/platforms/xiaohongshu.json": {"platform": "xiaohongshu", "status": "p0b_primary", "publish_modes": ["manual_package"]},
        "config/platforms/youtube_shorts.json": {"platform": "youtube_shorts", "status": "p0b_primary", "publish_modes": ["manual_package"], "auxiliary_metadata_language": "en"},
        "config/platforms/tiktok.json": {"platform": "tiktok", "status": "stub", "publish_modes": ["manual_package_stub"]},
        "config/platforms/kuaishou.json": {"platform": "kuaishou", "status": "stub", "publish_modes": ["manual_package_stub"]},
        "config/platforms/instagram_reels.json": {"platform": "instagram_reels", "status": "stub", "publish_modes": ["manual_package_stub"]},
        "config/score_profiles/trend_video_v1.json": {
            "profile_type": "trend",
            "version": "p0b_locked_2026_06_06",
            "weights": {
                "popularity": 0.2,
                "growth_speed": 0.2,
                "reproduction_clarity": 0.14,
                "production_feasibility": 0.14,
                "asset_availability": 0.1,
                "platform_fit": 0.1,
                "comment_sentiment": 0.08,
                "fatigue_or_overused_risk": -0.12,
            },
            "policy": {
                "popularity_and_growth_start_higher": True,
                "fatigue_uses_comment_growth_interaction_quality": True,
                "major_weight_changes_require_user_approval": True,
            },
        },
        "config/score_profiles/quality_ordinary_ai_v1.json": {
            "profile_type": "quality",
            "version": "1.0",
            "weights": {"technical_validity": 0.5, "semantic_fit": 0.5},
        },
        "config/route_profiles/ordinary_ai_format_video.json": {
            "route_id": "ordinary_ai_format_video",
            "default_generation_mode": "manual_generation_slot",
        },
    }
    for relative_path, data in defaults.items():
        path = base / relative_path
        next_data = data
        if path.exists():
            current = read_json(path)
            merged = deep_merge_defaults(current, data)
            merged = apply_policy_migrations(relative_path, merged)
            if merged != current:
                try:
                    write_json(path, merged)
                except PermissionError as exc:
                    append_jsonl(
                        base / "logs" / "config_migration_warnings.jsonl",
                        {
                            "path": relative_path,
                            "reason": "permission_denied",
                            "message": str(exc),
                            "created_at": utc_now(),
                        },
                    )
        else:
            next_data = apply_policy_migrations(relative_path, data)
            try:
                write_json(path, next_data)
            except PermissionError as exc:
                append_jsonl(
                    base / "logs" / "config_migration_warnings.jsonl",
                    {
                        "path": relative_path,
                        "reason": "permission_denied",
                        "message": str(exc),
                        "created_at": utc_now(),
                    },
                )


def ensure_project(root: str | Path) -> Path:
    base = root_path(root)
    for item in ROOT_DIRS:
        ensure_dir(base / item)
    init_config(base)
    init_db(base)
    return base


def permission_state(root: str | Path, capability: str) -> str:
    data = read_json(root_path(root) / "config/permissions.json")
    return data.get("permissions", {}).get(capability, "ask")


def fetch_one(conn: sqlite3.Connection, table: str, key: str, value: str) -> sqlite3.Row:
    row = conn.execute(f"SELECT * FROM {table} WHERE {key} = ?", (value,)).fetchone()
    if row is None:
        raise KeyError(f"{table}.{key} not found: {value}")
    return row


def job_dir(root: str | Path, job_id: str) -> Path:
    return root_path(root) / "generated_assets" / "jobs" / job_id
