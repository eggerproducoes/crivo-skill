# Modelo do e-mail de registro do Crivo

Envie em HTML (`htmlBody`) e com uma versão em texto simples (`body`, sem Markdown).
Substitua tudo que está entre `{{ }}`. Mantenha o português simples.

Assunto: `[Crivo] {{Tipo}} instalado(a): {{nome}} — {{dd/mm/aaaa}}`

```html
<div style="font-family:Arial,sans-serif;max-width:680px;color:#222;line-height:1.5">
  <h2 style="margin-bottom:4px">🛡️ Crivo — {{tipo}} instalado(a): {{nome}}</h2>
  <p style="color:#666;margin-top:0">{{dia da semana}}, {{dd/mm/aaaa}} · Escopo: {{global/projeto}} · Veredito: <b>{{veredito}}</b></p>

  <h3>Por que instalamos</h3>
  <p>{{motivo}}</p>

  <h3>O que ela faz</h3>
  <p>{{resumo do que a skill faz}}</p>

  <h3>Como o crivo verificou</h3>
  <table style="border-collapse:collapse;width:100%">
    <tr style="background:#f2f2f2"><th style="text-align:left;padding:6px;border:1px solid #ddd">Etapa</th><th style="text-align:left;padding:6px;border:1px solid #ddd">Resultado</th></tr>
    <!-- uma linha por etapa: Origem, Versão, Integridade, Varredura, Scripts/Permissões, Dependências -->
    <tr><td style="padding:6px;border:1px solid #ddd">{{etapa}}</td><td style="padding:6px;border:1px solid #ddd">{{resultado}}</td></tr>
  </table>

  <h3>Ajustes feitos</h3>
  <!-- ex.: removido Bash automático, retirados hooks, só N de M skills. Se não houve ajustes, escreva "Nenhum". -->
  <ul>
    <li>{{ajuste}}</li>
  </ul>

  <h3>Ressalvas</h3>
  <ol>
    <li>{{ressalva}}</li>
  </ol>

  <h3>Como remover</h3>
  <pre style="background:#f6f6f6;padding:10px;border-radius:4px">{{comando de remoção}}</pre>

  <h3>Dados do registro</h3>
  <ul>
    <li>Origem: {{url}}</li>
    <li>Versão/commit: {{commit}}</li>
    <li>Hash SHA-256 da pasta instalada: {{hash}}</li>
    <li>Caminho: {{caminho}}</li>
  </ul>
  <p style="color:#888;font-size:12px">Enviado automaticamente pela Crivo-Skill. Registro completo em ~/.claude/crivo/registro.md</p>
</div>
```
