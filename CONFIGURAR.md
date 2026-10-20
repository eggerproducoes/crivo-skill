# Configurar o Crivo

Tudo o que você precisa **copiar** e **trocar**. Os itens marcados com ✏️ têm valores pessoais.

> Antes: leia os arquivos do repositório e rode `bash testes/rodar-testes.sh`.

## 1. Copiar os arquivos

```bash
# a skill
mkdir -p ~/.claude/skills
cp -r skill/crivo-skill ~/.claude/skills/crivo-skill

# os scripts e a pasta de dados do Crivo
mkdir -p ~/.claude/crivo/ajustes ~/.claude/crivo/plugins ~/.claude/crivo/emails-pendentes
cp crivo/trava.py crivo/verificar-atualizacoes.py ~/.claude/crivo/
cp crivo/config.exemplo.json ~/.claude/crivo/config.json
cp crivo/instalados.exemplo.json ~/.claude/crivo/instalados.json
cp crivo/registro.exemplo.md ~/.claude/crivo/registro.md
```

Se você usa outro local para skills (ex.: só num projeto: `.claude/skills/`), ajuste o caminho do script de varredura citado no `SKILL.md` (Etapa 5) e o do modelo de e-mail (Etapa 11).

## 2. ✏️ `~/.claude/crivo/config.json` — o principal

| Campo | O que é | Troque? |
|---|---|---|
| `email.ativo` | Liga o e-mail de registro após cada instalação | ✏️ `true` se tiver conector de e-mail |
| `email.destino` | **Seu** e-mail. O Crivo nunca envia para outro endereço | ✏️ **obrigatório** se ativar |
| `email.conector` | Nome do conector de e-mail do seu agente (ex.: `gmail`) | ✏️ se usar outro |
| `idioma` | Idioma dos relatórios (ex.: `pt-BR`, `en`) | ✏️ se quiser |
| `quarentena_dias` | Idade mínima de uma versão para instalar | opcional (padrão 7) |
| `quarentena_critico_dias` | Idem para ferramentas críticas | opcional (padrão 14) |
| `verificar_a_cada_horas` | Frequência do verificador de atualizações | opcional (padrão 24) |
| `escopo_padrao` | `projeto` ou `global` | opcional |

## 3. ✏️ `~/.claude/settings.json` — hooks, telemetria e permissões

Abra `exemplos/settings.exemplo.json` e **mescle** os blocos no seu `~/.claude/settings.json` (não substitua o arquivo inteiro; junte as listas `hooks`, `permissions.deny`, `permissions.ask` e o bloco `env` com o que você já tem).

- **`hooks.PreToolUse`** → a trava. Usa `"$HOME/.claude/crivo/trava.py"`; se você copiou para outro lugar, ✏️ troque o caminho.
- **`hooks.SessionStart`** → o verificador de atualizações (1x por intervalo). Mesmo cuidado com o caminho.
- **`env`** → desliga telemetria de ferramentas que respeitam essas variáveis. Coloque aqui, não só no `.bashrc` (o `.bashrc` não chega aos comandos do agente).
- **`permissions`** → travas para quem conecta o GitHub ao agente (bloqueia apagar repositório, `push --force`, ler o token; pede aprovação para `push`, PRs, releases etc.). Remova o que não se aplica a você.
- `"onFailure": "block"` na trava: se o script falhar, ela **bloqueia** em vez de liberar. Se preferir o contrário, troque para `"continue"`.

Para validar o JSON depois de editar:
```bash
python3 -c "import json,os; json.load(open(os.path.expanduser('~/.claude/settings.json'))); print('ok')"
```
Abra `/hooks` no Claude Code para conferir que os hooks foram carregados.

## 4. Gerenciadores de pacotes (recomendado)

- **npm**: mescle `exemplos/npmrc.exemplo` no seu `~/.npmrc`. `min-release-age` exige npm 11.10+. A linha `prefix=${HOME}/.local` faz instalações globais ficarem no seu usuário — ✏️ remova se você usa outro esquema (nvm, Volta…).
- **pnpm** (não lê a quarentena do npm):
  ```bash
  pnpm config set minimum-release-age 10080 --global   # 7 dias, em minutos
  pnpm config set ignore-scripts true --global
  ```
- **pip**: use ambientes virtuais; considere `--require-hashes`.

## 5. Inventário

Abra `~/.claude/crivo/instalados.json` e **apague os exemplos** (ou troque pelo que você já tem instalado). O agente acrescenta itens a cada instalação. Tipos suportados pelo verificador: `node`, `github-release`, `github-tag`, `github-pasta` (com `pasta` ou `pastas`), `npm`.

## 6. Ajustes finos (opcional)

- **Trava** (`trava.py`): listas `COMANDOS` e `ARQUIVOS`. Inclua comandos do seu ecossistema (ex.: `composer require`, `gem install`) ou remova os que geram aviso demais.
- **Varredura** (`varredura.sh`): expressões de cada categoria; ajuste se aparecerem falsos positivos frequentes na sua área.
- **Mensagens do verificador**: o texto do aviso de início de sessão está em `verificar-atualizacoes.py` (função `main`).

## 7. Testar

```bash
bash testes/rodar-testes.sh          # no repositório
python3 -I ~/.claude/crivo/verificar-atualizacoes.py   # relatório completo agora
```

Depois reinicie o agente e peça: *"instale a skill X"* — ele deve aplicar o crivo antes de qualquer coisa.
