# Changelog

All notable changes to Plain Handoff are listed here. Versions follow semantic versioning (major.minor.patch).

## 1.0.1 (2026-10-15)

- README: download, install, clone and issue links now point to the new account name, github.com/onittindwani-ai. Old links still redirect. No change to the skill itself.

## 1.0.0 (2026-10-13)

First release.

- `SKILL.md`: 7 rules, the fact collection step, the 5 section handoff format, special situations (failed, partly done, surprise changes, risky next steps, decisions, vague replies, frustration, many small tasks), where detail goes, and a pre send checklist.
- `references/PLAIN-WORDS.md`: about 100 technical terms in 7 groups with plain versions, and a list of phrases to never use.
- `references/QUESTION-RULES.md`: the decision format, risk lines, a clear yes for risky actions, when not to ask, and 5 good and bad examples.
- `references/EXAMPLES.md`: 8 full before and after handoffs.
- `templates/`: standard, short and failed handoff forms, the vague request form, and always on snippets for CLAUDE.md and AGENTS.md (small and full versions).
- `scripts/check_handoff.py`: a dependency free, read only checker for structure, hidden risky actions, length, questions, honest testing (excuses don't count as proof), jargon, vague phrases, long dashes and code dumps, with file, stdin, text and JSON modes, exit codes and 12 built in self tests.
- `tests/`: 25 automatic tests, including every example in EXAMPLES.md, run on GitHub on Python 3.9, 3.11 and 3.13 for every change.
- `TESTS.md`: 6 hands on tests for Claude Code and Codex, with a planted problem for the surprise test, and Mac, Linux and Windows setup.
- Reviewed by an independent senior engineering pass before release; all must fix and should fix items addressed.
- Tested for real in Codex (October 2026), 3 runs in throwaway folders. Runs 1 and 2: the skill loaded through the AGENTS.md note and every handoff followed the format and passed the checker. Run 2 also showed a gap: the AI left a wrong price alone (correct) but did not warn about it. Rule 1 and the fact collection step now require reporting problems the AI noticed but did not fix. Run 3: the AI put the planted wrong price in "Heads up".
