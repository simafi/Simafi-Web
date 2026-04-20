# Plan de despliegue — SIMAFI Web (Django + MySQL)

Presupuesto orientativo: **10–20 USD/mes**.  
Contexto: varios municipios en la misma aplicación, sesión por credenciales, archivos en `MEDIA`, stack **Django + MySQL**.

## Archivos en el repositorio (VPS Linux)

| Archivo / carpeta | Uso |
|-------------------|-----|
| `requirements.txt` | Dependencias (incluye `gunicorn`, `python-dotenv`). |
| `.env.example` | Plantilla de variables; copiar a `.env` o `/etc/simafi.env` en el servidor. |
| `deploy/gunicorn.conf.py` | Configuración de Gunicorn. |
| `deploy/systemd/simafi-gunicorn.service.example` | Unidad systemd (copiar a `/etc/systemd/system/`). |
| `deploy/nginx/simafi.conf.example` | Proxy inverso + `/static/` y `/media/`. |
| `deploy/README.md` | Comandos de referencia. |

`settings.py` lee variables `DJANGO_*` (ver `.env.example`) y activa cabeceras HTTPS cuando `DEBUG=0`.

---

## 1. Recomendación de hosting (mejor encaje precio/rendimiento)

### Opción recomendada: **VPS Linux + todo en un servidor**

| Componente | Elección |
|------------|----------|
| **Servidor** | VPS con **Ubuntu Server 22.04 LTS** (o 24.04 LTS) |
| **App** | **Gunicorn** + **Nginx** (reverse proxy + HTTPS + estáticos/media) |
| **Base de datos** | **MySQL 8** o **MariaDB 10.11+** en el **mismo VPS** |
| **Archivos** | Disco del VPS (`MEDIA_ROOT`) con **copias de seguridad** periódicas |

**Por qué esta opción en 10–20 USD/mes**

- Una **base MySQL gestionada** (RDS, DigitalOcean Managed DB) suele **comerse solo** buena parte del presupuesto; en esta franja es más estable **MySQL/MariaDB en el mismo VPS** bien configurado.
- **Un solo despliegue** sirve para todos los municipios (multi-tenant con campo `empresa` / sesión).
- Control total de **Nginx**, **límites de subida**, **SSL** y **backups**.

### Proveedores típicos (referencia de mercado, 2026)

| Proveedor | Notas |
|-----------|--------|
| **Hetzner Cloud** | Muy buena relación precio/RAM en Europa; CX/CPX según stock. |
| **DigitalOcean** | “Droplet” desde ~12 USD/mes; documentación clara en inglés. |
| **Vultr / Linode (Akamai)** | Similar a DO; elegir región cercana a Honduras/Centroamérica si existe. |
| **OVH / otros EU** | Alternativa si preferís facturación o soporte en otro idioma. |

**Tamaño orientativo:** **2 vCPU, 4 GB RAM**, SSD **80 GB** mínimo (subidas PDF/documentos crecen con el tiempo). Si solo hay **10 USD** estrictos, se puede arrancar con **2 GB RAM** y vigilar memoria (swap, workers Gunicorn).

**No incluido en el precio del VPS:** dominio (~10–15 USD/año) y, si se usa, correo profesional aparte.

---

## 2. Alternativa si priorizáis “menos servidor”

- **PaaS** (Railway, Render, Fly.io): cómodo para despliegue por Git; en 10–20 USD hay que revisar **MySQL de pago**, **disco persistente** para `MEDIA` y **límites de RAM**. Puede encajar, pero suele ser **más caro o más frágil** que un VPS para esta carga.

---

## 3. Despliegue — fases

### Fase 0 — Pre-requisitos

- [ ] Dominio (DNS apuntando al VPS cuando exista IP fija).
- [ ] Acceso **SSH** al VPS (clave pública, usuario sin privilegios root para la app).
- [ ] Repositorio Git con el código (sin `SECRET_KEY` ni contraseñas commiteadas).

### Fase 1 — Servidor base

1. Actualizar sistema (`apt update && apt upgrade`).
2. Firewall: **solo 22 (SSH), 80, 443**; MySQL **no** expuesto a internet (solo `localhost` o red privada).
3. Crear usuario de sistema para la aplicación (ej. `simafi`).
4. Instalar **Python** (misma familia de versión que en desarrollo), **venv**, **pip**.

### Fase 2 — MySQL / MariaDB

1. Instalar **MariaDB** o **MySQL**.
2. Crear **base de datos** y **usuario** con permisos solo sobre esa BD.
3. Contraseña fuerte guardada en **variables de entorno** (no en el código).

### Fase 3 — Aplicación Django

1. Clonar repositorio en `/srv/simafi/app` (ruta de ejemplo).
2. Crear `venv`, instalar `requirements.txt`.
3. Variables de entorno (archivo `.env` no versionado o `/etc/simafi.env` con permisos restrictivos):
   - `DJANGO_SETTINGS_MODULE`
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS` (dominio/s)
   - Credenciales `DATABASES` (host `127.0.0.1`, puerto, usuario, contraseña, nombre BD)
   - `DJANGO_EMAIL_*` / SMTP si envían correo
4. `python manage.py migrate`
5. `python manage.py collectstatic` → `STATIC_ROOT`
6. Probar `manage.py check --deploy` y corregir avisos críticos.

### Fase 4 — Gunicorn + systemd

1. Gunicorn escuchando en **socket Unix** o `127.0.0.1:8001`.
2. Unidad **systemd** para arranque automático y reinicio ante fallos.
3. Ajustar **número de workers** según RAM (no saturar el VPS).

### Fase 5 — Nginx

1. `server` para el dominio: `proxy_pass` a Gunicorn.
2. **Let’s Encrypt** (certbot) para **HTTPS** y redirección HTTP → HTTPS.
3. `location /static/` → `STATIC_ROOT`.
4. `location /media/` → `MEDIA_ROOT` (o mismo volumen que la app).
5. `client_max_body_size` acorde a PDFs/documentos subidos.

### Fase 6 — Datos y operación

1. **Backup diario** de la BD (mysqldump o script) + retención (7/30 días).
2. **Backup periódico** de `MEDIA` (documentos de proveedores, ciudadano, etc.).
3. Copias en **otro sitio** (S3 compatible, otro servidor o descarga cifrada); el VPS no debe ser la única copia.
4. Monitorización mínima (ping o uptime) y revisión de **logs** (Nginx + Gunicorn).

### Fase 7 — Post-despliegue

1. Probar login por municipio, listados filtrados y **descarga de adjuntos**.
2. Verificar que **no** se accede a datos de otro municipio cambiando IDs en la URL (pruebas de aislamiento).
3. Documentar **quién** tiene acceso SSH y al panel de administración.

---

## 4. Checklist de seguridad (imprescindible)

- [ ] `DEBUG=False` en producción.
- [ ] `SECRET_KEY` única y secreta.
- [ ] HTTPS obligatorio.
- [ ] MySQL sin puerto público; usuario de BD con permisos mínimos.
- [ ] Copias de seguridad **probadas** (restaurar al menos una vez en un entorno de prueba).

---

## 5. Resumen presupuesto (orientativo)

| Concepto | Rango mensual (USD) |
|----------|---------------------|
| VPS 2 vCPU / 4 GB / ~80 GB SSD | **12–20** |
| Dominio (prorrateado mensual) | **~1** |
| MySQL en el mismo VPS | **0** (incluido en el VPS) |
| **Total típico** | **~13–21 USD/mes** |

*(Precios variables según proveedor, región y tipo de instancia.)*

---

## 6. Nota sobre multi-municipio

El aislamiento entre municipios depende de **filtros por `empresa` en consultas**, **comprobación en vistas** y **sesión tras login**. El despliegue no cambia ese modelo: un solo sitio, una BD, **backups que protegen a todos** (acceso a backups muy restringido).

---

*Documento generado como guía de despliegue; adaptar comandos exactos a la versión de Ubuntu y rutas del proyecto.*
