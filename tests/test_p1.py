from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from kairove.core import connect
from kairove.core import write_json
from kairove.p1 import _reachable_public_seed_results
from kairove.p1 import _wiki_official_results
from kairove.p1 import run_p1_demo


class P1Tests(unittest.TestCase):
    def test_wiki_official_fallback_terms_find_reference_candidates(self) -> None:
        calls: list[str] = []

        def fake_fetch(url: str, timeout: float = 8.0):
            calls.append(url)
            if "YouTube+Shorts" in url:
                return json.dumps(["YouTube Shorts", ["YouTube Shorts"], [""], ["https://en.wikipedia.org/wiki/YouTube_Shorts"]])
            return json.dumps(["too specific", [], [], []])

        with patch("kairove.p1._fetch_text", side_effect=fake_fetch):
            results, gaps = _wiki_official_results("overly specific YouTube Shorts AI short video official wiki reference")

        self.assertEqual(results[0]["url"], "https://en.wikipedia.org/wiki/YouTube_Shorts")
        self.assertEqual(results[0]["metadata_source"], "wikipedia_opensearch")
        self.assertTrue(any("YouTube+Shorts" in url for url in calls))
        self.assertNotIn("returned no reference candidates", " ".join(gaps))

    def test_public_seed_results_require_reachable_pages(self) -> None:
        def fake_fetch(url: str, timeout: float = 8.0):
            if "support.google.com" in url:
                return "<html><head><title>YouTube Shorts Help</title><meta name='description' content='Official help'></head></html>"
            raise OSError("blocked for test")

        with patch("kairove.p1._fetch_text", side_effect=fake_fetch):
            results, gaps = _reachable_public_seed_results("AI shorts trend", max_results=2)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["metadata_source"], "official_reachable_seed")
        self.assertEqual(results[0]["title"], "YouTube Shorts Help")
        self.assertTrue(any("unreachable" in gap for gap in gaps))

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

            with patch("kairove.p1._search_duckduckgo_lite", side_effect=fake_search), patch("kairove.p1._wiki_official_results", side_effect=fake_wiki), patch("kairove.p1._bilibili_public_web_results", return_value=([], ["bilibili disabled for test"])), patch("kairove.p1._youtube_api_results", return_value=([], ["youtube disabled for test"])), patch("kairove.p1._youtube_html_results", return_value=([], ["youtube html disabled for test"])), patch("kairove.p1._fetch_text", return_value="<html><head><title>Live snapshot</title></head></html>"):
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
                if "googleapis.com/youtube/v3/videos" in url:
                    return json.dumps({
                        "items": [
                            {
                                "id": "abc123",
                                "snippet": {
                                    "title": "API detail title",
                                    "channelTitle": "API channel",
                                    "publishedAt": "2026-01-01T00:00:00Z",
                                    "description": "detail description",
                                    "tags": ["ai", "shorts"],
                                    "thumbnails": {"high": {"url": "https://img.youtube.com/vi/abc123/hqdefault.jpg"}},
                                },
                                "contentDetails": {"duration": "PT1M2S", "definition": "hd", "caption": "false"},
                                "statistics": {"viewCount": "1000", "likeCount": "50", "commentCount": "4", "favoriteCount": "0"},
                            }
                        ]
                    })
                return ""

            with patch("kairove.p1._fetch_text", side_effect=fake_fetch):
                result = run_p1_demo(root, "youtube api trend", scout_mode="live")

            run_dir = root / "runs" / result["run_id"] / "p1_research"
            candidates = [json.loads(path.read_text(encoding="utf-8")) for path in (run_dir / "source_candidates").glob("sourcecand_*.json")]
            api_candidates = [item for item in candidates if item["metadata_source"] == "youtube_data_api_v3_search+videos_list"]
            self.assertEqual(len(api_candidates), 1)
            self.assertEqual(api_candidates[0]["title"], "API detail title")
            self.assertEqual(api_candidates[0]["observed_metrics"]["views"], 1000)
            self.assertEqual(api_candidates[0]["extra_metadata"]["duration_iso8601"], "PT1M2S")
            serialized = json.dumps(candidates, ensure_ascii=False)
            self.assertNotIn("secret-test-key", serialized)

    def test_bilibili_public_web_candidates_are_live_metadata(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kairove_p1_") as tmp:
            write_json(Path(tmp) / "config" / "permissions.json", {"permissions": {"research.web_search": "allow_with_limits", "research.collect_metadata": "allow", "research.download_reference_assets": "allow_with_limits", "research.browser_screenshot": "allow_with_limits"}})

            def fake_bilibili(query: str, max_results: int = 5):
                return ([
                    {
                        "url": "https://www.bilibili.com/video/BV1abc",
                        "title": "Bili public title",
                        "author": "Bili UP",
                        "published_at": "1780000000",
                        "metadata_source": "bilibili_public_web_search_api",
                        "observed_metrics": {"views": 1234, "likes": None, "comments": None, "shares": None, "favorites": 12, "danmaku": 3},
                        "cover_url": "https://i0.hdslb.com/bfs/archive/test-cover.jpg",
                        "extra_metadata": {"duration_seconds": 66},
                    }
                ], [])

            html = '<html><head><title>Snapshot title</title><meta name="description" content="Snapshot description"><meta property="og:title" content="OG title"></head><body><h1>Public visible headline</h1><p>Public visible page clue for format packaging.</p></body></html>'

            def fake_screenshot(conn, root, run_id, source_id, candidate_file, now):
                screenshot_path = "research_assets/screenshots/test/source_000001_asset_fake_screenshot.png"
                manifest_path = "research_assets/manifests/assets/asset_fake_screenshot.json"
                write_json(Path(root) / manifest_path, {"asset_type": "page_screenshot", "metadata": {"image_observation": {"width": 1280, "height": 720, "nonblank_score": 0.5, "likely_blank_or_single_color": False}}})
                return screenshot_path, manifest_path, None

            with patch("kairove.p1._bilibili_public_web_results", side_effect=fake_bilibili), patch("kairove.p1._youtube_api_results", return_value=([], ["youtube disabled for test"])), patch("kairove.p1._youtube_html_results", return_value=([], ["youtube html disabled for test"])), patch("kairove.p1._fetch_image_bytes", return_value=(b"fake-cover-bytes", "image/jpeg", None)), patch("kairove.p1._fetch_text", return_value=html), patch("kairove.p1._save_browser_screenshot", side_effect=fake_screenshot):
                result = run_p1_demo(tmp, "bilibili public web trend", scout_mode="live")

            root = Path(result["root"])
            run_dir = root / "runs" / result["run_id"] / "p1_research"
            candidates = [json.loads(path.read_text(encoding="utf-8")) for path in (run_dir / "source_candidates").glob("sourcecand_*.json")]
            bili = [item for item in candidates if item["metadata_source"] == "bilibili_public_web_search_api"]
            self.assertEqual(len(bili), 1)
            self.assertEqual(bili[0]["platform"], "bilibili")
            self.assertTrue(bili[0]["live_results_claimed"])
            self.assertEqual(bili[0]["evidence_mode"], "live_metadata")
            self.assertEqual(bili[0]["observed_metrics"]["views"], 1234)
            self.assertEqual(bili[0]["extra_metadata"]["duration_seconds"], 66)
            source_manifests = [json.loads(path.read_text(encoding="utf-8")) for path in (root / "research_assets" / "manifests" / "sources").glob("*.json")]
            bili_sources = [item for item in source_manifests if item["platform"] == "bilibili"]
            self.assertEqual(len(bili_sources), 1)
            self.assertTrue(bili_sources[0]["files_available"]["cover"])
            self.assertTrue(bili_sources[0]["files_available"]["page_snapshot"])
            self.assertTrue(bili_sources[0]["files_available"]["screenshots"])
            self.assertIsNotNone(bili_sources[0]["files"]["cover"])
            self.assertIsNotNone(bili_sources[0]["files"]["cover_manifest"])
            self.assertIsNotNone(bili_sources[0]["files"]["page_snapshot"])
            self.assertEqual(len(bili_sources[0]["files"]["screenshots"]), 1)
            self.assertEqual(bili_sources[0]["screenshot_observation"]["width"], 1280)
            self.assertFalse(bili_sources[0]["screenshot_observation"]["likely_blank_or_single_color"])
            self.assertTrue((root / bili_sources[0]["files"]["cover"]).exists())
            self.assertTrue((root / bili_sources[0]["files"]["page_snapshot"]).exists())
            self.assertEqual(bili_sources[0]["page_snapshot_metadata"]["title"], "Snapshot title")
            self.assertEqual(bili_sources[0]["page_snapshot_metadata"]["meta"]["description"], "Snapshot description")
            self.assertIn("Public visible headline", bili_sources[0]["page_snapshot_metadata"]["visible_text_snippets"])

            asset_manifests = list((root / "research_assets" / "manifests" / "assets").glob("*.json"))
            self.assertGreaterEqual(len(asset_manifests), 1)
            assets = [json.loads(path.read_text(encoding="utf-8")) for path in asset_manifests]
            asset = [item for item in assets if item["asset_type"] == "cover_image"][0]
            self.assertEqual(asset["asset_type"], "cover_image")
            self.assertEqual(asset["usage_policy"], "analysis_only")

            with connect(root) as conn:
                asset_rows = conn.execute("SELECT COUNT(*) AS c FROM assets WHERE asset_type = 'cover_image'").fetchone()["c"]
            self.assertEqual(asset_rows, 1)

            evidence_files = list((run_dir / "evidence_observations").glob("*.json"))
            self.assertTrue(evidence_files)
            evidence = [json.loads(path.read_text(encoding="utf-8")) for path in evidence_files if json.loads(path.read_text(encoding="utf-8"))["platform"] == "bilibili"][0]
            self.assertIn("observed_text", evidence)
            self.assertIn("cover_file", evidence["available_inputs"])
            self.assertIn("page_snapshot_file", evidence["available_inputs"])
            self.assertIn("page_screenshot_file", evidence["available_inputs"])
            self.assertIn("screenshot_basic_observation", evidence["available_inputs"])
            self.assertIn("page_metadata", evidence["available_inputs"])
            self.assertIn("full_video_content", evidence["missing_inputs"])
            self.assertNotIn("page_screenshot", evidence["missing_inputs"])
            self.assertEqual(evidence["content_visibility"], "metadata_cover_public_html_and_public_screenshot")
            self.assertIsNotNone(evidence["observed_visual"]["cover_file"])
            self.assertIsNotNone(evidence["observed_visual"]["page_snapshot_file"])
            self.assertIsNotNone(evidence["observed_visual"]["page_screenshot"])
            self.assertEqual(evidence["observed_visual"]["screenshot_observation"]["height"], 720)
            self.assertEqual(evidence["observed_text"]["page_metadata"]["open_graph"]["og:title"], "OG title")
            self.assertIn("Public visible headline", evidence["observed_text"]["page_visible_text_snippets"])

            understanding_files = list((run_dir / "understanding_reports").glob("*.json"))
            understanding = [json.loads(path.read_text(encoding="utf-8")) for path in understanding_files if json.loads(path.read_text(encoding="utf-8"))["source_id"] == bili_sources[0]["source_id"]][0]
            self.assertEqual(understanding["text_signals"]["page_metadata_title"], "Snapshot title")
            self.assertIn("Public visible page clue for format packaging.", understanding["text_signals"]["visible_text"])
            self.assertIsNotNone(understanding["visual_signals"]["page_screenshot"])
            self.assertEqual(understanding["visual_signals"]["screenshot_basic_observation"]["nonblank_score"], 0.5)

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
