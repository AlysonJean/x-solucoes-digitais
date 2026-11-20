# Selo de assinatura — X Soluções Digitais

Um único arquivo (`selo.js`) que coloca o selo "Desenvolvido por X Soluções Digitais" no rodapé de qualquer site. O selo:

- **Se adapta ao rodapé sozinho.** Usa a cor do texto do rodapé e troca o tom do azul em fundo escuro, inclusive quando o site muda entre modo claro e escuro.
- **Não interfere no site.** O estilo fica isolado (Shadow DOM): o CSS do site não quebra o selo, e o selo não mexe no site.
- **Rastreia a origem.** Cada clique leva o nome do site. Hoje abre o WhatsApp com a mensagem "Vi o seu trabalho no site X…". Quando o portfólio estiver no ar, passa a abrir a página com `utm_source=<site>`.
- **Tem plano B.** O link de dentro da tag aparece se o script não carregar.

## 1. Hospedar o `selo.js` (uma vez)

Hospede o arquivo num lugar só, e todos os sites carregam dele. Assim, uma mudança no arquivo vale para todos.

**Opção recomendada, grátis: este repositório + jsDelivr**
1. Suba este repositório no GitHub como **público** (`AlysonJean/x-solucoes-digitais`). O jsDelivr só lê repositórios públicos.
2. O endereço do selo fica: `https://cdn.jsdelivr.net/gh/AlysonJean/x-solucoes-digitais@main/selo/selo.js`
3. O jsDelivr guarda cópia em cache. A action `.github/workflows/limpar-cache-selo.yml` limpa o cache sozinha a cada push que altera o `selo.js`. Para limpar na mão, acesse
   `https://purge.jsdelivr.net/gh/AlysonJean/x-solucoes-digitais@main/selo/selo.js`.
4. O navegador também guarda cópia: o jsDelivr manda guardar por **7 dias**. Por isso os exemplos abaixo põem a hora no endereço (`?h=`, horas inteiras desde 1970, em UTC). A cada hora o endereço muda, o navegador busca a versão nova, e uma mudança no selo chega a todo mundo em até uma hora. O jsDelivr ignora o parâmetro no cache dele, então todos os visitantes dividem a mesma cópia. A hora é calculada no navegador, e não no servidor, porque o HTML da página costuma vir de cache.

Quando tiver o domínio próprio, é só mover para `https://xsolucoesdigitais.com.br/selo.js` e trocar o endereço nos sites.

## 2. Colocar no site

### HTML puro, WordPress, qualquer site

Antes de `</body>`:

```html
<script>
(function () {
  var s = document.createElement('script');
  s.src = 'https://cdn.jsdelivr.net/gh/AlysonJean/x-solucoes-digitais@main/selo/selo.js?h=' + Math.floor(Date.now() / 36e5);
  s.async = true;
  s.referrerPolicy = 'no-referrer';
  document.head.appendChild(s);
})();
</script>
```

Se a CSP do site bloquear script dentro do HTML (`script-src` sem `'unsafe-inline'`), ponha esse código num arquivo `.js` do próprio site e carregue o arquivo com `<script src="..." defer>`.

No rodapé:

```html
<x-selo site="nome-do-site">
  <a href="https://wa.me/5531975808477" style="color: inherit">Desenvolvido por X Soluções Digitais</a>
</x-selo>
```

### React com Vite (ex.: X Produções)

1. Peça o script pelo rodapé, com a hora no endereço. Exemplo pronto, com testes: `src/utils/seloAssinatura.ts` da X Produções (`carregarSeloAssinatura()`, chamada num `useEffect` do rodapé). Também serve o código da seção acima no `index.html`.
2. No componente do rodapé:

```jsx
<x-selo site="xproducoeseeventos.com.br">
  <a href="https://wa.me/5531975808477" style="color: inherit">Desenvolvido por X Soluções Digitais</a>
</x-selo>
```

### Next.js (ex.: PrepareC, Xcotas, LuhMoura)

Crie `components/selo-script.tsx`:

```tsx
'use client';

import { useEffect } from 'react';

const SELO_URL = 'https://cdn.jsdelivr.net/gh/AlysonJean/x-solucoes-digitais@main/selo/selo.js';

export function SeloScript() {
  useEffect(() => {
    if (customElements.get('x-selo') || document.querySelector('script[data-x-selo]')) return;
    const script = document.createElement('script');
    script.src = `${SELO_URL}?h=${Math.floor(Date.now() / 3_600_000)}`;
    script.async = true;
    script.referrerPolicy = 'no-referrer';
    script.dataset.xSelo = '';
    document.head.appendChild(script);
  }, []);
  return null;
}
```

No componente do rodapé:

```tsx
import { SeloScript } from '@/components/selo-script';

<x-selo site="preparec.com.br">
  <a href="https://wa.me/5531975808477" style="color: inherit">Desenvolvido por X Soluções Digitais</a>
</x-selo>
<SeloScript />
```

Se o site tiver CSP, libere `https://cdn.jsdelivr.net` no `script-src`. Outra saída, usada no Xofertas: servir o selo pelo próprio site, numa rota `/selo.js` que busca o arquivo no GitHub (`src/app/selo.js/route.ts` do Xofertas).

Com TypeScript, crie `x-selo.d.ts` para o editor aceitar a tag:

```ts
import 'react';

declare module 'react' {
  namespace JSX {
    interface IntrinsicElements {
      'x-selo': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement> & {
        site?: string;
        tema?: 'auto' | 'claro' | 'escuro';
        variante?: 'completo' | 'compacto' | 'icone';
      };
    }
  }
}
```

## 3. Opções

| Atributo   | Valores                              | Padrão              |
|------------|--------------------------------------|---------------------|
| `site`     | qualquer texto                       | domínio da página   |
| `tema`     | `auto`, `claro`, `escuro`            | `auto`              |
| `variante` | `completo`, `compacto`, `icone`      | `completo`          |

- **completo**: símbolo + "Desenvolvido por" + "X Soluções Digitais"
- **compacto**: símbolo + "X Soluções Digitais", para rodapés apertados
- **icone**: só o símbolo, com o texto no `title` e no `aria-label`

Tamanho: o selo usa 13 px por padrão. Para mudar, no CSS do site: `x-selo { font-size: 14px; }`

## 4. Quando o portfólio estiver no ar

No topo do `selo.js`, preencha:

```js
portfolio: 'https://xsolucoesdigitais.com.br',
```

Todos os sites passam a levar para o portfólio com `?utm_source=<site>&utm_medium=selo&utm_campaign=assinatura`. No Google Analytics, em Aquisição › Origem, aparece qual site trouxe cada visita.

## 5. Antes de colocar em site de cliente

Combine o selo no contrato ou na proposta. Uma linha resolve: "O rodapé do site incluirá o selo de autoria da X Soluções Digitais."

Para testar, abra o `exemplo.html` desta pasta no navegador.
