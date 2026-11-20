# Marca X Soluções Digitais: qual arquivo usar

## Logotipo (texto já em curvas, abre em qualquer programa)
| Arquivo | Onde usar |
|---|---|
| `logo-horizontal.svg` | Fundo claro (padrão) |
| `logo-horizontal-fundo-escuro.svg` | Fundo escuro |
| `logo-horizontal-preto.svg` / `-branco.svg` | Uma cor só: carimbo, gravação, impressão simples |
| `png/logo-horizontal*.png` | Onde não aceita SVG (Canva, Word, e-mail), 2400 px, fundo transparente |

## Símbolo
| Arquivo | Onde usar |
|---|---|
| `simbolo.svg` / `simbolo-fundo-escuro.svg` | Símbolo sozinho, a partir de 24 px |
| `simbolo-pequeno.svg` | Abaixo de 24 px (traço mais grosso, para os chevrons não se fundirem) |
| `simbolo-preto.svg` / `simbolo-branco.svg` | Uma cor só |

## Ícones
| Arquivo | Onde usar |
|---|---|
| `icones/avatar-claro-1080.png` / `avatar-escuro-1080.png` | Foto de perfil (Instagram, LinkedIn, WhatsApp Business). O corte redondo não corta o símbolo |
| `icones/favicon.svg` + `favicon-32.png` + `favicon-16.png` | Aba do navegador no seu site |
| `icones/apple-touch-icon.png` (180) / `icon-512.png` | Atalho no celular / PWA |

## Regras
- **Respiro:** deixe pelo menos ¼ da altura do símbolo livre em volta do logo.
- **Tamanho mínimo:** logo com 120 px de largura; símbolo com 16 px (use a versão pequena).
- **Cores:** Tinta `#14161B` · Azul `#3D5AFE` · Papel `#F4F3EE` · Grafite `#5A5F6B` · Azul para fundo escuro em tamanho pequeno `#8C9BFF`
- **Fontes (gratuitas, Google Fonts):** Space Grotesk (marca e títulos) e JetBrains Mono (detalhes)
- **Não fazer:** esticar, girar, trocar as cores dos chevrons entre si, aplicar sombra ou contorno.

Favicon no `<head>` do site:
```html
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
```
