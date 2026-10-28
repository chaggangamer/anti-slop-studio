#!/usr/bin/env python3
"""Check delivered audio: integrated loudness, true peak, loudness range, long silences.

Usage:
  python check_audio.py final.mp4
  python check_audio.py final.mp4 --target -14 --tolerance 1.5 --max-peak -1.0

Needs ffmpeg on PATH (uses the ebur128 and silencedetect filters). Exit codes: 0 pass, 1 findings,
2 usage or environment error. A passing number is not a good mix: listen as well.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys


def run_ffmpeg(args):
    proc = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *args],
                          capture_output=True, text=True)
    return proc.returncode, proc.stderr


def analyse(path):
    rc, err = run_ffmpeg(["-i", path, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"])
    if re.search(r"Stream .*Audio", err) is None:
        return {"has_audio": False}
    summary = err.rsplit("Summary:", 1)[-1]
    def grab(label):
        m = re.search(label + r":?\s+(-?\d+(?:\.\d+)?)\s*(?:LUFS|LU|dBFS)", summary)
        return float(m.group(1)) if m else None
    lufs = grab(r"I")
    lra = grab(r"LRA")
    pm = re.search(r"True peak:\s*\n?\s*Peak:\s+(-?\d+(?:\.\d+)?)\s*dBFS", summary)
    peak = float(pm.group(1)) if pm else None
    rc2, err2 = run_ffmpeg(["-i", path, "-vn", "-af", "silencedetect=noise=-50dB:d=1.5", "-f", "null", "-"])
    dur = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", err2)
    total = int(dur.group(1)) * 3600 + int(dur.group(2)) * 60 + float(dur.group(3)) if dur else None
    starts = [float(x) for x in re.findall(r"silence_start:\s*(-?\d+(?:\.\d+)?)", err2)]
    ends = re.findall(r"silence_end:\s*(\d+(?:\.\d+)?)\s*\|\s*silence_duration:\s*(\d+(?:\.\d+)?)", err2)
    silences = []
    for i, st in enumerate(starts):
        d = float(ends[i][1]) if i < len(ends) else (total - st if total else 0)
        silences.append({"start": round(max(st, 0), 2), "duration": round(d, 2)})
    return {"has_audio": True, "integrated_lufs": lufs, "loudness_range": lra,
            "true_peak_dbfs": peak, "duration": total, "silences": silences}


def evaluate(info, target, tol, max_peak):
    f = []
    if not info["has_audio"]:
        return [("A01", "no audio stream", "The file has no audio. A silent delivery is a draft, not a finish.")]
    lufs = info["integrated_lufs"]
    if lufs is None:
        f.append(("A02", "loudness unreadable", "Could not measure integrated loudness; check the file."))
    elif lufs < target - tol:
        f.append(("A03", "too quiet", f"{lufs:.1f} LUFS vs target {target:g} (+/-{tol:g}). Raise the mix and recheck peaks."))
    elif lufs > target + tol:
        f.append(("A04", "too loud", f"{lufs:.1f} LUFS vs target {target:g} (+/-{tol:g}). Platforms will turn it down; ease the limiter."))
    pk = info["true_peak_dbfs"]
    if pk is not None and pk > max_peak:
        f.append(("A05", "true peak too high", f"{pk:.1f} dBTP above {max_peak:g}. Lower the ceiling to avoid encoding clipping."))
    total = info.get("duration") or 0
    for s in info["silences"]:
        at_head = s["start"] <= 0.05
        at_tail = total and s["start"] + s["duration"] >= total - 0.05
        where = "at the start" if at_head else "at the end" if at_tail else "mid-piece"
        f.append(("A06", "long silence", f"{s['duration']:.1f}s of near-silence {where} (from {s['start']:.1f}s). Keep only if chosen."))
    return f



def _utf8():
    """Windows consoles default to a legacy code page; keep Hinglish and emoji printable."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def main(argv=None):
    _utf8()
    p = argparse.ArgumentParser(description="Check loudness, peaks and dead air.")
    p.add_argument("path", help="audio or video file")
    p.add_argument("--target", type=float, default=-14.0, help="integrated loudness target in LUFS (default -14)")
    p.add_argument("--tolerance", type=float, default=1.5, help="allowed deviation in LU (default 1.5)")
    p.add_argument("--max-peak", type=float, default=-1.0, help="maximum true peak in dBTP (default -1.0)")
    p.add_argument("--json", action="store_true", help="print JSON")
    a = p.parse_args(argv)
    if shutil.which("ffmpeg") is None:
        print("error: ffmpeg not found on PATH", file=sys.stderr)
        return 2
    try:
        open(a.path, "rb").close()
    except OSError as err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    info = analyse(a.path)
    findings = evaluate(info, a.target, a.tolerance, a.max_peak)
    if a.json:
        print(json.dumps({"info": info, "findings": [{"id": i, "label": l, "detail": d} for i, l, d in findings]}, indent=2))
    else:
        if info["has_audio"]:
            print(f"integrated {info['integrated_lufs']} LUFS | range {info['loudness_range']} LU | true peak {info['true_peak_dbfs']} dBTP")
        for i, l, d in findings:
            print(f"[{i} {l}] {d}")
        print(f"\n{len(findings)} finding(s)." + ("" if findings else " Numbers pass; now listen on a phone speaker and headphones."))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
