# 📋 CÓMO VER LOS LOGS DEL SERVIDOR DJANGO

## 🔍 Ubicación de los Logs

### **Opción 1: Terminal/Consola donde ejecutas el servidor**

Si ejecutaste el servidor con:
```bash
python manage.py runserver 8080
```

Los logs aparecen **directamente en esa misma terminal/consola** donde ejecutaste el comando.

**Pasos:**
1. Busca la ventana/terminal donde ejecutaste `python manage.py runserver`
2. Ahí verás todos los `print()` y mensajes de Django
3. Al guardar una declaración, busca mensajes que empiecen con:
   - `[CREAR Y CALCULAR TASAS]`
   - `[DEBUG]`
   - `[ERROR]`

### **Opción 2: Si usas Visual Studio Code**

1. Abre la terminal integrada (Ctrl + `)
2. Ejecuta el servidor ahí
3. Los logs aparecerán en la pestaña de "Terminal"

### **Opción 3: Si el servidor está en segundo plano**

1. Busca el proceso de Python que está ejecutando Django
2. O reinicia el servidor en una nueva terminal para ver los logs

## 🔎 Qué Buscar en los Logs

Al guardar una declaración, busca estos mensajes clave:

### ✅ **Si el proceso se ejecuta correctamente:**
```
================================================================================
[CREAR Y CALCULAR TASAS] ⚡⚡⚡ INICIANDO PROCESO COMPLETO DE TASAS ⚡⚡⚡
================================================================================
[CREAR Y CALCULAR TASAS] 🚀 EJECUTANDO BLOQUE TRY - PROCESO DE CREAR TASAS
[CREAR Y CALCULAR TASAS] 📊 TarifasICS encontradas: X
[CREAR Y CALCULAR TASAS] 📊 TOTAL Rubros registrados en tarifasics: X
[CREAR Y CALCULAR TASAS] ✅ [X] Tasa creada: Rubro=...
```

### ❌ **Si hay problemas:**
```
[CREAR Y CALCULAR TASAS] ⚠️⚠️⚠️ ADVERTENCIA: No se encontraron tarifasics...
[CREAR Y CALCULAR TASAS] ❌❌❌ ERROR CRÍTICO obteniendo tarifasics: ...
[CREAR Y CALCULAR TASAS] ❌ Error creando tasa para rubro ...
```

## 📝 Ejemplo de Log Completo

Cuando guardes una declaración, deberías ver algo como:

```
[DEBUG] Guardando en tabla declara (DeclaracionVolumen)...
[DEBUG] Declaración creada en tabla declara: 00000000006-2025
[DEBUG] Guardando tasas - Empresa: 0301, RTM: 114-03-23, EXPE: 1151, Año: 2025
[DEBUG] Tasa C0001 creada: 17127.77, idneg=15

================================================================================
[CREAR Y CALCULAR TASAS] ⚡⚡⚡ INICIANDO PROCESO COMPLETO DE TASAS ⚡⚡⚡
================================================================================
[CREAR Y CALCULAR TASAS] 🚀 EJECUTANDO BLOQUE TRY - PROCESO DE CREAR TASAS
[CREAR Y CALCULAR TASAS] 📊 TarifasICS encontradas: 5
[CREAR Y CALCULAR TASAS] 📊 TOTAL Rubros registrados en tarifasics: 5
[CREAR Y CALCULAR TASAS] ✅ [1] Tasa creada: Rubro=T0001, Tipo=F, Valor=0.00, ID=133
[CREAR Y CALCULAR TASAS] ✅ [2] Tasa creada: Rubro=C0002, Tipo=F, Valor=0.00, ID=134
...
```

## 💡 Consejos

1. **Si no ves logs**: El servidor podría estar ejecutándose en otra terminal
2. **Para copiar logs**: Selecciona el texto en la terminal y copia (Ctrl+C)
3. **Para buscar en logs**: Usa Ctrl+F en la terminal si tu terminal lo soporta
4. **Para guardar logs**: Redirige la salida a un archivo:
   ```bash
   python manage.py runserver 8080 > logs.txt 2>&1
   ```

## 🆘 Si No Encuentras los Logs

1. **Reinicia el servidor** en una terminal visible:
   ```bash
   cd C:\simafiweb\venv\Scripts\tributario
   python manage.py runserver 8080
   ```

2. **Guarda una declaración** y observa la terminal

3. **Copia los mensajes** que aparezcan y compártelos























