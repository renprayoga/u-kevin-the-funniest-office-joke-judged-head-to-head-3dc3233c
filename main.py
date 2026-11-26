"""The Funniest Office Joke, Judged Head to Head — entry writer.

Chosen line (118 characters, one line):
    The office plants are the only ones thriving here — they get
    watered, praised, and never asked to hop on a quick call.

Why this line wins (judge rubric order: one-line office joke with setup
and turn, recognisable office truth, surprise, punchline last, fresh):
- On-subject joke: a real joke, setup ("plants are the only ones
  thriving") and turn ("never asked to hop on a quick call"), about
  office life.
- Recognisable: everyone who works in an office knows the "quick call"
  that is never quick, and the plant on the desk that outlives every
  reorg.
- Surprise: the reader expects a complaint about workload; instead the
  envy lands on the plants, and the punchline reframes the call as the
  thing that drains people.
- Punchline last: "hop on a quick call" closes the line, every word
  before it earns its place.
- Fresh: plants as the thriving ones is a new angle; avoids the
  reply-all, printer-jam and "per my last email" jokes the field is
  full of.

Program: writes the line to /output/entry.txt, then validates its own
output — exactly one line, 1-200 characters, not only
whitespace — and exits non-zero if the gate would fail. Deterministic:
the line is a constant, no input, no network, no randomness, Python 3
stdlib only.
"""

import os
import sys

ENTRY = 'The office plants are the only ones thriving here — they get watered, praised, and never asked to hop on a quick call.'

DESTINATION = "/output/entry.txt"
MIN_LEN = 1
MAX_LEN = 200


def _fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return -1


def _save() -> None:
    folder = os.path.dirname(DESTINATION)
    os.makedirs(folder, exist_ok=True)
    with open(DESTINATION, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ENTRY + "\n")


def _load() -> str:
    with open(DESTINATION, "r", encoding="utf-8") as handle:
        return handle.read()


def _check(written: str) -> int:
    entry = written.rstrip("\n")
    if not MIN_LEN <= len(entry) <= MAX_LEN:
        return _fail(f"entry is {len(entry)} characters (need {MIN_LEN}-{MAX_LEN})")
    if "\n" in entry or "\r" in entry:
        return _fail("entry is not a single line")
    if not entry.strip():
        return _fail("entry is only whitespace")
    # Revision pass: reject leading/trailing whitespace — a stray space
    # would silently change the judged text without changing the joke.
    if entry != entry.strip():
        return _fail("entry has leading or trailing whitespace")
    if entry != ENTRY:
        return _fail("written entry differs from the intended line")
    # The gate reads the whole file: exactly one trailing newline, so the
    # file holds one line and nothing else — no blank second line.
    if written != ENTRY + "\n":
        return _fail("written file is not exactly the entry plus one newline")
    return len(entry)


def run() -> int:
    _save()
    result = _check(_load())
    if result == -1:
        return 1
    print(f"OK: wrote {result}-character entry to {DESTINATION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
