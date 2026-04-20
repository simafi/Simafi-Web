# Modelo Usuarios Actualizado - Documentación Final

## Resumen del Sistema

El modelo de usuarios ha sido actualizado para coincidir exactamente con la estructura SQL proporcionada. El sistema ahora incluye validación del código de municipio con el código de empresa de la tabla usuarios.

## Estructura de la Tabla Usuarios

```sql
CREATE TABLE `usuarios` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `empresa` CHAR(4) COLLATE latin1_swedish_ci DEFAULT '',
  `usuario` CHAR(15) COLLATE latin1_swedish_ci NOT NULL,
  `password` VARCHAR(255) COLLATE latin1_swedish_ci NOT NULL,
  `nombre` VARCHAR(100) COLLATE latin1_swedish_ci DEFAULT NULL,
  PRIMARY KEY USING BTREE (`id`),
  UNIQUE KEY `usuarios_idx1` USING BTREE (`empresa`, `usuario`, `password`)
) ENGINE=MyISAM
CHECKSUM=1 AUTO_INCREMENT=2 CHARACTER SET 'latin1' COLLATE 'latin1_swedish_ci';
```

## Modelo Django Actualizado

### Campos del Modelo
```python
class usuario(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=4, verbose_name="Código de Empresa", default='', db_collation='latin1_swedish_ci')
    usuario = models.CharField(max_length=15, verbose_name="Nombre de Usuario", db_collation='latin1_swedish_ci')
    password = models.CharField(max_length=255, verbose_name="Contraseña", db_collation='latin1_swedish_ci')
    nombre = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre", db_collation='latin1_swedish_ci')
```

### Configuración Meta
```python
class Meta:
    db_table = 'usuarios'
    verbose_name = "Usuario"
    verbose_name_plural = "Usuarios"
    ordering = ['nombre', 'usuario']
    unique_together = ('empresa', 'usuario', 'password')
    indexes = [
        models.Index(fields=['empresa']),
        models.Index(fields=['usuario']),
    ]
```

## Proceso de Validación de Login

### Paso 1: Validación del Formulario
```python
form = LoginForm(data=request.POST)
if form.is_valid():
    usuario_input = form.cleaned_data['usuario']
    password = form.cleaned_data['password']
    municipio_input = form.cleaned_data['municipio']
```

### Paso 2: Búsqueda del Usuario
```python
try:
    user = usuario.objects.get(usuario=usuario_input)
except usuario.DoesNotExist:
    error = "Usuario no existe. Verifique el usuario y contraseña."
```

### Paso 3: Validación Municipio-Empresa
```python
# Verificar que el código de municipio coincida con el código de empresa del usuario
if municipio_input.codigo != user.empresa:
    error = "El código de municipio no coincide con el código de empresa del usuario."
```

### Paso 4: Validación de Contraseña
```python
if user.password.startswith('pbkdf2_sha256'):
    # Contraseña hasheada
    from django.contrib.auth.hashers import check_password
    if check_password(password, user.password):
        # Login exitoso
        user.record_successful_login()
        return redirect('menu_general')
    else:
        # Contraseña incorrecta
        user.record_failed_login()
        error = "Usuario o contraseña incorrectos"
else:
    # Contraseña en texto plano (legacy)
    if user.password == password:
        # Login exitoso
        user.record_successful_login()
        return redirect('menu_general')
    else:
        # Contraseña incorrecta
        user.record_failed_login()
        error = "Usuario o contraseña incorrectos"
```

## Mensajes de Error

### 1. Usuario No Existe
- **Mensaje**: "Usuario no existe. Verifique el usuario y contraseña."
- **Condición**: Cuando no se encuentra un usuario con el nombre de usuario

### 2. Código de Municipio No Coincide
- **Mensaje**: "El código de municipio no coincide con el código de empresa del usuario."
- **Condición**: Cuando el código del municipio seleccionado no coincide con el código de empresa del usuario

### 3. Contraseña Incorrecta
- **Mensaje**: "Usuario o contraseña incorrectos"
- **Condición**: Cuando el usuario existe pero la contraseña no coincide

### 4. Error del Sistema
- **Mensaje**: "Error en el sistema: {detalles}"
- **Condición**: Cuando ocurre una excepción no controlada

## Casos de Prueba Validados

### Escenarios de Validación

1. **Login Válido - Municipio Coincide con Empresa**
   - Usuario: admin (empresa: 0001)
   - Municipio: 0001 - Tegucigalpa
   - Contraseña: admin123
   - **Resultado**: ✅ Éxito

2. **Login Inválido - Municipio No Coincide con Empresa**
   - Usuario: admin (empresa: 0001)
   - Municipio: 0002 - San Pedro Sula
   - Contraseña: admin123
   - **Resultado**: ❌ "El código de municipio no coincide con el código de empresa del usuario."

3. **Login Inválido - Usuario Incorrecto**
   - Usuario: nonexistent
   - Municipio: 0001 - Tegucigalpa
   - Contraseña: admin123
   - **Resultado**: ❌ "Usuario no existe"

4. **Login Inválido - Contraseña Incorrecta**
   - Usuario: admin (empresa: 0001)
   - Municipio: 0001 - Tegucigalpa
   - Contraseña: wrongpassword
   - **Resultado**: ❌ "Usuario o contraseña incorrectos"

## Datos de Prueba

### Usuarios de Prueba
```
admin - Empresa: 0001 - Nombre: Administrador
user1 - Empresa: 0002 - Nombre: Usuario Uno
inactive - Empresa: 0001 - Nombre: Usuario Inactivo
```

### Municipios de Prueba
```
0001 - Tegucigalpa
0002 - San Pedro Sula
0003 - La Ceiba
0004 - Choluteca
0005 - Comayagua
...
```

## Combinaciones Válidas

### Usuario admin (Empresa: 0001)
- ✅ Municipio: 0001 - Tegucigalpa
- ❌ Municipio: 0002 - San Pedro Sula
- ❌ Municipio: 0003 - La Ceiba
- ❌ Cualquier otro municipio

### Usuario user1 (Empresa: 0002)
- ❌ Municipio: 0001 - Tegucigalpa
- ✅ Municipio: 0002 - San Pedro Sula
- ❌ Municipio: 0003 - La Ceiba
- ❌ Cualquier otro municipio

## Seguridad Implementada

### 1. Validación de Municipio-Empresa
- Verificación obligatoria del código de municipio con el código de empresa
- Prevención de acceso con municipios incorrectos
- Validación en tiempo real

### 2. Hashing de Contraseñas
- Las contraseñas se hashean automáticamente al guardar
- Soporte para contraseñas legacy en texto plano
- Verificación segura con `check_password()`

### 3. Validación de Formularios
- Validación del lado del cliente y servidor
- Mensajes de error específicos
- Sanitización de datos

### 4. Restricciones de Base de Datos
- `unique_together = ('empresa', 'usuario', 'password')`
- Índices en campos críticos
- Collation específico para compatibilidad

## Archivos Modificados

### Modelos
- **`hola/models.py`**: Actualizado modelo `usuario` con estructura simplificada

### Formularios
- **`hola/forms.py`**: Actualizados `UsuarioRegistrationForm` y `UsuarioUpdateForm`

### Vistas
- **`hola/views.py`**: Simplificada validación de login

### Admin
- **`hola/admin.py`**: Actualizado `UsuarioAdmin` para campos disponibles

### Scripts de Prueba
- **`test_updated_model.py`**: Pruebas completas del modelo actualizado

## Resultados de Pruebas

### Pruebas de Validación Municipio-Empresa
```
✅ Login válido - municipio coincide con empresa
✅ Login inválido - municipio no coincide con empresa
✅ Login inválido - usuario incorrecto
✅ Login inválido - contraseña incorrecta
✅ Login inválido - usuario inexistente

Pruebas correctas: 5/5
Porcentaje de éxito: 100.0%
🎉 ¡Todas las pruebas pasaron!
```

### Pruebas de Restricciones de Modelo
```
✅ Empresa field constraint working
✅ Usuario field constraint working
✅ Password field constraint working
✅ Unique constraint working correctly
```

## Ventajas del Sistema Actualizado

### 1. Compatibilidad Total
- Estructura exacta con la tabla SQL proporcionada
- Collation específico para compatibilidad
- Campos requeridos y opcionales correctamente definidos

### 2. Seguridad Mejorada
- Validación adicional de municipio-empresa
- Prevención de acceso con municipios incorrectos
- Control granular de acceso por empresa

### 3. Integridad de Datos
- Verificación de consistencia entre municipios y empresas
- Validación en tiempo real
- Prevención de errores de usuario

### 4. Simplicidad
- Modelo simplificado sin campos innecesarios
- Validación directa y eficiente
- Fácil mantenimiento y extensión

## Uso del Sistema

### Crear un Usuario
```python
from hola.models import usuario
from django.contrib.auth.hashers import make_password

user = usuario.objects.create(
    empresa='0001',
    usuario='nuevo_usuario',
    password=make_password('contraseña_segura'),
    nombre='Nombre Completo'
)
```

### Validar Login con Municipio
```python
from hola.forms import LoginForm

form_data = {
    'usuario': 'admin',
    'password': 'admin123',
    'municipio': municipio.id  # Municipio con código que coincida con empresa
}

form = LoginForm(data=form_data)
if form.is_valid():
    # Procesar login con validación municipio-empresa
    pass
```

## Configuración de Municipios

### Agregar Nuevo Municipio
```python
from hola.models import Municipio

municipio = Municipio.objects.create(
    codigo='0004',
    descripcion='Nuevo Municipio'
)
```

### Verificar Municipios por Empresa
```python
# Obtener municipios que coinciden con empresa
empresa_code = '0001'
matching_municipios = Municipio.objects.filter(codigo=empresa_code)
```

## Notas Importantes

1. **Consistencia de Datos**: Los códigos de municipio deben coincidir exactamente con los códigos de empresa
2. **Validación Obligatoria**: La validación municipio-empresa es obligatoria para todos los logins
3. **Mensajes Claros**: Los mensajes de error son específicos y ayudan al usuario
4. **Compatibilidad**: El modelo coincide exactamente con la estructura SQL proporcionada
5. **Simplicidad**: Sistema simplificado sin campos innecesarios

## Próximos Pasos

1. **Implementar sesiones**: Agregar manejo de sesiones de usuario
2. **Logs de auditoría**: Implementar logs detallados de acceso
3. **Recuperación de contraseña**: Agregar funcionalidad de reset de contraseña
4. **Notificaciones**: Implementar notificaciones por email
5. **Roles y permisos**: Agregar sistema de roles más granular
6. **Configuración dinámica**: Permitir configuración de municipios-empresas desde admin

## Conclusión

El modelo de usuarios ha sido actualizado exitosamente para coincidir exactamente con la estructura SQL proporcionada. El sistema mantiene la validación municipio-empresa y todas las pruebas pasan al 100%. La estructura simplificada es más eficiente y fácil de mantener, mientras que la validación asegura que los usuarios solo puedan acceder con municipios que correspondan a su empresa. 