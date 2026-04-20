# Módulos Independientes - Puerto 8080

## Descripción General

Ambos módulos (Tributario y Catastro) están configurados para usar el puerto 8080, pero se ejecutan de forma completamente independiente.

## ⚠️ Importante: Ejecución Secuencial

**Los módulos NO pueden ejecutarse simultáneamente** ya que ambos usan el puerto 8080. Debes ejecutar uno a la vez:

1. **Cerrar completamente** el módulo que esté ejecutándose
2. **Ejecutar** el otro módulo
3. **Repetir** según necesites

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
├── catastro_modulo/               # Módulo Catastro
│   ├── manage.py
│   ├── catastro/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── core/
│   ├── usuarios/
│   ├── catastro_app/
│   └── templates/
│
├── run_tributario.bat            # Script ejecución Tributario (Puerto 8080)
├── run_catastro.bat              # Script ejecución Catastro (Puerto 8080)
└── [otros módulos existentes]
```

## Ejecución de Módulos

### Módulo Tributario

**Ubicación**: `C:\simafiweb\venv\Scripts\tributario\`

**Comandos de ejecución**:
```bash
# Opción 1: Script automático
run_tributario.bat

# Opción 2: Comando manual
cd C:\simafiweb\venv\Scripts\tributario
python manage.py runserver 8080
```

**URLs de acceso**:
- **Login**: `http://127.0.0.1:8080/`
- **Menú**: `http://127.0.0.1:8080/menu/`
- **Admin**: `http://127.0.0.1:8080/admin/`

### Módulo Catastro

**Ubicación**: `C:\simafiweb\venv\Scripts\catastro_modulo\`

**Comandos de ejecución**:
```bash
# Opción 1: Script automático
run_catastro.bat

# Opción 2: Comando manual
cd C:\simafiweb\venv\Scripts\catastro_modulo
python manage.py runserver 8080
```

**URLs de acceso**:
- **Login**: `http://127.0.0.1:8080/`
- **Menú**: `http://127.0.0.1:8080/menu/`
- **Admin**: `http://127.0.0.1:8080/admin/`

## Flujo de Trabajo Recomendado

### Escenario 1: Trabajar con Tributario
1. Ejecutar: `run_tributario.bat`
2. Acceder a: `http://127.0.0.1:8080/`
3. Trabajar en funcionalidades tributarias
4. **Cerrar** el servidor (Ctrl+C)
5. **Esperar** a que se libere el puerto

### Escenario 2: Trabajar con Catastro
1. Ejecutar: `run_catastro.bat`
2. Acceder a: `http://127.0.0.1:8080/`
3. Trabajar en funcionalidades catastrales
4. **Cerrar** el servidor (Ctrl+C)
5. **Esperar** a que se libere el puerto

### Escenario 3: Alternar entre Módulos
1. **Cerrar completamente** el módulo actual
2. **Verificar** que el puerto 8080 esté libre
3. **Ejecutar** el otro módulo
4. **Repetir** según necesites

## Verificación del Puerto

### Verificar si el puerto 8080 está en uso:
```bash
# Windows
netstat -ano | findstr :8080

# Si está en uso, ver el PID
tasklist /FI "PID eq [PID_NUMERO]"

# Terminar proceso si es necesario
taskkill /PID [PID_NUMERO] /F
```

### Verificar que el puerto esté libre:
```bash
# Debe mostrar "No se puede establecer una conexión"
telnet 127.0.0.1 8080
```

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

## Ventajas de la Configuración

### ✅ Independencia Total
- Cada módulo puede ejecutarse independientemente
- Configuraciones completamente separadas
- Sesiones completamente aisladas
- Base de datos compartida pero tablas separadas

### ✅ Desarrollo Paralelo
- Equipos pueden trabajar en módulos diferentes
- Testing independiente
- Deployment modular
- Mantenimiento separado

### ✅ Escalabilidad
- Nuevos módulos pueden agregarse fácilmente
- Cada módulo puede evolucionar independientemente
- Migración gradual desde legacy

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

# Ejecutar servidor
python manage.py runserver 8080
```

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

## Solución de Problemas

### Error: "Puerto ya en uso"
1. **Cerrar** el servidor actual (Ctrl+C)
2. **Esperar** 5-10 segundos
3. **Verificar** que el puerto esté libre
4. **Ejecutar** el otro módulo

### Error: "No se puede acceder al sitio"
1. **Verificar** que el servidor esté ejecutándose
2. **Comprobar** que no haya otro proceso en el puerto 8080
3. **Reiniciar** el servidor si es necesario

### Error: "Módulo no encontrado"
1. **Verificar** que estés en el directorio correcto
2. **Activar** el entorno virtual
3. **Instalar** dependencias si es necesario

## Próximos Pasos

1. **Desarrollar funcionalidades específicas** en cada módulo
2. **Crear nuevos módulos** siguiendo el patrón establecido
3. **Implementar APIs comunes** para comunicación entre módulos
4. **Configurar proxy reverso** para unificar acceso
5. **Considerar** puertos diferentes para ejecución simultánea

---
**Estado**: ✅ Módulos Independientes en Puerto 8080
**Última actualización**: 12 de Agosto, 2025








































