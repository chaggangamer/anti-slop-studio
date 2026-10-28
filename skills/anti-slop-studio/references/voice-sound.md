# Voice and sound

Contents: voiceover direction, music, effects, ambience, mix, verification.

Sound carries half the picture. Audible, intentional sound is also what separates a finished piece from a silent draft; many rejected edits fail on audio alone.

## Voiceover direction

Write down, before generating or recording:

- Voice type and age, warmth versus authority versus dryness, and why it fits the idea.
- Which word in each line carries the stress, and where the breath and pauses go.
- Pace relative to the picture; the line should land as the image does, not before.
- Pronunciation of brand, person, place and technical names, spelled phonetically where the engine needs it. For Hindi and Hinglish scripts see `references/hinglish.md`.
- Consistency across regenerated lines (same voice settings, same room feel).

Tells: uniform emphasis, identical pause length after every sentence, a "smiling" read on every line, no breath, and a voice that never changes energy between setup and payoff. Read the script aloud first and rewrite lines that are hard to say.

## Music

- Choose music for its role (pulse, tension, warmth, contrast), not as wallpaper.
- Edit the music to the picture: sync cuts and key reveals to audible beats, but do not cut on every beat. A hit that lands once at the turn is stronger than a hit on every cut.
- Use only music you have the rights to. Record the source and licence for every track.
- Leave space: arrangement that drops out under the voice or before the payoff is part of the design.

## Effects and ambience

- Every effect supports an action on screen. A default whoosh on every cut is the audio equivalent of a crossfade.
- Layer a few distinct sounds for the important moments instead of one big generic hit.
- Add subtle ambience or room tone so unrelated shots seem to live in one world. Silence is a tool when it is chosen; dead air is not.
- Make synthesised effects specific to the object. Vary pitch and timing so repeats do not machine-gun.

## Mix guidelines

- Loudness target for social and web delivery is commonly around -14 LUFS integrated; confirm the platform's current guidance. Keep true peak at or below about -1 dBTP so encoding does not clip.
- Voice sits clearly above music; music dips under speech rather than fighting it.
- Check on phone speakers and on headphones. The piece has to be audible, not only technically present.
- Remove inconsistent room tone and synthetic artefacts between lines. Match level and tone across generated and recorded lines.
- Normalise once at the end; do not stack limiters through the chain.

## Verification

```bash
python scripts/check_audio.py final.mp4 --target -14
```

It reports integrated loudness, loudness range, true peak, long silences, and a missing audio stream, and returns exit code 1 when a check fails. Listen as well; a clean number can still be a dull mix.
