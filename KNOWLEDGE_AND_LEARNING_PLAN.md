# Kairove Knowledge and Learning Plan

## 0. Purpose

This document defines Kairove's long-term knowledge base and learning system.

Kairove must not start from zero every run. It should learn from:

- researched sources;
- discovered formats;
- generated candidates;
- quality failures;
- user review;
- platform feedback;
- packaging performance;
- tool behavior.

---

## 1. Knowledge Base Areas

```text
research_knowledge
format_knowledge
fandom_character_knowledge
local_asset_knowledge
tool_capability_knowledge
job_memory
user_preference
platform_feedback
packaging_memory
```

---

## 2. Research Knowledge

Stores:

- sources;
- hot lists;
- comments;
- transcripts;
- screenshots;
- audio references;
- platform metrics;
- source manifests.

Used by:

- Source Scout;
- Format Miner;
- Trend Analyst;
- Asset Resolver.

---

## 3. Format Knowledge

Stores:

- format cards;
- format genomes;
- lifecycle state;
- similar formats;
- successful transfers;
- failed transfers;
- route recommendations;
- fatigue history.

Format learning update example:

```json
{
  "format_id": "fmt_000042",
  "learning_update": {
    "lifecycle_stage": "fatigue_rising",
    "successful_transfer": "anime_game_cp_teasing_version",
    "failed_transfer": "single_narration_version",
    "recommendation": "only produce high-variation versions"
  }
}
```

---

## 4. Fandom and Character Knowledge

Stores:

- worlds;
- characters;
- visual profiles;
- personality;
- speech style;
- relationships;
- CP dynamics;
- OOC risks;
- world scenes;
- suitable formats;
- unsuitable formats.

Every claim should have:

- source;
- confidence;
- user verification flag.

---

## 5. Tool Knowledge

Stores:

- available tools;
- missing tools;
- route compatibility;
- strengths and weaknesses;
- historical quality;
- failures and workarounds.

Used by:

- ToolSelector;
- AI Tool Imitation Council;
- Revision Engine.

---

## 6. User Preference Learning

Learn:

- accepted styles;
- rejected styles;
- preferred platforms;
- acceptable risk;
- disliked AI flavor;
- title/cover taste;
- character handling preferences.

Preference types:

```text
global
platform_specific
route_specific
format_specific
character_specific
packaging_specific
```

---

## 7. Platform Learning

Stores actual performance:

- views;
- likes;
- comments;
- shares;
- favorites;
- completion rate if available;
- audit status;
- comment sentiment.

Used to adjust:

- format scoring;
- platform packaging;
- timing;
- title strategy;
- thumbnail strategy.

---

## 8. Learning Entry Types

Learning outputs are divided into:

```text
observation:
  factual note, can be written automatically.

suggestion:
  proposed rule or weight change, needs user approval.

approved_rule:
  user-approved learning that can affect future behavior.
```

---

## 9. Reflection Reports

Kairove Regent should periodically write:

- post-job review;
- post-publish review;
- daily trend summary;
- weekly strategy review;
- failure cluster report.

Example:

```text
This week, character reenactment videos using reaction-cut editing scored higher than continuous two-character scenes.
Suggestion: prefer reaction-cut route for dialogue CP formats.
```

---

## 10. Weight Suggestions

Weight adjustment suggestions should include:

- current weight;
- suggested weight;
- evidence;
- sample size;
- confidence;
- affected score profile;
- whether user approval is required.

No core weight change should apply silently.

---

## 11. Acceptance Criteria

Knowledge and learning system is ready when it can:

1. Store memory entries.
2. Separate observations, suggestions, and approved rules.
3. Link memories to jobs, formats, tools, platforms, and assets.
4. Retrieve relevant past failures.
5. Generate learning update after a job.
6. Suggest score/profile changes without applying automatically.
---

## 12. Learning Operating Contract

Kairove's learning system records evidence, proposes changes, and retrieves useful memory. It should not silently mutate core behavior.

Learning layers:

```text
observation:
  Automatically written factual memory.

analysis:
  Agent interpretation of patterns and possible causes.

suggestion:
  Proposed rule, route preference, score weight, prompt pattern, or tool policy.

approved_rule:
  User-approved change allowed to affect future runs.
```

Only `approved_rule` can change default behavior. Suggestions remain pending until reviewed.

---

## 13. Memory Entry Schema

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

Every nontrivial learning entry should link to evidence. If there is no evidence, it is a hypothesis and should be labelled as such.

---

## 14. Retrieval Rules

Before each job, Kairove should retrieve relevant memory:

```text
format memories
similar source clusters
same route failures
same character/fandom notes
same tool performance
same platform packaging results
user preference rules
approved score profiles
```

Retrieval should prefer:

```text
approved rules over suggestions
recent evidence over old evidence
larger sample size over single examples
same route/platform over loosely similar cases
user decisions over agent guesses
```

Retrieved memory should be shown in job reports so the user can see what influenced the run.

---

## 15. Post-Job Learning Flow

After each job:

```text
1. Summarize what was attempted.
2. Compare selected candidate vs rejected candidates.
3. Record quality failures and retries.
4. Record which tools worked or failed.
5. Record user decisions.
6. Generate observations.
7. Generate suggestions only when evidence is enough.
8. Send suggestions to review queue.
```

Post-job learning should not wait for publishing feedback. It can learn about generation quality, retry patterns, prompt failures, and asset gaps immediately.

---

## 16. Post-Publish Learning Flow

After publishing:

```text
1. Fetch or manually record metrics.
2. Normalize metrics per platform.
3. Compare against similar jobs and platform baselines.
4. Summarize comment sentiment.
5. Identify title/cover/tag effects when possible.
6. Update platform feedback memory.
7. Suggest packaging or trend score changes if evidence supports it.
```

Metrics are noisy. Kairove should distinguish:

```text
strong signal:
  repeated result across similar videos, enough views, clear comment sentiment.

weak signal:
  one video, low views, platform timing uncertainty.

negative signal:
  audit issue, bad comments, low completion, obvious title/cover mismatch.
```

---

## 17. Format Miner Growth Loop

Format Miner should improve as it sees more video types.

Growth loop:

```text
1. Store extracted format cards and genomes.
2. Cluster similar formats.
3. Compare predicted performance vs actual performance.
4. Identify extraction fields that were missing.
5. Ask auxiliary agents to propose better fields.
6. Write pending schema/rule suggestions.
7. Apply only after user approval or explicit implementation update.
```

Example suggestion:

```json
{
  "suggestion_type": "format_schema_field",
  "field": "comment_roleplay_density",
  "reason": "High-performing abstract short drama formats often depend on viewers continuing the joke in comments.",
  "evidence_count": 12,
  "requires_user_approval": true
}
```

Format Miner growth is not just better scoring. It can add new detectable structures, new fatigue signals, new semantic-transfer warnings, and new route recommendations.

---

## 18. Trend Analyst Weight Learning

Trend weights must stay visible and versioned.

Learning can suggest changes for:

```text
heat weight
growth speed weight
freshness weight
fatigue penalty
comment sentiment weight
transferability weight
asset readiness weight
production cost penalty
platform fit weight
```

Suggestion example:

```json
{
  "suggestion_type": "trend_weight_change",
  "profile": "default_short_video",
  "current": {"heat": 0.24, "growth": 0.22, "fatigue_penalty": 0.10},
  "suggested": {"heat": 0.30, "growth": 0.28, "fatigue_penalty": 0.08},
  "reason": "Recent successful jobs came from high heat and fast growth even when similar-video count was high.",
  "sample_size": 9,
  "confidence": 0.68,
  "requires_user_approval": true
}
```

The system must distinguish high-volume popularity from stale overuse. Similar-video count is not automatically good or bad; it must be interpreted with engagement, growth, comment sentiment, freshness, and fatigue indicators.

---

## 19. Tool Learning

Tool learning records:

```text
which route a tool handled well
which prompt style worked
which parameters failed
cost and speed
rate limits
quality score distribution
common visual/audio problems
manual workaround notes
```

Tool recommendations should be route-specific. A tool can be strong for horror atmosphere and weak for two-character dialogue at the same time.

---

## 20. User Preference Learning

User decisions are high-value evidence.

Examples:

```text
User repeatedly rejects over-clean AI faces.
User approves official game assets for direct use.
User wants all-platform publishing by default.
User dislikes fixed duration buckets.
User prefers autonomous discovery over manual seed scouting.
```

Preference learning should record exact scope. A packaging preference should not automatically become a generation preference unless the user approves that broader rule.

---

## 21. Learning Safety and Versioning

Every approved rule should have:

```text
rule_id
scope
text
source suggestion
evidence
approved_by_user
created_at
version
supersedes
rollback_available
```

If a new approved rule conflicts with an older rule, Kairove should mark the older rule as superseded instead of deleting it.

---

## 22. Phase 0 Learning Scope

Phase 0 should implement learning as records and reports, not self-modifying behavior.

Minimum useful scope:

```text
write job observations
write quality failure clusters
write tool gap notes
write user decisions
write pending suggestions
show suggestions in compact context/index
require user approval before applying rules
```

This gives the system memory from the first real production chain without making it unpredictable.

---

## Cross-Phase Policy Alignment - 2026-06-06

Learning:

```text
Observations may automatically become memory.
Learning suggestions may be generated automatically.
Rule changes, weight changes, permission changes, and auto-publish strategy changes require user approval.
Suggestions must not silently become active rules.
```

Retention:

```text
Default retention is long-term.
Failed generations, old candidates, downloaded assets, QA reports, and publish packages keep source and usage records.
Cleanup requires manifest and traceable records.
Deleting generated assets asks.
Deleting local assets defaults deny.
```
