# Módulos Independientes - Nivel Superior

## Descripción General

Ahora los módulos están organizados al mismo nivel, cada uno con su propio `manage.py` y configuración completamente independiente.

## Estructura de Archivos

```
C:\simafiweb\venv\Scripts\
├── tributario/                    # Módulo Tributario
│   ├── manage.py
│   ├── tributario/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── tributario_app/
│   └── modules/
│       ├── core/
│       ├── usuarios/
│       └── [otros módulos]
│
├── catastro_modulo/               # Módulo Catastro (NUEVO)
│   ├── manage.py
│   ├── catastro/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── core/                      # Copiado desde tributario
│   ├── usuarios/                  # Copiado desde tributario
│   ├── catastro_app/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── signals.py
│   └── templates/
│       └── catastro_app/
│           ├── login.html
│           └── menu_principal.html
│
├── run_tributario.bat            # Script ejecución Tributario
├── run_catastro.bat              # Script ejecución Catastro
└── [otros módulos existentes]    # administrativo, ambiental, etc.
```

## Ejecución Independiente

### Módulo Tributario

**Ubicación**: `C:\simafiweb\venv\Scripts\tributario\`

**Comandos de ejecución**:
```bash
# Desde la línea de comandos
cd C:\simafiweb\venv\Scripts\tributario
python manage.py runserver 8080

# O usar el script
run_tributario.bat
```

**URLs de acceso**:
- **Login**: `http://127.0.0.1:8080/`
- **Menú**: `http://127.0.0.1:8080/menu/`
- **Admin**: `http://127.0.0.1:8080/admin/`

### Módulo Catastro

**Ubicación**: `C:\simafiweb\venv\Scripts\catastro_modulo\`

**Comandos de ejecución**:
```bash
# Desde la línea de comandos
cd C:\simafiweb\venv\Scripts\catastro_modulo
python manage.py runserver 8080

# O usar el script
run_catastro.bat
```

**URLs de acceso**:
- **Login**: `http://127.0.0.1:8080/`
- **Menú**: `http://127.0.0.1:8080/menu/`
- **Admin**: `http://127.0.0.1:8080/admin/`

## Configuraciones Específicas

### Módulo Tributario (settings.py)
- **Puerto**: 8080
- **Aplicaciones**: tributario_app + módulos compartidos
- **Sesiones**: Estándar de Django
- **Cookies**: Estándar de Django

### Módulo Catastro (settings.py)
- **Puerto**: 8080
- **Aplicaciones**: core, usuarios, catastro_app
- **Sesiones**: Configuración específica para catastro
- **Cookies**: `catastro_sessionid`

## Ventajas de la Nueva Estructura

### ✅ Independencia Total
- Cada módulo puede ejecutarse independientemente
- Configuraciones completamente separadas
- Puerto compartido (8080) - ejecutar uno a la vez
- Sesiones completamente aisladas

### ✅ Desarrollo Paralelo
- Equipos pueden trabajar en módulos diferentes
- Testing independiente
- Deployment modular
- Mantenimiento separado

### ✅ Escalabilidad
- Nuevos módulos pueden agregarse fácilmente al mismo nivel
- Cada módulo puede evolucionar independientemente
- Migración gradual desde legacy

### ✅ Seguridad
- Aislamiento completo entre módulos
- Sesiones independientes
- Configuraciones específicas por módulo

## Comandos de Gestión

### Módulo Tributario
```bash
cd C:\simafiweb\venv\Scripts\tributario

# Verificar configuración
python manage.py check

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver 8080
```

### Módulo Catastro
```bash
cd C:\simafiweb\venv\Scripts\catastro_modulo

# Verificar configuración
python manage.py check

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver 8080
```

## Scripts de Ejecución

### Windows Batch (.bat)
- **run_tributario.bat**: Ejecuta módulo tributario en puerto 8080
- **run_catastro.bat**: Ejecuta módulo catastro en puerto 8080

## Base de Datos Compartida

Ambos módulos comparten la misma base de datos pero con tablas separadas:

- **Tablas compartidas**: `mod_core_*`, `mod_usuarios_*`
- **Tablas tributario**: `tributario_app_*`
- **Tablas catastro**: `catastro_*`

## Credenciales de Prueba

### Módulo Tributario
```
Usuario: [crear según configuración legacy]
Contraseña: [según configuración legacy]
```

### Módulo Catastro
```
Usuario: admin
Contraseña: admin123
Municipio: Municipio de Prueba
```

## Funcionalidades del Módulo Catastro

### ✅ Implementado
- **Sistema de Login**: Autenticación independiente
- **Menú Principal**: Dashboard con todas las opciones
- **Gestión de Sesiones**: Variables de sesión específicas
- **Modelos de Datos**: Propiedades, terrenos, construcciones, vehículos, establecimientos
- **Plantillas**: Diseño moderno y responsivo

### 🔄 En Desarrollo
- **CRUD Completo**: Para cada modelo
- **Reportes**: Generación de informes
- **Configuración**: Parámetros del sistema
- **Validaciones**: Reglas de negocio específicas

## Próximos Pasos

1. **Ejecutar módulos independientemente** en el puerto 8080 (uno a la vez)
2. **Desarrollar funcionalidades específicas** en cada módulo
3. **Crear nuevos módulos** siguiendo el patrón de catastro_modulo
4. **Implementar APIs comunes** para comunicación entre módulos
5. **Configurar proxy reverso** para unificar acceso

---
**Estado**: ✅ Módulos Completamente Independientes al Mismo Nivel
**Última actualización**: 12 de Agosto, 2025
