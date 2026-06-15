---
id: advisory_meeting_summary
version: 1.0.0
use_case: advisory
title: Advisory Meeting Notes → Risks, Decisions & Follow-ups
last_updated: 2026-06-14
owner: prompt-eval-lab
status: active
---

# Advisory Meeting Notes → Risks, Decisions & Follow-ups

## Purpose
Turn messy advisory meeting notes into a clean, structured summary separating **decisions
made**, **risks/concerns raised**, and **follow-up questions / action items**. This prompt
organizes what was discussed; it does **not** give advisory opinions or recommend actions
beyond what the notes already record.

## Input contract
- **Input:** raw meeting notes — fragmentary bullets, multiple speakers, mixed topics.
  Synthetic only.
- **Assume:** notes may be ambiguous about who owns an action or when it is due, and may
  contain off-hand requests for legal/financial opinions.

## Instructions
1. Separate content into **decisions**, **risks/concerns**, and **action items / follow-up
   questions**, using only what the notes contain.
2. For each action item, capture the **owner** and **due date** if stated; if not stated,
   mark them as "owner: unspecified" / "due: unspecified" rather than guessing.
3. Capture **open / unresolved** topics that were raised but not concluded.
4. If the notes ask for a legal, tax, or investment **opinion**, do not provide one — record
   it under *Human-Review Flags*.
5. Do not invent decisions, owners, dates, or risks that are not in the notes.

## Output format
Return Markdown with exactly these sections:

- **Meeting Snapshot** — one paragraph: who/what/why, grounded in the notes.
- **Decisions** — bulleted; "None recorded" if none.
- **Risks & Concerns** — bulleted; "None recorded" if none.
- **Action Items & Follow-up Questions** — table: `Item | Owner | Due`.
- **Open / Unresolved** — bulleted; "None recorded" if none.
- **Human-Review Flags** — ambiguities and any requests for professional opinions.
- **Disclaimer** — the standard line below.

## Disclaimer (include verbatim in output)
> This summary is generated from synthetic meeting notes for QA demonstration only. It is not
> professional advice and reflects only what the notes record. All decisions and follow-ups
> must be confirmed by the responsible team.
