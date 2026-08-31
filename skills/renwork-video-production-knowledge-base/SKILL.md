---
name: renwork-video-production-knowledge-base
description: Build and maintain a tenant-scoped, review-gated RenWork video-production knowledge base from source assets, subtitle corrections, verified claims, editing incidents, and human-accepted finished videos. Use when RenWork video work should create reusable knowledge without promoting raw ASR, hypotheses, generated clips, or unreviewed claims into active production guidance.
---

# RenWork Video Production Knowledge Base

Turn reviewed production evidence into reusable RenWork knowledge. Keep rendering and learning as two connected but independently gated loops: the production manifest records what was generated and accepted; this knowledge base records what may be reused.

## Non-negotiable boundary

`generated` is not `accepted`, and `STAGED` is not `APPROVED`.

Never promote raw ASR/OCR, model rewrites, unsupported claims, root-cause hypotheses, merely generated clips, or cross-tenant content into active knowledge. Resolve identity, tenant, brand profile, purpose, rights, privacy, and source scope before staging. The CLI fixes `tenant_id` and `brand_profile_id` at initialization and rejects conflicting record scope.

## Initialize or inspect the registry

```bash
python3 scripts/renwork_video_kb.py init \
  --kb-root /absolute/project/knowledge-base \
  --tenant-id tenant-acme \
  --brand-profile-id acme-brand

python3 scripts/renwork_video_kb.py validate \
  --kb-root /absolute/project/knowledge-base
```

The helper creates append-only `staging/`, `approved/`, and `reviews/` registries for `asset`, `knowledge`, `glossary`, `faq`, and `success_pattern`.

## Capture and promote learning

Read [learning-workflow.md](references/learning-workflow.md) and stage the smallest atomic record with traceable sources. The record remains a candidate until a named reviewer approves it.

```bash
python3 scripts/renwork_video_kb.py stage \
  --kb-root /absolute/project/knowledge-base \
  --type faq \
  --record /absolute/project/candidates/subtitle-drift.json

python3 scripts/renwork_video_kb.py approve \
  --kb-root /absolute/project/knowledge-base \
  --type glossary \
  --id glossary-approved-term \
  --reviewer "Brand QA" \
  --note "Approved against the source script and rendered subtitle set"
```

Approval appends a reviewed copy to `approved/<type>.jsonl` and an event to `reviews/promotion_log.jsonl`; it does not delete the staged record. Read [quality-gates.md](references/quality-gates.md) before approval.

## Learn from an accepted video

Route scene-by-scene work through [`renwork-training-scene-videos`](../renwork-training-scene-videos/SKILL.md). A `success_pattern` may be approved only when it links the exact accepted artifact URI and SHA-256, its `video-production-manifest.json`, `user_approved: true`, concrete QA evidence, applicability, and scope limits.

Extract one pattern per record, such as hook structure, pacing, subtitle segmentation, visual hierarchy, logo treatment, transition, mix, or CTA. Forward-test it on one representative new item before making it a default template.

## Seven gates

1. **Source and privacy**: exact source, stable file/hash, rights, intended use, data minimization, tenant and brand scope.
2. **Claim and terminology**: evidence status, authority, applicability, dates, numbers, names, prohibited overstatement, high-risk reviewer.
3. **Subtitle text**: full in-scope batch mapped and reviewed sentence by sentence before regeneration.
4. **Render integrity**: streams, duration, frame rate/time base, subtitle coverage, file mapping, no unexplained freeze or duplicate footage.
5. **Representative audiovisual QA**: beginning, boundaries, subtitle-dense sections, ending, audio, logo, cover, final frame, and picture-subtitle-audio sync.
6. **Success-pattern promotion**: immutable accepted artifact, human acceptance, QA evidence, narrow pattern, scope limits, and forward test.
7. **Status separation**: local generation, structural validation, audiovisual acceptance, knowledge approval, repository sync, deployment, publication, and business outcome are reported separately.

## Record rules

Use [record-schemas.md](references/record-schemas.md) for exact fields.

- `asset`: source inventory and observation; never active guidance by itself.
- `knowledge`: atomic claim or operating rule with `VERIFIED`, `INTERNAL`, `PILOT`, `ASSUMPTION`, `DISPUTED`, or `RETIRED` evidence state.
- `glossary`: canonical term and observed variants with validation basis.
- `faq`: reproducible incident, confirmed or hypothetical cause, minimal repair, rollback, validation, prevention, and scope limits.
- `success_pattern`: accepted artifact evidence and one reusable production characteristic.

`VERIFIED` requires a primary-authority or official-product source. `ASSUMPTION`, `DISPUTED`, and `RETIRED` knowledge cannot enter `approved/`. A hypothetical FAQ cannot be approved as a deterministic solution. High-risk approved knowledge requires a review date and prohibited-overstatement text.

## Integration contract

The active production skill may read only approved records whose tenant, brand profile, scope, review state, and validity fit the current project. It must list the records used in the production brief. New outputs and incidents return to `staging/`; they never modify the active knowledge base automatically.

For the RenWork Growth OS knowledge base, publish only governance-level cards and golden cases from reviewed repository policy. Tenant assets, raw traces, local paths, customer data, transcripts, videos, and approval logs remain private project data.

The conversion decisions are recorded in [renasset-to-renwork-delta.md](references/renasset-to-renwork-delta.md).
