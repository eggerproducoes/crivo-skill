# Changelog

## Não lançado

## v1.0.0 — 2026-10-20
Primeira versão pública.
- Skill `crivo-skill`: processo em 11 etapas (origem, quarentena, isolamento, integridade, análise estática, vulnerabilidades, menor privilégio, veredito, instalação endurecida, registro, e-mail opcional).
- Riscos específicos de agentes: `allowed-tools` com permissões automáticas, hooks invasivos ou caros, servidores MCP, gatilhos amplos, propaganda embutida.
- `varredura.sh`: varredura estática somente leitura.
- `trava.py`: hook PreToolUse que pede aprovação para instalações e edições sensíveis.
- `verificar-atualizacoes.py`: verificador de atualizações com quarentena (Node, GitHub releases/tags/pastas, npm + OSV).
- `config.json`: configuração centralizada (e-mail, quarentena, idioma, escopo).
- Testes com amostras inofensivas.
