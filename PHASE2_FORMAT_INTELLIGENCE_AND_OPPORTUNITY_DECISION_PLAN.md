# Kairove Phase 2: Format Intelligence and Opportunity Decision Plan

## 0. Status

Phase 2 is the planning document after confirmed Phase 1.

Current status:

```text
Phase 0: confirmed, P0-B Lowest Complete Production Chain, implementation not started
Phase 1: confirmed, Trend and Source Intelligence Foundation, implementation not started
Phase 2: detailed planning draft, not yet confirmed for implementation
P3-P11: detailed planning drafts exist, not confirmed for implementation
```

Phase 2 exists because the work starts after P1 and is not part of P1.

Phase 2 should be discussed and accepted before implementation. Until accepted, it is a detailed draft, not a coding instruction.

---

## 1. Purpose

P1 finds current opportunities. Phase 2 decides which of those opportunities are strong enough to become reusable formats and production starts.

Phase 2 answers:

```text
Which discovered format is actually worth producing, why, and how should P0-B start from it?
```

Phase 2 does not answer:

```text
How to write the final script, resolve every asset, generate the final video, or publish it.
```

Those belong to P0-B and later production-chain layers.

---

## 2. One-Line Scope

```text
TrendOpportunityPacket + FormatObservation -> Format + FormatGenome + TrendScorecard -> ProductionStartPacket for P0-B
```

---

## 3. Phase Boundary

Phase 2 is the intelligence decision layer between trend discovery and production planning.

It is stronger than P1:

```text
P1: this looks like a repeated opportunity.
P2: this is or is not a reusable format worth starting production from.
```

It is weaker than P3+ production planning:

```text
P2: this format should be made, and these are the preserved/changeable elements.
P3+: here is the reproduction strategy, semantic transfer, script, storyboard, and route-specific plan.
```

P2 can prepare a `ProductionStartPacket` for P0-B. It must not silently create final scripts, assets, generated candidates, or publish packages.

---

## 4. Inputs

Primary inputs:

```text
TrendOpportunityPacket
FormatObservation
UnderstandingReport
SourceManifest
SourceCandidate clusters
Source clusters
comment sentiment summaries
AI method/tool guesses
ScoreProfile
UserPreference
Tool registry snapshot
Permission snapshot
ReviewItem history
existing Format memory if available
```

P2 should accept incomplete evidence, but every missing or weak signal must be visible.

---

## 5. Outputs

Primary outputs:

```text
Format
FormatGenome
FormatClusterReport
TrendScorecard
ScoreExplanationReport
ProductionOpportunityDecision
ProductionStartPacket for P0-B
ReviewItem when evidence/weights/policy are uncertain
DecisionLog entries
Phase2DecisionReport
```

The main handoff to P0-B is `ProductionStartPacket`.

---

## 6. Must Include

```text
Format Promotion:
  Promote strong FormatObservations into Format records when evidence is enough.

Format Genome v1:
  Extract reusable structure: roles, beats, pacing, visual grammar, audio/text function, repetition logic, transfer constraints.

Variant And Cluster Analysis:
  Distinguish true new formats from variants, remixes, reposts, and weakly similar videos.

TrendScorecard v1:
  Score heat, growth, freshness, repetition signal, comment sentiment, fatigue, transferability, asset readiness, tool readiness, source confidence, and production cost.

Fatigue Interpretation:
  Decide whether many similar videos mean useful popularity or stale overuse.

Weight Profiles:
  Store visible, versioned, editable, recalculable score weights.

Regent Gate 1:
  Select, defer, reject, or request more evidence for a format.

ProductionStartPacket:
  Hand P0-B enough information to create a production job without redoing trend analysis.

Review Report:
  Show the user why a format was selected, deferred, or rejected.
```

---

## 7. Must Not Include

```text
new broad platform crawling beyond P1 scope
video generation
full script council
asset resolver full version
MMD/3D route implementation
longform route implementation
platform publishing
post-publish feedback learning
self-applying score weight changes
hidden score changes
fake trend evidence
```

Phase 2 can estimate production feasibility, but it must not pretend assets/tools are ready when they are not.

---

## 8. Phase 2 Workstreams

P2 should be implemented as one continuous phase batch when confirmed, but it has internal workstreams:

```text
P2-A Input Loader and Evidence Binder
P2-B Cluster and Variant Analyzer
P2-C Format Promotion Engine
P2-D Format Genome Builder v1
P2-E TrendScorecard v1
P2-F Fatigue and Lifecycle Interpreter
P2-G Tool/Asset Readiness Estimator
P2-H Score Explanation and Weight Snapshot
P2-I Regent Gate 1 Decision
P2-J ProductionStartPacket Builder
P2-K Phase 2 Review Report and Tests
```

These are not separate phases and should not require separate user approval gates once P2 is confirmed.

---

## 9. Operating Flow

```text
1. Load P1 TrendOpportunityPackets.
2. Load related FormatObservations, UnderstandingReports, and evidence sources.
3. Bind every scoreable claim to sources, comments, metrics, or explicit missing evidence.
4. Cluster similar opportunities and sources.
5. Identify reposts, variants, shared music, shared character/topic, and true format similarity.
6. Decide whether observations can be promoted to Format records.
7. Build FormatGenome v1.
8. Run TrendScorecard v1.
9. Interpret fatigue and repetition signals.
10. Estimate production feasibility from tool and asset readiness snapshots.
11. Generate ScoreExplanationReport.
12. Run Regent Gate 1.
13. Create ProductionStartPacket for selected/deferred/review-needed formats.
14. Write ReviewItems and DecisionLogs.
15. Write Phase2DecisionReport.
16. Run fixture-based tests.
```

Dependencies:

```text
evidence binding before scoring
clustering before promotion
genome before production handoff
score explanation before Regent Gate 1
DecisionLog before ProductionStartPacket finalization
```

---

## 10. Agent Order

Phase 2 can use many small agents, but they should run in ordered passes.

Default agent pass order:

```text
1. EvidenceBinder
2. SourceIndependenceChecker
3. SimilarityClusterAgent
4. RepostAndVariantDetector
5. FormatPromotionAgent
6. GenomeSlotExtractor
7. BeatAndPacingMapper
8. VisualGrammarAgent
9. AudioTextFunctionAgent
10. TransferConstraintAgent
11. HeatScoreAgent
12. GrowthScoreAgent
13. CommentDirectionAgent
14. FatigueDetector
15. TransferabilityAgent
16. AssetReadinessEstimator
17. ToolReadinessEstimator
18. ProductionCostEstimator
19. ScorecardAssembler
20. ScoreExplanationAgent
21. RegentGate1
22. ProductionStartPacketAssembler
23. Phase2ReportWriter
```

Cheap-first rule:

```text
cheap agents do extraction, grouping, and obvious scoring
medium agents inspect semantics, fatigue, transferability, and explanation
strong agents only handle near-threshold decisions, high disagreement, or high-impact production starts
```

Disagreement handling:

```text
record disagreement
compare evidence
rerun relevant specialist if needed
escalate model tier if decision impact is high
create ReviewItem if still uncertain
Regent Gate 1 makes the final recorded decision
```

---

## 11. Format Promotion Rules

A `FormatObservation` can be promoted to `Format` when at least one condition is true:

```text
3+ independent examples share the same reusable structure
1 strong root example plus clear remixes/repetitions/comments
1 known template/challenge/trend with platform evidence
user manually approves promotion despite weak evidence
```

Promotion must record:

```text
evidence sources
source independence check
confidence
what is shared
what is variable
why it is not merely a repost
why it is not merely a loose theme
why it is production-relevant
review status
```

Promotion results:

```text
promote_new_format
attach_as_variant
keep_as_observation
needs_more_sources
reject_as_not_format
```

---

## 12. Cluster And Variant Analysis

Cluster analysis should distinguish:

```text
same format
variant of same format
same music but different format
same character/topic but different format
same script but different visual route
same visual style but different story format
repost/reupload
weak similarity only
```

This matters because similar-video count can be a positive heat signal or a negative fatigue signal.

Cluster output should include:

```json
{
  "format_cluster_report_id": "fmt_cluster_000001",
  "run_id": "run_000001",
  "cluster_label": "real-couple-denial-short-drama-variant",
  "members": ["src_000001", "src_000002"],
  "representative_sources": ["src_000001"],
  "similarity_reasons": [],
  "difference_axes": [],
  "repost_likelihood": 0.0,
  "variant_likelihood": 0.0,
  "new_format_likelihood": 0.0,
  "needs_more_sources": false
}
```

---

## 13. Format Genome v1

Genome fields:

```text
core_hook
role_structure
beat_sequence
pacing_profile
visual_grammar
audio_function
subtitle/text_function
comment_interaction_pattern
transferable_parts
non_transferable_parts
variant_axes
fatigue_signals
production_constraints
source_evidence_refs
```

The genome should make semantic transfer easier later, but it does not write the final script.

Example structure:

```json
{
  "format_genome_id": "fmt_genome_000001",
  "format_id": "fmt_000001",
  "core_hook": "one person denies a desire while evidence exposes them",
  "role_structure": [
    {"role": "denier", "function": "protects image while obviously guilty"},
    {"role": "teaser", "function": "reveals evidence and controls pacing"}
  ],
  "beat_sequence": [
    "setup denial",
    "evidence reveal",
    "defensive excuse",
    "collapse or exposed reaction"
  ],
  "transferable_parts": ["role dynamic", "evidence reveal", "punchline rhythm"],
  "non_transferable_parts": ["exact personal creator lines unless approved"],
  "variant_axes": ["characters", "object_of_desire", "setting", "visual style"],
  "production_constraints": ["needs readable subtitles", "needs clear reaction timing"],
  "confidence": 0.78
}
```

---

## 14. TrendScorecard v1

Score components:

```text
heat
growth
freshness
repetition_signal
comment_sentiment
fatigue_penalty
transferability
asset_readiness
tool_readiness
source_confidence
production_cost_penalty
```

Every scorecard must show:

```text
raw score
weight
weighted contribution
evidence
confidence
missing evidence
```

Default score scale:

```text
raw score: 0.0 to 10.0
confidence: 0.0 to 1.0
final score: normalized 0.0 to 10.0
```

Default signed weights:

```json
{
  "heat": 0.18,
  "growth": 0.20,
  "freshness": 0.11,
  "repetition_signal": 0.10,
  "comment_sentiment": 0.12,
  "transferability": 0.10,
  "asset_readiness": 0.07,
  "tool_readiness": 0.06,
  "source_confidence": 0.08,
  "fatigue_penalty": -0.15,
  "production_cost_penalty": -0.06
}
```

Weight principle:

```text
heat and growth have higher default weights
fatigue is a penalty, not a simple inverse of repetition
asset/tool readiness matter but should not dominate trend value in P2
weights are visible, versioned, editable, and recalculable
```

Scorecard shape:

```json
{
  "trend_scorecard_id": "trend_score_000001",
  "format_id": "fmt_000001",
  "score_profile_id": "trend_video_v1",
  "score_profile_version": "1.0",
  "components": {
    "heat": {
      "raw": 8.4,
      "weight": 0.18,
      "weighted": 1.512,
      "confidence": 0.76,
      "evidence": ["src_000001 metrics", "src_000002 metrics"],
      "missing_evidence": []
    }
  },
  "penalties": {},
  "final_score": 7.34,
  "threshold_profile": "p2_gate_default_v1",
  "recommended_decision": "start_p0b_job",
  "created_at": "..."
}
```

---

## 15. ScoreProfile and Recalculation

P2 must store a snapshot of the score profile with every scorecard.

Score profile fields:

```json
{
  "score_profile_id": "trend_video_v1",
  "profile_type": "trend",
  "version": "1.0",
  "weights": {},
  "thresholds": {
    "start_p0b_job": 7.2,
    "needs_user_review": 6.6,
    "needs_more_evidence": 5.2,
    "reject_below": 4.0
  },
  "change_note": "initial P2 default"
}
```

Rules:

```text
old scorecards keep their original weight snapshot
new weight profiles do not silently rewrite old decisions
user can later recalculate old scorecards under a new profile
recalculation must create a new scorecard version or recalculation report
weight changes require user approval before becoming default rules
```

The UI/report must show scores in a way the user can adjust later:

```text
component -> raw score -> weight -> contribution -> evidence -> confidence
```

---

## 16. Fatigue Interpretation

High similar-video count is positive when:

```text
engagement stays strong
comments ask for variants
comments quote or roleplay the format
new creators adapt creatively
trend is still growing
newer examples outperform older examples
```

High similar-video count is negative when:

```text
comments call it stale
engagement drops
videos become low-effort repeats
new examples underperform older examples
comments say they are tired of seeing it
format has reached obvious saturation
```

Do not treat repetition as automatically good or bad.

Fatigue output:

```json
{
  "fatigue_interpretation_id": "fatigue_000001",
  "format_id": "fmt_000001",
  "similar_count_signal": "positive_heat | negative_fatigue | mixed | unknown",
  "reasons_positive": [],
  "reasons_negative": [],
  "comment_direction": "asking_for_more | enjoying | mixed | stale_complaints | unknown",
  "lifecycle_stage_guess": "emerging | rising | peak | fatigue | dead | unknown",
  "confidence": 0.0
}
```

---

## 17. Tool and Asset Readiness Estimation

P2 estimates readiness. It does not resolve every asset or call generation tools.

Asset readiness estimates:

```text
official references found
local assets likely available
research assets available
required audio available or searchable
required voice profile available or user-provided
personal/unknown asset review needed
missing key asset likely blocking
```

Tool readiness estimates:

```text
same suspected AI method available
same suspected AI method not configured
same suspected AI method unavailable
alternative route likely possible
manual generation slot possible
tool setup item required
```

Output shape:

```json
{
  "readiness_summary_id": "ready_000001",
  "format_id": "fmt_000001",
  "asset_readiness": "ready | partial | needs_review | blocked | unknown",
  "tool_readiness": "ready | manual_slot_possible | not_configured | unavailable | unknown",
  "same_method_guess": [],
  "fallback_routes": [],
  "blocking_review_items": [],
  "tool_setup_items": []
}
```

Rules:

```text
readiness can affect decision but must not fake availability
if same AI method is unknown, say unknown
if same AI method is unavailable, recommend existing/fallback routes if plausible
if user action is needed, create ReviewItem or ToolSetupItem
```

---

## 18. ProductionOpportunityDecision

Decision values:

```text
start_p0b_job
defer
reject
needs_more_evidence
needs_user_review
```

Default decision logic:

```text
start_p0b_job:
  strong score, enough evidence, no blocking review/tool gap, production handoff clear.

needs_user_review:
  near threshold, subjective choice, uncertain source policy, weight uncertainty, or conflicting agents.

needs_more_evidence:
  promising but evidence count/source confidence is too weak.

defer:
  real opportunity, but timing/tool/assets/user preference makes immediate production unwise.

reject:
  weak, stale, not transferable, too costly, not a real format, or unsupported by evidence.
```

Thresholds are guidance, not hard laws. Regent Gate 1 may override with a recorded reason.

Decision schema:

```json
{
  "decision_id": "decision_000001",
  "format_id": "fmt_000001",
  "trend_scorecard_id": "trend_score_000001",
  "decision": "start_p0b_job",
  "reason": "High growth, strong comment sentiment, clear transferable structure.",
  "agent_votes": [],
  "thresholds_used": {},
  "required_review_items": [],
  "production_start_packet_id": "psp_000001",
  "created_at": "..."
}
```

---

## 19. Regent Gate 1

Regent Gate 1 is the P2 final decision gate.

It checks:

```text
scorecard result
evidence confidence
format genome clarity
source policy status
asset/tool readiness estimate
permission matrix
review items
budget/cost estimate
user preferences
agent disagreement
```

Regent Gate 1 must write:

```text
DecisionLog
ProductionOpportunityDecision
ReviewItems if needed
ProductionStartPacket when appropriate
```

Gate output must explain both positive and negative factors. A selected format should still show its weaknesses.

---

## 20. ProductionStartPacket

Purpose:

```text
Give P0-B a selected, scored, explainable format opportunity that can become a production job.
```

Schema:

```json
{
  "production_start_packet_id": "psp_000001",
  "format_id": "fmt_000001",
  "format_genome_id": "fmt_genome_000001",
  "trend_scorecard_id": "trend_score_000001",
  "selected_source_ids": ["src_000001", "src_000002"],
  "representative_source_ids": ["src_000001"],
  "decision": "start_p0b_job | defer | reject | needs_more_evidence | needs_user_review",
  "reason": "...",
  "recommended_job_type": "ordinary_ai_format_video",
  "recommended_production_routes": [],
  "recommended_transfer_targets": [],
  "must_preserve": [],
  "should_preserve": [],
  "can_change": [],
  "do_not_use": [],
  "asset_readiness_summary": {},
  "tool_readiness_summary": {},
  "risk_and_review_items": [],
  "score_snapshot": {},
  "evidence_refs": [],
  "created_at": "..."
}
```

P0-B may start from this packet instead of a manual seed.

If the decision is not `start_p0b_job`, P2 may still create a packet for review/defer records, but it must clearly mark that production should not start yet.

---

## 21. Review Items

P2 should create ReviewItems for:

```text
uncertain format promotion
near-threshold score decision
weight profile disagreement
unknown source policy affecting direct use
personal creator asset direct-use question
tool/API availability gap
same AI method unavailable
high production cost estimate
uncertain fatigue interpretation
user preference conflict
agent disagreement with high impact
```

Review items should be short and evidence-linked. They should not dump raw cluster data into the user queue.

Example:

```json
{
  "type": "weight_change",
  "blocking": false,
  "summary": "Growth score dominates this decision; review if current weight is too aggressive.",
  "system_recommendation": "Keep current weight for now; collect post-publish feedback before changing defaults.",
  "options": ["keep", "lower_growth_weight", "ask_more"]
}
```

---

## 22. Phase2DecisionReport

P2 must write a human-readable report.

Recommended report path:

```text
reports/phase_reports/phase2_decision_report_run_000001.md
```

Report sections:

```text
1. Run and input summary
2. Opportunities loaded from P1
3. Clusters and variant groups
4. Formats promoted, deferred, or rejected
5. Format genomes created
6. Trend scorecards and visible weights
7. Heat vs fatigue interpretation
8. Tool and asset readiness estimates
9. Regent Gate 1 decisions
10. ProductionStartPackets created
11. ReviewItems created
12. Missing evidence and recommended next scouting
13. Tests or validation notes
```

The report should let the user understand why Kairove wants to make something without opening raw JSON.

---

## 23. Storage Layout

P2 should reuse the project storage strategy.

Suggested layout:

```text
runs/run_000001/phase2/
  input_refs.json
  cluster_reports/
  format_promotion/
  format_genomes/
  scorecards/
  score_explanations/
  decisions/
  production_start_packets/
  review_items/
  phase2_decision_report.md

knowledge_base/formats/
  format_cards/
  format_genomes/

knowledge_base/scoring/
  score_profiles/
  trend_scorecards/
```

Rules:

```text
large evidence stays in research_assets
P2 references evidence instead of copying everything
score profiles are versioned
format genomes can later be promoted into long-term knowledge
old decisions remain reproducible
```

---

## 24. Relationship To P0-B

P0-B can start from:

```text
manual seed
approved source
ProductionStartPacket
```

When P0-B starts from a ProductionStartPacket, it should not redo P2 trend scoring. It can still create a P0-B simple format observation and semantic transfer brief as production artifacts, but those should reference P2 outputs.

P2 handoff responsibilities:

```text
selected format
why selected
representative evidence
score snapshot
must preserve / can change
asset/tool readiness estimate
review blockers
recommended route/job type
```

P0-B responsibilities after handoff:

```text
create Job
build semantic transfer brief
build asset requirement report
build prompt package/manual generation slot
import candidate
QA
retry/pass
packaging
manual publish package
```

---

## 25. Relationship To Later Phases

P2 should not collapse future phases into itself.

Later phases will likely take these responsibilities:

```text
P3:
  detailed reproduction strategy, semantic transfer, script, storyboard, direction.

P4:
  full asset resolver, character/world knowledge, audio/visual material system.

P5:
  generation tool selection, route execution, candidate generation.

P6:
  advanced multi-layer QA and retry.

P7:
  platform packaging and publishing.

P8:
  feedback learning and weight optimization.
```

P2 may prepare fields for those phases, but it must not implement them.

---

## 26. Tests

P2 should be testable with saved P1 fixtures and no live network requirement.

Required fixture groups:

```text
single strong source with remix evidence
three independent similar sources
same music but different format
same character/topic but different format
repost cluster
popular and still growing format
popular but stale/overused format
weak source confidence
missing comments/metrics
near-threshold score
same suspected AI method unavailable
```

Required tests:

```text
loads P1 TrendOpportunityPacket fixtures
clusters related sources
separates reposts from true variants
promotes strong observations into Format
keeps weak observations unpromoted
writes FormatGenome v1
writes TrendScorecard with visible weights
recalculates score under alternate ScoreProfile without mutating old scorecard
interprets repetition as positive heat when evidence supports it
interprets repetition as fatigue when evidence supports it
creates ReviewItems for uncertainty
creates ProductionStartPacket for selected format
refuses to start generation
writes Phase2DecisionReport
```

---

## 27. Acceptance Criteria

Phase 2 can be considered ready when Kairove can:

```text
read P1 TrendOpportunityPackets
bind scoreable claims to evidence
cluster related opportunities
separate same-format, variant, repost, same-music, same-topic, and weak-similarity cases
promote at least one strong observation into a Format
write FormatGenome v1
write TrendScorecard v1 with visible weights
explain positive popularity vs stale overuse
estimate tool/asset readiness without faking availability
create Regent Gate 1 decisions
create ProductionStartPacket for P0-B
create ReviewItems for uncertainty
write Phase2DecisionReport
avoid video generation and publishing
pass fixture-based tests
```

---

## 28. Non-Acceptance

Phase 2 is not acceptable if:

```text
it treats all repetition as good
it treats all repetition as stale
it hides score weights
it silently changes weight profiles
it promotes weak observations as full formats without confidence labels
it loses source evidence
it starts generation directly
it fakes missing evidence
it claims assets/tools are available without proof
it creates final scripts or prompts as if P3/P0-B already ran
it invents confirmed Phase 3+ implementation scope
```

---

## 29. Recommended Implementation Mode

When confirmed, implement P2 as one continuous phase batch.

Implementation order:

```text
1. Lock P2 data contracts and storage paths.
2. Build input loader from P1 outputs.
3. Build evidence binder.
4. Build cluster and variant analyzer.
5. Build format promotion engine.
6. Build FormatGenome v1 builder.
7. Build TrendScorecard v1 and ScoreProfile snapshots.
8. Build fatigue/lifecycle interpreter.
9. Build readiness estimator.
10. Build ScoreExplanationReport.
11. Build Regent Gate 1 decision logic.
12. Build ProductionStartPacket.
13. Build Phase2DecisionReport.
14. Add fixture-based tests.
```

No live crawling, generation, or publishing should be required for P2 tests.

---

## 30. Confirmation Checklist

Before Phase 2 is marked confirmed for implementation, accept or revise:

```text
Identity:
  Format Intelligence and Opportunity Decision.

Primary input:
  P1 TrendOpportunityPackets and FormatObservations.

Primary output:
  ProductionStartPacket for P0-B.

Format work:
  Format Genome v1, not the final self-evolving Format Miner.

Scoring work:
  TrendScorecard v1 with visible weights, not silent automatic optimization.

Decision gate:
  Regent Gate 1 selects/defer/rejects/request-more-evidence.

Implementation mode:
  One continuous Phase 2 batch once confirmed.

Non-goals:
  No video generation, no full asset resolver, no platform publishing, no fake evidence.

Boundary:
  P3-P11 remain rough map only until separately discussed.
```

---

## Cross-Phase Policy Alignment - 2026-06-06

P2 Format Miner / Trend Analyst work must follow these priorities:

```text
Primary Format Miner extraction order:
  hook
  rhythm
  shot/scene structure
  role relationship
  reversal point
  copywriting template
  audio/subtitle function
  visual style

Additional useful structure:
  audience expectation
  interaction trigger
  production difficulty
  asset requirements
  platform fit
```

Trend scoring policy:

```text
Hot-but-overused does not mean automatic rejection.
Reduce exact-copy weight and prefer variants.
Keep riding a trend when comment sentiment, recent growth, and interaction quality remain good.
Deduct or abandon when fatigue, negative sentiment, or growth decline is clear.
Weights must be visible, configurable, versioned, and recalculable.
Major weight changes require user approval.
```
