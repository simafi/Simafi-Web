#!/usr/bin/env python3
"""
Fix para el error UnboundLocalError: cannot access local variable 'tarifas_ics'
en la vista declaracion_volumen
"""

import os
import re

def fix_tarifas_ics_error():
    """Corregir el error de variable tarifas_ics no inicializada"""
    
    print("🔧 CORRIGIENDO ERROR DE tarifas_ics")
    print("=" * 50)
    
    # Buscar archivos de vistas
    vista_paths = [
        'C:/simafiweb/venv/Scripts/tributario/modules/tributario/views.py',
        'C:/simafiweb/venv/Scripts/tributario/modules/tributario/views_clean.py'
    ]
    
    for vista_path in vista_paths:
        if os.path.exists(vista_path):
            print(f"📝 Procesando: {vista_path}")
            
            try:
                # Leer archivo
                with open(vista_path, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                # Buscar la función declaracion_volumen
                if 'def declaracion_volumen(request):' in contenido:
                    print("✅ Función declaracion_volumen encontrada")
                    
                    # Buscar el patrón problemático
                    # El problema es que tarifas_ics se define dentro de un try/except
                    # pero se usa fuera sin inicialización previa
                    
                    # Patrón 1: Inicializar tarifas_ics al inicio de la función
                    patron_inicio = r'(def declaracion_volumen\(request\):[^{]*?)(municipio_codigo = )'
                    
                    if re.search(patron_inicio, contenido, re.DOTALL):
                        # Agregar inicialización de variables al inicio
                        inicializacion = '''    """Vista para declaración de volumen de ventas"""
    
    # Inicializar variables al inicio para evitar UnboundLocalError
    negocio = None
    declaraciones = []
    tarifas_ics = []
    mensaje = None
    exito = False
    
    '''
                        
                        contenido_nuevo = re.sub(
                            patron_inicio,
                            r'\1' + inicializacion + r'\2',
                            contenido,
                            flags=re.DOTALL
                        )
                        
                        if contenido_nuevo != contenido:
                            print("✅ Inicialización de variables agregada al inicio")
                            contenido = contenido_nuevo
                    
                    # Patrón 2: Asegurar que tarifas_ics siempre tenga un valor por defecto
                    # Buscar donde se define tarifas_ics dentro del try y agregar inicialización antes
                    patron_try_tarifas = r'(try:[^}]*?)(tarifas_ics_raw = TarifasICS\.obtener_tarifas_por_negocio)'
                    
                    if re.search(patron_try_tarifas, contenido, re.DOTALL):
                        # Agregar inicialización antes del try
                        contenido_nuevo = re.sub(
                            patron_try_tarifas,
                            r'\1                # Inicializar tarifas_ics por defecto\n                tarifas_ics = []\n                \n                \2',
                            contenido,
                            flags=re.DOTALL
                        )
                        
                        if contenido_nuevo != contenido:
                            print("✅ Inicialización de tarifas_ics agregada antes del try")
                            contenido = contenido_nuevo
                    
                    # Patrón 3: Asegurar que en el except también se inicialice tarifas_ics
                    patron_except = r'(except Exception as e:[^}]*?declaraciones = \[\])([\s]*?)(from tributario_app\.forms)'
                    
                    if re.search(patron_except, contenido, re.DOTALL):
                        contenido_nuevo = re.sub(
                            patron_except,
                            r'\1\n                tarifas_ics = []\2\3',
                            contenido,
                            flags=re.DOTALL
                        )
                        
                        if contenido_nuevo != contenido:
                            print("✅ Inicialización de tarifas_ics agregada en except")
                            contenido = contenido_nuevo
                    
                    # Crear backup del archivo original
                    backup_path = vista_path + '.backup_tarifas_fix'
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(open(vista_path, 'r', encoding='utf-8').read())
                    print(f"✅ Backup creado: {backup_path}")
                    
                    # Guardar archivo corregido
                    with open(vista_path, 'w', encoding='utf-8') as f:
                        f.write(contenido)
                    
                    print(f"✅ Archivo corregido: {vista_path}")
                    
                else:
                    print("⚠️  Función declaracion_volumen no encontrada en este archivo")
                    
            except Exception as e:
                print(f"❌ Error procesando {vista_path}: {e}")

def crear_vista_corregida_completa():
    """Crear una vista completamente corregida como referencia"""
    
    vista_corregida = '''def declaracion_volumen(request):
    """Vista para declaración de volumen de ventas"""
    from .models import DeclaracionVolumen, Negocio, TarifasICS, Rubro
    
    # Inicializar TODAS las variables al inicio para evitar UnboundLocalError
    negocio = None
    declaraciones = []
    tarifas_ics = []
    mensaje = None
    exito = False
    municipio_codigo = request.session.get('municipio_codigo', '0301')
    
    # Obtener parámetros de la URL
    rtm = request.GET.get('rtm', '')
    expe = request.GET.get('expe', '')
    
    if rtm and expe:
        try:
            # Buscar el negocio
            negocio = Negocio.objects.get(rtm=rtm, expe=expe, municipio=municipio_codigo)
            
            # Buscar declaraciones existentes
            declaraciones = DeclaracionVolumen.objects.filter(
                rtm=rtm, 
                expe=expe
            ).order_by('-ano', '-mes')
            
            # Obtener tarifas ICS vinculadas al negocio
            try:
                tarifas_ics_raw = TarifasICS.obtener_tarifas_por_negocio(negocio.id)
                tarifas_ics = []
                
                for tarifa_ics in tarifas_ics_raw:
                    # Buscar información del rubro
                    try:
                        rubro_info = Rubro.objects.get(
                            codigo=tarifa_ics.cod_tarifa,
                            municipio=municipio_codigo
                        )
                        rubro_nombre = rubro_info.descripcion
                    except Rubro.DoesNotExist:
                        try:
                            rubro_info = Rubro.objects.filter(
                                codigo__icontains=tarifa_ics.cod_tarifa[:3],
                                municipio=municipio_codigo
                            ).first()
                            rubro_nombre = rubro_info.descripcion if rubro_info else f"Rubro {tarifa_ics.cod_tarifa}"
                        except:
                            rubro_nombre = f"Rubro {tarifa_ics.cod_tarifa}"
                    except Exception as e:
                        rubro_nombre = f"Rubro {tarifa_ics.cod_tarifa}"
                    
                    # Agregar información del rubro al objeto tarifa_ics
                    tarifa_ics.rubro_nombre = rubro_nombre
                    tarifas_ics.append(tarifa_ics)
                    
            except Exception as e:
                print(f"Error al cargar tarifas ICS: {e}")
                tarifas_ics = []
                
        except Negocio.DoesNotExist:
            mensaje = "No se encontró el negocio con el RTM y expediente proporcionados"
            exito = False
        except Exception as e:
            print(f"Error al cargar declaraciones: {e}")
            mensaje = f"Error al cargar datos: {str(e)}"
            exito = False
            declaraciones = []
            tarifas_ics = []

    from tributario_app.forms import DeclaracionVolumenForm
    initial_data = {}
    if negocio:
        initial_data = {'rtm': rtm, 'expe': expe}
    form = DeclaracionVolumenForm(initial=initial_data)

    return render(request, 'declaracion_volumen.html', {
        'form': form, 
        'negocio': negocio, 
        'declaraciones': declaraciones,
        'tarifas_ics': tarifas_ics,  # ← SIEMPRE inicializada
        'mensaje': mensaje, 
        'exito': exito, 
        'municipio_codigo': municipio_codigo,
        'modulo': 'Tributario', 
        'descripcion': 'Declaración de Volumen de Ventas'
    })'''
    
    with open('vista_declaracion_volumen_corregida_completa.py', 'w', encoding='utf-8') as f:
        f.write(vista_corregida)
    
    print("✅ Vista corregida completa creada: vista_declaracion_volumen_corregida_completa.py")

def main():
    """Función principal"""
    print("🔧 FIX PARA ERROR UnboundLocalError: tarifas_ics")
    print("=" * 60)
    
    # Aplicar corrección
    fix_tarifas_ics_error()
    
    # Crear vista de referencia
    crear_vista_corregida_completa()
    
    print("\n" + "=" * 60)
    print("✅ CORRECCIÓN COMPLETADA")
    
    print("\n📋 Cambios realizados:")
    print("1. Inicialización de variables al inicio de la función")
    print("2. Inicialización de tarifas_ics antes del try")
    print("3. Inicialización de tarifas_ics en el except")
    print("4. Backup del archivo original creado")
    
    print("\n🚀 Pasos siguientes:")
    print("1. Reiniciar servidor Django")
    print("2. Probar la URL: http://127.0.0.1:8080/tributario/declaracion-volumen/")
    print("3. El error UnboundLocalError debería estar resuelto")

if __name__ == "__main__":
    main()
