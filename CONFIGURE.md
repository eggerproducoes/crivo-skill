🇧🇷 [Português](CONFIGURAR.md) · 🇬🇧 **English**

# Configuring Crivo

Everything you need to **copy** and **change**. Items marked ✏️ hold personal values.

> First: read the repository files and run `bash testes/rodar-testes.sh`.

## 1. Copy the files

```bash
# the skill — choose ONE language
mkdir -p ~/.claude/skills
cp -r skill-en/crivo-skill ~/.claude/skills/crivo-skill     # English
# or: cp -r skill/crivo-skill ~/.claude/skills/crivo-skill  # Portuguese

# Crivo's scripts and data folder
mkdir -p ~/.claude/crivo/ajustes ~/.claude/crivo/plugins ~/.claude/crivo/emails-pendentes
cp crivo/trava.py crivo/verificar-atualizacoes.py ~/.claude/crivo/
cp crivo/config.exemplo.json ~/.claude/crivo/config.json
cp crivo/instalados.exemplo.json ~/.claude/crivo/instalados.json
cp crivo/registro.exemplo.md ~/.claude/crivo/registro.md
```

If you keep skills somewhere else (e.g., only in one project: `.claude/skills/`), adjust the path to the scan script mentioned in `SKILL.md` (Step 5) and to the email template (Step 11).

## 2. ✏️ `~/.claude/crivo/config.json` — the main file

| Key | What it is | Change it? |
|---|---|---|
| `email.ativo` | Turns on the report email after each installation | ✏️ `true` if you have an email connector |
| `email.destino` | **Your** email address. Crivo never sends to any other address | ✏️ **required** if enabled |
| `email.conector` | Name of your agent's email connector (e.g., `gmail`) | ✏️ if you use another one |
| `idioma` | Language of the reports (e.g., `pt-BR`, `en`) | ✏️ use `en` for English |
| `quarentena_dias` | Minimum age of a version before installing | optional (default 7) |
| `quarentena_critico_dias` | Same, for critical tools | optional (default 14) |
| `verificar_a_cada_horas` | How often the update checker runs | optional (default 24) |
| `escopo_padrao` | `projeto` (project) or `global` | optional |

## 3. ✏️ `~/.claude/settings.json` — hooks, telemetry and permissions

Open `exemplos/settings.exemplo.json` and **merge** its blocks into your `~/.claude/settings.json` (do not replace the whole file; combine the `hooks`, `permissions.deny`, `permissions.ask` lists and the `env` block with what you already have).

- **`hooks.PreToolUse`** → the guard. It uses `"$HOME/.claude/crivo/trava.py"`; if you copied it elsewhere, ✏️ change the path.
- **`hooks.SessionStart`** → the update checker (once per interval). Same note about the path.
- **`env`** → turns off telemetry for tools that honor these variables. Put them here, not only in `.bashrc` (`.bashrc` does not reach the agent's commands).
- **`permissions`** → guards for anyone who connects GitHub to the agent (blocks deleting repositories, `push --force` and reading the token; asks for approval for `push`, PRs, releases, etc.). Remove what doesn't apply to you.
- `"onFailure": "block"` on the guard: if the script fails, it **blocks** instead of allowing. If you prefer the opposite, change it to `"continue"`.

To validate the JSON after editing:
```bash
python3 -c "import json,os; json.load(open(os.path.expanduser('~/.claude/settings.json'))); print('ok')"
```
Open `/hooks` in Claude Code to confirm the hooks were loaded.

## 4. Package managers (recommended)

- **npm**: merge `exemplos/npmrc.exemplo` into your `~/.npmrc`. `min-release-age` requires npm 11.10+. The line `prefix=${HOME}/.local` keeps global installs in your user folder — ✏️ remove it if you use another setup (nvm, Volta…).
- **pnpm** (does not read npm's quarantine):
  ```bash
  pnpm config set minimum-release-age 10080 --global   # 7 days, in minutes
  pnpm config set ignore-scripts true --global
  ```
- **pip**: use virtual environments; consider `--require-hashes`.

## 5. Inventory

Open `~/.claude/crivo/instalados.json` and **delete the examples** (or replace them with what you already have installed). The agent adds items on each installation. Types supported by the checker: `node`, `github-release`, `github-tag`, `github-pasta` (with `pasta` or `pastas`), `npm`.

## 6. Fine-tuning (optional)

- **Guard** (`trava.py`): the `COMANDOS` and `ARQUIVOS` lists. Add commands from your ecosystem (e.g., `composer require`, `gem install`) or remove the ones that warn too often.
- **Scan** (`varredura.sh`): the expressions for each category; adjust them if frequent false positives show up in your field.
- **Checker messages**: the session-start warning text is in `verificar-atualizacoes.py` (function `main`).

## 7. Test

```bash
bash testes/rodar-testes.sh          # in the repository
python3 -I ~/.claude/crivo/verificar-atualizacoes.py   # full report now
```

Then restart the agent and ask: *"install skill X"* — it should apply the Crivo before anything else.
