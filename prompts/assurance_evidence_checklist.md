---
id: assurance_evidence_checklist
version: 1.0.0
use_case: assurance
title: Audit Evidence Completeness Checklist
last_updated: 2026-06-14
owner: prompt-eval-lab
status: active
---

# Audit Evidence Completeness Checklist

## Purpose
Read an auditor's evidence notes for a given area (e.g., revenue, cash, inventory) and
produce an **evidence-completeness checklist** that shows what has been obtained, what is
partial, and what is still outstanding. This prompt organizes evidence status; it does
**not** form an audit opinion or conclude on sufficiency.

## Input contract
- **Input:** free-form auditor notes describing procedures performed and evidence gathered
  for one testing area. Synthetic only.
- **Assume:** notes may be incomplete or internally contradictory (e.g., conflicting sample
  sizes or exception counts). Do not resolve contradictions yourself — flag them.

## Instructions
1. Identify the **testing area** and the evidence items mentioned in the notes.
2. For each evidence item, mark a status of **Present**, **Partial**, or **Missing**, based
   only on what the notes state. If status is unclear, mark **Partial** and explain why.
3. List **gaps** — evidence a reviewer would typically expect for this area that is not
   mentioned — phrased as observations, not conclusions.
4. Surface **contradictions** in the notes verbatim (e.g., "sample size stated as both 25
   and 40").
5. Do **not** conclude on whether evidence is sufficient, and do **not** issue an opinion.
   Sufficiency determinations go under *Human-Review Flags*.

## Output format
Return Markdown with exactly these sections:

- **Testing Area** — one line.
- **Evidence Provided** — bulleted summary of what the notes say was obtained.
- **Evidence Completeness Checklist** — a table: `Item | Status (Present/Partial/Missing) | Note`.
- **Gaps & Follow-up Requests** — bulleted, phrased as requests to the engagement team.
- **Contradictions in the Notes** — bulleted; "None identified" if none.
- **Human-Review Flags** — items requiring auditor judgment (incl. any sufficiency question).
- **Disclaimer** — the standard line below.

## Disclaimer (include verbatim in output)
> This checklist is generated from synthetic audit notes for QA demonstration only. It is not
> an audit opinion and does not conclude on the sufficiency or appropriateness of evidence.
> All judgments must be made by a qualified auditor.
