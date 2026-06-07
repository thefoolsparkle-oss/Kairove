# Kairove Phase 8: Feedback Learning, Long-Term Memory, and Weight Optimization Plan

## 0. Status

Current status:

```text
Phase 8: detailed planning draft, not yet confirmed for implementation
Depends on: P7 PublishRecords, P6 QualityReports, user decisions, and metrics
Primary output: MemoryEntries, FeedbackReports, LearningSuggestions, WeightChangeSuggestions
Related capability doc: KNOWLEDGE_AND_LEARNING_PLAN.md
```

---

## 1. Purpose

Phase 8 makes Kairove learn from what happened.

It answers:

```text
What worked, what failed, what should be remembered, what should be suggested, and what should only become a rule after user approval?
```

Learning must improve future runs without making the system unpredictable.

---

## 2. One-Line Scope

```text
PublishRecords + Metrics + Quality/Retry/User Decisions -> FeedbackReport + MemoryEntries + PendingSuggestions
```

---

## 3. Must Include

```text
Post-Job Learning:
  Learn from generation failures, QA results, retry history, asset gaps, tool behavior, and user decisions.

Post-Publish Feedback:
  Collect or manually record views, likes, comments, shares, favorites, completion rate, audit status, and sentiment.

Memory Types:
  Separate observations, analysis, suggestions, and approved rules.

Weight Suggestions:
  Suggest score/quality/packaging weight changes with evidence, sample size, and confidence.

Format Miner Growth:
  Let Format Miner improve its schema/signals through reviewed suggestions.

Tool Learning:
  Track which tools work or fail for each route and context.

User Approval:
  No learning suggestion silently becomes a default rule.
```

---

## 4. Must Not Include

```text
silent score weight changes
silent rule changes
overfitting from one weak result
auto-deleting old knowledge
rewriting old decisions
fabricating platform metrics
changing permissions without user approval
```

---

## 5. Inputs

```text
PublishRecords
PlatformMetrics
manual metric entries
comments and sentiment summaries
QualityReports
RetryPlans
GenerationSteps
ToolPerformanceRecords
AssetResolutionReports
PackagingReports
User Review decisions
DecisionLogs
FormatGenome
TrendScorecards
ScoreProfiles
```

---

## 6. Outputs

```text
PostJobLearningReport
PostPublishFeedbackReport
MemoryEntries
LearningObservations
LearningAnalysis
LearningSuggestions
WeightChangeSuggestions
ToolPerformanceUpdates
FormatMemoryUpdates
UserPreferenceSuggestions
PlatformLearningReport
ReviewItems for approval
DecisionLogs
Phase8LearningReport
```

---

## 7. Workstreams

```text
P8-A Feedback Ingestion
P8-B Metric Normalization
P8-C Comment and Sentiment Summarization
P8-D Post-Job Learning
P8-E Tool and Route Learning
P8-F Format and Trend Learning
P8-G Packaging Learning
P8-H Weight Suggestion Engine
P8-I User Preference Learning
P8-J Approval and Versioning System
P8-K Learning Report and Tests
```

---

## 8. Learning Entry Types

```text
observation:
  Factual note, can be written automatically.

analysis:
  Agent interpretation of patterns and possible causes.

suggestion:
  Proposed behavior/rule/weight change; requires review before use.

approved_rule:
  User-approved rule that can affect future runs.
```

Only `approved_rule` can change default behavior.

---

## 9. Memory Entry Schema

```json
{
  "memory_id": "mem_000001",
  "memory_type": "observation | analysis | suggestion | approved_rule",
  "scope": "global | platform | route | format | character | tool | packaging | quality",
  "title": "...",
  "content": "...",
  "evidence": [
    {
      "object_type": "job | format | source | candidate | publish_record | quality_report",
      "object_id": "...",
      "field": "..."
    }
  ],
  "confidence": 0.72,
  "sample_size": 5,
  "status": "active | pending_review | rejected | superseded",
  "created_by": "Kairove Regent",
  "created_at": "..."
}
```

No evidence means hypothesis, not a rule.

---

## 10. Feedback Collection Windows

Default windows:

```text
T+1h early pulse if available
T+24h first useful result
T+72h short-term result
T+7d stable result
manual final entry when automatic metrics are unavailable
```

Metrics should link to:

```text
format
trend scorecard
title
cover
tags
platform payload
quality report
publish record
user notes
```

---

## 11. Metric Interpretation

Signal types:

```text
strong_signal:
  repeated result across similar jobs, enough views, clear comment direction.

weak_signal:
  one video, low views, timing uncertainty, incomplete platform metrics.

negative_signal:
  audit issue, bad comments, low completion, obvious title/cover mismatch.
```

Kairove should avoid over-learning from one video.

---

## 12. Post-Job Learning

Post-job learning runs even before publishing feedback.

It records:

```text
what was attempted
which route/tool was used
which candidates failed or passed
failure tags and retry history
asset gaps
user overrides
prompt patterns that helped or hurt
```

Examples:

```text
Tool X failed on continuous two-character dialogue.
Reaction-cut route preserved character identity better.
This format needs visible evidence object by beat 2.
User rejected this version as too generic AI.
```

---

## 13. Post-Publish Learning

Post-publish learning records:

```text
platform performance
comment sentiment
audience confusion or enjoyment
cover/title/tag effect clues
platform audit status
manual publishing notes
```

It should compare against:

```text
same platform baseline
same format history
same route history
same character/fandom history
similar publication time if known
```

---

## 14. Format Miner Growth

Format Miner can grow by suggesting:

```text
new genome fields
new fatigue signals
new comment behavior signals
new semantic transfer constraints
new route recommendations
new failure patterns
new lifecycle labels
```

Example:

```json
{
  "suggestion_type": "format_schema_field",
  "field": "comment_roleplay_density",
  "reason": "High-performing abstract short formats often depend on viewers continuing the joke in comments.",
  "evidence_count": 12,
  "requires_user_approval": true
}
```

Schema changes should be reviewed and versioned.

---

## 15. Trend and Quality Weight Suggestions

Weight suggestions can target:

```text
trend heat
growth speed
freshness
fatigue penalty
comment sentiment
transferability
asset readiness
tool readiness
production cost penalty
quality semantic transfer
quality character consistency
packaging title/cover weights
```

Suggestion schema:

```json
{
  "suggestion_type": "trend_weight_change",
  "profile": "trend_video_v1",
  "current": {"heat": 0.18, "growth": 0.20},
  "suggested": {"heat": 0.22, "growth": 0.24},
  "reason": "Recent successful jobs came from fast-growing formats even with high repetition.",
  "sample_size": 9,
  "confidence": 0.68,
  "requires_user_approval": true
}
```

Old scorecards remain reproducible. Recalculation creates new reports or versions.

---

## 16. Tool Learning

ToolPerformanceUpdate tracks:

```text
route context
input type
success/failure count
average quality
common failure tags
cost/speed
useful prompt patterns
successful workarounds
last failure
confidence
```

Tool recommendations must be context-specific. A tool may be strong for horror atmosphere and weak for two-character dialogue.

---

## 17. User Preference Learning

User decisions are high-value evidence.

Preference scopes:

```text
global
platform
route
format
character
relationship
packaging
quality
asset policy
```

Preference learning examples:

```text
user prefers autonomous scouting over manual seed
user dislikes fixed duration buckets
user allows official assets direct-use
user rejects over-clean AI faces
user wants all-platform publishing by default
```

A narrow preference should not become broad without approval.

---

## 18. Rule Approval and Versioning

Approved rule fields:

```text
rule_id
scope
rule_text
source_suggestion_id
evidence
approved_by_user
created_at
version
supersedes
rollback_available
```

If a rule conflicts with an old rule, mark the old rule `superseded`; do not delete it.

---

## 19. Review Items

Create ReviewItems for:

```text
weight changes
new Format Miner schema fields
route preference changes
platform packaging strategy changes
permission or asset-policy changes
broad user-preference rules
high-impact tool selection rules
```

Review actions:

```text
approve
reject
approve_once
need_more_samples
edit_and_approve
archive
```

---

## 20. Retrieval Before Future Runs

Before later jobs, Kairove should retrieve:

```text
approved rules
format memories
same route failures
same character/fandom notes
same tool performance
platform packaging history
user preference rules
pending warnings
```

Retrieval should prefer:

```text
approved rules over suggestions
recent evidence over old evidence
larger sample size over single examples
same route/platform over loose similarity
user decisions over agent guesses
```

---

## 21. Storage Layout

```text
knowledge_base/
  memory_entries/
  approved_rules/
  learning_suggestions/
  score_profiles/
  tool_performance/
  format_memory/
  platform_feedback/
  packaging_memory/

reports/phase_reports/
  phase8_learning_report.md

runs/run_000001/phase8/
  post_job_learning.md
  post_publish_feedback.md
  metric_snapshots/
  suggestions/
  approval_queue_refs.json
```

---

## 22. Tests

Fixture groups:

```text
job with no publish metrics
manual metric entry
successful high-heat format
stale overused format
repeated tool failure
packaging title improved performance
single weak data point
user rejects suggestion
user approves weight change
conflicting old rule
```

Required tests:

```text
writes observations automatically
keeps suggestions pending
requires approval for approved_rule
creates weight suggestion with evidence and sample size
does not mutate old scorecards
records tool performance by route
stores manual metrics
retrieves relevant memory for a future job
supersedes old rule instead of deleting
```

---

## 23. Acceptance Criteria

P8 is ready when Kairove can:

```text
collect/manual-record feedback
write post-job and post-publish reports
create evidence-linked memory entries
separate observation/analysis/suggestion/approved_rule
suggest weight/rule changes without applying silently
track tool and route performance
support user approval and versioning
retrieve memory for future runs
pass fixture-based tests
```

---

## 24. Non-Acceptance

P8 is not acceptable if:

```text
it silently changes weights
it silently changes rules
it overfits from one result
it fabricates metrics
it loses evidence links
it deletes old knowledge instead of superseding
it treats agent speculation as fact
```

---

## 25. Confirmation Checklist

Before P8 implementation, confirm or revise:

```text
which metrics to collect first
manual metric entry format
minimum sample size for suggestions
weight approval workflow
memory retrieval limits
rule rollback behavior
```

---

## Cross-Phase Policy Alignment - 2026-06-06

P8 learning policy:

```text
Observations may automatically become memory.
Learning suggestions may be generated automatically.
Rule changes require user approval.
Weight changes require user approval.
Permission changes require user approval.
Auto-publish strategy changes require user approval.
Learning suggestions must not silently become active rules.
```

Retention policy for learning evidence:

```text
Default retention is long-term.
Failed generations, old candidates, downloaded assets, QA reports, and publish packages keep source and usage records.
Cleanup is allowed only with manifest and traceable records.
Deleting generated assets asks.
Deleting local assets defaults deny.
```
