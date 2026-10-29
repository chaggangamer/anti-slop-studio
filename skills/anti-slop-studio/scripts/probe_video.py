#!/usr/bin/env python3
"""Probe a finished video: size, fps, duration, cut times, cuts per 10 s, optional contact sheet.

Usage:
  python probe_video.py final.mp4
  python probe_video.py final.mp4 --contact-sheet sheet.jpg --every 1 --cols 6
  python probe_video.py final.mp4 --shots-out shots.json   # feed to check_shots.py
  python probe_video.py reference.mp4 --threshold 0.35 --json

Needs ffmpeg and ffprobe on PATH. Cuts come from ffmpeg scene detection, so slow dissolves and
motion-heavy shots can be missed or over-counted: treat numbers as a guide and look at the sheet.
Exit codes: 0 ok, 2 usage or environment error.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys


def _utf8():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, p.stdout, p.stderr


def probe(path):
    rc, out, err = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path])
    if rc != 0:
        raise RuntimeError(err.strip() or "ffprobe failed")
    data = json.loads(out)
    vid = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    aud = next((s for s in data.get("streams", []) if s.get("codec_type") == "audio"), None)
    if vid is None:
        raise RuntimeError("no video stream found")
    num, _, den = (vid.get("avg_frame_rate") or "0/1").partition("/")
    fps = float(num) / float(den) if den and float(den) else 0.0
    duration = float(data.get("format", {}).get("duration") or vid.get("duration") or 0)
    return {"width": vid.get("width"), "height": vid.get("height"), "fps": round(fps, 2),
            "duration": round(duration, 2), "has_audio": aud is not None}


def detect_cuts(path, threshold):
    rc, out, err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-an",
                        "-vf", f"select='gt(scene,{threshold})',showinfo", "-f", "null", "-"])
    return sorted({round(float(t), 3) for t in re.findall(r"pts_time:(\d+(?:\.\d+)?)", err)})


def contact_sheet(path, out_path, every, cols, width):
    rc, out, err = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    try:
        dur = float(out.strip())
    except ValueError:
        dur = 0.0
    frames = max(int(dur / every) + 1, 1)
    rows = (frames + cols - 1) // cols
    vf = f"fps=1/{every},scale={width}:-1,drawtext=text='%{{pts\\:hms}}':x=6:y=h-th-6:fontcolor=white:box=1:boxcolor=black@0.5:fontsize=14,tile={cols}x{rows}"
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", path, "-vf", vf, "-frames:v", "1", out_path]
    rc, out, err = run(cmd)
    if rc != 0:  # drawtext needs fontconfig; retry without timestamps
        vf = f"fps=1/{every},scale={width}:-1,tile={cols}x{rows}"
        rc, out, err = run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", path, "-vf", vf,
                            "-frames:v", "1", out_path])
    if rc != 0:
        raise RuntimeError(err.strip() or "could not build contact sheet")
    return frames


def main(argv=None):
    _utf8()
    p = argparse.ArgumentParser(description="Probe video size, fps, cuts and build a contact sheet.")
    p.add_argument("path", help="video file")
    p.add_argument("--threshold", type=float, default=0.3, help="scene-change threshold 0-1 (default 0.3)")
    p.add_argument("--contact-sheet", metavar="OUT.jpg", help="write a tiled contact sheet image")
    p.add_argument("--every", type=float, default=1.0, help="seconds between sheet frames (default 1)")
    p.add_argument("--cols", type=int, default=6, help="sheet columns (default 6)")
    p.add_argument("--width", type=int, default=240, help="sheet thumbnail width (default 240)")
    p.add_argument("--shots-out", metavar="OUT.json", help="write shots.json for check_shots.py")
    p.add_argument("--sweep", action="store_true", help="also print cut counts at several thresholds")
    p.add_argument("--json", action="store_true", help="print JSON")
    a = p.parse_args(argv)
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        print("error: ffmpeg and ffprobe must be on PATH", file=sys.stderr)
        return 2
    try:
        open(a.path, "rb").close()
        info = probe(a.path)
        cuts = detect_cuts(a.path, a.threshold)
    except (OSError, RuntimeError, ValueError) as err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    bounds = [0.0] + [c for c in cuts if 0 < c < info["duration"]] + [info["duration"]]
    shots = [{"id": i + 1, "duration": round(b - a_, 3)} for i, (a_, b) in enumerate(zip(bounds, bounds[1:])) if b - a_ > 0.04]
    info["cuts"] = len(cuts)
    info["cut_times"] = cuts
    info["cuts_per_10s"] = round(len(cuts) / info["duration"] * 10, 2) if info["duration"] else 0
    info["average_shot_seconds"] = round(sum(s["duration"] for s in shots) / len(shots), 2) if shots else 0
    if a.sweep:
        info["sweep"] = {str(th): len(detect_cuts(a.path, th)) for th in (0.04, 0.08, 0.15, 0.3)}
    if a.contact_sheet:
        try:
            info["contact_sheet_frames"] = contact_sheet(a.path, a.contact_sheet, a.every, a.cols, a.width)
            info["contact_sheet"] = a.contact_sheet
        except RuntimeError as err:
            print(f"error: {err}", file=sys.stderr)
            return 2
    if a.shots_out:
        with open(a.shots_out, "w", encoding="utf-8") as fh:
            json.dump({"shots": shots}, fh, indent=2)
        info["shots_out"] = a.shots_out
    if a.json:
        print(json.dumps(info, indent=2))
    else:
        print(f"{info['width']}x{info['height']} @ {info['fps']} fps, {info['duration']}s, audio: {'yes' if info['has_audio'] else 'NO'}")
        print(f"{info['cuts']} detected cut(s), {info['cuts_per_10s']} per 10s, average shot {info['average_shot_seconds']}s")
        if a.sweep:
            print("cuts by threshold: " + ", ".join(f"{k}: {v}" for k, v in info["sweep"].items()) +
                  " (dark scenes with small text need low thresholds; low values also count in-scene growth)")
        if cuts:
            print("cuts at: " + ", ".join(f"{c:.2f}s" for c in cuts[:40]) + (" ..." if len(cuts) > 40 else ""))
        if a.contact_sheet:
            print(f"contact sheet: {a.contact_sheet} ({info['contact_sheet_frames']} frames). Look at it.")
        if a.shots_out:
            print(f"shots written to {a.shots_out}: run check_shots.py on it")
    return 0


if __name__ == "__main__":
    sys.exit(main())
