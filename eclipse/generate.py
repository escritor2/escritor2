#!/usr/bin/env python3
"""Gera o eclipse carmesim do perfil a partir das contribuicoes reais no GitHub.

Cada raio da coroa e um dia do ultimo ano. Sem dependencias externas; requer
GITHUB_TOKEN.

Uso:
    python eclipse/generate.py --out dist-eclipse
    python eclipse/generate.py --out /tmp/x --idle 40   # testa os estados
"""

import argparse
import json
import math
import os
import random
import re
import urllib.request
from datetime import date, datetime
from pathlib import Path
from xml.sax.saxutils import escape

from acts import BRT, build_acts
from pages import SERIF, chapters, quill

USER = "escritor2"
MONO = "ui-monospace,'SF Mono','Cascadia Mono',Menlo,Consolas,'DejaVu Sans Mono',monospace"
MONTHS = "jan fev mar abr mai jun jul ago set out nov dez".split()
W, H, CX, CY, R = 1000, 680, 500, 292, 128
BONE = "#F3E7DF"
BLOOD = "#DC143C"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar { weeks { contributionDays { date contributionCount } } }
    }
    repositories(first: 100, privacy: PUBLIC, isFork: false, ownerAffiliations: OWNER,
                 orderBy: {field: PUSHED_AT, direction: DESC}) {
      nodes {
        name pushedAt
        languages(first: 6, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } }
        defaultBranchRef {
          target {
            ... on Commit {
              history(first: 6) {
                totalCount
                nodes { messageHeadline committedDate author { user { login } } }
              }
            }
          }
        }
      }
    }
  }
}
"""


def fetch():
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "User-Agent": "profile-eclipse"},
    )
    with urllib.request.urlopen(request, timeout=40) as response:
        payload = json.load(response)
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    user = payload["data"]["user"]
    days = [
        (date.fromisoformat(d["date"]), d["contributionCount"])
        for week in user["contributionsCollection"]["contributionCalendar"]["weeks"]
        for d in week["contributionDays"]
    ]
    repos, commits = [], []
    skip = re.compile(r"^(merge\b|updated? with|initial commit|first commit)", re.I)
    for node in user["repositories"]["nodes"]:
        branch = node["defaultBranchRef"]
        history = branch["target"]["history"] if branch else {"totalCount": 0, "nodes": []}
        repos.append({
            "name": node["name"],
            "pushed": datetime.fromisoformat(node["pushedAt"].replace("Z", "+00:00")),
            "commits": history["totalCount"],
            "langs": [(e["node"]["name"], e["size"], e["node"]["color"] or "#A08A92") for e in node["languages"]["edges"]],
        })
        if node["name"] == USER:
            continue
        for item in history["nodes"]:
            login = ((item["author"] or {}).get("user") or {}).get("login")
            if login == USER and not skip.match(item["messageHeadline"]):
                moment = datetime.fromisoformat(item["committedDate"].replace("Z", "+00:00"))
                commits.append((moment, node["name"], item["messageHeadline"]))
    commits.sort(key=lambda c: c[0], reverse=True)
    latest = [(m.astimezone(BRT).date(), r, h) for m, r, h in commits[:16]]
    return days, repos, latest


def state(days):
    counts = [c for _, c in days]
    idle = 0
    for count in reversed(counts):
        if count:
            break
        idle += 1
    last = next((d for d, c in reversed(days) if c), days[-1][0])
    week = sum(counts[-7:])
    if idle >= 30:
        mood, power = "ECLIPSE TOTAL", .06
    elif idle >= 14:
        mood, power = "A PENA DESCANSA", .28
    elif idle >= 3:
        mood, power = "A TINTA SECA", .55
    elif max(counts[-3:]) >= 10:
        mood, power = "A PENA NÃO PARA", 1.0
    else:
        mood, power = "A TINTA ESTÁ FRESCA", .9
    return dict(idle=idle, week=week, mood=mood, power=power, year=sum(counts[-364:]), last=last)


def fmt(day):
    return f"{day.day:02d}/{MONTHS[day.month - 1]}"


def rays(days):
    recent = days[-364:]
    top = max(c for _, c in recent) or 1
    active, quiet = [], []
    for index, (_, count) in enumerate(recent):
        angle = math.radians(-90 + (index + 1) / len(recent) * 360)
        length = 12 + 112 * math.sqrt(count / top) if count else 4
        x0, y0 = CX + (R + 1) * math.cos(angle), CY + (R + 1) * math.sin(angle)
        x1, y1 = CX + (R + length) * math.cos(angle), CY + (R + length) * math.sin(angle)
        (active if count else quiet).append(f"M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}")
    return "".join(active), "".join(quiet)


def ring_text(names):
    chosen, size = [], 0
    for name in names * 3:
        if size + len(name) + 3 > 186:
            break
        chosen.append(name)
        size += len(name) + 3
    return escape("  ✦  ".join(chosen) + "  ✦  ")


def smoke(rng):
    out = []
    for _ in range(13):
        x, y = rng.randint(-40, W + 40), rng.randint(20, H)
        dx, seconds = rng.randint(-90, 90), rng.randint(36, 80)
        out.append(
            f'<ellipse rx="{rng.randint(170, 340)}" ry="{rng.randint(70, 150)}" fill="url(#smoke)" opacity="{rng.uniform(.3, .75):.2f}">'
            f'<animateTransform attributeName="transform" type="translate" values="{x} {y};{x + dx} {y - 34};{x} {y}" dur="{seconds}s" repeatCount="indefinite"/></ellipse>'
        )
    return "".join(out)


def embers(rng, count):
    out = []
    for _ in range(count):
        x, y = rng.randint(10, W - 10), rng.randint(420, H - 10)
        seconds = rng.randint(7, 17)
        begin = -rng.uniform(0, seconds)
        color = rng.choice((BLOOD, "#FF3355", "#FF7A5C", "#8E0B26"))
        out.append(
            f'<circle r="{rng.uniform(.8, 2.4):.1f}" fill="{color}" opacity="0">'
            f'<animateTransform attributeName="transform" type="translate" values="{x} {y};{x + rng.randint(-40, 40)} {y - 200};{x + rng.randint(-70, 70)} {y - rng.randint(320, 430)}" dur="{seconds}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;.8;0" keyTimes="0;.1;.7;1" dur="{seconds}s" begin="{begin:.1f}s" repeatCount="indefinite"/></circle>'
        )
    return "".join(out)


def code_rain(rng):
    """Colunas de codigo caindo nas laterais do eclipse."""
    out = []
    glyphs = "01{}<>/;=()[]$#"
    columns = list(range(22, 200, 26)) + list(range(806, 985, 26))
    for x in columns:
        seconds = rng.uniform(8, 17)
        cells = "".join(
            f'<tspan x="{x}" dy="17" fill-opacity="{(i + 1) / 15:.2f}"'
            + (' fill="#FFE4DE"' if i == 14 else "")
            + f">{escape(rng.choice(glyphs))}</tspan>"
            for i in range(15)
        )
        out.append(
            f'<text font-family="{MONO}" font-size="14" font-weight="700" fill="#E5284A">{cells}'
            f'<animateTransform attributeName="transform" type="translate" from="0 -280" to="0 {H - 90}" '
            f'dur="{seconds:.1f}s" begin="{-rng.uniform(0, seconds):.1f}s" repeatCount="indefinite"/></text>'
        )
    return "".join(out)


def falling(rng, count):
    out = []
    for i in range(count):
        side = rng.choice((rng.randint(26, 190), rng.randint(810, 974)))
        start, pool = rng.randint(50, 110), H - 18
        seconds = rng.uniform(2.6, 5.4)
        begin = i * .7
        hit = .34
        timing = f'dur="{seconds:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"'
        out.append(
            f'<ellipse cx="{side}" rx="1.3" ry="15" fill="#FF6B84">'
            f'<animate attributeName="cy" values="{start};{pool};{pool}" keyTimes="0;{hit};1" calcMode="spline" keySplines=".5 0 1 .7;0 0 1 1" {timing}/>'
            f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{hit};{hit + .001};1" {timing}/></ellipse>'
            f'<ellipse cx="{side}" cy="{pool + 2}" fill="none" stroke="#FF3355" rx="1" ry=".4" opacity="0">'
            f'<animate attributeName="rx" values="1;1;30;30" keyTimes="0;{hit};.72;1" {timing}/>'
            f'<animate attributeName="ry" values=".4;.4;6;6" keyTimes="0;{hit};.72;1" {timing}/>'
            f'<animate attributeName="opacity" values="0;0;.9;0;0" keyTimes="0;{hit};{hit + .02};.72;1" {timing}/></ellipse>'
        )
    return "".join(out)


def horizon_line(y, width):
    """Linha de energia na base, com um pulso que a percorre."""
    return (
        f'<rect y="{y}" width="{width}" height="20" fill="#120207"/>'
        f'<rect y="{y}" width="{width}" height="2" fill="#E5284A"/>'
        f'<rect y="{y - 1}" width="150" height="4" fill="#FFE4DE">'
        f'<animate attributeName="x" from="-150" to="{width}" dur="5s" repeatCount="indefinite"/></rect>'
    )


def eclipse(days, names, s):
    rng = random.Random("eclipse")
    active, quiet = rays(days)
    power = s["power"]
    total = s["mood"] == "ECLIPSE TOTAL"
    beat = max(2.2, 7 - s["week"] * .12)
    circumference = round(2 * math.pi * 262, 1)
    quote = "O autor desapareceu." if total else "Escrevo sistemas como quem escreve histórias."
    legend = f"CADA RAIO É UM DIA DE CÓDIGO   ✦   {s['year']} NO ÚLTIMO ANO   ✦   ÚLTIMA ESCRITA {fmt(s['last'])}   ✦   {s['mood']}"
    name = (f'x="500" y="{CY + 16}" text-anchor="middle" textLength="770" lengthAdjust="spacingAndGlyphs" '
            f'font-family="{SERIF}" font-size="78" font-weight="700" letter-spacing="3"')
    pulses = "".join(
        f'<circle cx="{CX}" cy="{CY}" fill="none" stroke="{BLOOD}" stroke-width="1.4" opacity="0">'
        f'<animate attributeName="r" values="{R};330" dur="{beat}s" begin="{i * beat / 2}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="{.5 * power};0" dur="{beat}s" begin="{i * beat / 2}s" repeatCount="indefinite"/></circle>'
        for i in range(2)
    ) if not total else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Gabriel Ferreira, desenvolvedor full stack. Eclipse carmesim cuja coroa tem um raio para cada dia de código do último ano.">
<title>Gabriel Ferreira · Desenvolvedor Full Stack</title>
<defs>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<radialGradient id="bg" cx="{CX}" cy="{CY}" r="620" gradientUnits="userSpaceOnUse"><stop stop-color="#2A040E"/><stop offset=".42" stop-color="#110207"/><stop offset="1" stop-color="#030102"/></radialGradient>
<radialGradient id="smoke"><stop stop-color="#7A0F28" stop-opacity=".34"/><stop offset="1" stop-color="#7A0F28" stop-opacity="0"/></radialGradient>
<radialGradient id="halo" cx="{CX}" cy="{CY}" r="290" gradientUnits="userSpaceOnUse"><stop offset=".42" stop-color="#FF2347" stop-opacity=".75"/><stop offset=".62" stop-color="#B00D2E" stop-opacity=".25"/><stop offset="1" stop-color="#B00D2E" stop-opacity="0"/></radialGradient>
<radialGradient id="ray" cx="{CX}" cy="{CY}" r="255" gradientUnits="userSpaceOnUse"><stop offset=".5" stop-color="#FFD3CF"/><stop offset=".62" stop-color="#FF2A4D"/><stop offset="1" stop-color="#A10A2B" stop-opacity=".12"/></radialGradient>
<radialGradient id="disk" cx=".38" cy=".32" r=".9"><stop stop-color="#180409"/><stop offset=".7" stop-color="#050102"/><stop offset="1" stop-color="#000"/></radialGradient>
<linearGradient id="fade" x2="0" y2="1"><stop offset=".78" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".78"/></linearGradient>
<path id="ring" d="M{CX} {CY - 262}A262 262 0 1 1 {CX - .01} {CY - 262}z"/>
<clipPath id="line"><rect x="170" y="584" width="0" height="46"><animate attributeName="width" values="0;660;660;0" keyTimes="0;.4;.96;1" dur="20s" repeatCount="indefinite"/></rect></clipPath>
<filter id="glow" x="-10%" y="-90%" width="120%" height="280%"><feGaussianBlur stdDeviation="9"/></filter>
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
{smoke(rng)}
<circle cx="{CX}" cy="{CY}" r="290" fill="url(#halo)" opacity="{power}"><animate attributeName="opacity" values="{power};{power * .62:.2f};{power}" dur="{beat}s" repeatCount="indefinite"/></circle>
{pulses}
<path d="{quiet}" stroke="#7A1026" stroke-width="1" opacity="{.75 * power:.2f}"/>
<path d="{active}" stroke="url(#ray)" stroke-width="1.8" opacity="{power}"/>
<g opacity="{.5 * power:.2f}"><g transform="translate({CX} {CY})"><g><animateTransform attributeName="transform" type="scale" values="1;1.05;1" dur="{beat}s" repeatCount="indefinite"/><path transform="translate({-CX} {-CY})" d="{active}" stroke="url(#ray)" stroke-width="3.2"/></g></g></g>
<path d="M{CX} {CY - R - 2}V{CY - R - 34}" stroke="#FFF" stroke-width="2.2" stroke-linecap="round"/>
<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#disk)"/>
<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="#FF4A63" stroke-width="1.6" opacity="{max(power, .3)}"/>
<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="#FFEFEA" stroke-width="3" stroke-linecap="round" stroke-dasharray="74 730" opacity="{max(power, .25)}"><animateTransform attributeName="transform" type="rotate" from="0 {CX} {CY}" to="360 {CX} {CY}" dur="12s" repeatCount="indefinite"/></circle>
<g><animateTransform attributeName="transform" type="rotate" from="0 {CX} {CY}" to="-360 {CX} {CY}" dur="130s" repeatCount="indefinite"/>
<circle cx="{CX}" cy="{CY}" r="278" fill="none" stroke="#8E1530" stroke-dasharray="1 9"/>
<text font-family="{MONO}" font-size="13" font-weight="700" fill="#E5425F"><textPath href="#ring" textLength="{circumference}" lengthAdjust="spacing">{ring_text(names)}</textPath></text></g>
<text {name} filter="url(#glow)" fill="{BLOOD}" opacity="{.95 * max(power, .35):.2f}">GABRIEL FERREIRA<animate attributeName="opacity" values=".95;.55;.95" dur="{beat}s" repeatCount="indefinite"/></text>
<text {name} fill="{BONE}" stroke="#030102" stroke-width="7" stroke-linejoin="round" paint-order="stroke">GABRIEL FERREIRA<animate attributeName="fill-opacity" values="0;0;1" keyTimes="0;.25;1" dur="1.8s" fill="freeze"/></text>
<text {name} fill="none" stroke="#FF2A4D" stroke-width="1.3" stroke-dasharray="3000" stroke-dashoffset="3000">GABRIEL FERREIRA<animate attributeName="stroke-dashoffset" from="3000" to="0" dur="1.8s" fill="freeze"/></text>
{glitch(name)}
<text x="500" y="{CY + 54}" text-anchor="middle" textLength="238" lengthAdjust="spacing" font-family="{SERIF}" font-size="15" font-weight="700" fill="#FF6B7F">DESENVOLVEDOR FULL STACK</text>
{embers(rng, 22 if total else 66 if s['mood'] == 'A PENA NÃO PARA' else 44)}
<rect width="{W}" height="{H}" fill="url(#fade)"/>
{code_rain(rng)}
<g clip-path="url(#line)"><text x="500" y="619" text-anchor="middle" textLength="640" lengthAdjust="{'spacing' if total else 'spacingAndGlyphs'}" font-family="{SERIF}" font-size="31" font-style="italic" fill="{BONE}">{quote}</text></g>
{quill(180, 820, 619, 20)}
<text x="500" y="648" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing=".4" fill="#D98896">{escape(legend)}</text>
{'' if total else falling(rng, min(14, s['week']))}
{horizon_line(H - 16, W)}
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="14" fill="none" stroke="#8E1530" stroke-width="1.5"/>
</svg>
"""


def glitch(name):
    """Corte horizontal e aberracao de cor que rasgam o nome de vez em quando."""
    out = '<clipPath id="cut"><rect y="258" width="1000" height="16"/><rect y="288" width="1000" height="10"/></clipPath>'
    keys = "0;.47;.471;.49;.491;.51;.511;1"
    timing = f'keyTimes="{keys}" dur="11s" repeatCount="indefinite"'
    for color, shift in (("#FF0033", -13), ("#FFFFFF", 11)):
        out += (
            f'<g clip-path="url(#cut)"><g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0;1;0" calcMode="discrete" {timing}/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;{shift} 0;{-shift} 0;{shift} 0;0 0;{-shift} 0;0 0" calcMode="discrete" {timing}/>'
            f'<text {name} fill="{color}">GABRIEL FERREIRA</text></g></g>'
        )
    return out


def epilogue(s):
    width, height = 1000, 300
    rng = random.Random("epilogue")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="Do processo à interface. Da ideia ao código. Continua no próximo commit.">
<title>Continua no próximo commit</title>
<defs>
<clipPath id="f"><rect width="{width}" height="{height}" rx="14"/></clipPath>
<radialGradient id="b" cy="1" r="1"><stop stop-color="#3A0612"/><stop offset=".6" stop-color="#0E0206"/><stop offset="1" stop-color="#030102"/></radialGradient>
<radialGradient id="wax" cx=".36" cy=".3" r=".85"><stop stop-color="#F0344F"/><stop offset=".55" stop-color="#A80C2C"/><stop offset="1" stop-color="#57000F"/></radialGradient>
<clipPath id="w"><rect x="130" y="52" width="0" height="60"><animate attributeName="width" values="0;740;740;0" keyTimes="0;.42;.96;1" dur="18s" repeatCount="indefinite"/></rect></clipPath>
</defs>
<g clip-path="url(#f)">
<rect width="{width}" height="{height}" fill="url(#b)"/>
<g clip-path="url(#w)"><text x="500" y="96" text-anchor="middle" textLength="730" lengthAdjust="spacingAndGlyphs" font-family="{SERIF}" font-size="36" font-style="italic" fill="{BONE}">Do processo à interface. Da ideia ao código.</text></g>
{quill(135, 865, 96, 18)}
<g transform="translate(500 176)">
<circle r="58" fill="{BLOOD}" opacity=".24"><animate attributeName="r" values="52;66;52" dur="4s" repeatCount="indefinite"/></circle>
<path fill="url(#wax)" d="M-40-14C-46-34-24-48-8-44C8-54 32-44 38-26C52-14 50 12 38 24C34 44 10 52-6 44C-24 52-44 38-44 20C-54 8-50-6-40-14z"/>
<circle r="30" fill="none" stroke="#6B0016" stroke-width="2"/>
<text y="11" text-anchor="middle" font-family="{SERIF}" font-size="30" font-weight="700" fill="#5A0012">GF</text>
</g>
<text x="500" y="266" text-anchor="middle" font-family="{SERIF}" font-size="20" font-style="italic" fill="#FF8C9C">Continua no próximo commit…<animate attributeName="opacity" values="1;.35;1" dur="3s" repeatCount="indefinite"/></text>
{embers(rng, 22).replace('420', '230')}
</g>
<rect x=".75" y=".75" width="{width - 1.5}" height="{height - 1.5}" rx="14" fill="none" stroke="#8E1530" stroke-width="1.5"/>
</svg>
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="dist-eclipse")
    parser.add_argument("--idle", type=int, default=0, help="zera os ultimos N dias, para testes")
    args = parser.parse_args()

    days, repos, commits = fetch()
    names = [r["name"] for r in repos if r["name"] != USER][:14]
    now = datetime.now(BRT)
    if args.idle:
        cut = len(days) - args.idle
        days = [(d, c if i < cut else 0) for i, (d, c) in enumerate(days)]
    s = state(days)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    files = {"eclipse": eclipse(days, names, s), "epilogue": epilogue(s), **chapters(), **build_acts(days, repos, commits, now)}
    for name, svg in files.items():
        (out / f"{name}.svg").write_text(svg, encoding="utf-8")
    print(s)


if __name__ == "__main__":
    main()
