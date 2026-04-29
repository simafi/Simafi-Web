## Entornos de ejecución (local / Supabase dev / Supabase prod)

Este repo soporta **tres modos** para correr Django en desarrollo en el **puerto 8010**:

### Local (Postgres local) — recomendado para pruebas
- **Script**: `run_tributario.ps1` o `run_tributario.bat`
- **DB**: Postgres local (`DJANGO_DB_*`)
- **Migraciones**: **sí** (se ejecutan en el script local)

### Supabase (dev) — pruebas locales apuntando a BD remota dev
- **Script**: `backend/run_supabase_dev.ps1`
- **DB**: Supabase dev (`DATABASE_URL`)
- **Migraciones**: **no** (para evitar tocar remoto por accidente)

### Supabase (prod) — solo cuando se necesite
- **Script**: `backend/run_supabase_prod.ps1`
- **DB**: Supabase prod (`DATABASE_URL`)
- **Migraciones**: **no** (si se requieren, deben correrse de forma controlada)

---

## Archivos `.env` por entorno

El `settings.py` carga `.env` con una **selección explícita** vía `DJANGO_ENV`.

Crea uno de estos archivos (en `C:\simafiweb`):
- `.env.local` (basado en `.env.local.example`)
- `.env.supabase_dev` (basado en `.env.supabase_dev.example`)
- `.env.supabase_prod` (basado en `.env.supabase_prod.example`)

Si `DJANGO_ENV` **no** está definido, se seguirá intentando cargar `.env` (comportamiento legado).

---

## Comandos rápidos

### 1) Local (Postgres local + migraciones + server)
En `C:\simafiweb`:

- PowerShell:
  - `.\run_tributario.ps1`

- CMD:
  - `run_tributario.bat`

### 2) Supabase dev (server local apuntando a Supabase dev)
En `C:\simafiweb\backend`:

- PowerShell:
  - `.\run_supabase_dev.ps1 -Port 8010 -DatabaseUrl "<TU_DATABASE_URL_DEV>"`

### 3) Supabase prod (server local apuntando a Supabase prod)
En `C:\simafiweb\backend`:

- PowerShell:
  - `.\run_supabase_prod.ps1 -Port 8010 -DatabaseUrl "<TU_DATABASE_URL_PROD>"`

---

## Notas de seguridad

- Nunca subas `.env*` con credenciales.
- Evita correr `migrate` contra Supabase prod desde local.

