# AIL + MoIE Recursive Research System
## Execution Plan v1.0

### Purpose

This plan turns the existing AIL + MoIE recursive research specification into a usable, auditable research system and benchmark.

The objective is not to prove every generated hypothesis correct. The objective is to operationalize a repeatable loop:

> **Problem → AIL assumptions → inversion → MoIE mechanisms → hypothesis → prediction → experiment → execution → evidence → JEV routing → updated theory → re-entry**

The implementation is designed to run on inexpensive/local resources first, with Freebuff used for coding/build/test execution and Hermes used for orchestration, reusable skills, persistent research memory, and provider/model routing.

---

# 1. What Has Already Been Demonstrated

Current empirical runs already show the research loop operating across multiple domains:

| Run | Domain | Outcome | What it demonstrates |
|---|---|---|---|
| DRB-001 | Software testing | Primary hypothesis unsupported | The loop can generate a falsifiable hypothesis and accept a negative result |
| DRB-002 | Astronomy | Hypothesis supported within synthetic conditions | The loop can produce a measurable scientific effect |
| DRB-003 | Ecology | Conditional support; competing mechanism weakened | The loop can separate mechanisms and narrow a broad claim |
| DRB-004 | Inventory/operations research | Conditional support | The loop can expose nonlinear tradeoffs and boundary conditions |
| DRB-005 | Epidemiology/network science | Support in tested regime | The loop can transfer to stochastic network modeling |

These are evidence of **workflow capability and cross-domain execution**, not proof of universal scientific validity or proof that every scientific conclusion is correct.

The next phase should preserve these runs unchanged and build on them.

---

# 2. System Architecture

## 2.1 Core components

### AIL

Responsible for:

- assumption inventory
- load-bearing assumption selection
- inversion
- re-derivation
- hypothesis generation

### MoIE

Responsible for multiple epistemic roles:

- Inversion Critic
- Deviant Scout
- Synthesizer
- Red Team
- Predictor

### Execution Layer

Responsible for:

- code generation
- dataset acquisition
- simulation
- experiment execution
- statistical analysis
- artifact generation

### JEV

Responsible for evidence routing and relationship classification:

- support
- contradiction
- partial support
- conditional support
- confound
- unknown
- novel finding
- escalation

### Persistence / Provenance

Responsible for:

- immutable run records
- inputs
- prompts/specifications
- model/provider metadata
- code version
- seeds
- datasets
- outputs
- evidence
- theory revisions
- next-test lineage

### Human

Responsible for:

- research objective
- constraints
- domain stakes
- authorization boundaries
- interpretation of consequential results
- acceptance/rejection of research direction

---

# 3. Freebuff + Hermes Division of Labor

## Freebuff: Build / Execute / Verify

Use Freebuff primarily as the implementation and execution surface.

Recommended responsibilities:

1. Implement schemas and state machine.
2. Implement JEV rules.
3. Implement evidence aggregation.
4. Create test harnesses.
5. Execute simulations and coding experiments.
6. Generate plots and raw artifacts.
7. Run unit/integration tests.
8. Perform code review and repository cleanup.
9. Produce reproducibility packages.
10. Maintain one isolated workspace per research run.

Freebuff currently provides CLI, desktop parallel-agent workflows, cloud GitHub sandboxes, specialized subagents, and multiple model choices, making it useful as the coding/execution layer. citeturn200642search0turn200642search1

### Freebuff rule

Freebuff should not be treated as the epistemic authority. Its job is to **build and execute** the experiment.

---

## Hermes: Orchestrate / Remember / Re-enter

Use Hermes primarily as the research orchestration and memory surface.

Recommended responsibilities:

1. Maintain the active research case.
2. Load domain-specific skills only when needed.
3. Preserve previous research cycles.
4. Record lessons learned.
5. Route research tasks to appropriate models/providers.
6. Spawn specialized research work where useful.
7. Re-ingest evidence summaries and detailed breakdowns.
8. Generate the updated-theory candidate.
9. Create the next research question.
10. Maintain researcher identity/preferences/context across sessions.

Hermes currently documents persistent memory, self-improving skills, provider-agnostic model routing, multi-agent capabilities, and reusable skill storage, which makes it a natural fit for the persistence/re-entry layer. citeturn200642search3turn200642search8

### Hermes rule

Hermes should not silently alter the historical record. New learning must become a **new versioned research state**.

---

# 4. Important Data-Handling Rule

Freebuff's current documentation states that prompts, messages, code, files, and repository data may be used to provide the service, and some providers/features may allow AI-training use depending on the model/feature notice. citeturn200642search1

Therefore:

- Do not place sensitive legal/family material, confidential client information, credentials, or regulated data into Freebuff until its applicable data-use terms are checked.
- Use synthetic/public research data for the benchmark phase.
- Keep provenance explicit when a cloud provider is involved.
- For sensitive real research, prefer local execution or a provider with an explicitly acceptable data policy.

This is an operational control, not a claim that Freebuff is unsafe.

---

# 5. Phase 0 — Freeze the Existing Evidence

## Objective

Create an immutable baseline before expanding anything.

## Deliverables

Create:

```text
research-benchmark/
  README.md
  BENCHMARK.md
  SPEC.md
  RESULTS.md
  runs/
    DRB-001/
    DRB-002/
    DRB-003/
    DRB-004/
    DRB-005/
```

For every run save:

- original prompt
- preregistration
- returned execution report
- code, if available
- parameters
- seeds
- raw outputs
- final interpretation
- stated limitations

## Acceptance criterion

No historical result is silently edited.

Corrections become versioned amendments.

---

# 6. Phase 1 — Complete the Reference Implementation

## Objective

Turn the existing specification into a small executable engine.

## Required modules

```text
ail_moie/
  schemas.py
  state_machine.py
  transitions.py
  jev.py
  evidence.py
  provenance.py
  persistence.py
  reentry.py
  runner.py
  cli.py

tests/
  test_state_machine.py
  test_jev.py
  test_evidence.py
  test_provenance.py
  test_reentry.py
  test_end_to_end.py
```

## State machine

Minimum states:

```text
INTAKE
ASSUMPTIONS
INVERSION
MECHANISMS
HYPOTHESIS
PREDICTION
DESIGN
PREREGISTERED
EXECUTING
RESULTS
EVIDENCE_SYNTHESIS
JEV_ROUTING
THEORY_UPDATE
REENTRY
ARCHIVED
```

## Core transition invariant

A state cannot advance unless its required artifact exists.

Example:

```text
HYPOTHESIS → PREDICTION
```

requires a hypothesis object.

```text
PREREGISTERED → EXECUTING
```

requires locked hypotheses, predictions, metrics, and falsification criteria.

```text
RESULTS → EVIDENCE_SYNTHESIS
```

requires raw or execution-referenced results.

```text
THEORY_UPDATE → REENTRY
```

requires an explicit updated-theory object and next-test proposal.

---

# 7. Phase 2 — JEV Decision Procedure

## Objective

Make JEV deterministic enough that two implementations receiving the same evidence package can produce the same routing decision when given the same configuration.

## Evidence object

Each evidence item should contain:

```json
{
  "id": "E-001",
  "claim": "medium window reduced absolute depth error",
  "source_type": "executed_result",
  "source_ref": "DRB-002/raw/results.json",
  "observed": true,
  "replicated": true,
  "directness": 0.95,
  "independence": 0.80,
  "quality": 0.85,
  "contradiction": 0.10,
  "scope_match": 0.80,
  "notes": "synthetic-data result"
}
```

## Proposed JEV procedure

### Step 1 — Validate evidence

Reject or downgrade evidence that lacks provenance, execution reference, or a defined observation.

### Step 2 — Normalize

Convert evidence into comparable relationship records:

```text
claim
expected relation
observed relation
scope
strength
counterevidence
```

### Step 3 — Score evidence

Initial reference score:

\[
W_i = D_i \times R_i \times I_i \times Q_i \times S_i
\]

where:

- \(D\) = directness
- \(R\) = reproducibility/replication
- \(I\) = independence
- \(Q\) = methodological quality
- \(S\) = scope match

Each factor is normalized to \([0,1]\).

### Step 4 — Aggregate for a claim

Maintain separate positive and negative evidence:

\[
E^+ = \sum W_i^{+}
\]

\[
E^- = \sum W_i^{-}
\]

Do not collapse contradiction into a single confidence number prematurely.

### Step 5 — Apply JEV thresholds

Initial reference thresholds:

```text
SUPPORT            if E+ - E- >= +0.35 and no critical contradiction
CONTRADICTION      if E- - E+ >= +0.35 and no critical support issue
PARTIAL            if |E+ - E-| < 0.35 but both sides are material
CONDITIONAL        if support is concentrated in explicit conditions
CONFOUND            if an alternative mechanism explains the effect
UNKNOWN            if evidence quality/directness is too low
NOVEL              if observed effect was not predicted but is reproducible
```

These thresholds are **initial parameters**, not sacred values. They are to be calibrated against expert decisions.

### Step 6 — Escalation

JEV must output an explicit human-review flag when:

- evidence conflicts materially;
- safety/ethical stakes are high;
- data provenance is incomplete;
- model output contradicts executed evidence;
- or a theory update would materially alter the research objective.

---

# 8. Phase 3 — Calibrate JEV Against Expert Decisions

## Objective

Determine whether JEV's routing decisions approximate decisions made by humans reviewing the same evidence package.

## Do not calibrate against model consensus

The calibration set must contain human judgments.

## Dataset structure

For each case:

```text
Evidence package
Original claim
Context
JEV decision
Expert decision
Expert confidence
Expert rationale
```

## Annotation task

Give experts the evidence package without revealing JEV's decision.

Ask them to select:

- support
- contradiction
- partial
- conditional
- confound
- unknown
- novel
- escalate

Then collect their rationale.

## Minimum pilot

Start with 25–50 cases.

Use cases drawn from the existing five research runs plus deliberately constructed synthetic disagreements.

## Agreement measures

Calculate:

- exact agreement
- Cohen's kappa for two raters where appropriate
- Fleiss' kappa for multiple raters where appropriate
- confusion matrix
- calibration/reliability curves for any confidence output

Do not optimize only for raw agreement.

Track which categories JEV systematically overuses or underuses.

## Expert disagreement

When experts disagree, preserve disagreement as data.

Do not force a false ground truth.

A calibrated result can be:

```text
Experts split 3–2
JEV = conditional
```

That is useful information.

---

# 9. Phase 4 — Persistence and Provenance

## Objective

Make every research conclusion traceable backward to the exact inputs and forward to the next research state.

## Required identifiers

Every object receives a stable ID:

```text
research_case_id
cycle_id
artifact_id
claim_id
evidence_id
hypothesis_id
experiment_id
theory_version
model_run_id
```

## Lineage graph

Every claim should be able to answer:

> Where did this come from?

Example:

```text
Claim C-17
  ← Evidence E-42
      ← Result R-42
          ← Experiment X-09
              ← Prediction P-09
                  ← Hypothesis H-09
                      ← Inversion I-09
                          ← Assumption A-09
                              ← Problem Q-09
```

## Provenance fields

Record:

- model/provider
- model version if available
- system prompt/version
- skill version
- tool versions
- git commit
- dataset hash
- code hash
- configuration hash
- random seed
- timestamp
- execution environment
- human approvals

## Immutable rule

Past research states are append-only.

A correction creates:

```text
Theory v1
→ Amendment v1.1
→ Theory v2
```

not a silent overwrite.

---

# 10. Phase 5 — Recursive Re-Entry

## Objective

Complete the research loop by feeding the result back into the system.

Every run must produce three evidence layers:

### One-paragraph Evidence Summary

Answers:

> What did the experiment actually show?

### Full Research Overview

Contains:

- problem
- assumptions
- inversions
- mechanisms
- hypothesis
- prediction
- experiment
- results
- limits

### Detailed Evidence Breakdown

Contains individual findings with:

- measurement
- comparison
- source
- uncertainty
- contradictions
- scope

Then JEV processes those layers.

Then the re-entry engine creates:

```text
Updated Theory
Remaining Unknowns
Rejected Mechanisms
New Conditions
Next Hypothesis
Next Experiment
```

## Critical invariant

The updated theory must be derived from the evidence package.

It cannot simply be the original theory restated with stronger language.

---

# 11. Phase 6 — Real Research Cycles

## Objective

Move from benchmark simulations to real public research datasets and reproducible published questions.

## Selection rule

Use research problems with:

- public data,
- executable analysis,
- clear outcome variables,
- manageable computational requirements,
- and established comparison methods where possible.

## First three real cycles

### Cycle A — Astronomy

Take the synthetic transit-window result into real public light curves.

Goal:

Determine whether the synthetic detrending bias survives contact with real photometric structure.

### Cycle B — Ecology

Take the population-predictability hypothesis into real ecological time series.

Goal:

Determine whether the synthetic variability/predictability relationship survives real ecological noise and richer forecasting models.

### Cycle C — Epidemiology

Take the network-heterogeneity result into a public contact-network dataset or a published network benchmark.

Goal:

Determine whether the synthetic hub/heterogeneity effect persists in empirical topology.

These are validation cycles, not guaranteed confirmations.

---

# 12. Phase 7 — Blind Domain Challenge

After the controlled real-data cycles, give the system a problem from a domain that has not been preselected for the framework.

The operator supplies only:

```text
Domain
Problem
Available data/tools
Constraints
```

The system must independently construct:

```text
assumptions
inversion
competing mechanisms
hypothesis
prediction
experiment
analysis
result
updated theory
next test
```

The operator must not inject the preferred mechanism.

This becomes the cleanest test of whether the framework itself generalizes.

---

# 13. Phase 8 — Freebuff Execution Workflow

For each research cycle:

### Step 1

Create a new Git branch:

```text
research/DRB-00X-domain-topic
```

### Step 2

Ask Freebuff to implement only the preregistered experimental design.

### Step 3

Run tests before execution.

### Step 4

Execute the experiment.

### Step 5

Save raw results.

### Step 6

Have a separate review pass inspect the implementation and outputs.

### Step 7

Commit everything needed for reproduction.

### Step 8

Return the complete evidence package to Hermes.

---

# 14. Hermes Research Workflow

For every cycle create a persistent Hermes research case.

Suggested skill structure:

```text
~/.hermes/skills/
  ail-research/
  moie-research/
  jev-evidence/
  reproducibility/
  domain-adapters/
```

The `ail-research` skill should teach the state sequence.

The `moie-research` skill should teach the five research roles.

The `jev-evidence` skill should contain the current decision procedure.

The `reproducibility` skill should enforce provenance and archival requirements.

Domain adapters should be separate so that the core method remains stable.

Hermes skills are designed to be reusable, progressively loaded, and agent-managed, which is well aligned with this separation between a stable core method and domain-specific capability packs. citeturn200642search7

---

# 15. Low-Cost Operating Mode

Because API budget is currently constrained, do not build the 100-agent architecture first.

Use:

```text
1 Human
   ↓
10 low-cost/local research workers
   ↓
1 synthesis/reasoning worker
   ↓
JEV
   ↓
Human
```

The 10 workers can be parallel Freebuff/Hermes tasks where resources permit.

Use the strongest model only for:

- synthesis,
- conflict resolution,
- difficult domain translation,
- or final research review.

Use cheaper/local models for:

- extraction,
- formatting,
- code scaffolding,
- repetitive analysis,
- and evidence packaging.

The point is to validate **architecture**, not spend tokens proving that tokens can be spent.

---

# 16. End-to-End Acceptance Test

The implementation is ready when one command can create a new case:

```bash
ailmoie new-case "research question"
```

and produce:

```text
case.json
preregistration.json
hypotheses.json
experiment/
results/raw.json
results/summary.md
evidence/summary.md
evidence/detail.json
jev/decision.json
theory/version-2.json
reentry/next-test.json
provenance/lineage.json
```

The entire package should be sufficient for another operator to understand:

1. what was asked;
2. what was assumed;
3. what was inverted;
4. what was hypothesized;
5. what was tested;
6. what actually happened;
7. what JEV concluded about the evidence;
8. what changed in the theory;
9. and what should be tested next.

---

# 17. Success Criteria

## Engineering

- schema validation passes;
- all state transitions are guarded;
- provenance is complete;
- persistence survives process restart;
- historical records remain immutable;
- end-to-end execution is reproducible.

## JEV

- deterministic on identical inputs/configuration;
- expert disagreement is preserved;
- calibration dataset exists;
- systematic routing errors are measurable;
- thresholds remain configurable and versioned.

## Research

- at least five preserved benchmark runs;
- at least three real-data research cycles;
- every cycle has a falsification criterion;
- every cycle produces evidence and an updated theory;
- failed hypotheses remain archived.

## Human usability

A human should be able to understand the state of a research cycle without reading every model transcript.

The top-level interface should expose:

```text
Problem
Current Theory
What Changed
Evidence Strength
Conflicts
Unknowns
Next Experiment
```

---

# 18. What Not to Build Yet

Do not begin with:

- 100+ agents;
- complicated distributed infrastructure;
- autonomous research swarms without persistence;
- automatic expert replacement claims;
- elaborate dashboards;
- custom model training;
- expensive API routing;
- unrestricted autonomous execution.

First validate the minimum recursive loop.

The architecture should become larger only when measurement shows that a larger architecture solves a demonstrated bottleneck.

---

# 19. Final Research Proposition

The system is investigating a concrete capability:

> **Can a human supply a problem and have an AI-mediated research system transform that problem into a falsifiable hypothesis, execute an appropriate test, synthesize the evidence, route the result, update the working theory, and generate the next research cycle?**

The system should not be judged by whether every hypothesis is correct.

It should be judged by whether the loop reliably converts uncertainty into progressively better-tested knowledge.

That is the artifact to preserve in GitHub.

---

# 20. Recommended Build Order

```text
1. Freeze DRB-001..005
2. Complete reference implementation
3. Add persistence + provenance
4. Implement deterministic JEV v1
5. Run 25–50-case expert calibration
6. Repair JEV from calibration findings
7. Add Hermes research skills + memory
8. Add Freebuff execution harness
9. Run real astronomy cycle
10. Run real ecology cycle
11. Run real epidemiology cycle
12. Run blind-domain cycle
13. Publish benchmark corpus
14. Only then test 10→1 and 100→10→1 scaling
```

## Final Principle

**Do not scale the number of agents until the research loop itself is stable.**

Scale:

**questions → experiments → evidence → knowledge**

not:

**agents → tokens → transcripts**.
