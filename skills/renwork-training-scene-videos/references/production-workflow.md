# Scene-by-scene production workflow

Use this reference when planning prompts, resuming interrupted generation, composing clips, or reviewing a final RenWork training video.

## 1. Scene contract

Define every scene before making provider calls:

| Field | Required decision |
|---|---|
| `scene_id` | Stable order and slug; do not reuse it for a different idea |
| `purpose` | The single business/training point the scene proves |
| `setting` | Concrete place, time, and environmental cues |
| `people_and_action` | Who is present and what visibly happens |
| `brand_cues` | Approved logo placement, colors, signage, clothing, or UI |
| `narration` | Spoken line mapped to this scene |
| `caption` | On-screen copy; shorter than narration when readability requires |
| `duration` | Target range and minimum usable hold time |
| `continuity` | Camera direction, wardrobe, lighting, and transition relationship |
| `references` | Exact local files or approved source URLs |
| `prohibited` | Unsupported claims, wrong logos, malformed UI/text, unsafe visuals |

Scene concepts observed in the originating workflow included a hands-on classroom, one-to-one diagnosis, overseas-buyer war room, exhibition lead desk, and live public class. They are examples, not a mandatory five-scene template.

## 2. Prompt structure

Write one prompt per scene. Keep it concrete:

```text
Purpose: <what this shot must communicate>
Setting: <specific physical environment>
People/action: <observable action, not abstract benefits>
Brand: <approved RenWork cues and logo treatment>
Camera/motion: <shot size, movement, pace>
Continuity: <relationship to previous/next scene>
Duration/aspect: <target seconds and ratio>
References: <attached files and what to borrow from each>
Avoid: <wrong text, extra logos, fabricated interfaces, frozen poses, artifacts>
```

Do not ask the model to render long paragraphs or precise software UI unless the selected model reliably supports it. Add exact titles, subtitles, badges, and progress bars during deterministic composition.

## 3. Provider-round continuation

Some providers or host applications may allow only one generated video in a round. Treat this as a resumable queue:

1. Scan the manifest.
2. Select the lowest-order scene not at `generated` or later.
3. Submit only that scene's prompt and references.
4. On success, save the file under its stable expected path and run `scan`.
5. Record the attempt and review result.
6. Start a new provider round for the next pending scene.

Never use a generic “continue” without checking the manifest first. The continuation message should name the next scene ID/title so the provider cannot regenerate or skip a scene.

If a provider reports quota exhaustion before returning a usable file, record the scene as `blocked`, preserve completed files, and stop or route to an explicitly approved alternative provider. Do not claim a scene exists from a progress message alone.

## 4. Per-scene review

Technical review:

- file exists and `ffprobe` parses it;
- expected video stream, dimensions, frame rate, and duration are present;
- no zero-byte, partial-download, or cloud-placeholder file;
- playback reaches the last frame without decode failure.

Content review:

- people, actions, and environment match the scene contract;
- brand cues are correct and no foreign tenant assets appear;
- motion is usable and does not freeze, warp, or jump unexpectedly;
- shot is distinct from accepted footage for other scenes;
- the visual can support its assigned narration and caption.

Mark `accepted` only after both reviews. Keep rejected attempts in attempt history; do not delete provenance needed to explain the selection.

## 5. Composition and synchronization

Create a timing map with one row per spoken line:

| start | end | scene/source range | narration | subtitle | transition |
|---:|---:|---|---|---|---|

Derive start/end from the final voice track or approved recording. Then map visuals to the resulting intervals. For every row, ask: “If audio were muted, would the picture still support this line?”

Apply subtitles, logo, scene badges, and progress indicators inside title-safe areas. Transitions must not hide the visual evidence needed by the narration. Check the first frame for black or stale content and the ending for accidental audio-only tail.

If review finds mismatch:

1. Identify the exact interval and whether the defect is source selection, timing, subtitle copy, voice line, or transition.
2. Correct the timing/source map.
3. Rerender a new version without overwriting the prior candidate.
4. Replay the changed interval plus its boundaries, then perform a complete final playback.

## 6. Cover and channel package

Track cover files separately by ratio, for example 16:9 and 1:1. Verify that the chosen cover is actually encoded as the opening frame/segment or applied by the target publishing workflow. A cover asset beside the MP4 does not satisfy `cover_applied`.

Companion copy must match the accepted film's facts, CTA, company identity, channel, and duration. Copy generation is not permission to publish.

## 7. Delivery package

Expected categories:

- `video-production-manifest.json`;
- approved scene clips;
- narration/audio and timing map or deterministic production script;
- cover variants;
- versioned composite and final release candidate;
- channel copy;
- technical probe results and human-review evidence.

Deliver only after `artifact_manifest.py validate --release-ready` passes, or label the package accurately with the remaining failed/pending gates.
