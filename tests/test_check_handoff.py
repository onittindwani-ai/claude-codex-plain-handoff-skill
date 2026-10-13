"""Tests for scripts/check_handoff.py.

Run from the skill folder:
    python3 -m unittest discover -s tests -v

Uses only the Python standard library.
"""

import importlib.util
import pathlib
import re
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_handoff.py"
EXAMPLES = ROOT / "references" / "EXAMPLES.md"

spec = importlib.util.spec_from_file_location("check_handoff", SCRIPT)
ch = importlib.util.module_from_spec(spec)
sys.modules["check_handoff"] = ch  # dataclasses look the module up while loading
spec.loader.exec_module(ch)


def load_examples():
    """Return a list of (title, before_text, after_text) from EXAMPLES.md."""
    text = EXAMPLES.read_text(encoding="utf-8")
    blocks = re.split(r"^## \d+\. ", text, flags=re.MULTILINE)[1:]
    out = []
    for block in blocks:
        title = block.splitlines()[0].strip()
        before = re.search(r"\*\*Before.*?\*\*\n((?:>.*\n?)+)", block)
        after = re.search(r"\*\*After:\*\*\n```\n(.*?)\n```", block, re.DOTALL)
        if before and after:
            before_text = "\n".join(line.lstrip("> ").rstrip() for line in before.group(1).splitlines())
            out.append((title, before_text, after.group(1)))
    return out


class TestExamples(unittest.TestCase):
    def test_eight_examples_found(self):
        self.assertEqual(len(load_examples()), 8)

    def test_every_after_passes_cleanly(self):
        for title, _, after in load_examples():
            with self.subTest(example=title):
                report = ch.check(after)
                self.assertEqual([f.code for f in report.errors], [], title)
                self.assertEqual([f.code for f in report.warnings], [], title)

    def test_every_before_fails(self):
        for title, before, _ in load_examples():
            with self.subTest(example=title):
                self.assertFalse(ch.check(before).passed(), title)


class TestRules(unittest.TestCase):
    good = ch.GOOD

    def codes(self, text, mode="standard"):
        return {f.code for f in ch.check(text, mode).findings}

    def test_good_passes(self):
        r = ch.check(self.good)
        self.assertTrue(r.passed(strict=True))

    def test_heads_up_required_and_first(self):
        no_heads = self.good.replace("**Heads up:** Nothing unexpected.\n\n", "")
        self.assertIn("missing-heads-up", self.codes(no_heads))
        moved = self.good.split("\n\n", 1)[1] + "\n\n**Heads up:** Nothing unexpected."
        self.assertIn("heads-up-not-first", self.codes(moved))

    def test_word_limits(self):
        long_text = self.good + "\n" + " word" * 100
        self.assertIn("too-long", self.codes(long_text))
        self.assertNotIn("too-long", self.codes(self.good, "short"))
        self.assertIn("too-long", self.codes(self.good + " extra" * 30, "short"))

    def test_one_question_only(self):
        two = self.good.replace("Nothing needed from you.", "Keep it? Or undo it?")
        self.assertIn("too-many-questions", self.codes(two))

    def test_untested_success_claim(self):
        claim = self.good.replace("Yes. I made 2 test bookings and both emails arrived.", "Yes, it's all done.")
        self.assertIn("untested-claim", self.codes(claim))

    def test_negated_success_is_not_a_claim(self):
        text = self.good.replace("Yes. I made 2 test bookings and both emails arrived.", "No, it isn't working yet.")
        self.assertNotIn("untested-claim", self.codes(text))

    def test_jargon_needs_explanation(self):
        raw = self.good.replace("Customers now get", "I deployed it so customers get")
        explained = self.good.replace("Customers now get", "I deployed it (put it live) so customers get")
        self.assertIn("jargon", self.codes(raw))
        self.assertNotIn("jargon", self.codes(explained))

    def test_options_without_recommendation(self):
        text = self.good.replace(
            "Nothing needed from you.",
            "Keep the new prices?\n- **A:** Keep\n- **B:** Undo",
        )
        self.assertIn("no-recommendation", self.codes(text))

    def test_long_dash_and_vague_phrase(self):
        self.assertIn("long-dash", self.codes(self.good.replace("finished.", "finished — fully.")))
        self.assertIn("vague-phrase", self.codes(self.good.replace("Nothing unexpected.", "Some minor tweaks.")))

    def test_wrapped_in_code_fence(self):
        self.assertTrue(ch.check("```\n" + self.good + "\n```").passed())

    def test_hidden_risky_action_fails(self):
        sneaky = self.good.replace(
            "Nothing, it's finished.",
            "Nothing. I also wiped the old customers table and emailed 400 customers.",
        )
        self.assertIn("hidden-risk", self.codes(sneaky))
        self.assertFalse(ch.check(sneaky).passed())

    def test_risky_action_in_heads_up_is_fine(self):
        honest = self.good.replace(
            "**Heads up:** Nothing unexpected.",
            "**Heads up:** I deleted 3 old test bookings. Nothing else changed.",
        ).replace("Nothing, it's finished.", "Nothing. The 3 test bookings were deleted as planned.")
        self.assertNotIn("hidden-risk", self.codes(honest))

    def test_excuses_are_not_proof_of_testing(self):
        for excuse in ("Yes, done. No time to test it.", "Yes, done. I can run it later.", "Not tested. It should work."):
            with self.subTest(excuse=excuse):
                text = self.good.replace("Yes. I made 2 test bookings and both emails arrived.", excuse)
                codes = self.codes(text)
                self.assertTrue({"untested-claim", "should-work"} & codes, excuse)

    def test_bullet_is_not_a_heading(self):
        text = self.good.replace(
            "- Customers now get a confirmation email after they book.",
            "- Customers now get a confirmation email after they book.\n- Does it work on phones: yes, I opened it on 2 phones.",
        )
        self.assertNotIn("duplicate-section", self.codes(text))

    def test_question_mark_in_link_is_not_a_question(self):
        text = self.good.replace("Nothing needed from you.", "Open https://example.com/page?id=4 and check it looks right?")
        self.assertNotIn("too-many-questions", self.codes(text))

    def test_new_jargon_words_caught(self):
        text = self.good.replace("Customers now get", "Pushed to main and opened a PR so customers get")
        self.assertIn("jargon", self.codes(text))

    def test_everyday_words_not_flagged(self):
        text = self.good.replace("Customers now get", "The video production page and index page now show, and customers get")
        self.assertNotIn("jargon", self.codes(text))

    def test_bad_word_limit_rejected(self):
        with self.assertRaises(ValueError):
            ch.check(self.good, max_words=0)


class TestCommandLine(unittest.TestCase):
    def run_cli(self, *args, stdin=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            input=stdin, capture_output=True, text=True,
        )

    def test_pass_exit_code(self):
        self.assertEqual(self.run_cli("--text", ch.GOOD).returncode, 0)

    def test_fail_exit_code(self):
        self.assertEqual(self.run_cli("--text", "All done, deployed to prod.").returncode, 1)

    def test_stdin_and_json(self):
        r = self.run_cli("--json", stdin=ch.GOOD)
        self.assertEqual(r.returncode, 0)
        self.assertIn('"passed": true', r.stdout)

    def test_self_test(self):
        self.assertEqual(self.run_cli("--self-test").returncode, 0)


if __name__ == "__main__":
    unittest.main()
