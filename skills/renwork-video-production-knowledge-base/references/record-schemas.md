# Registry record contract

The helper stores newline-delimited JSON under `<kb-root>/staging/` and `<kb-root>/approved/`. It injects the initialized `tenant_id` and `brand_profile_id` when absent and rejects conflicting values.

All staged records require `id`, `title`, and non-empty `sources`. Each source has a non-empty `uri` and should include `source_type` and `observed_at`. Supported source types include `user_asset`, `primary_authority`, `official_product`, `internal`, `observed_output`, `public_reference`, and `secondary`.

## `asset`

Required: `input_kind`, `source_uri`, `rights_status`, `privacy_classification`. `input_kind` is `text`, `audio`, `video`, `image`, or `manifest`. Store stable hashes and sync state in `observations` when available.

## `knowledge`

Required: `claim`, `domain`, `evidence_status`, `risk_level`, and `applicability`. `VERIFIED` requires `primary_authority` or `official_product` evidence. Approved high-risk records require `review_due` and `prohibited_overstatement`.

## `glossary`

Required: `canonical`, list of `variants`, `domain`, `language`, and `validation_note`. Preserve the observed variant; never rewrite source evidence in place.

## `faq`

Required: `symptom`, `impact`, `pipeline_stage`, `root_cause_status`, `root_cause`, `resolution`, list of `validation`, `rollback`, `prevention`, and `scope_limits`. `root_cause_status` is `confirmed` or `hypothesis`; only confirmed records can be approved as deterministic guidance.

## `success_pattern`

Required: `artifact_uri`, 64-character `artifact_sha256`, `manifest_uri`, `user_approved`, list of `qa_evidence`, `pattern`, `applicability`, and `scope_limits`. Approval requires `user_approved: true` and non-empty QA evidence.

Every approved record also has an `approval` object with `reviewer`, `reviewed_at`, and `note`.
