# Kairove Human Review Console Plan

## 0. Purpose

The Human Review Console is the user's control surface for Kairove.

Kairove should not dump raw logs on the user. It should present clear decision cards:

- what needs review;
- why it matters;
- what the system recommends;
- what options exist;
- what happens next.

---

## 1. Early Form

Early implementation can be:

```text
review_queue/*.json
reports/review_dashboard.html
scripts/review.py
```

Later it can become a local Web UI.

---

## 2. Review Queue

Review types:

```text
asset_review
risk_review
tool_setup
publish_approval
weight_change
character_mapping
high_cost_generation
retry_decision
user_preference_confirmation
```

Review statuses:

```text
pending
approved
rejected
deferred
resolved
archived
```

---

## 3. Decision Card

Each review item should show:

- short summary;
- why user input is needed;
- system recommendation;
- risk;
- evidence links;
- options;
- expected next action;
- free-form note.

Example:

```json
{
  "summary": "Approve CP semantic transfer?",
  "system_recommendation": "Approve with softer romance framing.",
  "options": [
    "approve",
    "approve_with_change",
    "choose_other_characters",
    "reject"
  ]
}
```

---

## 4. Candidate Comparison

For video candidates, console should show:

- video preview;
- key frames;
- quality score;
- failure tags;
- agent notes;
- prompt summary;
- cost;
- retry history.

Actions:

- select;
- reject;
- retry;
- merge preference;
- ask Regent to decide.

---

## 5. Asset Provenance Viewer

For each asset:

- source URL;
- source type;
- official/personal/unknown;
- usage policy;
- review status;
- used in jobs;
- local path;
- manifest.

---

## 6. Tool Setup Center

Shows:

- missing APIs;
- missing accounts;
- missing permissions;
- missing local installs;
- test status;
- impact of missing tool.

Example:

```text
Douyin publisher missing video publish permission.
Impact: can create package, cannot auto upload.
```

---

## 7. Permission Matrix Editor

User can edit:

- research permissions;
- asset permissions;
- generation permissions;
- publish permissions;
- system permissions.

Every change should be versioned and logged.

---

## 8. Score Profile Editor

User can:

- view weights;
- edit weights;
- compare before/after scores;
- apply suggestions;
- reject suggestions;
- rollback.

---

## 9. Dashboard

Home dashboard should show:

- active runs;
- active jobs;
- pending reviews;
- tool setup needs;
- best trend opportunities;
- recent failures;
- published performance;
- learning suggestions.

---

## 10. Acceptance Criteria

Human Review Console is ready when it can:

1. List pending review items.
2. Show decision cards.
3. Record user decisions.
4. Resolve review items.
5. Link decisions to decision logs.
6. Show candidate comparison reports.
7. Show tool setup queue.
8. Show permission and score profile summaries.

