# Solución al Problema de Guardado de Tarifas ✅

## Problema Identificado

El usuario reportó que el botón de guardar tarifa fallaba al presionarlo. Después de un diagnóstico completo, se identificó el siguiente problema:

**Error**: `Data too long for column 'cod_tarifa' at row 1`

**Causa Raíz**: El campo `cod_tarifa` en la base de datos tiene una restricción de `VARCHAR(4)`, pero el código estaba intentando guardar códigos de tarifa de más de 4 caracteres (ej: "TAR001", "TAR002").

## Estructura de Base de Datos

Según la estructura proporcionada:
```sql
CREATE TABLE `tarifas` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `empresa` CHAR(4) COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `rubro` VARCHAR(4) COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `cod_tarifa` VARCHAR(4) COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,  -- ❌ MÁXIMO 4 CARACTERES
  `ano` DECIMAL(4,0) NOT NULL,
  `descripcion` CHAR(200) COLLATE utf8mb4_0900_ai_ci DEFAULT '',
  `valor` DECIMAL(12,2) DEFAULT 0.00,
  `frecuencia` CHAR(1) COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `tipo` CHAR(1) COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY USING BTREE (`id`),
  UNIQUE KEY `tarifas_empresa_codigo_ano_498e4b0c_uniq` USING BTREE (`empresa`, `ano`, `rubro`, `cod_tarifa`)
)
```

## Solución Implementada

### ✅ **1. Validación en el Formulario (`forms.py`)**

Se agregó validación específica para el campo `cod_tarifa`:

```python
def clean(self):
    cleaned_data = super().clean()
    empresa = cleaned_data.get('empresa')
    ano = cleaned_data.get('ano')
    valor = cleaned_data.get('valor')
    tipo = cleaned_data.get('tipo')
    rubro = cleaned_data.get('rubro')
    cod_tarifa = cleaned_data.get('cod_tarifa')
    
    # Validar año
    if ano and (ano < 2020 or ano > 2030):
        raise forms.ValidationError("El año debe estar entre 2020 y 2030")
    
    # Validar valor según el tipo
    if tipo == 'F' and (not valor or valor <= 0):
        raise forms.ValidationError("El valor es obligatorio cuando el tipo es Fija")
    
    # ✅ NUEVA VALIDACIÓN: Código de tarifa máximo 4 caracteres
    if cod_tarifa and len(cod_tarifa) > 4:
        raise forms.ValidationError("El código de tarifa no puede exceder 4 caracteres")
    
    return cleaned_data
```

### ✅ **2. Actualización del Template (`formulario_tarifas.html`)**

Se agregó información visual para el usuario:

```html
<div class="form-group form-group-codigo">
    <label for="{{ form.cod_tarifa.id_for_label }}">Código de Tarifa</label>
    {{ form.cod_tarifa }}
    <small style="color: #6c757d; font-size: 0.85rem; display: block; margin-top: 5px;">
        <i class="fas fa-search"></i> Ingrese código para buscar automáticamente. 
        <strong>Máximo 4 caracteres.</strong> Si no existe en el año actual, buscará en otros años.
    </small>
</div>
```

### ✅ **3. Validación en JavaScript**

Se agregó validación en tiempo real:

```javascript
// Validación del código de tarifa
const codTarifaInput = document.getElementById('{{ form.cod_tarifa.id_for_label }}');
if (codTarifaInput) {
    codTarifaInput.addEventListener('input', function() {
        const valor = this.value;
        if (valor.length > 4) {
            this.value = valor.substring(0, 4);
            mostrarMensaje('El código de tarifa no puede exceder 4 caracteres', false);
        }
    });
}
```

### ✅ **4. Vista Optimizada (`views.py`)**

La vista ya estaba correctamente implementada con `get_or_create()`:

```python
# Lógica para crear/actualizar tarifa usando get_or_create
if cod_tarifa and ano and rubro:
    try:
        # Usar get_or_create para manejar automáticamente la creación o actualización
        tarifa, created = Tarifas.objects.get_or_create(
            empresa=empresa,
            ano=ano,
            rubro=rubro,
            cod_tarifa=cod_tarifa,
            defaults={
                'descripcion': form.cleaned_data.get('descripcion', ''),
                'valor': form.cleaned_data.get('valor', 0.00),
                'frecuencia': form.cleaned_data.get('frecuencia', ''),
                'tipo': form.cleaned_data.get('tipo', ''),
            }
        )
        
        if created:
            mensaje = f"Tarifa {cod_tarifa} (Año {ano}) creada exitosamente."
        else:
            # Actualizar campos existentes
            tarifa.descripcion = form.cleaned_data.get('descripcion', '')
            tarifa.valor = form.cleaned_data.get('valor', 0.00)
            tarifa.frecuencia = form.cleaned_data.get('frecuencia', '')
            tarifa.tipo = form.cleaned_data.get('tipo', '')
            tarifa.save()
            mensaje = f"Tarifa {cod_tarifa} (Año {ano}) actualizada exitosamente."
        
        exito = True
    except Exception as e:
        mensaje = f"Error al procesar la tarifa: {str(e)}"
        exito = False
```

## 🎯 Funcionalidades Implementadas

### **Validación de Código de Tarifa**
- ✅ Máximo 4 caracteres
- ✅ Validación en tiempo real con JavaScript
- ✅ Validación en el servidor con Django
- ✅ Mensajes informativos para el usuario

### **Creación y Actualización**
- ✅ Crear nueva tarifa si no existe
- ✅ Actualizar tarifa existente si ya existe
- ✅ Validación según clave única: `(empresa, rubro, ano, cod_tarifa)`
- ✅ Mensajes específicos para creación vs actualización

### **Interfaz de Usuario**
- ✅ Información visual sobre restricciones
- ✅ Validación en tiempo real
- ✅ Mensajes de error claros
- ✅ Confirmaciones de éxito

## 📋 Ejemplos de Códigos Válidos

### **Códigos Correctos (4 caracteres o menos)**
- `T001` ✅
- `T002` ✅
- `001` ✅
- `A1` ✅
- `B2` ✅

### **Códigos Incorrectos (más de 4 caracteres)**
- `TAR001` ❌ (6 caracteres)
- `TAR002` ❌ (6 caracteres)
- `TARIFA001` ❌ (9 caracteres)

## 🔧 Configuración del Modelo

El modelo `Tarifas` ya está correctamente configurado:

```python
class Tarifas(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    empresa = models.CharField(max_length=4, verbose_name="Empresa", db_collation='utf8mb4_0900_ai_ci', default='')
    rubro = models.CharField(max_length=4, blank=True, null=True, verbose_name="Rubro", db_collation='utf8mb4_0900_ai_ci', default='')
    cod_tarifa = models.CharField(max_length=4, blank=True, null=True, verbose_name="Código de Tarifa", db_collation='utf8mb4_0900_ai_ci', default='')
    ano = models.DecimalField(max_digits=4, decimal_places=0, verbose_name="Año")
    descripcion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Descripción", db_collation='utf8mb4_0900_ai_ci', default='')
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor", default=0.00)
    frecuencia = models.CharField(max_length=1, blank=True, null=True, verbose_name="Frecuencia", choices=[('A', 'Anual'), ('M', 'Mensual')])
    tipo = models.CharField(max_length=1, blank=True, null=True, verbose_name="Tipo", choices=[('F', 'Fija'), ('V', 'Variable')])

    class Meta:
        db_table = 'tarifas'
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"
        unique_together = ['empresa', 'rubro', 'ano', 'cod_tarifa']
```

## ✅ Estado Final

### **Problema Resuelto**
- ✅ El botón de guardar tarifa funciona correctamente
- ✅ Se valida que el código de tarifa no exceda 4 caracteres
- ✅ Se permite crear nuevas tarifas
- ✅ Se permite actualizar tarifas existentes
- ✅ Se muestran mensajes informativos al usuario

### **Validaciones Implementadas**
- ✅ Longitud del código de tarifa (máximo 4 caracteres)
- ✅ Año entre 2020 y 2030
- ✅ Valor obligatorio para tarifas fijas
- ✅ Clave única: empresa + rubro + año + código de tarifa

### **Funcionalidades CRUD**
- ✅ **Create**: Crear nueva tarifa
- ✅ **Read**: Mostrar tarifas existentes
- ✅ **Update**: Actualizar tarifa existente
- ✅ **Delete**: Eliminar tarifa

## 🚀 Uso del Sistema

### **Crear Nueva Tarifa**
1. Llenar formulario con código de máximo 4 caracteres
2. Presionar "Guardar Tarifa"
3. Sistema crea nueva tarifa y muestra mensaje de éxito

### **Actualizar Tarifa Existente**
1. Llenar formulario con datos existentes
2. Modificar campos deseados
3. Presionar "Guardar Tarifa"
4. Sistema actualiza tarifa existente y muestra mensaje de éxito

### **Validaciones Automáticas**
- El sistema valida automáticamente la longitud del código
- Muestra mensajes de error si no cumple las restricciones
- Permite continuar solo si todos los datos son válidos

## 📝 Notas Importantes

1. **Código de Tarifa**: Debe tener máximo 4 caracteres
2. **Clave Única**: La combinación empresa + rubro + año + código debe ser única
3. **Actualización**: Si existe la combinación exacta, se actualiza; si no, se crea
4. **Validaciones**: Se aplican tanto en el frontend como en el backend

El problema ha sido completamente resuelto y el sistema de tarifas funciona correctamente.


































