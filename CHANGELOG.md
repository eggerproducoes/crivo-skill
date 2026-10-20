# Changelog

🇧🇷 Português · 🇬🇧 English (cada entrada nas duas línguas / each entry in both languages)

## Não lançado / Unreleased

## v1.1.0 — 2026-10-20
- 🇧🇷 Publicação completa em inglês com o mesmo teor do português: `README.en.md`, `CONFIGURE.md`, `CONTRIBUTING.md`, `SECURITY.md` e a skill em `skill-en/`. Seletor de idioma no topo de cada documento. Modelo de e-mail ganhou a seção "Ajustes feitos".
- 🇬🇧 Full English publication with the same content as the Portuguese: `README.en.md`, `CONFIGURE.md`, `CONTRIBUTING.md`, `SECURITY.md` and the skill in `skill-en/`. Language switcher at the top of each document. The email template gained an "Adjustments made" section.

## v1.0.0 — 2026-10-20
- 🇬🇧 First public release (Portuguese only). Details below.

Primeira versão pública.
- Skill `crivo-skill`: processo em 11 etapas (origem, quarentena, isolamento, integridade, análise estática, vulnerabilidades, menor privilégio, veredito, instalação endurecida, registro, e-mail opcional).
- Riscos específicos de agentes: `allowed-tools` com permissões automáticas, hooks invasivos ou caros, servidores MCP, gatilhos amplos, propaganda embutida.
- `varredura.sh`: varredura estática somente leitura.
- `trava.py`: hook PreToolUse que pede aprovação para instalações e edições sensíveis.
- `verificar-atualizacoes.py`: verificador de atualizações com quarentena (Node, GitHub releases/tags/pastas, npm + OSV).
- `config.json`: configuração centralizada (e-mail, quarentena, idioma, escopo).
- Testes com amostras inofensivas.
