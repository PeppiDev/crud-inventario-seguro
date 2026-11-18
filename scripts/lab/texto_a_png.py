"""Renderiza un archivo de texto como captura de terminal. Uso: python texto_a_png.py <entrada.txt> <salida.png> [filtro_regex]"""
import html
import re
import sys

from playwright.sync_api import sync_playwright

entrada, salida = sys.argv[1], sys.argv[2]
import os
ANCHO = int(os.environ.get('ANCHO', '1300'))
lineas = open(entrada, encoding='utf-8').read().splitlines()
if len(sys.argv) > 3:
    patron = re.compile(sys.argv[3])
    lineas = [l for l in lineas if patron.search(l)]

def color(l):
    e = html.escape(l)
    if re.search(r'\bFAIL\b|FAILED|AssertionError|RECHAZADO', l): return f'<span style="color:#f87171">{e}</span>'
    if re.search(r'\.\.\. ok$|^OK$|ACEPTADO', l): return f'<span style="color:#4ade80">{e}</span>'
    if l.startswith(('$', '#')): return f'<span style="color:#93c5fd">{e}</span>'
    return e

cuerpo = '\n'.join(color(l) for l in lineas)
pagina = f'''<html><body style="margin:0;background:#0f172a"><pre style="font:15px/1.45 'DejaVu Sans Mono',monospace;color:#e2e8f0;padding:22px 26px;margin:0;white-space:pre-wrap;width:{ANCHO-50}px">{cuerpo}</pre></body></html>'''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': ANCHO, 'height': 200})
    pg.set_content(pagina); pg.screenshot(path=salida, full_page=True); b.close()
print('ok', salida)
