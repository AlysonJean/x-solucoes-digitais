<?php
/**
 * Plugin Name: Selo X Soluções Digitais
 * Description: Coloca o selo "Desenvolvido por X Soluções Digitais" no rodapé. O selo.js é buscado no GitHub pelo servidor e entregue pelo próprio site (/?x-selo=js), então o navegador de quem visita não fala com nenhum terceiro.
 * Version: 1.1.0
 * Author: X Soluções Digitais
 *
 * Instalação: copie este arquivo para wp-content/mu-plugins/ (plugin obrigatório, não aparece
 * para desativar no painel). Para tirar o selo, apague o arquivo e limpe o cache do site.
 * Origem: https://github.com/AlysonJean/x-solucoes-digitais/blob/main/selo/wordpress/x-selo.php
 */

defined( 'ABSPATH' ) || exit;

const X_SELO_FONTE    = 'https://raw.githubusercontent.com/AlysonJean/x-solucoes-digitais/main/selo/selo.js';
const X_SELO_WHATSAPP = '5531935027635';

/**
 * Entrega o selo.js pelo próprio site. A cópia fica guardada por 1 hora. Se o GitHub não
 * responder, vale a última cópia boa; sem nenhuma, sai um arquivo vazio e o link de dentro
 * da tag continua aparecendo.
 */
add_action(
	'init',
	static function (): void {
		if ( ! isset( $_GET['x-selo'] ) || 'js' !== $_GET['x-selo'] ) { // phpcs:ignore WordPress.Security.NonceVerification
			return;
		}
		$js = get_transient( 'x_selo_js' );
		if ( false === $js ) {
			$resposta = wp_remote_get( X_SELO_FONTE, array( 'timeout' => 5 ) );
			if ( ! is_wp_error( $resposta ) && 200 === wp_remote_retrieve_response_code( $resposta ) ) {
				$js = wp_remote_retrieve_body( $resposta );
				update_option( 'x_selo_js_reserva', $js, false );
				set_transient( 'x_selo_js', $js, HOUR_IN_SECONDS );
			} else {
				$js = (string) get_option( 'x_selo_js_reserva', '' );
				set_transient( 'x_selo_js', $js, 5 * MINUTE_IN_SECONDS );
			}
		}
		header( 'Content-Type: application/javascript; charset=utf-8' );
		header( 'Cache-Control: public, max-age=3600' );
		header( 'X-Content-Type-Options: nosniff' );
		echo $js; // phpcs:ignore WordPress.Security.EscapeOutput -- é o selo.js do repositório, não HTML.
		exit;
	},
	0
);

/**
 * Põe o selo no rodapé do tema ou do Elementor: no lugar de um link "Desenvolvido por..." que
 * já exista, ao lado do link da política de privacidade, ou numa faixa no fim do rodapé, nessa
 * ordem. Página sem rodapé fica sem selo.
 * O endereço do script leva a hora (?h=) para uma mudança no selo chegar em até 1 hora,
 * mesmo com a página guardada em cache.
 */
add_action(
	'wp_footer',
	static function (): void {
		if ( is_feed() || is_embed() ) {
			return;
		}
		$site = preg_replace( '/^www\./', '', (string) wp_parse_url( home_url(), PHP_URL_HOST ) );
		?>
<template id="x-selo-modelo"><x-selo site="<?php echo esc_attr( $site ); ?>"><a href="https://wa.me/<?php echo esc_attr( X_SELO_WHATSAPP ); ?>" target="_blank" rel="noopener" style="color: inherit">Desenvolvido por X Soluções Digitais</a></x-selo></template>
<script data-no-optimize="1" data-no-defer="1">
(function () {
	var rodapes = document.querySelectorAll('footer, [data-elementor-type="footer"], .site-footer');
	var rodape = rodapes[rodapes.length - 1];
	var modelo = document.getElementById('x-selo-modelo');
	if (!rodape || !modelo || document.querySelector('x-selo')) return;
	var selo = modelo.content.cloneNode(true);
	var credito = null;
	Array.prototype.forEach.call(rodape.querySelectorAll('a'), function (a) {
		if (!credito && /^\s*desenvolvido por/i.test(a.textContent)) credito = a;
	});
	var politica = rodape.querySelector('a[href*="privacidade"], a[href*="privacy"]');
	if (credito) {
		credito.parentNode.replaceChild(selo, credito);
	} else if (politica) {
		var grupo = document.createElement('span');
		grupo.style.cssText = 'display:inline-flex;flex-wrap:wrap;align-items:center;gap:8px 20px';
		politica.parentNode.insertBefore(grupo, politica);
		grupo.appendChild(politica);
		grupo.appendChild(selo);
	} else {
		var faixa = document.createElement('div');
		faixa.style.cssText = 'text-align:center;padding:12px 16px';
		faixa.appendChild(selo);
		rodape.appendChild(faixa);
	}
	var s = document.createElement('script');
	s.src = '<?php echo esc_js( home_url( '/' ) ); ?>?x-selo=js&h=' + Math.floor(Date.now() / 36e5);
	s.async = true;
	document.head.appendChild(s);
})();
</script>
		<?php
	},
	100
);
