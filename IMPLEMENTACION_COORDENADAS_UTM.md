# Implementación de Coordenadas UTM

## Resumen
Se ha implementado la conversión de coordenadas entre Lat/Lng (WGS84) y UTM (zona 16N para Honduras) en los módulos de Catastro y Control Tributario (Negocios).

## Cambios Realizados

### 1. Módulo de Utilidades de Coordenadas
**Archivo:** `venv/Scripts/tributario/utils_coordenadas.py`

- ✅ Función `latlng_to_utm(lat, lng)`: Convierte coordenadas de latitud/longitud a UTM
- ✅ Función `utm_to_latlng(easting, northing)`: Convierte coordenadas UTM a latitud/longitud
- ✅ Zona UTM configurada: 16N (Honduras)
- ✅ Manejo de errores robusto

### 2. Módulo Tributario - Negocios
**Archivo:** `venv/Scripts/tributario/tributario_app/views.py`

#### Al Guardar Coordenadas:
- ✅ **Actualización de negocio existente**: Convierte lat/lng a UTM antes de guardar
- ✅ **Creación de nuevo negocio**: Convierte lat/lng a UTM antes de guardar
- ✅ Las coordenadas se guardan en formato UTM en la base de datos

#### Al Cargar Coordenadas:
- ✅ **Función `buscar_negocio`**: Convierte UTM a lat/lng para mostrar en el mapa
- ✅ Las coordenadas se convierten automáticamente al cargar un negocio

#### Nuevo Endpoint:
- ✅ `convertir_utm_a_latlng`: Endpoint AJAX para conversión de coordenadas

### 3. Módulo Catastro
**Archivo:** `venv/Scripts/catastro/views.py`

#### Mapa Georreferenciado:
- ✅ **Predios (bdcata1)**: Convierte coordenadas UTM a lat/lng al mostrar en el mapa
- ✅ **Negocios**: Convierte coordenadas UTM a lat/lng al mostrar en el mapa
- ✅ **Centro del mapa**: Convierte coordenadas UTM a lat/lng para centrar el mapa

### 4. URLs Actualizadas
**Archivo:** `venv/Scripts/tributario/tributario_app/urls.py`

- ✅ Agregada ruta: `ajax/convertir-utm-a-latlng/`

## Flujo de Trabajo

### Al Guardar Coordenadas:
1. Usuario hace clic en el mapa → Se capturan coordenadas lat/lng
2. JavaScript envía lat/lng al servidor
3. **Backend convierte lat/lng → UTM**
4. Se guardan coordenadas UTM en la base de datos

### Al Cargar Coordenadas:
1. Se leen coordenadas UTM de la base de datos
2. **Backend convierte UTM → lat/lng**
3. Se envían coordenadas lat/lng al frontend
4. El mapa muestra la ubicación correcta

## Dependencias

### Requerida:
- `pyproj`: Biblioteca para conversión de coordenadas

### Instalación:
```bash
pip install pyproj
```

## Configuración UTM

- **Zona UTM**: 16N (Honduras)
- **Sistema de referencia**: WGS84 (EPSG:4326) → UTM 16N (EPSG:32616)

## Notas Importantes

1. **Compatibilidad hacia atrás**: Si `pyproj` no está disponible, el sistema usa las coordenadas originales sin conversión
2. **Validación**: Se valida que las coordenadas estén en rangos válidos antes de convertir
3. **Manejo de errores**: Si la conversión falla, se usan las coordenadas originales y se registra un warning en los logs

## Archivos Modificados

1. ✅ `venv/Scripts/tributario/utils_coordenadas.py` (nuevo)
2. ✅ `venv/Scripts/tributario/tributario_app/views.py`
3. ✅ `venv/Scripts/tributario/tributario_app/urls.py`
4. ✅ `venv/Scripts/catastro/views.py`

## Pruebas Recomendadas

1. **Guardar coordenadas en Negocios**:
   - Abrir formulario de Maestro de Negocios
   - Hacer clic en el mapa para establecer coordenadas
   - Guardar el negocio
   - Verificar en BD que las coordenadas estén en formato UTM

2. **Cargar coordenadas en Negocios**:
   - Buscar un negocio con coordenadas guardadas
   - Verificar que el mapa muestre la ubicación correcta

3. **Mapa de Catastro**:
   - Abrir mapa georreferenciado
   - Verificar que predios y negocios se muestren en ubicaciones correctas

## Estado de Implementación

✅ **Completado**: Todas las funcionalidades implementadas
✅ **Coordenadas se guardan en UTM**: Implementado
✅ **Coordenadas se muestran correctamente en mapas**: Implementado
✅ **Conversión bidireccional**: Implementado



