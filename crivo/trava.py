#!/usr/bin/env python3
"""Trava do Crivo (hook PreToolUse do Claude Code).

Intercepta instalações/atualizações de código de terceiros e alterações em
arquivos sensíveis. Nesses casos pede aprovação do usuário e lembra o agente
de aplicar a crivo-skill. Qualquer outra coisa passa sem interferência.
"""
import json
import re
import sys

COMANDOS = [
    (r"\bnpm\s+(install|i|add|ci|update|up|upgrade|exec|x|rebuild)\b", "npm"),
    (r"\bnpx\b|\bbunx\b|\buvx\b", "execução direta de pacote"),
    (r"\bpnpm\s+(add|install|i|update|up|dlx|create|exec)\b", "pnpm"),
    (r"\b(init|bundle)-artifact\.sh\b", "script da web-artifacts-builder (baixa pacotes do npm)"),
    (r"\byarn\s+(add|install|up|upgrade|dlx)\b", "yarn"),
    (r"\bbun\s+(add|install|i|x)\b", "bun"),
    (r"\bpip3?\s+install\b|\bpython3?\s+-m\s+pip\s+install\b", "pip"),
    (r"\bpipx\s+(install|run)\b|\buv\s+(pip\s+install|add|tool\s+install)\b", "pipx/uv"),
    (r"\b(curl|wget)\b[^|;&]*\|\s*(sudo\s+)?(ba|z|da)?sh\b", "script baixado executado direto"),
    (r"\b(ba|z)?sh\s+<\(\s*(curl|wget)", "script baixado executado direto"),
    (r"\bapt(-get)?\s+install\b|\bdpkg\s+-i\b|\bsnap\s+install\b|\bflatpak\s+install\b", "pacote do sistema"),
    (r"\b(cargo|go|gem)\s+install\b|\bbrew\s+install\b", "instalador de linguagem"),
    (r"\bclaude\s+(mcp\s+add|plugin\s+(install|marketplace\s+add))\b", "MCP/plugin do Claude"),
    (r"\bgh\s+extension\s+install\b", "extensão do gh"),
    (r"\bdocker\s+(pull|run)\b|\bpodman\s+(pull|run)\b", "imagem de container"),
    (r"\.claude/(skills|agents|commands|plugins)\b", "pasta de skills/agentes do Claude"),
    (r"\bsudo\b", "comando com sudo"),
    (r"\.claude/settings(\.local)?\.json|\.mcp\.json|\.npmrc|\.bashrc|\.profile|\.zshrc|\.claude/crivo/",
     "comando que mexe em configuração sensível"),
]

ARQUIVOS = [
    (r"/\.claude/(skills|agents|commands|plugins)/", "skill/agente/plugin do Claude"),
    (r"(^|/)\.mcp\.json$", "configuração de MCP"),
    (r"/\.claude/settings(\.local)?\.json$", "configurações do Claude Code"),
    (r"(^|/)\.(npmrc|bashrc|profile|zshrc)$", "configuração de shell/npm"),
    (r"/\.claude/crivo/", "arquivos do próprio Crivo"),
]


def main():
    try:
        dados = json.load(sys.stdin)
    except Exception:
        return
    ferramenta = dados.get("tool_name", "")
    entrada = dados.get("tool_input", {}) or {}

    motivo = None
    if ferramenta == "Bash":
        cmd = entrada.get("command", "")
        for padrao, nome in COMANDOS:
            if re.search(padrao, cmd):
                motivo = f"instalação/execução de terceiros ({nome})"
                break
    elif ferramenta in ("Write", "Edit", "NotebookEdit"):
        caminho = entrada.get("file_path", "") or entrada.get("notebook_path", "")
        for padrao, nome in ARQUIVOS:
            if re.search(padrao, caminho):
                motivo = f"alteração em arquivo sensível ({nome})"
                break

    if not motivo:
        return

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": (
                f"Crivo: {motivo}. Só aprove se o crivo de segurança já foi "
                "aplicado e você concorda com o veredito."
            ),
            "additionalContext": (
                f"Trava do Crivo acionada: {motivo}. Antes de prosseguir, aplique a "
                "skill crivo-skill (origem, quarentena de versão, integridade, varredura, "
                "permissões, veredito) e obtenha aprovação explícita do usuário. "
                "Se for parte de um crivo já aprovado, explique isso ao usuário."
            ),
        }
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
