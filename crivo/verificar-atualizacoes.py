#!/usr/bin/env python3
"""Verificador de atualizações do Crivo.

Só CONSULTA as fontes (GitHub, npm, nodejs.org) e compara com ~/.claude/crivo/instalados.json.
Nunca baixa nem instala nada. Atualizar é sempre um novo crivo, com aprovação do usuário.

Uso:
  python3 verificar-atualizacoes.py          relatório completo agora
  python3 verificar-atualizacoes.py --hook   modo SessionStart: no máximo 1 consulta por intervalo (config.json);
                                             avisa o agente/usuário só se houver novidade
"""
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.request

BASE = os.path.expanduser("~/.claude/crivo")
INV = os.path.join(BASE, "instalados.json")
CACHE = os.path.join(BASE, "ultima-verificacao.json")
CONFIG = os.path.join(BASE, "config.json")
AGORA = dt.datetime.now(dt.timezone.utc)


def _config():
    try:
        return json.load(open(CONFIG))
    except Exception:
        return {}


_CFG = _config()
QUARENTENA = int(_CFG.get("quarentena_dias", 7))                   # dias
QUARENTENA_CRITICO = int(_CFG.get("quarentena_critico_dias", 14))  # dias
INTERVALO_HORAS = float(_CFG.get("verificar_a_cada_horas", 24))


def data(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def http_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "crivo-verificador"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


def gh(endpoint):
    """Consulta a API do GitHub pelo gh (autenticado); cai para HTTP anônimo se precisar."""
    try:
        out = subprocess.run(["gh", "api", endpoint], capture_output=True, text=True, timeout=20)
        if out.returncode == 0:
            return json.loads(out.stdout)
    except Exception:
        pass
    return http_json("https://api.github.com/" + endpoint)


def verificar(item):
    t = item["tipo"]
    if t == "node":
        idx = http_json("https://nodejs.org/dist/index.json")
        linha = [r for r in idx if r["version"].startswith("v" + item["linha"] + ".")]
        novo = linha[0]
        seg = [r["version"] for r in linha if r.get("security") and r["version"] != item["versao"]
               and data(r["date"] + "T00:00:00Z") > data(next(x["date"] for x in linha if x["version"] == item["versao"]) + "T00:00:00Z")]
        return novo["version"], novo["date"] + "T00:00:00Z", (("correção de segurança em: " + ", ".join(seg)) if seg else "")
    if t == "github-release":
        r = gh(f"repos/{item['repo']}/releases/latest")
        return r["tag_name"], r["published_at"], ""
    if t == "github-tag":
        tags = gh(f"repos/{item['repo']}/tags?per_page=1")
        tag = tags[0]["name"]
        c = gh(f"repos/{item['repo']}/commits/{tags[0]['commit']['sha']}")
        return tag, c["commit"]["committer"]["date"], ""
    if t == "github-pasta":
        # "pastas" (lista) acompanha só as pastas que instalamos; vale a mudança mais recente entre elas
        melhor = None
        for pasta in item.get("pastas") or [item["pasta"]]:
            cs = gh(f"repos/{item['repo']}/commits?path={pasta}&per_page=1")
            if cs and (melhor is None or cs[0]["commit"]["committer"]["date"] > melhor[0]["commit"]["committer"]["date"]):
                melhor = cs
        sha = melhor[0]["sha"]
        msg = melhor[0]["commit"]["message"].splitlines()[0][:90]
        return sha, melhor[0]["commit"]["committer"]["date"], msg
    if t == "npm":
        d = http_json(f"https://registry.npmjs.org/{item['pacote']}")
        vs = [v for v in d["time"] if v.startswith(item["linha"] + ".") and "-" not in v]
        vs.sort(key=lambda v: d["time"][v], reverse=True)
        extra = ""
        try:  # vulnerabilidades conhecidas na versão instalada (OSV)
            body = json.dumps({"package": {"name": item["pacote"], "ecosystem": "npm"}, "version": item["versao"]}).encode()
            req = urllib.request.Request("https://api.osv.dev/v1/query", data=body, headers={"Content-Type": "application/json"})
            vulns = json.load(urllib.request.urlopen(req, timeout=15)).get("vulns", [])
            if vulns:
                extra = "VULNERABILIDADE na versão instalada: " + ", ".join(v["id"] for v in vulns[:3])
        except Exception:
            pass
        return vs[0], d["time"][vs[0]], extra
    raise ValueError("tipo desconhecido: " + t)


def rodar():
    inv = json.load(open(INV))["itens"]
    res = []
    for item in inv:
        atual = item.get("versao") or item.get("commit")
        try:
            novo, quando, nota = verificar(item)
        except Exception as e:
            res.append({"nome": item["nome"], "erro": str(e)[:120]})
            continue
        if novo == atual and not nota.startswith("VULNERABILIDADE"):
            continue
        if novo == atual:
            res.append({"nome": item["nome"], "atual": atual, "nova": novo, "nota": nota, "pronta": True, "dias": 0})
            continue
        dias = (AGORA - data(quando)).days
        limite = QUARENTENA_CRITICO if item.get("critico") else QUARENTENA
        res.append({"nome": item["nome"], "atual": atual[:12], "nova": novo[:12], "data": quando[:10], "dias": dias,
                    "pronta": dias >= limite, "quarentena": limite, "nota": nota,
                    "tem_ajustes_locais": bool(item.get("ajustes"))})
    out = {"verificado_em": AGORA.isoformat(timespec="seconds"), "novidades": res}
    json.dump(out, open(CACHE, "w"), indent=2, ensure_ascii=False)
    return out


def texto(out):
    linhas = []
    for r in out["novidades"]:
        if "erro" in r:
            linhas.append(f"- {r['nome']}: não consegui verificar ({r['erro']})")
            continue
        estado = "pronta para o crivo" if r["pronta"] else f"em quarentena ({r['dias']}/{r['quarentena']} dias)"
        aj = " · tem ajustes locais (reaplicar patch)" if r.get("tem_ajustes_locais") else ""
        nota = f" · {r['nota']}" if r.get("nota") else ""
        linhas.append(f"- {r['nome']}: {r['atual']} → {r['nova']} ({r.get('data','')}) — {estado}{aj}{nota}")
    return "\n".join(linhas)


def main():
    if "--hook" in sys.argv:
        try:
            cache = json.load(open(CACHE))
            if (AGORA - data(cache["verificado_em"])).total_seconds() < INTERVALO_HORAS * 3600:
                out = cache
            else:
                out = rodar()
        except Exception:
            try:
                out = rodar()
            except Exception:
                return  # sem rede etc.: não atrapalha o início da sessão
        prontas = [r for r in out["novidades"] if r.get("pronta")]
        if not prontas:
            return
        msg = texto({"novidades": prontas})
        print(json.dumps({
            "systemMessage": "Crivo: há atualizações prontas para avaliar:\n" + msg,
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": (
                    "Verificador do Crivo encontrou atualizações que já passaram da quarentena:\n" + msg +
                    "\nAvise o usuário no início da conversa (em português simples) e ofereça aplicar o crivo de "
                    "atualização (diff contra a versão registrada, reaplicar patches de ~/.claude/crivo/ajustes/, "
                    "aprovação, e-mail). Nunca atualize sem aprovação. Se o usuário já pediu outra coisa, faça "
                    "o pedido primeiro e mencione as atualizações em uma linha no final."
                ),
            },
        }, ensure_ascii=False))
        return
    out = rodar()
    print(f"Verificado em {out['verificado_em']}")
    print(texto(out) or "Tudo em dia: nenhuma atualização nas fontes.")


if __name__ == "__main__":
    main()
