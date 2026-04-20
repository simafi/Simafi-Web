#!/usr/bin/env python3
"""
Implementación completa del combobox de años para declaracion_volumen
usando datos de la tabla anos
"""

import os
import shutil

def crear_modelo_anos():
    """Crear modelo Anos si no existe"""
    modelo_anos = '''
class Anos(models.Model):
    """
    Modelo para la tabla anos.
    Estructura exacta según la tabla de base de datos.
    """
    id = models.AutoField(primary_key=True)
    ano = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    
    class Meta:
        db_table = 'anos'
        verbose_name = 'Año'
        verbose_name_plural = 'Años'
    
    def __str__(self):
        return str(self.ano)
'''
    
    with open('modelo_anos.py', 'w', encoding='utf-8') as f:
        f.write(modelo_anos)
    
    print("✅ Modelo Anos creado en modelo_anos.py")

def crear_vista_completa():
    """Crear vista completa para declaracion_volumen con soporte para años"""
    vista_completa = '''
def declaracion_volumen(request):
    """Vista para el formulario de declaración de volumen de ventas"""
    from .models import DeclaracionVolumen, Negocio, TarifasICS, Anos
    from .forms import DeclaracionVolumenForm
    from django.shortcuts import render
    from django.http import JsonResponse
    from decimal import Decimal
    
    # Obtener años disponibles de la tabla anos
    try:
        anos_disponibles = Anos.objects.all().order_by('-ano')
    except Exception as e:
        print(f"Error obteniendo años: {e}")
        anos_disponibles = []
    
    # Obtener parámetros de la URL
    rtm = request.GET.get('rtm', '')
    expe = request.GET.get('expe', '')
    
    # Buscar negocio si se proporcionan RTM y EXPE
    negocio = None
    if rtm and expe:
        try:
            negocio = Negocio.objects.get(rtm=rtm, expe=expe)
        except Negocio.DoesNotExist:
            negocio = None
    
    # Buscar declaración existente
    declaracion = None
    if rtm and expe:
        try:
            declaracion = DeclaracionVolumen.objects.get(rtm=rtm, expe=expe)
        except DeclaracionVolumen.DoesNotExist:
            declaracion = None
    
    if request.method == 'POST':
        form = DeclaracionVolumenForm(request.POST, instance=declaracion)
        if form.is_valid():
            instance = form.save(commit=False)
            
            # Asignar RTM y EXPE si están disponibles
            if rtm:
                instance.rtm = rtm
            if expe:
                instance.expe = expe
            
            # Calcular impuesto automáticamente
            total_ventas = (
                (instance.ventai or 0) +
                (instance.ventac or 0) + 
                (instance.ventas or 0) +
                (instance.ventap or 0)
            )
            
            # Aquí iría el cálculo del impuesto ICS
            # instance.impuesto_calculado = calcular_impuesto_ics(total_ventas)
            
            instance.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Declaración guardada exitosamente',
                'impuesto': float(instance.impuesto_calculado or 0)
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    else:
        form = DeclaracionVolumenForm(instance=declaracion)
    
    # Context con todos los datos necesarios
    context = {
        'form': form,
        'negocio': negocio,
        'rtm': rtm,
        'expe': expe,
        'declaracion': declaracion,
        'anos_disponibles': anos_disponibles,  # ← CLAVE: Pasar años al template
    }
    
    return render(request, 'declaracion_volumen.html', context)
'''
    
    with open('vista_declaracion_volumen_completa.py', 'w', encoding='utf-8') as f:
        f.write(vista_completa)
    
    print("✅ Vista completa creada en vista_declaracion_volumen_completa.py")

def crear_formulario_con_anos():
    """Crear formulario que carga años dinámicamente"""
    formulario_anos = '''
from django import forms
from .models import DeclaracionVolumen, Anos

class DeclaracionVolumenForm(forms.ModelForm):
    """Formulario para declaración de volumen con años dinámicos"""
    
    class Meta:
        model = DeclaracionVolumen
        fields = '__all__'
        widgets = {
            'ano': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_ano'
            }),
            'mes': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_mes'
            }),
            'ventai': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'id': 'id_ventai'
            }),
            'ventac': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '0',
                'id': 'id_ventac'
            }),
            'ventas': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0', 
                'id': 'id_ventas'
            }),
            'ventap': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'id': 'id_ventap'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Cargar años dinámicamente desde la tabla Anos
        try:
            anos_choices = [('', 'Seleccione un año')] + [
                (str(int(ano.ano)), str(int(ano.ano))) 
                for ano in Anos.objects.all().order_by('-ano')
            ]
            self.fields['ano'].widget.choices = anos_choices
        except Exception as e:
            print(f"Error cargando años: {e}")
            # Fallback con años estáticos
            current_year = 2024
            anos_choices = [('', 'Seleccione un año')] + [
                (str(year), str(year)) 
                for year in range(current_year, current_year - 10, -1)
            ]
            self.fields['ano'].widget.choices = anos_choices
        
        # Configurar meses
        meses_choices = [
            ('', 'Seleccione mes'),
            ('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'),
            ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'),
            ('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'),
            ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')
        ]
        self.fields['mes'].widget.choices = meses_choices
'''
    
    with open('formulario_declaracion_volumen_anos.py', 'w', encoding='utf-8') as f:
        f.write(formulario_anos)
    
    print("✅ Formulario con años creado en formulario_declaracion_volumen_anos.py")

def crear_template_fragment():
    """Crear fragmento de template para el combobox de años"""
    template_fragment = '''
<!-- Sección de Período de Declaración -->
<div class="form-section">
    <h4 class="section-title">
        <i class="fas fa-calendar"></i> Período de Declaración
    </h4>
    <div class="form-grid">
        <!-- Campo Año -->
        <div class="form-group form-group-ano">
            <label for="id_ano" class="required">
                <i class="fas fa-calendar"></i> Año
            </label>
            <select id="id_ano" name="ano" class="form-control" required>
                <option value="">Seleccione año</option>
                {% for ano in anos_disponibles %}
                    <option value="{{ ano.ano }}" 
                            {% if form.ano.value == ano.ano|stringformat:"s" %}selected{% endif %}>
                        {{ ano.ano }}
                    </option>
                {% endfor %}
            </select>
            <small class="form-text text-muted">
                Seleccione el año de la declaración
            </small>
        </div>
        
        <!-- Campo Mes -->
        <div class="form-group form-group-mes">
            <label for="id_mes" class="required">
                <i class="fas fa-calendar-alt"></i> Mes
            </label>
            <select id="id_mes" name="mes" class="form-control" required>
                <option value="">Seleccione mes</option>
                <option value="1" {% if form.mes.value == "1" %}selected{% endif %}>Enero</option>
                <option value="2" {% if form.mes.value == "2" %}selected{% endif %}>Febrero</option>
                <option value="3" {% if form.mes.value == "3" %}selected{% endif %}>Marzo</option>
                <option value="4" {% if form.mes.value == "4" %}selected{% endif %}>Abril</option>
                <option value="5" {% if form.mes.value == "5" %}selected{% endif %}>Mayo</option>
                <option value="6" {% if form.mes.value == "6" %}selected{% endif %}>Junio</option>
                <option value="7" {% if form.mes.value == "7" %}selected{% endif %}>Julio</option>
                <option value="8" {% if form.mes.value == "8" %}selected{% endif %}>Agosto</option>
                <option value="9" {% if form.mes.value == "9" %}selected{% endif %}>Septiembre</option>
                <option value="10" {% if form.mes.value == "10" %}selected{% endif %}>Octubre</option>
                <option value="11" {% if form.mes.value == "11" %}selected{% endif %}>Noviembre</option>
                <option value="12" {% if form.mes.value == "12" %}selected{% endif %}>Diciembre</option>
            </select>
            <small class="form-text text-muted">
                Seleccione el mes de la declaración
            </small>
        </div>
    </div>
</div>

<!-- CSS para el formulario -->
<style>
.form-section {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
}

.section-title {
    color: #495057;
    font-size: 1.1rem;
    margin-bottom: 15px;
    padding-bottom: 8px;
    border-bottom: 2px solid #007bff;
}

.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.form-group label.required::after {
    content: " *";
    color: #dc3545;
}

.form-control {
    border: 1px solid #ced4da;
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 14px;
}

.form-control:focus {
    border-color: #007bff;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

@media (max-width: 768px) {
    .form-grid {
        grid-template-columns: 1fr;
    }
}
</style>
'''
    
    with open('template_anos_completo.html', 'w', encoding='utf-8') as f:
        f.write(template_fragment)
    
    print("✅ Template completo creado en template_anos_completo.html")

def crear_script_poblacion():
    """Crear script para poblar la tabla anos"""
    script_poblacion = '''#!/usr/bin/env python3
"""
Script para poblar la tabla anos con datos de ejemplo
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

def poblar_tabla_anos():
    """Poblar tabla anos con años relevantes"""
    
    # Crear años desde 2015 hasta 2026
    anos_crear = list(range(2015, 2027))
    
    print(f"Poblando tabla anos con años: {anos_crear[0]} - {anos_crear[-1]}")
    
    creados = 0
    existentes = 0
    
    for ano in anos_crear:
        try:
            ano_obj, created = Anos.objects.get_or_create(ano=ano)
            if created:
                print(f"✅ Año {ano} creado")
                creados += 1
            else:
                print(f"ℹ️  Año {ano} ya existe")
                existentes += 1
        except Exception as e:
            print(f"❌ Error creando año {ano}: {e}")
    
    print(f"\\n📊 Resumen:")
    print(f"   - Años creados: {creados}")
    print(f"   - Años existentes: {existentes}")
    print(f"   - Total en BD: {Anos.objects.count()}")
    
    # Mostrar todos los años ordenados
    print("\\n📅 Años disponibles (más recientes primero):")
    anos_existentes = Anos.objects.all().order_by('-ano')
    for ano in anos_existentes:
        print(f"   - {int(ano.ano)}")

if __name__ == "__main__":
    poblar_tabla_anos()
'''
    
    with open('poblar_tabla_anos.py', 'w', encoding='utf-8') as f:
        f.write(script_poblacion)
    
    print("✅ Script de población creado en poblar_tabla_anos.py")

def crear_test_anos():
    """Crear test para verificar funcionamiento"""
    test_anos = '''#!/usr/bin/env python3
"""
Test para verificar que el combobox de años funciona correctamente
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
    from tributario_app.forms import DeclaracionVolumenForm
    print("✅ Django configurado correctamente")
except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    sys.exit(1)

def test_modelo_anos():
    """Test del modelo Anos"""
    print("\\n=== TEST MODELO ANOS ===")
    
    try:
        # Contar años
        total = Anos.objects.count()
        print(f"Total años en BD: {total}")
        
        if total > 0:
            # Obtener primer y último año
            primer_ano = Anos.objects.order_by('ano').first()
            ultimo_ano = Anos.objects.order_by('-ano').first()
            
            print(f"Rango de años: {int(primer_ano.ano)} - {int(ultimo_ano.ano)}")
            
            # Mostrar algunos años
            anos_sample = Anos.objects.all().order_by('-ano')[:5]
            print("Últimos 5 años:")
            for ano in anos_sample:
                print(f"  - {int(ano.ano)}")
        else:
            print("⚠️  No hay años en la base de datos")
            
        return total > 0
        
    except Exception as e:
        print(f"❌ Error en test modelo: {e}")
        return False

def test_formulario():
    """Test del formulario con años"""
    print("\\n=== TEST FORMULARIO ===")
    
    try:
        form = DeclaracionVolumenForm()
        
        # Verificar campo año
        if 'ano' in form.fields:
            print("✅ Campo 'ano' encontrado")
            
            # Verificar opciones
            ano_field = form.fields['ano']
            if hasattr(ano_field.widget, 'choices'):
                choices = list(ano_field.widget.choices)
                print(f"Opciones en combobox: {len(choices)}")
                
                # Mostrar primeras opciones
                print("Primeras opciones:")
                for i, (value, label) in enumerate(choices[:6]):
                    print(f"  {i+1}. Valor: '{value}', Texto: '{label}'")
                
                return len(choices) > 1  # Al menos opción vacía + años
            else:
                print("❌ Campo año no tiene opciones")
                return False
        else:
            print("❌ Campo 'ano' no encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Error en test formulario: {e}")
        return False

def test_integracion():
    """Test de integración completo"""
    print("\\n=== TEST INTEGRACIÓN ===")
    
    modelo_ok = test_modelo_anos()
    formulario_ok = test_formulario()
    
    if modelo_ok and formulario_ok:
        print("\\n✅ TODOS LOS TESTS PASARON")
        print("El combobox de años debería funcionar correctamente")
        return True
    else:
        print("\\n❌ ALGUNOS TESTS FALLARON")
        if not modelo_ok:
            print("- Problema con modelo/datos de años")
        if not formulario_ok:
            print("- Problema con formulario")
        return False

if __name__ == "__main__":
    print("🧪 TEST COMBOBOX DE AÑOS - DECLARACIÓN VOLUMEN")
    print("=" * 50)
    
    resultado = test_integracion()
    
    if not resultado:
        print("\\n💡 Sugerencias:")
        print("1. Ejecutar: python poblar_tabla_anos.py")
        print("2. Verificar configuración de Django")
        print("3. Revisar imports en formulario")
'''
    
    with open('test_anos_declaracion_volumen.py', 'w', encoding='utf-8') as f:
        f.write(test_anos)
    
    print("✅ Test creado en test_anos_declaracion_volumen.py")

def main():
    """Función principal"""
    print("🔧 IMPLEMENTACIÓN COMPLETA - COMBOBOX AÑOS DECLARACIÓN VOLUMEN")
    print("=" * 70)
    
    # Crear todos los archivos necesarios
    print("\\n1. Creando modelo...")
    crear_modelo_anos()
    
    print("\\n2. Creando vista...")
    crear_vista_completa()
    
    print("\\n3. Creando formulario...")
    crear_formulario_con_anos()
    
    print("\\n4. Creando template...")
    crear_template_fragment()
    
    print("\\n5. Creando script de población...")
    crear_script_poblacion()
    
    print("\\n6. Creando tests...")
    crear_test_anos()
    
    print("\\n" + "=" * 70)
    print("✅ IMPLEMENTACIÓN COMPLETADA")
    
    print("\\n📁 Archivos generados:")
    print("- modelo_anos.py (modelo Django)")
    print("- vista_declaracion_volumen_completa.py (vista)")
    print("- formulario_declaracion_volumen_anos.py (formulario)")
    print("- template_anos_completo.html (template)")
    print("- poblar_tabla_anos.py (población de datos)")
    print("- test_anos_declaracion_volumen.py (tests)")
    
    print("\\n🚀 Pasos siguientes:")
    print("1. Ejecutar: python poblar_tabla_anos.py")
    print("2. Integrar el código en tu aplicación Django")
    print("3. Ejecutar: python test_anos_declaracion_volumen.py")
    print("4. Reiniciar servidor Django")

if __name__ == "__main__":
    main()
