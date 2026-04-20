# Módulos Independientes - Funcionamiento Simultáneo

## Descripción General

El sistema está configurado para que los módulos **Tributario** y **Catastro** funcionen de forma completamente independiente y simultánea, sin afectarse uno al otro.

## Arquitectura de URLs

### Configuración Principal (`tributario/urls.py`)

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('catastro/', include('modules.catastro.urls')),  # Módulo de catastro (primero)
    path('', include('tributario_app.urls')),  # Aplicación legacy (después)
]
```

**Importante**: El módulo de catastro está configurado **antes** que la aplicación tributario para evitar conflictos de rutas.

## Módulo Tributario (Legacy)

### Acceso
- **URL Base**: `http://127.0.0.1:8080/`
- **Login**: `http://127.0.0.1:8080/`
- **Menú**: `http://127.0.0.1:8080/menu/`

### Características
- **Aplicación legacy** con funcionalidades existentes
- **Sistema de autenticación propio**
- **Sesiones independientes**
- **Base de datos compartida** pero con tablas separadas

### Funcionalidades Disponibles
- Bienes Inmuebles
- Industria y Comercio
- Misceláneos
- Convenios de Pagos
- Utilitarios
- Maestro de Negocios
- Informes
- Configuración

## Módulo Catastro (Nuevo)

### Acceso
- **URL Base**: `http://127.0.0.1:8080/catastro/`
- **Login**: `http://127.0.0.1:8080/catastro/login/`
- **Menú**: `http://127.0.0.1:8080/catastro/menu/`

### Credenciales de Prueba
```
Usuario: admin
Contraseña: admin123
Municipio: Municipio de Prueba
```

### Características
- **Módulo completamente independiente**
- **Sistema de autenticación propio**
- **Sesiones separadas** (prefijo `catastro_`)
- **Base de datos con prefijos únicos** (`mod_catastro_`)

### Funcionalidades Disponibles
- Bienes Inmuebles
- Industria y Comercio
- Vehículos
- Terrenos
- Construcciones
- Reportes
- Configuración

## Independencia Total

### 1. Autenticación Independiente
- **Tributario**: Usa su propio sistema de login
- **Catastro**: Usa su propio sistema de login
- **No hay interferencia** entre ambos sistemas

### 2. Sesiones Separadas
- **Tributario**: Variables de sesión estándar
- **Catastro**: Variables con prefijo `catastro_`
  - `catastro_municipio_codigo`
  - `catastro_usuario_id`
  - `catastro_usuario_nombre`

### 3. Base de Datos
- **Tablas compartidas**: `mod_core_*`, `mod_usuarios_*`
- **Tablas independientes**: 
  - Tributario: `tributario_app_*`
  - Catastro: `mod_catastro_*`

### 4. URLs y Namespaces
- **Tributario**: URLs sin namespace
- **Catastro**: URLs con namespace `catastro:`

## Flujo de Trabajo Simultáneo

### Escenario 1: Usuario Solo Tributario
1. Accede a `http://127.0.0.1:8080/`
2. Se autentica en el sistema tributario
3. Trabaja en funcionalidades tributarias
4. **No afecta** al módulo catastro

### Escenario 2: Usuario Solo Catastro
1. Accede a `http://127.0.0.1:8080/catastro/login/`
2. Se autentica en el sistema catastro
3. Trabaja en funcionalidades catastrales
4. **No afecta** al módulo tributario

### Escenario 3: Usuario Ambos Módulos
1. Puede tener **sesiones activas** en ambos módulos
2. **Navegación independiente** entre módulos
3. **Logout independiente** en cada módulo
4. **Datos separados** por módulo

## Ventajas de la Arquitectura

### ✅ Independencia Total
- Cada módulo funciona sin afectar al otro
- Fallos en un módulo no impactan al otro
- Mantenimiento independiente

### ✅ Escalabilidad
- Nuevos módulos pueden agregarse fácilmente
- Cada módulo puede evolucionar independientemente
- Migración gradual desde legacy

### ✅ Seguridad
- Autenticación separada por módulo
- Permisos independientes
- Aislamiento de datos

### ✅ Desarrollo
- Equipos pueden trabajar en paralelo
- Testing independiente
- Deployment modular

## Configuración Técnica

### Archivos de Configuración
```
tributario/
├── settings.py          # Configuración general
├── urls.py              # URLs principales
└── wsgi.py              # Servidor WSGI

modules/
├── catastro/            # Módulo catastro
│   ├── urls.py          # URLs del módulo
│   ├── views.py         # Vistas del módulo
│   ├── models.py        # Modelos del módulo
│   └── forms.py         # Formularios del módulo
└── [otros módulos]      # Futuros módulos

tributario_app/          # Aplicación legacy
├── urls.py              # URLs legacy
├── views.py             # Vistas legacy
└── models.py            # Modelos legacy
```

### Orden de Prioridad en URLs
1. **Admin** (`/admin/`)
2. **Catastro** (`/catastro/`)
3. **Tributario** (`/`)

## Próximos Pasos

1. **Desarrollo paralelo**: Ambos módulos pueden desarrollarse simultáneamente
2. **Nuevos módulos**: Seguir el patrón establecido por catastro
3. **Migración gradual**: Mover funcionalidades de legacy a módulos
4. **API unificada**: Crear APIs comunes para ambos módulos

---
**Estado**: ✅ Funcionando Independientemente
**Última actualización**: 12 de Agosto, 2025








































