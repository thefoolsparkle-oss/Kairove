from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from kairove.core import connect
from kairove.core import write_json
from kairove.p1 import run_p1_demo


class P1Tests(unittest.TestCase):
    def test_p1_demo_creates_research_outputs_without_live_claims(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kairove_p1_") as tmp:
            result = run_p1_demo(tmp, "ordinary AI short video trend")
            root = Path(result["root"])
            run_dir = root / "runs" / result["run_id"] / "p1_research"

            self.assertTrue((run_dir / "query_plans").is_dir())
            self.assertTrue((run_dir / "scout_results" / "scout_report.json").exists())
            self.assertTrue((run_dir / "source_candidates" / "dedupe_rank_report.json").exists())
            self.assertTrue((run_dir / "harvested_sources" / "harvest_report.json").exists())
            self.assertTrue((run_dir / "evidence_observations").is_dir())
            self.assertTrue((run_dir / "understanding_reports").is_dir())
            self.assertTrue((run_dir / "format_observations").is_dir())
            self.assertTrue((run_dir / "opportunity_packets").is_dir())
            self.assertTrue((run_dir / "reports" / "research_review.md").exists())
            self.assertTrue((run_dir / "reports" / "p1_self_check_report.json").exists())

            scout_report = json.loads((run_dir / "scout_results" / "scout_report.json").read_text(encoding="utf-8"))
            self.assertFalse(scout_report["live_results_claimed"])
            self.assertGreaterEqual(scout_report["candidate_count"], 4)
            self.assertGreaterEqual(scout_report["fixture_candidate_count"], 4)
            self.assertEqual(scout_report["live_candidate_count"], 0)

            self_check = json.loads((run_dir / "reports" / "p1_self_check_report.json").read_text(encoding="utf-8"))
            self.assertEqual(self_check["status"], "pass")

            opportunity_files = list((run_dir / "opportunity_packets").glob("*.json"))
            self.assertEqual(len(opportunity_files), 1)
            opportunity = json.loads(opportunity_files[0].read_text(encoding="utf-8"))
            self.assertEqual(opportunity["confidence_label"], "weak_observation")
            self.assertEqual(opportunity["p0b_handoff_readiness"], "needs_more_evidence")

            with connect(root) as conn:
                candidates = conn.execute("SELECT COUNT(*) AS c FROM source_candidates WHERE run_id = ?", (result["run_id"],)).fetchone()["c"]
                sources = conn.execute("SELECT COUNT(*) AS c FROM sources WHERE run_id = ?", (result["run_id"],)).fetchone()["c"]
                setup_items = conn.execute("SELECT COUNT(*) AS c FROM tool_setup_items").fetchone()["c"]
            self.assertGreaterEqual(candidates, 4)
            self.assertGreaterEqual(sources, 4)
            self.assertGreaterEqual(setup_items, 4)

            evidence_files = list((run_dir / "evidence_observations").glob("*.json"))
            self.assertGreaterEqual(len(evidence_files), 4)
            evidence = json.loads(evidence_files[0].read_text(encoding="utf-8"))
            self.assertIn("full_video_content", evidence["missing_inputs"])
            self.assertIn("understanding_limits", evidence)

            understanding_files = list((run_dir / "understanding_reports").glob("*.json"))
            understanding = json.loads(understanding_files[0].read_text(encoding="utf-8"))
            self.assertIn("evidence_observation_id", understanding)
            self.assertIn("understanding_limits", understanding)

    def test_fixture_mode_never_claims_live_results(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kairove_p1_") as tmp:
            result = run_p1_demo(tmp, "fixture honesty", scout_mode="fixture")
            run_dir = Path(result["root"]) / "runs" / result["run_id"] / "p1_research"
            for candidate_path in (run_dir / "source_candidates").glob("sourcecand_*.json"):
                candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
                self.assertEqual(candidate["evidence_mode"], "fixture")
                self.assertFalse(candidate["live_results_claimed"])

    def test_live_metadata_candidates_are_not_fixture(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kairove_p1_") as tmp:
            def fake_search(query: str, max_results: int = 5):
                return ([{"url": "https://example.com/live-result", "title": f"Live result for {query}"}], [])

            def fake_wiki(query: str, max_results: int = 5):
                return ([{"url": "https://en.wikipedia.org/wiki/Artificial_intelligence_art", "title": "Artificial intelligence art"}], [])

            with patch("kairove.p1._search_duckduckgo_lite", side_effect=fake_search), patch("kairove.p1._wiki_official_results", side_effect=fake_wiki):
                result = run_p1_demo(tmp, "live scout metadata", scout_mode="live")

            run_dir = Path(result["root"]) / "runs" / result["run_id"] / "p1_research"
            scout_report = json.loads((run_dir / "scout_results" / "scout_report.json").read_text(encoding="utf-8"))
            self.assertTrue(scout_report["live_results_claimed"])
            self.assertGreaterEqual(scout_report["live_candidate_count"], 1)
            self.assertEqual(scout_report["fixture_candidate_count"], 0)

            candidates = [json.loads(path.read_text(encoding="utf-8")) for path in (run_dir / "source_candidates").glob("sourcecand_*.json")]
            self.assertTrue(any(item["evidence_mode"] == "live_metadata" for item in candidates))
            self.assertTrue(all(item["evidence_mode"] != "fixture" for item in candidates))

            manifest_files = list((Path(result["root"]) / "research_assets" / "manifests" / "sources").glob("*.json"))
            self.assertTrue(any(json.loads(path.read_text(encoding="utf-8"))["source_mode"] == "live_metadata" for path in manifest_files))

    def test_youtube_api_key_uses_api_without_exposing_secret(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kairove_p1_") as tmp:
            root = Path(tmp)
            write_json(root / "config" / "secrets.local.json", {"youtube": {"api_key": "secret-test-key"}})

            def fake_fetch(url: str, timeout: float = 8.0):
                self.assertNotIn("secret-test-key", url.split("?")[0])
                if "googleapis.com/youtube/v3/search" in url:
                    return json.dumps({
                        "items": [
                            {
                                "id": {"videoId": "abc123"},
                                "snippet": {
                                    "title": "API title",
                                    "channelTitle": "API channel",
                                    "publishedAt": "2026-01-01T00:00:00Z",
                                },
                            }
                        ]
                    })
                return ""

            with patch("kairove.p1._fetch_text", side_effect=fake_fetch):
                result = run_p1_demo(root, "youtube api trend", scout_mode="live")

            run_dir = root / "runs" / result["run_id"] / "p1_research"
            candidates = [json.loads(path.read_text(encoding="utf-8")) for path in (run_dir / "source_candidates").glob("sourcecand_*.json")]
            api_candidates = [item for item in candidates if item["metadata_source"] == "youtube_data_api_v3_search"]
            self.assertEqual(len(api_candidates), 1)
            self.assertEqual(api_candidates[0]["title"], "API title")
            serialized = json.dumps(candidates, ensure_ascii=False)
            self.assertNotIn("secret-test-key", serialized)

    def test_bilibili_public_web_candidates_are_live_metadata(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kairove_p1_") as tmp:
            def fake_bilibili(query: str, max_results: int = 5):
                return ([
                    {
                        "url": "https://www.bilibili.com/video/BV1abc",
                        "title": "Bili public title",
                        "author": "Bili UP",
                        "published_at": "1780000000",
                        "metadata_source": "bilibili_public_web_search_api",
                        "observed_metrics": {"views": 1234, "likes": None, "comments": None, "shares": None, "favorites": 12, "danmaku": 3},
                    }
                ], [])

            with patch("kairove.p1._bilibili_public_web_results", side_effect=fake_bilibili), patch("kairove.p1._youtube_api_results", return_value=([], ["youtube disabled for test"])), patch("kairove.p1._youtube_html_results", return_value=([], ["youtube html disabled for test"])):
                result = run_p1_demo(tmp, "bilibili public web trend", scout_mode="live")

            run_dir = Path(result["root"]) / "runs" / result["run_id"] / "p1_research"
            candidates = [json.loads(path.read_text(encoding="utf-8")) for path in (run_dir / "source_candidates").glob("sourcecand_*.json")]
            bili = [item for item in candidates if item["metadata_source"] == "bilibili_public_web_search_api"]
            self.assertEqual(len(bili), 1)
            self.assertEqual(bili[0]["platform"], "bilibili")
            self.assertTrue(bili[0]["live_results_claimed"])
            self.assertEqual(bili[0]["evidence_mode"], "live_metadata")
            self.assertEqual(bili[0]["observed_metrics"]["views"], 1234)
            evidence_files = list((Path(result["root"]) / "runs" / result["run_id"] / "p1_research" / "evidence_observations").glob("*.json"))
            self.assertTrue(evidence_files)
            evidence = json.loads(evidence_files[0].read_text(encoding="utf-8"))
            self.assertIn("observed_text", evidence)
            self.assertIn("full_video_content", evidence["missing_inputs"])

    def test_douyin_xhs_are_probe_only_without_setup(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kairove_p1_") as tmp:
            result = run_p1_demo(tmp, "hard platform probe")
            run_dir = Path(result["root"]) / "runs" / result["run_id"] / "p1_research"
            scout_report = json.loads((run_dir / "scout_results" / "scout_report.json").read_text(encoding="utf-8"))
            probes = {item["platform"]: item for item in scout_report["scout_results"] if item["platform"] in {"douyin", "xiaohongshu"}}
            self.assertEqual(set(probes), {"douyin", "xiaohongshu"})
            self.assertTrue(all(item["status"] == "probe_only" for item in probes.values()))
            self.assertTrue(all(item["live_results_claimed"] is False for item in probes.values()))

    def test_p1_manual_seed_is_auxiliary(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kairove_p1_") as tmp:
            result = run_p1_demo(tmp, "manual seed calibration", manual_url="https://example.invalid/manual")
            root = Path(result["root"])
            run_dir = root / "runs" / result["run_id"] / "p1_research"
            ranked = json.loads((run_dir / "source_candidates" / "dedupe_rank_report.json").read_text(encoding="utf-8"))
            self.assertGreater(len(ranked["ranked_candidate_ids"]), 1)

            with connect(root) as conn:
                manual_count = conn.execute(
                    "SELECT COUNT(*) AS c FROM source_candidates WHERE run_id = ? AND platform = 'manual_seed'",
                    (result["run_id"],),
                ).fetchone()["c"]
            self.assertEqual(manual_count, 1)


if __name__ == "__main__":
    unittest.main()
