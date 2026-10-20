🇧🇷 [Português](README.md) · 🇬🇧 **English**

# Crivo 🛡️ — security before installing anything into your agent

**Crivo** (Portuguese for "sieve") is a skill for [Claude Code](https://code.claude.com) (and skill-compatible agents) that makes the agent **security-check everything it installs** — skills, plugins, MCP servers, npm/pip packages, binaries, `curl | bash` scripts — **before** installing, and only with your approval.

It was born from a practical need: installing a third-party skill means giving the agent instructions (and sometimes code) written by someone else, which run **with your permissions** — your files, your keys, your email, your deploys. Popularity is no guarantee: stars can be inflated, names can be imitated, and a version published yesterday may be the compromised one.

## What Crivo does

1. **Identifies** what is about to be installed and whether you really need it (including whether the agent already has something equivalent built in).
2. **Checks provenance and reputation** — real owner, imitated names, anomalous popularity, maintainer changes.
3. **Applies a version quarantine** — uses the newest version that is at least 7 days old (14 for critical tools). Malicious packages are usually discovered within that window.
4. **Downloads into an isolated folder, without executing anything.**
5. **Verifies integrity** — signatures, provenance (SLSA), checksums from two sources.
6. **Performs static analysis** — a scan script plus a real read-through: network, telemetry, secrets, hidden execution, persistence, and agent-specific risks:
   - `allowed-tools` that run commands **without asking for permission**;
   - hooks that read every message you send or that **call the AI on every response** (ongoing cost);
   - MCP servers and their credentials;
   - manipulative instructions and invisible characters.
7. **Looks up known vulnerabilities** (OSV) and evaluates dependencies.
8. **Shows the reach** — what the tool will be able to access once installed — and proposes least privilege (project scope, only the useful parts, no automatic permissions).
9. **Gives a verdict** (approved / approved with caveats / rejected) and **installs only after your "yes"**, from the already-verified files.
10. **Logs everything** — including what was *not* installed and why — in an inventory with the removal command.
11. **(Optional) Emails you** a summary, the caveats and the removal command.

Plus:
- 🔒 **Automatic guard** (hook): intercepts `npm install`, `npx`, `pip install`, `curl | bash`, `sudo`, `claude mcp add`, edits to skill folders and configuration files, and asks for approval.
- 🔄 **Update checker**: queries the sources of everything installed and warns when a new version has cleared quarantine. **It never installs anything by itself.**
- 🩹 **Preserved adjustments**: if you modify something third-party (e.g., remove automatic permissions), the change becomes a patch you can re-apply on the next update.

## What's in this repository

```
skill/crivo-skill/
  SKILL.md               ← the skill (the 11-step process) — Portuguese
  modelo-email.md        ← report email template — Portuguese
  scripts/varredura.sh   ← static scan (read-only)
skill-en/crivo-skill/
  SKILL.md               ← the skill in English (install one OR the other)
  email-template.md      ← report email template — English
  scripts/varredura.sh   ← same scan script
crivo/
  trava.py               ← hook that asks for approval for installs and sensitive edits
  verificar-atualizacoes.py  ← queries sources; warns at session start
  config.exemplo.json    ← ⚙️ what YOU need to configure (email, quarantine, language…)
  instalados.exemplo.json   ← inventory example
  registro.exemplo.md    ← log example
exemplos/
  settings.exemplo.json  ← blocks to merge into ~/.claude/settings.json
  npmrc.exemplo          ← hardened npm (no install scripts, with quarantine)
testes/
  rodar-testes.sh        ← tests the scan and the guard with samples
README.en.md · CONFIGURE.md · CONTRIBUTING.md · SECURITY.md   ← English docs
README.md · CONFIGURAR.md · CONTRIBUINDO.md · SEGURANCA.md    ← Portuguese docs
CHANGELOG.md
```

> File and folder names, configuration keys and the scripts' terminal messages are in Portuguese; the documentation and the skill are available in both languages with the same content.

## Installation

Consistent with the skill itself: **read before installing.** There are few files, all plain text.

```bash
git clone https://github.com/eggerproducoes/crivo-skill.git
cd crivo-skill
# read the files; then run the tests
bash testes/rodar-testes.sh
```

Then follow **[CONFIGURE.md](CONFIGURE.md)** — it lists every file to copy and **every value you must change** (email, paths, time limits).

Requirements: `bash`, `python3` (3.10+), `git`, `curl`. Optional: `gh` (authenticated GitHub CLI) so the update checker doesn't hit the anonymous rate limit.

## Lessons learned (why each rule exists)

Real cases found while using Crivo:
- A popular skill installed tools **globally and without confirmation** (`-g -y`) and sent the user's searches to telemetry that was on by default.
- A music plugin allowed `Bash` (any command) **without asking for permission** in 22 of its 53 skills.
- A reputable security plugin shipped hooks that **called the AI at the end of every response**, in every session — ongoing cost even without using the plugin.
- A repository named after a famous person **did not belong to them**, and had 221 thousand stars in 9 months.
- A marketing package released **6 versions on the same day**; the quarantine avoided all of them.
- "Do not track" variables set only in `.bashrc` **did not reach** the agent's commands.
- npm's quarantine (`min-release-age`) **does not apply to pnpm**, which needs its own setting.
- Skill scripts that run `npx`/`pip install` **internally** bypass guards that only look at the typed command.

## Limitations

- It's a skill: it depends on the agent following it. The guard (hook) reinforces it, but recognizes commands by text patterns — a heavily disguised command may slip through, and sometimes it warns needlessly.
- In modes that skip confirmations (e.g., "bypass permissions"), the approval prompt may not appear.
- The analysis is done by the agent itself: it greatly reduces risk, but **does not replace** a professional audit.
- The checker only runs when you open the agent.

## Contribute

Found an attack pattern the scan misses? An annoying false positive? A source type the checker doesn't know (PyPI, crates.io, Homebrew…)? See **[CONTRIBUTING.md](CONTRIBUTING.md)**. Vulnerabilities in Crivo itself: **[SECURITY.md](SECURITY.md)**. Contributions in Portuguese or English are welcome.

## License

[MIT](LICENSE).
