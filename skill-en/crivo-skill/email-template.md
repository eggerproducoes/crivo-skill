# Crivo report email template

Send it as HTML (`htmlBody`) together with a plain-text version (`body`, no Markdown).
Replace everything between `{{ }}`. Keep the language plain.

Subject: `[Crivo] {{Type}} installed: {{name}} — {{yyyy-mm-dd}}`

```html
<div style="font-family:Arial,sans-serif;max-width:680px;color:#222;line-height:1.5">
  <h2 style="margin-bottom:4px">🛡️ Crivo — {{type}} installed: {{name}}</h2>
  <p style="color:#666;margin-top:0">{{weekday}}, {{yyyy-mm-dd}} · Scope: {{global/project}} · Verdict: <b>{{verdict}}</b></p>

  <h3>Why we installed it</h3>
  <p>{{reason}}</p>

  <h3>What it does</h3>
  <p>{{summary of what it does}}</p>

  <h3>How Crivo checked it</h3>
  <table style="border-collapse:collapse;width:100%">
    <tr style="background:#f2f2f2"><th style="text-align:left;padding:6px;border:1px solid #ddd">Step</th><th style="text-align:left;padding:6px;border:1px solid #ddd">Result</th></tr>
    <!-- one row per step: Provenance, Version, Integrity, Scan, Scripts/Permissions, Dependencies -->
    <tr><td style="padding:6px;border:1px solid #ddd">{{step}}</td><td style="padding:6px;border:1px solid #ddd">{{result}}</td></tr>
  </table>

  <h3>Adjustments made</h3>
  <!-- e.g.: removed automatic Bash, removed hooks, only N of M skills. If none, write "None". -->
  <ul>
    <li>{{adjustment}}</li>
  </ul>

  <h3>Caveats</h3>
  <ol>
    <li>{{caveat}}</li>
  </ol>

  <h3>How to remove it</h3>
  <pre style="background:#f6f6f6;padding:10px;border-radius:4px">{{removal command}}</pre>

  <h3>Log data</h3>
  <ul>
    <li>Source: {{url}}</li>
    <li>Version/commit: {{commit}}</li>
    <li>SHA-256 hash of the installed folder: {{hash}}</li>
    <li>Path: {{path}}</li>
  </ul>
  <p style="color:#888;font-size:12px">Sent automatically by the Crivo skill. Full log at ~/.claude/crivo/registro.md</p>
</div>
```
