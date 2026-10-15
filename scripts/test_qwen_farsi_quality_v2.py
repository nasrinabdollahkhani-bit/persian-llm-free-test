#!/usr/bin/env python3
"""No-download / no-model unit contracts for the public Qwen Persian v2 candidate."""
import importlib
import unittest


class QualityV2ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q = importlib.import_module("qwen_farsi_quality_v2")
        cls.baseline = importlib.import_module("local_qwen_fa_smoke")

    def test_exactly_ten_synthetic_questions(self):
        self.assertEqual(len(self.q.PROMPTS), 10)
        self.assertEqual(len(set(self.q.PROMPTS)), 10)

    def test_first_five_prompts_identical_to_successful_baseline(self):
        self.assertEqual(self.q.PROMPTS[:5], self.baseline.PROMPTS[:5])

    def test_all_ten_prompts_identical_to_existing_generic_suite(self):
        self.assertEqual(self.q.PROMPTS, self.baseline.PROMPTS)

    def test_model_pinned_identically(self):
        self.assertEqual(self.q.EXPECTED_SHA256["model.safetensors"],
                         self.baseline.EXPECTED_SHA256["model.safetensors"])
        self.assertEqual(self.q.EXPECTED_SHA256["tokenizer.json"],
                         self.baseline.EXPECTED_SHA256["tokenizer.json"])
        self.assertEqual(len(self.q.EXPECTED_SHA256), 7)

    def test_sampling_matches_upstream_non_thinking_suggestion(self):
        p = self.q.GENERATION
        self.assertIs(p["do_sample"], True)
        self.assertEqual(p["temperature"], 0.7)
        self.assertEqual(p["top_p"], 0.8)
        self.assertEqual(p["top_k"], 20)
        self.assertLessEqual(p["max_new_tokens"], 160)

    def test_no_thinking_few_shot_contract(self):
        messages = self.q.build_messages("آزمون مصنوعی")
        self.assertEqual([x["role"] for x in messages],
                         ["system", "user", "assistant", "user"])
        self.assertEqual(messages[-1]["content"], "آزمون مصنوعی")
        self.assertIn("دسترسی نداری", messages[0]["content"])

    def test_heuristics_are_not_semantic_pass(self):
        result = self.q.observable_only("سلام")
        self.assertTrue(result["short_response_flag"])
        self.assertNotIn("pass", str(result).lower())
        self.assertGreater(result["persian_codepoint_count"], 0)

    def test_unique_seeds_and_stable_profile(self):
        seeds = [self.q.SEED + i for i in range(1, 11)]
        self.assertEqual(len(seeds), len(set(seeds)))
        self.assertIn("V2", self.q.PROFILE)


if __name__ == "__main__":
    unittest.main()
