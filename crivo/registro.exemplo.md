# Registro do Crivo

Tudo o que passou pelo crivo — instalado ou não. Copie para `~/.claude/crivo/registro.md`.

## Instalados
| Data | Nome | Versão / commit | Tipo | Fonte | SHA-256 / hash | Escopo / caminho | Integridade | Veredito, ressalvas e ajustes | Desinstalar |
|---|---|---|---|---|---|---|---|---|---|
| 2026-01-01 | exemplo-skill | v1.2.3 = abc123… (lançada 2025-12-20, 12 dias) | skill | github.com/dono/repo | hash da pasta | global: ~/.claude/skills/exemplo-skill | tag fixada + hash conferido | APROVADO COM RESSALVAS: … | `rm -rf ~/.claude/skills/exemplo-skill` |

## Analisados e NÃO instalados
| Data | Nome | Motivo |
|---|---|---|
| 2026-01-01 | dono/outro-repo | Libera Bash sem pedir em 20 skills; autor sem histórico. |

## Configurações de proteção aplicadas
- `~/.npmrc`: …
- `settings.json` (env, hooks, permissões): …

## E-mails de registro enviados
| Data | Item | Status | ID da mensagem |
|---|---|---|---|
