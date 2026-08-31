---
name: renwork-training-scene-videos
description: Produce resumable, scene-by-scene RenWork training, workshop, consulting, customer-service, or demo videos and track every scene, cover, composite, copy, revision, and acceptance gate. Use when a multi-scene RenWork video must survive provider round limits or interrupted generation; use a general brand-video skill for unrelated one-shot films.
---

# RenWork Training Scene Videos

Turn a training brief into independently reviewable scene clips, then a synchronized final package. Treat the artifact manifest as the operational record; chat history is not the source of truth.

## Non-negotiable state boundary

`generated` means a file exists. It does not mean the scene or final film is correct. Keep these states distinct:

`planned -> prompted -> generating -> generated -> technically_verified -> accepted`

Use `needs_revision` when the file plays but fails content review, and `blocked` when credentials, quota, missing inputs, permissions, or provider failure prevent progress. Never label the final package accepted until a human has reviewed picture, subtitles, and audio together.

## Start or resume a project

Resolve one workspace and one brand profile. Do not mix tenant assets, logos, claims, source footage, or credentials. Record the brief source, target channel, aspect ratio, duration, language, CTA, output directory, and the exact scene list.

Initialize a manifest when one does not exist:

```bash
python3 scripts/artifact_manifest.py init \
  --root /absolute/project/path \
  --project-id renwork-training-camp \
  --brand-profile-id renwork \
  --scene '1:training_classroom:全员实操培训' \
  --scene '2:consulting_diagnosis:1对1增长诊断'
```

If a manifest exists, scan it before generating anything:

```bash
python3 scripts/artifact_manifest.py scan --manifest /absolute/project/path/video-production-manifest.json
python3 scripts/artifact_manifest.py validate --manifest /absolute/project/path/video-production-manifest.json
```

Read [references/manifest-contract.md](references/manifest-contract.md) when creating, repairing, or integrating a manifest. Do not replace an existing manifest merely because its artifact paths are stale; scan or update it.

## Production workflow

1. Lock the scene contract before generation: purpose, visible people/action, setting, required brand cues, narration, on-screen caption, duration, continuity, source/reference images, and prohibited content.
2. Generate one independently usable clip per scene. Use the provider the user selected; provider names and quota behavior are runtime facts, not hard-coded assumptions.
3. After every attempt, record provider, attempt status, note, and selected file. When a provider permits only one clip per round, checkpoint the completed scene and continue with the next scene in a new round instead of regenerating prior scenes.
4. Verify each selected clip with `ffprobe` and visual playback. Reject a clip with wrong people/action, unreadable or fabricated UI, wrong logo, duplicate footage, abrupt freeze, black frames, or content that does not support its narration.
5. Compose only accepted or explicitly provisionally approved scene clips. Build the timing map from final narration/audio durations rather than guessed caption lengths.
6. Generate channel-ready cover variants and companion copy as separate tracked artifacts. Applying a cover means inserting or encoding it into the intended deliverable, not merely creating a PNG.
7. Review the rendered film in a real player at the beginning, every scene boundary, subtitle-dense sections, and the ending. Record each acceptance gate with evidence.

Read [references/production-workflow.md](references/production-workflow.md) for the scene contract, prompt structure, continuation rules, synchronization loop, and delivery package.

## Revision rules

- Preserve accepted scene clips unless the correction requires changing them.
- When picture, subtitle, and audio disagree, fix the timing map or source mapping and rerender all three as one unit; do not patch only the subtitle text.
- When mixing source videos, track source ranges and reject repeated shots unless repetition is intentional and documented.
- Do not silently loop billable generation. Record every attempt and stop when the provider blocks progress or repeated attempts fail for the same reason.
- Preserve earlier composites and increment the output version. Never overwrite the last accepted artifact.

## Acceptance gates

The release candidate must pass:

- `technical_playback`: final file parses, plays, has the intended streams, resolution, frame rate, and duration.
- `scene_content_match`: every scene visually supports its approved scene contract and narration.
- `picture_subtitle_audio_sync`: picture, subtitle, and spoken line align throughout the timeline.
- `no_duplicate_footage`: no accidental repeated shot or reused source range.
- `brand_consistency`: approved logo, colors, names, CTA, and tenant assets only.
- `cover_applied`: the approved cover is actually used in the released deliverable.
- `human_review`: a person reviewed the final rendered file, not only component files or preview frames.

Record gates with evidence:

```bash
python3 scripts/artifact_manifest.py gate \
  --manifest /absolute/project/path/video-production-manifest.json \
  --name picture_subtitle_audio_sync --status pass \
  --evidence 'QuickTime full playback, reviewer name, date'
```

Run `validate --release-ready` before delivery. A passing structural validation does not substitute for the human-review gate.

## Delivery contract

Return absolute paths for the manifest, selected scene clips, timing map or production script, cover variants, composite/release candidate, companion copy, and QA evidence. Report provider/attempt history, media metadata, unresolved issues, and whether the package is `generated`, `technically_verified`, or `accepted`.
