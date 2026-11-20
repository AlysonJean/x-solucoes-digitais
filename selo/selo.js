/*!
 * Selo de assinatura — X Soluções Digitais
 *
 * Uso:   <script src="URL_DO_SELO/selo.js" defer></script>
 *        <x-selo></x-selo>
 *
 * Atributos (todos opcionais):
 *   site      nome usado no rastreio (padrão: o domínio da página)
 *   tema      auto | claro | escuro         (padrão: auto — segue a cor do texto do rodapé)
 *   variante  completo | compacto | icone   (padrão: completo)
 */
(function () {
  'use strict';

  // ===== Configuração central: mude aqui e todos os sites atualizam =====
  var CONFIG = {
    // Quando o portfólio estiver no ar, coloque a URL aqui (ex.: 'https://xsolucoesdigitais.com.br').
    // Enquanto estiver vazio, o selo abre o WhatsApp com o nome do site na mensagem.
    portfolio: '',
    whatsapp: '5531975808477',
    nome: 'X Soluções Digitais',
    prefixo: 'Desenvolvido por',
    azul: '#3D5AFE',      // azul usado em fundo claro
    azulClaro: '#8C9BFF'  // azul usado em fundo escuro
  };
  // ======================================================================

  if (!window.customElements || customElements.get('x-selo')) return;

  var SIMBOLO =
    '<svg viewBox="7 7 86 86" aria-hidden="true" focusable="false">' +
    '<g fill="none" stroke-width="18" stroke-linecap="round" stroke-linejoin="round">' +
    '<path d="M16 16 36 50 16 84" stroke="currentColor"/>' +
    '<path class="azul" d="M84 16 64 50 84 84"/></g></svg>';

  var CSS =
    ':host{display:inline-block;font-size:13px;line-height:1;vertical-align:middle}' +
    ':host([hidden]){display:none}' +
    ':host([tema="claro"]){color:#14161B}' +
    ':host([tema="escuro"]){color:#F4F3EE}' +
    'a{box-sizing:border-box;display:inline-flex;align-items:center;gap:.6em;min-height:36px;' +
    'padding:0 1.1em;border:1px solid rgba(128,128,128,.35);' +
    'border-color:color-mix(in srgb,currentColor 22%,transparent);border-radius:999px;' +
    'color:inherit;font:inherit;font-size:1em;text-decoration:none;white-space:nowrap;background:transparent}' +
    'a:hover{border-color:color-mix(in srgb,currentColor 45%,transparent);' +
    'background:color-mix(in srgb,currentColor 6%,transparent)}' +
    'a:focus-visible{outline:2px solid var(--azul);outline-offset:2px}' +
    '@media (prefers-reduced-motion:no-preference){a{transition:border-color .2s,background-color .2s}}' +
    'svg{width:1.3em;height:1.3em;flex:none;display:block}' +
    '.azul{stroke:var(--azul)}' +
    '.prefixo{opacity:.8}' +
    '.nome{font-weight:600}' +
    ':host([variante="icone"]) a{padding:0;width:36px;justify-content:center}';

  // Converte qualquer cor CSS em [r, g, b, alfa] (0–255, alfa 0–1). getComputedStyle devolve a cor no
  // formato em que o site escreveu: Tailwind v4 usa oklch(), e há sites com lab(), lch() ou color().
  // O rgb() é lido direto; o resto passa por um canvas de 1 px, que entende tudo o que o navegador entende.
  var ctxCor = null;
  function paraRgba(cor) {
    cor = String(cor);
    var m = /^rgba?\(/i.test(cor) && cor.match(/[\d.]+%?/g);
    if (m && m.length >= 3) {
      var a = m[3] === undefined ? 1 : (m[3].slice(-1) === '%' ? parseFloat(m[3]) / 100 : Number(m[3]));
      return [Number(m[0]), Number(m[1]), Number(m[2]), a];
    }
    try {
      if (!ctxCor) {
        var tela = document.createElement('canvas');
        tela.width = tela.height = 1;
        ctxCor = tela.getContext('2d', { willReadFrequently: true });
      }
      ctxCor.clearRect(0, 0, 1, 1);
      ctxCor.fillStyle = '#000';
      ctxCor.fillStyle = cor;
      ctxCor.fillRect(0, 0, 1, 1);
      var d = ctxCor.getImageData(0, 0, 1, 1).data;
      return [d[0], d[1], d[2], d[3] / 255];
    } catch (e) {
      return [0, 0, 0, 1];
    }
  }

  function luminancia(rgba) {
    var c = rgba.slice(0, 3).map(function (v) {
      v = v / 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
  }

  // O fundo atrás do selo é escuro? Sobe pelos elementos até achar uma cor de fundo sólida e mede ela.
  // Se antes disso aparecer imagem ou degradê, ou se ninguém tiver cor de fundo, decide pela cor do texto:
  // texto claro quer dizer fundo escuro. (Só pelo texto erra no cinza médio sobre branco, ex.: text-gray-400.)
  function fundoEscuro(el) {
    for (var n = el; n && n.nodeType === 1; n = n.parentElement || (n.getRootNode && n.getRootNode().host)) {
      var cs = getComputedStyle(n);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') break;
      var fundo = paraRgba(cs.backgroundColor);
      if (fundo[3] >= 0.5) return luminancia(fundo) < 0.2;
    }
    return luminancia(paraRgba(getComputedStyle(el).color)) > 0.25;
  }

  function destino(site) {
    if (CONFIG.portfolio) {
      var u = new URL(CONFIG.portfolio);
      u.searchParams.set('utm_source', site);
      u.searchParams.set('utm_medium', 'selo');
      u.searchParams.set('utm_campaign', 'assinatura');
      return u.toString();
    }
    var msg = 'Olá! Vi o seu trabalho no site ' + site + ' e quero conversar sobre um projeto.';
    return 'https://wa.me/' + CONFIG.whatsapp + '?text=' + encodeURIComponent(msg);
  }

  function escapar(t) {
    return String(t).replace(/[&<>"]/g, function (ch) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch];
    });
  }

  // Sites com modo claro/escuro: quando o tema da página muda, o azul acompanha.
  var instancias = new Set();
  var agendado = false;
  function reavaliarTodos() {
    if (agendado) return;
    agendado = true;
    requestAnimationFrame(function () {
      agendado = false;
      instancias.forEach(function (el) { el._atualizarTema(); });
    });
  }
  new MutationObserver(reavaliarTodos).observe(document.documentElement, {
    attributes: true, attributeFilter: ['class', 'style', 'data-theme', 'data-mode']
  });
  if (document.body) {
    new MutationObserver(reavaliarTodos).observe(document.body, {
      attributes: true, attributeFilter: ['class', 'style', 'data-theme', 'data-mode']
    });
  }
  if (window.matchMedia) {
    var mq = window.matchMedia('(prefers-color-scheme: dark)');
    if (mq.addEventListener) mq.addEventListener('change', reavaliarTodos);
  }

  class XSelo extends HTMLElement {
    static get observedAttributes() { return ['site', 'tema', 'variante']; }

    connectedCallback() {
      instancias.add(this);
      this._render();
    }

    disconnectedCallback() {
      instancias.delete(this);
    }

    attributeChangedCallback() {
      if (this.isConnected) this._render();
    }

    _render() {
      var root = this.shadowRoot || this.attachShadow({ mode: 'open' });
      var variante = this.getAttribute('variante') || 'completo';
      var site = this.getAttribute('site') || location.hostname.replace(/^www\./, '') || 'site';
      var rotulo = CONFIG.prefixo + ' ' + CONFIG.nome;
      var texto = '';
      if (variante === 'completo') {
        texto = '<span class="prefixo">' + escapar(CONFIG.prefixo) + '</span>' +
          '<span class="nome">' + escapar(CONFIG.nome) + '</span>';
      } else if (variante === 'compacto') {
        texto = '<span class="nome">' + escapar(CONFIG.nome) + '</span>';
      }
      var extra = variante === 'completo' ? '' :
        ' aria-label="' + escapar(rotulo) + '" title="' + escapar(rotulo) + '"';

      root.innerHTML =
        '<style>' + CSS + '</style><style data-tema></style>' +
        '<a href="' + escapar(destino(site)) + '" target="_blank" rel="noopener"' + extra + '>' +
        SIMBOLO + texto + '</a>';
      this._atualizarTema();
    }

    _atualizarTema() {
      var root = this.shadowRoot;
      if (!root) return;
      var tema = this.getAttribute('tema') || 'auto';
      var escuro = tema === 'escuro' || (tema === 'auto' && fundoEscuro(this));
      var alvo = root.querySelector('style[data-tema]');
      if (alvo) alvo.textContent = ':host{--azul:' + (escuro ? CONFIG.azulClaro : CONFIG.azul) + '}';
    }
  }

  customElements.define('x-selo', XSelo);
})();
