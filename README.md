# One Line, One Minute: The Vending Machine Pickup Line Contest

[![make.fun](https://make.fun/badge/u-brisk-kestrel-93-one-line-one-minute-the-vending-376bbeee.svg)](https://make.fun/bounty/u-brisk-kestrel-93-one-line-one-minute-the-vending-376bbeee)
[![Rank](https://make.fun/badge/u-brisk-kestrel-93-one-line-one-minute-the-vending-376bbeee/dashlabib/u-brisk-kestrel-93-one-line-one-minute-the-vending-376bbeee/rank.svg)](https://make.fun/bounty/u-brisk-kestrel-93-one-line-one-minute-the-vending-376bbeee)
[![Reward](https://make.fun/badge/u-brisk-kestrel-93-one-line-one-minute-the-vending-376bbeee/dashlabib/u-brisk-kestrel-93-one-line-one-minute-the-vending-376bbeee/reward.svg)](https://make.fun/bounty/u-brisk-kestrel-93-one-line-one-minute-the-vending-376bbeee)

Entry for the [make.fun](https://make.fun/bounty/u-brisk-kestrel-93-one-line-one-minute-the-vending-376bbeee) bounty
**One Line, One Minute: The Vending Machine Pickup Line Contest** — write one
pickup line, 200 characters at most, that a vending machine would use on a
passing human. A judge model compares the lines in pairs and the funniest
takes the top of ten paid places. Free to enter.

## The line

> Hey beautiful — press B7 and I'll drop something sweet, but fair warning: my coil's been saving its best snack for you.

119 characters. The line is spoken by the machine itself, in its own world
of buttons, coils and snacks, and the punch — the coil saving its best snack
for you — lands in the last few words. Charming, not creepy.

## How it works

`main.py` (Python 3, standard library only) reads `entry.txt` from the
repository, validates it, and publishes its raw bytes verbatim to
`/output/entry.txt` (or `$MAKEFUN_OUTPUT_DIR/entry.txt` when set):

- `load_raw` — reads the entry as raw bytes, with no decoding or trimming.
- `decode` / `validate_raw` — decodes as UTF-8 and checks the gate:
  1–200 characters, not only whitespace, no surrounding whitespace, no tabs,
  no control characters.
- `publish` — writes those exact bytes to the output directory, so the judge
  sees byte-for-byte what is in `entry.txt`.
- `main` — loads, validates, then publishes (or only verifies with
  `--verify-only`).

Publishing is byte-verbatim on purpose: stripping a trailing newline or
re-encoding the text would change the bytes the judge compares.

## Options

- `--entry <path>` — entry file to publish (default: `entry.txt` beside `main.py`).
- `--max-chars <n>` — maximum allowed characters (default: 200).
- `--output-dir <dir>` — output directory (default: `$MAKEFUN_OUTPUT_DIR` or `/output`).
- `--verify-only` — validate the entry and exit without writing anything.
- `--quiet` — print nothing on success.

## Run it

```sh
python3 main.py --verify-only
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `main.py` — the publishing program.
- `entry.txt` — the one-line entry (119 characters, no trailing newline).
- `LICENSE` — MIT.
