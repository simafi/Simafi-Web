# Aplicación Administrativo

## Descripción
Sistema de configuración administrativa para todos los municipios. Esta aplicación maneja las tablas de uso estándar que son comunes para todos los municipios.

## Estructura de la Base de Datos

### Tabla: departamento
```sql
CREATE TABLE `departamento` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `codigo` CHAR(3) COLLATE latin1_swedish_ci NOT NULL DEFAULT '',
  `DESCRIPCION` VARCHAR(29) COLLATE latin1_swedish_ci NOT NULL,
  `departamento_field1` INTEGER DEFAULT NULL,
  PRIMARY KEY USING BTREE (`id`),
  UNIQUE KEY `departamento_idx1` USING BTREE (`codigo`)
) ENGINE=MyISAM
AUTO_INCREMENT=1 CHARACTER SET 'latin1' COLLATE 'latin1_swedish_ci';
```

## Funcionalidades

### Gestión de Departamentos
- ✅ **Crear**: Agregar nuevos departamentos
- ✅ **Leer**: Ver lista de departamentos existentes
- ✅ **Actualizar**: Modificar departamentos existentes
- ✅ **Eliminar**: Eliminar departamentos

### Características del Formulario
- ✅ **Diseño unificado**: Misma estética que otros formularios del sistema
- ✅ **Validación**: Código único por departamento
- ✅ **Responsive**: Diseño adaptable a diferentes dispositivos
- ✅ **Interfaz intuitiva**: Botones de acción claros y funcionales

## URLs Disponibles

- `/departamento/` - Formulario principal de gestión de departamentos
- `/ajax/buscar-departamento/` - Endpoint AJAX para buscar departamentos

## Instalación

1. Asegúrate de que la aplicación esté registrada en `INSTALLED_APPS`
2. Ejecuta las migraciones: `python manage.py migrate`
3. Accede a la URL del formulario

## Uso

1. **Crear Departamento**: Llena el formulario y haz clic en "Guardar Departamento"
2. **Editar Departamento**: Haz clic en "Editar" en la tabla y modifica los datos
3. **Eliminar Departamento**: Haz clic en "Eliminar" en la tabla (con confirmación)
4. **Limpiar Formulario**: Usa el botón "Limpiar" para resetear el formulario

## Tecnologías Utilizadas

- **Django**: Framework web
- **MySQL**: Base de datos
- **HTML/CSS/JavaScript**: Frontend
- **Font Awesome**: Iconos
- **Responsive Design**: Diseño adaptable







