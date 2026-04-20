#!/usr/bin/env python
"""
Obtiene las tarifas reales de la tabla tarifasimptoics
"""

import os
import sys
import django
import json

# Configurar Django
sys.path.append(r'c:\simafiweb\venv\Scripts\tributario')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')

try:
    django.setup()
    from tributario_app.models import TarifasImptoics
    DJANGO_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Django no disponible: {e}")
    DJANGO_AVAILABLE = False

def obtener_tarifas_desde_django():
    """
    Obtiene tarifas usando Django ORM
    """
    if not DJANGO_AVAILABLE:
        return None
    
    try:
        print("🔍 CONSULTANDO TARIFAS DESDE DJANGO ORM")
        print("=" * 45)
        
        # Consultar tarifas de categoría 1
        tarifas = TarifasImptoics.objects.filter(categoria=1).order_by('rango1')
        
        if not tarifas.exists():
            print("⚠️ No se encontraron tarifas en categoría 1")
            return None
        
        tarifas_list = []
        print("✅ TARIFAS REALES OBTENIDAS:")
        print("-" * 30)
        
        for i, tarifa in enumerate(tarifas, 1):
            tarifa_dict = {
                'rango1': float(tarifa.rango1),
                'rango2': float(tarifa.rango2), 
                'valor': float(tarifa.valor),
                'categoria': tarifa.categoria,
                'descripcion': f"Rango ${float(tarifa.rango1):,.0f} - ${float(tarifa.rango2):,.0f}"
            }
            tarifas_list.append(tarifa_dict)
            
            print(f"Rango {i}: ${tarifa.rango1:,.0f} - ${tarifa.rango2:,.0f} = {tarifa.valor}‰")
        
        return tarifas_list
        
    except Exception as e:
        print(f"❌ Error consultando Django: {e}")
        return None

def crear_tarifas_javascript(tarifas):
    """
    Crea archivo JavaScript con tarifas reales
    """
    if not tarifas:
        return False
    
    js_content = f"""/**
 * Tarifas ICS reales obtenidas de tabla tarifasimptoics
 * Generado automáticamente desde base de datos
 */

const TARIFAS_ICS_REALES = {json.dumps(tarifas, indent=4)};

// Función para obtener tarifas reales
function obtenerTarifasReales() {{
    return TARIFAS_ICS_REALES;
}}

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = {{ TARIFAS_ICS_REALES, obtenerTarifasReales }};
}}
"""
    
    try:
        with open('tarifas_ics_reales.js', 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        print(f"\n✅ JavaScript generado: tarifas_ics_reales.js")
        return True
        
    except Exception as e:
        print(f"❌ Error creando JavaScript: {e}")
        return False

def actualizar_calculadora_con_tarifas_reales(tarifas):
    """
    Actualiza el archivo de calculadora con tarifas reales
    """
    archivo_calculadora = 'declaracion_volumen_interactivo.js'
    
    if not os.path.exists(archivo_calculadora):
        print(f"⚠️ Archivo no encontrado: {archivo_calculadora}")
        return False
    
    try:
        # Leer archivo actual
        with open(archivo_calculadora, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Crear backup
        with open(archivo_calculadora + '.backup_tarifas', 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        # Reemplazar tarifas por defecto con tarifas reales
        tarifas_js = json.dumps(tarifas, indent=16)
        
        # Buscar y reemplazar la sección de tarifas por defecto
        import re
        patron_tarifas = r'this\.tarifas = \[.*?\];'
        nuevo_tarifas = f'this.tarifas = {tarifas_js};'
        
        contenido_actualizado = re.sub(
            patron_tarifas, 
            nuevo_tarifas, 
            contenido, 
            flags=re.DOTALL
        )
        
        # Escribir archivo actualizado
        with open(archivo_calculadora, 'w', encoding='utf-8') as f:
            f.write(contenido_actualizado)
        
        print(f"✅ Calculadora actualizada con tarifas reales")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando calculadora: {e}")
        return False

def actualizar_test_con_tarifas_reales(tarifas):
    """
    Actualiza la página de test con tarifas reales
    """
    archivo_test = 'test_calculo_automatico.html'
    
    if not os.path.exists(archivo_test):
        print(f"⚠️ Archivo test no encontrado: {archivo_test}")
        return False
    
    try:
        # Leer archivo test
        with open(archivo_test, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Crear backup
        with open(archivo_test + '.backup_tarifas', 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        # Generar HTML para mostrar tarifas reales
        tarifas_html = ""
        for i, tarifa in enumerate(tarifas, 1):
            if i <= len(tarifas) // 2:
                tarifas_html += f'<li>${tarifa["rango1"]:,.0f} - ${tarifa["rango2"]:,.0f}: {tarifa["valor"]}‰</li>\n                            '
        
        tarifas_html2 = ""
        for i, tarifa in enumerate(tarifas, 1):
            if i > len(tarifas) // 2:
                tarifas_html2 += f'<li>${tarifa["rango1"]:,.0f} - ${tarifa["rango2"]:,.0f}: {tarifa["valor"]}‰</li>\n                            '
        
        # Reemplazar rangos de ejemplo con rangos reales
        contenido_actualizado = contenido.replace(
            '<li>$0 - $1,000,000: 2.5‰</li>\n                            <li>$1,000,000 - $5,000,000: 4.0‰</li>\n                            <li>$5,000,000 - $10,000,000: 6.0‰</li>',
            tarifas_html.rstrip()
        )
        
        contenido_actualizado = contenido_actualizado.replace(
            '<li>$10,000,000 - $50,000,000: 8.0‰</li>\n                            <li>$50,000,000+: 10.0‰</li>',
            tarifas_html2.rstrip()
        )
        
        # Escribir archivo actualizado
        with open(archivo_test, 'w', encoding='utf-8') as f:
            f.write(contenido_actualizado)
        
        print(f"✅ Test actualizado con tarifas reales")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando test: {e}")
        return False

def main():
    """
    Función principal
    """
    print("🎯 OBTENIENDO TARIFAS REALES DE tarifasimptoics")
    print("=" * 50)
    
    # Intentar obtener tarifas desde Django
    tarifas = obtener_tarifas_desde_django()
    
    if tarifas:
        print(f"\n📊 TOTAL TARIFAS ENCONTRADAS: {len(tarifas)}")
        
        # Guardar en JSON
        with open('tarifas_reales.json', 'w', encoding='utf-8') as f:
            json.dump(tarifas, f, indent=2, ensure_ascii=False)
        print("✅ Tarifas guardadas en: tarifas_reales.json")
        
        # Crear JavaScript
        crear_tarifas_javascript(tarifas)
        
        # Actualizar calculadora
        actualizar_calculadora_con_tarifas_reales(tarifas)
        
        # Actualizar test
        actualizar_test_con_tarifas_reales(tarifas)
        
        print("\n🎉 ACTUALIZACIÓN COMPLETADA")
        print("   ✅ Tarifas reales obtenidas de BD")
        print("   ✅ Calculadora actualizada")
        print("   ✅ Test actualizado")
        print("   🔄 Reinicie el servidor de test")
        
    else:
        print("\n❌ NO SE PUDIERON OBTENER TARIFAS REALES")
        print("   Verifique la conexión a la base de datos")
        print("   Asegúrese que existan registros en tarifasimptoics")

if __name__ == "__main__":
    main()
