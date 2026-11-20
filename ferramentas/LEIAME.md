# Ferramentas: gerar os arquivos da marca

Todos os arquivos de `marca/` saem do script `gerar_marca.py`. Para mudar uma cor, a espessura do traço ou o texto do logo, mude o script e gere de novo. Não edite os SVGs na mão, senão eles ficam diferentes uns dos outros.

## Preparar (uma vez)

No terminal, na raiz do repositório:

```powershell
python -m venv .venv
.venv\Scripts\activate          # no Windows (no Linux/Mac: source .venv/bin/activate)
pip install -r ferramentas/requirements.txt
python -m playwright install chromium
```

## Gerar

```powershell
python ferramentas/gerar_marca.py            # SVGs e PNGs
python ferramentas/gerar_marca.py --so-svg   # só os SVGs (não precisa do Playwright)
```

Os arquivos saem direto em `marca/`. Depois é só fazer o commit.

## Onde mexer no `gerar_marca.py`

| Quero mudar | Onde |
|---|---|
| Cores | constantes `INK`, `PAPER`, `ACCENT`… no topo |
| Espessura do traço ou vão entre os chevrons | `STD` (padrão) e `SMALL` (até 24 px) |
| Texto ou tamanho do logo | função `build_logo()` |
| Tamanho dos PNGs | lista `jobs` em `build_pngs()` |

O texto do logo é convertido em curvas com as fontes de `fontes/`, então o SVG final não depende de a fonte estar instalada.
