# Kairove Phase 1: Trend and Source Intelligence Foundation

## Latest P1 Status Correction - 2026-06-12

| Scope | Skeleton | Live capability | Acceptance |
| --- | --- | --- | --- |
| confirmed | implemented and verified | public metadata/evidence live scouts connected for Search/Bilibili/YouTube/Wiki; Douyin/XHS probe-only | public metadata P1 acceptance complete with declared gaps |

The current P1 runtime proves the public metadata/evidence source intelligence foundation: query plan, live/fixture/manual candidate normalization, broad Search/Bilibili/YouTube/Wiki public metadata scouts, Douyin/XHS capability probes, source manifests, cover evidence, public HTML snapshots, unauthenticated browser screenshots, EvidenceObservations, Understanding Reports, weak Format Observation, TrendOpportunityPacket, research review report, and self-check report.

It does **not** mean platform deep-content automation is complete. Douyin/Xiaohongshu remain capability-probe and semi-automatic entry points unless login/API/browser setup is explicitly available. Comments/danmaku, transcript/audio analysis, video frame sampling/download, and logged-in recommendation context remain declared gaps.

P1 correction:

```text
P1 must not stop at URL discovery.
P1 owns the evidence viewing / page observation layer before Understanding Report v1.
P2 must only consume evidence-backed P1 outputs; P2 should not repair missing P1 evidence by doing source harvesting itself.
```

## 0. Purpose

Phase 1 teaches Kairove how to see the outside world.

It is not a video generation phase.
It is not a manual-link-only phase.
It is not the first complete production line.

Phase 1 builds the autonomous trend/source intelligence foundation that later production lines depend on.

---

## 1. Important Concept Split

Do not confuse these two things:

```text
Development Phase:
  A staged implementation step.

Production Line:
  A complete usable video-making pipeline.
```

Phase 0 is confirmed as P0-B: the lowest complete ordinary AI video production chain.

P0-B can start from an approved source or manual seed and carry one project through prompt package, manual generation slot, candidate registration, basic QA, packaging, and manual publish package.

Phase 1 is different. It does not replace P0-B and does not generate videos. It upgrades the front of the system so Kairove can autonomously discover what is currently worth making.

P1 is confirmed as the Phase 1 scope. The later layers below are dependency areas, not accepted phase numbers:

```text
foundation
trend/source intelligence
format understanding and scoring
reproduction planning
asset resolution
generation
quality/retry
packaging/publishing
```

The exact later phases are not fixed yet. This file defines the confirmed P1 scope.

---

## 2. Phase 1 Goal

Phase 1 goal:

```text
Kairove can autonomously find external video/source candidates, collect usable evidence, produce structured source understanding, and create early format observations for user review.
```

In plain language:

```text
Kairove should begin to find out what people are currently making.
```

---

## 3. Phase 1 Non-Goals

P1 must not implement:

- video generation;
- AI video model calls for production;
- full Format Miner;
- full Trend Analyst;
- full script/council production;
- MMD/3D;
- platform publishing;
- longform production;
- full Web UI;
- fake platform APIs.

P1 can create reports and structured observations, but it should not produce final videos.

---

## 4. P1 Main Principle

Manual seed support is useful, but it is not the main route.

Main route:

```text
Kairove searches and scouts by itself.
```

Manual seed route:

```text
User-provided links help debugging, calibration, and special cases.
```

Therefore:

```text
ManualSeedScout = auxiliary feature
Autonomous scouts = P1 core
```

---

## 5. P1 Workstreams

P1 is large. It should be discussed and implemented as workstreams, not pretending each workstream is a separate phase.

Suggested P1 workstreams:

```text
P1-A Autonomous Query Planner
P1-B SearchEngineScout
P1-C BilibiliScout v1
P1-D YouTubeScout v1
P1-E Wiki / Official Source Scout
P1-F Douyin / Xiaohongshu Capability Probe
P1-G ManualSeedScout auxiliary
P1-H Harvester v1
P1-I Evidence Viewing / Evidence Observation v1
P1-J Understanding Report v1
P1-K Format Observation v1
P1-L Research Review Report
```

---

## 6. P1-A Autonomous Query Planner

### Objective

Generate search plans automatically.

Kairove should not wait for the user to provide exact keywords.

### Inputs

- broad user goal;
- platform list;
- content categories;
- known user preferences;
- existing format memory;
- current date/time;
- optional target fandom/character/audio.

### Query Types

The planner should generate:

- general trend queries;
- platform-native terms;
- fandom-specific terms;
- AI video terms;
- meme/short drama terms;
- music/sound trend terms;
- official/wiki source queries;
- related-video expansion queries.

### Example Output

```json
{
  "query_plan_id": "query_plan_000001",
  "goal": "find currently popular abstract AI short video formats",
  "queries": [
    {
      "platform": "search",
      "query": "最近 爆火 AI 短视频 抽象 短剧",
      "purpose": "broad web discovery"
    },
    {
      "platform": "bilibili",
      "query": "AI 抽象 短剧",
      "purpose": "platform video search"
    },
    {
      "platform": "youtube",
      "query": "AI horror shorts trend",
      "purpose": "global AI video trend search"
    }
  ]
}
```

### Acceptance

The planner can generate a list of platform-specific search tasks from a broad goal.

---

## 7. P1-B SearchEngineScout

### Objective

Use general web search to find:

- hot video discussions;
- trend articles;
- official pages;
- wiki pages;
- creator/platform pages;
- videos indexed by search;
- AI tool clues.

### Why It Matters

SearchEngineScout is broad and resilient. It can find sources even when platform-specific access is limited.

### Outputs

Normalized SourceCandidates:

```json
{
  "candidate_source_id": "cand_src_000001",
  "platform": "search",
  "url": "...",
  "title": "...",
  "content_type": "article | video | wiki_page | topic_page | unknown",
  "source_type_guess": "official | wiki | personal_creator | unknown",
  "discovery_reason": ["web_search", "trend_query"]
}
```

### Acceptance

Given a query plan, SearchEngineScout returns normalized candidates and records the query used.

---

## 8. P1-C BilibiliScout v1

### Objective

Find B站 video candidates from search and basic public metadata.

### P1 Scope

Implement:

- keyword search where technically available;
- manual B站 URL ingestion;
- title/author/link/cover/metrics if available;
- source type guess;
- candidate normalization.

Do not require:

- complete comment crawling;
- danmaku crawling;
- full video download;
- automated login.

### Candidate Signals

Important signals:

- title;
- tags;
- view count;
- like/favorite/comment indicators if available;
- upload time;
- uploader;
- cover;
- repeated title phrases;
- AI/video/meme keywords.

### Acceptance

BilibiliScout can produce SourceCandidates from keyword search or manual B站 URLs.

---

## 9. P1-D YouTubeScout v1

### Objective

Find YouTube/Shorts candidates and broader global AI video trend clues.

### P1 Scope

Implement:

- keyword search via available web/API route;
- title/channel/link/metrics if available;
- candidate normalization;
- Shorts detection where possible.

### Important Uses

- AI video trend examples;
- horror/visual style trends;
- tool usage clues;
- longform references later.

### Acceptance

YouTubeScout can produce normalized candidates and record capability gaps if API is missing.

---

## 10. P1-E Wiki / Official Source Scout

### Objective

Find official and wiki references for characters, worlds, visual assets, and background knowledge.

### Sources

- official game/anime websites;
- official accounts;
- official PV pages;
- public wiki;
- fandom pages;
- encyclopedic pages.

### P1 Output

```json
{
  "candidate_source_id": "cand_src_000020",
  "platform": "wiki",
  "url": "...",
  "title": "...",
  "content_type": "wiki_page",
  "source_type_guess": "official | wiki",
  "discovery_reason": ["character_reference_search"]
}
```

### Current User Policy

Official assets can be direct-use.

Personal creator and unknown sources require review for direct use.

### Acceptance

Given a character/world/topic query, the scout can find candidate official/wiki sources and classify source type with confidence.

---

## 11. P1-F Douyin / Xiaohongshu Capability Probe

### Objective

Do not block P1 on difficult platforms, but detect what is possible.

For Douyin and Xiaohongshu, P1 should first implement capability probing:

```text
Can we search?
Can we access metadata?
Can we fetch comments?
Can we capture screenshots?
Does it require login?
Does it require API?
Does browser automation look necessary?
```

### Output

```json
{
  "platform": "douyin",
  "capabilities": {
    "search": "requires_browser_or_api",
    "metadata": "partial",
    "comments": "requires_auth",
    "download_video": "limited"
  },
  "missing_setup": [
    "login/session",
    "official API or browser automation"
  ]
}
```

### Acceptance

Kairove can report what is missing and create ToolSetupItems.

No fake Douyin/XHS API implementation is allowed.

---

## 12. P1-G ManualSeedScout Auxiliary

### Objective

Accept user-provided URLs or local files as seeds.

### Role

Manual seed is auxiliary:

- debugging;
- calibration;
- special user-selected videos;
- hard-to-access platform videos;
- examples for Format Miner.

It is not P1's main route.

### Acceptance

Given a URL, ManualSeedScout creates a SourceCandidate and preserves user notes.

---

## 13. P1-H Harvester v1

### Objective

Turn SourceCandidates into Sources and Assets with provenance.

### Harvest Levels

```text
metadata_only:
  title, URL, author, metrics, platform, collected_at.

snapshot:
  metadata + page snapshot or cover/screenshot.

analysis_pack:
  metadata + cover/screenshots/comments/transcript/audio reference if available.
```

### P1 Minimum

P1 must support:

- metadata harvest;
- source manifest;
- asset manifest if any file is saved;
- failure recording.

### P1 Preferred

Where possible:

- cover/screenshot;
- comments sample;
- transcript if platform provides it;
- audio metadata.

### Acceptance

For each selected candidate, Kairove creates a Source record and a source manifest.

---

## 14A. P1-I Evidence Viewing / Evidence Observation v1

### Objective

P1 must record what the system has actually seen before it claims to understand a source.

This layer sits between Harvester v1 and Understanding Report v1:

```text
SourceCandidate
-> Source manifest
-> EvidenceObservation
-> Understanding Report
-> Format Observation
```

### EvidenceObservation Minimum Fields

```json
{
  "evidence_observation_id": "evidenceobs_000001",
  "source_id": "src_000001",
  "candidate_source_id": "sourcecand_000001",
  "platform": "youtube",
  "url": "...",
  "evidence_mode": "live_metadata | fixture | manual_seed | browser_assisted_metadata",
  "metadata_source": "youtube_data_api_v3_search | bilibili_public_web_search_api | ...",
  "available_inputs": ["url", "title", "description", "cover_url", "cover_file", "page_snapshot_file", "page_metadata"],
  "missing_inputs": ["page_screenshot", "video_frames", "transcript", "comments", "audio_metadata", "full_video_content"],
  "observed_text": {"page_metadata": {}},
  "observed_visual": {"page_snapshot_file": null},
  "observed_metrics": {},
  "understanding_limits": [],
  "next_evidence_needed": [],
  "requires_review": true
}
```

Current detail metadata sources may include:

```text
YouTube:
  search.list for candidate discovery
  videos.list for title, channel, published_at, description, tags, thumbnail URL, duration, caption flag, and basic statistics

Bilibili:
  public web search metadata for candidate discovery
  public x/web-interface/view metadata for title, owner, description, cover URL, duration, dimensions, pages, and basic statistics
```

These are still metadata observations, not full viewing of video content.

If `research.download_reference_assets` is `allow` or `allow_with_limits`, P1 may save small cover/thumbnail images as `analysis_only` research assets. This is a lightweight evidence upgrade for packaging and visual-reference observation only. It still does not count as video viewing, frame sampling, transcript access, comment collection, or media download.

If `research.collect_metadata` is `allow` or `allow_with_limits`, P1 may save a small public HTML page snapshot and extracted page metadata (`title`, `description`, `og:*`, `twitter:*`) when the source URL is openly reachable. It may also extract a limited set of public visible text snippets from the saved HTML. This is public page metadata/text evidence only. It is not a browser screenshot, logged-in view, comment capture, video frame sample, transcript, or full content verification.

If `research.browser_screenshot` is `allow` or `allow_with_limits` and a browser runtime is available, P1 may save one public browser screenshot per harvested source. This screenshot must use a fresh unauthenticated browser context with no login cookies. P1 records basic screenshot quality metadata such as dimensions, file size, and a nonblank score so blank/error screenshots can be downgraded. It is visual page evidence only; it is not video frame sampling, not comment capture, not logged-in recommendation context, and not proof that the video content was watched.

### Acceptance

P1 can only create an Understanding Report from an EvidenceObservation.

If P1 has only metadata, the Understanding Report must say so and remain weak. It must not claim visual rhythm, exact format structure, audio, comments, or plot beats unless those inputs exist.

---

## 14B. P1-J Understanding Report v1

### Objective

Produce a structured summary sufficient for early format observation.

P1 Understanding Report can be incomplete, but it must not hallucinate missing data.

### Schema

```json
{
  "source_id": "src_000001",
  "summary": "...",
  "content_type_guess": ["dialogue_meme", "music_sync", "horror", "ai_visual_style"],
  "text_signals": {
    "title_keywords": [],
    "description_keywords": [],
    "visible_text": [],
    "transcript_summary": null
  },
  "visual_signals": {
    "style_guess": "...",
    "subject_guess": "...",
    "subtitle_style_guess": "...",
    "ai_generated_likelihood": null
  },
  "audio_signals": {
    "has_music": null,
    "music_or_sound_role": "...",
    "beat_or_hook_notes": []
  },
  "story_or_format_clues": {
    "roles": [],
    "beats": [],
    "hook": null,
    "punchline": null,
    "repeatable_parts": []
  },
  "confidence": 0.0,
  "missing_inputs": []
}
```

### Acceptance

For each harvested source, Kairove can produce an understanding report with confidence and missing input fields.

---

## 15. P1-J Format Observation v1

### Objective

Create early observations that some sources may share a format.

This is not full Format Miner.

### Output

```json
{
  "observation_id": "fmt_obs_000001",
  "candidate_format_name": "嘴硬不抽卡",
  "evidence_sources": ["src_000001", "src_000002"],
  "shared_signals": [
    "denial -> evidence -> collapse",
    "fast subtitles",
    "gacha topic"
  ],
  "possible_routes": [
    "script_council",
    "character_reenactment_council"
  ],
  "confidence": 0.68,
  "needs_more_sources": true
}
```

### P1 Behavior

P1 may produce:

- weak observation;
- watchlist item;
- "needs more sources";
- "not enough evidence".

Do not overstate confidence.

---

## 16. P1-K Research Review Report

### Objective

Generate a human-readable run report.

Output file:

```text
reports/run_000001_research_review.md
```

Report sections:

```text
1. Run summary
2. Queries used
3. Platforms checked
4. Source candidates found
5. Sources harvested
6. Harvest failures
7. Possible repeated formats
8. Official assets found
9. Personal/unknown assets needing review
10. Tool/API/login gaps
11. Recommended next actions
```

### Acceptance

User can read the report and understand what Kairove found without opening raw JSON.

---

## 17. P1 Data Outputs

P1 should create:

```text
source_candidates
sources
assets
source manifests
asset manifests
understanding reports
format observations
tool setup items
decision logs
review items
research review report
```

No video candidates are produced in P1.

---

## 18. P1 Acceptance Criteria

P1 is ready when Kairove can:

1. Start an autonomous trend/source run.
2. Generate search/query plans.
3. Search at least broad web plus one or two initial platforms.
4. Produce normalized SourceCandidates.
5. Deduplicate and rank candidates.
6. Harvest metadata and manifests.
7. Produce EvidenceObservations that record what was actually visible and what remains missing.
8. Save available evidence files when possible.
9. Assign source type and usage policy.
10. Record platform/API/login failures.
11. Produce Understanding Reports from EvidenceObservations only.
12. Produce early Format Observations.
13. Generate a human-readable Research Review Report.
14. Create ToolSetupItems for missing platform capability.
15. Treat ManualSeedScout as auxiliary, not the main route.

---

## 19. P1 Non-Acceptance

P1 is not acceptable if:

- it only works from manual URLs;
- it mixes research/local/generated assets;
- it loses source provenance;
- it silently fails platform access;
- it writes fake API outputs;
- it claims a full format with weak evidence;
- it generates video before the source intelligence layer is stable.

---

## 20. Open Questions Before Coding P1

These must be discussed:

1. Which first platform besides web search should be prioritized: B站 or YouTube?
2. How aggressive should initial web searching be?
3. Should P1 store raw HTML snapshots or only metadata at first?
4. Which source types count as official automatically?
5. What minimum evidence is needed for a Format Observation?
6. How should P1 handle Douyin/XHS manual/browser-only cases?
7. What should the first research review report look like?
---

## 21. Recommended Answers to P1 Open Questions

These answers are the current planning defaults. They are not implementation code and can be changed before P1 begins.

### 21.1 First Platform Priority

Default order:

```text
1. Broad web search
2. Bilibili
3. YouTube
4. Wiki / official source pages
5. Douyin / Xiaohongshu capability probe
```

Reason:

- broad web search gives resilience and can discover pages outside platform search;
- Bilibili is more important for Chinese anime/game/meme/short-video culture;
- YouTube is useful for global AI-video techniques and English trend clues;
- wiki/official pages are needed for character references, official assets, and source verification;
- Douyin/XHS are important but may need browser/manual/import workflows first, so P1 should detect capability gaps instead of pretending full API support exists.

### 21.2 Search Aggressiveness

P1 should be autonomous but capped.

Use three search rounds:

```text
Round 1: broad discovery queries
Round 2: related query expansion from promising candidates
Round 3: freshness and evidence checks for likely formats
```

Each run should record:

- queries attempted;
- platform searched;
- result count;
- candidates accepted;
- candidates rejected;
- why each expansion happened.

P1 should avoid endless crawling. If a run needs more evidence, it creates a follow-up recommendation instead of silently expanding forever.

### 21.3 Raw Snapshot Policy

Default:

```text
Store structured metadata for all candidates.
Store raw snapshots only for important, unstable, or review-worthy sources.
```

Raw snapshots are useful for later auditing, but storing every page immediately creates noise and storage pressure.

Important sources include:

- likely format roots;
- official pages;
- high-engagement trend examples;
- pages with comments or metadata that affect scoring;
- sources likely to disappear or change.

### 21.4 Automatic Official Source Rules

A source can be treated as official when at least one of these is true:

- it is from a verified official account;
- it is from an official domain controlled by the IP/project/company;
- it is a platform page clearly marked as official;
- it is an official game/anime/music/video release page;
- it is a wiki page used only as reference, not as direct asset authority.

If official status is uncertain, create a ReviewItem instead of guessing.

### 21.5 Minimum Evidence for Format Observation

P1 should not claim a full format too early.

A Format Observation can be created when there is at least one of these:

```text
A. 3+ similar source candidates from independent uploads/pages
B. 1 very strong source plus related examples/comments showing repetition
C. 1 source explicitly connected to a known recurring template/challenge/trend
```

Confidence labels:

```text
weak_observation
promising_observation
strong_observation
needs_more_sources
```

P1 should use weak labels freely. Full Format objects belong later.

### 21.6 Douyin / Xiaohongshu Handling

P1 should treat Douyin and Xiaohongshu as capability probes first.

Allowed P1 results:

- browser-searchable metadata;
- manually imported links;
- screenshots or exported page evidence if the user provides them;
- ToolSetupItems for login/API/browser automation gaps;
- notes about access restrictions.

Not allowed:

- fake API outputs;
- pretending full crawling works;
- making hidden platform assumptions without evidence.

### 21.7 Research Review Report Shape

The P1 review report should be useful without opening raw JSON.

Recommended structure:

```text
1. What this run tried to find
2. What platforms were searched
3. Query list and expansion reasons
4. Best source candidates
5. Harvested sources and saved evidence
6. Possible repeated formats
7. Official assets found
8. Personal/unknown assets needing review
9. Platform/tool/API gaps
10. Recommended next run
```

Each possible format should show:

- short description;
- evidence count;
- confidence label;
- source examples;
- why it may be worth following;
- what is still uncertain.

---

## 22. P1 Workstream Order

P1 workstreams are not mutually exclusive, but implementation should follow this order:

```text
1. Lock P1 data contracts and output folders
2. Build Autonomous Query Planner
3. Build SearchEngineScout
4. Build BilibiliScout v1
5. Build Harvester v1 and source manifests
6. Build Understanding Report v1
7. Add YouTubeScout v1
8. Add Wiki / Official Source Scout
9. Add Douyin / XHS capability probe
10. Add ManualSeedScout auxiliary route
11. Build Format Observation v1
12. Build Research Review Report
13. Add replay tests and fixture-based tests
```

Reasoning:

- query planning must exist before autonomous scouts are useful;
- broad web search should come before platform-specific fragility;
- Bilibili is the first high-value platform for this project;
- harvester and manifests must appear before deeper understanding;
- manual seed support should not become the main architecture;
- report generation should come after the pipeline can produce enough evidence.

---

## 23. P1 Planning Status

Current status:

```text
P1 scope: confirmed
P1 default answers: accepted
P1 implementation: public metadata/evidence foundation completed and verified
P1 live capability: Search/Bilibili/YouTube/Wiki public metadata scouts connected; Douyin/XHS probe-only
P1 acceptance: public metadata P1 acceptance complete with declared gaps
P1 confirmation: accepted by user
P1 implementation mode: one continuous P1 batch
```

Current implementation result:

```text
P1 can create query plans, record scout capability gaps, produce fixture/live/manual normalized SourceCandidates, harvest metadata/evidence Sources, save cover evidence, public HTML snapshots, unauthenticated browser screenshots, create EvidenceObservations, create Understanding Reports, create weak Format Observations, create TrendOpportunityPackets, write Research Review Reports, and write P1 self-check reports.
No live platform/API results are claimed in offline fixture mode.
```

Future changes to P1 scope should edit section 34 before coding changes are made.

---

## 24. P1 Implementation Contract (Merged)

Merged from `PHASE1_IMPLEMENTATION_BRIEF.md`.

P1 is confirmed in scope and implemented for the public metadata/evidence acceptance chain. Deep-content platform automation remains a declared gap.

Core outputs:

```text
runs/run_000001/query_plans/
runs/run_000001/scout_results/
runs/run_000001/source_candidates/
runs/run_000001/harvested_sources/
runs/run_000001/understanding_reports/
runs/run_000001/format_observations/
runs/run_000001/reports/research_review.md
```

Primary data contracts:

```text
QueryPlan
ScoutResult
SourceCandidate
Source
SourceManifest
UnderstandingReport
FormatObservation
ResearchReviewReport
```

Default implementation order:

```text
QueryPlan
SearchEngineScout
BilibiliScout v1
Harvester v1
ResearchReviewReport v1
YouTubeScout v1
Wiki / Official Source Scout
Douyin/XHS capability probe
ManualSeedScout auxiliary
FormatObservation v1
```

Default limits:

```json
{
  "max_candidates_total": 300,
  "max_harvested_sources_total": 60,
  "max_format_observations": 20,
  "max_sources_per_format_observation": 12
}
```

Raw snapshot policy:

```text
Save structured metadata for candidates.
Save raw snapshots only for important, unstable, official, high-engagement, or review-worthy sources.
```

P1 ready-to-code checklist:

```text
web search + Bilibili first
YouTube after web/Bilibili path works
Douyin/XHS as capability probes first
ManualSeedScout auxiliary only
Markdown report primary, JSON companion second
fixture-first tests
live network tests optional
no video generation
```
---

## 25. P1 Candidate Scope Contract

P1 is the autonomous trend/source intelligence layer.

Purpose:

```text
Find current external video/source opportunities, collect evidence, detect repeated formats, score whether they are worth following, and hand usable opportunity packets to P0-B.
```

P1 answers this question:

```text
What should Kairove make next, and what evidence supports that choice?
```

P1 does not answer this question:

```text
How should the final video be generated and published?
```

That remains P0-B / production-chain work.

P1 confirmed candidate shape:

```text
autonomous search first
manual seed auxiliary
broad web + Bilibili first
YouTube after web/Bilibili path works
wiki/official pages for reference and source verification
Douyin/XHS capability probes first, full automation later
harvest metadata/evidence/snapshots where possible
cluster similar sources into early repeated-format observations
score opportunities with visible weights
write a human-readable research review report
handoff opportunity packets to P0-B
```

---

## 26. P1 Must Include

P1 must include these capabilities to be useful:

```text
Autonomous Query Planner:
  Generates search plans without waiting for user-provided links.

SearchEngineScout:
  Finds broad web evidence, trend articles, search-result pages, platform pages, official pages, wiki pages, and related examples.

BilibiliScout v1:
  Finds Bilibili candidates and basic public metadata when accessible.

YouTubeScout v1:
  Finds YouTube/Shorts candidates and global AI-video/tool/style clues.

Wiki / Official Source Scout:
  Finds character/world/reference pages and official source candidates.

Douyin / Xiaohongshu Capability Probe:
  Detects what can be searched, viewed, imported, or automated, and writes setup gaps.

ManualSeedScout Auxiliary:
  Allows user links, but never becomes the main route.

Harvester v1:
  Saves structured metadata and selected evidence with provenance.

Understanding Report v1:
  Summarizes source content and signals without hallucinating missing data.

Format Observation v1:
  Detects early repeated formats without claiming full Format Miner confidence.

Opportunity Scoring v1:
  Scores source/format opportunities with visible weights and recalculation support.

Research Review Report:
  Produces a readable report for user review and P0-B handoff.
```

P1 should prefer evidence over confidence. If it cannot access a platform, it should create a capability/setup item instead of guessing.

---

## 27. P1 Must Not Include

P1 must not implement:

```text
video generation
P0-B production execution
full Format Miner
full Trend Analyst
full script council
asset resolver full version
MMD/3D route
longform route
platform upload
post-publish metrics learning
self-applying learning rules
full local web console
fake platform APIs
```

P1 may create weak observations, early scores, and research reports. It must not claim that an opportunity is production-ready unless it has enough evidence and a clear handoff package for P0-B.

---

## 28. P1 Operating Flow

P1 should run in this order:

```text
1. Run starts with a research goal.
2. Autonomous Query Planner creates query rounds.
3. SearchEngineScout runs broad discovery.
4. BilibiliScout v1 searches high-value Chinese video candidates.
5. Candidate Normalizer converts results into SourceCandidates.
6. Deduplicator merges exact/near duplicates.
7. Initial Ranker picks candidates worth harvesting.
8. Harvester saves metadata, snapshots, screenshots, comments, or files when available.
9. Usage Policy Assigner labels official/personal/unknown/review-needed status.
10. Evidence Observation v1 records visible metadata/text/cover/screenshot/transcript availability and missing inputs.
11. Understanding Report v1 summarizes each source from EvidenceObservation only.
12. Similarity Grouper clusters likely repeated formats.
13. Format Observation v1 writes weak/promising/strong observations.
14. Opportunity Scoring v1 scores which observations are worth following.
15. Wiki / Official Source Scout enriches references when relevant.
16. YouTubeScout v1 adds global/AI-tool/style evidence.
17. Douyin/XHS Capability Probe records access and setup gaps.
18. ManualSeedScout handles user-provided links as auxiliary evidence.
19. Research Review Report summarizes findings.
20. P1 writes Opportunity Packets for P0-B.
```

The order is not mutually exclusive, but implementation should respect dependencies:

```text
query plan before scouts
normalized candidates before harvest
harvested evidence before understanding
evidence observation before understanding
understanding before format observation
format observation before opportunity scoring
opportunity packet before P0-B handoff
```

---

## 29. Trend Opportunity Packet

P1's main handoff object should be a `TrendOpportunityPacket`.

Purpose:

```text
Give P0-B enough context to start a production job from a selected opportunity without re-researching from zero.
```

Schema:

```json
{
  "opportunity_id": "opp_000001",
  "run_id": "run_000001",
  "title": "真人嘴硬情侣短剧 -> 二游 CP 可迁移格式",
  "opportunity_type": "repeated_script | music_trend | dance_trend | ai_video_style | horror_short | abstract_short_drama | meme_format | official_asset_hook",
  "confidence_label": "weak | promising | strong | needs_more_sources",
  "score_total": 7.8,
  "score_profile_id": "p1_opportunity_default_v1",
  "score_components": {},
  "evidence_sources": ["src_000001", "src_000002"],
  "representative_examples": [],
  "format_observation_id": "fmt_obs_000001",
  "understanding_report_ids": [],
  "why_it_matters": "...",
  "why_it_may_be_stale": "...",
  "comment_sentiment_summary": "...",
  "asset_and_reference_notes": [],
  "tool_or_ai_method_guess": [],
  "p0b_handoff_readiness": "ready | needs_more_evidence | needs_user_review | blocked_by_tool_gap",
  "recommended_p0b_start_mode": "approved_source | manual_seed | opportunity_packet",
  "review_items": [],
  "created_at": "..."
}
```

P1 does not create a production job automatically unless later permission allows it. It prepares the packet so P0-B can start cleanly.

---

## 30. Opportunity Scoring v1

P1 needs scoring, but not the full Trend Analyst.

Score components:

```text
heat:
  Current engagement / visibility.

growth:
  Whether the format/topic appears to be accelerating.

freshness:
  Whether it is early enough to use.

repetition_signal:
  Whether multiple videos are using the same script, sound, structure, dance, or plot.

comment_sentiment:
  Whether viewers are enjoying it, roleplaying with it, asking for variants, or complaining that it is stale.

fatigue_penalty:
  Whether it is already overused, disliked, or treated as a dead joke.

transferability:
  Whether it can be moved into another character/style/world without losing the hook.

asset_readiness:
  Whether usable references/assets/sounds/official materials are available or reviewable.

tool_readiness:
  Whether Kairove can plausibly reproduce the format with available/manual tools.

source_confidence:
  Whether evidence is strong, fresh, and traceable.
```

Default signed weights:

```json
{
  "heat": 0.18,
  "growth": 0.20,
  "freshness": 0.12,
  "repetition_signal": 0.12,
  "comment_sentiment": 0.12,
  "transferability": 0.10,
  "asset_readiness": 0.07,
  "tool_readiness": 0.06,
  "source_confidence": 0.08,
  "fatigue_penalty": -0.15
}
```

Important rule:

```text
Many similar videos can be positive or negative.
```

It is positive when:

```text
engagement is strong
comments are playful or asking for variants
the format is still growing
new creators are adapting it
```

It is negative when:

```text
comments call it stale
engagement is falling
similar videos are low-quality repeats
viewers complain about seeing it too much
```

All score weights must be visible, versioned, editable, and recalculable.

---

## 31. AI Tool / Method Guessing In P1

P1 should record possible AI tool or production-method clues when the source itself appears AI-generated.

Examples:

```text
likely text-to-video
likely image-to-video
likely video-to-video
likely voice clone / TTS
likely subtitle template
likely editing template
likely official PV edit
unknown AI method
```

Evidence can include:

```text
visible watermark
creator tags
caption text
comments mentioning tools
visual artifacts
motion style
platform/tool trend articles
linked workflow posts
```

Output:

```json
{
  "method_guess_id": "method_guess_000001",
  "source_id": "src_000001",
  "guesses": [
    {
      "method": "image_to_video",
      "confidence": 0.62,
      "evidence": ["caption mentions AI video", "short single-shot motion", "visual artifact pattern"],
      "kairove_tool_available": "unknown | available | not_configured | unavailable",
      "suggested_action": "check_tool_registry | create_tool_setup_item | try_existing_route | ask_user"
    }
  ]
}
```

P1 must not overclaim tool identity. If the method is uncertain, it should say uncertain and create a follow-up note.

---

## 32. Download And Evidence Policy For P1

P1 should save evidence when allowed and technically possible.

Evidence types:

```text
metadata
page snapshot
screenshot
thumbnail / cover image
caption / transcript if available
comment sample / sentiment summary
short clip or source video when allowed and technically possible
audio reference metadata
source URL and platform IDs
```

Storage rules:

```text
research evidence -> research_assets/
user-provided local material -> local_assets/
generated outputs -> generated_assets/
```

P1 must always record:

```text
source URL
platform
source type
official/personal/unknown classification
usage policy
review status
what was downloaded or saved
why it was saved
which report/opportunity used it
```

If download is not possible, P1 should still save metadata and create a capability gap item.

---

## 33. P1 Recommended Implementation Mode

P1 is confirmed in scope and implemented for the public metadata/evidence acceptance chain. Deep-content platform automation remains a declared gap.

Confirmed implementation mode:

```text
P1 was implemented as one continuous phase batch for the public metadata/evidence acceptance chain. Further deep-content source work requires explicit permission because it involves higher-risk capabilities.
P1-A through P1-K are internal implementation order, not separate phases.
ManualSeedScout remains auxiliary.
Do not stop after manual-link support.
```

Why:

```text
P1 only becomes useful when autonomous query planning, scouting, harvesting, observation, scoring, and review report all connect.
A manual-only partial P1 would violate the core project direction.
```

---

## 34. P1 Confirmed Scope Checklist

The following defaults are accepted as the confirmed P1 scope:

```text
P1 identity:
  Autonomous trend/source intelligence layer.

Core output:
  TrendOpportunityPacket for P0-B.

Initial platform order:
  broad web search -> Bilibili -> YouTube -> wiki/official pages -> Douyin/XHS capability probe.

ManualSeedScout:
  auxiliary only.

Scoring:
  Opportunity Scoring v1 with visible weights, not full Trend Analyst.

Format work:
  Format Observation v1, not full Format Miner.

Evidence policy:
  save structured metadata broadly, save raw/snapshot/download evidence selectively with provenance.

Implementation mode:
  one continuous P1 batch once confirmed.

Non-goals:
  no video generation, no publishing, no fake APIs.
```

P1 is marked confirmed. Future scope changes should revise this section before coding.

---

## Cross-Phase Policy Alignment - 2026-06-06

P1 must follow the accepted cross-phase source policy:

```text
Preferred automatic search/collection directions:
  general web search
  official sites
  wiki sources
  Bilibili
  YouTube

Douyin and Xiaohongshu:
  capability probes and semi-automatic entry points unless setup allows more.

Missing API/login/cookie/download capability:
  create ToolSetupItem.

Do not:
  bypass platform restrictions
  pretend unstable or unavailable data was collected
  require large-scale downloads or comment crawling by default

Allowed by default:
  metadata collection

Default ask:
  large-scale downloads
  comment crawling
  asset downloads
```

P1 scoring must treat hot-but-overused formats as follows:

```text
Do not automatically reject overused formats.
Reduce exact-copy weight and prefer variant entry points.
Continue riding the trend when comment sentiment, growth, and interaction quality remain strong.
Deduct or abandon when fatigue, negative sentiment, or declining growth is clear.
```
