# Plain Handoff

A skill for Claude Code and Codex that ends every task with a short, plain English summary you will actually read.

**Download:** [latest release (zip)](https://github.com/onittindwani1/claude-codex-plain-handoff-skill/releases/latest) · **Source:** [github.com/onittindwani1/claude-codex-plain-handoff-skill](https://github.com/onittindwani1/claude-codex-plain-handoff-skill)

## The problem it solves

AI coding agents are good at telling you what they did. The trouble is how they tell you: a long block of technical words at the end of every task. Most people stop reading. Then the one line that mattered ("I also changed your login page", "payments are not tested yet") gets missed, you reply "fix everything", and the next round of work goes wrong.

Plain Handoff changes the ending, not the work. Every task now ends like this:

```
**Heads up:** I also renamed the "Contact" page to "Get in touch". Say "undo" and I'll change it back.

**What I did:**
- The contact form now emails you every time someone fills it in.

**Does it work:** Yes. I sent 3 test messages and all 3 arrived.

**Not done yet:** Nothing, it's finished.

**Your decision:** Nothing needed from you.
```

Instead of this:

> Implemented the contact form submission handler with server side validation, wired it to the transactional email provider via the existing SMTP config, added a honeypot field for spam mitigation, and refactored the ContactPage component (also renamed the route for consistency with the nav). Tests pass. Let me know if you have any questions.

## What it does

- **Surprises first.** Anything the AI did that you didn't ask for, anything that broke, anything it deleted, and any problem it noticed but didn't fix goes at the very top.
- **Plain words.** No unexplained technical words. 120 words or fewer.
- **Honest testing.** It never says "done" or "working" unless it actually tested it, and it says how.
- **One question at a time.** With options and its recommendation, so you can answer with one letter.
- **A guard against vague replies.** If you type "fix everything", it first gives you a short plan (2 to 4 lines) and flags anything risky before it starts.
- **Detail when you want it.** Type "details" and you get the full technical version, once.

## What's in the folder

| File | What it's for |
| --- | --- |
| `SKILL.md` | The skill itself: the rules, the format and the special situations |
| `references/PLAIN-WORDS.md` | About 100 technical words with plain versions, plus phrases to never use |
| `references/QUESTION-RULES.md` | How the AI must ask you for a decision |
| `references/EXAMPLES.md` | 8 full before and after examples |
| `templates/HANDOFF.md` | The standard, short and failed handoff forms |
| `templates/CLAUDE-MD-SNIPPET.md` | The always on block for Claude Code's CLAUDE.md |
| `templates/AGENTS-MD-SNIPPET.md` | The always on block for Codex's AGENTS.md |
| `scripts/check_handoff.py` | A checker the AI can run on its own summary before sending it |
| `tests/` | 25 automatic tests for the checker, including every example |
| `TESTS.md` | 6 hands on tests to prove it works after you install it |
| `.github/workflows/tests.yml` | Runs the automatic tests on GitHub for every change |

## Install it (about 2 minutes)

You need 2 things for the best result: the skill folder, and a short always on note. The note makes sure the AI follows the rule from the very first message.

### Claude Code

**Step 1. Put the folder in place.** Either download the zip from the [latest release](https://github.com/onittindwani1/claude-codex-plain-handoff-skill/releases/latest), or clone it with git (see "Install with git" below). Unzip the download, so you have a folder called `plain-handoff` with `SKILL.md` directly inside it. (Some unzip tools create `plain-handoff/plain-handoff/`. If yours did, use the inner folder.)

For every project on your computer (recommended), move it to your personal skills folder:

Mac or Linux:
```bash
mkdir -p ~/.claude/skills
mv ~/Downloads/plain-handoff ~/.claude/skills/
```

Windows (PowerShell):
```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills"
Move-Item "$HOME\Downloads\plain-handoff" "$HOME\.claude\skills\"
```

For one project only, put it inside that project instead: `your-project/.claude/skills/plain-handoff/`.

**Step 2. Add the always on note.** Open `templates/CLAUDE-MD-SNIPPET.md`, copy the small version, and paste it at the end of `~/.claude/CLAUDE.md` (for every project) or of `CLAUDE.md` in your project's main folder (for one project). Create the file if it doesn't exist.

**Step 3. Check it loaded.** Start Claude Code and type `/skills`. You should see `plain-handoff` in the list. If you added a new skills folder while Claude Code was open, type `/reload-skills` or restart it.

### Codex

**Step 1. Put the folder in place.** Codex looks for skills in a folder called `.agents/skills`.

For every project on your computer (recommended):

Mac or Linux:
```bash
mkdir -p ~/.agents/skills
mv ~/Downloads/plain-handoff ~/.agents/skills/
```

Windows (PowerShell):
```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\skills"
Move-Item "$HOME\Downloads\plain-handoff" "$HOME\.agents\skills\"
```

For one project only, put it inside that project instead: `your-project/.agents/skills/plain-handoff/`.

**Step 2. Add the always on note.** Open `templates/AGENTS-MD-SNIPPET.md`, copy the small version, and paste it at the end of `~/.codex/AGENTS.md` (for every project) or of `AGENTS.md` in your project's main folder (for one project). Create the file if it doesn't exist.

**Step 3. Check it loaded.** Start a new Codex session and type `/skills`. You should see `plain-handoff`. You can also call it directly by typing `$plain-handoff`.

### Using both tools?

Put one copy in each tool's skills folder, or keep one copy and link it into the other folder. Both tools follow linked folders. Mac or Linux example:

```bash
mkdir -p ~/.agents/skills
ln -s ~/.claude/skills/plain-handoff ~/.agents/skills/plain-handoff
```

### Install with git (easiest to keep up to date)

Claude Code, for every project:
```bash
git clone https://github.com/onittindwani1/claude-codex-plain-handoff-skill.git ~/.claude/skills/plain-handoff
```

Codex, for every project:
```bash
git clone https://github.com/onittindwani1/claude-codex-plain-handoff-skill.git ~/.agents/skills/plain-handoff
```

To update later, run `git pull` inside that folder. Then do Step 2 (the always on note) if you haven't yet.

### Updating to a new version

If you installed with git, run `git pull` inside the folder. If you used the zip, delete the old `plain-handoff` folder first, then move the new one in. (`mv` won't replace a folder that already exists.) Your CLAUDE.md or AGENTS.md note can stay as it is.

## Check that it works

Open `TESTS.md` and run the first 3 tests. They take about 5 minutes and prove the 3 most important rules: surprises first, honest testing and one question at a time.

The checker also has its own tests. From inside the `plain-handoff` folder:

```bash
python3 scripts/check_handoff.py --self-test
python3 -m unittest discover -s tests -v
```

On Windows, use `py` instead of `python3`.

## Everyday use

You don't need to do anything. The skill runs at the end of every task. A few useful phrases:

| Type this | What happens |
| --- | --- |
| `details` or `technical version` | You get the full technical report for the last task, once |
| `undo that` | The AI undoes the surprise it told you about in "Heads up" |
| `A` or `B` | Answers the decision question |
| `fix everything` | The AI gives you a short plan first, then waits for your yes if anything is risky |

## What the checker script does (and doesn't)

`scripts/check_handoff.py` only reads the text you give it and prints a result. It never writes or deletes files, never connects to the internet and needs no extra packages. It needs Python 3.9 or newer and is tested automatically on Python 3.9, 3.11 and 3.13 on every change, and locally on 3.14. You can read every line of it before running it.

## What it never does

- It never hides a problem to keep the summary short. Every failure, skipped step and unexpected change is still there, at the top.
- It never says "done" when it isn't sure.
- It never deletes, publishes, emails customers, spends money or changes a live site without asking you for a clear yes first.
- It doesn't change how the AI does the work, only how it reports back.

## Limits

- The AI follows the skill very well, but not perfectly every single time. The always on note in CLAUDE.md or AGENTS.md makes it much more reliable. If a handoff is too long or too technical, reply "use plain-handoff" and it will rewrite it.
- The checker measures structure and words. It catches risky actions (like deleting or emailing) that are mentioned but not put in "Heads up", but it can't know about a surprise the AI never wrote down, so the rules in `SKILL.md` matter most.
- If you have hundreds of skills installed, Codex may leave skill descriptions out of what the AI sees (it shows a "skills context budget" warning). We saw this in our own test. The always on note in AGENTS.md is what keeps the skill working in that case, so don't skip Step 2.
- Skills folders and settings change between tool versions. These steps match Claude Code and Codex as of October 2026. If something doesn't load, check your tool's own docs on skills.

## FAQ

**Will this make the AI do less work?** No. It only changes the summary at the end.

**I'm technical. Is this still useful?** Yes, for long sessions. Surprises first and honest testing help everyone. Type "details" whenever you want the full version.

**Can I change the word limit or the sections?** Yes. Edit `SKILL.md` and `templates/HANDOFF.md`. If you change the limit, use `--max-words` with the checker.

**Does it send my code anywhere?** No. It's text instructions and a small local Python script. Nothing is uploaded.

**How do I remove it?** Delete the `plain-handoff` folder from your skills folder, and remove the note from CLAUDE.md or AGENTS.md.

## Found a problem or have an idea?

Open an issue on [GitHub](https://github.com/onittindwani1/claude-codex-plain-handoff-skill/issues). Please don't paste private code, passwords or customer details into an issue.

## Licence

MIT. Free to use, change and share. See `LICENSE`.

Version 1.0.0. See `CHANGELOG.md`.
