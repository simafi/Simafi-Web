# 🛡️ Sistema de Protección de Código

Este sistema ayuda a proteger el código que ya funciona correctamente para evitar que se dañe con cambios futuros.

## 📋 Archivos de Protección

### 1. `proteger_codigo.py`
Script interactivo para crear respaldos y restaurar código.

**Uso básico:**
```bash
python proteger_codigo.py
```

**Funcionalidades:**
- ✅ Crear respaldo de archivo específico antes de cambios
- ✅ Crear checkpoint completo de todos los archivos críticos
- ✅ Listar respaldos disponibles
- ✅ Restaurar código desde respaldo
- ✅ Verificar puntos críticos del código

### 2. `pre_commit_check.py`
Script de verificación antes de hacer commits o cambios importantes.

**Uso:**
```bash
python pre_commit_check.py
```

**Verifica:**
- ✅ Que las funciones críticas existan
- ✅ Que los patrones críticos del código estén presentes
- ✅ Que los imports críticos estén correctos

## 🔄 Flujo de Trabajo Recomendado

### Antes de hacer cambios importantes:

1. **Crear checkpoint completo:**
   ```bash
   python proteger_codigo.py
   # Seleccionar opción 2: Crear checkpoint completo
   ```

2. **Si vas a modificar un archivo específico:**
   ```bash
   python proteger_codigo.py
   # Seleccionar opción 1: Crear respaldo de archivo específico
   ```

3. **Hacer tus cambios**

4. **Verificar que todo sigue funcionando:**
   ```bash
   python pre_commit_check.py
   ```

5. **Si algo se dañó, restaurar:**
   ```bash
   python proteger_codigo.py
   # Seleccionar opción 4: Restaurar respaldo
   ```

## 📦 Archivos Críticos Protegidos

- `simple_views.py` - Lógica de declaraciones y tasas
- `views.py` - Vistas principales
- `models.py` - Modelos de datos
- `ajax_views.py` - Vistas AJAX

## 🎯 Puntos Críticos Documentados

### `simple_views.py`
- **`declaracion_volumen`** (líneas 92-750): Función crítica para guardado de declaraciones
- **`crear_tasas_desde_tarifasics`** (líneas 409-589): Proceso crítico de transferencia de tasas

### `views.py`
- **`tarifas_crud`** (líneas 1650-1800): Vista del formulario de tarifas
- **`plan_arbitrio_crud`** (líneas 1800-2000): Vista del formulario de plan de arbitrio

## ⚠️ Mejores Prácticas

1. **Siempre crear respaldo antes de cambios grandes**
2. **Hacer cambios incrementales** - cambiar poco a poco, no todo de una vez
3. **Probar después de cada cambio** - verificar que sigue funcionando
4. **Documentar cambios importantes** - comentar qué y por qué cambias
5. **Usar Git** - además de estos respaldos, usar control de versiones

## 🔧 Integración con Git (Opcional)

Puedes integrar el pre-commit check con Git usando un hook:

```bash
# Crear hook de pre-commit
cp pre_commit_check.py .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Esto ejecutará las verificaciones automáticamente antes de cada commit.

## 📝 Notas Importantes

- Los respaldos se guardan en `backups/`
- Cada respaldo incluye metadata (fecha, razón, tamaño)
- Los checkpoints incluyen múltiples archivos a la vez
- Siempre se crea un respaldo antes de restaurar (por seguridad)

## 🆘 Si Algo Sale Mal

1. **Listar respaldos disponibles:**
   ```bash
   python proteger_codigo.py
   # Opción 3: Listar respaldos
   ```

2. **Restaurar el último checkpoint:**
   ```bash
   python proteger_codigo.py
   # Opción 4: Restaurar respaldo
   # Seleccionar el checkpoint más reciente
   ```

3. **Verificar que todo volvió a la normalidad:**
   ```bash
   python pre_commit_check.py
   ```























