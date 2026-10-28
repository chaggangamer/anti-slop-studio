# Before and after

Real output from the bundled scripts on small fictional examples; the files are in `examples/files/`. A clean scan does not make a piece good: it shows that the known tells are gone. The rewrites illustrate the method (delete first, state the true half, add one real detail). Their numbers and details are invented.


## English ad copy

The before text has an opener, a straw-man contrast and a buzzword pile. A triad or an exclamation mark on its own is normal writing, so the scanner only counts clusters of those. The after text drops all of it and says what happens.

**Before**

> In today's fast-paced world, finding the perfect bakery can feel overwhelming. That's where we come in. We're not just a bakery, we're a community, seamlessly blending tradition and innovation to elevate every celebration. Whether you're planning a birthday, a wedding, or a corporate event, our robust range of handcrafted cakes will unlock the joy of every occasion. Experience the difference today!

```text
$ python skills/anti-slop-studio/scripts/slop_scan.py examples/files/ad_before.md
L1    [S01 contrast framing] come in. We're not just a bakery, we're a community, seamlessly blending tradition and innovat
       -> State the true half directly, or join: 'faster and cheaper'.
L1    [S02 throat-clearing opener] In today's fast-paced world, finding the perfect bakery can feel overwhelming. Tha
       -> Delete; start at the first sentence that carries information.
L1    [S10 buzzword cluster] elevate, robust, seamlessly
       -> Use plain verbs and nouns; judge clusters, not single words.

61 words (English) | score 11.48 per 100 words | verdict: slop
Delete first, then rewrite. A clean scan is not proof of quality: run the taste pass.
(exit code 1)
```

**After**

> Order by 9 p.m. and pick up by 8 a.m. Birthday cakes start at one kilo. Wedding cakes need five days. Last Saturday the oven ran from 4 a.m. and the lemon cake was gone by noon.

```text
$ python skills/anti-slop-studio/scripts/slop_scan.py examples/files/ad_after.md
40 words (English) | score 0.0 per 100 words | verdict: clean
(exit code 0)
```


## Hinglish copy

A translated hook and stock superlatives, replaced by something a person would say aloud.

**Before**

> Kya aap jaante hain ki hamari quality ka dusra naam hai bharosa? Hum hain sabse best. Aaj hi sampark karein!

```text
$ python skills/anti-slop-studio/scripts/slop_scan.py examples/files/hinglish_before.md --hinglish
L1    [H01 translated CTA] in sabse best. Aaj hi sampark karein!
       -> Write what a person would say aloud.
L1    [H03 stock superlative] hain ki hamari quality ka dusra naam hai bharosa? Hum hain sabse best. Aaj hi sampark karei
       -> Replace with a proof point.
L1    [H03 stock superlative] rosa? Hum hain sabse best. Aaj hi sampark karein!
       -> Replace with a proof point.
L1    [H04 translated English hook] Kya aap jaante hain ki hamari quality ka dusra naam hai bharosa? Hum hain
       -> Open with the situation or the tension, not a translated hook.

20 words (Hinglish+English) | score 30.0 per 100 words | verdict: slop
Delete first, then rewrite. A clean scan is not proof of quality: run the taste pass.
(exit code 1)
```

**After**

> Kal subah 9 baje tak order karo. Shaam ko cake tumhare darwaze par. Der hui to paisa wapas.

```text
$ python skills/anti-slop-studio/scripts/slop_scan.py examples/files/hinglish_after.md --hinglish
18 words (Hinglish+English) | score 0.0 per 100 words | verdict: clean
(exit code 0)
```


## UI code

Template defaults (stock font, purple gradient, neon glow, bounce easing, particles) against a deliberate palette and a single easing curve.

**Before**

```text
$ python skills/anti-slop-studio/scripts/lint_visuals.py examples/files/ui_before.html --with-copy
examples/files/ui_before.html:2 [V01 template default font as primary] body { background: #000; font-family: 'Inter', sans-serif; }
       -> Choose a deliberate display plus body pairing for the direction.
examples/files/ui_before.html:2 [V06 pure black or white page background] body { background: #000; font-family: 'Inter', sans-serif; }
       -> Tint the base slightly warm or cool so it has depth.
examples/files/ui_before.html:3 [V02 purple or indigo gradient] .hero { background: linear-gradient(135deg, #6d28d9, #3b82f6); }
       -> Commit to a palette from the direction brief; skip the stock gradient.
examples/files/ui_before.html:4 [M01 overshoot easing] .card { border: 1px solid #e5e7eb; border-left: 4px solid #8b5cf6; box-shadow: 0 0 40px rg
       -> Use one easing family; overshoot only as a stated character choice.
examples/files/ui_before.html:4 [M08 slow micro-interaction] .card { border: 1px solid #e5e7eb; border-left: 4px solid #8b5cf6; box-shadow: 0 0 40px rg
       -> Keep UI-scale motion near 150 to 400 ms.
examples/files/ui_before.html:4 [V03 coloured glow] .card { border: 1px solid #e5e7eb; border-left: 4px solid #8b5cf6; box-shadow: 0 0 40px rg
       -> Use contrast, scale and a single accent instead of a neon halo.
examples/files/ui_before.html:4 [V04 coloured left-border strip] .card { border: 1px solid #e5e7eb; border-left: 4px solid #8b5cf6; box-shadow: 0 0 40px rg
       -> Reserve for real semantic state; separate cards with space or tone.
examples/files/ui_before.html:4 [V05 grey 1px border on many containers] 4 grey 1px borders
       -> Separate with whitespace, a tone shift, then soft elevation before adding a border.
examples/files/ui_before.html:6 [V11 tracked small-caps eyebrow labels] 2 wide-tracked labels
       -> Drop the eyebrow-above-headline habit unless the hierarchy needs it.
examples/files/ui_before.html:7 [M03 same animation preset repeated] 6x: fadeinup .6s ease-out
       -> Vary entries by role; one preset on everything is the template look.
examples/files/ui_before.html:7 [M04 stock fade-up preset] .a { animation: fadeInUp .6s ease-out; } .b { animation: fadeInUp .6s ease-out; } .c { ani
       -> Stagger and direct entries by meaning, not one preset on everything.
examples/files/ui_before.html:8 [M04 stock fade-up preset] .d { animation: fadeInUp .6s ease-out; } .e { animation: fadeInUp .6s ease-out; } .f { ani
       -> Stagger and direct entries by meaning, not one preset on everything.
examples/files/ui_before.html:9 [V03 large blurred orb or glow layer] .orb { filter: blur(120px); }
       -> Replace floating orbs with a real environment or a plain field.
examples/files/ui_before.html:11 [V10 emoji used as an icon] <h1>🚀 It's not just a tool — it's a teammate</h1>
       -> Use one real icon set at one weight.
examples/files/ui_before.html:13 [M02 particles or random motion] <script>const x = Math.random(); particles.init();</script>
       -> Attach motion to a real element reacting to a real event.

copy in examples/files/ui_before.html: 19 words, score 31.58, verdict slop
  [S01 contrast framing] 🚀 It's not just a tool — it's a teammate We seamlessly leverage robust, cutting-edg
  [S10 buzzword cluster] cutting-edge, elevate, leverage, robust, seamlessly

15 design/motion finding(s). Run the taste pass on the rendered result.
(exit code 1)
```

**After**

```text
$ python skills/anti-slop-studio/scripts/lint_visuals.py examples/files/ui_after.html --with-copy
copy in examples/files/ui_after.html: 16 words, score 0.0, verdict clean

0 design/motion finding(s).
(exit code 0)
```


## Edit rhythm

Every shot two seconds, every transition a crossfade, and a nine-word line on screen for two seconds, against a plan with varied lengths and transitions.

**Before**

```text
$ python skills/anti-slop-studio/scripts/check_shots.py examples/files/shots_before.json --format reel
[E04 slow open] first shot lasts 5.0s (limit 3.0s for reel)
       -> Start in the middle of something already moving or in tension.
[E05 one transition for everything] all 6 transitions are 'crossfade'
       -> Choose a grammar and break it once, deliberately, at the turn.
[E06 crossfade share] 6 of 6 transitions are fades or dissolves
       -> Grow scenes out of each other: match cut, shared shape, continuous move.
[E07 same shot size repeated] 5 shots in a row share one size
       -> Vary shot size to direct the eye.

7 shots, 17.0s total, average 2.43s | 4 finding(s)
(exit code 1)
```

**After**

```text
$ python skills/anti-slop-studio/scripts/check_shots.py examples/files/shots_after.json --format reel
6 shots, 15.0s total, average 2.5s | 0 finding(s)
(exit code 0)
```
