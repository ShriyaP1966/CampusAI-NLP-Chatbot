"""Evaluate retrieval, answers, abstention and refusals on a labelled question set.

Usage::

    python -m campusai.evaluate                   # print the report
    python -m campusai.evaluate --output evaluation/results.md

The question set (``data/eval/questions.csv``) has a ``split`` column. The
confidence thresholds in ``campusai/retriever.py`` were chosen on the ``dev``
rows, so the ``test`` rows are the fair numbers to quote.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from campusai.engine import CampusAI
from campusai.language import detect_language

DEFAULT_QUESTIONS = Path(__file__).resolve().parent.parent / "data" / "eval" / "questions.csv"
LANGUAGES = ("en", "hi", "mr")


@dataclass
class Tally:
    """Counts for one slice (a language and split) of the question set."""

    total: int = 0
    lang_ok: int = 0
    answerable: int = 0
    hit1: int = 0
    hit3: int = 0
    reciprocal_rank: float = 0.0
    answered: int = 0
    correct: int = 0
    out_of_scope: int = 0
    declined: int = 0
    unsafe: int = 0
    refused: int = 0
    failures: list[str] = field(default_factory=list)

    def merge(self, other: Tally) -> None:
        for name in (
            "total", "lang_ok", "answerable", "hit1", "hit3", "reciprocal_rank", "answered",
            "correct", "out_of_scope", "declined", "unsafe", "refused",
        ):  # fmt: skip
            setattr(self, name, getattr(self, name) + getattr(other, name))
        self.failures += other.failures


def load_questions(path: Path = DEFAULT_QUESTIONS) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def evaluate(bot: CampusAI, rows: list[dict[str, str]]) -> dict[tuple[str, str], Tally]:
    """Run every row through the engine. Returns tallies keyed by (split, language)."""
    tallies: dict[tuple[str, str], Tally] = defaultdict(Tally)
    for row in rows:
        tally = tallies[(row["split"], row["lang"])]
        question, kind = row["question"], row["kind"]
        detected = detect_language(question)
        tally.total += 1
        tally.lang_ok += detected == row["lang"]
        answer = bot.ask(question)

        if kind == "answerable":
            tally.answerable += 1
            expected = row["expected_source"]
            ranked = [h.chunk.chunk_id for h in bot.retriever.search(question, detected, k=3)]
            if expected in ranked[:1]:
                tally.hit1 += 1
            if expected in ranked:
                tally.hit3 += 1
                tally.reciprocal_rank += 1 / (ranked.index(expected) + 1)
            tally.answered += answer.found
            cited = [s.chunk_id for s in answer.sources]
            ok = answer.found and expected in cited and row["expected_phrase"] in answer.text
            tally.correct += ok
            if not ok:
                tally.failures.append(f"[{row['id']}] {question} -> {answer.status} {cited[:2]}")
        elif kind == "out_of_scope":
            tally.out_of_scope += 1
            tally.declined += answer.status == "not_found"
            if answer.status != "not_found":
                tally.failures.append(
                    f"[{row['id']}] {question} -> {answer.status} (should decline)"
                )
        elif kind == "unsafe":
            tally.unsafe += 1
            tally.refused += answer.status == "refused"
            if answer.status != "refused":
                tally.failures.append(
                    f"[{row['id']}] {question} -> {answer.status} (should refuse)"
                )
    return tallies


def _pct(num: float, den: int) -> str:
    return f"{100 * num / den:.1f}%" if den else "n/a"


def _mrr(tally: Tally) -> str:
    return f"{tally.reciprocal_rank / tally.answerable:.2f}" if tally.answerable else "n/a"


def _row(label: str, t: Tally) -> str:
    cells = [
        label,
        str(t.total),
        _pct(t.lang_ok, t.total),
        _pct(t.hit1, t.answerable),
        _pct(t.hit3, t.answerable),
        _mrr(t),
        _pct(t.correct, t.answerable),
        _pct(t.declined, t.out_of_scope),
        _pct(t.refused, t.unsafe),
    ]
    return "| " + " | ".join(cells) + " |"


HEADER = (
    "| Slice | Questions | Language ID | Hit@1 | Hit@3 | MRR | Answer correct "
    "| Declined out-of-scope | Refused unsafe |\n"
    "|---|---:|---:|---:|---:|---:|---:|---:|---:|"
)


def render(tallies: dict[tuple[str, str], Tally], splits: tuple[str, ...] = ("test", "dev")) -> str:
    """Render the results as Markdown tables, one per split plus one for everything."""
    sections = []
    for split in (*splits, "all"):
        lines = [f"**{'All questions' if split == 'all' else split.capitalize() + ' split'}**", ""]
        lines.append(HEADER)
        total = Tally()
        for lang in LANGUAGES:
            if split == "all":
                parts = [tallies[(s, lang)] for s in splits if (s, lang) in tallies]
            else:
                parts = [tallies[(split, lang)]] if (split, lang) in tallies else []
            lang_tally = Tally()
            for part in parts:
                lang_tally.merge(part)
            if lang_tally.total:
                lines.append(_row(lang, lang_tally))
                total.merge(lang_tally)
        lines.append(_row("**All languages**", total))
        sections.append("\n".join(lines))
    return "\n\n".join(sections)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--questions", type=Path, default=DEFAULT_QUESTIONS)
    parser.add_argument("--docs", type=Path, default=None, help="folder of documents to index")
    parser.add_argument("--output", type=Path, default=None, help="write the tables here")
    parser.add_argument("--failures", action="store_true", help="list every failed question")
    args = parser.parse_args()

    bot = CampusAI.from_directory(args.docs)
    tallies = evaluate(bot, load_questions(args.questions))
    report = render(tallies)
    print(report)
    if args.failures:
        print("\nFailures:")
        for tally in tallies.values():
            for line in tally.failures:
                print(" ", line)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
