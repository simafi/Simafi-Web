# Módulos Completamente Independientes

## Descripción General

Ahora cada módulo tiene su propio `manage.py` y configuración independiente, permitiendo ejecutar cada módulo de forma completamente separada.

## Estructura de Archivos

```
C:\simafiweb\venv\Scripts\tributario\
├── manage.py                    # Módulo Tributario
├── run_tributario.bat          # Script ejecución Tributario
├── run_tributario.ps1          # Script PowerShell Tributario
├── run_catastro.bat            # Script ejecución Catastro
├── run_catastro.ps1            # Script PowerShell Catastro
├── tributario/                 # Configuración Tributario
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tributario_app/             # Aplicación Legacy
└── modules/
    ├── core/
    ├── usuarios/
    └── catastro/
        ├── manage.py           # Módulo Catastro
        ├── catastro/           # Configuración Catastro
        │   ├── settings.py
        │   ├── urls.py
        │   └── wsgi.py
        ├── views.py
        ├── models.py
        ├── forms.py
        ├── urls.py
        └── templates/
```

## Ejecución Independiente

### Módulo Tributario

**Ubicación**: `C:\simafiweb\venv\Scripts\tributario\`

**Comandos de ejecución**:
```bash
# Desde la línea de comandos
cd C:\simafiweb\venv\Scripts\tributario
python manage.py runserver 8080

# O usar los scripts
run_tributario.bat
run_tributario.ps1
```

**URLs de acceso**:
- **Login**: `http://127.0.0.1:8080/`
- **Menú**: `http://127.0.0.1:8080/menu/`
- **Admin**: `http://127.0.0.1:8080/admin/`

### Módulo Catastro

**Ubicación**: `C:\simafiweb\venv\Scripts\tributario\modules\catastro\`

**Comandos de ejecución**:
```bash
# Desde la línea de comandos
cd C:\simafiweb\venv\Scripts\tributario\modules\catastro
python manage.py runserver 8081

# O usar los scripts
run_catastro.bat
run_catastro.ps1
```

**URLs de acceso**:
- **Login**: `http://127.0.0.1:8081/`
- **Menú**: `http://127.0.0.1:8081/menu/`
- **Admin**: `http://127.0.0.1:8081/admin/`

## Configuraciones Específicas

### Módulo Tributario (settings.py)
- **Puerto**: 8080
- **Aplicaciones**: tributario_app + módulos compartidos
- **Sesiones**: Estándar de Django
- **Cookies**: Estándar de Django

### Módulo Catastro (settings.py)
- **Puerto**: 8081
- **Aplicaciones**: Solo módulos necesarios (core, usuarios, catastro)
- **Sesiones**: Configuración específica para catastro
- **Cookies**: `catastro_sessionid` con path `/catastro/`

## Ventajas de la Nueva Estructura

### ✅ Independencia Total
- Cada módulo puede ejecutarse independientemente
- Configuraciones separadas
- Puertos diferentes (8080 y 8081)
- Sesiones completamente aisladas

### ✅ Desarrollo Paralelo
- Equipos pueden trabajar en módulos diferentes
- Testing independiente
- Deployment modular
- Mantenimiento separado

### ✅ Escalabilidad
- Nuevos módulos pueden agregarse fácilmente
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
cd C:\simafiweb\venv\Scripts\tributario\modules\catastro

# Verificar configuración
python manage.py check

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver 8081
```

## Scripts de Ejecución

### Windows Batch (.bat)
- **run_tributario.bat**: Ejecuta módulo tributario en puerto 8080
- **run_catastro.bat**: Ejecuta módulo catastro en puerto 8081

### PowerShell (.ps1)
- **run_tributario.ps1**: Ejecuta módulo tributario con colores
- **run_catastro.ps1**: Ejecuta módulo catastro con colores

## Base de Datos Compartida

Ambos módulos comparten la misma base de datos pero con tablas separadas:

- **Tablas compartidas**: `mod_core_*`, `mod_usuarios_*`
- **Tablas tributario**: `tributario_app_*`
- **Tablas catastro**: `mod_catastro_*`

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

## Próximos Pasos

1. **Ejecutar ambos módulos simultáneamente** en puertos diferentes
2. **Desarrollar funcionalidades específicas** en cada módulo
3. **Crear nuevos módulos** siguiendo el patrón de catastro
4. **Implementar APIs comunes** para comunicación entre módulos
5. **Configurar proxy reverso** para unificar acceso

---
**Estado**: ✅ Módulos Completamente Independientes
**Última actualización**: 12 de Agosto, 2025








































