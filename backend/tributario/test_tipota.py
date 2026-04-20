#!/usr/bin/env python
"""
Script de testeo para verificar el campo tipota en la tabla tasasdecla
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from tributario.models import TasasDecla, Negocio

def test_tipota_field():
    print("🔍 TESTEO DEL CAMPO TIPOTA")
    print("=" * 50)
    
    # 1. Verificar estructura de la tabla
    print("\n1. Verificando estructura de la tabla tasasdecla...")
    try:
        # Obtener un registro de prueba
        tasa = TasasDecla.objects.first()
        if tasa:
            print(f"✅ Registro encontrado: ID {tasa.id}")
            print(f"   - RTM: {tasa.rtm}")
            print(f"   - Rubro: {tasa.rubro}")
            print(f"   - Tipota: '{tasa.tipota}' (tipo: {type(tasa.tipota)})")
            print(f"   - Valor: {tasa.valor}")
            
            # Verificar si tiene atributo tipo (debería dar error)
            try:
                tipo_value = tasa.tipo
                print(f"   - Tipo (ANTIGUO): '{tipo_value}' (tipo: {type(tipo_value)})")
            except AttributeError:
                print("   - Tipo (ANTIGUO): ❌ Campo no existe (correcto)")
        else:
            print("❌ No se encontraron registros en tasasdecla")
            return
    
    except Exception as e:
        print(f"❌ Error al acceder a la tabla: {e}")
        return
    
    # 2. Verificar todos los registros
    print("\n2. Verificando todos los registros...")
    try:
        tasas = TasasDecla.objects.all()[:5]  # Primeros 5 registros
        print(f"📊 Total de registros: {TasasDecla.objects.count()}")
        
        for i, tasa in enumerate(tasas, 1):
            print(f"   {i}. ID {tasa.id} - RTM: {tasa.rtm} - Rubro: {tasa.rubro} - Tipota: '{tasa.tipota}'")
    
    except Exception as e:
        print(f"❌ Error al obtener registros: {e}")
    
    # 3. Verificar si hay registros con tipota vacío
    print("\n3. Verificando registros con tipota vacío...")
    try:
        tasas_vacias = TasasDecla.objects.filter(tipota='')
        print(f"📊 Registros con tipota vacío: {tasas_vacias.count()}")
        
        tasas_con_valor = TasasDecla.objects.exclude(tipota='')
        print(f"📊 Registros con tipota con valor: {tasas_con_valor.count()}")
        
        if tasas_con_valor.exists():
            print("   Valores encontrados:")
            for tasa in tasas_con_valor[:3]:
                print(f"   - ID {tasa.id}: tipota = '{tasa.tipota}'")
    
    except Exception as e:
        print(f"❌ Error al verificar registros: {e}")
    
    # 4. Test de simulación del contexto del template
    print("\n4. Simulando contexto del template...")
    try:
        # Simular lo que hace la vista
        tarifas_ics = []
        tasas = TasasDecla.objects.all()[:3]
        
        for tasa in tasas:
            tarifa_data = {
                'id': tasa.id,
                'rubro': tasa.rubro,
                'cod_tarifa': tasa.cod_tarifa,
                'frecuencia': tasa.frecuencia,
                'tipota': tasa.tipota or 'F',  # Misma lógica que en la vista
                'valor': tasa.valor,
                'nodecla': tasa.nodecla,
                'ano': tasa.ano
            }
            tarifas_ics.append(tarifa_data)
        
        print(f"📊 Datos preparados para template: {len(tarifas_ics)} registros")
        for i, tarifa in enumerate(tarifas_ics, 1):
            print(f"   {i}. ID {tarifa['id']} - Rubro: {tarifa['rubro']} - Tipota: '{tarifa['tipota']}'")
    
    except Exception as e:
        print(f"❌ Error en simulación: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Testeo completado")

if __name__ == "__main__":
    test_tipota_field()









































