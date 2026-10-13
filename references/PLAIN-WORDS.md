# Plain Words

Use this when writing a handoff. Left: the technical word. Middle: what to say instead. Right: when the technical word is still fine.

Golden rule: describe what changed for the person, not the machinery. "Your customers can now pay by card" beats any accurate technical sentence about the payment integration.

If a technical word is truly needed (for example the person will have to click a button with that name), use it once with a plain explanation in brackets: "Click Deploy (put the new version live)".

## Code and files

| Technical | Say instead | Technical word is fine when |
| --- | --- | --- |
| refactor | tidied up the code, nothing changes for users | never in a handoff |
| function, method | a piece of the code that does [job] | never; name the job instead |
| component | the [name] part of the page | the person uses that word |
| module, package | a part of the app | never |
| dependency | a ready made tool the app uses | they must install or approve it |
| library, SDK | a ready made toolkit from [company] | never |
| config, configuration | settings | never |
| environment variable, env var | a hidden setting (like a password or key) | they must set it themselves; then say where |
| hardcoded | written directly into the code | never |
| deprecated | old, and will stop working in future | never |
| bug | a mistake in the code | fine as is; most people know it |
| edge case | a rare situation, for example [example] | never; give the example |
| regression | something that used to work broke | never |
| null, undefined | empty, missing | never |
| syntax error | a typing mistake in the code | never |
| linter, lint | a spelling and style checker for code | never |
| build | getting the app ready to run | "the build failed" becomes "the app would not start" |
| compile | turn the code into a working app | never |
| CLI | the text command tool | never |

## Saving and sharing work (git)

| Technical | Say instead | Technical word is fine when |
| --- | --- | --- |
| commit | saved a checkpoint of the work | the person uses git themselves |
| push | uploaded the saved work to [GitHub] | never |
| pull | downloaded the latest work | never |
| branch | a separate copy to work on safely | the person must choose or name it |
| merge | combined the work into the main version | never |
| merge conflict | two changes clashed and I had to choose between them | never; say what you chose |
| pull request, PR | a change waiting for approval | the person reviews PRs; then link it |
| revert, roll back | undid the change | never |
| repository, repo | the project folder | never |
| diff | the list of changes | never |

## Websites, servers and hosting

| Technical | Say instead | Technical word is fine when |
| --- | --- | --- |
| deploy, ship, release | put the new version live | they press a button with that name |
| production, prod | the live version real customers use | never |
| staging, dev | a practice copy that customers can't see | never |
| server | the computer that runs the app online | never |
| localhost | only on this computer, not online yet | never |
| frontend | the part people see and click | never |
| backend | the behind the scenes part | never |
| API | a connection between two apps | they must create or copy an API key |
| endpoint | an address the app sends data to | never |
| webhook | an automatic message one app sends another | they must paste a webhook link |
| domain, DNS | the website address, its settings | they must change it at their provider |
| SSL, HTTPS, certificate | the padlock that keeps the site secure | never |
| cache | a saved copy to make things faster | "clear the cache" becomes "refresh the saved copy" |
| downtime | the site was offline | fine; add how long |
| latency, performance | speed | never |
| rate limit | a limit on how many requests are allowed | never |
| timeout | it took too long and gave up | never |

## Data and databases

| Technical | Say instead | Technical word is fine when |
| --- | --- | --- |
| database, DB | where the app stores its information | fine once; most people get it |
| migration | a change to how information is stored | never; say what it changes |
| schema | the layout of the stored information | never |
| table, row, record | the list, one entry | "row" is fine for spreadsheet users |
| query | a search of the stored information | never |
| seed data | sample information for testing | never |
| backup | a safety copy | fine as is |
| data loss | some information was deleted and can't be brought back | never soften this |
| duplicate | the same thing saved twice | fine as is |

## Testing and checks

| Technical | Say instead | Technical word is fine when |
| --- | --- | --- |
| unit test, integration test | an automatic check | never |
| test suite | all the automatic checks | never |
| tests pass | all the automatic checks passed | fine with "all" or a number |
| tests fail | [number] checks failed, meaning [effect] | never without the effect |
| CI, pipeline | the automatic checks that run online | never |
| type error | the code expected one kind of value and got another | never |
| flaky | sometimes passes, sometimes fails | never |
| smoke test | a quick check that the basics work | never |
| coverage | how much of the code the checks look at | never |

## Security and access

| Technical | Say instead | Technical word is fine when |
| --- | --- | --- |
| authentication, auth | logging in | never |
| authorization, permissions | who is allowed to do what | never |
| token, API key, secret | a password for apps | fine as is; never paste one in a handoff |
| encryption | locked so only the right people can read it | never |
| vulnerability | a weak spot someone could misuse | never |
| exposed, leaked | could be seen by people who shouldn't see it | never soften this |
| OAuth, SSO | signing in with Google, Microsoft or similar | never |

## AI words

| Technical | Say instead | Technical word is fine when |
| --- | --- | --- |
| context window | how much I can keep in mind at once | never |
| tokens | the amount of text I process (it affects cost) | when talking about cost; add the number |
| hallucination | I made something up that isn't true | fine with the plain version |
| prompt | the instruction you gave me | fine as is |
| agent | an AI that can take actions, not just chat | fine once |
| tool call | an action I took, like reading a file | never |
| subagent | a helper AI I used for part of the job | never |
| MCP | a connection that lets me use another app | never |

## Phrases to never use in a handoff

| Never say | Why | Say instead |
| --- | --- | --- |
| "Some minor tweaks" | Hides what changed | Name the change in one sentence |
| "Various improvements" | Hides what changed | List the 1 to 3 that matter |
| "Should work now" | Sounds tested, isn't | "I haven't tested it yet, because ..." or "I tested it and it works" |
| "Everything is done" | Rarely fully true | "It's finished" only after a real check; otherwise list what's left |
| "As discussed" or "as mentioned above" | They didn't read above | Say it again in one line |
| "Under the hood" or "behind the scenes" (with no detail) | Vague | Say what changed for them |
| "It's a known issue" | Sounds like an excuse | Say what it means for them and what to do |
| "Just" (as in "just run the migration") | Makes a hard thing sound easy | Say exactly what they need to do |
| "Robust", "seamless", "leverage", "streamline" | Empty words | Say the actual result |
| "Let me know if you have any questions" | Adds nothing | End after the decision line |

## Quick self test

Read your handoff and ask: could someone who has never written code explain each line back to me in their own words? If one line fails, rewrite that line with words from the middle column.
