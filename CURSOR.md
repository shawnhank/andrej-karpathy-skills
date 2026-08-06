# Using this repo with Cursor

This project includes a **Cursor project rule** so the Karpathy-inspired behavioral guidelines apply automatically when you work here.

## In this repository

1. Open the folder in Cursor.
2. The rule [`.cursor/rules/karpathy-guidelines.mdc`](.cursor/rules/karpathy-guidelines.mdc) is committed with `alwaysApply: true`, so you do not need extra installation steps.
3. In Cursor, you can confirm it under **Settings → Rules** (or the project rules UI), where `karpathy-guidelines` should appear.

## Use the same guidelines in another project

**Cursor (recommended):** Copy `.cursor/rules/karpathy-guidelines.mdc` into that project’s `.cursor/rules/` directory (create the folders if needed). Adjust or merge with existing rules as you like.

**Other tools:** If a stack only supports a root instruction file, copy [`CLAUDE.md`](CLAUDE.md) into that project instead (or merge its contents into your existing instructions).

## Optional: personal Agent Skills

If you want the same content as a reusable skill under `~/.cursor/skills`, use [`skills/karpathy-guidelines/SKILL.md`](skills/karpathy-guidelines/SKILL.md). You can copy or symlink it into your personal skills directory; use whatever layout you use for other skills.

## Claude Code vs Cursor

- **Claude Code:** Install via the plugin marketplace and [`README.md`](README.md) instructions; the plugin exposes the skill from this repo. Per-project use can also rely on `CLAUDE.md`.
- **Cursor:** Use the committed `.cursor/rules/` file as described above. Cursor does not read `.claude-plugin/` or `CLAUDE.md` by default.

## For contributors

The four principles live in a single source of truth, **[`shared/guidelines-body.md`](shared/guidelines-body.md)** (with a shared footer in [`shared/guidelines-footer.md`](shared/guidelines-footer.md)). Do **not** edit `CLAUDE.md`, `.cursor/rules/karpathy-guidelines.mdc`, or `skills/karpathy-guidelines/SKILL.md` by hand — they are generated.

When you change the principles:

1. Edit the shared source under `shared/`.
2. Run `python scripts/sync_guidelines.py` to regenerate the derived files.
3. Commit the shared source and the regenerated files together.

`python scripts/sync_guidelines.py --check` verifies the derived files are up to date; it runs automatically via the [pre-commit hook](.pre-commit-config.yaml) (`pre-commit install`).
