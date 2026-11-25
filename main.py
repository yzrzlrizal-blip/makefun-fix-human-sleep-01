"""Fix Human Sleep: Funniest Patch Note.

Reads the one-line patch note shipped in entry.txt, validates it against
the competition gate (UTF-8 text, 1-160 characters, a single non-blank
line), writes it verbatim to $MAKEFUN_OUTPUT_DIR/entry.txt (default
/output/entry.txt), then re-reads the output and verifies the bytes match.
Pure standard library; deterministic; exits non-zero on any bad input.
"""

import os
import sys

MAX_CHARS = 160


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(here, "entry.txt")

    try:
        with open(source_path, "r", encoding="utf-8") as handle:
            text = handle.read()
    except OSError as exc:
        return fail(f"cannot read entry.txt: {exc}")

    if not text or not text.strip():
        return fail("entry is empty or only whitespace")
    if "\n" in text.rstrip("\n") or "\r" in text:
        return fail("entry must be a single line")
    text = text.rstrip("\n")
    if len(text) < 1 or len(text) > MAX_CHARS:
        return fail(f"entry is {len(text)} characters, must be 1-{MAX_CHARS}")
    if any(ord(ch) < 32 and ch not in ("\t",) for ch in text):
        return fail("entry contains control characters")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.txt")
    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(out_path, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
    except OSError as exc:
        return fail(f"cannot write {out_path}: {exc}")

    try:
        with open(out_path, "r", encoding="utf-8") as handle:
            written = handle.read()
    except OSError as exc:
        return fail(f"cannot re-read {out_path}: {exc}")
    if written != text:
        return fail("verification failed: output does not match entry.txt")

    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
