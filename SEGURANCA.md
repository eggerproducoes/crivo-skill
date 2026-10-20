🇧🇷 **Português** · 🇬🇧 [English](SECURITY.md)

# Política de segurança

O Crivo é uma ferramenta de segurança — falhas nele podem dar uma falsa sensação de proteção.

## Como relatar uma vulnerabilidade

**Não abra uma issue pública** para vulnerabilidades. Use o recurso **"Report a vulnerability"** (aba *Security* deste repositório, *Private vulnerability reporting*).

Inclua:
- o que acontece e o impacto (ex.: um padrão que faz a trava liberar uma instalação sem aprovação);
- passos para reproduzir, com exemplos **inofensivos**;
- versão/commit do Crivo e do agente usados.

## O que conta como vulnerabilidade

- Contornar a trava (`trava.py`) com um comando de instalação comum.
- Fazer o verificador ou a varredura **executar** conteúdo de terceiros.
- Fazer o Crivo enviar dados para fora (além do e-mail opcional ao próprio usuário).
- Instruções no `SKILL.md` que levem o agente a pular a aprovação do usuário.

Falsos negativos da varredura (um padrão que ela não detecta) normalmente são **melhorias**, não vulnerabilidades — abra uma issue normal com um exemplo inofensivo.

## Limites conhecidos

Veja a seção "Limitações" do README. O Crivo reduz riscos; não substitui auditoria profissional.
