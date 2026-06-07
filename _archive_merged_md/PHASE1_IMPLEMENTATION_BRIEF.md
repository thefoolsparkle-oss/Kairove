# Kairove Phase 1 Implementation Brief

## 0. Status

This is a planning document, not implementation code.

Current status:

```text
Phase 1 planning: in progress
Phase 1 implementation: not started
Code writing: not allowed until the user explicitly asks
```

Purpose of this brief:

```text
Make P1 concrete enough to implement later without expanding beyond P1.
```

P1 still does not generate videos.

---

## 1. P1 Boundary

P1 builds the first autonomous trend/source intelligence layer.

P1 includes:

- autonomous query planning;
- broad web source discovery;
- Bilibili source discovery v1;
- YouTube source discovery v1 if access is practical;
- wiki and official page lookup;
- Douyin/Xiaohongshu capability probing;
- manual seed link support as an auxiliary route;
- source candidate normalization;
- source harvesting;
- provenance manifests;
- source understanding reports;
- weak/early format observations;
- human-readable research review reports;
- ToolSetupItems for missing login/API/browser capability.

P1 excludes:

- video generation;
- production jobs;
- final Format objects;
- full Trend Analyst scoring;
- full Format Miner;
- publishing;
- MMD/3D;
- longform;
- fake platform API output.

---

## 2. P1 Output Folders

Recommended folder layout:

```text
runs/
  run_000001/
    run_config.json
    decision_log.jsonl
    review_items.jsonl
    tool_setup_items.jsonl

    query_plans/
      query_plan_000001.json

    scout_results/
      search_engine.json
      bilibili.json
      youtube.json
      wiki_official.json
      douyin_xhs_capability.json
      manual_seed.json

    source_candidates/
      source_candidates.jsonl
      dedupe_report.json
      ranking_report.json

    harvested_sources/
      src_000001/
        source.json
        manifest.json
        metadata.json
        raw_snapshot.html
        transcript.txt
        comments.json
        cover.jpg
        screenshots/
        evidence_notes.md

    understanding_reports/
      src_000001_understanding.md
      src_000001_understanding.json

    format_observations/
      fmt_obs_000001.json
      fmt_obs_000001.md

    reports/
      research_review.md
      run_summary.json
```

Global folders used by P1:

```text
research_assets/
  sources/
  manifests/
  snapshots/
  comments/
  covers/
  screenshots/

local_assets/
  user_provided/
  trained_voice/
  official_assets_curated_by_user/

generated_assets/
  reserved_for_later_phases/
```

Rule:

```text
research_assets, local_assets, and generated_assets must never be mixed.
```

---

## 3. Conceptual Command Shape

These are not final CLI commands. They describe what future commands should do.

Autonomous trend patrol:

```text
kairove scout --mode auto_trend_patrol --platforms web,bilibili,youtube --categories ai_video,meme,horror,anime_game,music --max-candidates 300
```

Keyword/fandom research:

```text
kairove scout --mode keyword_search --keywords "AI短剧,抽象短剧,二游CP演绎" --platforms web,bilibili
```

Official/wiki reference research:

```text
kairove scout --mode fandom_research --world "example_world" --characters "A,B" --source-preference official,wiki,platform_video
```

Manual seed auxiliary route:

```text
kairove scout --mode manual_seed --urls urls.txt --intent analyze_and_reproduce
```

Every run should create a Run, a permission snapshot, a config snapshot, a decision log, and a final report.

---

## 4. P1 Data Contracts

These are implementation targets, not locked final database schemas.

### 4.1 QueryPlan

```json
{
  "query_plan_id": "query_plan_000001",
  "run_id": "run_000001",
  "mode": "auto_trend_patrol",
  "goal": "find current AI short video formats",
  "time_window": "recent",
  "platforms": ["search", "bilibili", "youtube"],
  "queries": [],
  "created_at": "..."
}
```

Each query item should include:

```json
{
  "query_id": "query_000001",
  "platform": "bilibili",
  "query": "AI 抽象短剧",
  "purpose": "find repeated script patterns",
  "round": 1,
  "source_reason": "planner_from_category",
  "max_results": 50
}
```

### 4.2 ScoutResult

```json
{
  "scout_result_id": "scout_result_000001",
  "run_id": "run_000001",
  "platform": "bilibili",
  "status": "completed | partial | failed | blocked",
  "queries_attempted": 0,
  "candidates_found": 0,
  "failures": [],
  "capability_notes": [],
  "created_at": "..."
}
```

### 4.3 SourceCandidate

Minimum P1 fields:

```json
{
  "candidate_source_id": "cand_src_000001",
  "run_id": "run_000001",
  "platform": "bilibili | youtube | search | wiki | douyin | xiaohongshu | manual",
  "url": "...",
  "canonical_url": "...",
  "title": "...",
  "author": "...",
  "content_type": "video | audio | article | wiki_page | topic_page | profile | unknown",
  "observed_metrics": {
    "views": null,
    "likes": null,
    "comments": null,
    "shares": null,
    "favorites": null
  },
  "published_at": null,
  "collected_at": "...",
  "discovery_reason": ["keyword_match"],
  "dedupe_key": "...",
  "initial_relevance_score": 0.0,
  "status": "new | selected_for_harvest | ignored | failed"
}
```

### 4.4 Source

Minimum P1 fields:

```json
{
  "source_id": "src_000001",
  "candidate_source_id": "cand_src_000001",
  "run_id": "run_000001",
  "platform": "bilibili",
  "url": "...",
  "source_type": "official | personal_creator | platform_user | wiki | search_result | generated | user_provided | unknown",
  "content_type": "video | image | audio | page | comment_thread | unknown",
  "usage_policy": "analysis_only | reference_only | style_analysis | direct_use | generated | user_provided | blocked | unknown",
  "review_status": "not_required | pending | approved | rejected",
  "harvest_status": "metadata_only | partial | complete | failed",
  "manifest_path": "...",
  "understanding_report_path": "...",
  "created_at": "...",
  "updated_at": "..."
}
```

### 4.5 SourceManifest

```json
{
  "manifest_id": "manifest_src_000001",
  "source_id": "src_000001",
  "original_url": "...",
  "platform": "bilibili",
  "source_type": "platform_user",
  "usage_policy": "analysis_only",
  "review_status": "pending",
  "local_files": [],
  "used_for": ["trend_analysis", "format_observation"],
  "provenance_notes": "...",
  "created_at": "..."
}
```

### 4.6 UnderstandingReport

JSON fields:

```json
{
  "understanding_report_id": "understand_000001",
  "source_id": "src_000001",
  "summary": "...",
  "visible_elements": [],
  "script_or_caption_summary": "...",
  "audio_clues": [],
  "visual_style_clues": [],
  "format_clues": [],
  "possible_ai_tools": [],
  "audience_signal_summary": "...",
  "confidence": "low | medium | high",
  "missing_evidence": []
}
```

Markdown version should be readable by the user.

### 4.7 FormatObservation

```json
{
  "format_observation_id": "fmt_obs_000001",
  "run_id": "run_000001",
  "observation_status": "weak_observation | promising_observation | strong_observation | needs_more_sources",
  "short_name": "...",
  "format_hypothesis": "...",
  "source_ids": [],
  "evidence_count": 0,
  "repeated_elements": [],
  "possible_transfer_targets": [],
  "why_it_may_be_hot": [],
  "why_it_may_be_tired": [],
  "uncertainties": [],
  "recommended_next_action": "collect_more | review | ignore | later_format_mining"
}
```

P1 FormatObservation is not a full Format.

---

## 5. Status Values

P1 should keep status values boring and explicit.

Run status:

```text
pending | running | waiting_for_user | failed | completed | abandoned
```

Scout status:

```text
not_started | running | completed | partial | blocked | failed
```

Harvest status:

```text
not_started | metadata_only | partial | complete | failed
```

Review status:

```text
not_required | pending | approved | rejected
```

Format observation status:

```text
weak_observation | promising_observation | strong_observation | needs_more_sources
```

Tool setup status:

```text
needed | requested | configured | failed | deferred
```

---

## 6. P1 Pipeline

Recommended run order:

```text
1. Create Run
2. Capture config and permission snapshot
3. Generate QueryPlan
4. Execute SearchEngineScout
5. Execute BilibiliScout v1
6. Execute YouTubeScout v1 if available
7. Execute Wiki / Official Source Scout
8. Probe Douyin/XHS capability
9. Normalize SourceCandidates
10. Deduplicate candidates
11. Rank candidates for harvest
12. Harvest selected sources
13. Write manifests
14. Produce UnderstandingReports
15. Produce FormatObservations
16. Create ReviewItems and ToolSetupItems
17. Write ResearchReviewReport
18. Mark Run completed / partial / failed
```

Hard rule:

```text
If a platform is blocked, record it. Do not invent data.
```

---

## 7. First Run Presets

### 7.1 General AI Video Trend Patrol

```json
{
  "mode": "auto_trend_patrol",
  "categories": ["ai_video", "meme", "horror", "anime_game", "music"],
  "platforms": ["search", "bilibili", "youtube"],
  "max_candidates": 300,
  "max_harvested_sources": 60
}
```

### 7.2 Chinese Short Video Format Patrol

```json
{
  "mode": "auto_trend_patrol",
  "categories": ["short_drama", "abstract_short", "hot_script", "anime_game_reenactment"],
  "platforms": ["search", "bilibili", "douyin_probe", "xiaohongshu_probe"],
  "max_candidates": 300,
  "max_harvested_sources": 50
}
```

### 7.3 Fandom / Character Reference Research

```json
{
  "mode": "fandom_research",
  "source_preference": ["official", "wiki", "platform_video"],
  "max_candidates": 120,
  "max_harvested_sources": 30
}
```

---

## 8. Research Review Report Template

Recommended Markdown structure:

```text
# Research Review: run_000001

## Summary
- Goal:
- Platforms checked:
- Candidates found:
- Sources harvested:
- Possible format observations:
- Review items:
- Tool setup items:

## Best Source Candidates
| Rank | Platform | Title | Why It Matters | Metrics | Status |

## Harvested Sources
| Source | Type | Usage Policy | Review Status | Local Evidence |

## Possible Formats
### fmt_obs_000001: short name
- Status:
- Evidence count:
- Repeated elements:
- Why it may be hot:
- Why it may be tired:
- Uncertainties:
- Recommended next action:

## Official Assets Found
| Source | Asset Type | Direct Use? | Notes |

## Assets Needing Review
| Source | Reason | Suggested Action |

## Platform / Tool Gaps
| Platform | Missing Capability | ToolSetupItem | Impact |

## Recommended Next Run
```

The report should help the user decide what to inspect next.

---

## 9. Test Fixture Plan

P1 tests should be fixture-first.

Use saved fixture inputs instead of live internet in normal tests:

```text
tests/fixtures/p1/
  search_results_sample.json
  bilibili_results_sample.json
  youtube_results_sample.json
  wiki_page_sample.html
  source_candidate_duplicates.jsonl
  source_manifest_sample.json
  understanding_report_sample.json
  format_observation_sample.json
```

Test categories:

- QueryPlan creates platform-specific queries;
- SourceCandidates normalize into stable fields;
- duplicate URLs collapse correctly;
- failed scout creates failure record;
- official source policy is assigned correctly;
- personal/unknown source creates ReviewItem;
- blocked platform creates ToolSetupItem;
- FormatObservation does not become full Format;
- ResearchReviewReport renders readable Markdown.

Live internet tests should be optional and clearly marked.

---

## 10. P1 Deferred Items

Do not pull these into P1 unless the user explicitly reopens scope:

- full browser automation for every platform;
- full comment crawling;
- full danmaku parsing;
- automatic video downloading everywhere;
- robust audio fingerprinting;
- deep AI-model detection;
- full TrendScorecard;
- full Format Miner;
- production route planning;
- generation model calls;
- publishing.

P1 can leave ToolSetupItems for these.

---

## 11. P1 Completion Criteria

P1 can be considered complete when one autonomous run can:

1. create a QueryPlan;
2. search broad web and Bilibili;
3. optionally search YouTube if available;
4. probe Douyin/XHS and report gaps;
5. normalize SourceCandidates;
6. deduplicate candidates;
7. harvest selected sources at metadata or partial level;
8. write manifests with provenance;
9. classify usage policy;
10. create ReviewItems for uncertain/personal assets;
11. create ToolSetupItems for missing capabilities;
12. generate UnderstandingReports;
13. generate weak/promising FormatObservations;
14. write a ResearchReviewReport;
15. pass fixture tests.

---

## 12. Next Discussion After This Brief

Before coding P1, discuss only these P1-specific decisions:

```text
1. Should P1 implementation start from Bilibili first after web search?
2. What exact max_candidates and max_harvested_sources should be default?
3. Should raw snapshots be enabled by default for important sources?
4. What should the first fixture examples look like?
5. Which report format is easiest for the user to review?
```

Do not use this discussion to schedule later phases.
---

## 13. P1 Default Decisions

These defaults answer the open questions in section 12. They can still be adjusted before coding, but they are the current recommended baseline.

### 13.1 First Implementation Priority

Default:

```text
Start with web search + Bilibili.
```

Implementation order inside P1:

```text
1. QueryPlan
2. SearchEngineScout
3. BilibiliScout v1
4. Harvester v1
5. ResearchReviewReport v1
6. YouTubeScout v1
7. Wiki / Official Source Scout
8. Douyin/XHS capability probe
9. ManualSeedScout auxiliary
10. FormatObservation v1
```

Reason:

- web search gives broad discovery and fallback evidence;
- Bilibili is high-value for Chinese anime/game/video-format culture;
- YouTube is useful, but less central than Bilibili for the first Chinese-language workflow;
- Douyin/XHS matter a lot, but P1 should first probe access honestly instead of pretending robust crawling exists;
- ManualSeedScout is kept late enough that it does not become the spine of the architecture.

### 13.2 Default Candidate and Harvest Limits

Default run limits:

```json
{
  "max_candidates_total": 300,
  "max_harvested_sources_total": 60,
  "max_format_observations": 20,
  "max_sources_per_format_observation": 12
}
```

Default platform candidate split:

```json
{
  "search": 100,
  "bilibili": 120,
  "youtube": 50,
  "wiki_official": 30,
  "douyin_xhs_probe": 0
}
```

`douyin_xhs_probe` has no normal candidate budget at first because it may produce capability reports, ToolSetupItems, and manually imported evidence rather than stable search results.

Harvest priority order:

```text
1. likely repeated video format examples
2. high-engagement examples
3. official asset/reference pages
4. pages with useful comments/audience signals
5. AI-tool clue sources
6. weaker related examples
```

Budget behavior:

- if fewer than 300 candidates are found, do not pad with junk;
- if more than 300 candidates are found, keep overflow counts and reasons in the run summary;
- if a source is clearly official and useful, it can be harvested even if its engagement metrics are low;
- if a platform is blocked, unused budget does not automatically transfer to endless crawling.

### 13.3 Raw Snapshot Default

Default:

```text
Raw snapshots are enabled for important sources, not for every candidate.
```

Save raw snapshots for:

- likely format roots;
- high-engagement examples;
- official pages and verified accounts;
- pages whose comments/metadata affect judgement;
- pages likely to disappear or change;
- sources that create ReviewItems.

Do not save raw snapshots by default for:

- weak search results;
- duplicate pages;
- login-only or account-private pages;
- pages with no relevance after ranking;
- low-value platform noise.

Snapshot manifest fields:

```json
{
  "snapshot_id": "snapshot_000001",
  "source_id": "src_000001",
  "snapshot_type": "html | screenshot | metadata_json | comment_json",
  "reason_saved": "high_engagement | official_reference | review_needed | unstable_source | format_root_candidate",
  "local_path": "...",
  "captured_at": "..."
}
```

### 13.4 First Fixture Examples

P1 should start with compact, hand-curated fixtures before live network tests.

Fixture set A: broad web search

```text
search_results_sample.json:
  Includes trend article, indexed video page, official page, weak unrelated result, duplicate result.
```

Fixture set B: Bilibili video discovery

```text
bilibili_results_sample.json:
  Includes anime/game reenactment example, AI short video example, repeated-script example, low-value duplicate.
```

Fixture set C: YouTube discovery

```text
youtube_results_sample.json:
  Includes AI horror short example, AI tool showcase, unrelated tutorial, duplicate canonical URL case.
```

Fixture set D: official/wiki source

```text
wiki_official_sample.json:
  Includes official character page, wiki character page, unknown fan mirror page.
```

Fixture set E: blocked platform probe

```text
douyin_xhs_probe_sample.json:
  Includes login required, rate limited, browser-only, manual import available.
```

Fixture set F: format observation

```text
format_observation_sample.json:
  Includes 3 similar sources, one strong source with comments, and one weak observation needing more evidence.
```

Fixture rule:

```text
Fixtures should contain fake/sample data shaped like real platform output, but must be clearly marked as fixtures.
```

### 13.5 Research Report Review Format

Default report style:

```text
Markdown first, JSON companion second.
```

Reason:

- Markdown is easiest for the user to read quickly;
- JSON keeps the data machine-readable for later UI and tests;
- both should point to the same source IDs and observation IDs.

The report should be scan-first, not essay-first.

Top summary should include:

```text
Run goal
Platforms attempted
Candidates found
Sources harvested
Possible format observations
Review items
Tool setup gaps
Recommended next action
```

Every possible format observation should show:

```text
status
short name
evidence count
source examples
why it may be hot
why it may be tired / overused
uncertainties
next action
```

User-review emphasis:

- put high-value items near the top;
- mark personal/unknown creator assets clearly;
- mark official direct-use assets clearly;
- show why Kairove thinks something is a trend;
- do not bury ToolSetupItems at the bottom if they block future work.

---

## 14. P1 User-Adjustable Knobs

These should be config values, not hardcoded constants.

```json
{
  "p1": {
    "max_candidates_total": 300,
    "max_harvested_sources_total": 60,
    "max_format_observations": 20,
    "store_raw_snapshots_for_important_sources": true,
    "store_raw_snapshots_for_all_sources": false,
    "default_platform_order": ["search", "bilibili", "youtube", "wiki_official", "douyin_xhs_probe"],
    "manual_seed_enabled": true,
    "manual_seed_is_primary": false,
    "live_network_tests_enabled_by_default": false
  }
}
```

Important rule:

```text
The user should be able to see these values in reports and adjust them later.
```

---

## 15. P1 Ready-To-Code Checklist

P1 should not start coding until these are accepted or deliberately changed:

- web search + Bilibili are the first real implementation targets;
- YouTube is included after the first web/Bilibili path works;
- Douyin/XHS are capability probes at first;
- ManualSeedScout is auxiliary;
- default candidate cap is 300;
- default harvest cap is 60;
- raw snapshots are saved only for important sources by default;
- Markdown research report is primary;
- JSON data outputs mirror the Markdown report;
- fixture-first tests are required;
- live network tests are optional.

---

## 16. Current P1 Planning Status

Current status:

```text
P1 default decisions: drafted
P1 implementation brief: drafted
P1 implementation: not started
```

Next discussion target:

```text
Review whether these P1 defaults are acceptable, then either adjust them or move back to Phase 0 implementation planning.
```
