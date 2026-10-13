# Examples: Before and After

8 real style handoffs. Each "before" is the kind of summary people stop reading. Each "after" is the same facts as a plain handoff. Notice that nothing important is removed: surprises and failures move to the top instead.

All names, numbers and projects below are invented examples.

---

## 1. A bug fix

**Before (what people skip):**
> I traced the issue to a race condition in the checkout flow where `useEffect` was firing before the cart state hydrated from localStorage, causing `cart.items` to be undefined on first render. I refactored the hook to gate on a `hydrated` flag, added a null guard in `CheckoutSummary`, and wrote 3 unit tests covering the empty, partial and full cart states. All 42 tests pass. I also updated `eslint` to the latest version since it was flagging the hook. Let me know if you'd like me to look at the other components using the same pattern.

**After:**
```
**Heads up:** I also updated the code style checker to a newer version. Nothing changes for customers. Say "undo" if you'd rather keep the old one.

**What I did:**
- Fixed the checkout page going blank for some customers when it first opened.

**Does it work:** Yes. I tested an empty cart, a cart with 1 item and a full cart, and all 42 automatic checks pass.

**Not done yet:** 2 other pages use the same risky pattern. They work today but could break the same way.

**Your decision:** Should I fix those 2 pages now?
- **A:** Yes, now (about 10 minutes)
- **B:** Later
I recommend **A**, because it stops the same problem coming back.
```

What changed: the surprise (an unrequested update) moved to the top, the jargon became the effect on customers, and the vague "let me know" became one clear question.

---

## 2. A new feature

**Before:**
> Implemented the booking confirmation flow. Added a `sendConfirmation` handler wired to the `booking.created` webhook, created a transactional template in Resend with dynamic fields for date, time and location, added an env var `RESEND_API_KEY` (you'll need to set this in Vercel), and updated the booking model with a `confirmationSentAt` timestamp. Tested locally with a sandbox key.

**After:**
```
**Heads up:** You need to add 1 password for the email service before this works on the live site. I can walk you through it in 2 minutes.

**What I did:**
- Customers now get a confirmation email with the date, time and place after they book.

**Does it work:** Yes on this computer, using a test account. Not yet on the live site, because of the missing password.

**Not done yet:** Adding the email password to the live site.

**Your decision:** Shall I walk you through adding it now?
- **A:** Yes
- **B:** Later
I recommend **A**, because until then no customer gets the email.
```

---

## 3. A failed task

**Before:**
> I attempted the Stripe integration but ran into a 401 from the API when creating the PaymentIntent. I suspect the publishable key is being used where the secret key is required, or the key is for test mode while the account is in live mode. I've left the code in place behind a feature flag so it doesn't affect production. Could you check the dashboard and confirm which keys are active?

**After:**
```
**Heads up:** Card payments don't work yet. Customers can't pay by card until this is fixed. Nothing else on the site is affected.

**What I did:**
- Built the card payment step, but kept it switched off so customers don't see a broken page.

**Does it work:** No. The payment company rejected the connection. I think the wrong key (a password for apps) is in place.

**Not done yet:** Connecting the right key and testing a real payment.

**Your decision:** Can you open your Stripe dashboard so I can show you which key to copy? It takes about 3 minutes.
```

---

## 4. A surprise change

**Before:**
> Done with the pricing page copy updates. While I was in `PricingTable.tsx` I noticed the annual toggle was calculating the discount wrong (it was applying 20% on top of the already discounted price), so I fixed the calculation. I also removed the unused `LegacyPlan` component and its styles.

**After:**
```
**Heads up:** 2 things you didn't ask for. First, I fixed a pricing mistake: yearly prices showed a bigger discount than you offer, so they now go up slightly. Second, I deleted an old pricing section no one could see.

**What I did:**
- Updated the wording on the pricing page as you asked.

**Does it work:** Yes. I checked the monthly and yearly prices on the page.

**Not done yet:** Nothing, it's finished.

**Your decision:** Keep the corrected yearly prices?
- **A:** Keep them (they now match your real discount)
- **B:** Put the old numbers back
I recommend **A**, because the old numbers promised a discount you don't give.
```

---

## 5. A database change

**Before:**
> Wrote and ran migration `20261013_add_customer_tags` which adds a `tags` jsonb column with a GIN index to the `customers` table, backfilled 3,212 rows with an empty array, and updated the Prisma schema. Migration applied successfully on staging. Ready to apply to prod when you are.

**After:**
```
**Heads up:** Nothing unexpected.

**What I did:**
- Added a way to put labels (like "VIP" or "wholesale") on each customer.
- Tried it on the practice copy of the app with all 3,212 customers. It worked.

**Does it work:** Yes on the practice copy. Not on the live app yet.

**Not done yet:** Making the same change on the live app.

**Your decision:** Make this change on the live app now?
- **A:** Yes, now (about 1 minute, the app keeps working)
- **B:** Tonight
I recommend **A**, because it's quick and only adds something. I'll make a safety copy first. This can be undone, but it takes some work.
```

---

## 6. A website release

**Before:**
> Merged PR #48 into main, CI is green, and the Vercel production deployment succeeded (build 2m 14s). Lighthouse performance went from 71 to 89. Note that the deploy invalidated the CDN cache so the first few page loads may be slower.

**After:**
```
**Heads up:** The first few visits after the update may load a little slower while the site warms up. This is normal and passes within minutes.

**What I did:**
- Put the new version of the website live.
- The site now loads noticeably faster (speed score up from 71 to 89).

**Does it work:** Yes. All automatic checks passed and I opened the live site to confirm.

**Not done yet:** Nothing, it's finished.

**Your decision:** Nothing needed from you.
```

---

## 7. A half finished job

**Before:**
> Progress update: completed the CSV import parser, validation layer and the preview UI. Remaining: duplicate detection, error reporting UI, and the commit step. Currently the import preview works but clicking "Import" is a no-op. I've stubbed `commitImport()`.

**After:**
```
**Heads up:** The Import button doesn't do anything yet. Please don't tell customers about this feature until it's finished.

**What I did:**
- You can now upload a spreadsheet of contacts and see a preview of them.

**Does it work:** The upload and preview work. The final import step doesn't exist yet.

**Not done yet:** Finding duplicates, showing errors, and actually saving the contacts. About 3 more steps.

**Your decision:** Carry on with the remaining steps now?
- **A:** Yes
- **B:** Pause here
I recommend **A**, so the feature is usable today.
```

---

## 8. A decision needed

**Before:**
> There are two approaches for the search: (1) Postgres full text search with tsvector, cheap and simple but weaker typo tolerance and no relevance tuning; (2) Algolia, excellent typo tolerance and speed but $0.50 per 1k requests beyond the free tier, plus vendor lock in and an additional sync job. Which would you prefer? I could also look at Meilisearch self hosted as a middle ground.

**After:**
```
**Heads up:** Nothing unexpected. I haven't built anything yet, I need your choice first.

**What I did:**
- Compared 2 ways to add a search box to your shop.

**Does it work:** Not built yet.

**Not done yet:** Building the search box once you choose.

**Your decision:** Which search do you want?
- **A:** Free, built in (fine for most searches, weaker with spelling mistakes)
- **B:** A paid search service (handles typos better, costs money as traffic grows)
I recommend **A** for now, because you can switch later if customers complain.
```

---

## What every "after" has in common

1. Surprises, problems and things the person must do come first.
2. Every sentence is about what changed for the person or their customers.
3. "Does it work" is honest and specific about how it was checked.
4. One clear question with options and a recommendation, or "Nothing needed from you".
5. Under 120 words, with no technical word left unexplained.
