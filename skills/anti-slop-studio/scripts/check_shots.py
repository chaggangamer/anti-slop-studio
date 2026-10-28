#!/usr/bin/env python3
"""Check an edit plan for rhythm and readability tells.

Usage:
  python check_shots.py shots.json --format reel
  python check_shots.py shots.csv --format film --target 30

Input: JSON {"shots": [...]} or a bare list, or CSV with a header. Each shot may have:
  duration (seconds, required), transition, size, text, id.
Checks: metronome edit, one-transition-for-everything, crossfade share, slow open, text that outruns
reading time, same shot size repeated, frantic or sluggish average shot length, total vs target.
Exit codes: 0 clean, 1 findings, 2 usage error. Findings are cues for a human eye.
"""
import argparse
import csv
import json
import re
import statistics
import sys

FORMATS = {
    # avg shot seconds (min, max), slow-open threshold seconds
    "reel": {"avg": (0.7, 4.5), "open": 3.0},
    "trailer": {"avg": (0.8, 5.0), "open": 4.0},
    "film": {"avg": (1.5, 12.0), "open": 8.0},
}


def load(path):
    if path.lower().endswith(".csv"):
        with open(path, encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
        return {"shots": rows}
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return data if isinstance(data, dict) else {"shots": data}


def words_in(text):
    return len(re.findall(r"[\w\u0900-\u097F'’-]+", text or ""))


def check(data, fmt="reel", target=None, sec_per_word=0.25, settle=0.25):
    spec = FORMATS[fmt]
    shots = data.get("shots", [])
    findings = []

    def add(rid, label, detail, fix):
        findings.append({"id": rid, "label": label, "detail": detail, "fix": fix})

    durs = []
    for i, s in enumerate(shots, 1):
        try:
            durs.append(float(s.get("duration")))
        except (TypeError, ValueError):
            raise ValueError(f"shot {i} has no numeric duration")
    if not durs:
        raise ValueError("no shots found")
    total = sum(durs)
    avg = total / len(durs)

    if len(durs) >= 5:
        cv = statistics.pstdev(durs) / avg if avg else 0
        if cv < 0.2:
            add("E01", "metronome edit", f"{len(durs)} shots, lengths vary only {cv:.0%}",
                "Let some shots breathe and some snap; hold longest on the line that matters.")
    lo, hi = spec["avg"]
    if avg < lo:
        add("E02", "frantic average shot length", f"average {avg:.2f}s for {fmt}",
            "Fewer, longer shots; not every beat needs a cut.")
    if avg > hi:
        add("E03", "sluggish average shot length", f"average {avg:.2f}s for {fmt}",
            "Tighten; cut earlier or give held shots a purpose.")
    if durs[0] > spec["open"]:
        add("E04", "slow open", f"first shot lasts {durs[0]:.1f}s (limit {spec['open']}s for {fmt})",
            "Start in the middle of something already moving or in tension.")

    trans = [str(s.get("transition", "")).strip().lower() for s in shots[1:] if s.get("transition")]
    if len(trans) >= 6 and len(set(trans)) == 1:
        add("E05", "one transition for everything", f"all {len(trans)} transitions are '{trans[0]}'",
            "Choose a grammar and break it once, deliberately, at the turn.")
    fades = [t for t in trans if re.search(r"fade|dissolve", t)]
    if trans and len(fades) / len(trans) > 0.25 and len(fades) >= 2:
        add("E06", "crossfade share", f"{len(fades)} of {len(trans)} transitions are fades or dissolves",
            "Grow scenes out of each other: match cut, shared shape, continuous move.")

    sizes = [str(s.get("size", "")).strip().lower() for s in shots]
    run = best = 1
    for a, b in zip(sizes, sizes[1:]):
        run = run + 1 if a and a == b else 1
        best = max(best, run)
    if best >= 4:
        add("E07", "same shot size repeated", f"{best} shots in a row share one size",
            "Vary shot size to direct the eye.")

    for i, s in enumerate(shots, 1):
        w = words_in(s.get("text", ""))
        if w:
            need = w * sec_per_word + settle
            if durs[i - 1] + 1e-9 < need:
                add("E08", "text outruns reading time",
                    f"shot {s.get('id', i)}: {w} word(s) in {durs[i - 1]:.2f}s, needs about {need:.2f}s",
                    "Lengthen the shot, cut words, or split across shots.")

    if target is not None and abs(total - target) > max(0.5, target * 0.05):
        add("E09", "length off target", f"total {total:.1f}s vs target {target:g}s",
            "Trim or extend to the delivery length.")
    return {"shots": len(durs), "total_seconds": round(total, 2), "average_seconds": round(avg, 2),
            "findings": findings}



def _utf8():
    """Windows consoles default to a legacy code page; keep Hinglish and emoji printable."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def main(argv=None):
    _utf8()
    p = argparse.ArgumentParser(description="Check shot rhythm and text readability.")
    p.add_argument("path", help="shots.json or shots.csv")
    p.add_argument("--format", choices=sorted(FORMATS), default="reel")
    p.add_argument("--target", type=float, help="target total length in seconds")
    p.add_argument("--sec-per-word", type=float, default=0.25, help="reading time per word (default 0.25)")
    p.add_argument("--allow", default="", help="comma-separated rule IDs to ignore")
    p.add_argument("--json", action="store_true", help="print JSON")
    a = p.parse_args(argv)
    try:
        data = load(a.path)
        target = a.target if a.target is not None else data.get("target_seconds")
        result = check(data, a.format, target, a.sec_per_word)
    except (OSError, ValueError, json.JSONDecodeError) as err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    allow = {x.strip().upper() for x in a.allow.split(",") if x.strip()}
    result["findings"] = [f for f in result["findings"] if f["id"] not in allow]
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for f in result["findings"]:
            print(f"[{f['id']} {f['label']}] {f['detail']}\n       -> {f['fix']}")
        print(f"\n{result['shots']} shots, {result['total_seconds']}s total, average {result['average_seconds']}s | "
              f"{len(result['findings'])} finding(s)")
    return 1 if result["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
