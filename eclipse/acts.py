"""Os atos da descida: cada um e um SVG animado, com dados reais quando indicado."""

import math
import random
from datetime import timedelta, timezone
from xml.sax.saxutils import escape

from pages import BLOOD, BONE, HOT, MONO, SERIF, quill

BRT = timezone(timedelta(hours=-3))
MONTHS = "jan fev mar abr mai jun jul ago set out nov dez".split()
WEEKDAYS = "segunda terça quarta quinta sexta sábado domingo".split()


def fmt(day):
    return f"{day.day:02d}/{MONTHS[day.month - 1]}"


def ash(rng, count, width, height):
    out = []
    for _ in range(count):
        x, y = rng.randint(10, width - 10), rng.randint(height // 2, height - 10)
        seconds = rng.randint(7, 18)
        begin = -rng.uniform(0, seconds)
        color = rng.choice((BLOOD, HOT, "#FF7A5C", "#8E0B26"))
        out.append(
            f'<circle r="{rng.uniform(.8, 2.3):.1f}" fill="{color}" opacity="0">'
            f'<animateTransform attributeName="transform" type="translate" values="{x} {y};{x + rng.randint(-60, 60)} {y - rng.randint(240, 420)}" dur="{seconds}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;.8;0" keyTimes="0;.1;.7;1" dur="{seconds}s" begin="{begin:.1f}s" repeatCount="indefinite"/></circle>'
        )
    return "".join(out)


def panel(act, title, subtitle, width, height, inner, defs=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{escape(title)}. {escape(subtitle)}">
<title>{escape(title)}</title>
<defs>
<clipPath id="frame"><rect width="{width}" height="{height}" rx="14"/></clipPath>
<radialGradient id="bg" cx=".5" cy=".5" r=".78"><stop stop-color="#34050F"/><stop offset=".55" stop-color="#100207"/><stop offset="1" stop-color="#030102"/></radialGradient>
<filter id="tg" x="-10%" y="-70%" width="120%" height="240%"><feGaussianBlur stdDeviation="8"/></filter>
{defs}
</defs>
<g clip-path="url(#frame)">
<rect width="{width}" height="{height}" fill="url(#bg)"/>
{inner}
<text x="{width / 2}" y="40" text-anchor="middle" font-family="{SERIF}" font-size="15" letter-spacing="6" fill="#FF6B7F">{escape(act)}</text>
<text x="{width / 2}" y="84" text-anchor="middle" filter="url(#tg)" font-family="{SERIF}" font-size="40" font-weight="700" fill="{BLOOD}">{escape(title)}</text>
<text x="{width / 2}" y="84" text-anchor="middle" font-family="{SERIF}" font-size="40" font-weight="700" fill="{BONE}">{escape(title)}</text>
<text x="{width / 2}" y="112" text-anchor="middle" font-family="{SERIF}" font-size="17" font-style="italic" fill="#E9C4C0">{escape(subtitle)}</text>
</g>
<rect x=".75" y=".75" width="{width - 1.5}" height="{height - 1.5}" rx="14" fill="none" stroke="#8E1530" stroke-width="1.5"/>
</svg>
"""


def spin(cx, cy, seconds, reverse=False):
    target = -360 if reverse else 360
    return (f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" '
            f'to="{target} {cx} {cy}" dur="{seconds}s" repeatCount="indefinite"/>')


def log_column(x, lines, seconds):
    """Coluna lateral de chamadas subindo sem parar."""
    step = 34
    total = step * len(lines)
    cells = "".join(
        f'<text x="{x}" y="{170 + copy * total + i * step}" font-family="{MONO}" font-size="12.5" font-weight="700" fill="#E5425F">{escape(line)}</text>'
        for copy in range(2) for i, line in enumerate(lines)
    )
    return (f'<g clip-path="url(#logs)"><g>{cells}<animateTransform attributeName="transform" type="translate" '
            f'from="0 0" to="0 {-total}" dur="{seconds}s" repeatCount="indefinite"/></g></g>')


def cycle():
    width, height, cx, cy = 1000, 800, 500, 432
    rng = random.Random("cycle")
    nodes = [
        (cx, cy - 230, "Frontend", "React · Vue/Nuxt", "TypeScript"),
        (cx + 199, cy + 115, "Backend", "PHP/Laravel · APIs", "Autenticação"),
        (cx - 199, cy + 115, "Dados", "SQLite · Prisma", "Google Sheets"),
    ]
    triangle = "M" + "L".join(f"{x} {y}" for x, y, *_ in nodes) + "z"
    body = ""
    for i, (x, y, name, line1, line2) in enumerate(nodes):
        body += (
            f'<circle cx="{x}" cy="{y}" r="86" fill="{BLOOD}" opacity="0"><animate attributeName="opacity" values=".55;0;0;.55" keyTimes="0;.2;.98;1" dur="6s" begin="{i * 2}s" repeatCount="indefinite"/></circle>'
            f'<circle cx="{x}" cy="{y}" r="78" fill="#100307" stroke="{BLOOD}" stroke-width="2.5"/>'
            f'<text x="{x}" y="{y - 8}" text-anchor="middle" font-family="{SERIF}" font-size="24" font-weight="700" fill="{BONE}">{name}</text>'
            f'<text x="{x}" y="{y + 16}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="#FF8C9C">{line1}</text>'
            f'<text x="{x}" y="{y + 34}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="#FF8C9C">{line2}</text>'
        )
    code = "fetch('/api')  ·  validate(request)  ·  authorize(user)  ·  persist(data)  ·  return response  ·  render(view)  ·  "
    orb = (
        f'<path d="{triangle}" fill="none" stroke="{BONE}" stroke-width="3.5" stroke-linejoin="round" stroke-dasharray="120 1260"><animate attributeName="stroke-dashoffset" from="120" to="-1260" dur="6s" repeatCount="indefinite"/></path>'
        f'<circle r="8" fill="#FFF"><animateMotion dur="6s" repeatCount="indefinite" path="{triangle}"/></circle>'
    )
    left = ["GET /api 200", "POST /auth 201", "GET /users 200", "PUT /data 200", "POST /login 200", "GET /health 200", "DELETE /row 204", "PATCH /item 200"]
    right = ["validate()", "authorize()", "query()", "persist()", "commit()", "respond()", "render()", "hydrate()"]
    inner = (
        f'<g>{spin(cx, cy, 60)}<circle cx="{cx}" cy="{cy}" r="262" fill="none" stroke="#8E1530" stroke-width="10" stroke-dasharray="46 30"/></g>'
        f'<g>{spin(cx, cy, 40, True)}<circle cx="{cx}" cy="{cy}" r="150" fill="none" stroke="#8E1530" stroke-width="5" stroke-dasharray="20 14"/></g>'
        f'<circle cx="{cx}" cy="{cy}" r="302" fill="none" stroke="{BLOOD}" stroke-width="2"/>'
        f'<circle cx="{cx}" cy="{cy}" r="318" fill="none" stroke="#8E1530" stroke-dasharray="2 9"/>'
        f'<g>{spin(cx, cy, 70, True)}<text font-family="{MONO}" font-size="16" font-weight="700" fill="#E5425F"><textPath href="#codering" textLength="1910" lengthAdjust="spacing">{escape(code)}</textPath></text></g>'
        f'<path d="{triangle}" fill="none" stroke="{BLOOD}" stroke-width="2.5"/>{orb}'
        f'<circle cx="{cx}" cy="{cy}" r="52" fill="url(#core)"><animate attributeName="r" values="46;60;46" dur="2s" repeatCount="indefinite"/></circle>'
        f'<text x="{cx}" y="{cy - 2}" text-anchor="middle" font-family="{SERIF}" font-size="18" font-weight="700" fill="{BONE}" stroke="#100307" stroke-width="4" paint-order="stroke">FULL</text>'
        f'<text x="{cx}" y="{cy + 20}" text-anchor="middle" font-family="{SERIF}" font-size="18" font-weight="700" fill="{BONE}" stroke="#100307" stroke-width="4" paint-order="stroke">STACK</text>'
        f'{body}{log_column(26, left, 22)}{log_column(860, right, 18)}{ash(rng, 28, width, height)}'
    )
    defs = (
        f'<path id="codering" d="M{cx} {cy - 304}A304 304 0 1 1 {cx - .01} {cy - 304}z"/>'
        '<clipPath id="logs"><rect y="136" width="1000" height="640"/></clipPath>'
        '<radialGradient id="core"><stop stop-color="#FF3355"/><stop offset=".7" stop-color="#A80C2C" stop-opacity=".7"/><stop offset="1" stop-color="#A80C2C" stop-opacity="0"/></radialGradient>'
    )
    return panel("ATO I", "O Ciclo Full Stack", "Da interface ao banco de dados, e de volta.", width, height, inner, defs)


def tree(repos, now):
    width, height = 1000, 1020
    rng = random.Random("blood-tree")
    groups = {}
    for repo in repos:
        for name, size, color in repo["langs"]:
            entry = groups.setdefault(name, dict(size=0, color=color, repos=[]))
            entry["size"] += size
        if repo["langs"]:
            groups[repo["langs"][0][0]]["repos"].append(repo)
    ranked = sorted((g for g in groups.items() if g[1]["repos"]), key=lambda g: -g[1]["size"])
    main, rest = ranked[:6], ranked[6:]
    loose = [r for r in repos if not r["langs"]] + [r for _, g in rest for r in g["repos"]]
    if loose:
        main.append(("Outros", dict(size=sum(g["size"] for _, g in rest), color="#A08A92", repos=loose)))
    total = sum(g["size"] for _, g in ranked) or 1
    # A maior linguagem fica no centro; as outras abrem para os lados.
    centered = sorted(main, key=lambda g: -g[1]["size"])
    layout = [None] * len(centered)
    left, right = (len(centered) - 1) // 2, (len(centered) - 1) // 2 + 1
    for i, item in enumerate(centered):
        if i % 2 == 0:
            layout[left] = item
            left -= 1
        else:
            layout[right] = item
            right += 1
    layout = [item for item in layout if item]

    layers, tips, recent, labels = {}, [], [], []

    def seg(x, y, angle, length, stroke):
        bend = rng.uniform(-.24, .24)
        end = angle + bend
        cx, cy = x + math.cos(angle) * length * .55, y + math.sin(angle) * length * .55
        x1, y1 = x + math.cos(end) * length, y + math.sin(end) * length
        if y1 < 150:
            y1 = 150 + rng.uniform(0, 30)
        x1 = min(max(x1, 26), width - 26)
        layers.setdefault(round(stroke * 2) / 2, []).append(f"M{x:.0f} {y:.0f}Q{cx:.0f} {cy:.0f} {x1:.0f} {y1:.0f}")
        return x1, y1, end

    def twig(x, y, angle, length, stroke, depth, repo):
        x1, y1, end = seg(x, y, angle, length, stroke)
        if depth == 0:
            tips.append((x1, y1))
            return x1, y1
        tip = None
        for side in (-1, 1):
            tip = twig(x1, y1, end + side * rng.uniform(.28, .62), length * rng.uniform(.68, .84), max(stroke * .62, .8), depth - 1, repo)
        return tip

    trunk_top = 760
    layers.setdefault(30.0, []).append(f"M500 {height - 72}C494 880 506 820 500 {trunk_top}")
    for side, spread in ((-1, 90), (1, 80), (-1, 170), (1, 150)):
        layers.setdefault(7.0, []).append(f"M500 {height - 80}Q{500 + side * spread * .5:.0f} {height - 74} {500 + side * spread} {height - 34}")
    count = len(layout)
    for index, (name, group) in enumerate(layout):
        spread = (index + .5) / count
        angle = -math.pi + .34 + spread * (math.pi - .68)
        stroke = 5 + 20 * math.sqrt(group["size"] / total)
        x, y, a = seg(500, trunk_top, angle, 190, stroke)
        x, y, a = seg(x, y, a * .78 + (-math.pi / 2) * .22, 150, stroke * .72)
        labels.append((x, y, name, group["color"], round(100 * group["size"] / total)))
        items = group["repos"]
        for j, repo in enumerate(items):
            fan = 0 if len(items) == 1 else (j / (len(items) - 1) - .5) * 1.5
            depth = 1 + min(3, int(math.log2(repo["commits"] + 1) / 2))
            tip = twig(x, y, a + fan, rng.uniform(62, 88), max(stroke * .42, 2.2), depth, repo)
            if (now - repo["pushed"]).days <= 7 and repo["name"] != "escritor2":
                recent.append((repo["name"], tip[0], tip[1]))

    wood = "".join(
        f'<path d="{"".join(paths)}" fill="none" stroke="#6B0E24" stroke-width="{stroke}" stroke-linecap="round"/>'
        for stroke, paths in sorted(layers.items(), reverse=True)
    )
    flow = ""
    for stroke, paths in layers.items():
        if stroke >= 2:
            flow += (
                f'<path d="{"".join(paths)}" fill="none" stroke="#FF3355" stroke-width="{max(stroke * .3, 1.2):.1f}" stroke-linecap="round" stroke-dasharray="14 150">'
                f'<animate attributeName="stroke-dashoffset" from="164" to="0" dur="{rng.uniform(2.4, 3.4):.1f}s" repeatCount="indefinite"/></path>'
            )
    fruit = "".join(
        f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rng.uniform(2.2, 4):.1f}" fill="{rng.choice((HOT, BLOOD, BONE))}"'
        + (f'><animate attributeName="opacity" values="1;.3;1" dur="{rng.uniform(1.5, 4.5):.1f}s" repeatCount="indefinite"/></circle>' if i % 3 == 0 else "/>")
        for i, (x, y) in enumerate(tips)
    )
    names = ""
    for x, y, name, color, share in labels:
        names += (
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{color}" stroke="#100307" stroke-width="2"/>'
            f'<text x="{x:.0f}" y="{y + 28:.0f}" text-anchor="middle" font-family="{SERIF}" font-size="20" font-weight="700" fill="{BONE}" stroke="#100307" stroke-width="5" stroke-linejoin="round" paint-order="stroke">{escape(name)} · {share}%</text>'
        )
    spots = recent[:5]
    tags = ""
    for i, (name, x, y) in enumerate(spots):
        shown = name if len(name) <= 24 else name[:23] + "…"
        box = min(max(x - 90, 14), width - 196)
        share = 1 / len(spots)
        tags += (
            f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{share * .08:.3f};{share * .9:.3f};{share:.3f};1" dur="{4 * len(spots)}s" begin="{i * 4}s" repeatCount="indefinite"/>'
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="12" fill="none" stroke="#FFF" stroke-width="2"/>'
            f'<rect x="{box:.0f}" y="{y + 16:.0f}" width="182" height="26" rx="5" fill="#0B0205" stroke="{HOT}"/>'
            f'<text x="{box + 91:.0f}" y="{y + 34:.0f}" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="#FFF">{escape(shown)}</text></g>'
        )
    moon = '<circle cx="500" cy="440" r="330" fill="url(#moon)"/>'
    pool = (f'<rect y="{height - 42}" width="{width}" height="42" fill="#0B0205"/>'
            f'<rect y="{height - 42}" width="{width}" height="2" fill="{HOT}" opacity=".7"/>')
    inner = moon + wood + flow + fruit + names + tags + pool + ash(rng, 40, width, height)
    defs = '<radialGradient id="moon"><stop stop-color="#C8102E" stop-opacity=".42"/><stop offset=".7" stop-color="#8E0B26" stop-opacity=".14"/><stop offset="1" stop-color="#8E0B26" stop-opacity="0"/></radialGradient>'
    return panel("ATO III", "A Árvore de Repositórios", f"Cada galho é um dos meus {len(repos)} repositórios públicos, nascendo da sua linguagem.", width, height, inner, defs)


def wheel():
    width, height, cx, cy, radius = 1000, 740, 500, 426, 240
    rng = random.Random("wheel")
    tech = [("JS", "JavaScript"), ("TS", "TypeScript"), ("Re", "React"), ("Vu", "Vue"), ("Nx", "Nuxt"), ("Tw", "Tailwind"),
            ("Ph", "PHP"), ("La", "Laravel"), ("No", "Node.js"), ("Pr", "Prisma"), ("Sq", "SQLite"), ("Gt", "Git")]
    spokes = ""
    for i in range(72):
        a = math.tau * i / 72
        r1, r2 = (112, 170) if i % 6 else (98, 196)
        spokes += f"M{cx + r1 * math.cos(a):.1f} {cy + r1 * math.sin(a):.1f}L{cx + r2 * math.cos(a):.1f} {cy + r2 * math.sin(a):.1f}"
    seconds = 72
    medals = ""
    for i, (mark, name) in enumerate(tech):
        a = math.tau * i / len(tech) - math.pi / 2
        x, y = round(cx + radius * math.cos(a), 1), round(cy + radius * math.sin(a), 1)
        medals += (
            f'<g><animateTransform attributeName="transform" type="rotate" from="0 {x} {y}" to="-360 {x} {y}" dur="{seconds}s" repeatCount="indefinite"/>'
            f'<circle cx="{x}" cy="{y}" r="50" fill="#100307" stroke="#8E1530" stroke-width="2"/>'
            f'<circle cx="{x}" cy="{y}" r="50" fill="{BLOOD}" fill-opacity=".35" stroke="{HOT}" stroke-width="3" opacity="0"><animate attributeName="opacity" values="0;1;0;0" keyTimes="0;.03;.1;1" dur="12s" begin="{i}s" repeatCount="indefinite"/></circle>'
            f'<text x="{x}" y="{y + 3}" text-anchor="middle" font-family="{SERIF}" font-size="30" font-weight="700" fill="{BONE}">{mark}</text>'
            f'<text x="{x}" y="{y + 24}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="#FF8C9C">{name}</text></g>'
        )
    inner = (
        f'<circle cx="{cx}" cy="{cy}" r="310" fill="none" stroke="#8E1530" stroke-dasharray="2 10"/>'
        f'<g>{spin(cx, cy, 40, True)}<path d="{spokes}" stroke="{BLOOD}" stroke-width="2.2"/></g>'
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#8E1530" stroke-width="2"/>'
        f'<g>{spin(cx, cy, seconds)}{medals}</g>'
        f'<circle cx="{cx}" cy="{cy}" r="92" fill="#050102" stroke="{HOT}" stroke-width="2.5"/>'
        f'<circle cx="{cx}" cy="{cy}" r="92" fill="none" stroke="#FFEFEA" stroke-width="3" stroke-linecap="round" stroke-dasharray="60 518">{spin(cx, cy, 5)}</circle>'
        f'<text x="{cx}" y="{cy + 2}" text-anchor="middle" font-family="{SERIF}" font-size="36" font-weight="700" fill="{BONE}">12</text>'
        f'<text x="{cx}" y="{cy + 28}" text-anchor="middle" font-family="{SERIF}" font-size="14" letter-spacing="2" fill="#FF8C9C">TECNOLOGIAS</text>'
        f'{ash(rng, 34, width, height)}'
    )
    return panel("ATO IV", "O Arsenal", "As ferramentas presentes nos meus projetos.", width, height, inner)


def codex(days):
    width, height = 1000, 590
    recent = days[-364:]
    cell, x0, y0 = 16.8, 62, 170
    glyphs = {
        0: '<rect x="4" y="9" width="4" height="3" fill="#4A1424"/>',
        1: '<rect x="1" y="8" width="10" height="4" fill="#A81A38"/>',
        2: '<rect x="1" y="5" width="10" height="7" fill="#D81F3E"/>',
        3: '<rect x="1" y="2" width="10" height="10" fill="#FF3D5A"/>',
        4: '<rect x="0" y="-1" width="12" height="13" fill="#FFE4DE"/>',
    }
    defs = "".join(f'<g id="r{level}">{shape}</g>' for level, shape in glyphs.items())

    def level(count):
        return 0 if not count else 1 if count <= 2 else 2 if count <= 5 else 3 if count <= 9 else 4

    columns, labels, last = "", "", None
    for w in range(0, len(recent), 7):
        col = w // 7
        x = x0 + col * cell
        marks = "".join(f'<use href="#r{level(c)}" x="{x:.1f}" y="{y0 + d * cell:.1f}"/>' for d, (_, c) in enumerate(recent[w:w + 7]))
        columns += f'<g>{marks}<animate attributeName="opacity" values=".78;1;.78" dur="6s" begin="{col * .09:.2f}s" repeatCount="indefinite"/></g>'
        month = recent[w][0].month
        if month != last and col < 51:
            if last is not None:
                labels += f'<text x="{x:.1f}" y="{y0 - 12}" font-family="{MONO}" font-size="12" font-weight="700" fill="#D98896">{MONTHS[month - 1]}</text>'
            last = month
    counts = [c for _, c in recent]
    streak = best_streak = 0
    for count in counts:
        streak = streak + 1 if count else 0
        best_streak = max(best_streak, streak)
    peak_day, peak = max(recent, key=lambda item: (item[1], item[0]))
    tally = [0] * 7
    for day, count in recent:
        tally[day.weekday()] += count
    stats = [
        ("MAIOR PICO", f"{peak} em {fmt(peak_day)}"),
        ("MAIOR SEQUÊNCIA", f"{best_streak} dias seguidos"),
        ("DIAS ATIVOS", f"{sum(1 for c in counts if c)} no ano"),
        ("DIA MAIS PRODUTIVO", WEEKDAYS[tally.index(max(tally))]),
    ]
    tablets = ""
    for i, (name, value) in enumerate(stats):
        x = 40 + i * 234
        tablets += (
            f'<rect x="{x}" y="340" width="218" height="96" rx="8" fill="#0B0205" stroke="#8E1530"/>'
            f'<text x="{x + 109}" y="374" text-anchor="middle" font-family="{SERIF}" font-size="13" letter-spacing="1.5" fill="#FF8C9C">{name}</text>'
            f'<text x="{x + 109}" y="412" text-anchor="middle" font-family="{SERIF}" font-size="23" font-weight="700" fill="{BONE}">{escape(value)}</text>'
        )
    legend = "".join(
        f'<use href="#r{i}" x="{330 + i * 76}" y="470"/><text x="{350 + i * 76}" y="481" font-family="{MONO}" font-size="12" fill="#D98896">{t}</text>'
        for i, t in enumerate(("0", "1–2", "3–5", "6–9", "10+"))
    )
    closing = f"{sum(counts)} contribuições no último ano. E contando."
    inner = (
        f'{labels}{columns}{tablets}{legend}'
        f'<text x="500" y="538" text-anchor="middle" font-family="{SERIF}" font-size="20" font-style="italic" fill="{BONE}">{closing}</text>'
        f'{ash(random.Random("codex"), 24, width, height)}'
    )
    return panel("ATO V", "O Registro", "Cada marca é um dia real do meu último ano.", width, height, inner, defs)


def diary(commits):
    width, height, top, bottom = 1000, 600, 138, 560
    if not commits:
        commits = [(None, "—", "O diário ainda está em branco.")]
    lines = list(commits)
    while len(lines) < 12:
        lines += commits
    lines = lines[:16]
    step = 46
    total = len(lines) * step
    body = ""
    for copy in range(2):
        for i, (day, repo, message) in enumerate(lines):
            y = top + 40 + copy * total + i * step
            shown = message if len(message) <= 56 else message[:55] + "…"
            repo_shown = repo if len(repo) <= 21 else repo[:20] + "…"
            body += (
                f'<text x="96" y="{y}" font-family="{MONO}" font-size="14" font-weight="700" fill="#FF6B7F">{fmt(day) if day else ""}</text>'
                f'<text x="174" y="{y}" font-family="{MONO}" font-size="13" fill="#B98A94">{escape(repo_shown)}</text>'
                f'<text x="372" y="{y}" font-family="{SERIF}" font-size="20" font-style="italic" fill="{BONE}">{escape(shown)}</text>'
            )
    inner = (
        f'<path d="M72 {top}V{bottom}" stroke="{BLOOD}" stroke-width="2"/>'
        f'<path d="M78 {top}V{bottom}" stroke="#8E1530"/>'
        f'<g clip-path="url(#win)"><g>{body}<animateTransform attributeName="transform" type="translate" from="0 0" to="0 {-total}" dur="{len(lines) * 4}s" repeatCount="indefinite"/></g></g>'
        f'<rect x="80" y="{top}" width="900" height="60" fill="url(#up)"/><rect x="80" y="{bottom - 60}" width="900" height="60" fill="url(#down)"/>'
    )
    defs = (
        f'<clipPath id="win"><rect x="80" y="{top}" width="900" height="{bottom - top}"/></clipPath>'
        '<linearGradient id="up" x2="0" y2="1"><stop stop-color="#14030A"/><stop offset="1" stop-color="#14030A" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="down" x2="0" y2="1"><stop stop-color="#14030A" stop-opacity="0"/><stop offset="1" stop-color="#14030A"/></linearGradient>'
    )
    return panel("ATO VI", "Diário do Autor", "Minhas últimas mensagens de commit, reais e sem edição.", width, height, inner, defs)


def contract():
    width, height = 1000, 780
    rng = random.Random("contract")
    edge = []
    for x in range(60, 941, 22):
        edge.append((x, 134 + rng.uniform(-7, 7)))
    for y in range(150, 741, 22):
        edge.append((940 + rng.uniform(-7, 7), y))
    for x in range(940, 59, -22):
        edge.append((x, 746 + rng.uniform(-7, 7)))
    for y in range(740, 149, -22):
        edge.append((60 + rng.uniform(-7, 7), y))
    sheet = "M" + "L".join(f"{x:.0f} {y:.0f}" for x, y in edge) + "z"
    loop = 16
    clauses = [
        "Cláusula I. O autor entrega interface, API e banco de dados.",
        "Cláusula II. O autor resolve problemas reais do dia a dia.",
        "Cláusula III. O autor segue evoluindo em arquitetura e testes.",
        "Cláusula IV. A parte contratante traz desafios à altura.",
    ]
    text = ""
    for i, clause in enumerate(clauses):
        y = 262 + i * 52
        start = round(.04 + i * .11, 2)
        text += (
            f'<clipPath id="c{i}"><rect x="112" y="{y - 26}" width="0" height="38"><animate attributeName="width" values="0;0;800;800;0;0" keyTimes="0;{start};{start + .1:.2f};.95;.98;1" dur="{loop}s" repeatCount="indefinite"/></rect></clipPath>'
            f'<text clip-path="url(#c{i})" x="118" y="{y}" font-family="{SERIF}" font-size="26" fill="#2A0A10">{escape(clause)}</text>'
        )
    signature = (
        f'<text x="600" y="618" font-family="{SERIF}" font-size="44" font-style="italic" fill="#A80C2C" fill-opacity="0" stroke="#A80C2C" stroke-width="1.5" stroke-dasharray="2200" stroke-dashoffset="2200">Gabriel Ferreira'
        f'<animate attributeName="stroke-dashoffset" values="2200;2200;0;0;2200;2200" keyTimes="0;.5;.72;.95;.98;1" dur="{loop}s" repeatCount="indefinite"/>'
        f'<animate attributeName="fill-opacity" values="0;0;1;1;0;0" keyTimes="0;.68;.74;.95;.98;1" dur="{loop}s" repeatCount="indefinite"/></text>'
    )
    seal = (
        f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;.74;.76;.95;.98;1" dur="{loop}s" repeatCount="indefinite"/>'
        f'<g transform="translate(232 618)"><g><animateTransform attributeName="transform" type="scale" values="2.4;2.4;1;1" keyTimes="0;.74;.78;1" dur="{loop}s" repeatCount="indefinite"/>'
        '<path fill="url(#wax)" d="M-52-18C-60-44-31-62-10-57C10-70 41-57 49-34C67-18 65 16 49 31C44 57 13 67-8 57C-31 67-57 49-57 26C-70 10-65-8-52-18z"/>'
        '<circle r="38" fill="none" stroke="#6B0016" stroke-width="2"/>'
        f'<text y="13" text-anchor="middle" font-family="{SERIF}" font-size="36" font-weight="700" fill="#5A0012">GF</text></g></g></g>'
    )
    call = (
        f'<text x="500" y="710" text-anchor="middle" font-family="{SERIF}" font-size="24" font-weight="700" fill="#A80C2C">Clique para assinar no LinkedIn ➜'
        '<animate attributeName="opacity" values="1;.3;1" dur="1.6s" repeatCount="indefinite"/></text>'
    )
    inner = (
        f'<path d="{sheet}" fill="url(#paper)" stroke="#6B1228" stroke-width="2"/>'
        f'<text x="500" y="202" text-anchor="middle" font-family="{SERIF}" font-size="30" font-weight="700" letter-spacing="6" fill="#7A0019">PARA QUEM RECRUTA</text>'
        f'<path d="M180 222H820" stroke="#7A0019"/>{text}'
        f'<path d="M560 636H880" stroke="#2A0A10"/><text x="880" y="656" text-anchor="end" font-family="{SERIF}" font-size="16" fill="#4A2A2E">assinatura do autor</text>'
        f'{signature}{seal}{call}'
    )
    defs = (
        '<radialGradient id="paper" cx=".5" cy=".42" r=".8"><stop stop-color="#F0E2D3"/><stop offset=".75" stop-color="#D9C2AC"/><stop offset="1" stop-color="#A9835F"/></radialGradient>'
        '<radialGradient id="wax" cx=".36" cy=".3" r=".85"><stop stop-color="#F0344F"/><stop offset=".55" stop-color="#A80C2C"/><stop offset="1" stop-color="#57000F"/></radialGradient>'
    )
    return panel("ATO VII", "A Última Página", "Ela só precisa de mais uma assinatura.", width, height, inner, defs)


def interlude(text, index):
    width, height = 1000, 120
    rng = random.Random(f"interlude{index}")
    ruler = "".join(
        f'<rect x="{x}" y="0" width="1.5" height="{16 if x % 100 == 0 else 7}" fill="#A80C2C"/>'
        for x in range(20, width, 20)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{escape(text)}">
<title>{escape(text)}</title>
<defs><clipPath id="f"><rect width="{width}" height="{height}" rx="10"/></clipPath><filter id="g" x="-10%" y="-90%" width="120%" height="280%"><feGaussianBlur stdDeviation="7"/></filter></defs>
<g clip-path="url(#f)"><rect width="{width}" height="{height}" fill="#050102"/>{ruler}
<text x="500" y="76" text-anchor="middle" filter="url(#g)" font-family="{SERIF}" font-size="34" font-style="italic" fill="{BLOOD}">{escape(text)}<animate attributeName="opacity" values="1;.4;1;.7;1" dur="{3 + index}s" repeatCount="indefinite"/></text>
<text x="500" y="76" text-anchor="middle" font-family="{SERIF}" font-size="34" font-style="italic" fill="{BONE}">{escape(text)}<animate attributeName="fill-opacity" values="1;1;.1;1;.2;1;1" keyTimes="0;.7;.71;.73;.75;.77;1" dur="{5 + index}s" repeatCount="indefinite"/></text>
<path d="M480 100L500 112L520 100" fill="none" stroke="{HOT}" stroke-width="2.5" stroke-linecap="round"><animateTransform attributeName="transform" type="translate" values="0 -4;0 2;0 -4" dur="1.4s" repeatCount="indefinite"/></path>
</g></svg>
"""


QUOTES = (
    "Role para baixo. A história continua.",
    "Ato II. Quatro histórias já escritas.",
    "O histórico é imutável.",
    "Quanto mais fundo, mais antigo o código.",
    "Você já leu mais da metade do manuscrito.",
    "Última página. Ela está esperando por você.",
)


def build_acts(days, repos, commits, now):
    files = {
        "act-cycle": cycle(),
        "act-tree": tree(repos, now),
        "act-wheel": wheel(),
        "act-year": codex(days),
        "act-diary": diary(commits),
        "act-contract": contract(),
    }
    for index, text in enumerate(QUOTES, 1):
        files[f"interlude-{index}"] = interlude(text, index)
    return files
