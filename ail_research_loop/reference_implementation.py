"""AIL + MoIE Recursive Research Protocol - reference implementation.

Standard-library-only implementation of:
- state machine + transition guards
- evidence weighting
- JEV decision procedure
- theory update / recursive re-entry envelope

This is intentionally a small, inspectable reference implementation.
It does not execute domain experiments itself; it governs the research record
around such experiments.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterable
import json
import math
import uuid


SCHEMA_VERSION = "1.0"
QUALITY_GATE = 0.60
PROMOTE_THRESHOLD = 0.70
CONTRADICTION_THRESHOLD = 0.70
MATERIAL_CONFOUND_THRESHOLD = 0.30
MARGIN_THRESHOLD = 0.15


class State(str, Enum):
    DRAFT = "DRAFT"
    PROBLEM_DEFINED = "PROBLEM_DEFINED"
    HYPOTHESIS_FORMED = "HYPOTHESIS_FORMED"
    PREREGISTERED = "PREREGISTERED"
    READY_TO_EXECUTE = "READY_TO_EXECUTE"
    EXECUTING = "EXECUTING"
    RESULTS_AVAILABLE = "RESULTS_AVAILABLE"
    EVIDENCE_SYNTHESIZED = "EVIDENCE_SYNTHESIZED"
    JEV_EVALUATED = "JEV_EVALUATED"
    THEORY_UPDATED = "THEORY_UPDATED"
    REENTRY_READY = "REENTRY_READY"
    COMPLETE = "COMPLETE"
    BLOCKED = "BLOCKED"
    FAILED_EXECUTION = "FAILED_EXECUTION"
    INVALIDATED = "INVALIDATED"


class Relation(str, Enum):
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    PARTIAL = "PARTIAL"
    CONDITIONAL = "CONDITIONAL"
    CONFOUND = "CONFOUND"
    UNKNOWN = "UNKNOWN"
    NOVEL = "NOVEL"


SOURCE_MULTIPLIER = {
    "executed_code": 1.00,
    "real_dataset": 1.00,
    "human_observation": 0.90,
    "synthetic_data": 0.80,
    "literature": 0.75,
    "model_assertion": 0.20,
}


@dataclass
class Problem:
    id: str
    domain: str
    question: str
    objective: str
    constraints: list[str] = field(default_factory=list)
    available_data: list[str] = field(default_factory=list)
    available_tools: list[str] = field(default_factory=list)
    version: str = SCHEMA_VERSION
    created_at: str = field(default_factory=lambda: now_iso())


@dataclass
class Hypothesis:
    id: str
    problem_id: str
    null: str
    primary: str
    alternatives: list[str]
    falsification_criteria: list[str]
    mechanism: str = ""
    version: str = SCHEMA_VERSION
    created_at: str = field(default_factory=lambda: now_iso())


@dataclass
class Prediction:
    id: str
    hypothesis_id: str
    outcome: str
    direction: str
    threshold: float | None = None
    unit: str = ""
    preregistered: bool = True


@dataclass
class EvidenceItem:
    id: str
    run_id: str
    claim: str
    source_type: str
    directness: float
    reproducibility: float
    independence: float
    method_quality: float
    confound_control: float
    consistency: float
    supports: list[str] = field(default_factory=list)
    contradicts: list[str] = field(default_factory=list)
    contradictory: bool = False
    value: Any = None
    metric: str = ""
    artifact_refs: list[str] = field(default_factory=list)
    scope_key: str = ""

    def validate(self) -> None:
        if self.source_type not in SOURCE_MULTIPLIER:
            raise ValueError(f"Unknown source_type: {self.source_type}")
        for name in (
            "directness",
            "reproducibility",
            "independence",
            "method_quality",
            "confound_control",
            "consistency",
        ):
            value = getattr(self, name)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0,1], got {value!r}")


@dataclass
class JEVDecision:
    id: str
    run_id: str
    relation: Relation
    support_score: float
    contradiction_score: float
    quality_score: float
    decision_margin: float
    promote: bool
    reentry_required: bool
    rationale: str
    evidence_ids: list[str]


@dataclass
class TheoryUpdate:
    id: str
    run_id: str
    original_theory: str
    updated_theory: str
    what_changed: list[str]
    boundary_conditions: list[str]
    remaining_unknowns: list[str]
    new_hypothesis: str | None
    next_experiment: str | None


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def uid(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def evidence_quality(e: EvidenceItem) -> float:
    """Base evidence quality before source-type multiplier."""
    return clamp01(
        0.25 * e.directness
        + 0.20 * e.reproducibility
        + 0.15 * e.independence
        + 0.20 * e.method_quality
        + 0.10 * e.confound_control
        + 0.10 * e.consistency
    )


def weighted_evidence(e: EvidenceItem) -> float:
    e.validate()
    return evidence_quality(e) * SOURCE_MULTIPLIER[e.source_type]


def _weighted_mean(items: Iterable[tuple[float, float]]) -> float:
    pairs = list(items)
    denom = sum(weight for _, weight in pairs)
    if denom <= 0:
        return 0.0
    return sum(value * weight for value, weight in pairs) / denom


def _is_supporting(e: EvidenceItem, hypothesis_id: str) -> bool:
    return hypothesis_id in e.supports and hypothesis_id not in e.contradicts


def _is_contradicting(e: EvidenceItem, hypothesis_id: str) -> bool:
    return e.contradictory or hypothesis_id in e.contradicts


def _has_novel_claim(e: EvidenceItem) -> bool:
    # Reference rule: caller can mark novelty explicitly in claim text using a prefix.
    return e.claim.strip().upper().startswith("NOVEL:")


def _scope_is_bounded(evidence: list[EvidenceItem]) -> bool:
    """Conservative default: bounded scope is declared by a nonempty shared scope_key."""
    scopes = {e.scope_key for e in evidence if e.scope_key}
    return bool(scopes)


def decide_jev(
    run_id: str,
    hypothesis_id: str,
    evidence: list[EvidenceItem],
    *,
    quality_gate: float = QUALITY_GATE,
    promote_threshold: float = PROMOTE_THRESHOLD,
    contradiction_threshold: float = CONTRADICTION_THRESHOLD,
    material_confound_threshold: float = MATERIAL_CONFOUND_THRESHOLD,
    margin_threshold: float = MARGIN_THRESHOLD,
) -> JEVDecision:
    """Apply the deterministic JEV decision procedure.

    The procedure intentionally uses conservative ordering:
    UNKNOWN -> NOVEL -> CONFOUND -> CONDITIONAL -> EQUAL/NOT_EQUAL/PARTIAL.
    """
    for e in evidence:
        e.validate()

    if not evidence:
        return JEVDecision(
            id=uid("jev"),
            run_id=run_id,
            relation=Relation.UNKNOWN,
            support_score=0.0,
            contradiction_score=0.0,
            quality_score=0.0,
            decision_margin=0.0,
            promote=False,
            reentry_required=True,
            rationale="No relevant evidence was supplied.",
            evidence_ids=[],
        )

    relevant = [e for e in evidence if _is_supporting(e, hypothesis_id) or _is_contradicting(e, hypothesis_id)]
    if not relevant:
        relevant = evidence

    support_weights = [weighted_evidence(e) for e in relevant if _is_supporting(e, hypothesis_id)]
    contradiction_weights = [weighted_evidence(e) for e in relevant if _is_contradicting(e, hypothesis_id)]
    total_weight = sum(weighted_evidence(e) for e in relevant)

    support_score = clamp01(sum(support_weights) / total_weight) if total_weight else 0.0
    contradiction_score = clamp01(sum(contradiction_weights) / total_weight) if total_weight else 0.0
    quality_score = _weighted_mean((evidence_quality(e), weighted_evidence(e)) for e in relevant)
    margin = support_score - contradiction_score

    novel = any(_has_novel_claim(e) for e in relevant)
    contradiction_high = contradiction_score >= material_confound_threshold
    support_high = support_score >= material_confound_threshold
    both_material = support_high and contradiction_high

    rationale_parts: list[str] = []
    if novel:
        relation = Relation.NOVEL
        promote = False
        rationale_parts.append("At least one evidence item is explicitly marked NOVEL.")
    elif both_material and abs(margin) < margin_threshold:
        relation = Relation.CONFOUND
        promote = False
        rationale_parts.append("Material support and contradiction remain unresolved within the decision margin.")
    elif quality_score < quality_gate:
        relation = Relation.UNKNOWN
        promote = False
        rationale_parts.append(f"Mean evidence quality {quality_score:.3f} is below gate {quality_gate:.3f}.")
    elif _scope_is_bounded(relevant) and support_score >= promote_threshold and contradiction_score < contradiction_threshold:
        relation = Relation.CONDITIONAL
        promote = True
        rationale_parts.append("Support clears the promotion threshold but evidence is explicitly scope-bounded.")
    elif support_score >= promote_threshold and contradiction_score < contradiction_threshold and margin >= margin_threshold:
        relation = Relation.EQUAL
        promote = True
        rationale_parts.append("Support clears the promotion threshold, contradiction is low, and the margin is material.")
    elif contradiction_score >= contradiction_threshold and support_score < 0.30 and quality_score >= quality_gate:
        relation = Relation.NOT_EQUAL
        promote = False
        rationale_parts.append("Contradictory evidence clears the contradiction threshold while support remains low.")
    elif support_score > 0.0 and support_score < promote_threshold and contradiction_score < material_confound_threshold:
        relation = Relation.PARTIAL
        promote = False
        rationale_parts.append("Evidence supports part of the claim but does not justify promotion.")
    elif both_material:
        relation = Relation.CONFOUND
        promote = False
        rationale_parts.append("Competing mechanisms remain materially unresolved.")
    else:
        relation = Relation.UNKNOWN
        promote = False
        rationale_parts.append("Evidence does not meet a promotion or falsification rule.")

    rationale_parts.append(
        f"support={support_score:.3f}, contradiction={contradiction_score:.3f}, "
        f"quality={quality_score:.3f}, margin={margin:.3f}."
    )

    return JEVDecision(
        id=uid("jev"),
        run_id=run_id,
        relation=relation,
        support_score=round(support_score, 6),
        contradiction_score=round(contradiction_score, 6),
        quality_score=round(quality_score, 6),
        decision_margin=round(margin, 6),
        promote=promote,
        reentry_required=True,
        rationale=" ".join(rationale_parts),
        evidence_ids=[e.id for e in relevant],
    )


ALLOWED_TRANSITIONS: dict[State, set[State]] = {
    State.DRAFT: {State.PROBLEM_DEFINED, State.INVALIDATED, State.BLOCKED},
    State.PROBLEM_DEFINED: {State.HYPOTHESIS_FORMED, State.INVALIDATED, State.BLOCKED},
    State.HYPOTHESIS_FORMED: {State.PREREGISTERED, State.INVALIDATED, State.BLOCKED},
    State.PREREGISTERED: {State.READY_TO_EXECUTE, State.BLOCKED, State.INVALIDATED},
    State.READY_TO_EXECUTE: {State.EXECUTING, State.BLOCKED, State.INVALIDATED},
    State.EXECUTING: {State.RESULTS_AVAILABLE, State.FAILED_EXECUTION, State.BLOCKED},
    State.FAILED_EXECUTION: {State.READY_TO_EXECUTE, State.INVALIDATED, State.BLOCKED},
    State.RESULTS_AVAILABLE: {State.EVIDENCE_SYNTHESIZED, State.INVALIDATED, State.BLOCKED},
    State.EVIDENCE_SYNTHESIZED: {State.JEV_EVALUATED, State.INVALIDATED, State.BLOCKED},
    State.JEV_EVALUATED: {State.THEORY_UPDATED, State.INVALIDATED, State.BLOCKED},
    State.THEORY_UPDATED: {State.REENTRY_READY, State.INVALIDATED, State.BLOCKED},
    State.REENTRY_READY: {State.COMPLETE, State.PROBLEM_DEFINED, State.BLOCKED},
    State.COMPLETE: set(),
    State.BLOCKED: {State.DRAFT, State.PROBLEM_DEFINED, State.HYPOTHESIS_FORMED, State.PREREGISTERED, State.READY_TO_EXECUTE, State.EXECUTING, State.RESULTS_AVAILABLE, State.EVIDENCE_SYNTHESIZED, State.JEV_EVALUATED, State.THEORY_UPDATED, State.REENTRY_READY},
    State.INVALIDATED: set(),
}


class IllegalTransition(ValueError):
    pass


@dataclass
class ResearchCycle:
    id: str
    problem: Problem
    state: State = State.DRAFT
    hypothesis: Hypothesis | None = None
    predictions: list[Prediction] = field(default_factory=list)
    evidence: list[EvidenceItem] = field(default_factory=list)
    jev: JEVDecision | None = None
    theory_update: TheoryUpdate | None = None
    history: list[tuple[str, str, str]] = field(default_factory=list)
    frozen_preregistration: bool = False
    completed_results: Any = None

    def _transition(self, target: State, reason: str) -> None:
        if target not in ALLOWED_TRANSITIONS[self.state]:
            raise IllegalTransition(f"{self.state.value} -> {target.value} is not allowed")
        self.history.append((self.state.value, target.value, reason))
        self.state = target

    def define_problem(self) -> None:
        if not self.problem.domain or not self.problem.question or not self.problem.objective:
            raise ValueError("Problem requires domain, question, and objective")
        self._transition(State.PROBLEM_DEFINED, "problem validated")

    def form_hypothesis(self, hypothesis: Hypothesis) -> None:
        if hypothesis.problem_id != self.problem.id:
            raise ValueError("Hypothesis problem_id mismatch")
        if not hypothesis.primary or not hypothesis.null or not hypothesis.falsification_criteria:
            raise ValueError("Hypothesis requires primary, null, and falsification criteria")
        self.hypothesis = hypothesis
        self._transition(State.HYPOTHESIS_FORMED, "hypothesis and falsification criteria recorded")

    def preregister(self, predictions: list[Prediction]) -> None:
        if self.hypothesis is None:
            raise ValueError("Cannot preregister without hypothesis")
        if not predictions:
            raise ValueError("At least one prediction is required")
        if any(not p.preregistered for p in predictions):
            raise ValueError("All predictions must be preregistered")
        if any(p.hypothesis_id != self.hypothesis.id for p in predictions):
            raise ValueError("Prediction hypothesis_id mismatch")
        self.predictions = list(predictions)
        self.frozen_preregistration = True
        self._transition(State.PREREGISTERED, "predictions frozen")

    def edit_predictions(self, predictions: list[Prediction]) -> None:
        if self.frozen_preregistration:
            raise PermissionError("Preregistered predictions are immutable; create a new version/cycle")
        self.predictions = list(predictions)

    def ready(self) -> None:
        if self.state != State.PREREGISTERED:
            raise IllegalTransition("Cycle must be PREREGISTERED before READY_TO_EXECUTE")
        self._transition(State.READY_TO_EXECUTE, "experiment prerequisites satisfied")

    def start_execution(self) -> None:
        self._transition(State.EXECUTING, "execution started")

    def record_results(self, results: Any) -> None:
        if self.state != State.EXECUTING:
            raise IllegalTransition("Results can only be recorded from EXECUTING")
        self.completed_results = results
        self._transition(State.RESULTS_AVAILABLE, "raw results recorded")

    def record_execution_failure(self, error: str) -> None:
        if self.state != State.EXECUTING:
            raise IllegalTransition("Execution failure can only be recorded from EXECUTING")
        self.completed_results = {"error": error}
        self._transition(State.FAILED_EXECUTION, "execution failed")

    def synthesize_evidence(self, evidence: list[EvidenceItem]) -> None:
        if self.hypothesis is None:
            raise ValueError("Hypothesis missing")
        if self.state != State.RESULTS_AVAILABLE:
            raise IllegalTransition("Evidence synthesis requires RESULTS_AVAILABLE")
        for item in evidence:
            item.validate()
        self.evidence = list(evidence)
        self._transition(State.EVIDENCE_SYNTHESIZED, "evidence normalized")

    def evaluate_jev(self) -> JEVDecision:
        if self.hypothesis is None:
            raise ValueError("Hypothesis missing")
        if self.state != State.EVIDENCE_SYNTHESIZED:
            raise IllegalTransition("JEV requires EVIDENCE_SYNTHESIZED")
        self.jev = decide_jev(self.id, self.hypothesis.id, self.evidence)
        self._transition(State.JEV_EVALUATED, "JEV classification completed")
        return self.jev

    def update_theory(
        self,
        updated_theory: str,
        what_changed: list[str],
        boundary_conditions: list[str],
        remaining_unknowns: list[str],
        new_hypothesis: str | None,
        next_experiment: str | None,
    ) -> TheoryUpdate:
        if self.hypothesis is None or self.jev is None:
            raise ValueError("Hypothesis and JEV decision required")
        if self.state != State.JEV_EVALUATED:
            raise IllegalTransition("Theory update requires JEV_EVALUATED")
        update = TheoryUpdate(
            id=uid("theory"),
            run_id=self.id,
            original_theory=self.hypothesis.primary,
            updated_theory=updated_theory,
            what_changed=what_changed,
            boundary_conditions=boundary_conditions,
            remaining_unknowns=remaining_unknowns,
            new_hypothesis=new_hypothesis,
            next_experiment=next_experiment,
        )
        self.theory_update = update
        self._transition(State.THEORY_UPDATED, "theory updated from evidence")
        return update

    def reentry(self) -> None:
        if self.state != State.THEORY_UPDATED:
            raise IllegalTransition("Re-entry requires THEORY_UPDATED")
        if self.theory_update is None:
            raise ValueError("Theory update missing")
        if not self.theory_update.new_hypothesis and not self.theory_update.next_experiment:
            self._transition(State.REENTRY_READY, "explicit stop condition")
        else:
            self._transition(State.REENTRY_READY, "next research cycle materialized")

    def archive(self) -> None:
        if self.state != State.REENTRY_READY:
            raise IllegalTransition("Only REENTRY_READY cycles may be archived")
        self._transition(State.COMPLETE, "immutable archive created")

    def resume_after_failure(self) -> None:
        if self.state != State.FAILED_EXECUTION:
            raise IllegalTransition("Only FAILED_EXECUTION can be resumed")
        self._transition(State.READY_TO_EXECUTE, "execution plan repaired/versioned")

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "version": SCHEMA_VERSION,
            "problem": asdict(self.problem),
            "state": self.state.value,
            "hypothesis": asdict(self.hypothesis) if self.hypothesis else None,
            "predictions": [asdict(p) for p in self.predictions],
            "evidence": [asdict(e) for e in self.evidence],
            "jev": {
                **asdict(self.jev),
                "relation": self.jev.relation.value,
            } if self.jev else None,
            "theory_update": asdict(self.theory_update) if self.theory_update else None,
            "history": self.history,
            "frozen_preregistration": self.frozen_preregistration,
            "completed_results": self.completed_results,
        }


def to_json(obj: Any) -> str:
    return json.dumps(obj.as_dict() if hasattr(obj, "as_dict") else asdict(obj), indent=2, sort_keys=True, default=str)


if __name__ == "__main__":
    # Minimal smoke demonstration of the protocol.
    problem = Problem(
        id=uid("problem"),
        domain="software_testing",
        question="Does targeting behavioral assumption boundaries improve mutation detection?",
        objective="Measure mutation kill-rate difference under equal mutation budgets.",
    )
    cycle = ResearchCycle(id=uid("run"), problem=problem)
    cycle.define_problem()
    hypothesis = Hypothesis(
        id=uid("hyp"),
        problem_id=problem.id,
        null="Assumption-targeted mutation does not improve kill rate.",
        primary="Assumption-targeted mutation improves kill rate under equal budgets.",
        alternatives=["Any improvement is caused by mutation-type composition."],
        falsification_criteria=["No effect or negative effect across preregistered matched trials."],
        mechanism="Tests that target behavioral boundaries expose faults missed by structurally broad selection.",
    )
    cycle.form_hypothesis(hypothesis)
    cycle.preregister([
        Prediction(uid("pred"), hypothesis.id, "mutation_kill_rate", "increase", 0.01, "absolute", True)
    ])
    cycle.ready()
    cycle.start_execution()
    cycle.record_results({"executed": True, "trials": 100})
    cycle.synthesize_evidence([
        EvidenceItem(
            id=uid("ev"),
            run_id=cycle.id,
            claim="ATMS kill rate was 0.80 vs random 0.84.",
            source_type="executed_code",
            directness=1.0,
            reproducibility=0.9,
            independence=0.8,
            method_quality=0.9,
            confound_control=0.7,
            consistency=0.8,
            contradicts=[hypothesis.id],
        )
    ])
    print(to_json(cycle))
