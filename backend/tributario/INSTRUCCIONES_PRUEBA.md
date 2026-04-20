# Instrucciones para Probar el Sistema de Búsqueda de Negocios

## 1. Acceder al Formulario
- Abre tu navegador
- Ve a: `http://127.0.0.1:8000/maestro-negocios/`

## 2. Datos de Prueba
Usa estos datos que sabemos que existen en la base de datos:

**Empresa:** 0301
**RTM:** 29  
**Expediente:** 4

## 3. Pasos de Prueba
1. Ingresa "0301" en el campo Empresa
2. Ingresa "29" en el campo RTM
3. Ingresa "4" en el campo Expediente
4. Haz clic fuera de cualquiera de estos campos (evento blur)

## 4. Resultado Esperado
- El formulario debería llenarse automáticamente con:
  - Nombre del Negocio: "PULPERIA ROSITA"
  - Comerciante: "CABRERA ALBERTO MARIA ROSA"
  - RTN Personal: "0056-073-014"
  - Catastral: "567314"
  - Dirección: "COL. EL SIETE DOS CUADRAS ABAJO DEL CARRIL DE"
  - Actividad: "113-13"
  - Fecha Inicio: "1998-07-01"

## 5. Verificar Logs
- Abre la consola del navegador (F12)
- Deberías ver logs como:
  - "Buscando negocio con RTM: 29, Expediente: 4, Empresa: 0301"
  - "URL de búsqueda: /ajax/buscar-negocio/?empre=0301&rtm=29&expe=4"
  - "Datos recibidos: {...}"
  - "Negocio encontrado y formulario rellenado."

## 6. Otros Datos de Prueba
Si el primer conjunto no funciona, prueba con:
- Empresa: 0301, RTM: 37, Expediente: 5
- Empresa: 0301, RTM: 8, Expediente: 6

## 7. Solución de Problemas
Si no funciona:
1. Verifica que el servidor Django esté ejecutándose
2. Revisa la consola del navegador para errores
3. Revisa los logs del servidor Django
4. Verifica que la base de datos MySQL esté conectada 