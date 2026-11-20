# X Soluções Digitais

Identidade visual e selo de assinatura da **X Soluções Digitais**: sites, sistemas e automação, por Alyson Jean.

<img src="marca/logo-horizontal.svg" alt="X Soluções Digitais" width="320">

## O que tem aqui

```
x-solucoes-digitais/
├── marca/          logos, símbolo, ícones e favicons (SVG e PNG) + guia de uso
├── selo/           selo "Desenvolvido por" para o rodapé dos sites
│   ├── selo.js        o componente (um arquivo, sem dependências)
│   ├── exemplo.html   página de teste, abra no navegador
│   └── LEIAME.md      instalação em HTML, React e Next.js
├── ferramentas/    scripts que geram os arquivos da marca a partir do código
└── .github/        action que atualiza o cache do selo a cada push
```

- **Usar a marca:** veja [`marca/LEIAME.md`](marca/LEIAME.md). Lá diz qual arquivo usar em cada lugar.
- **Colocar o selo num site:** veja [`selo/LEIAME.md`](selo/LEIAME.md).
- **Mudar cor, traço ou texto do logo:** edite `ferramentas/gerar_marca.py` e gere tudo de novo (veja [`ferramentas/LEIAME.md`](ferramentas/LEIAME.md)).

## Selo em uma linha

```html
<script src="https://cdn.jsdelivr.net/gh/AlysonJean/x-solucoes-digitais@main/selo/selo.js" defer></script>
<x-selo site="nome-do-site"></x-selo>
```

Funciona só com o repositório **público** no GitHub, porque o jsDelivr só lê repositórios públicos.

## Cores e fontes

| Nome | Hex |
|---|---|
| Tinta | `#14161B` |
| Azul | `#3D5AFE` |
| Papel | `#F4F3EE` |
| Grafite | `#5A5F6B` |
| Azul em fundo escuro (tamanho pequeno) | `#8C9BFF` |

Fontes: **Space Grotesk** (marca e títulos) e **JetBrains Mono** (detalhes). As duas são gratuitas, no Google Fonts.

## Direitos

A marca X Soluções Digitais (nome, símbolo e logotipo) pertence a Alyson Jean e não pode ser usada por terceiros. A fonte Space Grotesk em `ferramentas/fontes/` é distribuída sob a SIL Open Font License (veja `OFL.txt`).
