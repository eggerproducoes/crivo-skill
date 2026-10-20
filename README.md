# Crivo 🛡️ — segurança antes de instalar qualquer coisa no seu agente

**Crivo** é uma skill para o [Claude Code](https://code.claude.com) (e agentes compatíveis com skills) que obriga o agente a **verificar a segurança de tudo o que for instalado** — skills, plugins, servidores MCP, pacotes npm/pip, binários, scripts `curl | bash` — **antes** de instalar, e só com a sua aprovação.

Ela nasceu de uma necessidade prática: instalar uma skill de terceiro é dar ao agente instruções (e às vezes código) escritas por outra pessoa, que rodam **com as suas permissões** — seus arquivos, suas chaves, seu e-mail, seus deploys. Popularidade não é garantia: estrelas podem ser infladas, nomes podem ser imitados, e uma versão publicada ontem pode ser a versão comprometida.

> 🇬🇧 **English summary** at the end.

## O que o Crivo faz

1. **Identifica** o que vai ser instalado e se você realmente precisa (inclusive se o agente já tem algo equivalente embutido).
2. **Verifica origem e reputação** — dono real, nome imitado, popularidade anômala, troca de mantenedor.
3. **Aplica quarentena de versão** — usa a versão mais nova que já tem pelo menos 7 dias (14 para ferramentas críticas). Pacotes maliciosos costumam ser descobertos nesse prazo.
4. **Baixa numa pasta isolada, sem executar nada.**
5. **Confere integridade** — assinaturas, procedência (SLSA), checksums de duas fontes.
6. **Faz análise estática** — script de varredura + leitura de verdade: rede, telemetria, segredos, execução escondida, persistência, e os riscos próprios de agentes:
   - `allowed-tools` que liberam comandos **sem pedir permissão**;
   - hooks que leem cada mensagem sua ou que **chamam a IA a cada resposta** (custo contínuo);
   - servidores MCP e suas credenciais;
   - instruções manipuladoras e caracteres invisíveis.
7. **Consulta vulnerabilidades conhecidas** (OSV) e avalia dependências.
8. **Mostra o alcance** — o que a ferramenta poderá acessar depois de instalada — e propõe o menor privilégio (escopo de projeto, só as partes úteis, sem permissões automáticas).
9. **Dá um veredito** (aprovado / com ressalvas / reprovado) e **só instala com o seu "sim"**, a partir dos arquivos já verificados.
10. **Registra tudo** — inclusive o que *não* foi instalado e por quê — num inventário com o comando de remoção.
11. **(Opcional) Envia um e-mail** para você com o resumo, as ressalvas e o comando para remover.

E mais:
- 🔒 **Trava automática** (hook): intercepta `npm install`, `npx`, `pip install`, `curl | bash`, `sudo`, `claude mcp add`, edições em pastas de skills e arquivos de configuração, e pede aprovação.
- 🔄 **Verificador de atualizações**: consulta as fontes de tudo que está instalado e avisa quando uma versão nova já passou da quarentena. **Nunca instala sozinho.**
- 🩹 **Ajustes preservados**: se você modificar algo de terceiros (ex.: tirar permissões automáticas), o ajuste vira um patch reaplicável na próxima atualização.

## O que tem neste repositório

```
skill/crivo-skill/
  SKILL.md               ← a skill (o processo em 11 etapas)
  modelo-email.md        ← modelo do e-mail de registro
  scripts/varredura.sh   ← varredura estática (só lê arquivos)
crivo/
  trava.py               ← hook que pede aprovação para instalações e edições sensíveis
  verificar-atualizacoes.py  ← consulta fontes; avisa no início da sessão
  config.exemplo.json    ← ⚙️ o que VOCÊ precisa configurar (e-mail, quarentena, idioma…)
  instalados.exemplo.json
  registro.exemplo.md
exemplos/
  settings.exemplo.json  ← blocos para mesclar no ~/.claude/settings.json
  npmrc.exemplo          ← npm endurecido (sem scripts de instalação, com quarentena)
testes/
  rodar-testes.sh        ← testa varredura e trava com amostras
CONFIGURAR.md            ← passo a passo do que trocar
CONTRIBUINDO.md · SEGURANCA.md · CHANGELOG.md
```

## Instalação

Coerente com a própria skill: **leia antes de instalar.** São poucos arquivos, todos em texto.

```bash
git clone https://github.com/eggerproducoes/crivo-skill.git
cd crivo-skill
# leia os arquivos; depois rode os testes
bash testes/rodar-testes.sh
```

Depois siga **[CONFIGURAR.md](CONFIGURAR.md)** — ele lista cada arquivo a copiar e **cada valor que você deve trocar** (e-mail, caminhos, prazos).

Requisitos: `bash`, `python3` (3.10+), `git`, `curl`. Opcional: `gh` (GitHub CLI autenticado) para o verificador de atualizações não esbarrar no limite de consultas anônimas.

## Lições aprendidas (por que cada regra existe)

Casos reais encontrados ao usar o Crivo:
- Uma skill popular instalava ferramentas **globalmente e sem confirmação** (`-g -y`) e enviava as buscas do usuário para telemetria ligada por padrão.
- Um plugin de música liberava `Bash` (qualquer comando) **sem pedir permissão** em 22 das suas 53 skills.
- Um plugin de segurança respeitável trazia hooks que **chamavam a IA ao fim de toda resposta**, em todas as sessões — custo contínuo mesmo sem usar o plugin.
- Um repositório com o nome de uma pessoa famosa **não era dela**, e tinha 221 mil estrelas em 9 meses.
- Um pacote de marketing lançou **6 versões no mesmo dia**; a quarentena evitou todas.
- Variáveis de "não rastrear" colocadas só no `.bashrc` **não chegavam** aos comandos do agente.
- A quarentena do npm (`min-release-age`) **não vale para o pnpm**, que precisa de configuração própria.
- Scripts de skills que rodam `npx`/`pip install` **por dentro** escapam de travas que olham só o comando digitado.

## Limitações

- É uma skill: depende de o agente segui-la. A trava (hook) reforça, mas reconhece comandos por padrões de texto — um comando muito disfarçado pode escapar, e às vezes ela avisa à toa.
- Em modos que pulam confirmações (ex.: "bypass permissions"), o pedido de aprovação pode não aparecer.
- A análise é feita pelo próprio agente: reduz muito o risco, mas **não substitui** uma auditoria profissional.
- O verificador só roda quando você abre o agente.

## Contribua

Achou um padrão de ataque que a varredura não pega? Um falso positivo chato? Um tipo de fonte que o verificador não conhece (PyPI, crates.io, Homebrew…)? Veja **[CONTRIBUINDO.md](CONTRIBUINDO.md)**. Vulnerabilidades no próprio Crivo: **[SEGURANCA.md](SEGURANCA.md)**.

## Licença

[MIT](LICENSE).

---

## 🇬🇧 English summary

**Crivo** ("sieve" in Portuguese) is a Claude Code skill that makes the agent **security-vet anything before installing it** — skills, plugins, MCP servers, npm/pip packages, binaries, `curl | bash` scripts — and install only with your explicit approval. It checks provenance and reputation (impersonation, inflated stars), enforces a **version quarantine** (7 days; 14 for critical tools), downloads into an isolated folder without executing anything, verifies integrity (signatures/SLSA provenance/two-source checksums), runs a static scan plus a real read-through (network, telemetry, secrets, hidden installs, persistence, agent-specific risks such as `allowed-tools` auto-approvals and costly or invasive hooks), checks OSV advisories, proposes least privilege, gives a verdict, logs everything with an uninstall command, and can email you a report. A PreToolUse hook enforces approval for install commands, and an update checker warns when new versions clear quarantine (it never auto-installs). Documentation is in Portuguese; contributions in English are welcome.
