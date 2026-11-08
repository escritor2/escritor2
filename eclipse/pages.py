"""Capitulos animados dos projetos em destaque. Conteudo fixo, em SVG puro."""

from xml.sax.saxutils import escape

SERIF = "'Palatino Linotype','Book Antiqua',Palatino,Georgia,'Times New Roman','DejaVu Serif',serif"
MONO = "ui-monospace,'SF Mono','Cascadia Mono',Menlo,Consolas,'DejaVu Sans Mono',monospace"
LOOP = 9
BONE, BLOOD, HOT, DARK = "#F3E7DF", "#DC143C", "#FF3355", "#3A0612"


def timed(attr, values, keys):
    return f'<animate attributeName="{attr}" values="{values}" keyTimes="{keys}" dur="{LOOP}s" repeatCount="indefinite"/>'


def show(start, end=.93):
    return timed("opacity", "0;0;1;1;0;0", f"0;{start};{start + .03:.3f};{end};{end + .04:.3f};1")


def quill(x0, x1, y, seconds):
    """Pena que atravessa a linha enquanto o texto e revelado."""
    timing = f'dur="{seconds}s" repeatCount="indefinite"'
    return (
        f'<g><animateTransform attributeName="transform" type="translate" values="{x0} {y};{x1} {y};{x1} {y};{x0} {y}" keyTimes="0;.4;.96;1" {timing}/>'
        f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;.4;.43;.97;1" {timing}/>'
        '<path d="M0 0C6-14 20-42 56-62C54-40 42-16 15-6C10-4 4-2 0 0z" fill="#F3E7DF"/>'
        '<path d="M0 0C14-20 30-40 56-62" fill="none" stroke="#C8102E" stroke-width="1.3"/>'
        '<circle r="2.2" fill="#FF3355"/></g>'
    )


def rotor(cx, cy, r, seconds, dash="2 10"):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#8E1530" stroke-width="1.5" stroke-dasharray="{dash}">'
            f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{seconds}s" repeatCount="indefinite"/></circle>')


def lock_scene(cx=340, cy=96):
    shackle = (
        f'<path d="M{cx - 24} {cy - 8}V{cy - 36}a24 24 0 0 1 48 0V{cy - 8}" fill="none" stroke="{BONE}" stroke-width="9">'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 -18;0 -18;0 0;0 0" keyTimes="0;.5;.56;.85;.9;1" dur="{LOOP}s" repeatCount="indefinite"/></path>'
    )
    body = (
        f'<rect x="{cx - 40}" y="{cy - 10}" width="80" height="66" rx="10" fill="#14040A" stroke="{BLOOD}" stroke-width="2.5"/>'
        f'<circle cx="{cx}" cy="{cy + 16}" r="8" fill="{BLOOD}"/><path d="M{cx - 5} {cy + 18}L{cx - 8} {cy + 40}H{cx + 8}L{cx + 5} {cy + 18}z" fill="{BLOOD}"/>'
        f'<rect x="{cx - 40}" y="{cy - 10}" width="80" height="66" rx="10" fill="#5EE0A8" opacity="0">{timed("opacity", "0;0;.4;0;0", "0;.5;.54;.72;1")}</rect>'
    )
    key = (
        f'<g>{timed("opacity", "0;1;1;0;0", "0;.06;.46;.52;1")}'
        f'<animateTransform attributeName="transform" type="translate" values="{cx - 150} {cy + 28};{cx - 62} {cy + 28};{cx - 62} {cy + 28}" keyTimes="0;.36;1" dur="{LOOP}s" repeatCount="indefinite"/>'
        f'<circle cx="-22" r="13" fill="none" stroke="{BONE}" stroke-width="5"/><rect x="-9" y="-3" width="62" height="6" fill="{BONE}"/><rect x="38" y="3" width="5" height="9" fill="{BONE}"/><rect x="47" y="3" width="5" height="12" fill="{BONE}"/></g>'
    )
    word = f'<text x="{cx}" y="{cy + 80}" text-anchor="middle" font-family="{SERIF}" font-size="15" font-style="italic" fill="#7FE8B8" opacity="0">{show(.56, .85)}Autorizado</text>'
    return rotor(cx, cy + 8, 82, 28) + rotor(cx, cy + 8, 70, 18, "16 8") + shackle + body + key + word


def tally_scene(cx=340, cy=96):
    badge = (
        f'<clipPath id="scan"><rect x="{cx - 76}" y="{cy - 84}" width="152" height="74" rx="8"/></clipPath>'
        f'<rect x="{cx - 76}" y="{cy - 84}" width="152" height="74" rx="8" fill="#14040A" stroke="{BLOOD}" stroke-width="2.5"/>'
        f'<circle cx="{cx - 44}" cy="{cy - 56}" r="13" fill="{BONE}"/><rect x="{cx - 62}" y="{cy - 40}" width="36" height="18" rx="7" fill="{BONE}"/>'
        f'<rect x="{cx - 14}" y="{cy - 66}" width="72" height="6" fill="#B98A94"/><rect x="{cx - 14}" y="{cy - 50}" width="54" height="6" fill="#6B2730"/><rect x="{cx - 14}" y="{cy - 34}" width="64" height="6" fill="#6B2730"/>'
        f'<g clip-path="url(#scan)"><rect x="{cx - 76}" width="152" height="3" fill="{HOT}"><animate attributeName="y" values="{cy - 84};{cy - 13};{cy - 84}" dur="2.6s" repeatCount="indefinite"/></rect></g>'
    )
    marks, step = "", 0
    for group in range(3):
        x = cx - 104 + group * 76
        for i in range(5):
            if i < 4:
                x1, y1, x2, y2 = x + i * 12, cy + 12, x + i * 12 - 3, cy + 62
            else:
                x1, y1, x2, y2 = x - 10, cy + 54, x + 46, cy + 20
            start = round(.04 + step * .05, 2)
            marks += (
                f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{HOT if i == 4 else BONE}" stroke-width="4" stroke-linecap="round" stroke-dasharray="70" stroke-dashoffset="70">'
                f'{timed("stroke-dashoffset", "70;70;0;0;70;70", f"0;{start};{start + .04:.2f};.93;.97;1")}</path>'
            )
            step += 1
    return badge + marks


def book_scene(cx=340, cy=96):
    book = (
        f'<path d="M{cx} {cy + 52}C{cx - 30} {cy + 34} {cx - 76} {cy + 36} {cx - 104} {cy + 48}V{cy - 22}C{cx - 76} {cy - 34} {cx - 30} {cy - 32} {cx} {cy - 14}C{cx + 30} {cy - 32} {cx + 76} {cy - 34} {cx + 104} {cy - 22}V{cy + 48}C{cx + 76} {cy + 36} {cx + 30} {cy + 34} {cx} {cy + 52}z" fill="#E9DACE" stroke="{BLOOD}" stroke-width="2.5"/>'
        f'<path d="M{cx} {cy - 14}V{cy + 52}" stroke="#A67F76" stroke-width="2"/>'
    )
    lines = "".join(
        f'<rect x="{cx + side * 14 - (76 if side < 0 else 0)}" y="{cy - 6 + i * 11}" width="76" height="3" fill="#6B2730"/>'
        for side in (-1, 1) for i in range(4)
    )
    floats = ""
    glyphs = "{ } ( ) < / > ; = ✦ λ #".split()
    for i, glyph in enumerate(glyphs):
        x = cx - 92 + i * 17
        begin = i * .55
        floats += (
            f'<text x="{x}" font-family="{MONO}" font-size="17" font-weight="700" fill="{HOT if i % 2 else BONE}" opacity="0">{escape(glyph)}'
            f'<animate attributeName="y" values="{cy - 14};{cy - 92}" dur="4.4s" begin="{begin}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;0" dur="4.4s" begin="{begin}s" repeatCount="indefinite"/></text>'
        )
    return rotor(cx, cy - 14, 104, 34, "1 11") + floats + book + lines


def fire_scene(cx=340, cy=96):
    lines = "".join(f'<rect x="{cx - 36}" y="{cy - 44 + i * 15}" width="{72 - (i * 11) % 26}" height="4" fill="#6B2730"/>' for i in range(6))
    page = (
        f'<clipPath id="burn"><rect x="{cx - 60}" y="{cy - 72}" width="120" height="150">'
        f'{timed("height", "150;150;0;0;150;150", "0;.12;.62;.94;.97;1")}</rect></clipPath>'
        f'<g clip-path="url(#burn)"><path d="M{cx - 50} {cy - 66}H{cx + 28}L{cx + 50} {cy - 44}V{cy + 70}H{cx - 50}z" fill="#E9DACE"/>{lines}</g>'
    )
    flames = ""
    for i, (dx, size, speed) in enumerate(((-34, 14, 1.1), (-10, 20, .8), (18, 17, .95), (40, 12, 1.3))):
        base = cy + 74
        low = (f"M{cx + dx - size / 2} {base}Q{cx + dx - size} {base - size} {cx + dx} {base - size * 2.2}"
               f"Q{cx + dx + size} {base - size} {cx + dx + size / 2} {base}z")
        high = (f"M{cx + dx - size / 2} {base}Q{cx + dx - size * .7} {base - size * 1.2} {cx + dx + 5} {base - size * 2.8}"
                f"Q{cx + dx + size * 1.1} {base - size * 1.1} {cx + dx + size / 2} {base}z")
        color = BLOOD if i % 2 else "#FF6A3D"
        flames += (
            f'<path d="{low}" fill="{color}" opacity=".9"><animate attributeName="d" values="{low};{high};{low}" dur="{speed}s" repeatCount="indefinite"/></path>'
        )
    fire = (
        f'<g opacity="0">{timed("opacity", "0;0;1;1;0;0", "0;.1;.15;.62;.7;1")}'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 -112;0 -112" keyTimes="0;.12;.62;1" dur="{LOOP}s" repeatCount="indefinite"/>{flames}</g>'
    )
    pdf = (
        f'<g opacity="0">{show(.68)}'
        f'<circle cx="{cx}" cy="{cy + 8}" r="52" fill="#7E0A24" stroke="{HOT}" stroke-width="2.5"/>'
        f'<circle cx="{cx}" cy="{cy + 8}" r="41" fill="none" stroke="#3A0612" stroke-width="2"/>'
        f'<text x="{cx}" y="{cy + 18}" text-anchor="middle" font-family="{SERIF}" font-size="28" font-weight="700" fill="{BONE}">PDF</text></g>'
    )
    return page + fire + pdf


def page(numeral, title, tagline, stack, scene):
    width, height = 480, 300
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{escape(title)}: {escape(tagline)}">
<title>{escape(title)}</title>
<defs>
<radialGradient id="b" cx=".72" cy=".34" r=".9"><stop stop-color="#3A0612"/><stop offset=".55" stop-color="#0F0307"/><stop offset="1" stop-color="#040102"/></radialGradient>
<filter id="n" x="-50%" y="-30%" width="200%" height="160%"><feGaussianBlur stdDeviation="9"/></filter>
<clipPath id="c"><rect width="{width}" height="{height}" rx="12"/></clipPath>
</defs>
<g clip-path="url(#c)"><rect width="{width}" height="{height}" fill="url(#b)"/>
<rect x="11" y="11" width="{width - 22}" height="{height - 22}" rx="6" fill="none" stroke="#6B1228"/>
<text x="30" y="52" font-family="{SERIF}" font-size="15" letter-spacing="4" fill="#FF6B7F">CAPÍTULO</text>
<text x="30" y="150" filter="url(#n)" font-family="{SERIF}" font-size="104" font-weight="700" fill="{BLOOD}">{numeral}<animate attributeName="opacity" values="1;.45;1" dur="4s" repeatCount="indefinite"/></text>
<text x="30" y="150" font-family="{SERIF}" font-size="104" font-weight="700" fill="{BONE}">{numeral}</text>
{scene}
<path d="M30 192H450" stroke="#6B1228"/>
<text x="30" y="227" font-family="{SERIF}" font-size="28" font-weight="700" fill="{BONE}">{escape(title)}</text>
<text x="30" y="252" font-family="{SERIF}" font-size="17" font-style="italic" fill="#E9C4C0">{escape(tagline)}</text>
<text x="30" y="276" font-family="{MONO}" font-size="12.5" font-weight="700" fill="#FF6B7F">{escape("  ✦  ".join(stack))}</text></g>
<rect x=".75" y=".75" width="{width - 1.5}" height="{height - 1.5}" rx="12" fill="none" stroke="#8E1530" stroke-width="1.5"/>
</svg>
"""


def chapters():
    return {
        "chapter-safe": page("I", "SAFE", "Entrada e saída escolar sob controle", ("Laravel", "Vue 3", "SQLite"), lock_scene()),
        "chapter-presenca": page("II", "Controle de presença", "Frequência conectada aos dados", ("Nuxt", "Prisma", "Tailwind"), tally_scene()),
        "chapter-acervo": page("III", "Acervo Digital", "Biblioteca com leitura e IA", ("Nuxt", "Laravel", "Groq API"), book_scene()),
        "chapter-descarte": page("IV", "Descarte de insumos", "Do registro operacional ao PDF", ("React", "TypeScript", "Vite"), fire_scene()),
    }
