# Visual design and imagery

Contents: root cause, commit to a direction, rules, imagery tells, generated text and logos, thumbnails, verification.

## Root cause

AI design converges on the average of millions of templates, so unexamined output shares one fingerprint: warm or purple-blue gradients, glowing dark sections, a grey-bordered card for everything, a centred hero with a badge above the headline, three feature cards in a row, a default sans headline. None of these is bad alone. Together, with no decision behind them, they read as machine-made.

Written taste guidance is weak ("be distinctive" often adds more). What works is a locked direction plus mechanical checks plus a human eye on the rendered result.

## Commit to a direction

Pick one named direction (editorial, brutalist, industrial-mono, organic, quiet-product, paper-craft, kinetic-type, and so on) and lock its tokens in the brief: palette, type pairing, radius, texture, spacing scale, motion. Hold them everywhere. "Clean and modern" is the default, not a direction.

## Rules

1. **Palette:** one dominant hue, one neutral, one sharp accent. At most three active hues; extend with tints and shades, not new hues. Tint blacks and whites slightly so they have depth.
2. **Type:** a deliberate display plus body pairing chosen for the tone. Avoid the template defaults (Inter, Roboto, Open Sans, Poppins, Montserrat, Geist) as the headline voice. Use weight and size for hierarchy rather than more families. One mathematical type scale, body at 16 px or larger on screen.
3. **Cards and containers:** separate with whitespace first, then a small background shift, then soft elevation. Add a border only if those fail, and avoid a flat grey line on everything. Keep coloured left strips for real semantic state.
4. **Spacing:** one scale (multiples of 8 with 4 as a half-step). Space inside a component is smaller than space between components, which is smaller than space between sections. Vary section rhythm down the page.
5. **Contrast:** measure it (APCA or WCAG) rather than eyeballing, especially on dark themes and thin type.
6. **Dark mode:** a deliberate choice for the product, not a reflex. Glow, neon borders and floating gradient orbs are the strongest dark-mode tells.
7. **Layout:** one focal point and one accent per screen. Break the three-equal-cards habit with a lead item and supporting items.
8. **States:** design hover, focus, active, disabled, loading, empty and error, not only the resting state.
9. **Icons:** one icon set at one weight. Do not draw icons or illustrations from scratch in code; use a real pack or real assets.

## Imagery tells (generated images and footage frames)

| Tell | Cause | Fix |
|---|---|---|
| Plastic, waxy skin | Model smoothing | Specify texture, real lens, natural light, then retouch |
| Dead-centre subject, perfect symmetry | Model comfort zone | Off-centre framing, negative space, let parts fall into shadow |
| Everything evenly lit | "Everything is the hero" lighting | Directional light with a clear key and real shadow |
| Generic stock subjects ("diverse team at a laptop") | Generic prompt | Specific person, place, lens and moment |
| Smeared text, odd hands, drifting detail | Unreviewed generation | Review at full zoom, regenerate or repair |
| Different look in every shot | No style anchor | Reference-condition on one locked look |

## Generated text, logos and interface

Never ship generated text for anything that must be correct: logos, labels, UI, charts, packaging, prices, legal lines, calls to action. Rebuild them as real typography, vector logos and real data. Use generated imagery for mood and scenario, and real or approved material for evidence.

## Thumbnails and posters

One subject, one short line, high contrast, readable at phone-feed size. Test at the smallest size it will appear. Avoid stacking a glow, a gradient, a stroke and a drop shadow on the same text.

## Verification

- Run `scripts/lint_visuals.py` on any HTML, CSS, JSX or SVG you built.
- Render the page or frame and look at the picture, not the code. You ship what renders.
- Squint test: shrink to thumbnail. If every section looks like the same box, it is monotonous, not consistent.
- Compare two builds from the same brief side by side; the shared fingerprint only shows up in pairs.
