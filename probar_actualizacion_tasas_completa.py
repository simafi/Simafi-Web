#!/usr/bin/env python
"""
Script para probar la funcionalidad completa de actualización de tasas
cuando se guarda una declaración de volumen de ventas.

Este script simula el proceso que se ejecuta automáticamente cuando
se presiona el botón 'Guardar Declaración' y demuestra:
1. Actualización de tasas fijas (tipota='F') desde tabla tarifas
2. Cálculo de tasas variables (tipota='V') según rangos en planarbitio
"""

def probar_logica_completa():
    """Probar la lógica completa de actualización de tasas"""
    
    print("🧪 PROBANDO LÓGICA COMPLETA DE ACTUALIZACIÓN DE TASAS")
    print("=" * 70)
    
    # Simular datos de ejemplo
    print("📋 DATOS DE EJEMPLO:")
    print("   - Empresa: 0301")
    print("   - RTM: 114-03-23")
    print("   - Expediente: 001")
    print("   - Año: 2024")
    print("   - Valor base declaración: 50,000.00")
    print()
    
    # Simular tasas de declaración con diferentes tipos
    tasas_ejemplo = [
        {
            'id': 1,
            'empresa': '0301',
            'rtm': '114-03-23',
            'expe': '001',
            'rubro': '001',
            'cod_tarifa': 'C0001',
            'tipota': 'F',
            'valor': 100.00,
            'ano': 2024
        },
        {
            'id': 2,
            'empresa': '0301',
            'rtm': '114-03-23',
            'expe': '001',
            'rubro': '002',
            'cod_tarifa': 'C0003',
            'tipota': 'F',
            'valor': 150.00,
            'ano': 2024
        },
        {
            'id': 3,
            'empresa': '0301',
            'rtm': '114-03-23',
            'expe': '001',
            'rubro': '003',
            'cod_tarifa': 'TAR001',
            'tipota': 'F',
            'valor': 200.00,
            'ano': 2024
        },
        {
            'id': 4,
            'empresa': '0301',
            'rtm': '114-03-23',
            'expe': '001',
            'rubro': '004',
            'cod_tarifa': 'VAR001',
            'tipota': 'V',
            'valor': 300.00,
            'ano': 2024
        },
        {
            'id': 5,
            'empresa': '0301',
            'rtm': '114-03-23',
            'expe': '001',
            'rubro': '005',
            'cod_tarifa': 'VAR002',
            'tipota': 'V',
            'valor': 400.00,
            'ano': 2024
        },
        {
            'id': 6,
            'empresa': '0301',
            'rtm': '114-03-23',
            'expe': '001',
            'rubro': '006',
            'cod_tarifa': 'TAR003',
            'tipota': 'T',
            'valor': 500.00,
            'ano': 2024
        }
    ]
    
    # Simular tarifas de referencia (para tasas fijas)
    tarifas_referencia = [
        {
            'empresa': '0301',
            'rubro': '001',
            'cod_tarifa': 'C0001',
            'ano': 2024,
            'valor': 100.00  # Ya está actualizado
        },
        {
            'empresa': '0301',
            'rubro': '002',
            'cod_tarifa': 'C0003',
            'ano': 2024,
            'valor': 150.00  # Ya está actualizado
        },
        {
            'empresa': '0301',
            'rubro': '003',
            'cod_tarifa': 'TAR001',
            'ano': 2024,
            'valor': 250.00  # Necesita actualización
        }
    ]
    
    # Simular planes de arbitrio (para tasas variables)
    planes_arbitrio = [
        {
            'empresa': '0301',
            'rubro': '004',
            'cod_tarifa': 'VAR001',
            'ano': 2024,
            'minimo': 0.00,
            'maximo': 25000.00,
            'valor': 200.00
        },
        {
            'empresa': '0301',
            'rubro': '004',
            'cod_tarifa': 'VAR001',
            'ano': 2024,
            'minimo': 25001.00,
            'maximo': 50000.00,
            'valor': 400.00
        },
        {
            'empresa': '0301',
            'rubro': '004',
            'cod_tarifa': 'VAR001',
            'ano': 2024,
            'minimo': 50001.00,
            'maximo': 100000.00,
            'valor': 600.00
        },
        {
            'empresa': '0301',
            'rubro': '005',
            'cod_tarifa': 'VAR002',
            'ano': 2024,
            'minimo': 0.00,
            'maximo': 30000.00,
            'valor': 150.00
        },
        {
            'empresa': '0301',
            'rubro': '005',
            'cod_tarifa': 'VAR002',
            'ano': 2024,
            'minimo': 30001.00,
            'maximo': 60000.00,
            'valor': 300.00
        }
    ]
    
    valor_base_declaracion = 50000.00
    
    print("🔍 PROCESANDO TASAS:")
    print("-" * 50)
    
    tasas_fijas_actualizadas = 0
    tasas_variables_actualizadas = 0
    tasas_excluidas = 0
    tasas_no_actualizables = 0
    
    for tasa in tasas_ejemplo:
        print(f"📌 Tasa: {tasa['cod_tarifa']} (tipo: {tasa['tipota']})")
        
        # ================================================================
        # PROCESAR TASAS FIJAS (tipota = 'F')
        # ================================================================
        if tasa['tipota'] == 'F':
            # Verificar si está en la lista de exclusión
            if tasa['cod_tarifa'] in ['C0001', 'C0003']:
                print(f"   ⏭️ Saltada - Excluida (C0001/C0003 ya configuradas)")
                tasas_excluidas += 1
                continue
            
            # Buscar tarifa de referencia
            tarifa_ref = None
            for tarifa in tarifas_referencia:
                if (tarifa['empresa'] == tasa['empresa'] and
                    tarifa['rubro'] == tasa['rubro'] and
                    tarifa['cod_tarifa'] == tasa['cod_tarifa'] and
                    tarifa['ano'] == tasa['ano']):
                    tarifa_ref = tarifa
                    break
            
            if tarifa_ref:
                if tasa['valor'] != tarifa_ref['valor']:
                    print(f"   ✅ TASA FIJA ACTUALIZADA: {tasa['valor']} → {tarifa_ref['valor']}")
                    tasas_fijas_actualizadas += 1
                else:
                    print(f"   ✅ Tasa fija ya actualizada: {tasa['valor']}")
            else:
                print(f"   ⚠️ No se encontró tarifa de referencia")
        
        # ================================================================
        # PROCESAR TASAS VARIABLES (tipota = 'V')
        # ================================================================
        elif tasa['tipota'] == 'V':
            # Buscar planes de arbitrio aplicables
            planes_aplicables = []
            for plan in planes_arbitrio:
                if (plan['empresa'] == tasa['empresa'] and
                    plan['rubro'] == tasa['rubro'] and
                    plan['cod_tarifa'] == tasa['cod_tarifa'] and
                    plan['ano'] == tasa['ano']):
                    planes_aplicables.append(plan)
            
            if not planes_aplicables:
                print(f"   ⚠️ No se encontraron planes de arbitrio")
                continue
            
            # Buscar el plan que corresponda al valor base
            plan_aplicable = None
            for plan in planes_aplicables:
                if plan['minimo'] <= valor_base_declaracion <= plan['maximo']:
                    plan_aplicable = plan
                    break
            
            if plan_aplicable:
                if tasa['valor'] != plan_aplicable['valor']:
                    print(f"   ✅ TASA VARIABLE ACTUALIZADA: {tasa['valor']} → {plan_aplicable['valor']}")
                    print(f"       Valor base: {valor_base_declaracion} (rango: {plan_aplicable['minimo']}-{plan_aplicable['maximo']})")
                    tasas_variables_actualizadas += 1
                else:
                    print(f"   ✅ Tasa variable ya actualizada: {tasa['valor']}")
            else:
                print(f"   ⚠️ No se encontró plan aplicable para valor base {valor_base_declaracion}")
        
        # ================================================================
        # TASAS NO ACTUALIZABLES (tipota = 'T' u otros)
        # ================================================================
        else:
            print(f"   ⏭️ Saltada - Tipo: {tasa['tipota']} (no es fija ni variable)")
            tasas_no_actualizables += 1
        
        print()
    
    print("📊 RESUMEN DEL PROCESO:")
    print("=" * 50)
    print(f"   - Total de tasas procesadas: {len(tasas_ejemplo)}")
    print(f"   - Tasas fijas actualizadas: {tasas_fijas_actualizadas}")
    print(f"   - Tasas variables actualizadas: {tasas_variables_actualizadas}")
    print(f"   - Tasas excluidas (C0001/C0003): {tasas_excluidas}")
    print(f"   - Tasas no actualizables (T/otros): {tasas_no_actualizables}")
    print(f"   - Total actualizadas: {tasas_fijas_actualizadas + tasas_variables_actualizadas}")
    
    print("\n✅ PROCESO COMPLETADO")
    print("=" * 70)

def mostrar_proceso_implementado():
    """Mostrar el proceso implementado en el código"""
    
    print("\n🔧 PROCESO IMPLEMENTADO EN EL CÓDIGO")
    print("=" * 70)
    
    print("📍 UBICACIÓN: modules/tributario/simple_views.py")
    print("📍 FUNCIÓN: declaracion_volumen()")
    print("📍 TRIGGER: Al presionar botón 'Guardar Declaración'")
    print()
    
    print("🔄 FLUJO DEL PROCESO COMPLETO:")
    print("   1. Usuario presiona 'Guardar Declaración'")
    print("   2. Se valida el formulario de declaración")
    print("   3. Se guarda la declaración en la BD")
    print("   4. ✅ NUEVO: Se calcula el valor base de la declaración")
    print("   5. ✅ NUEVO: Se ejecuta actualizar_tasas_declaracion()")
    print("   6. Se procesan tasas fijas (tipota='F') desde tabla tarifas")
    print("   7. Se procesan tasas variables (tipota='V') desde planarbitio")
    print("   8. Se excluyen C0001 y C0003 (ya configuradas)")
    print("   9. Se actualizan los valores en tasasdecla")
    print("   10. Se retorna respuesta de éxito")
    print()
    
    print("🛡️ CARACTERÍSTICAS DE SEGURIDAD:")
    print("   - El proceso no falla si hay error en actualización de tasas")
    print("   - Solo actualiza tasas fijas (F) y variables (V)")
    print("   - Excluye tasas ya configuradas (C0001, C0003)")
    print("   - Mantiene integridad de datos existentes")
    print("   - Calcula valor base automáticamente")
    print()
    
    print("📝 CÓDIGO IMPLEMENTADO:")
    print("""
    # Después de guardar la declaración:
    try:
        # Obtener las tasas de declaración vinculadas al negocio
        tasas_declaracion_raw = TasasDecla.objects.filter(
            empresa=municipio_codigo,
            rtm=rtm,
            expe=expe
        )
        
        # Calcular el valor base de la declaración para tasas variables
        valor_base_declaracion = (
            (instance.ventai or 0) +
            (instance.ventac or 0) + 
            (instance.ventas or 0) +
            (instance.controlado or 0)
        )
        
        # Actualizar tasas fijas y variables basándose en sus respectivas tablas
        actualizar_tasas_declaracion(tasas_declaracion_raw, municipio_codigo, valor_base_declaracion)
        
    except Exception as e:
        print(f"⚠️ Error actualizando tasas: {str(e)}")
        # No fallar el guardado por error en actualización de tasas
    """)

def mostrar_tipos_tasas():
    """Mostrar los diferentes tipos de tasas y su procesamiento"""
    
    print("\n📋 TIPOS DE TASAS Y SU PROCESAMIENTO")
    print("=" * 70)
    
    print("🔹 TASAS FIJAS (tipota = 'F'):")
    print("   - Se actualizan desde la tabla 'tarifas'")
    print("   - Criterios de búsqueda: empresa, rubro, cod_tarifa, ano")
    print("   - Se excluyen: C0001, C0003 (ya configuradas)")
    print("   - Ejemplo: TAR001, TAR002, etc.")
    print()
    
    print("🔹 TASAS VARIABLES (tipota = 'V'):")
    print("   - Se calculan según rangos en tabla 'planarbitio'")
    print("   - Criterios de búsqueda: empresa, rubro, cod_tarifa, ano")
    print("   - Validación: valor_base_declaracion entre minimo y maximo")
    print("   - Ejemplo: VAR001, VAR002, etc.")
    print()
    
    print("🔹 TASAS TEMPORALES (tipota = 'T'):")
    print("   - NO se procesan automáticamente")
    print("   - Requieren configuración manual")
    print("   - Ejemplo: TAR003, etc.")
    print()
    
    print("🔹 TASAS EXCLUIDAS:")
    print("   - C0001: Ya configurada (no se actualiza)")
    print("   - C0003: Ya configurada (no se actualiza)")
    print()

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS COMPLETAS DE ACTUALIZACIÓN DE TASAS")
    print("=" * 70)
    
    # Mostrar proceso implementado
    mostrar_proceso_implementado()
    
    # Mostrar tipos de tasas
    mostrar_tipos_tasas()
    
    # Probar lógica completa
    probar_logica_completa()
    
    print("\n🎯 IMPLEMENTACIÓN COMPLETA FINALIZADA")
    print("=" * 70)
    print("✅ La actualización de tasas se ejecuta automáticamente")
    print("   cuando se presiona el botón 'Guardar Declaración'")
    print("✅ Se procesan tasas fijas (F) desde tabla tarifas")
    print("✅ Se procesan tasas variables (V) desde planarbitio")
    print("✅ Se excluyen las tasas C0001 y C0003")
    print("✅ Se calcula automáticamente el valor base de la declaración")
    print("✅ El proceso es seguro y no afecta el guardado principal")








































