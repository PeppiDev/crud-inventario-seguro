## 7. Conclusiones

**SAST y DAST se complementan.**

- **SonarQube (SAST)** encontró problemas que solo se ven en el código: la clave secreta escrita en `settings.py` y el `COPY . .` del Dockerfile. ZAP no puede ver ninguno de los dos.
- **ZAP (DAST)** encontró problemas que solo existen en ejecución: cabeceras faltantes (CSP), atributos de cookies y un CORS abierto que agregó una dependencia (WhiteNoise), no nuestro código. SonarQube no los marcó.
- **Ninguna de las dos** detecta sola un fallo de autorización (IDOR). Eso lo cubrimos con pruebas automáticas y con el recorrido cruzado ana/beto/sofia en ZAP.
- **También hay falsos positivos (Z-05)**, que se confirman con verificación manual.
- **Las correcciones también hay que verificarlas.** El primer re-análisis de ZAP encontró Z-06 y el de Sonar encontró S6470, ambos nuevos. Por eso hicimos un ciclo más de corrección en cada herramienta.

**Riesgos residuales.**

1. No se limitan los intentos de login (S-1).
2. No hay registro de auditoría por usuario (S-3).
3. SQLite y sus respaldos no se cifran en reposo.
4. El enmascarado es solo de presentación.
5. El laboratorio usa HTTP. En producción las cookies Secure y HSTS dependen de `DJANGO_HTTPS=True`.
6. La clave de respaldo de la v1 (`django-insecure-…`) sigue visible en el historial público de git. Nunca se usó en producción (PythonAnywhere toma la suya de `.env`) y no debe reutilizarse.
7. Solo hicimos escaneo pasivo; un escaneo activo autorizado podría encontrar más.
8. Estos cambios todavía no se despliegan en PythonAnywhere.

**Aportes.** Ver la tabla de la sección 1. Ambos revisamos los hallazgos y las decisiones antes de cerrar cada corrección.
