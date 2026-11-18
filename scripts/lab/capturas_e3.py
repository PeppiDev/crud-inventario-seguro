"""Capturas Eval 3 del CRUD en Docker (127.0.0.1:8000), datos ficticios.
Uso: python capturas_e3.py <dir_salida> <archivo_cuentas>
Registra en consola_csp.txt los mensajes de consola (violaciones CSP) de cada página."""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8000'
salida = Path(sys.argv[1]); salida.mkdir(parents=True, exist_ok=True)
cuentas = dict(l.split()[:2] for l in Path(sys.argv[2]).read_text().splitlines() if len(l.split()) >= 2)
consola = []

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1100, 'height': 700}, locale='es-CL')
    pg = ctx.new_page()
    pg.on('console', lambda m: consola.append(f'[{m.type}] {pg.url} {m.text}'))

    def foto(nombre):
        pg.wait_for_load_state('networkidle')
        pg.screenshot(path=str(salida / f'{nombre}.png'), full_page=True); print('ok', nombre)

    def login(usuario, clave):
        pg.goto(BASE + '/cuentas/login/')
        pg.fill('#id_username', usuario); pg.fill('#id_password', clave)
        pg.click('form:not([action]) button[type=submit]'); pg.wait_for_load_state()

    def logout():
        pg.goto(BASE + '/'); pg.click('header form button[type=submit]'); pg.wait_for_load_state()

    pg.goto(BASE + '/1/'); foto('01_anonimo_redirige_login')
    login('ana', 'clave-incorrecta-de-prueba'); foto('02_login_invalido')
    login('ana', cuentas['ana']); foto('03_listado_ana')
    pg.goto(BASE + '/1/'); foto('04_detalle_ana_propietaria')
    logout(); foto('05_logout_post')

    login('beto', cuentas['beto'])
    pg.goto(BASE + '/nuevo/')
    pg.fill('#id_nombre', 'Toner negro'); pg.select_option('#id_categoria', 'tecnologia')
    pg.fill('#id_cantidad', '3'); pg.fill('#id_correo_proveedor', 'pedidos@toner-ficticio.cl')
    pg.click('form:not([action]) button[type=submit]'); pg.wait_for_load_state()
    pg.goto(BASE + '/'); foto('06_listado_beto_solo_propios')
    pg.goto(BASE + '/1/'); foto('07_beto_detalle_ajeno_404')
    pg.goto(BASE + '/1/editar/'); foto('08_beto_editar_ajeno_404')
    logout()

    login('sofia', cuentas['sofia'])
    pg.goto(BASE + '/'); foto('09_listado_supervisora_enmascarado')
    pg.goto(BASE + '/1/'); foto('10_detalle_supervisora_enmascarado')
    pg.goto(BASE + '/1/editar/'); foto('11_supervisora_editar_404')
    logout()
    b.close()

(salida / 'consola_csp.txt').write_text('\n'.join(consola) or 'Sin mensajes de consola (0 violaciones CSP).\n')
print('consola:', len(consola))
