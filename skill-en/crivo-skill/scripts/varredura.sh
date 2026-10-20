#!/usr/bin/env bash
# Crivo: varredura estática de uma pasta em quarentena.
# Só LÊ arquivos (grep/find). Nunca executa nada do alvo.
# Uso: bash varredura.sh <pasta>
set -u
ALVO="${1:?uso: varredura.sh <pasta>}"
[ -d "$ALVO" ] || { echo "pasta não encontrada: $ALVO"; exit 1; }

EXC=(--exclude-dir=.git --exclude-dir=node_modules)
MAX=15   # linhas exibidas por categoria

secao() { printf '\n== %s ==\n' "$1"; }
busca() { # $1 título, $2 regex (PCRE)
  local r; r=$(grep -rnIP "${EXC[@]}" -e "$2" "$ALVO" 2>/dev/null | sed "s|^$ALVO/||" | cut -c1-220)
  secao "$1"
  if [ -n "$r" ]; then
    echo "$r" | head -n $MAX
    local n; n=$(echo "$r" | wc -l); [ "$n" -gt $MAX ] && echo "... (+$((n-MAX)) linhas)"
  else echo "(nada)"; fi
}

secao "Arquivos"
echo "Total: $(find "$ALVO" -type f -not -path '*/.git/*' | wc -l) arquivos, $(du -sh "$ALVO" | cut -f1)"
find "$ALVO" -type f -not -path '*/.git/*' | sed "s|^$ALVO/||" | head -n 40

secao "Binários / executáveis"
find "$ALVO" -type f -not -path '*/.git/*' \( -perm -u+x -o -name '*.so' -o -name '*.node' -o -name '*.exe' -o -name '*.dll' -o -name '*.wasm' \) | sed "s|^$ALVO/||" | head -n $MAX
grep -rlP "${EXC[@]}" '^\x7fELF' "$ALVO" 2>/dev/null | sed "s|^$ALVO/|ELF: |" | head -n $MAX

busca "Scripts de instalação" '"(pre|post)?install"\s*:|setup\(|cmdclass|build\.rs|"prepare"\s*:'
busca "Rede (envio/download)" '\bcurl\b|\bwget\b|fetch\(|axios|https?\.request|XMLHttpRequest|WebSocket|/dev/tcp|\bnc\s+-|urllib|requests\.(get|post)|socket\.'
busca "Execução dinâmica" 'eval\(|new Function\(|child_process|execSync|spawn\(|subprocess|os\.system|\|\s*(ba|z)?sh\b|base64\s+-d|atob\(|Buffer\.from\([^)]*base64'
busca "Acesso a segredos" '(?<![A-Za-z0-9_])\.env\b(?!\.)|\.ssh|id_rsa|id_ed25519|\.aws|credentials|\.npmrc|\.netrc|\.git-credentials|keychain|bash_history|Cookies|Object\.(keys|entries)\(process\.env\)|JSON\.stringify\(process\.env\)|dict\(os\.environ\)|GITHUB_TOKEN|API_KEY|SECRET'
busca "Persistência / sistema" 'crontab|systemctl|\.bashrc|\.profile|\.zshrc|authorized_keys|/etc/|sudo\b|chmod\s+\+?[0-7]*s|\.claude/settings|hooks?\s*:'
busca "Manipulação do agente (prompt injection)" '(?i)ignore (all |the )?(previous|prior|above)|disregard|do not (tell|inform|mention|ask)|without (asking|confirmation|telling)|silently|secretly|não (informe|avise|pergunte)|sem (perguntar|avisar)|bypass|override (your|the) (rules|instructions)|you are now|system prompt'
busca "Ofuscação (hex/unicode escapes longos)" '(\\x[0-9a-fA-F]{2}){8,}|(\\u[0-9a-fA-F]{4}){8,}|[A-Za-z0-9+/]{200,}={0,2}'

secao "Caracteres Unicode invisíveis / bidirecionais"
grep -rnP "${EXC[@]}" '[\x{200B}-\x{200F}\x{202A}-\x{202E}\x{2060}-\x{2064}\x{FEFF}\x{E0000}-\x{E007F}]' "$ALVO" 2>/dev/null | sed "s|^$ALVO/||" | cut -c1-160 | head -n $MAX | grep . || echo "(nada)"

secao "Linhas muito longas (possível código minificado/ofuscado)"
grep -rlIP "${EXC[@]}" '^.{1000,}$' "$ALVO" 2>/dev/null | sed "s|^$ALVO/||" | head -n $MAX

secao "Domínios citados"
grep -rhoIP "${EXC[@]}" 'https?://[A-Za-z0-9.-]+' "$ALVO" 2>/dev/null | sed -E 's|https?://||' | sort | uniq -c | sort -rn | head -n 30

printf '\nVarredura concluída. Isto aponta onde olhar; a leitura humana/do agente continua obrigatória.\n'
