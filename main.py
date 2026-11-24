#!/usr/bin/env python3
"""Publish the one-line entry for u-brisk-kestrel-93-one-line-one-minute-the-vending-376bbeee.

The entry is one pickup line, 200 characters at most, that a vending machine
would use on a passing human. This program reads the line from entry.txt in
the repository, validates it, and publishes its raw bytes verbatim to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt when set).

Publishing is byte-verbatim on purpose: the judge compares the exact bytes
the program writes, so the program never strips, re-encodes or re-wraps the
text. Validation rejects anything that is not UTF-8 text, is empty or only
whitespace, or is longer than the limit.
"""

import argparse
import os
import sys

DEFAULT_MAX_CHARS = 200
ENTRY_FILENAME = "entry.txt"
OUTPUT_FILENAME = "entry.txt"


def load_raw(entry_path):
    """Read the entry file as raw bytes, without any decoding or trimming."""
    with open(entry_path, "rb") as handle:
        return handle.read()


def decode(raw):
    """Decode raw bytes as UTF-8, raising a clear error on bad bytes."""
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"entry is not valid UTF-8: {exc}") from exc


def validate(text, max_chars):
    """Check the decoded entry against the competition gate.

    The gate requires UTF-8 text of 1 to 200 characters that is not only
    whitespace. Surrounding whitespace is rejected rather than stripped,
    because stripping would change the bytes the judge sees.
    """
    if not text:
        raise ValueError("entry is empty")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if len(text) > max_chars:
        raise ValueError(
            f"entry is {len(text)} characters, over the {max_chars} limit"
        )
    if text != text.strip():
        raise ValueError("entry has surrounding whitespace; remove it")
    if "\t" in text:
        raise ValueError("entry contains a tab character")
    for char in text:
        if ord(char) < 0x20 and char not in ("\n",):
            raise ValueError("entry contains a control character")
    return text


def validate_raw(raw, max_chars):
    """Decode and validate raw entry bytes in one step."""
    return validate(decode(raw), max_chars)


def resolve_output_dir(explicit=None):
    """Return the output directory, honouring the grader's override."""
    if explicit:
        return explicit
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def resolve_entry_path(explicit):
    """Return the entry file path, defaulting to entry.txt beside main.py."""
    if explicit:
        return explicit
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, ENTRY_FILENAME)


def publish(raw, output_dir):
    """Write the raw entry bytes verbatim to the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, OUTPUT_FILENAME)
    with open(output_path, "wb") as handle:
        handle.write(raw)
    return output_path


def parse_args(argv):
    """Parse the command-line options for this publisher."""
    parser = argparse.ArgumentParser(
        description="Publish the one-line entry verbatim to the output directory."
    )
    parser.add_argument(
        "--entry",
        default=None,
        help="Path to the entry file (default: entry.txt beside main.py).",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=DEFAULT_MAX_CHARS,
        help="Maximum allowed characters (default: 200).",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory (default: $MAKEFUN_OUTPUT_DIR or /output).",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Validate the entry and exit without writing anything.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Print nothing on success.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    """Load, validate and publish the entry, or only verify it."""
    args = parse_args(argv)
    entry_path = resolve_entry_path(args.entry)
    try:
        raw = load_raw(entry_path)
        text = validate_raw(raw, args.max_chars)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.verify_only:
        if not args.quiet:
            print(f"Valid ({len(text)} chars): {text}")
        return 0
    if "\n" in text:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    output_path = publish(raw, resolve_output_dir(args.output_dir))
    if not args.quiet:
        print(f"Wrote {len(raw)} bytes to {output_path} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
