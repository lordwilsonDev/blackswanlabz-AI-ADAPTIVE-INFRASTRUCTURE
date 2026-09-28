import unittest

from reference_implementation import (
    EvidenceItem,
    Hypothesis,
    Prediction,
    Problem,
    Relation,
    ResearchCycle,
    State,
    decide_jev,
    uid,
)


class TestJEV(unittest.TestCase):
    def test_unknown_without_evidence(self):
        d = decide_jev("run", "hyp", [])
        self.assertEqual(d.relation, Relation.UNKNOWN)
        self.assertFalse(d.promote)

    def test_strong_support(self):
        e = EvidenceItem(
            id=uid("ev"), run_id="run", claim="supports hypothesis", source_type="executed_code",
            directness=1, reproducibility=1, independence=1,
            method_quality=1, confound_control=1, consistency=1,
            supports=["hyp"]
        )
        d = decide_jev("run", "hyp", [e])
        self.assertEqual(d.relation, Relation.EQUAL)
        self.assertTrue(d.promote)

    def test_conditional_support_when_scope_bounded(self):
        e = EvidenceItem(
            id=uid("ev"), run_id="run", claim="supports hypothesis in N=1000 simulations", source_type="synthetic_data",
            directness=1, reproducibility=1, independence=1,
            method_quality=1, confound_control=1, consistency=1,
            supports=["hyp"], scope_key="N=1000|static"
        )
        d = decide_jev("run", "hyp", [e])
        self.assertEqual(d.relation, Relation.CONDITIONAL)
        self.assertTrue(d.promote)

    def test_not_equal(self):
        e = EvidenceItem(
            id=uid("ev"), run_id="run", claim="contradicts hypothesis", source_type="executed_code",
            directness=1, reproducibility=1, independence=1,
            method_quality=1, confound_control=1, consistency=1,
            contradicts=["hyp"]
        )
        d = decide_jev("run", "hyp", [e])
        self.assertEqual(d.relation, Relation.NOT_EQUAL)
        self.assertFalse(d.promote)

    def test_confound_preserves_disagreement(self):
        support = EvidenceItem(
            id=uid("ev"), run_id="run", claim="support", source_type="executed_code",
            directness=1, reproducibility=1, independence=1,
            method_quality=1, confound_control=0.8, consistency=0.8,
            supports=["hyp"]
        )
        contradiction = EvidenceItem(
            id=uid("ev"), run_id="run", claim="contradiction", source_type="executed_code",
            directness=1, reproducibility=1, independence=1,
            method_quality=1, confound_control=0.8, consistency=0.8,
            contradicts=["hyp"]
        )
        d = decide_jev("run", "hyp", [support, contradiction])
        self.assertEqual(d.relation, Relation.CONFOUND)
        self.assertFalse(d.promote)


class TestStateMachine(unittest.TestCase):
    def setUp(self):
        self.problem = Problem(
            id=uid("problem"), domain="test", question="q", objective="o"
        )
        self.cycle = ResearchCycle(uid("run"), self.problem)

    def build_to_preregistered(self):
        self.cycle.define_problem()
        h = Hypothesis(
            id=uid("hyp"), problem_id=self.problem.id,
            null="H0", primary="H1", alternatives=["A"],
            falsification_criteria=["criterion"]
        )
        self.cycle.form_hypothesis(h)
        self.cycle.preregister([
            Prediction(uid("pred"), h.id, "metric", "increase", 0.1, "x", True)
        ])

    def test_illegal_jump_rejected(self):
        with self.assertRaises(Exception):
            self.cycle.start_execution()

    def test_preregistration_freezes_predictions(self):
        self.build_to_preregistered()
        with self.assertRaises(PermissionError):
            self.cycle.edit_predictions([])

    def test_negative_evidence_cycle_can_finish(self):
        self.build_to_preregistered()
        self.cycle.ready()
        self.cycle.start_execution()
        self.cycle.record_results({"ok": True})
        h = self.cycle.hypothesis
        e = EvidenceItem(
            id=uid("ev"), run_id=self.cycle.id, claim="negative", source_type="executed_code",
            directness=1, reproducibility=1, independence=1,
            method_quality=1, confound_control=1, consistency=1,
            contradicts=[h.id]
        )
        self.cycle.synthesize_evidence([e])
        d = self.cycle.evaluate_jev()
        self.assertEqual(d.relation, Relation.NOT_EQUAL)
        self.cycle.update_theory(
            updated_theory="H1 unsupported in this setup",
            what_changed=["directional advantage absent"],
            boundary_conditions=["tested benchmark only"],
            remaining_unknowns=["composition confound"],
            new_hypothesis="H2", next_experiment="composition-matched control"
        )
        self.cycle.reentry()
        self.cycle.archive()
        self.assertEqual(self.cycle.state, State.COMPLETE)


if __name__ == "__main__":
    unittest.main()
