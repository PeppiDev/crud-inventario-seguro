**Amenazas STRIDE.**

| ID | STRIDE | Componente | Amenaza | Control | Estado |
|---|---|---|---|---|---|
| S-1 | Spoofing | Login | Fuerza bruta o *credential stuffing* contra `/cuentas/login/` (CWE-307) | Hash PBKDF2 y mensaje de error genérico | **Residual**: falta limitar intentos (p. ej. django-axes) |
| S-2 | Tampering | Formularios y logout | CSRF para crear, editar, borrar o cerrar sesión de otro usuario (CWE-352) | `CsrfViewMiddleware`, logout solo por POST y SameSite=Lax | Controlado (pruebas 403/405) |
| S-3 | Repudiation | CRUD | Un operador niega haber borrado un producto | Solo el log de acceso de gunicorn | **Residual**: falta auditoría por usuario |
| S-4 | Information disclosure | Detalle y listado | IDOR: leer el producto o el correo de otro cambiando el ID (CWE-639) | `get_queryset` por propietario, 404 y enmascarado para el supervisor | Controlado (ZAP: beto 404) |
| S-5 | Information disclosure | Navegador | Caché o lectura de cookies por script (Z-02, M-01) | `no-store`, `csrftoken` HttpOnly y CSP | Corregido |
