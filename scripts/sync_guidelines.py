#!/usr/bin/env python3
"""Generate the guideline files from a single shared source.

The four Karpathy principles are published verbatim in several places
(`CLAUDE.md`, the Cursor rule, and the Agent Skill). Keeping them in sync by
hand is error-prone, so this script treats `shared/guidelines-body.md` (plus a
shared footer) as the single source of truth and regenerates every derived
file from it.

Usage:
    python scripts/sync_guidelines.py           # write the derived files
    python scripts/sync_guidelines.py --check    # exit 1 if any file is stale
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SHARED = REPO_ROOT / "shared"
BODY_PATH = SHARED / "guidelines-body.md"
FOOTER_PATH = SHARED / "guidelines-footer.md"

CURSOR_DESCRIPTION = (
    "Behavioral guidelines to reduce common LLM coding mistakes. Use when "
    "writing, reviewing, or refactoring code to avoid overcomplication, make "
    "surgical changes, surface assumptions, and define verifiable success "
    "criteria."
)


@dataclass(frozen=True)
class Target:
    """A file generated from the shared guideline source."""

    path: str
    title: str
    intro: str
    front_matter: str = ""
    include_footer: bool = False


TARGETS: list[Target] = [
    Target(
        path="CLAUDE.md",
        title="# CLAUDE.md",
        intro=(
            "Behavioral guidelines to reduce common LLM coding mistakes. "
            "Merge with project-specific instructions as needed."
        ),
        include_footer=True,
    ),
    Target(
        path=".cursor/rules/karpathy-guidelines.mdc",
        title="# Karpathy behavioral guidelines",
        intro=(
            "Behavioral guidelines to reduce common LLM coding mistakes. "
            "Merge with project-specific instructions as needed."
        ),
        front_matter=(
            "---\n"
            f"description: {CURSOR_DESCRIPTION}\n"
            "alwaysApply: true\n"
            "---\n"
        ),
        include_footer=True,
    ),
    Target(
        path="skills/karpathy-guidelines/SKILL.md",
        title="# Karpathy Guidelines",
        intro=(
            "Behavioral guidelines to reduce common LLM coding mistakes, "
            "derived from [Andrej Karpathy's observations]"
            "(https://x.com/karpathy/status/2015883857489522876) on LLM "
            "coding pitfalls."
        ),
        front_matter=(
            "---\n"
            "name: karpathy-guidelines\n"
            f"description: {CURSOR_DESCRIPTION}\n"
            "license: MIT\n"
            "---\n"
        ),
    ),
]


def render(target: Target, body: str, footer: str) -> str:
    """Assemble the full contents of a derived file."""
    parts: list[str] = []
    if target.front_matter:
        parts.append(target.front_matter)
    parts.append(f"{target.title}\n")
    parts.append(f"{target.intro}\n")
    parts.append(body)
    if target.include_footer:
        parts.append(footer)
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify derived files are up to date instead of writing them",
    )
    args = parser.parse_args()

    body = BODY_PATH.read_text(encoding="utf-8").strip("\n") + "\n"
    footer = FOOTER_PATH.read_text(encoding="utf-8").strip("\n") + "\n"

    stale: list[str] = []
    for target in TARGETS:
        expected = render(target, body, footer)
        path = REPO_ROOT / target.path
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == expected:
            continue
        if args.check:
            stale.append(target.path)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")
            print(f"updated {target.path}")

    if args.check and stale:
        print(
            "The following files are out of sync with shared/guidelines-body.md:",
            file=sys.stderr,
        )
        for name in stale:
            print(f"  - {name}", file=sys.stderr)
        print(
            "Run `python scripts/sync_guidelines.py` and commit the result.",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
