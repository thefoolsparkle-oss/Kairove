# Kairove Format Miner and Trend Analyst Brief

## 0. Status

This is a capability implementation brief, not a confirmed numbered phase.

Current status:

```text
Capability area: drafted
Global phase number: not assigned
Implementation: not started
Code writing: not allowed until the user explicitly asks
```

Purpose:

```text
Define how Kairove turns source understanding into reusable video formats, then scores whether those formats are worth producing.
```

---

## 1. Why This Layer Matters

Format Miner and Trend Analyst are central Kairove brain layers.

Source Scout answers:

```text
What did Kairove find?
```

Video Understanding answers:

```text
What is inside each source?
```

Format Miner answers:

```text
What repeated format or reusable structure is emerging across sources?
```

Trend Analyst answers:

```text
Is this format hot, growing, usable, overdone, tired, or not worth making?
```

This layer must not just summarize videos. It must detect reusable structures and make the score explainable.

---

## 2. Inputs

Primary inputs:

- `UnderstandingReport` objects;
- `FormatObservation` objects from P1;
- source metadata;
- engagement metrics;
- comment summaries;
- platform/source type;
- publication timestamps;
- detected audio/music clues;
- detected script/caption clues;
- detected visual/style clues;
- prior `Format` memory;
- prior scorecards and feedback.

Optional inputs:

- user-provided examples;
- platform ranking pages;
- manually reviewed source labels;
- user adjustments to score weights;
- post-publish performance from previous jobs.

---

## 3. Outputs

Primary outputs:

```text
FormatCandidate
FormatCluster
FormatCard
FormatGenome
TrendScorecard
ScoreExplanationReport
FormatMemoryUpdate
ReviewItem when confidence is low or user judgement is needed
```

Filesystem outputs:

```text
runs/run_000001/format_mining/
  format_candidates.jsonl
  format_clusters.json
  format_cards/
    fmt_000001.json
    fmt_000001.md
  format_genomes/
    fmt_000001_genome.json
  trend_scorecards/
    trend_score_000001.json
    trend_score_000001.md
  reports/
    format_trend_review.md
```

Knowledge outputs:

```text
knowledge_base/formats/
  format_cards/
  format_genomes/
  evidence/
  score_history/
```

---

## 4. Format Miner Scope

Format Miner should identify reusable video formats, not just topics.

A format can be based on:

- repeated script structure;
- repeated relationship structure;
- repeated joke/punchline structure;
- repeated caption/subtitle format;
- repeated audio/music usage;
- repeated visual sequence;
- repeated editing rhythm;
- repeated role swap pattern;
- repeated character reenactment setup;
- repeated horror/abstract short-drama setup;
- repeated AI tool/style signature;
- repeated platform challenge or meme structure.

Examples:

```text
"couple denies affection -> evidence appears -> collapse reaction"
"anime/game characters reenact a real couple argument"
"one character calmly narrates while impossible visual events escalate"
"hot audio drives a sequence of short reaction cuts"
"horror short uses domestic normality -> one impossible detail -> hard cut"
```

---

## 5. Format Miner Pipeline

Recommended order:

```text
1. Collect eligible UnderstandingReports
2. Extract format signals
3. Normalize signals into comparable features
4. Cluster similar sources
5. Compare clusters to existing Format memory
6. Decide new format vs variant vs weak observation
7. Build FormatCard
8. Build FormatGenome
9. Attach evidence and confidence
10. Request review if confidence is low or source policy is unclear
11. Hand accepted format candidates to Trend Analyst
```

---

## 6. Format Signals

Format Miner should extract multiple signal groups.

### 6.1 Script Signals

Examples:

- repeated opening line;
- repeated denial/confession/reversal shape;
- repeated joke setup;
- repeated escalation ladder;
- repeated final punchline;
- repeated narration style;
- repeated subtitle phrase;
- repeated role labels.

### 6.2 Visual Signals

Examples:

- shot count;
- scene type;
- camera framing;
- recurring props;
- character positions;
- visual transformation;
- subtitle layout;
- cover style;
- color/lighting style;
- AI visual style clues.

### 6.3 Audio Signals

Examples:

- same song;
- same sound meme;
- same lyric fragment;
- same timing cue;
- same voice tone;
- same silence/drop moment;
- same SFX beat.

### 6.4 Structure Signals

Examples:

- intro -> setup -> reveal -> reaction -> payoff;
- split-screen comparison;
- before/after;
- question/answer;
- accusation/defense/exposure;
- normal scene/impossible detail/horror cut;
- comment-response format;
- ranking/list format.

### 6.5 Production Signals

Examples:

- likely AI video model;
- likely image model;
- likely text-to-speech or voice clone;
- likely editing template;
- whether Kairove can reproduce with available tools;
- whether missing tools should create ToolSetupItems.

---

## 7. FormatCandidate

A `FormatCandidate` is a possible format before clustering or confirmation.

Minimum fields:

```json
{
  "format_candidate_id": "fmt_cand_000001",
  "run_id": "run_000001",
  "source_id": "src_000001",
  "understanding_report_id": "understand_000001",
  "candidate_summary": "...",
  "signal_groups": {
    "script": [],
    "visual": [],
    "audio": [],
    "structure": [],
    "production": []
  },
  "confidence": "low | medium | high",
  "created_at": "..."
}
```

---

## 8. FormatCluster

A `FormatCluster` groups candidates that appear to share a reusable format.

Minimum fields:

```json
{
  "format_cluster_id": "fmt_cluster_000001",
  "run_id": "run_000001",
  "candidate_ids": [],
  "source_ids": [],
  "cluster_summary": "...",
  "shared_signals": [],
  "variant_signals": [],
  "evidence_count": 0,
  "source_diversity": {
    "platform_count": 0,
    "creator_count": 0,
    "time_span_days": 0
  },
  "cluster_confidence": "weak | promising | strong",
  "recommended_action": "create_new_format | attach_to_existing | collect_more | reject"
}
```

---

## 9. New Format vs Existing Variant

Format Miner must avoid creating duplicates.

Compare each cluster against existing formats using:

- shared script structure;
- shared visual/editing rhythm;
- shared audio cue;
- shared relationship/role structure;
- shared audience recognition;
- shared production route;
- historical evidence.

Decision values:

```text
new_format
variant_of_existing
weak_observation
not_a_format
needs_more_sources
```

Rules:

- if structure is the same but characters/world/style differ, usually variant;
- if only topic is similar but structure differs, not the same format;
- if only one source exists and no repetition evidence exists, weak observation;
- if comments explicitly identify it as a meme/template/challenge, confidence increases;
- if repeated sources are all from one uploader only, confidence is lower unless engagement strongly supports spread.

---

## 10. FormatCard

A `FormatCard` is the human-readable and machine-readable representation of a confirmed or candidate format.

Minimum JSON fields:

```json
{
  "format_id": "fmt_000001",
  "format_status": "candidate | active | watchlist | rejected | retired",
  "short_name": "...",
  "one_sentence_summary": "...",
  "format_type": "script | visual | audio | editing | character_reenactment | horror | abstract_short | hybrid",
  "core_loop": "...",
  "required_elements": [],
  "optional_elements": [],
  "forbidden_or_fragile_elements": [],
  "typical_duration_range": "context_dependent",
  "source_ids": [],
  "evidence_summary": "...",
  "known_variants": [],
  "recommended_transfer_targets": [],
  "recommended_routes": [],
  "production_difficulty": "low | medium | high | unknown",
  "confidence": 0.0,
  "created_at": "...",
  "updated_at": "..."
}
```

Markdown version should show:

```text
What the format is
Why Kairove thinks it is a format
Evidence examples
Reusable structure
What can be changed
What should not be changed
Possible transfer targets
Production concerns
Trend score summary
```

---

## 11. FormatGenome

A `FormatGenome` is the deeper structural representation used for transfer and reproduction.

Minimum fields:

```json
{
  "format_id": "fmt_000001",
  "beats": [
    {
      "beat_id": "beat_01",
      "function": "setup | escalation | reveal | reaction | payoff",
      "description": "...",
      "required": true,
      "timing_hint": "...",
      "replaceable_parts": [],
      "non_replaceable_parts": []
    }
  ],
  "roles": [],
  "relationship_pattern": "...",
  "visual_pattern": "...",
  "audio_pattern": "...",
  "caption_pattern": "...",
  "editing_pattern": "...",
  "transfer_rules": [],
  "failure_risks": []
}
```

The genome should make semantic transfer possible later.

Example transfer logic:

```text
真人情侣嘴硬短剧 -> 二游/动漫 CP 角色替换
```

The exact characters, fandom, style, and production route are not decided by Format Miner. It only preserves the reusable pattern.

---

## 12. Trend Analyst Scope

Trend Analyst scores a format's production opportunity.

It must distinguish:

```text
popular and still worth using
popular but already tired
small but growing fast
large but negative sentiment
niche but very transferable
hot but impossible with current tools
```

It should never output only one number without explanation.

---

## 13. Trend Score Dimensions

Positive dimensions:

```text
heat_score
velocity_score
engagement_quality
remixability
format_strength
transfer_potential
production_feasibility
audience_fit
freshness
```

Penalty dimensions:

```text
fatigue_penalty
overdone_penalty
negative_sentiment_penalty
production_risk_penalty
tool_gap_penalty
source_confidence_penalty
platform_unsuitability_penalty
```

User preference:

```text
heat_score and velocity_score should usually have higher weight.
```

But the system must show all weights and allow later adjustment.

---

## 14. Default Score Profile

Default `trend_video_v1` profile:

```yaml
score_profile_id: trend_video_v1
profile_type: trend
version: 1.0
positive:
  heat_score: 0.22
  velocity_score: 0.22
  engagement_quality: 0.14
  remixability: 0.12
  format_strength: 0.11
  transfer_potential: 0.09
  production_feasibility: 0.06
  audience_fit: 0.03
  freshness: 0.01
penalties:
  fatigue_penalty: -0.12
  overdone_penalty: -0.08
  negative_sentiment_penalty: -0.10
  production_risk_penalty: -0.06
  tool_gap_penalty: -0.05
  source_confidence_penalty: -0.04
  platform_unsuitability_penalty: -0.03
```

Notes:

- heat and velocity are intentionally high;
- fatigue and overdone penalties matter, but they should not automatically kill a format if audience response is still strong;
- weights are defaults, not permanent truth;
- every scorecard stores the profile version used.

---

## 15. Heat vs Overdone Logic

Trend Analyst must not confuse high repetition with fatigue.

High repetition can be positive when:

- many independent creators are using the format;
- engagement remains strong;
- comments are positive or participatory;
- variants keep appearing;
- audience asks for more versions;
- new fandoms/characters/styles keep adapting it.

High repetition can be negative when:

- comments call it tired, boring, or overused;
- engagement is falling across newer examples;
- creators repeat it with little variation;
- audience sentiment becomes mocking or hostile;
- watch/like/comment ratios decline;
- the format depends on a joke whose surprise is gone.

Trend Analyst should output both:

```text
popularity_reason
fatigue_reason
```

This lets the user understand whether a crowded format is still worth using.

---

## 16. TrendScorecard

Minimum JSON fields:

```json
{
  "scorecard_id": "trend_score_000001",
  "format_id": "fmt_000001",
  "run_id": "run_000001",
  "score_profile_id": "trend_video_v1",
  "score_profile_version": "1.0",
  "positive_scores": {
    "heat_score": {
      "score": 0.0,
      "weight": 0.22,
      "weighted": 0.0,
      "evidence": []
    }
  },
  "penalties": {
    "fatigue_penalty": {
      "score": 0.0,
      "weight": -0.12,
      "weighted": 0.0,
      "evidence": []
    }
  },
  "final_score": 0.0,
  "confidence": "low | medium | high",
  "decision": "make_video | observe | collect_more | reject | ask_user",
  "reason": "...",
  "created_at": "..."
}
```

Mandatory rule:

```text
Every score must show raw score, weight, weighted contribution, and evidence.
```

---

## 17. Decision Thresholds

Default thresholds:

```yaml
decision_thresholds:
  make_video: 7.2
  observe: 5.5
  collect_more: 4.0
  reject_below: 4.0
```

Overrides:

- if source confidence is low, decision can become `collect_more` even when score is high;
- if tool gap is severe, decision can become `ask_user` or `observe`;
- if user specifically asks to make a format, Trend Analyst should still score it but not block automatically;
- if official/source policy review is needed, decision should create ReviewItem.

---

## 18. Agent Structure

Format Miner should be a council, not one monolithic prompt.

Suggested sub-agents:

```text
ScriptStructureMiner
VisualPatternMiner
AudioPatternMiner
EditingRhythmMiner
RoleRelationshipMiner
FormatClusterer
ExistingFormatMatcher
VariantJudge
FormatGenomeWriter
FormatEvidenceAuditor
```

Trend Analyst sub-agents:

```text
HeatEstimator
VelocityEstimator
EngagementQualityJudge
SentimentFatigueJudge
RemixabilityJudge
ProductionFeasibilityJudge
ToolGapJudge
ScorecardBuilder
ScoreProfileAuditor
```

Order:

```text
Format signal extraction -> clustering -> existing format matching -> format card/genome -> scoring -> score audit -> Regent gate
```

Agents should disagree visibly when needed.

Disagreement output:

```json
{
  "disagreement_type": "format_match | fatigue | feasibility | sentiment | score_weight",
  "positions": [],
  "recommended_resolution": "use_stronger_model | collect_more_sources | ask_user | proceed_with_low_confidence"
}
```

---

## 19. Growth and Learning

Format Miner must grow over time.

It should learn:

- known formats;
- variants;
- formats that worked;
- formats that failed;
- transfer routes that succeeded;
- tool routes that failed;
- audience fatigue patterns;
- score profiles that over/under-estimated results.

But it must not silently change core score weights.

Learning update types:

```text
observation
suggestion
approved_rule
```

Weight changes require user approval.

---

## 20. Reports

Format/Trend review report:

```text
runs/run_000001/format_mining/reports/format_trend_review.md
```

Report structure:

```text
1. Summary
2. Candidate formats found
3. New formats vs variants
4. Evidence table
5. Format cards
6. Trend scorecards
7. Heat vs fatigue explanation
8. Recommended make/observe/reject list
9. Weight profile used
10. Low-confidence items
11. ReviewItems created
12. Suggested next data collection
```

The user should be able to see:

- why a format exists;
- why it scored high or low;
- which weights mattered;
- whether it is hot or already tired;
- what evidence is weak;
- what can be adjusted later.

---

## 21. Fixture Test Plan

Fixture folders:

```text
tests/fixtures/format_trend/
  understanding_reports_cluster_01.jsonl
  format_observations_sample.jsonl
  existing_formats_sample.json
  comment_sentiment_sample.json
  engagement_metrics_sample.json
  score_profile_trend_video_v1.yaml
  expected_format_card_sample.json
  expected_trend_scorecard_sample.json
```

Test cases:

- repeated script sources cluster into one format;
- same structure with different characters becomes variant;
- same topic with different structure does not merge;
- one-source evidence remains weak observation;
- high repetition with positive comments scores as opportunity;
- high repetition with negative comments scores as fatigue;
- scorecard exposes raw score, weight, weighted contribution, and evidence;
- changing score profile version can recalculate without mutating old scorecard;
- low source confidence creates collect_more or ReviewItem;
- severe tool gap changes decision to ask_user or observe.

---

## 22. Non-Goals

This capability brief does not implement:

- source crawling;
- video downloading;
- video generation;
- asset resolution;
- semantic transfer execution;
- quality judging;
- publishing;
- full UI weight editor.

It defines the data and logic needed before those steps.

---

## 23. Acceptance Criteria

This capability is ready when Kairove can:

1. read multiple UnderstandingReports;
2. extract script, visual, audio, structure, and production signals;
3. group similar sources into FormatClusters;
4. decide new format vs variant vs weak observation;
5. create FormatCards;
6. create FormatGenomes;
7. compare against existing format memory;
8. produce TrendScorecards with visible weights;
9. distinguish popularity from fatigue;
10. show why repeated videos are good or bad evidence;
11. recommend make/observe/collect_more/reject/ask_user;
12. create review items for low confidence or policy uncertainty;
13. write a readable Format/Trend review report;
14. pass fixture tests.

---

## 24. Ready-To-Schedule Checklist

Before this capability becomes an implementation phase, decide:

- whether it should be one phase or split into Format Miner and Trend Analyst phases;
- whether P1 must be complete first;
- how many UnderstandingReports are required for the first real run;
- whether comment sentiment is required or optional at first;
- whether score profile editing happens by config file first or UI later;
- whether format memory is stored in SQLite, files, or both.

Until then, this remains a prepared capability brief, not a numbered phase.