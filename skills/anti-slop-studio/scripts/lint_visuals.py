#!/usr/bin/env python3
"""Lint HTML, CSS, JS, JSX, SVG or storyboard text for AI design and motion tells.

Usage:
  python lint_visuals.py index.html
  python lint_visuals.py styles.css animation.js --with-copy
  python lint_visuals.py index.html --allow V03,M01 --format json

Rules V* are static design tells, M* are motion tells. Exit codes: 0 clean, 1 findings, 2 usage error.
Findings are cues, not verdicts: a deliberate choice stays. Suppress it with --allow ID, or put
"slop-ok: reason" on that line (comment in CSS, JS or HTML) and note it in the direction brief.
--with-copy also runs slop_scan.py on the visible text of HTML/JSX files.
"""
import argparse
import colorsys
import json
import os
import re
import sys

I = re.I
HEX = re.compile(r"#(?:[0-9a-f]{8}|[0-9a-f]{6}|[0-9a-f]{3})\b", I)
RGB = re.compile(r"rgba?\(\s*(\d{1,3})\s*[, ]\s*(\d{1,3})\s*[, ]\s*(\d{1,3})", I)
HSL = re.compile(r"hsla?\(\s*(\d{1,3}(?:\.\d+)?)(?:deg)?\s*[, ]\s*(\d{1,3}(?:\.\d+)?)%", I)
DEFAULT_FONTS = ("inter", "roboto", "open sans", "poppins", "montserrat", "geist", "lato")


def parse_color(tok):
    """Return (h 0-360, s 0-1, v 0-1) or None."""
    tok = tok.strip()
    if tok.startswith("#"):
        h = tok[1:]
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    else:
        m = RGB.match(tok)
        if not m:
            return None
        r, g, b = (min(int(x), 255) / 255 for x in m.groups())
    hh, ss, vv = colorsys.rgb_to_hsv(r, g, b)
    return hh * 360, ss, vv


def colors_in(s):
    out = []
    for m in HEX.finditer(s):
        c = parse_color(m.group(0))
        if c:
            out.append(c)
    for m in RGB.finditer(s):
        c = parse_color(m.group(0))
        if c:
            out.append(c)
    for m in HSL.finditer(s):
        h, sat = float(m.group(1)), float(m.group(2)) / 100
        out.append((h % 360, sat, 0.8))
    return out


def saturated(c, min_s=0.35):
    return c[1] >= min_s and 0.2 <= c[2]


def lint(text, path=""):
    lines = text.split("\n")
    findings = []

    def add(rid, label, line, snip, fix):
        if "slop-ok" in lines[line - 1].lower():
            return
        findings.append({"id": rid, "label": label, "line": line,
                         "text": re.sub(r"\s+", " ", snip).strip()[:90], "fix": fix, "file": path})

    all_colors = []
    anim_counts = {}
    infinite = []
    gray_borders = []
    glass = []
    eyebrow = []
    dash_lines = []

    for n, line in enumerate(lines, 1):
        low = line.lower()
        # V01 default font as primary family
        m = re.search(r"font-family\s*:\s*([^;}{]+)", line, I)
        if m:
            first = m.group(1).split(",")[0].strip().strip("'\"").lower()
            if first in DEFAULT_FONTS:
                add("V01", "template default font as primary", n, line,
                    "Choose a deliberate display plus body pairing for the direction.")
        # V02 purple/blue gradient
        if "gradient(" in low:
            cols = colors_in(line)
            if any(240 <= c[0] <= 300 and c[1] >= 0.35 for c in cols) and len(cols) >= 2:
                add("V02", "purple or indigo gradient", n, line,
                    "Commit to a palette from the direction brief; skip the stock gradient.")
        # V03 glow
        for sm in re.finditer(r"(?:box-shadow|text-shadow|drop-shadow)\s*[:(]([^;}]+)", line, I):
            val = sm.group(1)
            blurs = [int(x) for x in re.findall(r"(\d{2,3})px", val)]
            cols = colors_in(val)
            if blurs and max(blurs) >= 18 and any(saturated(c, 0.5) for c in cols):
                add("V03", "coloured glow", n, line,
                    "Use contrast, scale and a single accent instead of a neon halo.")
                break
        if re.search(r"filter\s*:\s*blur\(\s*(?:[6-9]\d|\d{3,})px", line, I):
            add("V03", "large blurred orb or glow layer", n, line,
                "Replace floating orbs with a real environment or a plain field.")
        # V04 coloured left strip on cards
        m = re.search(r"border-left\s*:\s*([3-6])px\s+solid\s+([^;}]+)", line, I)
        if m:
            cols = colors_in(m.group(2))
            if cols and saturated(cols[0], 0.3):
                add("V04", "coloured left-border strip", n, line,
                    "Reserve for real semantic state; separate cards with space or tone.")
        # V05 grey 1px borders (counted)
        for _ in re.finditer(r"(?<![\w-])border\s*:\s*1px\s+solid\s+(?:#(?:e|d|c|f)[0-9a-f]{2,5}\b|rgba\(\s*(?:0|255)\s*,\s*(?:0|255)\s*,\s*(?:0|255)\s*,\s*0?\.\d+)", line, I):
            gray_borders.append(n)
        # V06 pure black/white page background on body/html
        if re.search(r"(?:body|html)[^{]*\{[^}]*background(?:-color)?\s*:\s*(?:#000(?:000)?|#fff(?:fff)?|black|white)\b", line, I):
            add("V06", "pure black or white page background", n, line,
                "Tint the base slightly warm or cool so it has depth.")
        # V08 glassmorphism (counted)
        for _ in re.finditer(r"backdrop-filter\s*:\s*blur", line, I):
            glass.append(n)
        # V11 eyebrow label (counted)
        for _ in re.finditer(r"letter-spacing\s*:\s*0?\.(?:1[2-9]|2\d?|3\d?)em", line, I):
            eyebrow.append(n)
        # V10 emoji as icons in headings or buttons
        if re.search(r"<(?:h[1-4]|button)[^>]*>[^<]*[\U0001F300-\U0001FAFF]", line):
            add("V10", "emoji used as an icon", n, line, "Use one real icon set at one weight.")
        # V12 em dashes in markup copy
        if "\u2014" in line and re.search(r">[^<]*\u2014[^<]*<", line):
            dash_lines.append(n)
        # collect colors from style lines
        if re.search(r"color|background|fill|stroke|--[\w-]+\s*:", line, I):
            all_colors.extend(colors_in(line))
        # --- motion ---
        # M01 overshoot or bounce easing
        for cm in re.finditer(r"cubic-bezier\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)", line, I):
            y1, y2 = float(cm.group(2)), float(cm.group(4))
            if y1 < -0.05 or y1 > 1.05 or y2 < -0.05 or y2 > 1.05:
                add("M01", "overshoot easing", n, line,
                    "Use one easing family; overshoot only as a stated character choice.")
        if re.search(r"ease(?:In|Out|InOut)?(?:Back|Bounce|Elastic)|\b(?:bounce|elastic|wobble|rubber-?band)\b", line, I) \
                and not re.search(r"^\s*(?://|/\*|\*|#)", line):
            add("M01", "bounce or elastic easing", n, line,
                "Use one easing family; overshoot only as a stated character choice.")
        # M02 particles and randomness driving visuals
        if re.search(r"\b(?:particles?|confetti|sparkles?|shockwave|firefl(?:y|ies))\b|Math\.random\(", line, I) \
                and not re.search(r"^\s*(?://|/\*|\*)", line):
            add("M02", "particles or random motion", n, line,
                "Attach motion to a real element reacting to a real event.")
        # M03 same animation preset repeated (counted)
        for am in re.finditer(r"(?:animation|transition)\s*:\s*([^;}{]+)", line, I):
            key = re.sub(r"\s+", " ", am.group(1).strip().lower())
            anim_counts.setdefault(key, []).append(n)
            if "infinite" in key:
                infinite.append(n)
        # M04 stock fade-up preset names
        if re.search(r"\bfade-?in-?up\b|\banimate-fade|\bfadeInUp\b|\bAOS\.init\b|\bdata-aos\b", line, I):
            add("M04", "stock fade-up preset", n, line,
                "Stagger and direct entries by meaning, not one preset on everything.")
        # M05/M06 effect keywords
        if re.search(r"\b(?:glitch|rgb-?split|chromatic[- ]aberration|camera[- ]?shake|lens[- ]?flare|light[- ]?leak|grid[- ]floor|screen-?shake)\b", line, I) \
                and not re.search(r"^\s*(?://|/\*|\*)", line):
            add("M06", "stock energy effect", n, line, "Hold the frame and cut on the sound.")
        # M07 crossfade or dissolve between scenes
        if re.search(r"\bcross-?fade\b|\bcross-?dissolve\b|\bdissolve\b", line, I):
            add("M07", "crossfade or dissolve", n, line,
                "Grow each scene out of the previous one: match cut, shared shape, continuous move.")
        # M08 long micro-interaction durations
        for dm in re.finditer(r"transition\s*:[^;}]*?(\d+(?:\.\d+)?)(ms|s)\b", line, I):
            val = float(dm.group(1)) * (1000 if dm.group(2).lower() == "s" else 1)
            if val >= 1000:
                add("M08", "slow micro-interaction", n, line, "Keep UI-scale motion near 150 to 400 ms.")
                break

    if len(gray_borders) >= 4:
        add("V05", "grey 1px border on many containers", gray_borders[0],
            f"{len(gray_borders)} grey 1px borders",
            "Separate with whitespace, a tone shift, then soft elevation before adding a border.")
    if len(glass) >= 3:
        add("V08", "glassmorphism on many surfaces", glass[0], f"{len(glass)} backdrop blurs",
            "Use blur for one surface that needs it, not as a default skin.")
    if len(eyebrow) >= 2:
        add("V11", "tracked small-caps eyebrow labels", eyebrow[0], f"{len(eyebrow)} wide-tracked labels",
            "Drop the eyebrow-above-headline habit unless the hierarchy needs it.")
    if len(dash_lines) >= 3:
        add("V12", "em dashes in visible copy", dash_lines[0], f"{len(dash_lines)} lines with em dashes",
            "Rewrite the copy; run slop_scan.py.")
    for key, ns in anim_counts.items():
        if len(ns) >= 6 and key not in ("none", "0s"):
            add("M03", "same animation preset repeated", ns[0], f"{len(ns)}x: {key[:50]}",
                "Vary entries by role; one preset on everything is the template look.")
    if len(infinite) >= 3:
        add("M05", "many infinite float or pulse loops", infinite[0], f"{len(infinite)} infinite animations",
            "Looping ornaments distract; animate what carries meaning.")
    # V07 too many saturated hue families
    fam = {int(c[0] // 30) for c in all_colors if c[1] >= 0.3 and c[2] >= 0.35}
    if len(fam) > 4:
        add("V07", "more than three or four hue families", 1, f"{len(fam)} hue families in use",
            "Cap at three active hues plus neutrals; extend with tints and shades.")
    return sorted(findings, key=lambda f: (f["line"], f["id"]))


def visible_text(html):
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    text = re.sub(r"<[^>]+>", "\n", html)
    return re.sub(r"\n\s*\n+", "\n\n", text)



def _utf8():
    """Windows consoles default to a legacy code page; keep Hinglish and emoji printable."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def main(argv=None):
    _utf8()
    p = argparse.ArgumentParser(description="Lint design and motion code for AI tells.")
    p.add_argument("paths", nargs="+", help="files to lint")
    p.add_argument("--format", choices=["text", "json"], default="text")
    p.add_argument("--allow", default="", help="comma-separated rule IDs to ignore")
    p.add_argument("--with-copy", action="store_true", help="also scan visible text with slop_scan.py")
    a = p.parse_args(argv)
    allow = {x.strip().upper() for x in a.allow.split(",") if x.strip()}
    results, copy_results = [], []
    for path in a.paths:
        try:
            text = open(path, encoding="utf-8").read()
        except OSError as err:
            print(f"error: {err}", file=sys.stderr)
            return 2
        results.extend(f for f in lint(text, path) if f["id"] not in allow)
        if a.with_copy and path.lower().endswith((".html", ".htm", ".jsx", ".tsx", ".svg", ".md", ".txt")):
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import slop_scan
            body = visible_text(text) if path.lower().endswith((".html", ".htm", ".jsx", ".tsx", ".svg")) else text
            r = slop_scan.scan(body, allow)
            r["file"] = path
            r["verdict"] = slop_scan.verdict(r, 4.0)
            copy_results.append(r)
    if a.format == "json":
        print(json.dumps({"findings": results, "copy": copy_results}, ensure_ascii=False, indent=2))
    else:
        for f in results:
            print(f"{f['file']}:{f['line']} [{f['id']} {f['label']}] {f['text']}\n       -> {f['fix']}")
        for r in copy_results:
            print(f"\ncopy in {r['file']}: {r['words']} words, score {r['score']}, verdict {r['verdict']}")
            for f in r["findings"][:8]:
                print(f"  [{f['id']} {f['label']}] {f['text']}")
        print(f"\n{len(results)} design/motion finding(s)." + (" Run the taste pass on the rendered result." if results else ""))
    bad_copy = any(r["verdict"] == "slop" for r in copy_results)
    return 1 if results or bad_copy else 0


if __name__ == "__main__":
    sys.exit(main())
