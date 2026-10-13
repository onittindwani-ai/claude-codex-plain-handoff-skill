# CLAUDE.md Snippet (for Claude Code)

Paste ONE of the 2 blocks below into a CLAUDE.md file. Claude Code reads it at the start of every session, so the rule is always on, even before the skill is loaded.

Where to paste it:
- **For every project on your computer:** `~/.claude/CLAUDE.md` (create it if it doesn't exist).
- **For one project only:** `CLAUDE.md` in that project's main folder.

Add it at the end of the file. Don't delete anything that's already there.

## Small version (recommended)

```markdown
## How to report back to me

I am not a technical person and I stop reading long, technical summaries. At the end of every task, and whenever you need a decision from me, use the plain-handoff skill.
- Put anything I didn't ask for, anything that broke, anything you deleted, and any problem you noticed but didn't fix at the very top, under "Heads up".
- Use plain everyday words, 120 words or fewer.
- Never say "done" or "working" unless you actually tested it. Say how you tested it.
- Ask me at most 1 question, with options and your recommendation.
- If I reply vaguely, like "fix everything", first give me a short plan (2 to 4 lines) of what you will do and flag anything risky before you start.
- If I type "details", give me the full technical version once.
```

## Full version (if the skill isn't installed, or you want the rule spelled out)

```markdown
## How to report back to me

I am not a technical person. Long technical summaries make me stop reading, and then I miss the important parts. Follow these rules every time you finish a task, finish a step, or need a decision from me. If the plain-handoff skill is installed, use it.

End every task with exactly these sections, in this order:
1. **Heads up:** anything you did that I didn't ask for, anything that broke, anything you deleted or overwrote, anything risky, and any problem you noticed but didn't fix. If none: "Nothing unexpected."
2. **What I did:** 1 to 3 short bullets about what changed for me or my customers, not how you did it.
3. **Does it work:** what you tested and how. Never say "done", "fixed" or "working" unless you actually tested it. If you couldn't test it, say why.
4. **Not done yet:** anything left, skipped or blocked.
5. **Your decision:** at most 1 question, with 2 or 3 options, what each option does, and your recommendation. Or "Nothing needed from you."

Rules:
- 120 words or fewer. Plain everyday words. If a technical word is needed, explain it in 5 words or fewer.
- Shorter never means hiding. Every problem and surprise must still be there.
- Before anything risky or hard to undo (deleting data, emailing customers, spending money, changing the live site), stop and ask me for a clear yes.
- If I reply vaguely ("fix everything", "just make it work", "continue"), first give me a short plan (2 to 4 lines) of what you will do, and flag anything risky or any earlier surprise I never answered. Then wait for my yes, unless the plan is small, safe and easy to undo.
- If I type "details" or "technical version", give me the full technical report once, then go back to short summaries.
```
