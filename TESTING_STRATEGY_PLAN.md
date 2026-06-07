# Kairove Testing Strategy Plan

## 0. Purpose

This document defines how Kairove should be tested.

Kairove has many moving parts. Tests must focus on:

- core objects;
- permissions;
- manifests;
- decision logs;
- data flow;
- failure handling;
- reproducibility.

---

## 1. Test Levels

```text
unit tests:
  pure functions, schema validation, permission checks.

integration tests:
  run -> job -> decision log -> review item flows.

fixture tests:
  saved JSON inputs for agents and councils.

filesystem tests:
  directory creation, manifests, asset paths.

external tool tests:
  safe dry-run tests for APIs or local tools.

end-to-end dry run:
  no real paid API, no real publish, but full object flow.
```

---

## 2. Phase 0 Tests

Required:

- config loads;
- permission matrix returns allow/ask/deny;
- run can be created;
- job can be created;
- decision log can be written;
- review item can be created and resolved;
- tool setup item can be created;
- directory paths are correct;
- database schema initializes.

---

## 3. Schema Tests

Validate:

- Run;
- Job;
- SourceCandidate;
- Source;
- Asset;
- Format;
- Scorecard;
- DecisionLog;
- ReviewItem;
- GenerationStep;
- Candidate;
- QualityReport;
- PublishRecord;
- MemoryEntry.

---

## 4. Permission Tests

Cases:

- official asset direct use allowed;
- personal creator direct use asks user;
- unknown source asks user;
- high-cost generation asks if configured;
- auto publish denied when permission deny;
- fetch metrics allowed when configured.

---

## 5. Manifest Tests

Cases:

- source manifest written;
- asset manifest written;
- source path exists;
- usage policy exists;
- review status exists;
- hash computed if file exists.

---

## 6. Agent Fixture Tests

Each agent group should have saved JSON fixtures:

```text
fixtures/
  source_scout/
  harvester/
  format_miner/
  trend_analyst/
  reproduction/
  generation/
  quality/
  retry/
  packaging/
```

Agent tests should verify structured outputs, not exact prose.

---

## 7. External API Tests

External tests must be safe:

- auth check;
- capability check;
- dry-run if supported;
- tiny request only with user permission;
- no public publish unless explicitly enabled.

If API missing, test should produce tool setup item rather than fail silently.

---

## 8. Regression Tests

Every fixed failure should become a regression fixture when possible:

- wrong source policy;
- missing decision log;
- candidate without generation step;
- scorecard not reproducible;
- retry plan not preserving successful parts.

---

## 9. Acceptance Criteria

Testing strategy is ready when:

1. Phase 0 has unit and integration tests.
2. Permission behavior is covered.
3. Manifest writing is covered.
4. Decision log and review queue are covered.
5. Agent fixture pattern exists.
6. External API missing states are tested safely.
---

## 10. Confirmed P0-B Test Scope

Because P0-B is confirmed, tests should treat P0-B as required. P0-A tests remain required as the foundation subset inside P0-B.

```text
P0-A:
  Foundation skeleton tests only.

P0-B:
  Foundation tests plus one lowest complete production-chain dry run.
```

No test should require real paid API calls, real crawling, or real public publishing unless the user explicitly enables those capabilities.

---

## 11. P0-A Foundation Subset Test Pack

```text
config_load_test
permission_matrix_test
folder_skeleton_test
database_init_test
run_create_test
job_create_test
decision_log_test
review_item_test
tool_setup_item_test
source_manifest_stub_test
asset_manifest_stub_test
phase_report_test
```

The P0-A subset passes when the system can create and remember project state safely. This is necessary but not sufficient for Phase 0 completion.

---

## 12. P0-B Required Test Pack

P0-B adds a dry production-chain fixture.

```text
approved_source_intake_test
source_manifest_provenance_test
format_observation_stub_test
semantic_transfer_brief_test
route_plan_test
asset_requirement_report_test
prompt_package_test
manual_generation_slot_test
candidate_import_test
candidate_manifest_test
basic_technical_qa_test
basic_semantic_qa_report_test
retry_decision_test
manual_publish_package_test
end_to_end_manual_chain_test
```

P0-B passes when Kairove can honestly move one approved source through a complete manual-slot production chain without pretending external automation exists.

---

## 13. Manual Slot Fixture

Manual generation slot tests should use a tiny local fixture video or placeholder media file that is clearly marked as a test fixture.

Test should verify:

```text
slot instructions are written
prompt package exists
input asset links exist
user output import path exists
imported output receives an asset id
candidate links to generation step
candidate links to source chain
QA report can read the candidate
publish package can include the candidate
```

The fixture is not proof of AI generation quality. It only proves the system can manage the chain.

---

## 14. Phase Boundary Regression Rule

P0-B is the confirmed Phase 0 test scope. If Phase 0 scope changes later, this testing plan must be updated before implementation continues.

---

## Cross-Phase Policy Test Alignment - 2026-06-06

Tests should protect these cross-phase defaults when relevant:

```text
manual publish package is default
auto-publish never occurs without permission
missing platform/API/login/download capability creates ToolSetupItem
personal/unknown direct-use assets create review path
official assets keep provenance
score weights remain visible and reproducible
learning suggestions do not silently become active rules
generated asset deletion asks
local asset deletion defaults deny
P0-B tests do not require paid API, network crawling, real generation, or real publishing
```
