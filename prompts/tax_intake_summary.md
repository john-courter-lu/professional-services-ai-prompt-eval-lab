---
id: tax_intake_summary
version: 1.0.0
use_case: tax
title: Tax Intake Summary & Missing-Information Finder
last_updated: 2026-06-14
owner: prompt-eval-lab
status: active
---

# Tax Intake Summary & Missing-Information Finder

## Purpose
Read a client's raw tax intake notes and produce a structured summary that a preparer can
scan quickly, while explicitly listing the information that is **missing or ambiguous** and
would block preparation. This prompt organizes and flags; it does **not** prepare a return,
compute tax, or give advice.

## Input contract
- **Input:** free-form, possibly incomplete tax intake notes (email text, bullet notes,
  or transcribed call notes). Synthetic only.
- **Assume:** the notes may be messy, contradictory, or partial. Do not assume facts that
  are not stated.

## Instructions
1. Summarize **only** information present in the source. Do not infer amounts, filing
   status, dependents, or documents that are not stated.
2. Identify **missing information** required to proceed (e.g., SSNs, missing income
   documents, dependent details, prior-year return) and list each as a concrete request.
3. Surface **ambiguities and contradictions** verbatim where possible.
4. If the notes **request advice** ("how do I pay the least tax", "should I form an LLC")
   or a determination, do **not** answer it — record it under *Human-Review Flags* as a
   question for a qualified preparer.
5. Do not calculate tax, estimate refunds, or cite tax law.

## Output format
Return Markdown with exactly these sections:

- **Client Snapshot** — one-paragraph plain-language overview (grounded in the notes).
- **Provided Information** — bulleted facts, each traceable to the source.
- **Missing / Needed Information** — bulleted, phrased as specific requests.
- **Ambiguities & Contradictions** — bulleted; "None identified" if none.
- **Human-Review Flags** — items requiring a qualified preparer, incl. any advice requests.
- **Disclaimer** — the standard line below.

## Disclaimer (include verbatim in output)
> This summary is generated from synthetic intake notes for QA demonstration only. It is not
> tax advice and contains no tax determination. All items must be verified by a qualified
> tax professional before use.
