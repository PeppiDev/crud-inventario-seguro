"""Extrae de ZAP la petición y respuesta (solo cabeceras) de una URL, sin secretos.

Uso: python zap_evidencia.py <url> <metodo> <archivo_salida> [n-esima coincidencia, desde 0]
Los valores de las cookies (sessionid, csrftoken) y del cuerpo se reemplazan
por [OCULTO]; se conserva el nombre de la cookie y sus atributos.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ZAP = 'http://127.0.0.1:8090'
KEY = os.environ['ZAP_API_KEY']


def api(ruta, **params):
    params['apikey'] = KEY
    url = f'{ZAP}/JSON/{ruta}/?{urllib.parse.urlencode(params)}'
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(url, timeout=60) as r:
        return json.load(r)


def ocultar(cabeceras):
    cabeceras = re.sub(r'(sessionid|csrftoken)=[^;\s]+', r'\1=[OCULTO]', cabeceras)
    return cabeceras.strip()


def main():
    url, metodo, salida = sys.argv[1], sys.argv[2], sys.argv[3]
    n = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    mensajes = api('core/view/messages', baseurl=url)['messages']
    coincidencias = [m for m in mensajes
                     if m['requestHeader'].split('\r\n', 1)[0].startswith((f'{metodo} {url} ', f'{metodo} {url}?'))]
    if len(coincidencias) <= n:
        sys.exit(f'sin mensajes para {metodo} {url}')
    m = coincidencias[n]
    texto = (f'# Mensaje ZAP id {m["id"]}\n\n## Petición\n{ocultar(m["requestHeader"])}\n'
             f'[cuerpo omitido]\n\n## Respuesta\n{ocultar(m["responseHeader"])}\n[cuerpo omitido]\n')
    with open(salida, 'w') as f:
        f.write(texto)
    print(texto)


if __name__ == '__main__':
    main()
