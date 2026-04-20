#!/usr/bin/env python3
"""
Script para corregir la implementación del combobox de años en declaracion_volumen
Asegura que los datos de la tabla 'anos' se muestren correctamente
"""

import os
import re

def corregir_vista_declaracion_volumen():
    """Corregir la vista para asegurar que pase anos_disponibles al template"""
    
    # Buscar archivos de vistas
    archivos_vistas = [
        'venv/Scripts/tributario/tributario_app/views.py',
        'venv/Scripts/tributario/modules/tributario/views.py',
        'views_declara_corregido.py'
    ]
    
    for archivo in archivos_vistas:
        if os.path.exists(archivo):
            print(f"📝 Procesando: {archivo}")
            
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                # Buscar la función declaracion_volumen
                if 'def declaracion_volumen(request):' in contenido:
                    print(f"✅ Función declaracion_volumen encontrada en {archivo}")
                    
                    # Verificar si ya importa Anos
                    if 'from .models import' in contenido and 'Anos' not in contenido:
                        # Agregar Anos a los imports
                        contenido = re.sub(
                            r'from \.models import ([^\\n]+)',
                            r'from .models import \1, Anos',
                            contenido
                        )
                        print("✅ Import de Anos agregado")
                    
                    # Verificar si ya obtiene anos_disponibles
                    if 'anos_disponibles' not in contenido:
                        # Buscar donde agregar la obtención de años
                        patron_insercion = r'(def declaracion_volumen\(request\):[^}]+?)(context = {)'
                        
                        if re.search(patron_insercion, contenido, re.DOTALL):
                            # Agregar obtención de años antes del context
                            reemplazo = r'\1    # Obtener años disponibles de la tabla anos\n    anos_disponibles = Anos.objects.all().order_by(\'-ano\')\n    \n    \2'
                            contenido = re.sub(patron_insercion, reemplazo, contenido, flags=re.DOTALL)
                            print("✅ Obtención de anos_disponibles agregada")
                    
                    # Verificar si el context incluye anos_disponibles
                    if "'anos_disponibles':" not in contenido:
                        # Agregar anos_disponibles al context
                        contenido = re.sub(
                            r"(context = {[^}]+?)(})",
                            r"\1        'anos_disponibles': anos_disponibles,\n    \2",
                            contenido,
                            flags=re.DOTALL
                        )
                        print("✅ anos_disponibles agregado al context")
                    
                    # Guardar archivo corregido
                    with open(archivo, 'w', encoding='utf-8') as f:
                        f.write(contenido)
                    
                    print(f"✅ Archivo {archivo} corregido")
                
            except Exception as e:
                print(f"❌ Error procesando {archivo}: {e}")

def crear_script_poblacion_anos():
    """Crear script para poblar la tabla anos con datos de ejemplo"""
    
    script_poblacion = '''#!/usr/bin/env python3
"""
Script para poblar la tabla anos con años de ejemplo
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')

try:
    django.setup()
    from tributario_app.models import Anos
    print("✅ Django configurado correctamente")
except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    sys.exit(1)

def poblar_anos():
    """Poblar tabla anos con años de ejemplo"""
    
    # Años a crear (últimos 10 años + próximos 2)
    ano_actual = 2024
    anos_crear = list(range(ano_actual - 8, ano_actual + 3))  # 2016-2026
    
    print(f"Creando años: {anos_crear}")
    
    for ano in anos_crear:
        try:
            ano_obj, created = Anos.objects.get_or_create(ano=ano)
            if created:
                print(f"✅ Año {ano} creado")
            else:
                print(f"ℹ️  Año {ano} ya existe")
        except Exception as e:
            print(f"❌ Error creando año {ano}: {e}")
    
    # Mostrar resumen
    total_anos = Anos.objects.count()
    print(f"\\n📊 Total años en base de datos: {total_anos}")
    
    anos_existentes = Anos.objects.all().order_by('-ano')
    print("Años disponibles:")
    for ano in anos_existentes:
        print(f"  - {ano.ano}")

if __name__ == "__main__":
    poblar_anos()
'''
    
    with open('poblar_anos.py', 'w', encoding='utf-8') as f:
        f.write(script_poblacion)
    
    print("✅ Script de población creado: poblar_anos.py")

def verificar_template():
    """Verificar que el template use correctamente anos_disponibles"""
    
    template_path = 'venv/Scripts/tributario/tributario_app/templates/declaracion_volumen.html'
    
    if os.path.exists(template_path):
        print(f"📝 Verificando template: {template_path}")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Verificar estructura del combobox de años
            if 'id_ano' in contenido and 'anos_disponibles' in contenido:
                print("✅ Template ya tiene la estructura correcta para años")
                
                # Verificar el loop específico
                if '{% for ano in anos_disponibles %}' in contenido:
                    print("✅ Loop de años encontrado en template")
                else:
                    print("⚠️  Loop de años no encontrado, verificar implementación")
            else:
                print("❌ Template no tiene la estructura correcta para años")
                
        except Exception as e:
            print(f"❌ Error verificando template: {e}")
    else:
        print(f"❌ Template no encontrado: {template_path}")

def generar_template_corregido():
    """Generar fragmento de template corregido para el combobox de años"""
    
    template_fragment = '''
<!-- Combobox de Años - Corregido -->
<div class="form-group form-group-ano">
    <label for="id_ano" class="required">
        <i class="fas fa-calendar"></i> Año
    </label>
    <select id="id_ano" name="ano" class="form-control" required>
        <option value="">Seleccione año</option>
        {% for ano in anos_disponibles %}
            <option value="{{ ano.ano }}" {% if form.ano.value == ano.ano|stringformat:"s" %}selected{% endif %}>
                {{ ano.ano }}
            </option>
        {% endfor %}
    </select>
    <small class="form-text text-muted">
        Seleccione el año de la declaración
    </small>
</div>
'''
    
    with open('template_anos_corregido.html', 'w', encoding='utf-8') as f:
        f.write(template_fragment)
    
    print("✅ Fragmento de template corregido guardado: template_anos_corregido.html")

def main():
    """Función principal"""
    print("🔧 CORRECCIÓN DEL COMBOBOX DE AÑOS - DECLARACIÓN VOLUMEN")
    print("=" * 60)
    
    # 1. Corregir vistas
    print("\\n1. Corrigiendo vistas...")
    corregir_vista_declaracion_volumen()
    
    # 2. Crear script de población
    print("\\n2. Creando script de población...")
    crear_script_poblacion_anos()
    
    # 3. Verificar template
    print("\\n3. Verificando template...")
    verificar_template()
    
    # 4. Generar template corregido
    print("\\n4. Generando fragmento de template...")
    generar_template_corregido()
    
    print("\\n" + "=" * 60)
    print("✅ CORRECCIÓN COMPLETADA")
    print("\\nArchivos generados:")
    print("- poblar_anos.py (para poblar datos)")
    print("- template_anos_corregido.html (fragmento de template)")
    print("\\nPasos siguientes:")
    print("1. Ejecutar: python poblar_anos.py")
    print("2. Verificar que la vista pase 'anos_disponibles' al template")
    print("3. Reiniciar el servidor Django")

if __name__ == "__main__":
    main()
