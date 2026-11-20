"""Renderiza SVGs em PNG com fundo transparente, usando o Chromium do Playwright.

Uso direto: python ferramentas/renderizar_png.py saida.png largura altura entrada.svg
"""
import sys
from pathlib import Path


def renderizar(jobs):
    """jobs: lista de (saida_png, largura, altura, entrada_svg)."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for out, w, h, src in jobs:
            svg = Path(src).read_text(encoding="utf-8")
            page.set_viewport_size({"width": int(w), "height": int(h)})
            page.set_content(
                "<html><body style='margin:0;background:transparent'>"
                f"<div style='width:{w}px;height:{h}px;display:flex'>"
                f"<style>svg{{width:100%;height:100%;display:block}}</style>{svg}</div></body></html>"
            )
            page.screenshot(path=str(out), omit_background=True,
                            clip={"x": 0, "y": 0, "width": int(w), "height": int(h)})
            print("ok", out)
        browser.close()


if __name__ == "__main__":
    out, w, h, src = sys.argv[1:5]
    renderizar([(out, int(w), int(h), src)])
