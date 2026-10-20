🇧🇷 [Português](CONTRIBUINDO.md) · 🇬🇧 **English**

# Contributing to Crivo

Thank you for wanting to improve Crivo! The idea is to pool what each of us learns while examining skills, plugins and packages, so everyone can install more safely.

## Ways to contribute

- **New risk pattern** — something you found that the scan didn't catch (e.g., a new way to hide telemetry, a dangerous manifest field). Open an *issue* with a **harmless** example that reproduces the pattern.
- **False positive** — something flagged as suspicious that is common and legitimate. Describe the context.
- **Lesson learned** — a real case (without exposing people) that justifies a new rule in `SKILL.md`.
- **New sources for the checker** — PyPI, crates.io, Homebrew, Docker Hub, editor extensions…
- **New guard patterns** — install commands from other ecosystems.
- **Translation** — the project is in Portuguese and English; other languages are welcome.

## How to submit a change

1. Fork and create a branch.
2. Change what you need. If you touch the scan or the guard, **add a case in `testes/`** (a harmless sample and/or a command in `rodar-testes.sh`).
3. Run `bash testes/rodar-testes.sh` — everything must pass.
4. Update `CHANGELOG.md` (the "Unreleased" section).
5. **Keep both languages in sync**: if you change a document or the skill, update its counterpart (`README.md` ↔ `README.en.md`, `CONFIGURAR.md` ↔ `CONFIGURE.md`, `CONTRIBUINDO.md` ↔ `CONTRIBUTING.md`, `SEGURANCA.md` ↔ `SECURITY.md`, `skill/` ↔ `skill-en/`). If you can't translate, say so in the PR and a maintainer will help.
6. Open a *pull request* explaining **which risk the change covers** and **how it was tested**.

## Important rules

- **Test samples are harmless text.** No functional malicious code, no links to real malware, no instructions that cause harm if executed. Use `.invalid`/`example.com` domains.
- **No personal data**: emails, paths with usernames, tokens, private repository names.
- **The skill and scripts must not gain external dependencies** (only `bash`, standard-library `python3`, `git`, `curl`; `gh` optional). Crivo must be auditable by reading a few files.
- **The scripts only read and query.** Nothing in Crivo may install, download-and-execute, or send data to third parties (except the optional email to the user themselves).
- Changes to the agent's behavior (the `SKILL.md` text) must explain **why** — preferably with a real case.

## Style

- Plain language, short sentences. Technical terms get a brief explanation the first time.
- Scripts: short comments saying what and why.

## Questions

Open an *issue* with the `question` label (`pergunta`).
