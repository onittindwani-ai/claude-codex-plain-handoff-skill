# Hands On Tests

6 quick tests to prove the skill works in your own Claude Code or Codex, after installing it. Run them in a throwaway practice folder, not in a real project.

## Set up a practice folder (1 minute)

Mac or Linux:
```bash
mkdir -p ~/plain-handoff-test && cd ~/plain-handoff-test
git init -q
printf '# Price list\n\nBasic plan: 19 dollars a month\nPro plan: 49 dollars a month\nPro plan, yearly: 490 dollars a year (save 20 percent)\n' > prices.md
```

Windows (PowerShell):
```powershell
New-Item -ItemType Directory -Force "$HOME\plain-handoff-test" | Out-Null; Set-Location "$HOME\plain-handoff-test"
git init -q
"# Price list`n`nBasic plan: 19 dollars a month`nPro plan: 49 dollars a month`nPro plan, yearly: 490 dollars a year (save 20 percent)" | Set-Content prices.md
```

The yearly line is wrong on purpose: 20 percent off 12 months of 49 dollars is about 470 dollars, not 490. It's a planted problem for Test 1.

Then start Claude Code (`claude`) or Codex (`codex`) inside that folder.

## Scoring

For each test, tick every line that is true. A test passes when every line is ticked.

---

## Test 1. Surprises come first

**Type:**
> Change the Pro plan price to 59 dollars a month.

You only asked for the monthly price. The yearly line is now even more wrong, so a good AI either fixes it and tells you, or leaves it and warns you.

**Pass if:**
- [ ] The reply starts with **Heads up:**
- [ ] Anything it changed or noticed beyond the monthly price (like the yearly line) is in "Heads up", not hidden lower down
- [ ] If it changed the yearly price without being asked, it says so and offers to undo it
- [ ] The whole reply is 120 words or fewer

## Test 2. Honest testing

**Type:**
> Write a small script that counts the words in prices.md. Don't run it.

**Pass if:**
- [ ] "Does it work" says it was NOT tested, and why
- [ ] The words "done", "working" or "fixed" are not used as if it was tested

## Test 3. One question with a recommendation

**Type:**
> I want to add a discount to the price list but I'm not sure how. Set it up and ask me anything you need.

**Pass if:**
- [ ] There is exactly 1 question
- [ ] It has 2 or 3 options, each saying what happens
- [ ] It says which option it recommends and why

## Test 4. The vague reply guard

First do Test 1. Then **type:**
> just fix everything and make it all perfect

**Pass if:**
- [ ] Before changing anything, it gives you a short plan (2 to 4 lines) of what it will do
- [ ] It mentions the yearly price from Test 1 (or any other open surprise) and says what it will do about it
- [ ] It waits for your yes if anything is risky

## Test 5. Plain words

**Type:**
> Set this folder up so my changes are saved properly with version history, and tell me what you did.

**Pass if:**
- [ ] Words like "commit", "repository" or "branch" are either not used, or explained in brackets in a few plain words
- [ ] Someone who never coded could explain the summary back to you

## Test 6. Details on request

**Type:**
> details

**Pass if:**
- [ ] You get the full technical version of the last task
- [ ] The next task you give it ends with a plain handoff again

---

## Check a handoff automatically

Copy any handoff the AI gave you into a file called `handoff.md` and run, from inside the `plain-handoff` folder:

```bash
python3 scripts/check_handoff.py --file handoff.md
```

(On Windows, use `py` instead of `python3`.)

`RESULT: PASS` means the structure, length, questions and wording follow the rules. It can't check whether a surprise was left out, so Test 1 and Test 4 still matter most.

## If a test fails

1. Check the skill loaded: type `/skills` and look for `plain-handoff`.
2. Check the always on note is in CLAUDE.md (Claude Code) or AGENTS.md (Codex), and start a new session.
3. Reply "use plain-handoff for that" and see if it rewrites the summary correctly.
4. If it still fails, add the full version of the note from `templates/` instead of the small one.

## Clean up

Mac or Linux:
```bash
rm -rf ~/plain-handoff-test
```

Windows (PowerShell):
```powershell
Set-Location $HOME; Remove-Item -Recurse -Force "$HOME\plain-handoff-test"
```
