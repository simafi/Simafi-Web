#!/usr/bin/env python
"""
Script de testeo para encontrar dónde el campo tasa está recibiendo
valores incorrectos (valor_tasa o saldoact) en lugar de 0.
"""
import os
import sys
import re

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def buscar_asignaciones_tasa():
    """Busca todas las asignaciones al campo tasa en el código"""
    print("="*80)
    print("🔍 BUSCANDO ASIGNACIONES AL CAMPO 'tasa'")
    print("="*80)
    
    archivos_analizar = []
    
    # Buscar archivos Python en modules/tributario
    for root, dirs, files in os.walk('modules/tributario'):
        for file in files:
            if file.endswith('.py'):
                archivos_analizar.append(os.path.join(root, file))
    
    problemas_encontrados = []
    
    for archivo in archivos_analizar:
        try:
            with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
                contenido = f.read()
                lineas = contenido.split('\n')
                
                for num_linea, linea in enumerate(lineas, 1):
                    # Buscar asignaciones a tasa
                    # Patrones problemáticos:
                    # - tasa = valor_tasa
                    # - tasa = saldoact
                    # - tasa = valor
                    # - tasa=valor_tasa
                    # - tasa=saldoact
                    # - tasa=valor
                    # - .tasa = algo que no sea 0 o Decimal('0')
                    
                    # Patrón: tasa = variable_que_no_sea_0
                    patrones_problematicos = [
                        r'tasa\s*=\s*valor_tasa',
                        r'tasa\s*=\s*saldoact',
                        r'tasa\s*=\s*valor[^_]',  # valor pero no valor_tasa ni valor_otra_cosa
                        r'tasa\s*=\s*\w+\[',  # tasa = diccionario[key]
                        r'\.tasa\s*=\s*valor_tasa',
                        r'\.tasa\s*=\s*saldoact',
                        r'\.tasa\s*=\s*valor[^_]',
                    ]
                    
                    # Patrón correcto que debemos verificar
                    patron_correcto = r'tasa\s*=\s*Decimal\([\'"]0\.00[\'"]\)|tasa\s*=\s*Decimal\([\'"]0[\'"]\)|tasa\s*=\s*0|tasa\s*=\s*0\.00'
                    
                    # Verificar si hay asignación a tasa
                    if 'tasa' in linea and '=' in linea:
                        # Verificar si es asignación problemática
                        es_problema = False
                        problema_tipo = None
                        
                        for patron in patrones_problematicos:
                            if re.search(patron, linea, re.IGNORECASE):
                                es_problema = True
                                problema_tipo = f"Asignación problemática: {patron}"
                                break
                        
                        # Si no es problema pero tampoco es correcto, revisar más
                        if not es_problema:
                            # Verificar si NO es una asignación correcta
                            if not re.search(patron_correcto, linea, re.IGNORECASE):
                                # Podría ser un problema si no es comentario
                                if not linea.strip().startswith('#') and 'tasa' in linea.lower():
                                    # Verificar si es una asignación (no solo una comparación o uso)
                                    if re.search(r'tasa\s*=', linea, re.IGNORECASE):
                                        # Excluir casos donde tasa está en un string o comentario
                                        if not ('"' in linea and 'tasa' in linea.split('"')[0] if '"' in linea else True):
                                            es_problema = True
                                            problema_tipo = "Asignación a tasa que no es explícitamente 0"
                        
                        if es_problema:
                            problemas_encontrados.append({
                                'archivo': archivo,
                                'linea': num_linea,
                                'codigo': linea.strip(),
                                'tipo': problema_tipo
                            })
        except Exception as e:
            print(f"⚠️ Error leyendo {archivo}: {e}")
    
    # Mostrar resultados
    print(f"\n📊 RESUMEN:")
    print(f"   Archivos analizados: {len(archivos_analizar)}")
    print(f"   Problemas encontrados: {len(problemas_encontrados)}")
    
    if problemas_encontrados:
        print(f"\n❌ PROBLEMAS ENCONTRADOS:")
        print("="*80)
        for problema in problemas_encontrados:
            print(f"\n📁 Archivo: {problema['archivo']}")
            print(f"   Línea: {problema['linea']}")
            print(f"   Tipo: {problema['tipo']}")
            print(f"   Código: {problema['codigo']}")
    else:
        print("\n✅ No se encontraron asignaciones problemáticas a 'tasa'")
    
    return problemas_encontrados

def buscar_transacciones_ics_create():
    """Busca donde se crea TransaccionesIcs y verifica el campo tasa"""
    print("\n" + "="*80)
    print("🔍 BUSCANDO CREACIONES DE TransaccionesIcs")
    print("="*80)
    
    archivos_analizar = []
    for root, dirs, files in os.walk('modules/tributario'):
        for file in files:
            if file.endswith('.py'):
                archivos_analizar.append(os.path.join(root, file))
    
    creaciones_encontradas = []
    
    for archivo in archivos_analizar:
        try:
            with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
                contenido = f.read()
                
                # Buscar TransaccionesIcs(
                if 'TransaccionesIcs(' in contenido:
                    lineas = contenido.split('\n')
                    en_bloque_transaccion = False
                    bloque_inicio = 0
                    bloque_lineas = []
                    nivel_indentacion = 0
                    
                    for num_linea, linea in enumerate(lineas, 1):
                        if 'TransaccionesIcs(' in linea:
                            en_bloque_transaccion = True
                            bloque_inicio = num_linea
                            bloque_lineas = [linea]
                            nivel_indentacion = len(linea) - len(linea.lstrip())
                        elif en_bloque_transaccion:
                            bloque_lineas.append(linea)
                            # Verificar si termina el bloque
                            if linea.strip() and not linea.strip().startswith('#') and ')' in linea:
                                # Verificar si es el cierre del constructor
                                indent_actual = len(linea) - len(linea.lstrip())
                                if indent_actual <= nivel_indentacion and ')' in linea:
                                    # Analizar el bloque
                                    bloque_completo = '\n'.join(bloque_lineas)
                                    
                                    # Buscar asignación a tasa
                                    tasa_encontrada = False
                                    tasa_valor = None
                                    
                                    # Patrones para buscar tasa
                                    patrones_tasa = [
                        r'tasa\s*=\s*(\w+)',
                        r'tasa\s*=\s*([^,\n\)]+)',
                    ]
                                    
                                    for patron in patrones_tasa:
                                        match = re.search(patron, bloque_completo, re.IGNORECASE)
                                        if match:
                                            tasa_encontrada = True
                                            tasa_valor = match.group(1).strip()
                                            break
                                    
                                    # Verificar si tasa está correctamente asignada
                                    es_correcto = False
                                    if tasa_encontrada:
                                        if 'Decimal' in tasa_valor and '0' in tasa_valor:
                                            es_correcto = True
                                        elif tasa_valor == '0' or tasa_valor == '0.00':
                                            es_correcto = True
                                        elif tasa_valor.startswith('Decimal') and '0' in tasa_valor:
                                            es_correcto = True
                                    
                                    creaciones_encontradas.append({
                                        'archivo': archivo,
                                        'linea_inicio': bloque_inicio,
                                        'linea_fin': num_linea,
                                        'bloque': bloque_completo[:500],  # Primeros 500 caracteres
                                        'tasa_encontrada': tasa_encontrada,
                                        'tasa_valor': tasa_valor,
                                        'es_correcto': es_correcto
                                    })
                                    
                                    # Reset
                                    en_bloque_transaccion = False
                                    bloque_lineas = []
        except Exception as e:
            print(f"⚠️ Error analizando {archivo}: {e}")
    
    print(f"\n📊 CREACIONES DE TransaccionesIcs ENCONTRADAS: {len(creaciones_encontradas)}")
    
    problemas = [c for c in creaciones_encontradas if not c['es_correcto']]
    
    if problemas:
        print(f"\n❌ CREACIONES CON PROBLEMAS: {len(problemas)}")
        for creacion in problemas:
            print(f"\n📁 Archivo: {creacion['archivo']}")
            print(f"   Líneas: {creacion['linea_inicio']}-{creacion['linea_fin']}")
            print(f"   Tasa encontrada: {creacion['tasa_encontrada']}")
            print(f"   Valor de tasa: {creacion['tasa_valor']}")
            print(f"   Código:\n{creacion['bloque'][:300]}...")
    else:
        print("\n✅ Todas las creaciones de TransaccionesIcs tienen tasa correctamente asignada a 0")
    
    return problemas

if __name__ == '__main__':
    print("🚀 INICIANDO TESTEO DEL CAMPO 'tasa'")
    print("="*80)
    
    # Buscar asignaciones problemáticas
    problemas_asignaciones = buscar_asignaciones_tasa()
    
    # Buscar creaciones de TransaccionesIcs
    problemas_creaciones = buscar_transacciones_ics_create()
    
    # Resumen final
    print("\n" + "="*80)
    print("📋 RESUMEN FINAL")
    print("="*80)
    print(f"   Asignaciones problemáticas: {len(problemas_asignaciones)}")
    print(f"   Creaciones problemáticas: {len(problemas_creaciones)}")
    
    if problemas_asignaciones or problemas_creaciones:
        print("\n❌ SE ENCONTRARON PROBLEMAS - REVISAR CÓDIGO")
        sys.exit(1)
    else:
        print("\n✅ NO SE ENCONTRARON PROBLEMAS")
        sys.exit(0)

















