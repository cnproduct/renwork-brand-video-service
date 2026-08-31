# Reviewed video-learning workflow

## 1. Ingest

Inventory text, audio, video, images, manifests, subtitles, scripts, covers, and final artifacts. Record the exact URI, source type, observation time, rights/privacy state, tenant, brand profile, and SHA-256 for stable local files. Keep raw extraction separate from corrected or generated interpretation.

For video, inspect container, codecs, duration, resolution, frame rate, audio streams, and time base. Sample the beginning, scene boundaries, subtitle-dense sections, and ending. Metadata inspection is not audiovisual acceptance.

## 2. Subtitle and script learning

1. Map each script and subtitle file to its source clip, scene, manifest, and final artifact.
2. Extract all in-scope subtitle text before regeneration.
3. Classify each proposal: ASR, punctuation, terminology, meaning, compliance, timing, segmentation, or typography.
4. Check names, numbers, units, dates, institutions, product terms, buyer-evidence wording, prices, claims, and CTA against sources.
5. Present original, proposal, reason, confidence, and unresolved evidence sentence by sentence.
6. Promote terminology or phrasing only after the batch is explicitly reviewed.
7. Regenerate one affected item, verify the synchronized render, then expand to the batch.

## 3. Claim learning

Create one atomic claim per record. Assign evidence status, risk, applicability, review date, permitted phrasing, prohibited overstatement, and exact sources. Current or high-risk product, buyer, pricing, legal, financial, compliance, performance, or customer claims require authoritative-source checks and a named human reviewer.

Keep buyer evidence, contact verification, and sales priority independent. A public clue, email address, match score, or inaccessible customs source does not prove a confirmed buyer or recent transaction.

## 4. Incident to FAQ

Stage a FAQ when an incident is reproducible or evidence supports a useful diagnostic route. Capture symptom, impact, affected artifact, pipeline stage, expected versus observed state, detection/reproduction, root cause status, minimal repair, rollback, post-repair evidence, prevention, and scope limits.

Hypotheses remain staged. Confirmed fixes must be narrow enough that similar symptoms with different causes are not hidden.

## 5. Accepted-video learning

Only create an approvable success pattern from an exact artifact that has human acceptance and QA evidence. Link the artifact hash and production manifest. Record what was checked: script, subtitle text, timing, audio, frames, brand, duration, cover, final frame, delivery, and any waived gates.

Extract one reusable pattern at a time and state intended audience, format, use case, parameter values, and limits. Test on one new representative item before default activation.

## 6. Reuse

1. Retrieve only approved records matching tenant, brand profile, scope, audience, and review date.
2. List the exact record IDs in the production brief.
3. Generate without editing the active knowledge registry.
4. Validate and obtain audiovisual acceptance.
5. Return new observations, failures, and strengths to staging for the next review cycle.
