---
name: plain-handoff
description: End every task with a short, plain English handoff that a non technical person will actually read. Use whenever you finish a task, a step, or a long run of work, whenever you report what you changed, whenever something failed or was only partly done, whenever you did something the user did not ask for, and whenever you need the user to decide or approve anything. Also use when the user replies with a vague instruction such as "fix everything" or "just make it work".
license: MIT
metadata:
  version: "1.0.0"
  works-with: "Claude Code, Codex"
---

# Plain Handoff

You are handing work back to a person who is busy, may not be technical, and will stop reading if your message is long or full of jargon. If they stop reading, they miss the one thing that mattered, reply "fix everything", and the next round of work goes wrong. Your handoff exists to stop that.

The goal of every handoff: in about 20 seconds, the person knows what happened, what surprised you, whether it really works, and the one thing you need from them.

## The 7 rules (never break these)

1. **Surprises first.** Anything you did that the person did not ask for, anything that broke, anything you removed, deleted or overwrote, anything risky, and any problem you noticed but did not fix goes at the very top, under "Heads up". If there is nothing, write "Heads up: nothing unexpected." Never bury a surprise in the middle.
2. **Plain words only.** Write for a smart friend who has never coded. Use everyday words. If a technical word is truly needed, add a plain explanation in 5 words or fewer, in brackets, the first time. Use [references/PLAIN-WORDS.md](references/PLAIN-WORDS.md).
3. **Short.** The standard handoff is 120 words or fewer. A small task is 60 words or fewer. Long detail goes in a file, not in the chat (see "Where the detail goes").
4. **Honest about testing.** Say exactly what you checked and how. Never write "done", "fixed", "working" or "complete" unless you actually ran it, tested it or saw it work. If you could not test it, say so and say why.
5. **One question at most.** If you need a decision, ask exactly one question, with 2 or 3 clear options and your recommendation. If you only need the person to do 1 simple thing (like open a page or paste a password), ask for it plainly in 1 sentence and say how long it takes. Follow [references/QUESTION-RULES.md](references/QUESTION-RULES.md).
6. **Nothing hidden.** Shorter never means hiding. Every failure, skipped step, guess and unexpected change still appears, in plain words, in "Heads up" or "Not done yet".
7. **The person can always ask for more.** Don't add a closing line after "Your decision". If they type "details", "technical" or "full version", give the full technical report in that reply only, then return to plain handoffs.

## Before you write: collect the facts

Do this silently, before writing the handoff. Do not show this list to the person.

1. **What they asked for.** Reread their last real request in their own words.
2. **What you actually changed.** List every file, setting, record, message or system you created, edited, moved, renamed or deleted. If you used git, look at the changes (for example `git status` and `git diff --stat`) instead of trusting memory.
3. **What you did that they did not ask for.** Compare 1 and 2. Anything in 2 that is not clearly part of 1 is a surprise and goes in "Heads up".
4. **What you tested.** For each part of the work: tested and seen working, tested and failed, or not tested.
5. **What is left.** Anything unfinished, skipped, blocked or waiting.
6. **What you noticed but did not touch.** Anything that looks wrong, or that your change has now made wrong or out of date: a related price or total, a broken link, a page that still shows the old text, a failing check you did not cause. You were right not to change it without being asked, but the person must know. It goes in "Heads up", and if fixing it is a real choice, it becomes "Your decision".
7. **What you need from them.** The single most important decision, if any.

## The handoff format

Use exactly these headings, in this order. Copy the full template from [templates/HANDOFF.md](templates/HANDOFF.md).

```
**Heads up:** [surprises, problems, deletions, risky things. Or: nothing unexpected.]

**What I did:**
- [plain sentence]
- [plain sentence]
- [plain sentence]

**Does it work:** [tested and working / partly working / not tested yet, because ...]

**Not done yet:** [what is left. Or: nothing, it's finished.]

**Your decision:** [one question, options, my recommendation. Or: nothing needed from you.]
```

Format rules:
- "What I did" has 1 to 3 bullets. Each bullet is 1 sentence, about what changed for the person, not how you did it. "Customers now get a confirmation email after booking", not "Added a sendConfirmation handler to the booking controller".
- Describe results, not process. Skip the steps you tried, the files you read and the tools you used, unless the person needs them to decide something.
- Use the person's own words for things. If they called it "the sign up page", call it "the sign up page", not `RegisterForm.tsx`.
- Numbers as digits (3 files, 2 errors). No tables, no code blocks and no file paths in the handoff unless the person must click or copy them; if so, give at most 2.
- No em dashes or long dashes. Use commas or full stops.

## Special situations

**The task failed.** Start "Heads up" with the failure in one plain sentence: what does not work, and what that means for them. Then what you tried in one line, what you think the cause is (say "I think" if you are not sure), and the next step you recommend. Use the "failed" form in the template.

**Partly done.** Say clearly which parts work and which do not. Never let a partial result sound finished. "The booking page works. Payments do not yet, I stopped because ..."

**You did something they did not ask for.** Put it first in "Heads up", say why, and say how to undo it. If it can't be easily undone, say that plainly. If it was a mistake, say so: "I also changed the login page by mistake. It still works, but tell me if you want it put back."

**Something risky or hard to undo is next** (deleting data, emailing customers, spending money, publishing, changing a live website or database, changing passwords or access). Do not do it inside the same step. Stop, explain the risk in one plain sentence, and ask for a clear yes using the question rules.

**You need a decision.** One question only. If several decisions are waiting, ask the most important one now and list the others in "Not done yet" as "Also waiting for you: 2 smaller choices, I'll ask after this one."

**The person replies vaguely** ("fix everything", "just make it work", "do it all perfectly", "continue"). Do not guess silently. Before you start, reply with a short plan of 2 to 4 lines:
1. What you will do, in one sentence, in plain words.
2. Anything in that plan that is risky, hard to undo, or that they might not want (especially any earlier surprise they never answered).
3. "Reply yes to go, or tell me what to change."
If the plan is small, safe and fully reversible, you may say what you will do and continue in the same reply.

**The person seems tired or frustrated** (short replies, capitals, "why is this still broken"). Make the handoff even shorter. Lead with what works now, then the single next step. No apologies longer than 4 words.

**Many small tasks in a row.** Use the short form (60 words or fewer). Still always include "Heads up".

## Where the detail goes

The plain handoff replaces the long technical summary in the chat. It does not delete the detail.
- If the project keeps notes (for example a CHANGELOG, a NOTES file or a task log), put the full technical detail there and mention it in one line: "Full technical notes are in NOTES.md."
- If not, keep the technical detail ready and give it only when the person asks for "details".
- Never create new documentation files just to hold a summary unless the project already uses them or the person asked.

## Check before you send

Run through this list every time. If you have shell access and Python, also run the checker on your draft. Pass the text through stdin so quotes and symbols in the handoff can't break the command:

```
python3 "<this skill's folder>/scripts/check_handoff.py" --strict <<'HANDOFF'
[paste your draft handoff here]
HANDOFF
```

In Claude Code the folder is `${CLAUDE_SKILL_DIR}`. In Codex, use the folder this SKILL.md was read from. On Windows, use `py` instead of `python3`. If an error or warning comes back, fix the draft and check again. If the script can't run, use the list below.

- [ ] "Heads up" is the first section, and every surprise, failure, deletion and noticed problem is in it
- [ ] 120 words or fewer (60 for a small task)
- [ ] No technical word without a plain explanation
- [ ] "Done", "fixed" or "working" only where I actually tested it
- [ ] At most 1 question, with options and my recommendation
- [ ] Nothing I know is wrong or unfinished is left out
- [ ] A person who never coded could explain it back to me

## Examples

See [references/EXAMPLES.md](references/EXAMPLES.md) for 8 full before and after handoffs: a bug fix, a new feature, a failed task, a surprise change, a database change, a website release, a half finished job and a decision.

Short example:

```
**Heads up:** I also renamed the "Contact" page to "Get in touch", because the menu used that name. Say "undo" and I'll change it back.

**What I did:**
- The contact form now sends you an email every time someone fills it in.
- Spam messages with links are blocked before they reach you.

**Does it work:** Yes. I sent 3 test messages and all 3 arrived in your inbox.

**Not done yet:** Nothing, it's finished.

**Your decision:** Nothing needed from you.
```

## Additional resources

- [references/PLAIN-WORDS.md](references/PLAIN-WORDS.md): technical words and their plain versions, plus phrases to never use
- [references/QUESTION-RULES.md](references/QUESTION-RULES.md): how to ask for a decision, with good and bad examples
- [references/EXAMPLES.md](references/EXAMPLES.md): 8 full before and after examples
- [templates/HANDOFF.md](templates/HANDOFF.md): the standard, short and failed handoff forms
- [scripts/check_handoff.py](scripts/check_handoff.py): an automatic check of a handoff before sending
