# Contribuindo com o Crivo

Obrigado por querer melhorar o Crivo! A ideia é juntar o que cada um aprende ao examinar skills, plugins e pacotes, para todo mundo instalar com mais segurança.

## Formas de contribuir

- **Novo padrão de risco** — algo que você encontrou e a varredura não pegou (ex.: um jeito novo de esconder telemetria, um campo de manifesto perigoso). Abra uma *issue* com um exemplo **inofensivo** que reproduza o padrão.
- **Falso positivo** — algo marcado como suspeito que é comum e legítimo. Descreva o contexto.
- **Lição aprendida** — um caso real (sem expor pessoas) que justifique uma regra nova no `SKILL.md`.
- **Novas fontes no verificador** — PyPI, crates.io, Homebrew, Docker Hub, extensões de editor…
- **Novos padrões na trava** — comandos de instalação de outros ecossistemas.
- **Tradução** — o projeto é em português; versões em outros idiomas são bem-vindas.

## Como enviar uma mudança

1. Faça um fork e crie uma branch.
2. Altere o que precisar. Se mexer na varredura ou na trava, **adicione um caso em `testes/`** (amostra inofensiva e/ou comando no `rodar-testes.sh`).
3. Rode `bash testes/rodar-testes.sh` — tudo precisa passar.
4. Atualize o `CHANGELOG.md` (seção "Não lançado").
5. Abra um *pull request* explicando **o risco que a mudança cobre** e **como foi testada**.

## Regras importantes

- **Amostras de teste são texto inofensivo.** Nada de código malicioso funcional, links para malware real, ou instruções que causem dano se executadas. Use domínios `.invalid`/`example.com`.
- **Nada de dados pessoais**: e-mails, caminhos com nome de usuário, tokens, nomes de repositórios privados.
- **A skill e os scripts não podem ganhar dependências externas** (só `bash`, `python3` da biblioteca padrão, `git`, `curl`; `gh` opcional). O Crivo precisa ser auditável lendo poucos arquivos.
- **Os scripts só leem e consultam.** Nada no Crivo deve instalar, baixar e executar, ou enviar dados para terceiros (exceto o e-mail opcional, para o próprio usuário).
- Mudanças no comportamento do agente (texto do `SKILL.md`) devem explicar o **porquê** — de preferência com um caso real.

## Estilo

- Português simples, frases curtas. Termos técnicos com explicação breve na primeira vez.
- Scripts: comentários curtos dizendo o que e por quê.

## Dúvidas

Abra uma *issue* com a etiqueta `pergunta`.
