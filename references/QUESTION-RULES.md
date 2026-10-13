# Question Rules

How to ask a person for a decision so they can answer in seconds, and so a tired "yes" never causes damage.

## Why this matters

When a decision is buried inside a long technical message, most people skip it and reply "ok" or "fix everything". The AI then guesses. A clear question with a recommendation turns that guess into a real choice.

## The shape of every question

```
**Your decision:** [The question in 1 plain sentence.]
- **A:** [option] ([what happens if you choose it])
- **B:** [option] ([what happens if you choose it])
I recommend **A**, because [1 short reason]. [Risk line, only if needed.]
```

If you only need the person to do 1 simple thing (open a page, paste a password, click a button), skip the options and ask plainly: "Can you open your Stripe dashboard so I can show you which key to copy? It takes about 3 minutes."

Rules:
1. **One question.** Never 2 questions in one message. If more are waiting, ask the most important one and say how many smaller ones are left.
2. **2 or 3 options.** Never more than 3. Never leave it open ("what do you want to do?") when you can offer options. (The 1 simple thing above is the only exception.)
3. **Each option says what happens.** The person should not have to imagine the result.
4. **Always recommend.** Say which option you would pick and why, in 1 short reason. The person can still choose another.
5. **Easy to answer.** They should be able to reply with one letter or one word.
6. **Plain words.** Same rules as the handoff. No jargon in the options.

## The risk line

Add one risk line when any option is hard to undo, costs money, reaches real people, or touches live data.

| Risk | Risk line to add |
| --- | --- |
| Can be undone easily | (no line needed) |
| Can be undone, with some effort | "This can be undone, but it takes some work." |
| Can't be undone | "This can't be undone." |
| Reaches real people | "This will be sent to [number] real customers." |
| Costs money | "This will cost about [amount]." |
| Changes the live website or app | "Customers will see this straight away." |

For anything that can't be undone, reaches real people, costs money, deletes something, or changes the live website, app or data, the person must reply with a clear yes. "Ok", "sure" or "fix everything" is not a clear yes for these. Ask again in one line: "Just to be sure: reply YES to [action]."

## When NOT to ask

Do not ask about things the person can't judge or doesn't care about. Decide yourself, choosing the safe and reversible option, and mention it in one line under "What I did".

Don't ask:
- Which internal tool, library or file name to use
- How to structure the code
- Whether to fix a small mistake you made yourself (fix it and mention it)
- Things they already answered earlier in this conversation

Do ask:
- Anything that changes what users or customers see or receive
- Anything that costs money, deletes something or can't be undone
- Anything where their business knowledge decides the answer (prices, policies, wording, who gets access)
- Anything you did that they didn't ask for, if keeping it is a real choice

## Good and bad examples

### 1. A design choice

**Bad:**
> I've implemented the modal with a controlled state pattern. Should I also add the portal wrapper and keyboard trap for accessibility, and do you want the backdrop click to dismiss, or should we keep it explicit given the form state? Also the z-index might conflict with the header.

**Good:**
> **Your decision:** Should the pop up close when someone clicks outside it?
> - **A:** Yes (faster, but they could lose what they typed)
> - **B:** No, only with the close button (safer for long forms)
> I recommend **B**, because people fill in a long form in that pop up.

### 2. Something you did that they didn't ask for

**Bad:**
> Note: I also bumped several dependencies and refactored the utils folder while I was in there.

**Good:**
> **Your decision:** While fixing the bug, I also updated 4 ready made tools the app uses. Keep the updates?
> - **A:** Keep them (newer and safer, all checks still pass)
> - **B:** Undo them (back to exactly how it was)
> I recommend **A**, because all 42 automatic checks still pass with the updates.

### 3. A risky step

**Bad:**
> Ready to run the migration on prod, ok to proceed?

**Good:**
> **Your decision:** Change how customer addresses are stored on the live app?
> - **A:** Yes, do it now (takes about 2 minutes, the app keeps working)
> - **B:** Wait, do it tonight when fewer people use it
> I recommend **B**, because it's the safest time. I'll make a safety copy first either way. This can be undone, but it takes some work.

### 4. Several decisions waiting

**Bad:**
> A few things: 1) logo size? 2) which email provider? 3) should the free plan include exports? 4) dark mode?

**Good:**
> **Your decision:** Should the free plan include downloading reports?
> - **A:** Yes (more people sign up)
> - **B:** No, paid plans only (more reason to upgrade)
> I recommend **B**, because it's the main reason to pay.
> Also waiting for you: 3 smaller choices. I'll ask after this one.

### 5. A vague reply

The person replies: "just fix everything and make it all work perfectly"

**Bad:** silently changing 14 files, including the undo of an earlier change they never decided on.

**Good:**
> Here's what I'll do: fix the 2 broken buttons on the checkout page and finish the email step.
> One thing first: earlier I changed the login page by mistake, and you haven't told me whether to keep it. I'll put it back the way it was unless you say keep.
> Reply yes to go, or tell me what to change.

## Checklist for every question

- [ ] Only 1 question
- [ ] 2 or 3 options, each with what happens
- [ ] My recommendation and 1 reason
- [ ] A risk line if it can't be undone, costs money, reaches people or changes the live app
- [ ] A clear YES required for those risky actions
- [ ] Plain words only
