#!/usr/bin/env python3
"""Scan prose (English and Hinglish) for AI-slop patterns, judged by density.

Usage:
  python slop_scan.py draft.md
  cat draft.txt | python slop_scan.py -
  python slop_scan.py draft.md --format json --allow S11,S12

Exit codes: 0 clean or watch, 1 slop (score above --max-score, or a high-severity hit), 2 usage error.
A single hit is normal writing. Clusters in a paragraph, and score per 100 words, are what matter.
Suppress a deliberate choice with --allow ID. Fenced code blocks are ignored.
"""
import argparse
import json
import re
import statistics
import sys

I = re.I

# (id, label, weight, regex, fix)  weight 3 = high severity (always fails)
RULES = [
    ("S01", "contrast framing", 2,
     re.compile(r"\bnot\s+(?:just|only|merely|simply)\b[^.\n]{0,80}?\b(?:but|also|it['’]s|it is|we['’]re|we are|you['’]re|they['’]re|this is|that['’]s)\b", I),
     "State the true half directly, or join: 'faster and cheaper'."),
    ("S01", "contrast framing", 2,
     re.compile(r"\b(?:isn['’]t|is not|wasn['’]t|aren['’]t)\s+(?:about\s+)?[^.\n]{1,60}?[.;,\u2014\u2013]\s+(?:it['’]s|it is|this is|that['’]s)\s+(?:about\s+)?", I),
     "Drop the straw man and say what it is."),
    ("S01", "contrast framing", 2,
     re.compile(r"\bno [^.\n]{1,25}\.\s+no [^.\n]{1,25}\.\s+just\b", I),
     "Name the one real thing instead of the 'no, no, just' pattern."),
    ("S02", "throat-clearing opener", 2,
     re.compile(r"\b(?:in today['’]s (?:fast-paced |digital |ever-changing |modern )?(?:world|landscape|age|era)|in the (?:ever-evolving|rapidly (?:changing|evolving)) |when it comes to |let['’]s (?:dive|delve|explore|unpack)|at the end of the day|needless to say|in the realm of)", I),
     "Delete; start at the first sentence that carries information."),
    ("S03", "summary closer", 2,
     re.compile(r"\b(?:in conclusion|in summary|to sum up|to summari[sz]e|the bottom line is|all in all)\b", I),
     "Stop at the last real point."),
    ("S04", "hedge stacking", 1,
     re.compile(r"\b(?:might|may|could|can) (?:potentially|possibly|perhaps)\b|\bit(?:['’]s| is) (?:worth|important|crucial) (?:noting|to note|to remember|mentioning)\b|\bit should be noted\b|\bthat said,|\bhaving said that\b", I),
     "Commit, or say exactly what is uncertain."),
    ("S05", "faux-insight setup", 2,
     re.compile(r"\bhere['’]s (?:the (?:thing|deal|kicker|catch|truth)|why|what|how)\b|\bthat['’]s the real \w+|\bthe real (?:unlock|challenge|story|secret|magic)\b|\blet that sink in\b|\bread that again\b|\band honestly\?", I),
     "Say the insight itself."),
    ("S06", "dramatic colon reveal", 1,
     re.compile(r"(?:^|[.!?]\s+)(?:the (?:best part|catch|kicker|result|secret|truth|twist|problem|solution|upside|downside)|one thing):\s", I | re.M),
     "Use a plain sentence; colons are for lists and labels."),
    ("S07", "trailing -ing analysis", 1,
     re.compile(r",\s+(?:highlighting|underscoring|showcasing|emphasi[sz]ing|reflecting|demonstrating|illustrating|reinforcing|ensuring|fostering|enabling|paving the way)\s+(?:the|its|a|how|that|our|their)\b", I),
     "Cut the clause or give it a fact in its own sentence."),
    ("S08", "importance puffery", 2,
     re.compile(r"\b(?:a testament to|stands as a|serves as a|plays an? (?:crucial|pivotal|vital|key|important) role|rich tapestry|vibrant (?:community|landscape)|game[- ]chang(?:er|ing)|revolutioni[sz](?:e|es|ed|ing)|unlock(?:s|ing)? the (?:power|potential)|to the next level|next[- ]level)\b", I),
     "Replace with the concrete effect, with a number if there is one."),
    ("S09", "weasel attribution", 1,
     re.compile(r"\b(?:experts (?:say|agree|believe)|studies (?:show|suggest)|research (?:shows|suggests)|many (?:people )?(?:believe|say|argue)|some (?:say|argue)|it is (?:widely|often) (?:believed|said))\b", I),
     "Name the source or drop the claim."),
    ("S18", "false range", 1,
     re.compile(r"\b(?:ranging|spanning|everything|anything|whether)\s+from\b[^.\n]{3,60}?\bto\b|(?:^|[.!?]\s+)from\s+[^,.\n]{3,40}\s+to\s+[^,.\n]{3,40},", I | re.M),
     "Name the real items; a 'from X to Y' spectrum that is not a spectrum says nothing."),
    ("S19", "hedging about source availability", 2,
     re.compile(r"\b(?:while|although) (?:specific )?(?:details|information|data) (?:is|are) (?:limited|scarce|unavailable)|\bbased on (?:the )?(?:available|provided) (?:information|sources|data)|\bin the (?:provided|available) (?:sources|search results)|\bnot (?:widely )?(?:available|documented|disclosed)\b|\bdoes not (?:by itself )?establish\b|\bshould be (?:treated|presented|viewed) as\b[^.\n]{0,60}\brather than\b", I),
     "Say what is known and cite it, or say plainly what is missing and stop."),
    ("S20", "promotional or travel-guide language", 1,
     re.compile(r"\b(?:rich (?:cultural )?(?:heritage|history|tapestry)|breathtaking|must[- ](?:visit|see)|stunning (?:natural )?beauty|enduring legacy|lasting legacy|clean and modern|steadfast dedication|profound heritage|watershed moment|key turning point|continues? to captivate|leaves? a lasting impact|deeply rooted)\b", I),
     "Replace with a checkable detail: what it looks like, how many, since when."),
    ("S23", "vague association", 1,
     re.compile(r"\b(?:widely|closely|often|commonly)\s+(?:associated|connected|linked)\s+(?:with|to)\b|\bassociated with (?:the )?(?:leadership|development|growth)\b", I),
     "State the actual relationship: who did what, when."),
    ("S15", "colourful verb inflation", 1,
     re.compile(r"\b(?:garnered|boasts|ushers? in|spearhead(?:s|ed)?|ignite(?:s|d)?)\b", I),
     "Use the plain verb."),
    ("S16", "placeholder or chatbot residue", 3,
     re.compile(r"\[(?:your|insert|company|brand|client)\b[^\]\[]*\]|\[(?:full )?name\]|\bas an ai (?:language )?model\b|\bi hope this (?:email|message|helps)\b|\bgreat question\b|\bi['’]d be happy to\b|\bfeel free to reach out\b|\bcertainly!|\bsure thing!", I),
     "Remove; these are the loudest tells."),
]

BUZZ = re.compile(
    r"\b(?:delv(?:e|es|ed|ing)|tapestry|crucial|pivotal|seamless(?:ly)?|robust|leverag(?:e|es|ed|ing)|elevat(?:e|es|ed|ing)|navigat(?:e|es|ed|ing)|realm|holistic|synerg(?:y|ies)|cutting-edge|state-of-the-art|empower(?:s|ed|ing)?|unleash(?:es|ed|ing)?|foster(?:s|ed|ing)?|intricate|multifaceted|testament|underscor(?:e|es|ed|ing)|bespoke|transformative|groundbreaking|streamlin(?:e|es|ed|ing)|harness(?:es|ed|ing)?|resonat(?:e|es|ed|ing)|ever-evolving|comprehensive solution|landscape)\b",
    I)

HINGLISH_RULES = [
    ("H01", "translated CTA", 2,
     re.compile(r"अभी खरीदें|आज ही संपर्क करें|हमसे जुड़ें|अधिक जानकारी के लिए|\baaj hi (?:sampark|contact) (?:karein|kijiye|kare)\b|\bsampark karein\b|\bhamse jud(?:iye|en)\b", I),
     "Write what a person would say aloud."),
    ("H02", "sanskritised register in casual copy", 1,
     re.compile(r"उत्कृष्ट|सर्वोत्तम|सर्वश्रेष्ठ|अद्वितीय|अत्याधुनिक|\bsarvottam\b|\butkrisht\b|\bsarvashreshth\b|\badvitiya\b|\batyadhunik\b", I),
     "Use the word the audience actually says."),
    ("H03", "stock superlative", 1,
     re.compile(r"\bsabse (?:best|behtar(?:in)?)\b|\bnumber (?:1|one|ek)\b|quality ka dusra naam|\bek naya andaz\b|\bnaye daur\b|\bhar zaroorat\b|\bbejod\b", I),
     "Replace with a proof point."),
    ("H04", "translated English hook", 2,
     re.compile(r"\bkya aap jaante hain\b|\bkya aapne kabhi socha\b|क्या आप जानते हैं|क्या आपने कभी सोचा|\bek aisi duniya\b|\bimagine karo\b", I),
     "Open with the situation or the tension, not a translated hook."),
]

SPELLING_VARIANTS = [
    ("nahi", "nahin", "nhi"),
    ("bahut", "bohot", "bohut"),
    ("kyun", "kyu", "kyon"),
    ("accha", "achha", "acha"),
    ("mein", "main_loc"),  # placeholder second form is ignored below
]

DEV = re.compile(r"[\u0900-\u097F]")
ROMAN_HINDI = re.compile(r"\b(?:hai|hain|nahi|nahin|aur|kaam|aapka|hamara|kya|kyun|bahut|accha|achha|karo|karein|kijiye|mein|tum|aap)\b", I)
CONJ = re.compile(r"\b(?:moreover|furthermore|in addition|additionally|on the other hand|in contrast|however)\b", I)
INLINE_HEADER = re.compile(r"^\s*[-*+]\s+\*\*[^*]+\*\*")
LIST_OR_TABLE = re.compile(r"^\s*(?:[-*+]\s|\d+[.)]\s|\|)")
SENT_SPLIT = re.compile(r"(?<=[.!?\u0964])\s+")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")
DASH = re.compile(r"\u2014|\s\u2013\s|\s--\s")
BOLD = re.compile(r"\*\*[^*\n]+\*\*")
LIST3 = re.compile(r"\b[\w'’-]+(?: [\w'’-]+)?, [\w'’-]+(?: [\w'’-]+)?,? (?:and|or|aur) [\w'’-]+(?: [\w'’-]+)?\b", I)


def strip_code(text):
    text = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    return re.sub(r"`[^`\n]*`", " ", text)


def words(text):
    return len(re.findall(r"[\w\u0900-\u097F'’-]+", text))


def paragraphs(text):
    """Yield (start_line, paragraph_text)."""
    lines = text.split("\n")
    buf, start = [], 0
    for i, line in enumerate(lines):
        if line.strip() == "":
            if buf:
                yield start + 1, "\n".join(buf)
                buf = []
        else:
            if not buf:
                start = i
            buf.append(line)
    if buf:
        yield start + 1, "\n".join(buf)


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def snippet(text, m, width=70):
    s = max(0, m.start() - 15)
    e = min(len(text), m.end() + width - 15)
    return re.sub(r"\s+", " ", text[s:e]).strip()


def scan(raw, allow=(), hinglish=None):
    text = strip_code(raw)
    total_words = max(words(text), 1)
    if hinglish is None:
        hinglish = bool(DEV.search(text)) or len(ROMAN_HINDI.findall(text)) >= 4
    findings = []

    def add(rid, label, weight, line, snip, fix):
        if rid in allow:
            return
        findings.append({"id": rid, "label": label, "weight": weight, "line": line, "text": snip, "fix": fix})

    rules = RULES + (HINGLISH_RULES if hinglish else [])
    for rid, label, weight, rx, fix in rules:
        for m in rx.finditer(text):
            add(rid, label, weight, line_of(text, m.start()), snippet(text, m), fix)

    for start, para in paragraphs(text):
        pw = words(para)
        # S10 buzzword cluster
        hits = list(BUZZ.finditer(para))
        if len(hits) >= 2:
            found = sorted({h.group(0).lower() for h in hits})
            add("S10", "buzzword cluster", min(len(hits), 4), start, ", ".join(found),
                "Use plain verbs and nouns; judge clusters, not single words.")
        # S11 em-dash density
        d = len(DASH.findall(para))
        if d >= 3 or (pw >= 20 and d / pw * 80 > 1.5 and d >= 2):
            add("S11", "em-dash habit", min(d, 4), start, f"{d} dashes in {pw} words",
                "Use commas, full stops or parentheses.")
        # S12 rule of three
        t = len(LIST3.findall(para))
        if t >= 3:
            add("S12", "rule of three", min(t - 1, 4), start, f"{t} triads in one paragraph",
                "Use the real count; three only when there are three.")
        # S13 decoration
        prose_lines = [ln for ln in para.split("\n") if not LIST_OR_TABLE.match(ln)]  # bold labels in lists and tables are normal
        b = len(BOLD.findall("\n".join(prose_lines)))
        e = len(EMOJI.findall(para))
        if b >= 3 or e >= 3:
            add("S13", "decoration", 1, start, f"{b} bold spans, {e} emoji",
                "Let sentence structure carry emphasis.")
        # S21 conjunction pile
        cj = len(CONJ.findall(para))
        if cj >= 3:
            add("S21", "stacked transition words", min(cj - 1, 4), start, f"{cj} transition words in one paragraph",
                "Cut most; let the order of sentences carry the logic.")
        # S22 inline-header vertical list
        ih = sum(1 for ln in para.split("\n") if INLINE_HEADER.match(ln))
        if ih >= 4:
            add("S22", "inline-header bullet list", 1, start, f"{ih} bullets that start with a bold label",
                "Write it as prose, or as a table if it is real reference material.")
        # S14 even rhythm
        sents = [s for s in SENT_SPLIT.split(para.replace("\n", " ")) if words(s) > 0]
        if len(sents) >= 5:
            lens = [words(s) for s in sents]
            mean = statistics.mean(lens)
            if mean > 0 and statistics.pstdev(lens) / mean < 0.22:
                add("S14", "even rhythm", 1, start, f"{len(sents)} sentences, near-uniform length (~{mean:.0f} words)",
                    "Vary sentence length on purpose.")

    if hinglish:
        for sent in SENT_SPLIT.split(text):
            if DEV.search(sent) and ROMAN_HINDI.search(sent):
                add("H06", "Devanagari and Roman Hindi mixed in one sentence", 1, line_of(text, text.find(sent[:20]) if sent[:20] in text else 0),
                    re.sub(r"\s+", " ", sent)[:70], "Pick one script per sentence; English words may stay in Roman.")
        low = text.lower()
        for group in SPELLING_VARIANTS:
            present = [w for w in group if w != "main_loc" and re.search(r"\b" + w + r"\b", low)]
            if len(present) >= 2:
                add("H05", "mixed Roman Hindi spelling", 1, 1, " / ".join(present),
                    "Pick one spelling scheme and keep it.")

    score = sum(f["weight"] for f in findings) / total_words * 100
    high = any(f["id"] == "S16" for f in findings)  # placeholders and chatbot residue always block
    return {"words": total_words, "hinglish": hinglish, "score": round(score, 2),
            "high_severity": high, "findings": sorted(findings, key=lambda f: (f["line"], f["id"]))}


def verdict(result, max_score):
    if result["high_severity"] or result["score"] >= max_score:
        return "slop"
    if result["score"] >= max_score / 3:
        return "watch"
    return "clean"



def _utf8():
    """Windows consoles default to a legacy code page; keep Hinglish and emoji printable."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def main(argv=None):
    _utf8()
    p = argparse.ArgumentParser(description="Scan prose for AI-slop patterns by density.")
    p.add_argument("path", help="file to scan, or - for stdin")
    p.add_argument("--format", choices=["text", "json"], default="text")
    p.add_argument("--allow", default="", help="comma-separated rule IDs to ignore (deliberate choices)")
    p.add_argument("--max-score", type=float, default=4.0, help="weighted hits per 100 words that counts as slop (default 4)")
    p.add_argument("--hinglish", action="store_true", help="force Hinglish rules on")
    a = p.parse_args(argv)
    try:
        raw = sys.stdin.read() if a.path == "-" else open(a.path, encoding="utf-8").read()
    except OSError as err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    allow = {x.strip().upper() for x in a.allow.split(",") if x.strip()}
    result = scan(raw, allow, True if a.hinglish else None)
    v = verdict(result, a.max_score)
    result["verdict"] = v
    if a.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for f in result["findings"]:
            print(f"L{f['line']:<4} [{f['id']} {f['label']}] {f['text']}\n       -> {f['fix']}")
        mode = "Hinglish+English" if result["hinglish"] else "English"
        print(f"\n{result['words']} words ({mode}) | score {result['score']} per 100 words | verdict: {v}")
        if v != "clean":
            print("Delete first, then rewrite. A clean scan is not proof of quality: run the taste pass.")
    return 0 if v != "slop" else 1


if __name__ == "__main__":
    sys.exit(main())
