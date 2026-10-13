#!/usr/bin/env python3
"""Check a plain-handoff summary before it is sent to a person.

The checker enforces the plain-handoff rules that can be measured:
  * "Heads up" exists and is the first section
  * the required sections exist, in the right order
  * risky actions (deleting, emailing, publishing, charging) appear in
    "Heads up", not hidden lower down
  * the handoff stays inside its word budget
  * at most 1 question is asked
  * success words ("done", "fixed", "working") are backed by a real test
  * technical words carry a short plain explanation
  * vague filler phrases, long dashes and code dumps are avoided

It cannot judge truth or tone, and it cannot know about a surprise that
was never written down. Those are still the writer's job.

Usage:
  check_handoff.py --file handoff.md
  check_handoff.py --strict < handoff.md
  check_handoff.py --text "<handoff>"
  check_handoff.py --file handoff.md --mode short --json
  check_handoff.py --self-test

Exit codes:
  0  pass (warnings may be present unless --strict)
  1  fail (at least 1 error, or a warning with --strict)
  2  usage problem (no input, unreadable file, bad option)

What this script does and does not do: it only reads the text you give
it. It never writes files, never uses the network and needs no third
party packages. Needs Python 3.9 or newer; tested on 3.9, 3.11, 3.13 and 3.14.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

VERSION = "1.0.0"

SECTIONS: Tuple[str, ...] = (
    "Heads up",
    "What I did",
    "Does it work",
    "Not done yet",
    "Your decision",
)
REQUIRED: Dict[str, Tuple[str, ...]] = {
    "standard": SECTIONS,
    "short": ("Heads up", "What I did", "Does it work"),
}
WORD_LIMITS: Dict[str, int] = {"standard": 120, "short": 60}

# Technical words that need a plain explanation in brackets. Matching is
# whole word and case insensitive. Words with common everyday meanings
# ("production", "hook", "index", "build") are left out on purpose to avoid
# false alarms on marketing or business text.
JARGON: Tuple[str, ...] = (
    "refactor", "refactored", "dependency", "dependencies", "env var",
    "environment variable", "deploy", "deployed", "deployment", "prod",
    "staging", "migration", "schema", "endpoint", "api", "webhook",
    "commit", "committed", "merge", "merged", "pull request", "pr",
    "push", "pushed", "branch", "main branch", "repo", "repository", "ci",
    "pipeline", "null", "undefined", "localhost", "frontend", "backend",
    "server", "config", "hardcoded", "regression", "linter", "lint",
    "compile", "compiled", "cache", "latency", "auth", "oauth", "token",
    "tokens", "sdk", "cli", "npm", "diff", "rollback", "query", "payload",
    "json", "yaml", "typescript", "runtime", "stack trace",
    "race condition", "hydration", "ssr", "graphql", "rls", "component",
    "middleware", "cron", "docker", "kubernetes", "jsonb", "backfill",
    "backfilled", "feature flag", "unit test", "integration test",
    "test suite", "type error", "dns", "ssl",
)

SUCCESS = r"(done|fixed|working|works|complete|completed|finished|resolved)"
SUCCESS_WORDS = re.compile(r"\b" + SUCCESS + r"\b", re.IGNORECASE)
NEGATIONS = (
    r"not|isn't|isnt|doesn't|doesnt|don't|dont|never|no longer|haven't|"
    r"havent|hasn't|hasnt|wasn't|wasnt|couldn't|couldnt|can't|cant|cannot|no"
)
NEGATED_SUCCESS = re.compile(
    r"\b(" + NEGATIONS + r")\b[^.!?\n]{0,25}\b" + SUCCESS + r"\b", re.IGNORECASE
)
# Proof of testing must be in the past tense: "I tested", "all checks passed".
EVIDENCE = re.compile(
    r"\b(tested|checked|ran|passed|opened|confirmed|sent|tried|clicked|"
    r"loaded|verified|saw|viewed|arrived)\b",
    re.IGNORECASE,
)
NEGATED_EVIDENCE = re.compile(
    r"\b(" + NEGATIONS + r"|without)\b[^.!?\n]{0,20}\b(test|tested|checked|run|ran|tried|verified|opened)\b"
    r"|\bno time to (test|check|run)\b|\buntested\b|\b(can|will|could) (test|check|run) it later\b",
    re.IGNORECASE,
)
# Risky actions must be reported in "Heads up", not hidden lower down.
RISKY = re.compile(
    r"\b(delet\w*|remov\w*|wip(e|ed|ing)|overwr\w*|dropped|emailed|messaged|"
    r"sent to \d+|published|charged|refunded|cancel(l)?ed|reset)\b",
    re.IGNORECASE,
)
VAGUE_PHRASES: Tuple[str, ...] = (
    "some minor tweaks", "minor tweaks", "various improvements",
    "should work now", "should be working", "as mentioned above",
    "as discussed", "let me know if you have any questions",
    "under the hood", "it's a known issue", "seamless", "robust",
    "leverage", "streamline",
)
LONG_DASHES = re.compile("[‒–—―]")
CODE_FENCE = re.compile(r"^\s*```", re.MULTILINE)
URL = re.compile(r"https?://\S+")
FILE_PATH = re.compile(
    r"(?:[\w.-]+/)+[\w.-]+\.\w{1,5}"
    r"|\b[\w-]+\.(?:tsx?|jsx?|py|rb|go|rs|sql|ya?ml|json|css|html)\b"
)
# A heading is a section name at the start of a line, in bold or followed
# by a colon. Bullets such as "- Does it work on phones?" are not headings.
HEADING = re.compile(
    r"^[ \t]*(?:\*\*|__)\s*(" + "|".join(re.escape(s) for s in SECTIONS) + r")\s*:?\s*(?:\*\*|__)\s*:?"
    r"|^[ \t]*(" + "|".join(re.escape(s) for s in SECTIONS) + r")\s*:",
    re.IGNORECASE | re.MULTILINE,
)


@dataclass
class Finding:
    level: str  # "error" or "warning"
    code: str
    message: str


@dataclass
class Report:
    words: int
    limit: int
    mode: str
    sections: List[str]
    findings: List[Finding] = field(default_factory=list)

    @property
    def errors(self) -> List[Finding]:
        return [f for f in self.findings if f.level == "error"]

    @property
    def warnings(self) -> List[Finding]:
        return [f for f in self.findings if f.level == "warning"]

    def passed(self, strict: bool = False) -> bool:
        return not self.errors and not (strict and self.warnings)

    def to_dict(self, strict: bool = False) -> dict:
        return {
            "version": VERSION,
            "mode": self.mode,
            "words": self.words,
            "word_limit": self.limit,
            "sections_found": self.sections,
            "passed": self.passed(strict),
            "errors": [f.__dict__ for f in self.errors],
            "warnings": [f.__dict__ for f in self.warnings],
        }


def strip_code_fence(text: str) -> str:
    """Remove a single wrapping ``` block, so a handoff pasted inside one still checks."""
    lines = text.strip().splitlines()
    if len(lines) >= 2 and lines[0].strip().startswith("```") and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1])
    return text


def split_sections(text: str) -> List[Tuple[str, str]]:
    """Return (section name, body) pairs in the order they appear."""
    matches = list(HEADING.finditer(text))
    parts: List[Tuple[str, str]] = []
    for i, m in enumerate(matches):
        raw = m.group(1) or m.group(2)
        name = next(s for s in SECTIONS if s.lower() == raw.lower())
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        parts.append((name, text[m.end():end].strip()))
    return parts


def count_words(text: str) -> int:
    cleaned = re.sub(r"[*_`#>]", " ", URL.sub(" link ", text))
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'.,%$/-]*", cleaned))


def has_explanation(text: str, end: int) -> bool:
    """A technical word counts as explained if a bracket opens within 3 words after it."""
    return bool(re.match(r"\s*(?:[\w'-]+\s+){0,3}\(", text[end:end + 60]))


def find_jargon(text: str) -> List[str]:
    found: List[str] = []
    plain = URL.sub(" ", text)
    for term in JARGON:
        pattern = re.compile(r"(?<![\w-])" + re.escape(term) + r"(?![\w-])", re.IGNORECASE)
        for m in pattern.finditer(plain):
            if not has_explanation(plain, m.end()):
                found.append(term)
                break
    return found


def check(text: str, mode: str = "standard", max_words: Optional[int] = None) -> Report:
    if mode not in WORD_LIMITS:
        raise ValueError("mode must be 'standard' or 'short'")
    if max_words is not None and max_words < 1:
        raise ValueError("max_words must be 1 or more")
    text = strip_code_fence(text)
    limit = max_words if max_words is not None else WORD_LIMITS[mode]
    sections = split_sections(text)
    names = [name for name, _ in sections]
    body = dict(sections)
    report = Report(words=count_words(text), limit=limit, mode=mode, sections=names)
    add = report.findings.append

    # Structure
    if not names:
        add(Finding("error", "no-sections", "No handoff sections found. Start with **Heads up:** and use the template."))
    else:
        if "Heads up" not in names:
            add(Finding("error", "missing-heads-up", "Missing \"Heads up\". Surprises and problems must come first, or say \"Nothing unexpected\"."))
        elif names[0] != "Heads up":
            add(Finding("error", "heads-up-not-first", "\"Heads up\" must be the first section, before \"%s\"." % names[0]))
        first = HEADING.search(text)
        if first and text[: first.start()].strip():
            add(Finding("warning", "text-before-heads-up", "Text before the first section may hide a surprise. Start with **Heads up:**."))
        for req in REQUIRED[mode]:
            if req != "Heads up" and req not in names:
                add(Finding("error", "missing-section", "Missing section \"%s\"." % req))
        order = [SECTIONS.index(n) for n in names]
        if order != sorted(order):
            add(Finding("warning", "section-order", "Sections are out of order. Use: " + ", ".join(SECTIONS) + "."))
        for d in sorted({n for n in names if names.count(n) > 1}):
            add(Finding("warning", "duplicate-section", "Section \"%s\" appears more than once." % d))

        # Hidden surprises: risky actions mentioned outside "Heads up".
        # "Your decision" is skipped because it proposes actions, it doesn't report them.
        heads = body.get("Heads up", "")
        for name, section_body in sections:
            if name in ("Heads up", "Your decision"):
                continue
            for m in RISKY.finditer(section_body):
                if m.group(0).lower() not in heads.lower():
                    add(Finding("error", "hidden-risk", "\"%s\" is mentioned under \"%s\" but not in \"Heads up\". Deletions, sends and other risky actions must be at the top." % (m.group(0), name)))
                    break
        last_body = sections[-1][1]
        if names[-1] == "Your decision" and "\n\n" in last_body.strip():
            add(Finding("warning", "text-after-decision", "There is extra text after \"Your decision\". A PS can hide a surprise; move it to \"Heads up\"."))

    # Length
    if report.words > limit:
        add(Finding("error", "too-long", "%d words, over the %d word limit for a %s handoff. Move detail to notes." % (report.words, limit, mode)))

    # Questions (question marks inside links don't count)
    questions = URL.sub(" ", text).count("?")
    if questions > 1:
        add(Finding("error", "too-many-questions", "%d questions found. Ask at most 1 and list the rest under \"Not done yet\"." % questions))

    # Decision quality
    decision = body.get("Your decision", "")
    options = re.findall(r"\*\*[A-C]:\*\*|^\s*[-*]\s*[A-C][:.)]", decision, re.MULTILINE)
    if len(options) >= 2 and "recommend" not in decision.lower():
        add(Finding("warning", "no-recommendation", "The decision gives options but no recommendation. Say which you recommend and why."))
    if len(options) > 3:
        add(Finding("warning", "too-many-options", "More than 3 options. Offer 2 or 3."))

    # Honest testing
    works = body.get("Does it work", "")
    claims = "\n".join(b for n, b in sections if n in ("What I did", "Does it work"))
    positive = SUCCESS_WORDS.findall(NEGATED_SUCCESS.sub(" ", claims))
    proof = EVIDENCE.search(NEGATED_EVIDENCE.sub(" ", works))
    if positive and not proof:
        add(Finding("warning", "untested-claim", "Says \"%s\" but \"Does it work\" doesn't say how it was tested." % positive[0].lower()))
    if works and re.search(r"\bshould\b", works, re.IGNORECASE) and not proof:
        add(Finding("warning", "should-work", "\"Should\" in \"Does it work\" sounds tested but isn't. Say what you tested, or that you haven't."))

    # Plain language
    jargon = find_jargon(text)
    if jargon:
        add(Finding("warning", "jargon", "Technical words without a plain explanation: " + ", ".join(sorted(set(jargon))) + ". See references/PLAIN-WORDS.md."))
    lowered = text.lower()
    vague = [p for p in VAGUE_PHRASES if p in lowered]
    if vague:
        add(Finding("warning", "vague-phrase", "Vague or empty phrases: " + ", ".join(vague) + "."))
    if LONG_DASHES.search(text):
        add(Finding("warning", "long-dash", "Long dashes found. Use a comma or a full stop."))
    if len(CODE_FENCE.findall(text)) >= 2:
        add(Finding("warning", "code-block", "Code blocks don't belong in a plain handoff. Put them in notes."))
    paths = set(FILE_PATH.findall(URL.sub(" ", text)))
    if len(paths) > 2:
        add(Finding("warning", "file-paths", "%d file names or paths. Give at most 2, only if the person must open them." % len(paths)))
    return report


def render(report: Report, strict: bool = False) -> str:
    lines = [
        "plain-handoff check v%s (%s mode)" % (VERSION, report.mode),
        "Words: %d of %d" % (report.words, report.limit),
        "Sections: " + (", ".join(report.sections) if report.sections else "none found"),
    ]
    lines += ["ERROR  [%s] %s" % (f.code, f.message) for f in report.errors]
    lines += ["WARN   [%s] %s" % (f.code, f.message) for f in report.warnings]
    if report.passed(strict):
        lines.append("RESULT: PASS" + (" with %d warning(s)" % len(report.warnings) if report.warnings else ""))
    else:
        lines.append("RESULT: FAIL")
    return "\n".join(lines)


GOOD = """**Heads up:** Nothing unexpected.

**What I did:**
- Customers now get a confirmation email after they book.

**Does it work:** Yes. I made 2 test bookings and both emails arrived.

**Not done yet:** Nothing, it's finished.

**Your decision:** Nothing needed from you."""


def _self_test_cases() -> List[Tuple[str, str, str, bool, set]]:
    """(name, text, mode, should pass, finding codes that must appear)."""
    g = GOOD
    return [
        ("good handoff passes cleanly", g, "standard", True, set()),
        ("missing heads up fails", g.replace("**Heads up:** Nothing unexpected.\n\n", ""), "standard", False, {"missing-heads-up"}),
        ("heads up not first fails", g.split("\n\n", 1)[1] + "\n\n**Heads up:** Nothing unexpected.", "standard", False, {"heads-up-not-first"}),
        ("hidden deletion fails", g.replace("Nothing, it's finished.", "Nothing. I also deleted the old customer list."), "standard", False, {"hidden-risk"}),
        ("too long fails", g + "\n" + " word" * 120, "standard", False, {"too-long"}),
        ("two questions fail", g.replace("Nothing needed from you.", "Keep it? Or undo it?"), "standard", False, {"too-many-questions"}),
        ("untested claim warns", g.replace("Yes. I made 2 test bookings and both emails arrived.", "Yes, it's done."), "standard", True, {"untested-claim"}),
        ("excuse is not proof", g.replace("Yes. I made 2 test bookings and both emails arrived.", "Yes, done. No time to test it."), "standard", True, {"untested-claim"}),
        ("jargon warns", g.replace("Customers now get", "I refactored the webhook so customers get"), "standard", True, {"jargon"}),
        ("explained jargon is fine", g.replace("Customers now get", "I fixed the webhook (an automatic message) so customers get"), "standard", True, set()),
        ("long dash warns", g.replace("Nothing, it's finished.", "Nothing — it's finished."), "standard", True, {"long-dash"}),
        ("short mode passes", "**Heads up:** Nothing unexpected.\n\n**What I did:** Fixed the typo on the home page.\n\n**Does it work:** Yes, I opened the page and checked.", "short", True, set()),
    ]


def self_test() -> int:
    cases = _self_test_cases()
    failures = 0
    for name, text, mode, should_pass, codes in cases:
        r = check(text, mode)
        found = {f.code for f in r.findings}
        ok = r.passed() == should_pass and codes <= found and (codes or not r.findings)
        print(("ok    " if ok else "FAIL  ") + name + ("" if ok else "  (found: %s)" % sorted(found)))
        failures += 0 if ok else 1
    print("%d of %d self tests passed" % (len(cases) - failures, len(cases)))
    return 0 if failures == 0 else 1


def read_input(args: argparse.Namespace) -> Optional[str]:
    if args.text is not None:
        return args.text
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            return fh.read()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Check a plain-handoff summary before sending it.")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--text", help="the handoff text (use --file or stdin if it contains quotes)")
    src.add_argument("--file", help="a file containing the handoff")
    ap.add_argument("--mode", choices=sorted(WORD_LIMITS), default="standard", help="standard (120 words) or short (60 words)")
    ap.add_argument("--max-words", type=int, help="override the word limit (1 or more)")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    ap.add_argument("--json", action="store_true", help="print the result as JSON")
    ap.add_argument("--self-test", action="store_true", help="run the built in tests")
    ap.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()
    if args.max_words is not None and args.max_words < 1:
        print("error: --max-words must be 1 or more", file=sys.stderr)
        return 2
    try:
        text = read_input(args)
    except OSError as exc:
        print("error: could not read file: %s" % exc, file=sys.stderr)
        return 2
    if text is None:
        ap.print_usage(sys.stderr)
        print("error: give --file, --text, or pipe the handoff in", file=sys.stderr)
        return 2
    if not text.strip():
        print("error: the handoff is empty", file=sys.stderr)
        return 2

    report = check(text, args.mode, args.max_words)
    print(json.dumps(report.to_dict(args.strict), indent=2) if args.json else render(report, args.strict))
    return 0 if report.passed(args.strict) else 1


if __name__ == "__main__":
    sys.exit(main())
