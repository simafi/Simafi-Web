# Actualización del Modelo de Usuario (usuario)

## Resumen de Cambios

Se ha actualizado el modelo `usuario` en `hola/models.py` para incluir campos más completos y funcionalidades avanzadas de gestión de usuarios.

## Nuevos Campos Agregados

### Información Personal
- `email` (EmailField): Correo electrónico único
- `nombres` (CharField): Nombres del usuario
- `apellidos` (CharField): Apellidos del usuario

### Información de Contacto
- `telefono` (CharField): Número de teléfono
- `celular` (CharField): Número de celular
- `direccion` (TextField): Dirección completa

### Información de Identificación
- `identidad` (CharField): Número de identidad
- `rtn` (CharField): RTN (Registro Tributario Nacional)

### Estados y Fechas
- `is_active` (BooleanField): Indica si el usuario está activo
- `is_staff` (BooleanField): Indica si es personal administrativo
- `is_superuser` (BooleanField): Indica si es superusuario
- `date_joined` (DateTimeField): Fecha de registro
- `last_login` (DateTimeField): Último acceso

### Información Laboral
- `cargo` (CharField): Cargo del usuario
- `departamento` (CharField): Departamento
- `oficina` (CharField): Oficina asignada

### Campos de Auditoría
- `created_at` (DateTimeField): Fecha de creación
- `updated_at` (DateTimeField): Fecha de última actualización
- `created_by` (ForeignKey): Usuario que creó el registro

### Notas y Comentarios
- `notas` (TextField): Notas adicionales sobre el usuario

### Campos de Seguridad
- `password_changed_at` (DateTimeField): Fecha del último cambio de contraseña
- `failed_login_attempts` (PositiveIntegerField): Contador de intentos fallidos
- `locked_until` (DateTimeField): Fecha hasta la cual está bloqueada la cuenta

## Métodos Agregados

### Gestión de Nombres
- `get_full_name()`: Retorna el nombre completo del usuario
- `get_short_name()`: Retorna el nombre corto del usuario

### Gestión de Seguridad
- `is_locked()`: Verifica si la cuenta está bloqueada
- `lock_account(duration_minutes=30)`: Bloquea la cuenta por un tiempo determinado
- `unlock_account()`: Desbloquea la cuenta
- `record_failed_login()`: Registra un intento fallido de login
- `record_successful_login()`: Registra un login exitoso

## Configuración de Meta

### Ordenamiento
- Los usuarios se ordenan por nombres, apellidos y usuario

### Índices de Base de Datos
- Índice en campo `usuario`
- Índice en campo `email`
- Índice en campo `identidad`
- Índice en campo `is_active`

## Formularios Actualizados

### Nuevos Formularios en `forms.py`
- `UsuarioRegistrationForm`: Formulario completo de registro de usuarios
- `UsuarioUpdateForm`: Formulario para actualizar información de usuario
- `ChangePasswordForm`: Formulario para cambiar contraseña

## Interfaz de Administración

### Admin Configurado en `admin.py`
- `UsuarioAdmin`: Configuración completa del admin para usuarios
- Campos organizados en secciones lógicas
- Filtros y búsquedas avanzadas
- Campos de solo lectura para auditoría

## Migraciones Aplicadas

1. **0015_alter_usuario_options_usuario_apellidos_and_more.py**
   - Agregó todos los nuevos campos al modelo usuario
   - Configuró índices de base de datos
   - Actualizó opciones Meta

2. **0016_alter_usuario_password.py**
   - Aumentó el tamaño del campo password de 128 a 255 caracteres
   - Necesario para almacenar contraseñas hasheadas

## Funcionalidades de Seguridad

### Bloqueo Automático de Cuentas
- Después de 5 intentos fallidos de login, la cuenta se bloquea automáticamente
- El bloqueo dura 30 minutos por defecto
- Se puede desbloquear manualmente o automáticamente con login exitoso

### Seguimiento de Contraseñas
- Se registra la fecha del último cambio de contraseña
- Las contraseñas se hashean automáticamente al guardar

### Auditoría
- Se registra quién creó cada usuario
- Se mantienen fechas de creación y actualización
- Se registra el último acceso

## Compatibilidad

### Campos Mantenidos
- `id`: Clave primaria (AutoField)
- `usuario`: Nombre de usuario único
- `password`: Contraseña (ahora con max_length=255)

### Migración de Datos
- Los usuarios existentes mantienen sus datos
- Los nuevos campos se inicializan con valores por defecto apropiados
- No se pierde información existente

## Pruebas

Se incluye un archivo de prueba `test_usuario_model.py` que verifica:
- Creación de usuarios con datos completos
- Creación de usuarios con datos mínimos
- Funcionalidades de bloqueo/desbloqueo
- Métodos de gestión de nombres
- Seguimiento de intentos de login
- Actualización de información

## Uso Recomendado

### Crear un Nuevo Usuario
```python
from hola.models import usuario

user = usuario.objects.create(
    usuario='nuevo_usuario',
    password='contraseña_segura',
    email='usuario@ejemplo.com',
    nombres='Juan',
    apellidos='Pérez',
    is_active=True
)
```

### Verificar Estado de Cuenta
```python
if user.is_locked():
    print("Cuenta bloqueada")
else:
    print("Cuenta activa")
```

### Registrar Login Exitoso
```python
user.record_successful_login()
```

## Notas Importantes

1. **Contraseñas**: Siempre se hashean automáticamente al guardar
2. **Campos Opcionales**: La mayoría de campos nuevos son opcionales para mantener compatibilidad
3. **Índices**: Se han agregado índices para mejorar el rendimiento de consultas
4. **Auditoría**: Todos los cambios importantes se registran automáticamente

## Próximos Pasos

1. Actualizar las vistas de login para usar los nuevos métodos de seguridad
2. Implementar formularios de registro de usuarios
3. Agregar funcionalidades de recuperación de contraseña
4. Implementar notificaciones por email
5. Agregar roles y permisos más granulares 