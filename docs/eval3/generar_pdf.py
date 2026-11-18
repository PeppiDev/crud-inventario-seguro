"""Une las secciones del informe y genera el PDF.
Uso (desde la raíz del repo):
  uv run --with playwright --with markdown python docs/eval3/generar_pdf.py
Requiere una vez: uv run --with playwright playwright install chromium"""
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
orden = ['01-identificacion', '02-sonarqube-login', '03-datos-sesiones', '04-docker',
         '05-zap-inicial', '05b-stride', '06-correcciones', '07-conclusiones', '08-fuentes']
md = '\n\n'.join((AQUI / f'{n}.md').read_text(encoding='utf-8').rstrip() for n in orden) + '\n'
(AQUI / 'Informe_Eval3.md').write_text(md, encoding='utf-8')
subprocess.run([sys.executable, str(AQUI.parent.parent / 'scripts/lab/md_a_pdf.py'), str(AQUI / 'Informe_Eval3.md'),
                str(AQUI / 'Informe_Eval3_Ulloa_Castillo.pdf'), 'Evaluación 3 · Desarrollo Seguro · Ulloa – Castillo'], check=True)
