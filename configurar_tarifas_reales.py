#!/usr/bin/env python
"""
Configurador manual para ingresar las tarifas reales de tarifasimptoics
"""

def configurar_tarifas_manualmente():
    """
    Permite ingresar manualmente las tarifas reales
    """
    print("🔧 CONFIGURADOR MANUAL DE TARIFAS ICS")
    print("=" * 40)
    print("Ingrese las tarifas reales de la tabla 'tarifasimptoics'")
    print("Formato: rango1, rango2, valor")
    print("Ejemplo: 0, 1000000, 2.5")
    print("Escriba 'fin' para terminar")
    print()
    
    tarifas = []
    
    while True:
        try:
            entrada = input(f"Tarifa {len(tarifas)+1}: ").strip()
            
            if entrada.lower() == 'fin':
                break
                
            if not entrada:
                continue
                
            # Parsear entrada
            partes = [p.strip() for p in entrada.split(',')]
            if len(partes) != 3:
                print("❌ Formato incorrecto. Use: rango1, rango2, valor")
                continue
                
            rango1 = float(partes[0])
            rango2 = float(partes[1]) 
            valor = float(partes[2])
            
            tarifa = {
                'rango1': rango1,
                'rango2': rango2,
                'valor': valor,
                'descripcion': f"Rango ${rango1:,.0f} - ${rango2:,.0f}"
            }
            
            tarifas.append(tarifa)
            print(f"✅ Agregada: ${rango1:,.0f} - ${rango2:,.0f} = {valor}‰")
            
        except ValueError:
            print("❌ Error: Ingrese números válidos")
        except KeyboardInterrupt:
            break
    
    if not tarifas:
        print("⚠️ No se ingresaron tarifas")
        return None
        
    print(f"\n📊 TOTAL TARIFAS: {len(tarifas)}")
    return tarifas

def actualizar_archivos_con_tarifas(tarifas):
    """
    Actualiza los archivos con las tarifas reales
    """
    import json
    
    # Guardar JSON
    with open('tarifas_reales.json', 'w') as f:
        json.dump(tarifas, f, indent=2)
    print("✅ Guardado: tarifas_reales.json")
    
    # Actualizar JavaScript calculadora
    try:
        with open('declaracion_volumen_interactivo.js', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Crear backup
        with open('declaracion_volumen_interactivo.js.backup', 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        # Reemplazar tarifas por defecto
        tarifas_js = json.dumps(tarifas, indent=12)
        
        import re
        patron = r'this\.tarifas = \[.*?\];'
        reemplazo = f'this.tarifas = {tarifas_js};'
        
        contenido_nuevo = re.sub(patron, reemplazo, contenido, flags=re.DOTALL)
        
        with open('declaracion_volumen_interactivo.js', 'w', encoding='utf-8') as f:
            f.write(contenido_nuevo)
        
        print("✅ Actualizado: declaracion_volumen_interactivo.js")
        
    except Exception as e:
        print(f"❌ Error actualizando JS: {e}")
    
    # Actualizar HTML test
    try:
        with open('test_calculo_automatico.html', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Generar HTML de tarifas
        html_tarifas1 = ""
        html_tarifas2 = ""
        
        mitad = len(tarifas) // 2
        
        for i, tarifa in enumerate(tarifas):
            linea = f'<li>${tarifa["rango1"]:,.0f} - ${tarifa["rango2"]:,.0f}: {tarifa["valor"]}‰</li>'
            if i < mitad:
                html_tarifas1 += linea + "\n                            "
            else:
                html_tarifas2 += linea + "\n                            "
        
        # Reemplazar sección de tarifas
        patron1 = r'<li>\$0 - \$1,000,000: 2\.5‰</li>.*?<li>\$5,000,000 - \$10,000,000: 6\.0‰</li>'
        patron2 = r'<li>\$10,000,000 - \$50,000,000: 8\.0‰</li>.*?<li>\$50,000,000\+: 10\.0‰</li>'
        
        contenido = re.sub(patron1, html_tarifas1.strip(), contenido, flags=re.DOTALL)
        contenido = re.sub(patron2, html_tarifas2.strip(), contenido, flags=re.DOTALL)
        
        with open('test_calculo_automatico.html', 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print("✅ Actualizado: test_calculo_automatico.html")
        
    except Exception as e:
        print(f"❌ Error actualizando HTML: {e}")

if __name__ == "__main__":
    print("Por favor ingrese las tarifas reales de su tabla 'tarifasimptoics':")
    print("Consulte: SELECT rango1, rango2, valor FROM tarifasimptoics WHERE categoria=1 ORDER BY rango1;")
    print()
    
    tarifas = configurar_tarifas_manualmente()
    
    if tarifas:
        print("\n🔄 Actualizando archivos...")
        actualizar_archivos_con_tarifas(tarifas)
        
        print("\n🎉 CONFIGURACIÓN COMPLETADA")
        print("   ✅ Tarifas reales configuradas")
        print("   ✅ Calculadora actualizada") 
        print("   ✅ Test actualizado")
        print("   🔄 Reinicie el servidor de test")
    else:
        print("\n❌ Configuración cancelada")
