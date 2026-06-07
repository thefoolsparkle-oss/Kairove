from __future__ import annotations

import tempfile
import unittest
import json
from pathlib import Path

from kairove.core import connect, ensure_project
from kairove.p0b import (
    build_manual_publish_package,
    build_planning_artifacts,
    create_job,
    create_run,
    import_candidate,
    intake_manual_source,
    run_p0b_demo,
)


class P0BTests(unittest.TestCase):
    def test_init_creates_config_dirs_and_db(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kairove_p0b_") as tmp:
            root = ensure_project(tmp)
            self.assertTrue((root / "config" / "permissions.json").exists())
            self.assertTrue((root / "config" / "tools.json").exists())
            self.assertTrue((root / "data" / "kairove.sqlite3").exists())
            self.assertTrue((root / "generated_assets" / "jobs").is_dir())
            self.assertTrue((root / "config" / "platforms" / "youtube_shorts.json").exists())
            self.assertTrue((root / "config" / "platforms" / "tiktok.json").exists())

    def test_p0b_demo_completes_offline_chain(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kairove_p0b_") as tmp:
            result = run_p0b_demo(tmp, "一个热门嘴硬情侣短剧的格式种子", "嘴硬情侣格式迁移测试")
            root = Path(result["root"])
            job_dir = root / "generated_assets" / "jobs" / result["job_id"]

            self.assertTrue((job_dir / "sources" / "source_refs.json").exists())
            self.assertTrue((job_dir / "planning" / "format_observation.json").exists())
            self.assertTrue((job_dir / "planning" / "semantic_transfer_brief.md").exists())
            self.assertTrue((job_dir / "prompts" / "prompt_package_000001" / "positive_prompt.txt").exists())
            self.assertTrue((job_dir / "manual_slots" / "manual_slot_000001" / "slot_manifest.json").exists())
            self.assertTrue((job_dir / "generation" / "candidate_manifest.json").exists())
            self.assertTrue((job_dir / "quality" / result["candidate_id"] / "technical_quality_report.json").exists())
            self.assertTrue((job_dir / "publish" / "readiness_report.json").exists())
            self.assertTrue((job_dir / "publish" / "manual_publish_package" / "final_video.mp4").exists())
            self.assertTrue((job_dir / "publish" / "manual_publish_package" / "titles" / "selected_title.txt").exists())
            self.assertTrue((job_dir / "publish" / "manual_publish_package" / "platform_payloads" / "youtube_shorts.json").exists())
            self.assertTrue((job_dir / "publish" / "manual_publish_package" / "platform_payloads" / "tiktok.json").exists())
            self.assertTrue((job_dir / "publish" / "manual_publish_package" / "source_and_asset_provenance.md").exists())
            self.assertTrue((job_dir / "publish" / "manual_publish_package" / "review_summary.md").exists())
            self.assertTrue((job_dir / "publish" / "manual_publish_package" / "self_check_report.md").exists())
            self.assertTrue((job_dir / "reports" / "self_check_report.json").exists())
            self.assertTrue((root / "reports" / "phase_reports" / "phase0_completion.md").exists())

            score_stub = json.loads((job_dir / "planning" / "score_stub.json").read_text(encoding="utf-8"))
            self.assertIn("popularity", score_stub["visible_weights"])
            self.assertIn("growth_speed", score_stub["visible_weights"])

            source_refs = json.loads((job_dir / "sources" / "source_refs.json").read_text(encoding="utf-8"))
            self.assertEqual(source_refs["primary_source"]["mode"], "text")
            self.assertEqual(source_refs["primary_source"]["provenance"]["linked_job"], result["job_id"])

            payloads = json.loads((job_dir / "publish" / "platform_payloads.json").read_text(encoding="utf-8"))
            self.assertEqual(payloads["youtube_shorts"]["status"], "ready_manual")
            self.assertEqual(payloads["tiktok"]["status"], "blocked_tool_setup")

            readiness = json.loads((job_dir / "publish" / "readiness_report.json").read_text(encoding="utf-8"))
            self.assertTrue(readiness["is_test_fixture"])
            self.assertFalse(readiness["real_publish_ready"])

            self_check = json.loads((job_dir / "reports" / "self_check_report.json").read_text(encoding="utf-8"))
            self.assertEqual(self_check["status"], "pass")

            with connect(root) as conn:
                run = conn.execute("SELECT status FROM runs WHERE run_id = ?", (result["run_id"],)).fetchone()
                job = conn.execute("SELECT status FROM jobs WHERE job_id = ?", (result["job_id"],)).fetchone()
                self.assertEqual(run["status"], "completed")
                self.assertEqual(job["status"], "completed_p0b")

    def test_unknown_source_creates_review_item(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kairove_p0b_") as tmp:
            root = ensure_project(tmp)
            run_id = create_run(root, "unknown url seed")
            job_id = create_job(root, run_id, "unknown source review")
            source_id = intake_manual_source(root, run_id, job_id, "url", "https://example.invalid/video", source_type="unknown", content_type="video")
            build_planning_artifacts(root, run_id, job_id, source_id, "test")

            with connect(root) as conn:
                review_count = conn.execute("SELECT COUNT(*) AS c FROM review_items WHERE job_id = ?", (job_id,)).fetchone()["c"]
                source = conn.execute("SELECT review_status FROM sources WHERE source_id = ?", (source_id,)).fetchone()
            self.assertEqual(review_count, 1)
            self.assertEqual(source["review_status"], "pending")

    def test_import_missing_candidate_raises(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kairove_p0b_") as tmp:
            root = ensure_project(tmp)
            run_id = create_run(root, "seed")
            job_id = create_job(root, run_id, "missing candidate")
            with self.assertRaises(FileNotFoundError):
                import_candidate(root, job_id, root / "missing.mp4", run_id=run_id)

    def test_packaging_requires_qa(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kairove_p0b_") as tmp:
            root = ensure_project(tmp)
            run_id = create_run(root, "seed")
            job_id = create_job(root, run_id, "qa required")
            fixture = root / "tests" / "fixtures" / "candidate.mp4"
            fixture.write_bytes(b"fixture")
            candidate_id = import_candidate(root, job_id, fixture, run_id=run_id, fixture=True)
            with self.assertRaises(ValueError):
                build_manual_publish_package(root, job_id, candidate_id)


if __name__ == "__main__":
    unittest.main()
