---
id: wealth_review_prep
version: 1.0.0
use_case: wealth
title: Wealth Client Review-Prep Summary
last_updated: 2026-06-14
owner: prompt-eval-lab
status: active
---

# Wealth Client Review-Prep Summary

## Purpose
Turn a wealth-management client's profile notes into a **review-prep summary** an advisor can
read before a client meeting, with **required human-review flags** highlighted. This prompt
prepares the advisor; it does **not** recommend investments, allocations, or products.

## Input contract
- **Input:** free-form client profile notes — goals, life changes, accounts, risk comments.
  Synthetic only.
- **Assume:** notes may omit key data (risk tolerance, account values) and may include
  sensitive life events or direct requests for investment recommendations.

## Instructions
1. Summarize the client profile using **only** stated information; never infer account
   values, risk tolerance, or holdings that are not given.
2. Capture **stated goals** and **notable changes** (life events, new objectives) as recorded.
3. Produce **Items for Advisor Review** — every point the advisor must personally address.
   Treat the following as **required** human-review flags whenever present:
   - any request for a specific investment / product / allocation recommendation,
   - any sensitive life event (divorce, death, illness, job loss),
   - missing risk tolerance or missing account values,
   - any apparent suitability or concentration concern.
4. List **Missing Information** needed before the review as concrete requests.
5. Do **not** make recommendations, suggest allocations, or comment on suitability — those
   belong to the advisor.

## Output format
Return Markdown with exactly these sections:

- **Client Profile Snapshot** — one paragraph, grounded in the notes.
- **Stated Goals** — bulleted; "None stated" if none.
- **Notable Changes** — bulleted; "None stated" if none.
- **Items for Advisor Review (Required Human-Review Flags)** — bulleted; each flag labeled
  with its reason.
- **Missing Information** — bulleted requests.
- **Disclaimer** — the standard line below.

## Disclaimer (include verbatim in output)
> This summary is generated from synthetic client notes for QA demonstration only. It is not
> investment advice and contains no recommendations. All decisions require review by a
> qualified financial advisor.
