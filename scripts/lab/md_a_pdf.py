"""Convierte un Markdown a PDF A4 con el estilo de la presentación. Uso: md_a_pdf.py <entrada.md> <salida.pdf> "<pie>" """
import sys
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

md = Path(sys.argv[1]).read_text(encoding='utf-8')
pie = sys.argv[3] if len(sys.argv) > 3 else ''
body = markdown.markdown(md, extensions=['tables', 'fenced_code', 'attr_list', 'md_in_html'])
css = """
body { font-family: 'Carlito','Calibri','DejaVu Sans',sans-serif; font-size: 11pt; color:#1B2430; line-height:1.5; }
h1 { font-family: 'Caladea','Cambria',serif; color:#0F3D3E; font-size: 22pt; margin:0 0 4pt; }
h1 + p { color:#64748B; margin-top:0; }
h2 { font-family: 'Caladea','Cambria',serif; color:#0F3D3E; font-size: 15pt; border-bottom: 1.5pt solid #0F766E; padding-bottom:3pt; margin-top:16pt; break-after: avoid; }
p { margin: 5pt 0; }
table { border-collapse: collapse; width:100%; margin: 6pt 0 10pt; font-size: 9.5pt; }
th { background:#0F3D3E; color:#fff; text-align:left; padding:4pt 5pt; }
td { border-bottom: 0.5pt solid #CBD5D1; padding:4pt 5pt; vertical-align: top; }
code { font-family:'DejaVu Sans Mono',monospace; font-size: 9pt; background:#EEF3F2; padding:0 2pt; }
img { max-width:100%; display:block; margin:4pt auto; border:0.5pt solid #CBD5D1; }
img.media { max-width:62%; }
img.term { max-width:88%; }
img.chica { max-width:46.5%; display:inline-block; margin:2pt 1%; vertical-align:top; }
.pie { text-align:center; font-size:8.5pt; color:#64748B; margin:0 0 8pt; }
.salto { break-before: page; }
pre { font-size:8pt; background:#EEF3F2; padding:5pt; white-space:pre-wrap; }
td, th { overflow-wrap: anywhere; }
td:first-child { white-space: nowrap; }
hr { border: 0; border-top: 0.5pt solid #CBD5D1; margin: 14pt 0; }
"""
html = f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>"
with sync_playwright() as p:
    tmp = Path(sys.argv[1]).with_suffix('.render.html'); tmp.write_text(html, encoding='utf-8')
    b = p.chromium.launch(); pg = b.new_page(); pg.goto(tmp.resolve().as_uri()); pg.wait_for_load_state('networkidle')
    pg.pdf(path=sys.argv[2], format='A4', print_background=True, display_header_footer=True,
           header_template='<span></span>',
           footer_template=f'<div style="font-size:8pt;color:#64748B;width:100%;text-align:center">{pie} · <span class="pageNumber"></span>/<span class="totalPages"></span></div>',
           margin={'top': '16mm', 'bottom': '18mm', 'left': '16mm', 'right': '16mm'})
    b.close()
tmp.unlink()
print('ok')
