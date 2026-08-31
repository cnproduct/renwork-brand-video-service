# Artifact manifest contract

`video-production-manifest.json` is the resumable source of truth for a scene-video project. Keep it inside the project root. Use `scripts/artifact_manifest.py` to create and mutate it so updates remain atomic and auditable.

## Core records

- `project`: project ID, absolute root, brand profile, brief source, channel, ratio, target duration, and timestamps.
- `scenes`: stable scene ID/order/slug/title, expected path, current state, selected artifact, and attempt history.
- `artifacts`: relative path, role, byte size, modification time, SHA-256, and media metadata when `ffprobe` is available.
- `stages`: coarse progress for planning, scene generation, composition, cover, copy, and technical validation.
- `acceptance_gates`: status, evidence, reviewer, note, and timestamp for final release decisions.
- `history`: machine-written state changes. Do not remove earlier failed attempts merely to make a project look complete.

## State semantics

Scene states:

- `planned`: contract exists but prompt has not been sent.
- `prompted`: request was submitted; no confirmed generation is running.
- `generating`: provider visibly accepted the job.
- `generated`: a non-empty local artifact exists.
- `technically_verified`: artifact parses and plays; content may still be wrong.
- `needs_revision`: review found a correctable defect.
- `accepted`: scene passed technical and content review.
- `blocked`: progress needs a quota reset, credential, permission, missing input, or provider change.

Gate states are `pending`, `pass`, `fail`, or `waived`. A waiver must identify the reviewer and rationale. `human_review` should not be waived for a user-facing final film.

## Artifact roles

The scanner classifies conventional names into `scene_video`, `composite_video`, `final_video`, `cover`, `channel_copy`, `audio`, `production_script`, or `other`. Naming helps discovery but does not prove semantic correctness.

Stable scene names should use:

```text
scene<order>_<slug>.mp4
```

Version final outputs instead of overwriting an accepted file, for example:

```text
renwork_training_v01_composite.mp4
renwork_training_v02_syncfix.mp4
renwork_training_v03_accepted.mp4
```

## Useful commands

Record a generation/review outcome:

```bash
python3 scripts/artifact_manifest.py set-scene \
  --manifest /absolute/project/video-production-manifest.json \
  --scene-id scene1 --status generated \
  --artifact scene1_training_classroom.mp4 \
  --attempt-status succeeded --provider seedance \
  --note 'Downloaded from provider round 1'
```

Mark a rejected attempt:

```bash
python3 scripts/artifact_manifest.py set-scene \
  --manifest /absolute/project/video-production-manifest.json \
  --scene-id scene1 --status needs_revision \
  --attempt-status rejected --provider seedance \
  --note 'Logo malformed and action does not match narration'
```

Rescan after moving or generating files:

```bash
python3 scripts/artifact_manifest.py scan --manifest /absolute/project/video-production-manifest.json
```

Structural validation:

```bash
python3 scripts/artifact_manifest.py validate --manifest /absolute/project/video-production-manifest.json
```

Release validation additionally requires all scenes accepted, a final video, a cover, and all acceptance gates passed:

```bash
python3 scripts/artifact_manifest.py validate \
  --manifest /absolute/project/video-production-manifest.json \
  --release-ready
```

The scanner can discover additional layouts with repeatable `--glob` arguments. Globs are evaluated below the project root and must not escape it.
