# AIL CSM Harness — File Manifest

21-file skillpack. Each file has one responsibility. Load only what you need; the full harness is the union.

| # | File | Purpose | Inputs | Outputs |
|---|------|---------|--------|---------|
| 1 | README.md | Package overview, quick start, reading order, core principle | None | Orientation |
| 2 | MANIFEST.md | File inventory with purpose, inputs, outputs | None | Inventory map |
| 3 | 01_problem_intake.md | Intake criteria: what makes a problem suitable for CSM | Problem statement | Suitable / unsuitable verdict |
| 4 | 02_assumption_inventory.md | Assumption elicitation, load-bearing selection, catalog format | Problem framing | Assumption catalog |
| 5 | 03_axiom_inversion.md | Inversion method: stages, examples, falsification conditions | Load-bearing assumption | Inverted hypothesis space |
| 6 | 04_rederivation.md | Re-deriving hypothesis from inverted assumption | Inverted assumption | Candidate hypotheses |
| 7 | 05_moie_mechanisms.md | Five MoIE roles, competing mechanisms, discrimination design | Candidate hypotheses | Mechanism set + test design |
| 8 | 06_hypothesis.md | Hypothesis formulation, falsifiability, H0/H1/alternatives | Mechanism set | Hypothesis spec |
| 9 | 07_prediction.md | Preregistered predictions, frozen before execution | Hypothesis spec | Prediction package |
| 10 | 08_experimental_design.md | Controls, parameters, metrics, replication, statistical plan | Prediction package | Experimental design spec |
| 11 | 09_execution.md | Code execution, determinism, seeds, reproducibility | Design spec | Raw results + code |
| 12 | 10_raw_results.md | Raw output preservation, no silent editing | Executed output | Preserved raw artifact |
| 13 | 11_statistical_results.md | Analysis, uncertainty, confidence, effect thresholds | Raw results | Statistical results |
| 14 | 12_jev_routing.md | JEV decision procedure, evidence object, weights, thresholds | Raw + statistical results | JEV decision |
| 15 | 13_evidence_synthesis.md | Three evidence layers: summary, overview, detailed breakdown | JEV decision + results | Evidence package |
| 16 | 14_theory_update.md | Updated theory, remaining unknowns, next-test lineage | Evidence package | Updated theory |
| 17 | 15_recursive_reentry.md | Re-entry protocol, re-entry invariants | Updated theory | Next-cycle proposal |
| 18 | 16_provenance.md | Lineage graph, immutable records, amendment discipline | Full case record | Provenance ledger |
| 19 | 17_human_escalation.md | When to escalate, what to ask, authority boundaries | Case + flags | Escalation record |
| 20 | 18_state_machine.md | Full 13-state spec with guarded transitions and invariants | State + artifact state | Transition verdict |
| 21 | 19_cross_domain_validation.md | Cross-domain validation template; includes two domain case appendices | Completed cases | Validation record |

## Load order for first pass

Read in file-number order.

## Load order for a working operator

Core loop: 01 → 02 → 03 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14 → 15

Governance: 16, 17

Enforcement: 18

Template: 19
