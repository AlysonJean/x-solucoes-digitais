"""Gera todos os arquivos da marca X Soluções Digitais (direção A — Código).

Uso, a partir da raiz do repositório:
    python ferramentas/gerar_marca.py            # SVGs + PNGs
    python ferramentas/gerar_marca.py --so-svg   # só os SVGs

Requisitos: pip install -r ferramentas/requirements.txt
            python -m playwright install chromium   (só para os PNGs)
"""
import io
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

RAIZ = Path(__file__).resolve().parent.parent
FONTES = RAIZ / "ferramentas" / "fontes"
FONT_700 = FONTES / "SpaceGrotesk-Bold.ttf"
FONT_500 = FONTES / "SpaceGrotesk-Medium.ttf"
OUT = RAIZ / "marca"

# ---- Cores da marca ---------------------------------------------------------
INK = "#14161B"         # Tinta
PAPER = "#F4F3EE"       # Papel
ACCENT = "#3D5AFE"      # Azul
ACCENT_DARK = "#8C9BFF" # Azul para fundo escuro em tamanho pequeno
MUTED_DARK = "#A9AEBA"  # "Digitais" no logo de fundo escuro

# ---- Geometria do símbolo (grade 100 x 100) ---------------------------------
# Padrão: traço 14, pontas em 39/61 (vão de 8 entre os chevrons)
STD = {"w": 14, "l": "M15 15 39 50 15 85", "r": "M85 15 61 50 85 85"}
# Pequeno (até 24 px): traço 18, vão de 10 — usado no selo e no favicon
SMALL = {"w": 18, "l": "M16 16 36 50 16 84", "r": "M84 16 64 50 84 84"}


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def symbol(geo, left, right, transform=""):
    t = f' transform="{transform}"' if transform else ""
    return (
        f'<g fill="none" stroke-width="{geo["w"]}" stroke-linecap="round" stroke-linejoin="round"{t}>'
        f'<path d="{geo["l"]}" stroke="{left}"/>'
        f'<path d="{geo["r"]}" stroke="{right}"/></g>'
    )


def svg(viewbox, body, title="X Soluções Digitais"):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" aria-label="{title}">'
        f"<title>{title}</title>{body}</svg>\n"
    )


class Line:
    """Uma linha de texto convertida em curvas, com kerning (HarfBuzz)."""

    def __init__(self, font_path, text, size, tracking_em=-0.02):
        self.tt = TTFont(font_path)
        self.gs = self.tt.getGlyphSet()
        order = self.tt.getGlyphOrder()
        upem = self.tt["head"].unitsPerEm
        self.s = size / upem
        data = io.BytesIO()
        self.tt.save(data)
        font = hb.Font(hb.Face(data.getvalue()))
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(font, buf, {"kern": True, "liga": True})
        track = tracking_em * upem
        self.glyphs = []
        x = 0.0
        n = len(buf.glyph_infos)
        for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
            self.glyphs.append((order[info.codepoint], x + pos.x_offset, pos.y_offset))
            x += pos.x_advance + (track if i < n - 1 else 0)

    def _each(self, pen, x0, baseline):
        for name, gx, gy in self.glyphs:
            tp = TransformPen(pen, (self.s, 0, 0, -self.s, x0 + gx * self.s, baseline - gy * self.s))
            self.gs[name].draw(tp)

    def bounds(self, x0, baseline):
        bp = BoundsPen(self.gs)
        self._each(bp, x0, baseline)
        return bp.bounds

    def path(self, x0, baseline):
        pen = SVGPathPen(self.gs, ntos=fmt)
        self._each(pen, x0, baseline)
        return pen.getCommands()


def build_logo():
    F = 48                 # corpo do texto na grade do símbolo
    cap = 0.70 * F         # altura das maiúsculas
    l1 = Line(FONT_700, "X Soluções", F)
    l2 = Line(FONT_500, "Digitais", F)
    base1, base2 = 8 + cap, 92
    # alinha a borda visual esquerda das duas linhas em x = 116
    x1 = 116 - l1.bounds(0, base1)[0]
    x2 = 116 - l2.bounds(0, base2)[0]
    b1, b2 = l1.bounds(x1, base1), l2.bounds(x2, base2)
    right = max(b1[2], b2[2])
    bottom = max(92, b2[3])
    vb = f"8 8 {fmt(right - 8)} {fmt(bottom - 8)}"
    p1, p2 = l1.path(x1, base1), l2.path(x2, base2)
    variants = {
        "logo-horizontal.svg": (INK, ACCENT, INK, ACCENT),
        "logo-horizontal-fundo-escuro.svg": (PAPER, ACCENT, PAPER, MUTED_DARK),
        "logo-horizontal-preto.svg": (INK, INK, INK, INK),
        "logo-horizontal-branco.svg": ("#FFFFFF",) * 4,
    }
    for name, (sl, sr, t1, t2) in variants.items():
        body = symbol(STD, sl, sr) + f'<path d="{p1}" fill="{t1}"/><path d="{p2}" fill="{t2}"/>'
        (OUT / name).write_text(svg(vb, body), encoding="utf-8")
    return right - 8, bottom - 8


def build_symbols():
    for name, (l, r) in {
        "simbolo.svg": (INK, ACCENT),
        "simbolo-fundo-escuro.svg": (PAPER, ACCENT),
        "simbolo-preto.svg": (INK, INK),
        "simbolo-branco.svg": ("#FFFFFF", "#FFFFFF"),
    }.items():
        (OUT / name).write_text(svg("8 8 84 84", symbol(STD, l, r)), encoding="utf-8")
    (OUT / "simbolo-pequeno.svg").write_text(svg("7 7 86 86", symbol(SMALL, INK, ACCENT)), encoding="utf-8")


def tile(geo, bg, left, right, scale, rx):
    off = 50 - 50 * scale
    t = f"translate({fmt(off)} {fmt(off)}) scale({fmt(scale)})"
    return f'<rect width="100" height="100" rx="{rx}" fill="{bg}"/>' + symbol(geo, left, right, t)


def build_icons():
    ic = OUT / "icones"
    ic.mkdir(exist_ok=True)
    files = {
        # em tamanho pequeno sobre fundo escuro, o azul claro lê melhor
        "favicon.svg": tile(SMALL, INK, PAPER, ACCENT_DARK, 0.66, 22),
        "app-icon.svg": tile(STD, INK, PAPER, ACCENT, 0.58, 0),
        "avatar-claro.svg": tile(STD, PAPER, INK, ACCENT, 0.5, 0),
        "avatar-escuro.svg": tile(STD, INK, PAPER, ACCENT, 0.5, 0),
    }
    for name, body in files.items():
        (ic / name).write_text(svg("0 0 100 100", body), encoding="utf-8")


def build_pngs(logo_w, logo_h):
    from renderizar_png import renderizar  # mesmo diretório

    lh = round(2400 * logo_h / logo_w)
    jobs = [
        ("png/logo-horizontal.png", 2400, lh, "logo-horizontal.svg"),
        ("png/logo-horizontal-fundo-escuro.png", 2400, lh, "logo-horizontal-fundo-escuro.svg"),
        ("png/simbolo.png", 1024, 1024, "simbolo.svg"),
        ("png/simbolo-fundo-escuro.png", 1024, 1024, "simbolo-fundo-escuro.svg"),
        ("icones/avatar-claro-1080.png", 1080, 1080, "icones/avatar-claro.svg"),
        ("icones/avatar-escuro-1080.png", 1080, 1080, "icones/avatar-escuro.svg"),
        ("icones/apple-touch-icon.png", 180, 180, "icones/app-icon.svg"),
        ("icones/icon-512.png", 512, 512, "icones/app-icon.svg"),
        ("icones/favicon-32.png", 32, 32, "icones/favicon.svg"),
        ("icones/favicon-16.png", 16, 16, "icones/favicon.svg"),
    ]
    (OUT / "png").mkdir(exist_ok=True)
    renderizar([(OUT / o, w, h, OUT / s) for o, w, h, s in jobs])


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    w, h = build_logo()
    build_symbols()
    build_icons()
    print("SVGs gerados em", OUT)
    if "--so-svg" not in sys.argv:
        build_pngs(w, h)
        print("PNGs gerados.")
