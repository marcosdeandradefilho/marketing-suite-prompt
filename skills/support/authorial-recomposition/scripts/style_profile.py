#!/usr/bin/env python3
"""Descriptive style profiler for editorial use.

This script does not detect AI authorship, provenance, or watermarks.
It reports simple surface statistics to support revision decisions.
"""

import re
import sys
import json
import statistics
from collections import Counter
from pathlib import Path

WORD_RE = re.compile(r"\b[\wÀ-ÖØ-öø-ÿ'-]+\b", re.UNICODE)
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ])")


def words(text):
    return WORD_RE.findall(text)


def sentences(text):
    parts = [p.strip() for p in SENTENCE_SPLIT.split(text.strip()) if p.strip()]
    return parts or ([text.strip()] if text.strip() else [])


def paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def safe_stdev(values):
    return statistics.pstdev(values) if len(values) > 1 else 0.0


def profile(text):
    ws = words(text)
    ss = sentences(text)
    ps = paragraphs(text)
    sent_lens = [len(words(s)) for s in ss]
    para_sents = [len(sentences(p)) for p in ps]
    lower = [w.lower() for w in ws]
    counts = Counter(lower)

    lexical_diversity = (len(counts) / len(ws)) if ws else 0.0
    hapax = sum(1 for _, c in counts.items() if c == 1)
    hapax_ratio = (hapax / len(counts)) if counts else 0.0

    triads = len(re.findall(r"\b[^,;:.!?]{2,40},\s+[^,;:.!?]{2,40}\s+e\s+[^,;:.!?]{2,40}(?:[.;])", text, flags=re.I))
    colon_count = text.count(":")
    semicolon_count = text.count(";")
    dash_count = text.count("—") + text.count("–")
    paren_count = text.count("(") + text.count(")")

    return {
        "words": len(ws),
        "sentences": len(ss),
        "paragraphs": len(ps),
        "sentence_words_mean": round(statistics.mean(sent_lens), 2) if sent_lens else 0,
        "sentence_words_stdev": round(safe_stdev(sent_lens), 2),
        "sentence_words_min": min(sent_lens) if sent_lens else 0,
        "sentence_words_max": max(sent_lens) if sent_lens else 0,
        "paragraph_sentences_mean": round(statistics.mean(para_sents), 2) if para_sents else 0,
        "paragraph_sentences_stdev": round(safe_stdev(para_sents), 2),
        "lexical_diversity_type_token": round(lexical_diversity, 4),
        "hapax_ratio": round(hapax_ratio, 4),
        "punctuation": {
            "colon": colon_count,
            "semicolon": semicolon_count,
            "dash": dash_count,
            "parenthesis_marks": paren_count,
        },
        "possible_triad_patterns": triads,
        "top_words": counts.most_common(20),
        "note": "Indicadores descritivos para revisão editorial; não inferem autoria nem origem por IA."
    }


def main():
    if len(sys.argv) != 2:
        print("Uso: python style_profile.py arquivo.txt", file=sys.stderr)
        raise SystemExit(2)
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    print(json.dumps(profile(text), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
