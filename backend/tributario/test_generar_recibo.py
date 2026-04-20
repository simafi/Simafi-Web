#!/usr/bin/env python
"""
Script de prueba para diagnosticar por qué no se genera el recibo
"""
import os
import sys
import django

# Cambiar al directorio correcto
os.chdir(r'C:\simafiweb')

# Configurar Django
sys.path.append('C:\\simafiweb')
sys.path.append('C:\\simafiweb\\venv\\Scripts')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion.settings')

try:
    django.setup()
    DJANGO_CONFIGURADO = True
except Exception as e:
    print(f"⚠️ Error configurando Django: {e}")
    DJANGO_CONFIGURADO = False
    sys.exit(1)

from django.db.models import Q
# Importar desde el módulo correcto
try:
    from venv.Scripts.tributario.models import TransaccionesIcs, TasasDecla, Actividad, Negocio, Rubro
except ImportError:
    # Intentar importación alternativa
    import sys
    sys.path.insert(0, r'C:\simafiweb\venv\Scripts')
    from tributario.models import TransaccionesIcs, TasasDecla, Actividad, Negocio, Rubro
from decimal import Decimal

def test_generar_recibo(empresa, rtm, expe, tipo='cuota', cuota_hasta=1, monto=None):
    """
    Prueba completa de generación de recibo
    """
    print("=" * 80)
    print("🔍 TEST DE GENERACIÓN DE RECIBO")
    print("=" * 80)
    print(f"\n📋 Parámetros:")
    print(f"   Empresa: {empresa}")
    print(f"   RTM: {rtm}")
    print(f"   EXPE: {expe}")
    print(f"   Tipo: {tipo}")
    if tipo == 'cuota':
        print(f"   Cuota hasta: {cuota_hasta}")
    else:
        print(f"   Monto: {monto}")
    print()
    
    # PASO 1: Verificar que existe el negocio
    print("📌 PASO 1: Verificar negocio")
    print("-" * 80)
    try:
        negocio = Negocio.objects.filter(empresa=empresa, rtm=rtm, expe=expe).first()
        if negocio:
            print(f"✅ Negocio encontrado:")
            print(f"   ID: {negocio.id}")
            print(f"   Nombre: {negocio.nombrenego}")
            print(f"   Comerciante: {negocio.comerciante}")
        else:
            print(f"❌ Negocio NO encontrado con empresa={empresa}, rtm={rtm}, expe={expe}")
            return False
    except Exception as e:
        print(f"❌ Error al buscar negocio: {e}")
        return False
    print()
    
    # PASO 2: Verificar transacciones pendientes
    print("📌 PASO 2: Verificar transacciones pendientes")
    print("-" * 80)
    try:
        transacciones_pendientes = TransaccionesIcs.objects.filter(
            empresa=empresa,
            rtm=rtm,
            expe=expe,
            operacion='D',
            saldoact__gt=0
        ).order_by('ano', 'mes', 'rubro')
        
        total_transacciones = transacciones_pendientes.count()
        print(f"✅ Transacciones encontradas: {total_transacciones}")
        
        if total_transacciones == 0:
            print("❌ No hay transacciones pendientes con saldoact > 0")
            print("\n🔍 Verificando todas las transacciones (sin filtro de saldo):")
            todas = TransaccionesIcs.objects.filter(
                empresa=empresa,
                rtm=rtm,
                expe=expe,
                operacion='D'
            )
            print(f"   Total transacciones con operacion='D': {todas.count()}")
            if todas.exists():
                print("\n   Primeras 5 transacciones:")
                for i, t in enumerate(todas[:5], 1):
                    print(f"   {i}. Año: {t.ano}, Mes: {t.mes}, Rubro: {t.rubro}, SaldoAct: {t.saldoact}")
            return False
        
        print("\n   Primeras 10 transacciones pendientes:")
        for i, t in enumerate(transacciones_pendientes[:10], 1):
            print(f"   {i}. Año: {t.ano}, Mes: {t.mes}, Rubro: {t.rubro}, SaldoAct: {t.saldoact}")
    except Exception as e:
        print(f"❌ Error al buscar transacciones: {e}")
        import traceback
        traceback.print_exc()
        return False
    print()
    
    # PASO 3: Agrupar por periodos
    print("📌 PASO 3: Agrupar transacciones por periodos (año-mes)")
    print("-" * 80)
    try:
        transacciones_lista = list(transacciones_pendientes)
        periodos = {}
        
        for trans in transacciones_lista:
            ano = int(float(trans.ano)) if trans.ano else 0
            mes_str = str(trans.mes).strip() if trans.mes else ''
            if mes_str.isdigit():
                mes_normalizado = mes_str.zfill(2)
            else:
                mes_normalizado = mes_str.zfill(2) if mes_str else '00'
            
            periodo_key = f"{ano}-{mes_normalizado}"
            
            if periodo_key not in periodos:
                periodos[periodo_key] = {
                    'ano': ano,
                    'mes': mes_normalizado,
                    'transacciones': []
                }
            periodos[periodo_key]['transacciones'].append(trans)
        
        # Ordenar periodos
        def ordenar_periodo(item):
            periodo_data = item[1]
            ano = periodo_data['ano']
            mes_str = periodo_data['mes']
            mes_num = int(mes_str) if mes_str.isdigit() else 0
            return (ano, mes_num)
        
        periodos_ordenados = sorted(periodos.items(), key=ordenar_periodo)
        
        print(f"✅ Periodos únicos encontrados: {len(periodos_ordenados)}")
        for periodo_key, periodo_data in periodos_ordenados[:10]:
            print(f"   {periodo_key}: {len(periodo_data['transacciones'])} transacciones")
    except Exception as e:
        print(f"❌ Error al agrupar periodos: {e}")
        import traceback
        traceback.print_exc()
        return False
    print()
    
    # PASO 4: Determinar transacciones a pagar
    print("📌 PASO 4: Determinar transacciones a pagar")
    print("-" * 80)
    try:
        transacciones_a_pagar = []
        periodos_a_pagar = []
        
        if tipo == 'cuota':
            periodos_a_pagar = periodos_ordenados[:cuota_hasta]
            print(f"✅ Modo cuota: Seleccionando primeros {cuota_hasta} periodos")
            for periodo_key, periodo_data in periodos_a_pagar:
                for trans in periodo_data['transacciones']:
                    transacciones_a_pagar.append(trans)
        else:
            monto_abono = Decimal(str(monto)) if monto else Decimal('0')
            monto_restante = monto_abono
            print(f"✅ Modo parcial: Monto a abonar: L. {monto_abono}")
            
            for periodo_key, periodo_data in periodos_ordenados:
                if monto_restante <= 0:
                    break
                
                saldo_periodo = Decimal('0')
                for trans in periodo_data['transacciones']:
                    saldo_pendiente = Decimal(str(trans.saldoact)) if trans.saldoact else Decimal('0')
                    if saldo_pendiente > 0:
                        saldo_periodo += saldo_pendiente
                
                if saldo_periodo > 0:
                    if monto_restante >= saldo_periodo:
                        for trans in periodo_data['transacciones']:
                            saldo_pendiente = Decimal(str(trans.saldoact)) if trans.saldoact else Decimal('0')
                            if saldo_pendiente > 0:
                                transacciones_a_pagar.append({
                                    'transaccion': trans,
                                    'monto_a_aplicar': saldo_pendiente
                                })
                        monto_restante -= saldo_periodo
                    else:
                        for trans in periodo_data['transacciones']:
                            if monto_restante <= 0:
                                break
                            saldo_pendiente = Decimal(str(trans.saldoact)) if trans.saldoact else Decimal('0')
                            if saldo_pendiente > 0:
                                monto_a_aplicar = min(monto_restante, saldo_pendiente)
                                transacciones_a_pagar.append({
                                    'transaccion': trans,
                                    'monto_a_aplicar': monto_a_aplicar
                                })
                                monto_restante -= monto_a_aplicar
        
        print(f"✅ Transacciones a pagar: {len(transacciones_a_pagar)}")
        if len(transacciones_a_pagar) == 0:
            print("❌ No hay transacciones seleccionadas para pagar")
            return False
    except Exception as e:
        print(f"❌ Error al determinar transacciones a pagar: {e}")
        import traceback
        traceback.print_exc()
        return False
    print()
    
    # PASO 5: Vincular con cuentas desde TasasDecla
    print("📌 PASO 5: Vincular rubros con cuentas desde TasasDecla")
    print("-" * 80)
    transacciones_por_cuenta = {}
    cuentas_no_encontradas = []
    cuentas_encontradas = []
    
    for item in transacciones_a_pagar:
        if tipo == 'cuota':
            trans = item
            monto = Decimal(str(trans.saldoact)) if trans.saldoact else Decimal('0')
        else:
            trans = item['transaccion']
            monto = item['monto_a_aplicar']
        
        rubro = trans.rubro or ''
        ano_trans = int(float(trans.ano)) if trans.ano else 0
        
        # Buscar cuenta en TasasDecla
        cuenta = ''
        try:
            tasa_decla = TasasDecla.objects.filter(
                empresa=empresa,
                rtm=rtm,
                expe=expe,
                ano=ano_trans,
                rubro=rubro
            ).first()
            
            if tasa_decla and tasa_decla.cuenta:
                cuenta = tasa_decla.cuenta.strip()
                if cuenta not in cuentas_encontradas:
                    cuentas_encontradas.append(cuenta)
            else:
                if rubro not in cuentas_no_encontradas:
                    cuentas_no_encontradas.append(rubro)
        except Exception as e:
            print(f"   ⚠️ Error buscando cuenta para rubro {rubro}: {e}")
        
        if not cuenta:
            cuenta = 'SIN_CUENTA'
        
        # Obtener descripción desde Actividad
        descripcion = ''
        try:
            actividad = Actividad.objects.filter(
                empresa=empresa,
                codigo=cuenta
            ).first()
            
            if actividad and actividad.descripcion:
                descripcion = actividad.descripcion.strip()
        except Exception as e:
            print(f"   ⚠️ Error buscando descripción para cuenta {cuenta}: {e}")
        
        # Fallback a descripción del rubro
        if not descripcion:
            try:
                rubro_obj = Rubro.objects.filter(empresa=empresa, codigo=rubro).first()
                if rubro_obj and rubro_obj.descripcion:
                    descripcion = rubro_obj.descripcion.strip()
            except:
                pass
        
        if not descripcion:
            descripcion = f'Rubro {rubro}'
        
        # Agrupar por cuenta
        if cuenta not in transacciones_por_cuenta:
            transacciones_por_cuenta[cuenta] = {
                'cuenta': cuenta,
                'descripcion': descripcion,
                'valor': Decimal('0')
            }
        
        transacciones_por_cuenta[cuenta]['valor'] += monto
    
    print(f"✅ Cuentas encontradas en TasasDecla: {len(cuentas_encontradas)}")
    if cuentas_encontradas:
        print(f"   Cuentas: {', '.join(cuentas_encontradas[:10])}")
    
    if cuentas_no_encontradas:
        print(f"⚠️ Rubros sin cuenta en TasasDecla: {len(cuentas_no_encontradas)}")
        print(f"   Rubros: {', '.join(cuentas_no_encontradas[:10])}")
    
    print(f"\n✅ Transacciones agrupadas por cuenta: {len(transacciones_por_cuenta)}")
    for cuenta, data in list(transacciones_por_cuenta.items())[:10]:
        print(f"   {cuenta}: {data['descripcion'][:50]}... = L. {float(data['valor']):.2f}")
    print()
    
    # PASO 6: Resumen final
    print("📌 PASO 6: Resumen final")
    print("-" * 80)
    total_valor = sum(float(item['valor']) for item in transacciones_por_cuenta.values())
    print(f"✅ Total de transacciones procesadas: {len(transacciones_a_pagar)}")
    print(f"✅ Total de cuentas: {len(transacciones_por_cuenta)}")
    print(f"✅ Total a pagar: L. {total_valor:.2f}")
    print()
    
    if len(transacciones_por_cuenta) > 0:
        print("✅ RECIBO PUEDE SER GENERADO")
        return True
    else:
        print("❌ NO SE PUEDE GENERAR RECIBO - No hay transacciones agrupadas")
        return False


if __name__ == '__main__':
    # Parámetros de prueba - CAMBIAR SEGÚN NECESITE
    EMPRESA = '0301'
    RTM = '114-03-23'
    EXPE = '1151'
    TIPO = 'cuota'  # 'cuota' o 'parcial'
    CUOTA_HASTA = 1
    MONTO = None  # Solo si TIPO == 'parcial'
    
    print("\n" + "=" * 80)
    print("🧪 SCRIPT DE PRUEBA - GENERACIÓN DE RECIBO")
    print("=" * 80)
    print("\n💡 Para cambiar los parámetros, edite las variables al final del script")
    print()
    
    resultado = test_generar_recibo(EMPRESA, RTM, EXPE, TIPO, CUOTA_HASTA, MONTO)
    
    print("\n" + "=" * 80)
    if resultado:
        print("✅ TEST COMPLETADO - El recibo puede generarse")
    else:
        print("❌ TEST FALLIDO - Revisar los pasos anteriores")
    print("=" * 80)

