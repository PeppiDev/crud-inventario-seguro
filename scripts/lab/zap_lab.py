"""Recorrido manual reproducible del CRUD a través del proxy de OWASP ZAP.

Uso:
  uv run -q --with playwright python zap_lab.py <etiqueta> <dir_salida> <archivo_cuentas>

Requisitos: ZAP en modo daemon escuchando en 127.0.0.1:8090 (API con clave en
la variable ZAP_API_KEY) y el CRUD en http://127.0.0.1:8000 (Docker Compose).

Pasos:
 1. Sesión nueva de ZAP y contexto limitado a http://127.0.0.1:8000.
 2. Chromium headless usa ZAP como proxy (sin excepción para loopback) y
    recorre: login inválido, login válido, CRUD completo, acceso cruzado
    a un registro ajeno, supervisor en solo lectura y logout por POST.
 3. Espera a que termine el análisis pasivo.
 4. Exporta reportes HTML, JSON y Markdown filtrados al objetivo y guarda
    las URL visitadas y los hosts vistos en el árbol Sites.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

ZAP = 'http://127.0.0.1:8090'
KEY = os.environ['ZAP_API_KEY']
OBJETIVO = 'http://127.0.0.1:8000'
CONTEXTO = 'crud-lab'


def api(ruta, **params):
    params['apikey'] = KEY
    url = f'{ZAP}/JSON/{ruta}/?{urllib.parse.urlencode(params)}'
    # La API se consulta directo, sin pasar por el proxy.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(url, timeout=120) as r:
        return json.load(r)


def leer_cuentas(ruta):
    cuentas = {}
    for linea in Path(ruta).read_text().splitlines():
        partes = linea.split()
        if len(partes) >= 2:
            cuentas[partes[0]] = partes[1]
    return cuentas


def login(page, usuario, clave):
    page.goto(f'{OBJETIVO}/cuentas/login/')
    page.fill('#id_username', usuario)
    page.fill('#id_password', clave)
    page.click('form:not([action]) button[type=submit]')
    page.wait_for_load_state()


def logout(page):
    page.goto(f'{OBJETIVO}/')
    page.click('header form button[type=submit]')
    page.wait_for_load_state()


def crear(page, nombre, categoria, cantidad, correo):
    page.goto(f'{OBJETIVO}/nuevo/')
    page.fill('#id_nombre', nombre)
    page.select_option('#id_categoria', categoria)
    page.fill('#id_cantidad', str(cantidad))
    page.fill('#id_correo_proveedor', correo)
    page.click('form:not([action]) button[type=submit]')
    page.wait_for_load_state()


def recorrido(cuentas, registro):
    with sync_playwright() as p:
        navegador = p.chromium.launch(args=[
            f'--proxy-server={ZAP.removeprefix("http://")}',
            '--proxy-bypass-list=<-loopback>',
        ])
        ctx = navegador.new_context()
        page = ctx.new_page()

        def paso(texto):
            registro.append(texto)
            print(' -', texto)

        page.goto(f'{OBJETIVO}/')
        paso('GET / sin sesión (redirige al login)')
        login(page, 'ana', 'clave-incorrecta-de-prueba')
        paso('Login inválido de ana')
        login(page, 'ana', cuentas['ana'])
        paso('Login válido de ana')
        crear(page, 'Resma carta', 'oficina', 50, 'ventas@papelera-ficticia.cl')
        crear(page, 'Cloro 1L', 'limpieza', 12, 'contacto@limpieza-ficticia.cl')
        crear(page, 'Cantidad fuera de rango', 'oficina', 10000, 'x@ficticio.cl')
        paso('Crear 2 productos y 1 rechazado por validación (cantidad 10000)')
        page.goto(f'{OBJETIVO}/')
        page.click('text=Resma carta')
        page.wait_for_load_state()
        id_resma = page.url.rstrip('/').split('/')[-1]
        page.goto(f'{OBJETIVO}/{id_resma}/editar/')
        page.fill('#id_cantidad', '45')
        page.click('form:not([action]) button[type=submit]')
        page.wait_for_load_state()
        paso(f'Detalle y edición del producto {id_resma}')
        page.goto(f'{OBJETIVO}/')
        page.click('text=Cloro 1L')
        page.wait_for_load_state()
        id_cloro = page.url.rstrip('/').split('/')[-1]
        page.goto(f'{OBJETIVO}/{id_cloro}/eliminar/')
        page.click('form:not([action]) button[type=submit]')
        page.wait_for_load_state()
        paso(f'Eliminar el producto {id_cloro}')
        logout(page)
        paso('Logout por POST con CSRF')

        login(page, 'beto', cuentas['beto'])
        paso('Login válido de beto')
        for ruta in (f'/{id_resma}/', f'/{id_resma}/editar/', f'/{id_resma}/eliminar/'):
            r = page.goto(f'{OBJETIVO}{ruta}')
            paso(f'beto pide {ruta} (producto de ana) -> {r.status}')
        logout(page)

        login(page, 'sofia', cuentas['sofia'])
        page.goto(f'{OBJETIVO}/')
        r = page.goto(f'{OBJETIVO}/{id_resma}/')
        paso(f'sofia (supervisora) ve el detalle {id_resma} -> {r.status}')
        r = page.goto(f'{OBJETIVO}/{id_resma}/editar/')
        paso(f'sofia intenta editar {id_resma} -> {r.status}')
        logout(page)

        r = page.goto(f'{OBJETIVO}/{id_resma}/')
        paso(f'Sin sesión, GET /{id_resma}/ -> {r.status} {page.url}')
        navegador.close()


def main():
    etiqueta, salida, archivo_cuentas = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
    salida.mkdir(parents=True, exist_ok=True)
    cuentas = leer_cuentas(archivo_cuentas)

    version = api('core/view/version')['version']
    api('core/action/newSession', name=f'crud-{etiqueta}', overwrite='true')
    api('context/action/newContext', contextName=CONTEXTO)
    api('context/action/includeInContext', contextName=CONTEXTO, regex=r'http://127\.0\.0\.1:8000.*')
    inicio = time.strftime('%Y-%m-%d %H:%M:%S %z')

    registro = []
    recorrido(cuentas, registro)

    while int(api('pscan/view/recordsToScan')['recordsToScan']) > 0:
        time.sleep(2)

    urls = sorted(set(api('core/view/urls', baseurl=OBJETIVO)['urls']))
    hosts = api('core/view/hosts')['hosts']
    mensajes = api('core/view/numberOfMessages', baseurl=OBJETIVO)['numberOfMessages']
    alertas = api('alert/view/alertsSummary', baseurl=OBJETIVO)['alertsSummary']
    resumen = {
        'etiqueta': etiqueta, 'zap_version': version, 'inicio': inicio,
        'objetivo': OBJETIVO, 'contexto': CONTEXTO, 'mensajes': mensajes,
        'hosts_en_sites': hosts, 'urls_visitadas': urls, 'pasos': registro,
        'resumen_alertas': alertas,
    }
    (salida / 'cobertura.json').write_text(json.dumps(resumen, indent=2, ensure_ascii=False))

    for plantilla, ext in (('traditional-html', 'html'), ('traditional-json', 'json'), ('traditional-md', 'md')):
        api('reports/action/generate', title=f'CRUD Inventario - ZAP {etiqueta}',
            template=plantilla, sites=OBJETIVO, contexts=CONTEXTO,
            reportDir='/zap/wrk', reportFileName=f'zap_{etiqueta}.{ext}')
    print(json.dumps({k: resumen[k] for k in ('zap_version', 'mensajes', 'hosts_en_sites', 'resumen_alertas')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
