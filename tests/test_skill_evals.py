from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('run_skill_evals', ROOT / 'scripts/run_skill_evals.py')
assert SPEC and SPEC.loader
EVALS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EVALS)


class SkillEvalTests(unittest.TestCase):
    def test_usage_metrics_do_not_claim_failed_reads(self):
        events = [
            {'type': 'item.completed', 'item': {'type': 'command_execution', 'command': 'cat .agents/skills/golang-testing/SKILL.md', 'exit_code': 1}},
            {'type': 'item.completed', 'item': {'type': 'command_execution', 'command': 'cat .agents/skills/golang-quality-linting/references/linting.md', 'exit_code': 0}},
            {'type': 'turn.completed', 'usage': {'input_tokens': 100, 'cached_input_tokens': 80, 'output_tokens': 20}},
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'trace.jsonl'
            path.write_text('CLI notice\n' + '\n'.join(json.dumps(event) for event in events))
            metrics = EVALS.codex_metrics(path)
            self.assertEqual(100, metrics['input_tokens'])
            self.assertEqual(80, metrics['cached_input_tokens'])
            self.assertEqual(2, metrics['tool_calls'])
            self.assertEqual([], metrics['skills_read'])
            self.assertEqual(['golang-quality-linting/references/linting.md'], metrics['references_read'])

    def test_shared_suite_covers_all_skills_and_negative_activation(self):
        cases = EVALS.cases_from(ROOT / 'evals/cases.json')
        skills = {path.name for path in (ROOT / 'plugins/golang-development/skills').iterdir()}
        self.assertEqual(skills, {skill for case in cases for skill in case['skills']})
        self.assertTrue(any(not case['skills'] for case in cases))

    def test_native_adapter_preserves_rubrics_and_negative_activation(self):
        with tempfile.TemporaryDirectory() as directory:
            plugin = Path(directory)
            cases = EVALS.cases_from(ROOT / 'evals/cases.json')
            EVALS.write_claude_suite(plugin, cases)
            for case in cases:
                folder = plugin / 'evals' / case['name']
                self.assertTrue((folder / 'prompt.md').read_text().endswith(case['prompt'] + '\n'))
                self.assertTrue((folder / 'graders/outcome.md').read_text().endswith(case['rubric'] + '\n'))
            negative = (plugin / 'evals/unrelated-request/graders/no-activation.md').read_text()
            self.assertIn('max: 0\narm: both', negative)

    def test_invalid_cases_are_rejected_before_execution(self):
        valid = EVALS.cases_from(ROOT / 'evals/cases.json')[0]
        for cases in [[valid, valid], [dict(valid, name='../escape')], [dict(valid, prompt='')], [dict(valid, skills='golang-testing')], ['not an object'], []]:
            with self.subTest(cases=cases), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'cases.json'
                path.write_text(json.dumps({'schema_version': 1, 'cases': cases}))
                with self.assertRaises(ValueError):
                    EVALS.cases_from(path)


if __name__ == '__main__':
    unittest.main()
