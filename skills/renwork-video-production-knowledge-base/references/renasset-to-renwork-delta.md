# RenAsset to RenWork conversion delta

Source baseline: `cnproduct/renasset-brand-video-master` at commit `9599b71158f1a85fe57b9aa62efd107e1953dcc5`.

The source repository remains unchanged. This conversion reuses governance mechanics, not RenAsset brand facts or financial content.

| Area | Preserved from RenAsset | RenWork conversion | Not migrated |
|---|---|---|---|
| Learning boundary | Candidate extraction never means approval | `STAGED` and `APPROVED` remain separate and append-only | Automatic promotion from ASR, agent scores, or file presence |
| Record types | asset, knowledge, glossary, FAQ, success pattern | Same five types with required tenant and brand-profile scope | RenAsset-specific product taxonomy |
| Evidence states | VERIFIED, INTERNAL, PILOT, ASSUMPTION, DISPUTED, RETIRED | Retained for claims and operating knowledge | Treating marketing copy as verification |
| Claims gate | Authoritative support and human review for high-risk financial claims | Applies to any high-risk product, buyer, pricing, legal, financial, compliance, performance, or customer claim | RenAsset financial policies, bank-specific claims, or terminology |
| Subtitle learning | Sentence-level corrections before regeneration | Adds exact project/manifest mapping and preserves full-batch review | Silent LLM rewriting or ASR text as truth |
| Incident FAQ | Confirmed vs hypothesis root cause | Adds project, tenant, brand profile, artifact hash, rollback, and validation scope | Universalizing one incident |
| Success-pattern gate | User-approved artifact plus QA evidence | Requires immutable artifact hash and production manifest; recommends forward test | Video AQI or opening a file as acceptance |
| Delivery states | Local, QA, sync, publication separated | Adds knowledge approval, Git repository, deployment, destination verification, and business result | Reporting repository publication as production deployment |
| Brand system | RenAsset visual DNA | Resolve current RenWork tenant brand profile at runtime | RenAsset logo, colors, finance positioning, and hard-coded contact claims |

## Capability state after conversion

- **AVAILABLE**: policy, append-only CLI, scope validation, approval gates, tests, and integration contract.
- **AVAILABLE BY COMPOSITION**: scene acceptance evidence from `renwork-training-scene-videos` can support a staged `success_pattern`.
- **REQUIRES HUMAN REVIEW**: subtitle meaning changes, claims, FAQ root causes, reusable success patterns, public knowledge cards, and template activation.
- **NOT CLAIMED**: automatic cross-repository synchronization, production deployment, external publication, or business-performance improvement.
