# Implementación de Coordenadas UTM en Catastro

## Resumen
Se ha implementado la funcionalidad para mostrar y guardar coordenadas en formato UTM en los formularios de catastro.

## Cambios Realizados

### 1. Endpoints AJAX para Conversión de Coordenadas
**Archivo:** `venv/Scripts/catastro/views.py`

- ✅ `ajax_convertir_latlng_a_utm`: Convierte coordenadas lat/lng a UTM
- ✅ `ajax_convertir_utm_a_latlng`: Convierte coordenadas UTM a lat/lng

**Archivo:** `venv/Scripts/catastro/urls.py`
- ✅ Agregadas rutas para los endpoints de conversión

### 2. Formulario Bienes Inmuebles
**Archivo:** `venv/Scripts/catastro/templates/bienes_inmuebles_form.html`

#### Funcionalidades Implementadas:
- ✅ **Al hacer clic en el mapa**: Convierte lat/lng a UTM usando AJAX y guarda en formato UTM
- ✅ **Al cargar coordenadas**: Si hay coordenadas UTM, las convierte a lat/lng solo para mostrar en el mapa
- ✅ **Display de coordenadas**: Muestra coordenadas en formato UTM (2 decimales)
- ✅ **Campos del formulario**: Guardan y muestran coordenadas en formato UTM

#### Funciones JavaScript Modificadas:
- `applyFromMap()`: Convierte lat/lng a UTM antes de guardar
- `syncMapFromInputs()`: Convierte UTM a lat/lng para mostrar en el mapa
- `updateDisplay()`: Muestra coordenadas UTM (no lat/lng)
- Carga inicial: Convierte UTM a lat/lng para posicionar el mapa

### 3. Vista de Catastro
**Archivo:** `venv/Scripts/catastro/views.py`

- ✅ **Al cargar coordenadas en formulario**: Muestra coordenadas UTM directamente (sin conversión)
- ✅ **Mapa georreferenciado**: Convierte UTM a lat/lng solo para mostrar marcadores en el mapa, pero los datos se mantienen en UTM

### 4. Flujo de Trabajo

#### Al Guardar Coordenadas:
1. Usuario hace clic en el mapa → Se capturan coordenadas lat/lng
2. JavaScript llama a `ajax_convertir_latlng_a_utm`
3. Backend convierte lat/lng → UTM
4. Se guardan coordenadas UTM en los campos del formulario
5. Se guardan coordenadas UTM en la base de datos

#### Al Cargar Coordenadas:
1. Se leen coordenadas UTM de la base de datos
2. Se muestran coordenadas UTM directamente en los campos del formulario
3. Para mostrar en el mapa: JavaScript convierte UTM → lat/lng usando AJAX
4. El mapa muestra la ubicación correcta usando lat/lng

## Archivos Modificados

1. ✅ `venv/Scripts/catastro/views.py` - Funciones AJAX de conversión
2. ✅ `venv/Scripts/catastro/urls.py` - Rutas para endpoints AJAX
3. ✅ `venv/Scripts/catastro/templates/bienes_inmuebles_form.html` - JavaScript actualizado

## Estado de Implementación

✅ **Completado**: 
- Coordenadas se muestran en formato UTM en formularios
- Coordenadas se guardan en formato UTM
- Conversión automática lat/lng ↔ UTM para mostrar en mapas
- Endpoints AJAX funcionando

## Notas Importantes

1. **Formato de visualización**: Las coordenadas UTM se muestran con 2 decimales (ej: 500000.00)
2. **Mapa interactivo**: El mapa sigue funcionando con lat/lng internamente, pero las coordenadas guardadas están en UTM
3. **Compatibilidad**: El sistema mantiene compatibilidad con coordenadas existentes


