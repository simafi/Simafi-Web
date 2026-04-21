from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def simple_redirect(request):
    """Simple redirect view for missing functions"""
    return redirect('tributario:maestro_negocios')

def simple_render(request):
    """Simple render view for missing functions"""
    # Crear un objeto negocio simulado para evitar errores de template
    class NegocioSimulado:
        def __init__(self):
            self.empresa = '0301'
            self.rtm = ''
            self.expe = ''
            self.fecha_ini = None
            self.fecha_can = None
            self.identidad = ''
            self.rtnpersonal = ''
            self.comerciante = ''
            self.rtnnego = ''
            self.nombrenego = ''
            self.actividad = ''
            self.identidadrep = ''
            self.representante = ''
            self.estatus = 'A'
            self.catastral = ''
            self.cx = '0.0000000'
            self.cy = '0.0000000'
            self.direccion = ''
            self.telefono = ''
            self.celular = ''
            self.correo = ''
            self.pagweb = ''
            self.socios = ''
            self.comentario = ''
    
    negocio = NegocioSimulado()
    
    return render(request, 'maestro_negocios.html', {
        'negocio': negocio,
        'empresa': '0301',
        'modulo': 'Tributario',
        'descripcion': 'Gestión de impuestos y tasas municipales'
    })

def declaracion_volumen(request):
    """Vista para declaración de volumen de ventas"""
    print(f"DECLARACION_VOLUMEN EJECUTANDOSE - Metodo: {request.method}")
    print(f"   - URL: {request.path}")
    print(f"   - Query params: {request.GET}")
    
    # Obtener parámetros de la URL
    rtm = request.GET.get('rtm', '')
    expe = request.GET.get('expe', '')
    empresa = request.GET.get('empresa', '')
    ano = request.GET.get('ano', '')
    
    # Si empresa no viene en la URL, usar default temporal (se actualizará del negocio si existe)
    municipio_codigo = "0301"
    if not empresa:
        empresa = municipio_codigo
    
    # MANEJAR PETICIONES POST Y AJAX
    if request.method == 'POST':
        print("="*80)
        print("[DEBUG] PETICION POST RECIBIDA")
        print(f"[DEBUG] Headers: {dict(request.headers)}")
        print(f"[DEBUG] X-Requested-With: {request.headers.get('X-Requested-With')}")
        print("="*80)
        
        # Verificar si es petición AJAX
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        content_type = request.headers.get('Content-Type', '')
        
        if is_ajax:
            print("[DEBUG] Procesando como petición AJAX")
            try:
                if 'application/json' in content_type:
                    # Petición AJAX con JSON
                    data = json.loads(request.body)
                    accion = data.get('accion')
                    form_data = data.get('form_data', {})
                else:
                    # Petición AJAX con form-data
                    accion = request.POST.get('accion')
                    form_data = request.POST
                
                print(f"[DEBUG] Acción AJAX: {accion}")
                if accion == 'guardar':
                    print("[DEBUG] Procesando guardado AJAX...")
                    print(f"[DEBUG] Datos originales: {form_data}")
                    # Limpiar valores con separadores de miles (comas) antes de validar
                    datos_limpiados = form_data.copy()
                    campos_numericos = ['ano', 'ventai', 'ventac', 'ventas', 'valorexcento', 'controlado', 'factor', 'ajuste', 'impuesto', 'multadecla']
                    for campo in campos_numericos:
                        if campo in datos_limpiados:
                            valor = datos_limpiados[campo]
                            if valor and str(valor).strip():  # Solo procesar si no está vacío
                                # Remover comas (separadores de miles) antes de validar
                                valor_limpio = str(valor).replace(',', '').strip()
                                datos_limpiados[campo] = valor_limpio
                            else:
                                # Convertir cadenas vacías a 0 para campos numéricos
                                datos_limpiados[campo] = '0'
                    
                    # SIEMPRE recalcular valor_base para AJAX
                    ventai = float(datos_limpiados.get('ventai', 0) or 0)
                    ventac = float(datos_limpiados.get('ventac', 0) or 0)
                    ventas = float(datos_limpiados.get('ventas', 0) or 0)
                    valorexcento = float(datos_limpiados.get('valorexcento', 0) or 0)
                    controlado = float(datos_limpiados.get('controlado', 0) or 0)
                    valor_base_calculado = ventai + ventac + ventas + valorexcento + controlado
                    datos_limpiados['valor_base'] = valor_base_calculado
                    print(f"[DEBUG] Valor base calculado para AJAX: {valor_base_calculado}")
                    print(f"[DEBUG] Valores individuales: ventai={ventai}, ventac={ventac}, ventas={ventas}, valorexcento={valorexcento}, controlado={controlado}")
                    
                    # Asegurar que impuesto tenga un valor por defecto
                    if 'impuesto' not in datos_limpiados or not datos_limpiados['impuesto']:
                        datos_limpiados['impuesto'] = 0
                    
                    print(f"[DEBUG] Datos finales para formulario: {datos_limpiados}")
                    from tributario_app.forms import DeclaracionVolumenForm
                    form = DeclaracionVolumenForm(datos_limpiados)
                    
                    if form.is_valid():
                        print("[DEBUG] Formulario AJAX válido")
                        
                        # Guardar en la base de datos
                        try:
                            from tributario.models import TasasDecla, DeclaracionVolumen
                            from decimal import Decimal, InvalidOperation
                            from django.utils import timezone
                            
                            # Función helper para convertir valores a Decimal de forma segura
                            def safe_decimal(valor, default=Decimal('0.00')):
                                """Convierte un valor a Decimal de forma segura"""
                                if valor is None:
                                    return default
                                if isinstance(valor, Decimal):
                                    return valor
                                try:
                                    # Convertir a string, remover comas y espacios
                                    valor_str = str(valor).replace(',', '').strip()
                                    if not valor_str or valor_str == '':
                                        return default
                                    return Decimal(valor_str)
                                except (ValueError, InvalidOperation, TypeError) as e:
                                    print(f"[WARNING] Error convirtiendo '{valor}' a Decimal: {e}, usando default {default}")
                                    return default
                            
                            # PRIMERO: Guardar/Actualizar en la tabla declara (DeclaracionVolumen)
                            print("[DEBUG] Guardando en tabla declara (DeclaracionVolumen)...")
                            
                            # Obtener datos del formulario validado
                            idneg = int(datos_limpiados.get('idneg', 0))
                            empresa = datos_limpiados.get('empresa', '0301')
                            rtm = datos_limpiados.get('rtm', '')
                            expe = datos_limpiados.get('expe', '')
                            ano = int(datos_limpiados.get('ano', 2025))
                            tipo = int(datos_limpiados.get('tipo', 1))
                            mes = int(datos_limpiados.get('mes', 10))
                            
                            # VALIDACIÓN: Verificar si existen pagos (operacion = 'P') en el año de la declaración
                            # Vinculación: empresa, rtm, expe y año
                            from tributario.models import TransaccionesIcs
                            pagos_existentes = TransaccionesIcs.objects.filter(
                                empresa=empresa,
                                rtm=rtm,
                                expe=expe,
                                ano=Decimal(ano),  # Convertir a Decimal para comparación correcta
                                operacion='P'  # Operación de Pago
                            ).exists()
                            
                            if pagos_existentes:
                                return JsonResponse({
                                    'exito': False,
                                    'mensaje': f'⚠️ Validación: No se puede guardar la declaración porque existen pagos registrados para el año {ano} (empresa={empresa}, RTM={rtm}, EXPE={expe}). No se permite modificar declaraciones cuando ya hay pagos aplicados.',
                                    'tipo_validacion': True,  # Indicar que es una validación, no un error técnico
                                    'impuesto': 0
                                })
                            
                            # Obtener usuario de la sesión del sistema
                            usuario_sesion = request.session.get('usuario', 'Sistema')
                            print(f"[DEBUG] Usuario de sesión para creación: {usuario_sesion}")
                            
                            # Obtener número de declaración desde anoemprenu
                            from tributario.models import AnoEmpreNu
                            from datetime import datetime as dt
                            ano_int = int(ano) if ano else dt.now().year
                            
                            # Buscar registro en anoemprenu para esta empresa y año
                            try:
                                ano_emprenu = AnoEmpreNu.objects.get(empresa=empresa, ano=ano_int)
                                print(f"[DEBUG] Registro anoemprenu existente: nudecla={ano_emprenu.nudecla}")
                            except AnoEmpreNu.DoesNotExist:
                                # Crear nuevo registro si no existe
                                ano_emprenu = AnoEmpreNu.objects.create(
                                    empresa=empresa,
                                    ano=ano_int,
                                    nudecla=0,
                                    nopermiso=0,
                                    noplanes=0
                                )
                                print(f"[DEBUG] Registro anoemprenu creado para empresa={empresa}, ano={ano_int}")
                            
                            # Buscar declaración existente
                            try:
                                declaracion = DeclaracionVolumen.objects.get(
                                    empresa=empresa,
                                    rtm=rtm,
                                    expe=expe,
                                    ano=ano
                                )
                                # Si la declaración ya existe, usar su nodecla existente
                                nodecla = declaracion.nodecla
                                print(f"[DEBUG] Declaración existente, usando nodecla: {nodecla}")
                                
                                # Actualizar registro existente
                                declaracion.ventai = safe_decimal(datos_limpiados.get('ventai', 0))
                                declaracion.ventac = safe_decimal(datos_limpiados.get('ventac', 0))
                                declaracion.ventas = safe_decimal(datos_limpiados.get('ventas', 0))
                                declaracion.valorexcento = safe_decimal(datos_limpiados.get('valorexcento', 0))
                                declaracion.controlado = safe_decimal(datos_limpiados.get('controlado', 0))
                                # Guardar valor_base en la columna real (MySQL exige NOT NULL sin default)
                                declaracion.valor_base = safe_decimal(valor_base_calculado)
                                # unidad es DecimalField pero puede venir como int, convertir a Decimal sin decimales
                                unidad_val = datos_limpiados.get('unidad', 0)
                                try:
                                    declaracion.unidad = Decimal(str(int(float(safe_decimal(unidad_val)))))
                                except:
                                    declaracion.unidad = Decimal('0')
                                declaracion.factor = safe_decimal(datos_limpiados.get('factor', 0))
                                declaracion.multadecla = safe_decimal(datos_limpiados.get('multadecla', 0))
                                declaracion.impuesto = safe_decimal(datos_limpiados.get('impuesto', 0))
                                declaracion.ajuste = safe_decimal(datos_limpiados.get('ajuste_interanual', 0))
                                declaracion.tipo = tipo
                                declaracion.mes = mes
                                declaracion.nodecla = nodecla  # Mantener el nodecla existente
                                declaracion.fechssys = timezone.now()
                                declaracion.usuario = usuario_sesion
                                declaracion.save()
                                print(f"[DEBUG] Declaración actualizada en tabla declara: {nodecla}")
                            except DeclaracionVolumen.DoesNotExist:
                                # Si es nueva declaración, incrementar el número secuencial en anoemprenu
                                ano_emprenu.nudecla = (ano_emprenu.nudecla or 0) + 1
                                ano_emprenu.save()
                                
                                # Formatear número con ceros a la izquierda (11 dígitos) y año
                                # Ejemplo: 1 → "0000000001-2025"
                                nudecla_formateado = str(int(ano_emprenu.nudecla)).zfill(11)
                                nodecla = f"{nudecla_formateado}-{ano_int}"
                                print(f"[DEBUG] Nueva declaración, número generado: {nodecla} (nudecla={ano_emprenu.nudecla})")
                                
                                # Crear nuevo registro
                                declaracion = DeclaracionVolumen.objects.create(
                                    idneg=idneg,
                                    empresa=empresa,
                                    rtm=rtm,
                                    expe=expe,
                                    ano=ano,
                                    tipo=tipo,
                                    mes=mes,
                                    ventai=safe_decimal(datos_limpiados.get('ventai', 0)),
                                    ventac=safe_decimal(datos_limpiados.get('ventac', 0)),
                                    ventas=safe_decimal(datos_limpiados.get('ventas', 0)),
                                    valorexcento=safe_decimal(datos_limpiados.get('valorexcento', 0)),
                                    controlado=safe_decimal(datos_limpiados.get('controlado', 0)),
                                    valor_base=safe_decimal(valor_base_calculado),
                                    unidad=safe_decimal(datos_limpiados.get('unidad', 0), Decimal('0')),
                                    factor=safe_decimal(datos_limpiados.get('factor', 0)),
                                    multadecla=safe_decimal(datos_limpiados.get('multadecla', 0)),
                                    impuesto=safe_decimal(datos_limpiados.get('impuesto', 0)),
                                    ajuste=safe_decimal(datos_limpiados.get('ajuste_interanual', 0)),
                                    nodecla=nodecla,
                                    fechssys=timezone.now(),
                                    usuario=usuario_sesion
                                )
                                print(f"[DEBUG] Declaración creada en tabla declara: {nodecla}")
                            
                            # SEGUNDO: Guardar en la tabla TasasDecla
                            print(f"[DEBUG] Guardando en tabla TasasDecla...")
                            
                            impuesto = float(datos_limpiados.get('impuesto', 0))
                            multa = float(datos_limpiados.get('multadecla', 0))
                            
                            print(f"[DEBUG] Guardando tasas - Empresa: {empresa}, RTM: {rtm}, EXPE: {expe}, Año: {ano}")
                            print(f"[DEBUG] Número de declaración: {nodecla}")
                            print(f"[DEBUG] Impuesto: {impuesto}, Multa: {multa}")
                            
                            # Guardar C0001 - Impuesto
                            if impuesto > 0:
                                # Convertir ano a Decimal para la consulta
                                ano_decimal_c0001 = Decimal(str(ano)) if ano else Decimal('0')
                                # Buscar registro existente sin nodecla para evitar conflictos
                                try:
                                    tasa_impuesto = TasasDecla.objects.get(
                                        empresa=empresa,
                                        rtm=rtm,
                                        expe=expe,
                                        ano=ano_decimal_c0001,
                                        rubro='C0001'
                                    )
                                    # Actualizar registro existente
                                    tasa_impuesto.valor = safe_decimal(impuesto)
                                    tasa_impuesto.nodecla = nodecla
                                    tasa_impuesto.idneg = idneg  # Actualizar idneg también
                                    tasa_impuesto.save()
                                    print(f"[DEBUG] Tasa C0001 actualizada: {impuesto}, idneg={idneg}")
                                except TasasDecla.DoesNotExist:
                                    # Crear nuevo registro
                                    tasa_impuesto = TasasDecla.objects.create(
                                        empresa=empresa,
                                        idneg=idneg,  # Guardar id del negocio
                                        rtm=rtm,
                                        expe=expe,
                                        ano=ano_decimal_c0001,
                                        rubro='C0001',
                                        nodecla=nodecla,
                                        cod_tarifa='C001',
                                        frecuencia='M',  # Mensual
                                        valor=safe_decimal(impuesto),
                                        cuenta='11.7.1.01.09.00',
                                        cuentarez='11.7.1.98.01.00',
                                        tipota='F'  # Fijo
                                    )
                                    print(f"[DEBUG] Tasa C0001 creada: {impuesto}, idneg={idneg}")
                            
                            # Guardar C0003 - Multa Declaración Tardía (SIEMPRE actualizar, incluso si es 0)
                            # Convertir ano a Decimal para la consulta
                            ano_decimal_c0003 = Decimal(str(ano)) if ano else Decimal('0')
                            
                            # Obtener cuenta y cuentarez desde TarifasICS para C0003
                            cuenta_c0003 = '11.7.1.01.09.00'  # Valor por defecto
                            cuentarez_c0003 = '11.7.1.98.01.00'  # Valor por defecto
                            
                            try:
                                from tributario.models import TarifasICS
                                tarifa_c0003 = TarifasICS.objects.filter(
                                    empresa=empresa,
                                    rtm=rtm,
                                    expe=expe,
                                    rubro='C0003'
                                ).first()
                                
                                if tarifa_c0003:
                                    if tarifa_c0003.cuenta:
                                        cuenta_c0003 = tarifa_c0003.cuenta.strip()
                                    if tarifa_c0003.cuentarez:
                                        cuentarez_c0003 = tarifa_c0003.cuentarez.strip()
                                    print(f"[DEBUG] C0003 - Cuenta obtenida desde TarifasICS: cuenta={cuenta_c0003}, cuentarez={cuentarez_c0003}")
                                else:
                                    print(f"[DEBUG] C0003 - No se encontró en TarifasICS, usando valores por defecto")
                            except Exception as e:
                                print(f"[DEBUG] C0003 - Error obteniendo cuenta desde TarifasICS: {e}, usando valores por defecto")
                            
                            # Buscar registro existente sin nodecla para evitar conflictos
                            try:
                                tasa_multa = TasasDecla.objects.get(
                                    empresa=empresa,
                                    rtm=rtm,
                                    expe=expe,
                                    ano=ano_decimal_c0003,
                                    rubro='C0003'
                                )
                                # Actualizar registro existente (incluso si multa es 0)
                                tasa_multa.valor = safe_decimal(multa)
                                tasa_multa.nodecla = nodecla
                                tasa_multa.idneg = idneg  # Actualizar idneg también
                                # Actualizar cuenta y cuentarez desde TarifasICS
                                tasa_multa.cuenta = cuenta_c0003
                                tasa_multa.cuentarez = cuentarez_c0003
                                tasa_multa.save()
                                print(f"[DEBUG] Tasa C0003 actualizada: {multa}, idneg={idneg}, cuenta={cuenta_c0003}")
                            except TasasDecla.DoesNotExist:
                                # Crear nuevo registro solo si multa > 0
                                if multa > 0:
                                    tasa_multa = TasasDecla.objects.create(
                                        empresa=empresa,
                                        idneg=idneg,  # Guardar id del negocio
                                        rtm=rtm,
                                        expe=expe,
                                        ano=ano_decimal_c0003,
                                        rubro='C0003',
                                        nodecla=nodecla,
                                        cod_tarifa='C003',
                                        frecuencia='A',  # Anual
                                        valor=safe_decimal(multa),
                                        cuenta=cuenta_c0003,  # Cuenta desde TarifasICS
                                        cuentarez=cuentarez_c0003,  # Cuenta rezago desde TarifasICS
                                        tipota='F'  # Fijo
                                    )
                                    print(f"[DEBUG] Tasa C0003 creada: {multa}, idneg={idneg}, cuenta={cuenta_c0003}")
                                else:
                                    print(f"[DEBUG] Tasa C0003 no creada (valor 0 y no existe registro previo)")
                            
                            # Obtener las tasas actualizadas para refrescar el grid
                            tasas_actualizadas = []
                            try:
                                # Convertir ano a Decimal para la consulta
                                ano_filtro = Decimal(str(ano)) if ano else None
                                tasas = TasasDecla.objects.filter(
                                    empresa=empresa,
                                    rtm=rtm,
                                    expe=expe
                                )
                                if ano_filtro:
                                    tasas = tasas.filter(ano=ano_filtro)
                                tasas = tasas.values('rubro', 'valor', 'nodecla', 'frecuencia', 'cuenta', 'cuentarez', 'tipota')
                                
                                for tasa in tasas:
                                    tasas_actualizadas.append({
                                        'rubro': tasa['rubro'],
                                        'valor': float(tasa['valor']),
                                        'nodecla': tasa['nodecla'],
                                        'frecuencia': tasa['frecuencia'],
                                        'cuenta': tasa['cuenta'],
                                        'cuentarez': tasa['cuentarez'],
                                        'tipota': tasa['tipota']
                                    })
                                
                                print(f"[DEBUG] Tasas actualizadas obtenidas: {len(tasas_actualizadas)} registros")
                                
                            except Exception as e:
                                print(f"[DEBUG] Error obteniendo tasas actualizadas: {e}")
                                tasas_actualizadas = []
                            
                            # ========================================================================
                            # 🔄 FUNCIONALIDAD CRÍTICA: Crear y actualizar tasas según plan de arbitrios y tarifas
                            # Este proceso se ejecuta AUTOMÁTICAMENTE al guardar la declaración
                            # IMPORTANTE: Este proceso DEBE ejecutarse SIEMPRE después de guardar C0001 y C0003
                            # ========================================================================
                            # VERIFICACIÓN: Este bloque SIEMPRE debe ejecutarse, no puede ser omitido
                            print("\n")
                            print("="*100)
                            print("="*100)
                            print("[CREAR Y CALCULAR TASAS] ⚡⚡⚡ INICIANDO PROCESO COMPLETO DE TASAS ⚡⚡⚡")
                            print("[CREAR Y CALCULAR TASAS] ⚠️ ESTE PROCESO DEBE EJECUTARSE SIEMPRE")
                            print("="*100)
                            print(f"[CREAR Y CALCULAR TASAS] Parámetros recibidos:")
                            print(f"   - Empresa: {empresa}")
                            print(f"   - RTM: {rtm}")
                            print(f"   - EXPE: {expe}")
                            print(f"   - IDNeg: {idneg}")
                            print(f"   - Año: {ano}")
                            print(f"   - Nodecla: {nodecla}")
                            print("="*100)
                            print()
                            tasas_calculadas = []
                            tasas_error_calc = []
                            tasas_creadas = []
                            
                            # IMPORTANTE: Este try asegura que el proceso continúe incluso si hay errores
                            # PERO DEBE EJECUTARSE SIEMPRE - No debe haber ninguna condición que lo omita
                            print(f"[CREAR Y CALCULAR TASAS] 🚀 EJECUTANDO BLOQUE TRY - PROCESO DE CREAR TASAS")
                            try:
                                # Importar modelos necesarios - ESTOS DEBEN ESTAR DISPONIBLES
                                from tributario.models import TasasDecla, Tarifas, PlanArbitrio, Rubro
                                from tributario.models import TarifasICS
                                from decimal import Decimal
                                
                                print(f"[CREAR Y CALCULAR TASAS] ✅ Modelos importados correctamente")
                                print(f"[CREAR Y CALCULAR TASAS] ✅ TarifasICS disponible: {TarifasICS}")
                                print(f"[CREAR Y CALCULAR TASAS] ✅ TasasDecla disponible: {TasasDecla}")
                                
                                # Crear un diccionario con los parámetros necesarios
                                tasa_params = {
                                    'empresa': empresa,
                                    'rtm': rtm,
                                    'expe': expe,
                                    'ano': ano,
                                }
                                
                                print(f"[CREAR Y CALCULAR TASAS] Parámetros validados: {tasa_params}")
                                
                                # Calcular valorbase
                                valorbase = (safe_decimal(datos_limpiados.get('ventai', 0)) + 
                                            safe_decimal(datos_limpiados.get('ventac', 0)) +
                                            safe_decimal(datos_limpiados.get('ventas', 0)) +
                                            safe_decimal(datos_limpiados.get('valorexcento', 0)) +
                                            safe_decimal(datos_limpiados.get('controlado', 0)))
                                
                                print(f"[CREAR Y CALCULAR TASAS] Valorbase calculado: {valorbase}")
                                
                                # ============================================================
                                # PASO 1: Obtener rubros registrados en tarifasics para este negocio
                                # ============================================================
                                print(f"\n[CREAR Y CALCULAR TASAS] {'='*90}")
                                print(f"[CREAR Y CALCULAR TASAS] PASO 1: Buscar TarifasICS")
                                print(f"[CREAR Y CALCULAR TASAS] {'='*90}")
                                rubros_registrados = []
                                try:
                                    print(f"[CREAR Y CALCULAR TASAS] 🔍 Buscando tarifasics con filtros:")
                                    print(f"   - empresa='{empresa}'")
                                    print(f"   - rtm='{rtm}'")
                                    print(f"   - expe='{expe}'")
                                    print(f"   - idneg={idneg} (no se usa en filtro)")
                                    
                                    # IMPORTANTE: Buscar TODAS las tarifasics sin filtrar por idneg
                                    # Esto asegura que se carguen todas las tasas configuradas
                                    tarifas_ics = TarifasICS.objects.filter(
                                        empresa=empresa,
                                        rtm=rtm,
                                        expe=expe
                                    )
                                    print(f"[CREAR Y CALCULAR TASAS] 📊 TarifasICS encontradas: {tarifas_ics.count()}")
                                    
                                    # Si no se encontraron, intentar sin filtro de empresa (por si acaso)
                                    if not tarifas_ics.exists():
                                        print(f"[CREAR Y CALCULAR TASAS] ⚠️ No se encontraron tarifasics con empresa, intentando solo con rtm y expe")
                                        tarifas_ics = TarifasICS.objects.filter(
                                            rtm=rtm,
                                            expe=expe
                                        )
                                        print(f"[CREAR Y CALCULAR TASAS] 📊 TarifasICS encontradas (sin empresa): {tarifas_ics.count()}")
                                    
                                    if not tarifas_ics.exists():
                                        print(f"[CREAR Y CALCULAR TASAS] ⚠️⚠️⚠️ ADVERTENCIA: No se encontraron tarifasics para empresa={empresa}, rtm={rtm}, expe={expe}")
                                        print(f"[CREAR Y CALCULAR TASAS] Esto significa que NO se crearán tasas adicionales desde tarifasics")
                                    else:
                                        print(f"[CREAR Y CALCULAR TASAS] ✅ Se encontraron {tarifas_ics.count()} tarifasics, procesando todas...")
                                    
                                    for tarifa_ics in tarifas_ics:
                                        rubro_cod = tarifa_ics.rubro or ''
                                        print(f"[CREAR Y CALCULAR TASAS] 📋 Procesando tarifa_ics: id={tarifa_ics.id}, rubro='{rubro_cod}', cod_tarifa='{tarifa_ics.cod_tarifa}', idneg={tarifa_ics.idneg}")
                                        
                                        # Procesar TODAS las tasas de tarifasics sin restricciones
                                        # Incluye C0001 y C0003 si están en tarifasics
                                        if rubro_cod and rubro_cod.strip():
                                            # Cargar TODAS las tasas de tarifasics hacia tasasdecla
                                            # Usar el idneg de tarifasics si está disponible, sino usar el del negocio
                                            idneg_tarifa = tarifa_ics.idneg if (tarifa_ics.idneg and tarifa_ics.idneg > 0) else idneg
                                            rubros_registrados.append({
                                                'rubro': rubro_cod,
                                                'cod_tarifa': tarifa_ics.cod_tarifa or '',
                                                'valor_default': tarifa_ics.valor or Decimal('0.00'),
                                                'cuenta': tarifa_ics.cuenta or '',
                                                'cuentarez': tarifa_ics.cuentarez or '',
                                                'idneg': idneg_tarifa
                                            })
                                            print(f"[CREAR Y CALCULAR TASAS] ✅ Agregado a rubros_registrados: Rubro={rubro_cod}, Cod_Tarifa={tarifa_ics.cod_tarifa}, IDNeg={idneg_tarifa}, Valor={tarifa_ics.valor}")
                                        else:
                                            print(f"[CREAR Y CALCULAR TASAS] ⚠️ Saltando tarifa_ics id={tarifa_ics.id} (rubro vacío o inválido: '{rubro_cod}')")
                                    
                                    print(f"[CREAR Y CALCULAR TASAS] 📊 TOTAL Rubros registrados en tarifasics: {len(rubros_registrados)}")
                                    if len(rubros_registrados) == 0:
                                        print(f"[CREAR Y CALCULAR TASAS] ⚠️⚠️⚠️ ADVERTENCIA CRÍTICA: No se agregaron rubros a rubros_registrados")
                                        print(f"[CREAR Y CALCULAR TASAS] Esto significa que NO se crearán tasas desde tarifasics")
                                    else:
                                        for r in rubros_registrados:
                                            print(f"   ✅ Rubro: {r['rubro']}, Cod_Tarifa: {r['cod_tarifa']}, Cuenta: {r['cuenta']}, CuentaRez: {r['cuentarez']}, IDNeg: {r['idneg']}, Valor: {r['valor_default']}")
                                except Exception as e:
                                    print(f"[CREAR Y CALCULAR TASAS] ❌❌❌ ERROR CRÍTICO obteniendo tarifasics: {e}")
                                    import traceback
                                    traceback.print_exc()
                                    print(f"[CREAR Y CALCULAR TASAS] El proceso continuará pero NO se crearán tasas desde tarifasics")
                                
                                # ============================================================
                                # PASO 2: Crear tasas faltantes para cada rubro registrado
                                # IMPORTANTE: Este paso SIEMPRE debe ejecutarse, incluso si rubros_registrados está vacío
                                # ============================================================
                                print(f"\n[CREAR Y CALCULAR TASAS] {'='*90}")
                                print(f"[CREAR Y CALCULAR TASAS] PASO 2: Crear tasas desde TarifasICS")
                                print(f"[CREAR Y CALCULAR TASAS] {'='*90}")
                                ano_decimal = Decimal(str(ano)) if ano else Decimal('0')
                                print(f"[CREAR Y CALCULAR TASAS] 📅 Año para crear tasas: {ano_decimal}")
                                print(f"[CREAR Y CALCULAR TASAS] 🔄 Total de rubros a procesar: {len(rubros_registrados)}")
                                
                                if len(rubros_registrados) == 0:
                                    print(f"[CREAR Y CALCULAR TASAS] ⚠️⚠️⚠️ CRÍTICO: rubros_registrados está vacío!")
                                    print(f"[CREAR Y CALCULAR TASAS] No se crearán tasas desde tarifasics porque no hay rubros registrados")
                                    print(f"[CREAR Y CALCULAR TASAS] Revisar si se encontraron tarifasics anteriormente")
                                else:
                                    print(f"[CREAR Y CALCULAR TASAS] ✅ Iniciando creación de {len(rubros_registrados)} tasas desde tarifasics")
                                
                                tasas_creadas_count = 0
                                tasas_existentes_count = 0
                                
                                for rubro_info in rubros_registrados:
                                    rubro_cod = rubro_info['rubro']
                                    cod_tarifa = rubro_info['cod_tarifa']
                                    
                                    # Obtener idneg desde rubro_info (viene de tarifasics) o usar el idneg del negocio
                                    idneg_tasa = rubro_info.get('idneg', idneg) or idneg
                                    
                                    print(f"[CREAR Y CALCULAR TASAS] 🔍 [{tasas_creadas_count + tasas_existentes_count + 1}/{len(rubros_registrados)}] Verificando tasa: Rubro={rubro_cod}, Cod_Tarifa={cod_tarifa}, IDNeg={idneg_tasa}")
                                    
                                    # Verificar si ya existe la tasa en TasasDecla
                                    # IMPORTANTE: No filtrar por cod_tarifa porque puede variar
                                    tasa_existente = TasasDecla.objects.filter(
                                        empresa=empresa,
                                        rtm=rtm,
                                        expe=expe,
                                        ano=ano_decimal,
                                        rubro=rubro_cod
                                    ).first()
                                    
                                    if tasa_existente:
                                        print(f"[CREAR Y CALCULAR TASAS] ⚠️ Tasa ya existe para Rubro={rubro_cod}: ID={tasa_existente.id}, Valor={tasa_existente.valor}, Nodecla={tasa_existente.nodecla}, Cod_Tarifa={tasa_existente.cod_tarifa}, IDNeg={tasa_existente.idneg}")
                                        tasas_existentes_count += 1
                                        # Actualizar idneg si es diferente y actualizar cod_tarifa si es diferente
                                        if tasa_existente.idneg != idneg_tasa:
                                            print(f"[CREAR Y CALCULAR TASAS] 🔄 Actualizando idneg de '{tasa_existente.idneg}' a '{idneg_tasa}'")
                                            tasa_existente.idneg = idneg_tasa
                                            tasa_existente.save()
                                        if tasa_existente.cod_tarifa != cod_tarifa:
                                            print(f"[CREAR Y CALCULAR TASAS] 🔄 Actualizando cod_tarifa de '{tasa_existente.cod_tarifa}' a '{cod_tarifa}'")
                                            tasa_existente.cod_tarifa = cod_tarifa
                                            tasa_existente.save()
                                    else:
                                        print(f"[CREAR Y CALCULAR TASAS] ✅ Tasa NO existe, procediendo a crear: Rubro={rubro_cod}, Cod_Tarifa={cod_tarifa}")
                                    
                                    if not tasa_existente:
                                        # Obtener información del rubro
                                        try:
                                            rubro_obj = Rubro.objects.filter(
                                                empresa=empresa,
                                                codigo=rubro_cod
                                            ).first()
                                            
                                            tipota = 'F'  # Por defecto Fija
                                            frecuencia = 'A'  # Por defecto Anual
                                            
                                            # Obtener frecuencia y tipo desde la tabla Tarifas
                                            # Vinculación: tarifas.empresa = tasasdecla.empresa AND tarifas.rubro = tasasdecla.rubro AND tarifas.cod_tarifa = tasasdecla.cod_tarifa
                                            try:
                                                tarifa_info = None
                                                if cod_tarifa:
                                                    tarifa_info = Tarifas.objects.filter(
                                                        empresa=empresa,
                                                        rubro=rubro_cod,
                                                        cod_tarifa=cod_tarifa
                                                    ).first()
                                                
                                                # Si no se encontró con cod_tarifa, intentar solo con empresa y rubro
                                                if not tarifa_info:
                                                    tarifa_info = Tarifas.objects.filter(
                                                        empresa=empresa,
                                                        rubro=rubro_cod
                                                    ).first()
                                                
                                                if tarifa_info:
                                                    # Obtener frecuencia desde Tarifas (tarifas.frecuencia → tasasdecla.frecuencia)
                                                    if tarifa_info.frecuencia:
                                                        frecuencia = tarifa_info.frecuencia.upper()
                                                        print(f"[CREAR Y CALCULAR TASAS] 📅 Frecuencia obtenida desde Tarifas: {frecuencia} para empresa={empresa}, rubro={rubro_cod}")
                                                    
                                                    # Obtener tipo desde Tarifas (tarifas.tipo → tasasdecla.tipota)
                                                    if tarifa_info.tipo:
                                                        tipota = tarifa_info.tipo.upper()
                                                        print(f"[CREAR Y CALCULAR TASAS] 🏷️  Tipo obtenido desde Tarifas: {tipota} para empresa={empresa}, rubro={rubro_cod}")
                                                else:
                                                    print(f"[CREAR Y CALCULAR TASAS] ⚠️ No se encontró tarifa para empresa={empresa}, rubro={rubro_cod}, cod_tarifa={cod_tarifa}, usando valores por defecto")
                                            except Exception as e:
                                                print(f"[CREAR Y CALCULAR TASAS] ⚠️ Error obteniendo info desde Tarifas: {e}, usando valores por defecto")
                                            
                                            # Si no se obtuvo el tipo desde Tarifas, usar el del Rubro como fallback
                                            if tipota == 'F' and rubro_obj:
                                                if hasattr(rubro_obj, 'tipo') and rubro_obj.tipo:
                                                    # Si tipo es 'V' o 'Variable', usar 'V'
                                                    tipo_str = str(rubro_obj.tipo).upper()
                                                    if 'V' in tipo_str or 'VARIABLE' in tipo_str:
                                                        tipota = 'V'
                                                        print(f"[CREAR Y CALCULAR TASAS] 🏷️  Tipo obtenido desde Rubro (fallback): {tipota}")
                                            
                                            # Usar cuentas de tarifasics si están disponibles, si no del rubro, si no valores por defecto
                                            cuenta = rubro_info.get('cuenta', '') or ''
                                            cuentarez = rubro_info.get('cuentarez', '') or ''
                                            
                                            if not cuenta and rubro_obj:
                                                cuenta = getattr(rubro_obj, 'cuenta', '') or ''
                                            if not cuenta:
                                                cuenta = '11.7.1.01.09.00'  # Valor por defecto
                                            
                                            if not cuentarez and rubro_obj:
                                                cuentarez = getattr(rubro_obj, 'cuntarez', '') or getattr(rubro_obj, 'cuentarez', '') or ''
                                            if not cuentarez:
                                                cuentarez = '11.7.1.98.01.00'  # Valor por defecto
                                            
                                            # idneg_tasa ya se definió antes del bloque if not tasa_existente
                                            print(f"[CREAR Y CALCULAR TASAS] Creando tasa: Rubro={rubro_cod}, Cod_Tarifa={cod_tarifa}, Tipo={tipota}, Cuenta={cuenta}, CuentaRez={cuentarez}, IDNeg={idneg_tasa}")
                                            
                                            # Crear nueva tasa en TasasDecla
                                            nueva_tasa = TasasDecla.objects.create(
                                                empresa=empresa,
                                                idneg=idneg_tasa,  # Usar el idneg de tarifasics o del negocio
                                                rtm=rtm,
                                                expe=expe,
                                                ano=ano_decimal,
                                                rubro=rubro_cod,
                                                cod_tarifa=cod_tarifa or '',
                                                nodecla=nodecla,
                                                frecuencia=frecuencia,
                                                valor=rubro_info['valor_default'],
                                                cuenta=cuenta,
                                                cuentarez=cuentarez,
                                                tipota=tipota
                                            )
                                            tasas_creadas.append({
                                                'rubro': rubro_cod,
                                                'cod_tarifa': cod_tarifa,
                                                'tipota': tipota,
                                                'valor': float(rubro_info['valor_default'])
                                            })
                                            tasas_creadas_count += 1
                                            print(f"[CREAR Y CALCULAR TASAS] ✅ [{tasas_creadas_count}] Tasa creada: Rubro={rubro_cod}, Tipo={tipota}, Frecuencia={frecuencia}, Valor={rubro_info['valor_default']}, ID={nueva_tasa.id}")
                                        except Exception as e:
                                            print(f"[CREAR Y CALCULAR TASAS] ❌ Error creando tasa para rubro {rubro_cod}: {e}")
                                            import traceback
                                            traceback.print_exc()
                                            tasas_error_calc.append({
                                                'rubro': rubro_cod,
                                                'error': f'Error creando tasa: {str(e)}'
                                            })
                                
                                print(f"\n[CREAR Y CALCULAR TASAS] {'='*90}")
                                print(f"[CREAR Y CALCULAR TASAS] 📊 RESUMEN FINAL DEL PASO 2 (CREACIÓN DE TASAS)")
                                print(f"[CREAR Y CALCULAR TASAS] {'='*90}")
                                print(f"[CREAR Y CALCULAR TASAS]   ✅ Rubros encontrados en tarifasics: {len(rubros_registrados)}")
                                print(f"[CREAR Y CALCULAR TASAS]   ✅ Tasas creadas NUEVAS: {tasas_creadas_count}")
                                print(f"[CREAR Y CALCULAR TASAS]   ⚠️  Tasas existentes (no creadas): {tasas_existentes_count}")
                                print(f"[CREAR Y CALCULAR TASAS]   📊 Total procesadas: {len(rubros_registrados)}")
                                print(f"[CREAR Y CALCULAR TASAS] {'='*90}")
                                
                                if tasas_creadas_count == 0 and len(rubros_registrados) > 0:
                                    print(f"\n[CREAR Y CALCULAR TASAS] ⚠️⚠️⚠️ PROBLEMA DETECTADO:")
                                    print(f"[CREAR Y CALCULAR TASAS] Se encontraron {len(rubros_registrados)} rubros pero NO se creó ninguna tasa nueva")
                                    print(f"[CREAR Y CALCULAR TASAS] POSIBLES CAUSAS:")
                                    print(f"   1. Todas las tasas ya existen en tasasdecla (revisar si están con el mismo año)")
                                    print(f"   2. Hay errores en la creación (revisar logs anteriores con ❌)")
                                    print(f"   3. Filtros de búsqueda están excluyendo las tasas (empresa, rtm, expe, ano)")
                                    print(f"[CREAR Y CALCULAR TASAS] ACCIÓN: Revisar logs anteriores para cada rubro")
                                elif len(rubros_registrados) == 0:
                                    print(f"\n[CREAR Y CALCULAR TASAS] ⚠️⚠️⚠️ PROBLEMA CRÍTICO:")
                                    print(f"[CREAR Y CALCULAR TASAS] No se encontraron rubros en tarifasics")
                                    print(f"[CREAR Y CALCULAR TASAS] Verificar que existan registros en tarifasics para:")
                                    print(f"   - empresa='{empresa}', rtm='{rtm}', expe='{expe}'")
                                    print(f"[CREAR Y CALCULAR TASAS] ACCIÓN: Verificar que las tarifasics existan en la base de datos")
                                else:
                                    print(f"\n[CREAR Y CALCULAR TASAS] ✅✅✅ ÉXITO:")
                                    print(f"[CREAR Y CALCULAR TASAS] Se crearon {tasas_creadas_count} tasas nuevas desde tarifasics")
                                
                                # ============================================================
                                # PASO 3: Obtener todas las tasas del negocio (existentes + nuevas)
                                # ============================================================
                                print(f"\n[CREAR Y CALCULAR TASAS] {'='*90}")
                                print(f"[CREAR Y CALCULAR TASAS] PASO 3: Calcular valores de tasas (Fijas y Variables)")
                                print(f"[CREAR Y CALCULAR TASAS] {'='*90}")
                                tasas_decla_calc = TasasDecla.objects.filter(
                                    empresa=empresa,
                                    rtm=rtm,
                                    expe=expe
                                )
                                
                                if ano:
                                    tasas_decla_calc = tasas_decla_calc.filter(ano=Decimal(ano))
                                
                                total_tasas = tasas_decla_calc.count()
                                print(f"[CREAR Y CALCULAR TASAS] 📊 Total de tasas encontradas en TasasDecla: {total_tasas}")
                                print(f"[CREAR Y CALCULAR TASAS]   (Esto incluye las tasas recién creadas + las existentes)")
                                if total_tasas == 0:
                                    print(f"[CREAR Y CALCULAR TASAS] ⚠️ ADVERTENCIA: No se encontraron tasas en TasasDecla después de la creación")
                                elif len(rubros_registrados) > 0 and total_tasas < len(rubros_registrados) + 2:  # +2 por C0001 y C0003
                                    print(f"[CREAR Y CALCULAR TASAS] ⚠️ ADVERTENCIA: Se esperaban más tasas. Total: {total_tasas}, Esperadas: {len(rubros_registrados) + 2}")
                                else:
                                    print(f"[CREAR Y CALCULAR TASAS] ✅ Total de tasas correcto")
                                
                                # Procesar cada tasa
                                for tasa_calc in tasas_decla_calc:
                                    try:
                                        rubro_tasa_calc = tasa_calc.rubro or ''
                                        ano_tasa_calc = tasa_calc.ano
                                        
                                        print(f"[CALCULAR TASAS] Procesando: Rubro={rubro_tasa_calc}, Año={ano_tasa_calc}, Tipo={tasa_calc.tipota}")
                                        
                                        # TASA FIJA (Tipo "F")
                                        if tasa_calc.tipota == 'F':
                                            try:
                                                # Vinculación: tarifas.empresa = tasasdecla.empresa AND tarifas.rubro = tasasdecla.rubro AND tarifas.cod_tarifa = tasasdecla.cod_tarifa
                                                cod_tarifa_tasa = tasa_calc.cod_tarifa or ''
                                                tarifa = None
                                                
                                                if cod_tarifa_tasa:
                                                    tarifa = Tarifas.objects.filter(
                                                        empresa=empresa,
                                                        rubro=rubro_tasa_calc,
                                                        cod_tarifa=cod_tarifa_tasa
                                                    ).first()
                                                
                                                # Si no se encontró con cod_tarifa, intentar solo con empresa y rubro
                                                if not tarifa:
                                                    tarifa = Tarifas.objects.filter(
                                                        empresa=empresa,
                                                        rubro=rubro_tasa_calc
                                                    ).first()
                                                
                                                if tarifa and tarifa.valor:
                                                    tasa_calc.valor = tarifa.valor
                                                    # Actualizar frecuencia desde Tarifas si está disponible
                                                    if tarifa.frecuencia:
                                                        tasa_calc.frecuencia = tarifa.frecuencia.upper()
                                                        print(f"[CALCULAR TASAS] 📅 Frecuencia actualizada desde Tarifas: {tarifa.frecuencia.upper()}")
                                                    # Actualizar tipo (tipota) desde Tarifas si está disponible
                                                    if tarifa.tipo:
                                                        tasa_calc.tipota = tarifa.tipo.upper()
                                                        print(f"[CALCULAR TASAS] 🏷️  Tipo actualizado desde Tarifas: {tarifa.tipo.upper()}")
                                                    tasa_calc.save()
                                                    tasas_calculadas.append({
                                                        'rubro': rubro_tasa_calc,
                                                        'ano': str(int(ano_tasa_calc)),
                                                        'tipo': 'F',
                                                        'valor': str(tarifa.valor),
                                                        'frecuencia': tarifa.frecuencia.upper() if tarifa.frecuencia else 'A',
                                                        'mensaje': 'Tasa fija actualizada desde tarifas'
                                                    })
                                                    print(f"[CALCULAR TASAS] ✅ Tasa Fija actualizada: {rubro_tasa_calc} = {tarifa.valor}, Frecuencia: {tarifa.frecuencia.upper() if tarifa.frecuencia else 'A'}, Tipo: {tarifa.tipo.upper() if tarifa.tipo else 'F'}")
                                            except Exception as e:
                                                print(f"[CALCULAR TASAS] ❌ Error en tasa fija: {e}")
                                                tasas_error_calc.append({
                                                    'rubro': rubro_tasa_calc,
                                                    'error': str(e)
                                                })
                                        
                                        # TASA VARIABLE (Tipo "V")
                                        elif tasa_calc.tipota == 'V':
                                            try:
                                                plan = PlanArbitrio.objects.filter(
                                                    empresa=empresa,
                                                    rubro=rubro_tasa_calc,
                                                    ano=ano_tasa_calc
                                                ).order_by('codigo').filter(
                                                    minimo__lt=valorbase,
                                                    maximo__gte=valorbase
                                                ).first()
                                                
                                                if plan and plan.valor:
                                                    tasa_calc.valor = plan.valor
                                                    tasa_calc.save()
                                                    tasas_calculadas.append({
                                                        'rubro': rubro_tasa_calc,
                                                        'ano': str(int(ano_tasa_calc)),
                                                        'tipo': 'V',
                                                        'valor': str(plan.valor),
                                                        'mensaje': f'Tasa variable actualizada según plan de arbitrio (rango {plan.minimo}-{plan.maximo})'
                                                    })
                                                    print(f"[CALCULAR TASAS] ✅ Tasa Variable actualizada: {rubro_tasa_calc} = {plan.valor}")
                                                else:
                                                    # Intentar con rangos inclusivos
                                                    plan = PlanArbitrio.objects.filter(
                                                        empresa=empresa,
                                                        rubro=rubro_tasa_calc,
                                                        ano=ano_tasa_calc
                                                    ).order_by('codigo').filter(
                                                        minimo__lte=valorbase,
                                                        maximo__gte=valorbase
                                                    ).first()
                                                    
                                                    if plan and plan.valor:
                                                        tasa_calc.valor = plan.valor
                                                        tasa_calc.save()
                                                        tasas_calculadas.append({
                                                            'rubro': rubro_tasa_calc,
                                                            'ano': str(int(ano_tasa_calc)),
                                                            'tipo': 'V',
                                                            'valor': str(plan.valor),
                                                            'mensaje': f'Tasa variable actualizada según plan de arbitrio (rango {plan.minimo}-{plan.maximo})'
                                                        })
                                                        print(f"[CALCULAR TASAS] ✅ Tasa Variable actualizada: {rubro_tasa_calc} = {plan.valor}")
                                                    else:
                                                        tasas_error_calc.append({
                                                            'rubro': rubro_tasa_calc,
                                                            'error': f'No se encontró plan de arbitrio con rango que incluya {valorbase}'
                                                        })
                                                        print(f"[CALCULAR TASAS] ⚠️  No se encontró plan para {rubro_tasa_calc}")
                                            except Exception as e:
                                                print(f"[CALCULAR TASAS] ❌ Error en tasa variable: {e}")
                                                tasas_error_calc.append({
                                                    'rubro': rubro_tasa_calc,
                                                    'error': str(e)
                                                })
                                        
                                    except Exception as e:
                                        print(f"[CALCULAR TASAS] ❌ Error procesando tasa: {e}")
                                        tasas_error_calc.append({
                                            'rubro': 'N/A',
                                            'error': str(e)
                                        })
                                
                                print(f"\n[CREAR Y CALCULAR TASAS] {'='*100}")
                                print(f"[CREAR Y CALCULAR TASAS] ✅✅✅ PROCESO COMPLETADO ✅✅✅")
                                print(f"[CREAR Y CALCULAR TASAS] {'='*100}")
                                print(f"[CREAR Y CALCULAR TASAS]   📊 Tasas creadas desde tarifasics: {len(tasas_creadas)}")
                                print(f"[CREAR Y CALCULAR TASAS]   🔢 Tasas calculadas/actualizadas: {len(tasas_calculadas)}")
                                print(f"[CREAR Y CALCULAR TASAS]   ⚠️  Errores encontrados: {len(tasas_error_calc)}")
                                if tasas_error_calc:
                                    print(f"[CREAR Y CALCULAR TASAS]   Lista de errores:")
                                    for error in tasas_error_calc:
                                        rubro_error = error.get('rubro', 'N/A')
                                        mensaje_error = error.get('error', 'Desconocido')
                                        print(f"      - Rubro: {rubro_error}, Error: {mensaje_error}")
                                print(f"[CREAR Y CALCULAR TASAS] {'='*100}")
                                print()
                            
                            except Exception as e:
                                print(f"[CREAR Y CALCULAR TASAS] ❌❌❌ ERROR GENERAL EN PROCESO DE TASAS: {e}")
                                import traceback
                                traceback.print_exc()
                                print(f"[CREAR Y CALCULAR TASAS] ⚠️ El proceso de tasas falló, pero la declaración se guardó correctamente")
                                # Asegurar que las listas estén inicializadas para evitar errores después
                                if 'tasas_creadas' not in locals():
                                    tasas_creadas = []
                                if 'tasas_calculadas' not in locals():
                                    tasas_calculadas = []
                                if 'tasas_error_calc' not in locals():
                                    tasas_error_calc = []
                            
                            # Agregar información de tasas creadas y calculadas al mensaje
                            mensaje_final = 'Declaración guardada exitosamente en tabla declara y TasasDecla'
                            if len(tasas_creadas) > 0:
                                mensaje_final += f'. {len(tasas_creadas)} tasa(s) creada(s) desde rubros registrados'
                            if len(tasas_calculadas) > 0:
                                mensaje_final += f'. {len(tasas_calculadas)} tasa(s) calculada(s) según plan de arbitrios y tarifas'
                            
                            return JsonResponse({
                                'exito': True,
                                'mensaje': mensaje_final,
                                'impuesto': impuesto,
                                'multa': multa,
                                'tasas_actualizadas': tasas_actualizadas,
                                'tasas_creadas': tasas_creadas,  # Nuevas tasas creadas
                                'tasas_calculadas': tasas_calculadas,  # Tasas actualizadas desde plan/tarifas
                                'tasas_error_calc': tasas_error_calc,   # Errores en el proceso
                                'valor_base': valor_base_calculado,
                                'nodecla': nodecla
                            })
                            
                        except Exception as e:
                            print(f"[DEBUG] Error guardando en base de datos: {str(e)}")
                            return JsonResponse({
                                'exito': False,
                                'mensaje': f'Error al guardar en base de datos: {str(e)}',
                                'impuesto': 0
                            })
                    else:
                        print(f"[DEBUG] Formulario AJAX inválido: {form.errors}")
                        return JsonResponse({
                            'exito': False,
                            'mensaje': 'Error en el formulario',
                            'errores': form.errors
                        })
                elif accion == 'generar_transacciones':
                    print("[DEBUG] Procesando generar_transacciones AJAX...")
                    try:
                        from datetime import date
                        from tributario.models import TransaccionesIcs, Negocio as NegocioModel, TasasDecla, DeclaracionVolumen
                        from decimal import Decimal
                        from django.utils import timezone
                        
                        # Obtener datos del JSON
                        empresa_get = data.get('empresa', '')
                        rtm_get = data.get('rtm', '')
                        expe_get = data.get('expe', '')
                        ano_get = data.get('ano', '')
                        mes_get = data.get('mes', '')
                        
                        print(f"[GENERAR TRANSACCIONES] Datos recibidos: empresa={empresa_get}, rtm={rtm_get}, expe={expe_get}, ano={ano_get}, mes={mes_get}")
                        
                        # Validar parámetros
                        if not empresa_get or not rtm_get or not expe_get:
                            return JsonResponse({
                                'exito': False,
                                'mensaje': 'Empresa, RTM y Expediente son obligatorios para generar transacciones',
                                'impuesto': 0
                            })
                        
                        # Buscar el negocio
                        try:
                            negocio_obj = NegocioModel.objects.get(
                                empresa=empresa_get,
                                rtm=rtm_get,
                                expe=expe_get
                            )
                        except NegocioModel.DoesNotExist:
                            return JsonResponse({
                                'exito': False,
                                'mensaje': f'No se encontró el negocio con RTM={rtm_get} y EXPE={expe_get}',
                                'impuesto': 0
                            })
                        
                        # Buscar la declaración
                        declaracion_actual = None
                        if ano_get and mes_get:
                            try:
                                declaracion_actual = DeclaracionVolumen.objects.filter(
                                    empresa=empresa_get,
                                    rtm=rtm_get,
                                    expe=expe_get,
                                    ano=int(ano_get),
                                    mes=int(mes_get)
                                ).first()
                            except Exception:
                                pass
                            # Si el usuario pidió un año/mes específico, NO usar fallback.
                            if not declaracion_actual:
                                return JsonResponse({
                                    'exito': False,
                                    'tipo_validacion': True,
                                    'mensaje': (
                                        f'⚠️ Validación: No existe una declaración guardada para el período '
                                        f'{ano_get}/{mes_get} (empresa={empresa_get}, RTM={rtm_get}, EXPE={expe_get}). '
                                        f'Guarde la declaración de ese período antes de generar transacciones.'
                                    ),
                                    'impuesto': 0
                                })
                        
                        if not declaracion_actual:
                            # Sin año/mes explícitos: usar la última declaración como compatibilidad
                            declaracion_actual = DeclaracionVolumen.objects.filter(
                                empresa=empresa_get,
                                rtm=rtm_get,
                                expe=expe_get
                            ).order_by('-ano', '-mes').first()
                        
                        if not declaracion_actual:
                            return JsonResponse({
                                'exito': False,
                                'mensaje': 'No se encontró una declaración para generar transacciones. Debe guardar una declaración primero.',
                                'impuesto': 0
                            })
                        
                        # Obtener tasas de tasasdecla vinculadas a esta declaración
                        nodecla_declaracion = declaracion_actual.nodecla
                        ano_declaracion = int(declaracion_actual.ano) if declaracion_actual.ano else 0
                        mes_declaracion = int(declaracion_actual.mes) if declaracion_actual.mes else 0
                        tipo_declaracion = int(declaracion_actual.tipo) if declaracion_actual.tipo else 0
                        
                        print(f"[GENERAR TRANSACCIONES] Declaración: nodecla={nodecla_declaracion}, año={ano_declaracion}, mes={mes_declaracion}, tipo={tipo_declaracion}")
                        
                        tasas_declaracion = TasasDecla.objects.filter(
                            empresa=empresa_get,
                            rtm=rtm_get,
                            expe=expe_get,
                            nodecla=nodecla_declaracion
                        ).order_by('rubro', 'cod_tarifa')
                        
                        if not tasas_declaracion.exists():
                            return JsonResponse({
                                'exito': False,
                                'mensaje': f'No se encontraron tasas en tasasdecla para la declaración {nodecla_declaracion}. Debe calcular las tasas primero.',
                                'impuesto': 0
                            })
                        
                        print(f"[GENERAR TRANSACCIONES] Tasas encontradas: {tasas_declaracion.count()}")
                        
                        # VALIDACIÓN: Verificar si existen pagos (operacion = 'P') en el año de la declaración
                        # Vinculación: empresa, rtm, expe y año
                        pagos_existentes = TransaccionesIcs.objects.filter(
                            empresa=empresa_get,
                            rtm=rtm_get,
                            expe=expe_get,
                            ano=Decimal(ano_declaracion),  # Convertir a Decimal para comparación correcta
                            operacion='P'  # Operación de Pago
                        ).exists()
                        
                        if pagos_existentes:
                            return JsonResponse({
                                'exito': False,
                                'mensaje': f'⚠️ Validación: No se pueden generar transacciones porque existen pagos registrados para el año {ano_declaracion} (empresa={empresa_get}, RTM={rtm_get}, EXPE={expe_get}). No se permite regenerar transacciones cuando ya hay pagos aplicados.',
                                'tipo_validacion': True,  # Indicar que es una validación, no un error técnico
                                'impuesto': 0
                            })
                        
                        # Si no hay pagos, eliminar transacciones existentes del mismo año antes de generar nuevas
                        # Buscar transacciones de facturación (operacion = 'F') del año de la declaración
                        transacciones_existentes = TransaccionesIcs.objects.filter(
                            empresa=empresa_get,
                            rtm=rtm_get,
                            expe=expe_get,
                            ano=ano_declaracion,
                            operacion='F'  # Operación de Facturación
                        )
                        
                        transacciones_eliminadas = 0
                        if transacciones_existentes.exists():
                            transacciones_eliminadas = transacciones_existentes.count()
                            print(f"[GENERAR TRANSACCIONES] ⚠️ Eliminando {transacciones_eliminadas} transacción(es) existente(s) del año {ano_declaracion} antes de generar nuevas...")
                            transacciones_existentes.delete()
                            print(f"[GENERAR TRANSACCIONES] ✅ Transacciones eliminadas exitosamente")
                        
                        # Obtener última transacción para calcular saldo inicial (después de eliminar las del año)
                        ultima_transaccion = TransaccionesIcs.objects.filter(
                            empresa=empresa_get,
                            rtm=rtm_get,
                            expe=expe_get
                        ).order_by('-vencimiento', '-fecha', '-id').first()
                        
                        saldo_inicial = Decimal('0.00')
                        if ultima_transaccion:
                            saldo_inicial = ultima_transaccion.monto
                        
                        usuario = request.session.get('usuario', '')
                        transacciones_creadas = []
                        transacciones_actualizadas = 0
                        transacciones_nuevas = 0
                        
                        # Obtener año vigente (año actual)
                        from datetime import datetime
                        ano_vigente = datetime.now().year
                        print(f"[GENERAR TRANSACCIONES] Año declaración: {ano_declaracion}, Año vigente: {ano_vigente}, Tipo: {tipo_declaracion}")
                        
                        # Función para crear o actualizar una transacción
                        def crear_o_actualizar_transaccion(rtm_val, expe_val, empresa_val, idneg_val, nodecla_str, 
                                            rubro_val, cod_tarifa_val, valor_tasa_val, 
                                            ano_trans, mes_trans, fecha_vencimiento_val):
                            """
                            Crea o actualiza una transacción según empresa, rtm, expe, ano, mes y rubro.
                            El monto se establece con el valor de la tasa.
                            """
                            mes_str = str(mes_trans).zfill(2) if mes_trans else ''
                            
                            # Buscar transacción existente
                            transaccion_existente = TransaccionesIcs.objects.filter(
                                empresa=empresa_val,
                                rtm=rtm_val,
                                expe=expe_val,
                                ano=ano_trans,
                                mes=mes_str,
                                rubro=rubro_val
                            ).first()
                            
                            # El monto es el valor de la tasa
                            monto_val = valor_tasa_val
                            
                            if transaccion_existente:
                                # ACTUALIZAR transacción existente
                                print(f"[GENERAR TRANSACCIONES] ⚠️ Transacción existente encontrada para empresa={empresa_val}, rtm={rtm_val}, expe={expe_val}, ano={ano_trans}, mes={mes_str}, rubro={rubro_val}. Actualizando...")
                                transaccion_existente.idneg = idneg_val
                                transaccion_existente.nodeclara = nodecla_str[:20] if nodecla_str else ''  # Truncar a 20 caracteres si es necesario
                                transaccion_existente.operacion = 'F'  # F = Facturación
                                # fecha = fecha de emisión / generación del cargo
                                transaccion_existente.fecha = date.today()
                                # vencimiento = fecha de vencimiento real de la cuota
                                transaccion_existente.vencimiento = fecha_vencimiento_val
                                transaccion_existente.monto = monto_val
                                transaccion_existente.tasa = Decimal('0.00')
                                transaccion_existente.usuario = usuario
                                transaccion_existente.fechasys = timezone.now()
                                transaccion_existente.save()
                                # Forzar tasa a 0 después de guardar (protección adicional)
                                TransaccionesIcs.objects.filter(id=transaccion_existente.id).update(tasa=Decimal('0.00'))
                                print(f"[GENERAR TRANSACCIONES] ✅ Transacción actualizada: ID={transaccion_existente.id}, Monto={monto_val}")
                                return transaccion_existente
                            else:
                                # CREAR nueva transacción
                                nueva_transaccion = TransaccionesIcs(
                                    idneg=idneg_val,
                                    nodeclara=nodecla_str[:20] if nodecla_str else '',  # Truncar a 20 caracteres si es necesario
                                    empresa=empresa_val,
                                    rtm=rtm_val,
                                    expe=expe_val,
                                    rubro=rubro_val,
                                    ano=ano_trans,
                                    mes=mes_str,
                                    operacion='F',  # F = Facturación
                                    # fecha = fecha de emisión / generación del cargo
                                    fecha=date.today(),
                                    # vencimiento = fecha de vencimiento real de la cuota
                                    vencimiento=fecha_vencimiento_val,
                                    monto=monto_val,
                                    tasa=Decimal('0.00'),
                                    usuario=usuario,
                                    fechasys=timezone.now()
                                )
                                nueva_transaccion.save()
                                # Forzar tasa a 0 después de guardar (protección adicional)
                                TransaccionesIcs.objects.filter(id=nueva_transaccion.id).update(tasa=Decimal('0.00'))
                                print(f"[GENERAR TRANSACCIONES] ✅ Nueva transacción creada: ID={nueva_transaccion.id}, Monto={monto_val}")
                                return nueva_transaccion
                        
                        # Procesar cada tasa y crear transacciones según frecuencia y tipo
                        for tasa in tasas_declaracion:
                            frecuencia = tasa.frecuencia or ''
                            valor_tasa = tasa.valor or Decimal('0.00')
                            cod_tarifa = tasa.cod_tarifa or 'DEC'
                            rubro = tasa.rubro or ''
                            
                            print(f"[GENERAR TRANSACCIONES] Procesando: Rubro={rubro}, Tarifa={cod_tarifa}, Frecuencia={frecuencia}, Valor={valor_tasa}")
                            
                            # Obtener número de declaración (nodecla)
                            # El nodecla viene de tasasdecla y tiene formato "expe-ano" (ej: "1151-2025")
                            # En TransaccionesIcs, nodeclara es CharField(20), así que guardamos el nodecla completo como string
                            nodecla_str = ''
                            if nodecla_declaracion:
                                try:
                                    nodecla_str = str(nodecla_declaracion).strip()
                                    # Asegurar que no exceda 20 caracteres (límite del campo CHAR(20))
                                    if len(nodecla_str) > 20:
                                        nodecla_str = nodecla_str[:20]
                                        print(f"[GENERAR TRANSACCIONES] ⚠️ nodecla truncado a 20 caracteres: '{nodecla_str}'")
                                except (ValueError, TypeError) as e:
                                    print(f"[GENERAR TRANSACCIONES] ⚠️ Error al procesar nodecla '{nodecla_declaracion}': {e}")
                                    nodecla_str = ''
                            
                            print(f"[GENERAR TRANSACCIONES] nodecla original: '{nodecla_declaracion}', nodeclara (string): '{nodecla_str}'")
                            
                            # Asegurar que rtm no exceda el límite del modelo (16 caracteres según estructura real)
                            rtm_valor = str(rtm_get)[:16] if rtm_get else ''
                            
                            # LÓGICA SEGÚN FRECUENCIA Y TIPO
                            # Frecuencia A (Anual) = Cargo único por año
                            # Frecuencia M (Mensual) = Cargos mensuales (12 cuotas o desde mes de ingreso)
                            
                            if frecuencia == 'A':  # FRECUENCIA ANUAL - CARGO ÚNICO POR AÑO
                                if tipo_declaracion == 1:  # Tipo Normal (1 = Normal según tabla declara)
                                    # 1 cargo único: mes de enero, fecha último día del mes de enero (31/01)
                                    fecha_vencimiento = date(ano_declaracion, 1, 31)
                                    
                                    # Verificar si ya existe antes de crear/actualizar
                                    existe_antes = TransaccionesIcs.objects.filter(
                                        empresa=empresa_get, rtm=rtm_valor, expe=expe_get,
                                        ano=ano_declaracion, mes='01', rubro=rubro
                                    ).exists()
                                    
                                    nueva_trans = crear_o_actualizar_transaccion(
                                        rtm_valor, expe_get, empresa_get, 
                                        negocio_obj.id if negocio_obj else 0,
                                        nodecla_str, rubro, cod_tarifa, valor_tasa,
                                        ano_declaracion, 1, fecha_vencimiento
                                    )
                                    transacciones_creadas.append({
                                        'id': nueva_trans.id,
                                        'rubro': rubro,
                                        'tarifa': cod_tarifa,
                                        'valor': float(valor_tasa),
                                        'vencimiento': fecha_vencimiento.strftime('%Y-%m-%d'),
                                        'ano': ano_declaracion,
                                        'mes': 1,
                                        'accion': 'actualizada' if existe_antes else 'creada'
                                    })
                                    print(f"[GENERAR TRANSACCIONES] Anual Normal - Cargo único: Fecha={fecha_vencimiento}, Monto={nueva_trans.monto}")
                                    
                                elif tipo_declaracion == 2:  # Tipo Apertura (2 = Apertura según tabla declara)
                                    # 1 cargo único según el mes y año que se ingrese la declaración
                                    # Fecha: último día del mes de declaración
                                    from calendar import monthrange
                                    ultimo_dia = monthrange(ano_declaracion, mes_declaracion)[1]
                                    fecha_vencimiento = date(ano_declaracion, mes_declaracion, ultimo_dia)
                                    
                                    # Verificar si ya existe antes de crear/actualizar
                                    mes_str_ap = str(mes_declaracion).zfill(2)
                                    existe_antes = TransaccionesIcs.objects.filter(
                                        empresa=empresa_get, rtm=rtm_valor, expe=expe_get,
                                        ano=ano_declaracion, mes=mes_str_ap, rubro=rubro
                                    ).exists()
                                    
                                    nueva_trans = crear_o_actualizar_transaccion(
                                        rtm_valor, expe_get, empresa_get,
                                        negocio_obj.id if negocio_obj else 0,
                                        nodecla_str, rubro, cod_tarifa, valor_tasa,
                                        ano_declaracion, mes_declaracion, fecha_vencimiento
                                    )
                                    transacciones_creadas.append({
                                        'id': nueva_trans.id,
                                        'rubro': rubro,
                                        'tarifa': cod_tarifa,
                                        'valor': float(valor_tasa),
                                        'vencimiento': fecha_vencimiento.strftime('%Y-%m-%d'),
                                        'ano': ano_declaracion,
                                        'mes': mes_declaracion,
                                        'accion': 'actualizada' if existe_antes else 'creada'
                                    })
                                    print(f"[GENERAR TRANSACCIONES] Anual Apertura - Cargo único: Fecha={fecha_vencimiento}, Monto={nueva_trans.monto}")
                            
                            elif frecuencia == 'M':  # FRECUENCIA MENSUAL - CARGOS MENSUALES
                                if tipo_declaracion == 1:  # Tipo Normal (1 = Normal según tabla declara)
                                    # IMPORTANTE: Para tipo Normal y frecuencia M, generar SIEMPRE 12 cuotas
                                    # La cuota de enero SIEMPRE es último día del mes (31/01)
                                    # El resto de las cuotas (febrero a diciembre) se graban con el día 11 de cada mes
                                    print(f"[GENERAR TRANSACCIONES] Tipo Normal + Frecuencia M: Generando 12 cuotas para rubro {rubro}")
                                    for mes_cuota in range(1, 13):
                                        if mes_cuota == 1:
                                            # Enero: SIEMPRE último día del mes (31/01)
                                            fecha_vencimiento = date(ano_declaracion, 1, 31)
                                        else:
                                            # Resto de meses (febrero a diciembre): día 11 de cada mes
                                            fecha_vencimiento = date(ano_declaracion, mes_cuota, 11)
                                        
                                        # Verificar si ya existe antes de crear/actualizar
                                        mes_str = str(mes_cuota).zfill(2)
                                        existe_antes = TransaccionesIcs.objects.filter(
                                            empresa=empresa_get, rtm=rtm_valor, expe=expe_get,
                                            ano=ano_declaracion, mes=mes_str, rubro=rubro
                                        ).exists()
                                        
                                        nueva_trans = crear_o_actualizar_transaccion(
                                            rtm_valor, expe_get, empresa_get,
                                            negocio_obj.id if negocio_obj else 0,
                                            nodecla_str, rubro, cod_tarifa, valor_tasa,
                                            ano_declaracion, mes_cuota, fecha_vencimiento
                                        )
                                        transacciones_creadas.append({
                                            'id': nueva_trans.id,
                                            'rubro': rubro,
                                            'tarifa': cod_tarifa,
                                            'valor': float(valor_tasa),
                                            'vencimiento': fecha_vencimiento.strftime('%Y-%m-%d'),
                                            'ano': ano_declaracion,
                                            'mes': mes_cuota,
                                            'accion': 'actualizada' if existe_antes else 'creada'
                                        })
                                        print(f"[GENERAR TRANSACCIONES] Mensual Normal - Cuota {mes_cuota}/12: Fecha={fecha_vencimiento}, Monto={nueva_trans.monto}, Acción={'Actualizada' if existe_antes else 'Creada'}")
                                
                                elif tipo_declaracion == 2:  # Tipo Apertura (2 = Apertura según tabla declara)
                                    # Cuotas desde el mes de ingreso de la declaración hasta el mes 12 (diciembre)
                                    # Enero: fecha último día del mes (31/01), resto: fecha 11/mes
                                    for mes_cuota in range(mes_declaracion, 13):
                                        if mes_cuota == 1:
                                            fecha_vencimiento = date(ano_declaracion, 1, 31)
                                        else:
                                            fecha_vencimiento = date(ano_declaracion, mes_cuota, 11)
                                        
                                        # Verificar si ya existe antes de crear/actualizar
                                        mes_str = str(mes_cuota).zfill(2)
                                        existe_antes = TransaccionesIcs.objects.filter(
                                            empresa=empresa_get, rtm=rtm_valor, expe=expe_get,
                                            ano=ano_declaracion, mes=mes_str, rubro=rubro
                                        ).exists()
                                        
                                        nueva_trans = crear_o_actualizar_transaccion(
                                            rtm_valor, expe_get, empresa_get,
                                            negocio_obj.id if negocio_obj else 0,
                                            nodecla_str, rubro, cod_tarifa, valor_tasa,
                                            ano_declaracion, mes_cuota, fecha_vencimiento
                                        )
                                        transacciones_creadas.append({
                                            'id': nueva_trans.id,
                                            'rubro': rubro,
                                            'tarifa': cod_tarifa,
                                            'valor': float(valor_tasa),
                                            'vencimiento': fecha_vencimiento.strftime('%Y-%m-%d'),
                                            'ano': ano_declaracion,
                                            'mes': mes_cuota,
                                            'accion': 'actualizada' if existe_antes else 'creada'
                                        })
                                        print(f"[GENERAR TRANSACCIONES] Mensual Apertura - Cuota {mes_cuota}: Fecha={fecha_vencimiento}, Monto={nueva_trans.monto}, Acción={'Actualizada' if existe_antes else 'Creada'}")
                            
                            else:
                                # Frecuencia desconocida - usar lógica por defecto
                                print(f"[GENERAR TRANSACCIONES] ⚠️ Frecuencia desconocida: '{frecuencia}', usando fecha por defecto")
                                fecha_vencimiento = date(ano_declaracion, mes_declaracion if mes_declaracion > 0 else 1, 11)
                                
                                # Verificar si ya existe antes de crear/actualizar
                                mes_str = str(mes_declaracion).zfill(2) if mes_declaracion else '01'
                                existe_antes = TransaccionesIcs.objects.filter(
                                    empresa=empresa_get, rtm=rtm_valor, expe=expe_get,
                                    ano=ano_declaracion, mes=mes_str, rubro=rubro
                                ).exists()
                                
                                nueva_trans = crear_o_actualizar_transaccion(
                                    rtm_valor, expe_get, empresa_get,
                                    negocio_obj.id if negocio_obj else 0,
                                    nodecla_str, rubro, cod_tarifa, valor_tasa,
                                    ano_declaracion, mes_declaracion, fecha_vencimiento
                                )
                                transacciones_creadas.append({
                                    'id': nueva_trans.id,
                                    'rubro': rubro,
                                    'tarifa': cod_tarifa,
                                    'valor': float(valor_tasa),
                                    'vencimiento': fecha_vencimiento.strftime('%Y-%m-%d'),
                                    'ano': ano_declaracion,
                                    'mes': mes_declaracion,
                                    'accion': 'actualizada' if existe_antes else 'creada'
                                })
                        
                        # Contar transacciones creadas y actualizadas
                        for t in transacciones_creadas:
                            if t.get('accion') == 'actualizada':
                                transacciones_actualizadas += 1
                            else:
                                transacciones_nuevas += 1
                        
                        # Construir mensaje resumen
                        mensaje_resumen = f"Se procesaron {len(transacciones_creadas)} transacciones: {transacciones_nuevas} nuevas, {transacciones_actualizadas} actualizadas"
                        
                        if transacciones_eliminadas > 0:
                            mensaje_resumen = f"Se eliminaron {transacciones_eliminadas} transacción(es) existente(s) del año {ano_declaracion}. " + mensaje_resumen
                        
                        return JsonResponse({
                            'exito': True,
                            'mensaje': mensaje_resumen,
                            'transacciones_procesadas': len(transacciones_creadas),
                            'transacciones_nuevas': transacciones_nuevas,
                            'transacciones_actualizadas': transacciones_actualizadas,
                            'transacciones_eliminadas': transacciones_eliminadas,
                            'detalle': transacciones_creadas,
                            'impuesto': 0
                        })
                    except Exception as e:
                        import traceback
                        error_detalle = traceback.format_exc()
                        print(f"[GENERAR TRANSACCIONES] Error: {error_detalle}")
                        return JsonResponse({
                            'exito': False,
                            'mensaje': f'Error al generar transacciones: {str(e)}',
                            'impuesto': 0
                        })
                else:
                    print(f"[DEBUG] Acción AJAX no reconocida: {accion}")
                    return JsonResponse({
                        'exito': False,
                        'mensaje': f'Acción no reconocida: {accion}',
                        'impuesto': 0
                    })
            except Exception as e:
                print(f"[DEBUG] Error en procesamiento AJAX: {str(e)}")
                return JsonResponse({
                    'exito': False,
                    'mensaje': f'Error: {str(e)}',
                    'impuesto': 0
                })
        
        # Si no es AJAX, continuar con el procesamiento normal
        print("[DEBUG] Procesando como petición POST normal")
        # Aquí se puede agregar lógica para peticiones POST normales si es necesario
    
    # Inicializar variables
    negocio = None
    declaraciones = []
    tarifas_ics = []
    tasas_decla = []
    declaras = []
    declaracion_existente = None
    anos_disponibles = []
    mensaje = ""
    exito = True
    # municipio_codigo se inicializó arriba, usar empresa como referencia
    municipio_codigo = empresa
    
    # Resolver período por defecto (solo calendario / URL; NO cargar última declaración automáticamente).
    # - Si viene `ano` o `mes` en la URL, respetarlos.
    # - Si faltan, usar año y mes calendario actuales.
    from datetime import datetime as _dt

    mes_vigente = request.GET.get('mes', '')

    if not ano:
        ano = str(_dt.now().year)
        print(f"   - INFO Año por defecto (calendario, sin ?ano= en URL): {ano}")

    if not mes_vigente:
        mes_vigente = str(_dt.now().month).zfill(2)
        print(f"   - INFO Mes por defecto (calendario, sin ?mes= en URL): {mes_vigente}")
    
    # Buscar negocio si se proporcionan RTM y EXPE
    if rtm and expe:
        try:
            from tributario.models import Negocio
            negocio = Negocio.objects.get(rtm=rtm, expe=expe)
            print(f"   - Negocio encontrado: {negocio.nombrenego}")
            print(f"   - ID Negocio: {negocio.id}")
            # Si no se proporcionó empresa en la URL, usar la del negocio
            if not request.GET.get('empresa'):
                if hasattr(negocio, 'empresa') and negocio.empresa:
                    empresa = negocio.empresa
                    print(f"   - INFO Usando empresa del negocio: {empresa}")
        except Exception as e:
            print(f"   - Error buscando negocio: {e}")
            negocio = None
    
    # Obtener años disponibles para el combobox (desde tabla `anos`)
    # Reglas:
    # - Mostrar años desde el inicio de operaciones hasta el año actual.
    # - Si no existe un "año inicio" en la BD, usar:
    #   1) variable de entorno SIMAFI_ANO_INICIO_OPERACIONES (si existe),
    #   2) el mínimo año existente en tabla `anos`,
    #   3) el mínimo año con declaraciones en el municipio,
    #   4) o el año actual.
    # - Crear automáticamente en `anos` los años faltantes en ese rango.
    try:
        from django.db.models import Min
        from datetime import datetime
        import os
        from tributario.models import DeclaracionVolumen, Anos

        ano_actual_int = datetime.now().year

        ano_inicio = None

        # 1) Override por variable de entorno
        env_inicio = (os.environ.get('SIMAFI_ANO_INICIO_OPERACIONES') or '').strip()
        if env_inicio.isdigit():
            ano_inicio = int(env_inicio)

        # 2) Si hay años ya cargados en tabla `anos`, usar el mínimo
        if ano_inicio is None:
            min_ano_tabla = Anos.objects.aggregate(m=Min('ano')).get('m')
            try:
                if min_ano_tabla is not None:
                    ano_inicio = int(min_ano_tabla)
            except Exception:
                ano_inicio = None

        # 3) Año inicio por municipio: mínimo año registrado en declaraciones
        if ano_inicio is None:
            min_ano_decl = DeclaracionVolumen.objects.filter(empresa=empresa).aggregate(m=Min('ano')).get('m')
            try:
                if min_ano_decl is not None:
                    ano_inicio = int(min_ano_decl)
            except Exception:
                ano_inicio = None

        if ano_inicio is None:
            ano_inicio = ano_actual_int

        # Crear años faltantes en tabla `anos`
        for y in range(ano_inicio, ano_actual_int + 1):
            Anos.objects.get_or_create(ano=y)

        anos_disponibles = Anos.objects.filter(ano__gte=ano_inicio, ano__lte=ano_actual_int).order_by('-ano')
        print(f"   - OK Años disponibles (anos): {[str(int(a.ano)) for a in anos_disponibles]}")
    except Exception as e:
        print(f"   - ERROR Error obteniendo años desde anos: {e}")
        # Fallback: si falla, al menos mostrar el año actual
        anos_disponibles = []
    
    # Buscar declaración existente si se proporcionan todos los parámetros (empresa, rtm, expe, ano)
    if empresa and rtm and expe and ano:
        try:
            # Buscar declaración específica según empresa, rtm, expe y ano
            # La clave única es (empresa, rtm, expe, ano)
            declaracion_existente = DeclaracionVolumen.objects.filter(
                empresa=empresa,
                rtm=rtm, 
                expe=expe, 
                ano=ano
            ).first()
            
            if declaracion_existente:
                print(f"   - OK Declaración existente encontrada: {declaracion_existente.nodecla}")
                print(f"   - OK Empresa: {declaracion_existente.empresa}, RTM: {declaracion_existente.rtm}, EXPE: {declaracion_existente.expe}, Año: {declaracion_existente.ano}")
                print(f"   - OK Mes de la declaración: {declaracion_existente.mes}")
                # Usar el mes de la declaración existente
                mes_vigente = str(declaracion_existente.mes).zfill(2) if declaracion_existente.mes else mes_vigente
            else:
                print(f"   - INFO No existe declaración para empresa={empresa}, rtm={rtm}, expe={expe}, ano={ano}")
                # Si no existe declaración, usar mes vigente
                if not mes_vigente:
                    mes_vigente = str(_dt.now().month).zfill(2)
                print(f"   - INFO Usando mes vigente para nueva declaración: {mes_vigente}")
        except Exception as e:
            print(f"   - ERROR Error buscando declaración existente: {e}")
            declaracion_existente = None
    elif rtm and expe and ano:
        # Si no se proporciona empresa, intentar buscar sin ella (compatibilidad hacia atrás)
        try:
            declaracion_existente = DeclaracionVolumen.objects.filter(
                rtm=rtm, 
                expe=expe, 
                ano=ano
            ).first()
            
            if declaracion_existente:
                print(f"   - OK Declaración existente encontrada (sin empresa): {declaracion_existente.nodecla}")
                print(f"   - OK Mes de la declaración: {declaracion_existente.mes}")
                mes_vigente = str(declaracion_existente.mes).zfill(2) if declaracion_existente.mes else mes_vigente
            else:
                print(f"   - INFO No existe declaración para rtm={rtm}, expe={expe}, ano={ano}")
        except Exception as e:
            print(f"   - ERROR Error buscando declaración existente: {e}")
            declaracion_existente = None
    
    # Buscar declaraciones existentes para el grid
    if rtm and expe:
        try:
            from tributario.models import DeclaracionVolumen, TarifasICS, TasasDecla, Rubro
            from django.db.models import Prefetch
            
            declaraciones = DeclaracionVolumen.objects.filter(rtm=rtm, expe=expe).order_by('-ano', '-mes')
            tarifas_ics = TarifasICS.objects.filter(rtm=rtm, expe=expe).order_by('-rtm', '-expe')
            
            # Cargar tasas_decla con JOIN a rubros para obtener descripciones
            tasas_decla = TasasDecla.objects.filter(rtm=rtm, expe=expe).select_related().order_by('-rtm', '-expe')
            
            # Agregar descripciones de rubros a cada tasa
            for tasa in tasas_decla:
                try:
                    rubro = Rubro.objects.filter(empresa=tasa.empresa, codigo=tasa.rubro).first()
                    if rubro:
                        tasa.rubro_descripcion = rubro.descripcion
                    else:
                        tasa.rubro_descripcion = f"Rubro {tasa.rubro} no encontrado"
                except Exception as e:
                    tasa.rubro_descripcion = f"Error: {str(e)}"
            
            declaras = DeclaracionVolumen.objects.filter(rtm=rtm, expe=expe).order_by('-ano', '-mes')
            print(f"   - OK Declaraciones encontradas: {declaraciones.count()}")
            print(f"   - OK Tarifas ICS encontradas: {tarifas_ics.count()}")
            print(f"   - OK Tasas Decla encontradas: {tasas_decla.count()}")
            print(f"   - OK Declaras encontradas: {declaras.count()}")
            mensaje = f"Datos cargados correctamente para RTM: {rtm}, EXPE: {expe}"
            exito = True
        except Exception as e:
            print(f"   - ERROR Error al cargar declaraciones: {e}")
            mensaje = f"Error al cargar datos: {str(e)}"
            exito = False
            declaraciones = []
            tarifas_ics = []
            tasas_decla = []
            declaras = []
    
    # Crear formulario con datos iniciales
    try:
        from tributario_app.forms import DeclaracionVolumenForm
        initial_data = {}
        if negocio:
               initial_data = {
                   'rtm': rtm, 
                   'expe': expe,
                   'idneg': negocio.id,
                   'empresa': empresa or negocio.empresa or municipio_codigo
               }
        
        # Crear formulario con la instancia si existe, o con initial_data si no
        if declaracion_existente:
            # Usar la instancia para que el formulario calcule valor_base correctamente
            form = DeclaracionVolumenForm(instance=declaracion_existente)
            print(f"[CARGA AUTO] Formulario creado con instancia: {declaracion_existente}")
        else:
            # Si no hay declaración existente, usar año y mes vigente
            initial_data.update({
                'ano': ano,
                'mes': mes_vigente
            })
            print(f"   - INFO Configurando año vigente: {ano}, mes vigente: {mes_vigente}")
            form = DeclaracionVolumenForm(initial=initial_data)
            print(f"[CARGA AUTO] Formulario creado con initial_data")
    except Exception as e:
        print(f"   - ERROR Error creando formulario: {e}")
        form = None
    
    # Context para el template
    context = {
        'form': form,
        'negocio': negocio,
        'declaraciones': declaraciones,
        'tarifas_ics': tarifas_ics,
        'tasas_decla': tasas_decla,
        'declaras': declaras,
        'declaracion_existente': declaracion_existente,
        'anos_disponibles': anos_disponibles,
        'mensaje': mensaje,
        'exito': exito,
        'municipio_codigo': municipio_codigo,
        'modulo': 'Tributario',
        'descripcion': 'Declaración de Volumen de Ventas',
        'rtm': rtm,
        'expe': expe,
        'empresa': empresa,
        'ano': ano,
        'mes_vigente': mes_vigente,
        'numero_declaracion': declaracion_existente.nodecla if declaracion_existente else None
    }
    
    print(f"   - OK Renderizando template declaracion_volumen.html")
    return render(request, 'declaracion_volumen.html', context)

@csrf_exempt
def buscar_declaracion_existente(request):
    """API endpoint para búsqueda de declaraciones existentes"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    # Obtener parámetros (empresa + rtm + expe + ano definen la consulta principal)
    rtm = request.GET.get('rtm', '')
    expe = request.GET.get('expe', '')
    ano = request.GET.get('ano', '')
    mes = request.GET.get('mes', '')
    empresa = (request.GET.get('empresa') or '').strip()
    if not empresa:
        empresa = (request.session.get('empresa') or '').strip()
    
    print(f"BUSQUEDA API - empresa={empresa}, RTM: {rtm}, EXPE: {expe}, ANO: {ano}, MES: {mes}")
    
    if not rtm or not expe:
        return JsonResponse({'error': 'RTM y EXPE son requeridos'}, status=400)
    
    try:
        from tributario.models import DeclaracionVolumen
        
        # Construir filtros
        filtros = {'rtm': rtm, 'expe': expe}
        if empresa:
            filtros['empresa'] = empresa
        if ano:
            filtros['ano'] = ano
        if mes:
            filtros['mes'] = mes
        
        # Buscar declaraciones
        declaraciones = DeclaracionVolumen.objects.filter(**filtros).order_by('-ano', '-mes')
        
        print(f"   - Declaraciones encontradas: {declaraciones.count()}")
        
        # Preparar datos para respuesta
        declaraciones_data = []
        for decl in declaraciones:
            declaraciones_data.append({
                'id': decl.id,
                'nodecla': decl.nodecla,
                'empresa': decl.empresa,
                'idneg': decl.idneg,
                'rtm': decl.rtm,
                'expe': decl.expe,
                'ano': decl.ano,
                'tipo': decl.tipo,
                'mes': decl.mes,
                'ventai': float(decl.ventai) if decl.ventai else 0,
                'ventac': float(decl.ventac) if decl.ventac else 0,
                'ventas': float(decl.ventas) if decl.ventas else 0,
                'valorexcento': float(decl.valorexcento) if decl.valorexcento else 0,
                'controlado': float(decl.controlado) if decl.controlado else 0,
                'unidad': float(decl.unidad) if decl.unidad else 0,
                'factor': float(decl.factor) if decl.factor else 0,
                'multadecla': float(decl.multadecla) if decl.multadecla else 0,
                'impuesto': float(decl.impuesto) if decl.impuesto else 0,
                'ajuste': float(decl.ajuste) if decl.ajuste else 0,
                'fechssys': decl.fechssys.strftime('%d/%m/%Y %H:%M:%S') if decl.fechssys else None,
                'usuario': decl.usuario
            })
        
        # Declaración a mostrar en el formulario:
        # - Si hay año y mes: exacta.
        # - Si solo hay año: la más reciente por mes dentro de ese año (comportamiento al cambiar el combo año).
        q_negocio = {'rtm': rtm, 'expe': expe}
        if empresa:
            q_negocio['empresa'] = empresa

        declaracion_especifica = None
        if ano and mes:
            declaracion_especifica = DeclaracionVolumen.objects.filter(
                **q_negocio, ano=ano, mes=mes
            ).first()

            if declaracion_especifica:
                print(f"   - Declaracion especifica encontrada: {declaracion_especifica.nodecla}")
            else:
                print(f"   - No existe declaracion para {ano}-{mes}")
        elif ano:
            declaracion_especifica = (
                DeclaracionVolumen.objects.filter(**q_negocio, ano=ano)
                .order_by('-mes')
                .first()
            )
            if declaracion_especifica:
                print(
                    f"   - Declaracion por año (mes más reciente en {ano}): "
                    f"{declaracion_especifica.nodecla} mes={declaracion_especifica.mes}"
                )
            else:
                print(f"   - No existe declaracion para el año {ano}")
        
        return JsonResponse({
            'success': True,
            'declaraciones': declaraciones_data,
            'declaracion_especifica': {
                'id': declaracion_especifica.id,
                'nodecla': declaracion_especifica.nodecla,
                'empresa': declaracion_especifica.empresa,
                'idneg': declaracion_especifica.idneg,
                'rtm': declaracion_especifica.rtm,
                'expe': declaracion_especifica.expe,
                'ano': declaracion_especifica.ano,
                'tipo': declaracion_especifica.tipo,
                'mes': declaracion_especifica.mes,
                'ventai': float(declaracion_especifica.ventai) if declaracion_especifica.ventai else 0,
                'ventac': float(declaracion_especifica.ventac) if declaracion_especifica.ventac else 0,
                'ventas': float(declaracion_especifica.ventas) if declaracion_especifica.ventas else 0,
                'valorexcento': float(declaracion_especifica.valorexcento) if declaracion_especifica.valorexcento else 0,
                'controlado': float(declaracion_especifica.controlado) if declaracion_especifica.controlado else 0,
                'unidad': float(declaracion_especifica.unidad) if declaracion_especifica.unidad else 0,
                'factor': float(declaracion_especifica.factor) if declaracion_especifica.factor else 0,
                'multadecla': float(declaracion_especifica.multadecla) if declaracion_especifica.multadecla else 0,
                'impuesto': float(declaracion_especifica.impuesto) if declaracion_especifica.impuesto else 0,
                'ajuste': float(declaracion_especifica.ajuste) if declaracion_especifica.ajuste else 0,
                'fechssys': declaracion_especifica.fechssys.strftime('%d/%m/%Y %H:%M:%S') if declaracion_especifica.fechssys else None,
                'usuario': declaracion_especifica.usuario
            } if declaracion_especifica else None,
            'total_encontradas': len(declaraciones_data)
        })
        
    except Exception as e:
        print(f"   - Error en busqueda API: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
def configurar_tasas_negocio(request):
    """Vista para configurar las tasas de un negocio específico"""
    # Obtener el municipio del usuario desde la sesión
    empresa = request.session.get('empresa', '0301')
    
    # Obtener datos del negocio desde la URL o POST
    negocio_id = request.GET.get('negocio_id') or request.POST.get('negocio_id')
    rtm = request.GET.get('rtm') or request.POST.get('rtm')
    expe = request.GET.get('expe') or request.POST.get('expe')
    
    # Variables para el contexto
    negocio = None
    tarifas_ics = []
    mensaje = None
    exito = False
    
    # Buscar el negocio
    print(f"[DEBUG CONFIG TASAS] empresa={empresa}, rtm={rtm}, expe={expe}")
    if negocio_id or (rtm and expe):
        try:
            from tributario.models import Negocio
            if negocio_id:
                negocio = Negocio.objects.get(id=negocio_id)
                print(f"[DEBUG CONFIG TASAS] Negocio encontrado por ID: {negocio.nombrenego}")
            else:
                print(f"[DEBUG CONFIG TASAS] Buscando por empresa={empresa}, rtm={rtm}, expe={expe}")
                negocio = Negocio.objects.get(
                    empresa=empresa,
                    rtm=rtm,
                    expe=expe
                )
                print(f"[DEBUG CONFIG TASAS] Negocio encontrado: {negocio.nombrenego}")
        except Exception as e:
            print(f"[DEBUG CONFIG TASAS] Error al buscar negocio: {str(e)}")
            mensaje = f"Error al buscar negocio: {str(e)}"
            exito = False
    
    # Si no se encontró el negocio, mostrar error
    if not negocio:
        return render(request, 'configurar_tasas_negocio.html', {
            'negocio': None,
            'tarifas_ics': [],
            'mensaje': mensaje or "Debe especificar un negocio válido",
            'exito': False,
            'empresa': empresa,
            'modulo': 'Tributario',
            'descripcion': 'Configurar Tasas del Negocio'
        })
    
    # Manejar solicitudes POST
    if request.method == 'POST':
        try:
            from tributario_app.forms import TarifasICSForm
            from tributario.models import TarifasICS, Rubro, Tarifas
            
            accion = request.POST.get('accion')
            
            if accion == 'agregar_tarifa':
                # Verificar si es actualización o inserción
                tarifa_id = request.POST.get('tarifa_id', '').strip()
                
                # Obtener datos del formulario
                rubro = request.POST.get('rubro', '').strip()
                tarifa_rubro = request.POST.get('cod_tarifa', '').strip()
                valor_personalizado = request.POST.get('valor_personalizado', '').strip()
                cuenta = request.POST.get('cuenta', '').strip()
                cuentarez = request.POST.get('cuentarez', '').strip()
                
                print(f"[DEBUG TARIFA] tarifa_id={tarifa_id}, rubro={rubro}, cod_tarifa={tarifa_rubro}, valor={valor_personalizado}, cuenta={cuenta}, cuentarez={cuentarez}")
                
                if not rubro or not tarifa_rubro:
                    mensaje = "Rubro y Código de Tarifa son requeridos"
                    exito = False
                else:
                    try:
                        # Usar el valor personalizado o 0
                        valor_final = float(valor_personalizado) if valor_personalizado else 0.00
                        
                        if tarifa_id:
                            # ACTUALIZAR registro existente
                            print(f"[DEBUG TARIFA] Actualizando tarifa ID {tarifa_id}")
                            try:
                                tarifa_ics = TarifasICS.objects.get(id=tarifa_id, idneg=negocio.id)
                                tarifa_ics.rubro = rubro
                                tarifa_ics.cod_tarifa = tarifa_rubro
                                tarifa_ics.valor = valor_final
                                tarifa_ics.cuenta = cuenta
                                tarifa_ics.cuentarez = cuentarez
                                tarifa_ics.save()
                                
                                mensaje = "Tarifa actualizada exitosamente"
                                exito = True
                                print(f"[DEBUG TARIFA] Tarifa actualizada exitosamente")
                            except TarifasICS.DoesNotExist:
                                mensaje = "Tarifa no encontrada para actualizar"
                                exito = False
                                print(f"[DEBUG TARIFA] Tarifa no encontrada")
                        else:
                            # INSERTAR nuevo registro
                            # Verificar si ya existe una tarifa para este rubro
                            tarifa_existente = TarifasICS.objects.filter(
                                empresa=empresa,
                                rtm=negocio.rtm,
                                expe=negocio.expe,
                                rubro=rubro
                            ).first()
                            
                            if tarifa_existente:
                                # Ya existe, actualizar en lugar de insertar
                                print(f"[DEBUG TARIFA] Ya existe tarifa para rubro {rubro}, actualizando...")
                                tarifa_existente.cod_tarifa = tarifa_rubro
                                tarifa_existente.valor = valor_final
                                tarifa_existente.cuenta = cuenta
                                tarifa_existente.cuentarez = cuentarez
                                tarifa_existente.save()
                                
                                mensaje = "Tarifa actualizada exitosamente (registro existente)"
                                exito = True
                            else:
                                # No existe, crear nueva
                                print(f"[DEBUG TARIFA] Creando nueva tarifa para rubro {rubro}")
                                tarifa_ics = TarifasICS(
                                    empresa=empresa,
                                    idneg=negocio.id,
                                    rtm=negocio.rtm,
                                    expe=negocio.expe,
                                    rubro=rubro,
                                    cod_tarifa=tarifa_rubro,
                                    valor=valor_final,
                                    cuenta=cuenta,
                                    cuentarez=cuentarez
                                )
                                tarifa_ics.save()
                                
                                mensaje = "Tarifa agregada exitosamente"
                                exito = True
                                print(f"[DEBUG TARIFA] Tarifa creada exitosamente")
                        
                    except ValueError as e:
                        mensaje = f"Error en el valor numérico: {str(e)}"
                        exito = False
                        print(f"[DEBUG TARIFA] Error de valor: {str(e)}")
                    except Exception as e:
                        mensaje = f"Error al procesar tarifa: {str(e)}"
                        exito = False
                        print(f"[DEBUG TARIFA] Error general: {str(e)}")
                    
            elif accion == 'eliminar_tarifa':
                # Eliminar tarifa ICS
                tarifa_id = request.POST.get('tarifa_id')
                if tarifa_id:
                    try:
                        tarifa_ics = TarifasICS.objects.get(id=tarifa_id, idneg=negocio.id)
                        tarifa_ics.delete()
                        mensaje = "Tarifa eliminada exitosamente"
                        exito = True
                    except TarifasICS.DoesNotExist:
                        mensaje = "Tarifa no encontrada"
                        exito = False
                else:
                    mensaje = "ID de tarifa requerido"
                    exito = False
                    
            elif accion == 'actualizar_valor':
                # Actualizar valor de tarifa ICS
                tarifa_id = request.POST.get('tarifa_id')
                nuevo_valor = request.POST.get('valor')
                if tarifa_id and nuevo_valor:
                    try:
                        tarifa_ics = TarifasICS.objects.get(id=tarifa_id, idneg=negocio.id)
                        tarifa_ics.valor = nuevo_valor
                        tarifa_ics.save()
                        mensaje = "Valor actualizado exitosamente"
                        exito = True
                    except TarifasICS.DoesNotExist:
                        mensaje = "Tarifa no encontrada"
                        exito = False
                else:
                    mensaje = "ID de tarifa y valor requeridos"
                    exito = False
                    
        except Exception as e:
            mensaje = f"Error en el servidor: {str(e)}"
            exito = False
    
    # Obtener tarifas ICS del negocio
    try:
        from tributario.models import TarifasICS
        tarifas_ics = TarifasICS.objects.filter(idneg=negocio.id).order_by('cod_tarifa')
    except Exception as e:
        tarifas_ics = []
        if not mensaje:
            mensaje = f"Error al cargar tarifas: {str(e)}"
            exito = False
    
    # Crear formulario inicial
    try:
        from tributario_app.forms import TarifasICSForm
        form = TarifasICSForm(initial={
            'idneg': negocio.id,
            'rtm': negocio.rtm,
            'expe': negocio.expe
        })
    except Exception as e:
        form = None
        if not mensaje:
            mensaje = f"Error al crear formulario: {str(e)}"
            exito = False
    
    return render(request, 'configurar_tasas_negocio.html', {
        'negocio': negocio,
        'tarifas_ics': tarifas_ics,
        'form': form,
        'mensaje': mensaje,
        'exito': exito,
        'empresa': empresa,
        'modulo': 'Tributario',
        'descripcion': 'Configurar Tasas del Negocio'
    })

@csrf_exempt
def obtener_tarifas_rubro(request):
    """Vista AJAX para obtener las tarifas de un rubro específico"""
    if request.method != 'POST':
        return JsonResponse({
            'exito': False,
            'mensaje': 'Método no permitido'
        })
    
    try:
        rubro_codigo = request.POST.get('rubro', '').strip()
        empresa = request.session.get('empresa', '0301')
        
        if not rubro_codigo:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Código de rubro requerido'
            })
        
        from tributario.models import Tarifas
        
        # Obtener año vigente (año actual)
        from datetime import datetime
        ano_vigente = datetime.now().year
        
        # Buscar tarifas del rubro para el año vigente y categoría 'C' (Comercial)
        tarifas = Tarifas.objects.filter(
            empresa=empresa,
            rubro=rubro_codigo,
            ano=ano_vigente,
            tipomodulo='C'  # Solo tarifas comerciales
        ).order_by('cod_tarifa')
        
        # Convertir a lista de diccionarios
        tarifas_data = []
        for tarifa in tarifas:
            tarifas_data.append({
                'cod_tarifa': tarifa.cod_tarifa,
                'descripcion': tarifa.descripcion,
                'valor': str(tarifa.valor),
                'frecuencia': tarifa.frecuencia,
                'tipo': tarifa.tipo
            })
        
        return JsonResponse({
            'exito': True,
            'tarifas': tarifas_data,
            'mensaje': f'Se encontraron {len(tarifas_data)} tarifas para el rubro {rubro_codigo}'
        })
        
    except Exception as e:
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al obtener tarifas: {str(e)}'
        })

@csrf_exempt
def obtener_datos_rubro(request):
    """Vista AJAX para obtener cuenta y cuentarez de un rubro específico"""
    if request.method != 'POST':
        return JsonResponse({
            'exito': False,
            'mensaje': 'Método no permitido'
        })
    
    try:
        rubro_codigo = request.POST.get('rubro', '').strip()
        empresa = request.session.get('empresa', '0301')
        
        if not rubro_codigo:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Código de rubro requerido'
            })
        
        from tributario.models import Rubro
        
        # Buscar el rubro
        try:
            rubro = Rubro.objects.get(empresa=empresa, codigo=rubro_codigo)
            
            return JsonResponse({
                'exito': True,
                'datos': {
                    'cuenta': rubro.cuenta or '',
                    'cuentarez': rubro.cuentarez or '',
                    'descripcion': rubro.descripcion or ''
                },
                'mensaje': f'Datos del rubro {rubro_codigo} obtenidos correctamente'
            })
        except Rubro.DoesNotExist:
            return JsonResponse({
                'exito': False,
                'mensaje': f'Rubro {rubro_codigo} no encontrado',
                'datos': {
                    'cuenta': '',
                    'cuentarez': '',
                    'descripcion': ''
                }
            })
        
    except Exception as e:
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al obtener datos del rubro: {str(e)}',
            'datos': {
                'cuenta': '',
                'cuentarez': '',
                'descripcion': ''
            }
        })

@csrf_exempt
def obtener_actividades_ajax(request):
    """Vista AJAX para obtener las actividades (cuentas contables)"""
    if request.method != 'POST':
        return JsonResponse({
            'exito': False,
            'mensaje': 'Método no permitido'
        })
    
    try:
        empresa = request.POST.get('empresa', '').strip()
        
        if not empresa:
            empresa = request.session.get('empresa', '0301')
        
        from tributario.models import Actividad
        
        # Obtener todas las actividades de la empresa
        actividades = Actividad.objects.filter(empresa=empresa).order_by('codigo')
        
        # Convertir a lista de diccionarios
        actividades_data = []
        for actividad in actividades:
            actividades_data.append({
                'codigo': actividad.codigo,
                'cuentarez': actividad.cuentarez or '',
                'descripcion': actividad.descripcion or ''
            })
        
        return JsonResponse({
            'exito': True,
            'actividades': actividades_data,
            'mensaje': f'Se encontraron {len(actividades_data)} actividades'
        })
        
    except Exception as e:
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al obtener actividades: {str(e)}'
        })

def simple_ajax(request):
    """Simple AJAX view for missing functions"""
    return JsonResponse({'success': False, 'error': 'Función no implementada'})

@csrf_exempt
def buscar_identificacion(request):
    """Vista AJAX para buscar identificación por DNI"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            identidad = data.get('identidad', '').strip()
            
            if not identidad:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'El número de identidad es obligatorio'
                })
            
            # Buscar en la tabla identificacion
            try:
                from tributario.models import Identificacion
                identificacion = Identificacion.objects.get(identidad=identidad)
                
                return JsonResponse({
                    'exito': True,
                    'identificacion': {
                        'identidad': identificacion.identidad,
                        'nombres': identificacion.nombres or '',
                        'apellidos': identificacion.apellidos or '',
                        'nombre_completo': f"{identificacion.nombres or ''} {identificacion.apellidos or ''}".strip()
                    }
                })
            except Identificacion.DoesNotExist:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Identidad no encontrada en la base de datos'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Datos JSON inválidos'
            })
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error en el servidor: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })


def cierre_anual(request):
    """Vista para cierre anual"""
    class NegocioSimulado:
        def __init__(self):
            self.empresa = '0301'
            self.rtm = ''
            self.expe = ''
            self.fecha_ini = None
            self.fecha_can = None
            self.identidad = ''
            self.rtnpersonal = ''
            self.comerciante = ''
            self.rtnnego = ''
            self.nombrenego = ''
            self.actividad = ''
            self.identidadrep = ''
            self.representante = ''
            self.estatus = 'A'
            self.catastral = ''
            self.cx = '0.0000000'
            self.cy = '0.0000000'
            self.direccion = ''
            self.telefono = ''
            self.celular = ''
            self.correo = ''
            self.pagweb = ''
            self.socios = ''
            self.comentario = ''
    
    negocio = NegocioSimulado()
    
    return render(request, 'cierre_anual.html', {
        'negocio': negocio,
        'empresa': '0301',
        'modulo': 'Tributario',
        'descripcion': 'Cierre Anual'
    })

def cargo_anual(request):
    """Vista para cargo anual"""
    class NegocioSimulado:
        def __init__(self):
            self.empresa = '0301'
            self.rtm = ''
            self.expe = ''
            self.fecha_ini = None
            self.fecha_can = None
            self.identidad = ''
            self.rtnpersonal = ''
            self.comerciante = ''
            self.rtnnego = ''
            self.nombrenego = ''
            self.actividad = ''
            self.identidadrep = ''
            self.representante = ''
            self.estatus = 'A'
            self.catastral = ''
            self.cx = '0.0000000'
            self.cy = '0.0000000'
            self.direccion = ''
            self.telefono = ''
            self.celular = ''
            self.correo = ''
            self.pagweb = ''
            self.socios = ''
            self.comentario = ''
    
    negocio = NegocioSimulado()
    
    return render(request, 'cargo_anual.html', {
        'negocio': negocio,
        'empresa': '0301',
        'modulo': 'Tributario',
        'descripcion': 'Cargo Anual'
    })

def recargos_moratorios(request):
    """Vista para recargos moratorios"""
    class NegocioSimulado:
        def __init__(self):
            self.empresa = '0301'
            self.rtm = ''
            self.expe = ''
            self.fecha_ini = None
            self.fecha_can = None
            self.identidad = ''
            self.rtnpersonal = ''
            self.comerciante = ''
            self.rtnnego = ''
            self.nombrenego = ''
            self.actividad = ''
            self.identidadrep = ''
            self.representante = ''
            self.estatus = 'A'
            self.catastral = ''
            self.cx = '0.0000000'
            self.cy = '0.0000000'
            self.direccion = ''
            self.telefono = ''
            self.celular = ''
            self.correo = ''
            self.pagweb = ''
            self.socios = ''
            self.comentario = ''
    
    negocio = NegocioSimulado()
    
    return render(request, 'recargos_moratorios.html', {
        'negocio': negocio,
        'empresa': '0301',
        'modulo': 'Tributario',
        'descripcion': 'Recargos Moratorios'
    })

def informes(request):
    """Vista para informes"""
    class NegocioSimulado:
        def __init__(self):
            self.empresa = '0301'
            self.rtm = ''
            self.expe = ''
            self.fecha_ini = None
            self.fecha_can = None
            self.identidad = ''
            self.rtnpersonal = ''
            self.comerciante = ''
            self.rtnnego = ''
            self.nombrenego = ''
            self.actividad = ''
            self.identidadrep = ''
            self.representante = ''
            self.estatus = 'A'
            self.catastral = ''
            self.cx = '0.0000000'
            self.cy = '0.0000000'
            self.direccion = ''
            self.telefono = ''
            self.celular = ''
            self.correo = ''
            self.pagweb = ''
            self.socios = ''
            self.comentario = ''
    
    negocio = NegocioSimulado()
    
    return render(request, 'informes.html', {
        'negocio': negocio,
        'empresa': '0301',
        'modulo': 'Tributario',
        'descripcion': 'Informes'
    })

def miscelaneos(request):
    """Vista para misceláneos"""
    # Obtener el municipio del usuario desde la sesión
    empresa = request.session.get('empresa', '0301')
    
    # Cargar oficinas disponibles
    oficinas = []
    try:
        from tributario.models import Oficina
        oficinas = Oficina.objects.filter(empresa=empresa).order_by('codigo')
    except Exception as e:
        print(f"Error al cargar oficinas: {e}")
        oficinas = []
    
    return render(request, 'miscelaneos.html', {
        'modulo': 'Tributario',
        'descripcion': 'Misceláneos',
        'empresa': empresa,
        'oficinas': oficinas
    })

def convenios_pagos(request):
    """Vista para convenios de pagos"""
    class NegocioSimulado:
        def __init__(self):
            self.empresa = '0301'
            self.rtm = ''
            self.expe = ''
            self.fecha_ini = None
            self.fecha_can = None
            self.identidad = ''
            self.rtnpersonal = ''
            self.comerciante = ''
            self.rtnnego = ''
            self.nombrenego = ''
            self.actividad = ''
            self.identidadrep = ''
            self.representante = ''
            self.estatus = 'A'
            self.catastral = ''
            self.cx = '0.0000000'
            self.cy = '0.0000000'
            self.direccion = ''
            self.telefono = ''
            self.celular = ''
            self.correo = ''
            self.pagweb = ''
            self.socios = ''
            self.comentario = ''
    
    negocio = NegocioSimulado()
    
    return render(request, 'convenios_pagos.html', {
        'negocio': negocio,
        'empresa': '0301',
        'modulo': 'Tributario',
        'descripcion': 'Convenios de Pagos'
    })

def actividad_crud(request):
    """Vista para CRUD de actividades"""
    # Obtener el municipio del usuario desde la sesión
    empresa = request.session.get('empresa', '0301')
    
    # Variables para el contexto
    actividades = []
    empresa_filtro = None
    mensaje = None
    exito = False
    
    if request.method == 'POST':
        try:
            from tributario.models import Actividad
            
            accion = request.POST.get('accion')
            empresa = request.POST.get('empresa', '')
            codigo = request.POST.get('codigo', '')
            descripcion = request.POST.get('descripcion', '')
            
            if accion == 'nuevo':
                # Limpiar campos para nuevo registro
                mensaje = 'Formulario preparado para nueva actividad'
                exito = True
                
            elif accion == 'guardar':
                if not empresa or not codigo or not descripcion:
                    mensaje = 'Todos los campos son obligatorios'
                    exito = False
                else:
                    # Verificar si ya existe la actividad
                    if Actividad.objects.filter(empresa=empresa, codigo=codigo).exists():
                        # Actualizar actividad existente
                        actividad = Actividad.objects.get(empresa=empresa, codigo=codigo)
                        actividad.descripcion = descripcion
                        actividad.save()
                        mensaje = f'Actividad {codigo} actualizada correctamente'
                        exito = True
                    else:
                        # Crear nueva actividad
                        Actividad.objects.create(
                            empresa=empresa,
                            codigo=codigo,
                            descripcion=descripcion
                        )
                        mensaje = f'Actividad {codigo} creada correctamente'
                        exito = True
                        
            elif accion == 'eliminar':
                codigo_eliminar = request.POST.get('codigo')
                empresa_eliminar = request.POST.get('empresa')
                
                if codigo_eliminar and empresa_eliminar:
                    try:
                        actividad = Actividad.objects.get(empresa=empresa_eliminar, codigo=codigo_eliminar)
                        actividad.delete()
                        mensaje = f'Actividad {codigo_eliminar} eliminada correctamente'
                        exito = True
                    except Actividad.DoesNotExist:
                        mensaje = 'Actividad no encontrada'
                        exito = False
                else:
                    mensaje = 'Código y empresa son obligatorios para eliminar'
                    exito = False
                    
        except Exception as e:
            mensaje = f'Error: {str(e)}'
            exito = False
    
    # Cargar actividades si hay un municipio seleccionado
    if empresa:
        try:
            from tributario.models import Actividad
            actividades = Actividad.objects.filter(empresa=empresa).order_by('codigo')
            empresa_filtro = empresa
        except Exception as e:
            print(f"Error al cargar actividades: {e}")
            actividades = []
    
    return render(request, 'actividad.html', {
        'empresa': empresa,
        'actividades': actividades,
        'empresa_filtro': empresa_filtro,
        'mensaje': mensaje,
        'exito': exito,
        'modulo': 'Tributario',
        'descripcion': 'Gestión de Actividades'
    })

def oficina_crud(request):
    """Vista para CRUD de oficinas"""
    # Obtener el municipio del usuario desde la sesión
    empresa = request.session.get('empresa', '0301')
    
    # Variables para el contexto
    oficinas = []
    empresa_filtro = None
    mensaje = None
    exito = False
    
    if request.method == 'POST':
        try:
            from tributario.models import Oficina
            
            accion = request.POST.get('accion')
            empresa = request.POST.get('empresa', '')
            codigo = request.POST.get('codigo', '')
            descripcion = request.POST.get('descripcion', '')
            
            if accion == 'nuevo':
                # Limpiar campos para nuevo registro
                mensaje = 'Formulario preparado para nueva oficina'
                exito = True
                
            elif accion == 'guardar':
                if not empresa or not codigo or not descripcion:
                    mensaje = 'Todos los campos son obligatorios'
                    exito = False
                else:
                    # Verificar si ya existe la oficina
                    if Oficina.objects.filter(empresa=empresa, codigo=codigo).exists():
                        # Actualizar oficina existente
                        oficina = Oficina.objects.get(empresa=empresa, codigo=codigo)
                        oficina.descripcion = descripcion
                        oficina.save()
                        mensaje = f'Oficina {codigo} actualizada correctamente'
                        exito = True
                    else:
                        # Crear nueva oficina
                        Oficina.objects.create(
                            empresa=empresa,
                            codigo=codigo,
                            descripcion=descripcion
                        )
                        mensaje = f'Oficina {codigo} creada correctamente'
                        exito = True
                        
            elif accion == 'eliminar':
                codigo_eliminar = request.POST.get('codigo')
                empresa_eliminar = request.POST.get('empresa')
                
                if codigo_eliminar and empresa_eliminar:
                    try:
                        oficina = Oficina.objects.get(empresa=empresa_eliminar, codigo=codigo_eliminar)
                        oficina.delete()
                        mensaje = f'Oficina {codigo_eliminar} eliminada correctamente'
                        exito = True
                    except Oficina.DoesNotExist:
                        mensaje = 'Oficina no encontrada'
                        exito = False
                else:
                    mensaje = 'Código y empresa son obligatorios para eliminar'
                    exito = False
                    
        except Exception as e:
            mensaje = f'Error: {str(e)}'
            exito = False
    
    # Cargar oficinas si hay un municipio seleccionado
    if empresa:
        try:
            from tributario.models import Oficina
            oficinas = Oficina.objects.filter(empresa=empresa).order_by('codigo')
            empresa_filtro = empresa
        except Exception as e:
            print(f"Error al cargar oficinas: {e}")
            oficinas = []
    
    return render(request, 'oficina.html', {
        'empresa': empresa,
        'oficinas': oficinas,
        'empresa_filtro': empresa_filtro,
        'mensaje': mensaje,
        'exito': exito,
        'modulo': 'Tributario',
        'descripcion': 'Gestión de Oficinas'
    })

def rubros_crud(request):
    """Vista para CRUD de rubros"""
    # Obtener el municipio del usuario desde la sesión
    empresa = request.session.get('empresa', '0301')
    
    # Variables para el contexto
    rubros = []
    actividades = []
    empresa_filtro = None
    mensaje = None
    exito = False
    
    if request.method == 'POST':
        try:
            from tributario.models import Rubro
            from tributario.models import Actividad
            
            action = request.POST.get('action')
            empresa = request.POST.get('empresa', '')
            codigo = request.POST.get('codigo', '')
            descripcion = request.POST.get('descripcion', '')
            tipo = request.POST.get('tipo', '')
            cuenta = request.POST.get('cuenta', '')
            cuntarez = request.POST.get('cuntarez', '')
            
            if action == 'nuevo':
                # Limpiar campos para nuevo registro
                mensaje = 'Formulario preparado para nuevo rubro'
                exito = True
                
            elif action == 'guardar':
                if not empresa or not codigo or not descripcion or not tipo or not cuenta or not cuntarez:
                    mensaje = 'Todos los campos son obligatorios'
                    exito = False
                else:
                    # Verificar si ya existe el rubro
                    if Rubro.objects.filter(empresa=empresa, codigo=codigo).exists():
                        # Actualizar rubro existente
                        rubro = Rubro.objects.get(empresa=empresa, codigo=codigo)
                        rubro.descripcion = descripcion
                        rubro.tipo = tipo
                        rubro.cuenta = cuenta
                        rubro.cuntarez = cuntarez
                        rubro.save()
                        mensaje = f'Rubro {codigo} actualizado correctamente'
                        exito = True
                    else:
                        # Crear nuevo rubro
                        Rubro.objects.create(
                            empresa=empresa,
                            codigo=codigo,
                            descripcion=descripcion,
                            tipo=tipo,
                            cuenta=cuenta,
                            cuntarez=cuntarez
                        )
                        mensaje = f'Rubro {codigo} creado correctamente'
                        exito = True
                        
            elif action == 'eliminar':
                codigo_eliminar = request.POST.get('codigo')
                empresa_eliminar = request.POST.get('empresa')
                
                if codigo_eliminar and empresa_eliminar:
                    try:
                        rubro = Rubro.objects.get(empresa=empresa_eliminar, codigo=codigo_eliminar)
                        rubro.delete()
                        mensaje = f'Rubro {codigo_eliminar} eliminado correctamente'
                        exito = True
                    except Rubro.DoesNotExist:
                        mensaje = 'Rubro no encontrado'
                        exito = False
                else:
                    mensaje = 'Código y empresa son obligatorios para eliminar'
                    exito = False
                    
        except Exception as e:
            mensaje = f'Error: {str(e)}'
            exito = False
    
    # Cargar rubros y actividades si hay un municipio seleccionado
    if empresa:
        try:
            from tributario.models import Rubro
            from tributario.models import Actividad
            rubros = Rubro.objects.filter(empresa=empresa).order_by('codigo')
            actividades = Actividad.objects.filter(empresa=empresa).order_by('codigo')
            empresa_filtro = empresa
        except Exception as e:
            print(f"Error al cargar rubros/actividades: {e}")
            rubros = []
            actividades = []
    
    # Crear un contexto básico para el formulario
    form_context = {
        'empresa': empresa,
        'codigo': '',
        'descripcion': '',
        'tipo': '',
        'cuenta': '',
        'cuntarez': ''
    }
    
    return render(request, 'formulario_rubros.html', {
        'empresa': empresa,
        'rubros': rubros,
        'actividades': actividades,
        'empresa_filtro': empresa_filtro,
        'mensaje': mensaje,
        'exito': exito,
        'form': form_context,  # Agregar contexto del formulario
        'modulo': 'Tributario',
        'descripcion': 'Gestión de Rubros'
    })

# Vista duplicada comentada para evitar conflictos - se usa la de views.py
# def tarifas_crud(request):
#     """Vista para CRUD de tarifas"""
    empresa = request.session.get('empresa', '0301')
    codigo_rubro = request.GET.get('codigo_rubro', '')
    ano_filtro = request.GET.get('ano', '')  # Obtener año del filtro
    
    # Imports necesarios al inicio
    from tributario.models import Tarifas
    # from tributario_app.forms import TarifasForm
    
    # Variables para el contexto
    tarifas = []
    empresa_filtro = None
    mensaje = None
    exito = False
    
    if request.method == 'POST':
        try:
            accion = request.POST.get('accion')
            
            if accion == 'eliminar':
                # Manejar eliminación de tarifa
                empresa_eliminar = request.POST.get('empresa')
                cod_tarifa_eliminar = request.POST.get('cod_tarifa')
                rubro_eliminar = request.POST.get('rubro')
                ano_eliminar = request.POST.get('ano')
                
                if empresa_eliminar and cod_tarifa_eliminar and rubro_eliminar and ano_eliminar:
                    try:
                        tarifa = Tarifas.objects.get(
                            empresa=empresa_eliminar,
                            cod_tarifa=cod_tarifa_eliminar,
                            rubro=rubro_eliminar,
                            ano=ano_eliminar
                        )
                        descripcion_eliminada = tarifa.descripcion
                        tarifa.delete()
                        mensaje = f'Tarifa {cod_tarifa_eliminar} ({descripcion_eliminada}) eliminada correctamente'
                        exito = True
                    except Tarifas.DoesNotExist:
                        mensaje = 'Tarifa no encontrada'
                        exito = False
                else:
                    mensaje = 'Empresa, código de tarifa, rubro y año son obligatorios para eliminar'
                    exito = False
                
                # Preparar formulario después de la eliminación
                # Mantener el rubro de la tarifa eliminada
                initial_data = {'empresa': empresa}
                if rubro_eliminar:
                    initial_data['rubro'] = rubro_eliminar
                elif codigo_rubro:
                    initial_data['rubro'] = codigo_rubro
                form = TarifasForm(initial=initial_data)
                
                # Actualizar los filtros para mantener la consulta filtrada
                if rubro_eliminar:
                    codigo_rubro = rubro_eliminar
                if ano_eliminar:
                    ano_filtro = ano_eliminar
            else:
                # Manejar guardado/actualización de tarifa
                form = TarifasForm(request.POST)
                if form.is_valid():
                    try:
                        # El modelo se encarga de la lógica de actualización vs creación
                        tarifa = form.save(commit=False)
                        tarifa.empresa = empresa
                        tarifa.rubro = request.POST.get('rubro', '').strip() or codigo_rubro
                        tarifa.save()
                        
                        # Determinar si fue creación o actualización
                        if tarifa.pk:
                            mensaje = f"Tarifa {tarifa.cod_tarifa} (Año {tarifa.ano}) procesada exitosamente."
                            exito = True
                        else:
                            mensaje = f"Error al procesar la tarifa."
                            exito = False
                        
                        # Limpiar formulario después de cualquier operación
                        initial_data = {'empresa': empresa}
                        if codigo_rubro:
                            initial_data['rubro'] = codigo_rubro
                        form = TarifasForm(initial=initial_data)
                    except Exception as e:
                        mensaje = f"Error al procesar la tarifa: {str(e)}"
                        exito = False
                else:
                    mensaje = f"Error en el formulario: {form.errors}"
                    exito = False
        except Exception as e:
            mensaje = f"Error al procesar la tarifa: {str(e)}"
            exito = False
    else:
        # Preparar formulario inicial
        initial_data = {'empresa': empresa}
        if codigo_rubro:
            initial_data['rubro'] = codigo_rubro
        form = TarifasForm(initial=initial_data)
    
    # Obtener tarifas del municipio, filtrando por rubro y año si se especifica
    if empresa:
        try:
            tarifas_query = Tarifas.objects.filter(empresa=empresa)
            if codigo_rubro:
                tarifas_query = tarifas_query.filter(rubro=codigo_rubro)
            if ano_filtro:
                tarifas_query = tarifas_query.filter(ano=ano_filtro)
            tarifas = tarifas_query.order_by('rubro', 'ano', 'cod_tarifa')
            empresa_filtro = empresa
        except Exception as e:
            print(f"Error al cargar tarifas: {e}")
            tarifas = []
    
    return render(request, 'formulario_tarifas.html', {
        'form': form,
        'tarifas': tarifas,
        'empresa_filtro': empresa_filtro,
        'ano_filtro': ano_filtro,
        'mensaje': mensaje,
        'exito': exito,
        'modulo': 'Tributario',
        'descripcion': 'Gestión de Tarifas'
    })

def plan_arbitrio_crud(request):
    """Vista para CRUD de plan de arbitrios con herencia de parámetros y filtrado del grid"""
    from tributario.models import PlanArbitrio, Rubro
    from tributario.models import Tarifas
    # from tributario_app.forms import PlanArbitrioForm
    
    # Obtener parámetros de herencia desde la URL
    # Priorizar el parámetro GET sobre la sesión cuando esté presente
    empresa = request.GET.get('empresa', '') or request.session.get('municipio_id', '')
    
    # Debug: Mostrar valores antes del procesamiento
    print(f"🔍 DEBUG - Valores antes del procesamiento:")
    print(f"   Session municipio_id: '{request.session.get('municipio_id', '')}'")
    print(f"   GET empresa: '{request.GET.get('empresa', '')}'")
    print(f"   Municipio código inicial: '{empresa}'")
    print(f"   Prioridad: GET empresa sobre Session municipio_id")
    
    # Limpiar y formatear el código de municipio
    if empresa:
        empresa = str(empresa).strip()  # Eliminar espacios
        print(f"   Municipio después de strip: '{empresa}'")
        # Solo aplicar zfill si no tiene 4 dígitos ya
        if len(empresa) < 4:
            empresa = empresa.zfill(4)
            print(f"   Municipio después de zfill: '{empresa}'")
        else:
            print(f"   Municipio sin zfill (ya tiene 4 dígitos): '{empresa}'")
    
    rubro_codigo = request.GET.get('rubro', '')
    ano_heredado = request.GET.get('ano', '')
    cod_tarifa_heredado = request.GET.get('cod_tarifa', '')
    
    mensaje = ''
    exito = False
    
    print(f"🔍 Plan de Arbitrio - Parámetros heredados:")
    print(f"   Municipio (raw): {request.session.get('municipio_id', '')} o {request.GET.get('empresa', '')}")
    print(f"   Municipio (formateado): {empresa}")
    print(f"   Rubro: {rubro_codigo}")
    print(f"   Año: {ano_heredado}")
    print(f"   Código Tarifa: {cod_tarifa_heredado}")
    print(f"   URL completa: {request.get_full_path()}")
    print(f"   Método: {request.method}")
    
    # Obtener descripción del rubro si viene heredado
    descripcion_rubro = ''
    if rubro_codigo and empresa:
        try:
            rubro_obj = Rubro.objects.get(empresa=empresa, codigo=rubro_codigo)
            descripcion_rubro = rubro_obj.descripcion
            print(f"OK Rubro encontrado: {descripcion_rubro}")
        except Rubro.DoesNotExist:
            print(f"ERROR Rubro {rubro_codigo} no encontrado en municipio {empresa}")
    
    # Datos iniciales para el formulario con parámetros heredados
    initial_data = {
        'empresa': empresa,
        'rubro': rubro_codigo,
        'cod_tarifa': cod_tarifa_heredado,
        'ano': ano_heredado if ano_heredado else '',
    }
    
    if request.method == 'POST':
        accion = request.POST.get('action', 'guardar')
        print(f"🔍 Acción solicitada: {accion}")
        
        if accion == 'guardar':
            form = PlanArbitrioForm(request.POST, initial=initial_data)
            if form.is_valid():
                try:
                    # Verificar si ya existe un plan con los mismos parámetros únicos
                    empresa = form.cleaned_data['empresa']
                    rubro = form.cleaned_data['rubro']
                    cod_tarifa = form.cleaned_data['cod_tarifa']
                    ano = form.cleaned_data['ano']
                    codigo = form.cleaned_data['codigo']
                    
                    plan_existente = None
                    try:
                        plan_existente = PlanArbitrio.objects.get(
                            empresa=empresa,
                            rubro=rubro,
                            cod_tarifa=cod_tarifa,
                            ano=ano,
                            codigo=codigo
                        )
                        # Si existe, actualizar
                        for field, value in form.cleaned_data.items():
                            setattr(plan_existente, field, value)
                        plan_existente.save()
                        mensaje = f"Plan de arbitrio {codigo} actualizado exitosamente."
                        exito = True
                        print(f"OK Plan de arbitrio actualizado: {codigo}")
                    except PlanArbitrio.DoesNotExist:
                        # Si no existe, crear nuevo
                        plan_nuevo = form.save()
                        mensaje = f"Plan de arbitrio {plan_nuevo.codigo} creado exitosamente."
                        exito = True
                        print(f"OK Plan de arbitrio creado: {plan_nuevo.codigo}")
                        
                except Exception as e:
                    mensaje = f"Error al procesar el plan de arbitrio: {str(e)}"
                    exito = False
                    print(f"ERROR Error: {e}")
            else:
                # Manejar errores específicos del formulario
                if form.errors:
                    error_messages = []
                    plan_existente_data = None
                    
                    for field, errors in form.errors.items():
                        if field == '__all__':
                            # Errores generales (como duplicados)
                            for error in errors:
                                if 'Ya existe un plan de arbitrio' in str(error):
                                    # Si es un error de duplicado, cargar los datos existentes
                                    empresa = form.cleaned_data.get('empresa')
                                    rubro = form.cleaned_data.get('rubro')
                                    cod_tarifa = form.cleaned_data.get('cod_tarifa')
                                    ano = form.cleaned_data.get('ano')
                                    codigo = form.cleaned_data.get('codigo')
                                    
                                    if all([empresa, rubro, cod_tarifa, ano, codigo]):
                                        try:
                                            plan_existente = PlanArbitrio.objects.get(
                                                empresa=empresa,
                                                rubro=rubro,
                                                cod_tarifa=cod_tarifa,
                                                ano=ano,
                                                codigo=codigo
                                            )
                                            plan_existente_data = {
                                                'empresa': plan_existente.empresa,
                                                'rubro': plan_existente.rubro,
                                                'cod_tarifa': plan_existente.cod_tarifa,
                                                'ano': plan_existente.ano,
                                                'codigo': plan_existente.codigo,
                                                'descripcion': plan_existente.descripcion,
                                                'minimo': plan_existente.minimo,
                                                'maximo': plan_existente.maximo,
                                                'valor': plan_existente.valor,
                                            }
                                            error_messages.append(f"⚠️ Registro existente encontrado. Los datos han sido cargados para su modificación.")
                                        except PlanArbitrio.DoesNotExist:
                                            error_messages.append(f"⚠️ {error}")
                                    else:
                                        error_messages.append(f"⚠️ {error}")
                                else:
                                    error_messages.append(f"ERROR {error}")
                        else:
                            # Errores de campos específicos
                            for error in errors:
                                error_messages.append(f"ERROR {field}: {error}")
                    
                    mensaje = "Se encontraron los siguientes errores:<br>" + "<br>".join(error_messages)
                    
                    # Si se encontró un plan existente, crear nuevo formulario con esos datos
                    if plan_existente_data:
                        form = PlanArbitrioForm(initial=plan_existente_data)
                        mensaje += "<br><br><strong>💡 Los datos del registro existente han sido cargados. Puede modificarlos y guardar para actualizar el registro.</strong>"
                else:
                    mensaje = "Error en el formulario. Verifique los datos ingresados."
                exito = False
                print(f"ERROR Errores en formulario: {form.errors}")
        
        elif accion == 'eliminar':
            empresa = request.POST.get('empresa')
            rubro = request.POST.get('rubro')
            cod_tarifa = request.POST.get('cod_tarifa')
            ano = request.POST.get('ano')
            codigo = request.POST.get('codigo')
            
            if empresa and rubro and cod_tarifa and ano and codigo:
                try:
                    plan = PlanArbitrio.objects.get(
                        empresa=empresa,
                        rubro=rubro,
                        cod_tarifa=cod_tarifa,
                        ano=ano,
                        codigo=codigo
                    )
                    descripcion_eliminada = plan.descripcion
                    plan.delete()
                    mensaje = f'Plan de arbitrio {codigo} ({descripcion_eliminada}) eliminado correctamente'
                    exito = True
                    print(f"OK Plan eliminado: {codigo}")
                except PlanArbitrio.DoesNotExist:
                    mensaje = 'Plan de arbitrio no encontrado'
                    exito = False
                    print(f"ERROR Plan no encontrado: {codigo}")
            else:
                mensaje = 'Datos insuficientes para eliminar el plan de arbitrio'
                exito = False
        
        elif accion == 'nuevo':
            # Limpiar formulario pero mantener parámetros heredados
            initial_data = {
                'empresa': empresa,
                'rubro': rubro_codigo,
                'cod_tarifa': cod_tarifa_heredado,
                'ano': ano_heredado if ano_heredado else '',
            }
            mensaje = 'Formulario preparado para nuevo plan de arbitrio'
            exito = True
    
    # Crear formulario con datos iniciales
    form = PlanArbitrioForm(initial=initial_data)
    
    # Filtrar grid de planes de arbitrio según parámetros heredados
    planes_query = PlanArbitrio.objects.filter(empresa=empresa)
    
    # Aplicar filtros adicionales si están presentes
    if rubro_codigo:
        planes_query = planes_query.filter(rubro=rubro_codigo)
        print(f"🔍 Filtrando por rubro: {rubro_codigo}")
    
    if ano_heredado:
        planes_query = planes_query.filter(ano=ano_heredado)
        print(f"🔍 Filtrando por año: {ano_heredado}")
    
    if cod_tarifa_heredado:
        planes_query = planes_query.filter(cod_tarifa=cod_tarifa_heredado)
        print(f"🔍 Filtrando por código de tarifa: {cod_tarifa_heredado}")
    
    # Ordenar planes por Año, Rubro, Código de Tarifa, Categoría y Código
    planes_arbitrio = planes_query.order_by('ano', 'rubro', 'cod_tarifa', 'tipocat', 'codigo')
    
    print(f"📊 Planes encontrados: {planes_arbitrio.count()}")
    
    context = {
        'form': form,
        'modulo': 'Tributario',
        'descripcion': 'Gestión de Plan de Arbitrios',
        'empresa_filtro': empresa,
        'rubro_filtro': rubro_codigo,
        'ano_filtro': ano_heredado,
        'cod_tarifa_filtro': cod_tarifa_heredado,
        'planes_arbitrio': planes_arbitrio,
        'mensaje': mensaje,
        'exito': exito,
    }
    
    return render(request, 'formulario_plan_arbitrio.html', context)

def plan_arbitrio(request):
    """Vista para plan arbitrio"""
    class NegocioSimulado:
        def __init__(self):
            self.empresa = '0301'
            self.rtm = ''
            self.expe = ''
            self.fecha_ini = None
            self.fecha_can = None
            self.identidad = ''
            self.rtnpersonal = ''
            self.comerciante = ''
            self.rtnnego = ''
            self.nombrenego = ''
            self.actividad = ''
            self.identidadrep = ''
            self.representante = ''
            self.estatus = 'A'
            self.catastral = ''
            self.cx = '0.0000000'
            self.cy = '0.0000000'
            self.direccion = ''
            self.telefono = ''
            self.celular = ''
            self.correo = ''
            self.pagweb = ''
            self.socios = ''
            self.comentario = ''
    
    negocio = NegocioSimulado()
    
    return render(request, 'plan_arbitrio.html', {
        'negocio': negocio,
        'empresa': '0301',
        'modulo': 'Tributario',
        'descripcion': 'Plan Arbitrio'
    })

def validar_plan_arbitrio(request):
    """
    Vista AJAX para validar si existe un plan de arbitrio según la clave única planarbitio_idx1
    También permite búsqueda solo por código para búsqueda interactiva
    """
    if request.method != 'POST':
        return JsonResponse({
            'exito': False,
            'mensaje': 'Método no permitido'
        })
    
    try:
        import json
        from django.http import JsonResponse
        from tributario.models import PlanArbitrio
        
        # Obtener datos del request
        data = json.loads(request.body)
        empresa = data.get('empresa', '').strip()
        rubro = data.get('rubro', '').strip()
        cod_tarifa = data.get('cod_tarifa', '').strip()
        ano = data.get('ano', '').strip()
        codigo = data.get('codigo', '').strip()
        
        # Si solo se proporciona código, buscar por código únicamente
        if codigo and not all([empresa, rubro, cod_tarifa, ano]):
            print(f"🔍 Búsqueda interactiva por código: {codigo}")
            try:
                # Buscar por código únicamente
                plan_existente = PlanArbitrio.objects.filter(codigo=codigo).first()
                
                if plan_existente:
                    return JsonResponse({
                        'exito': True,
                        'existe': True,
                        'concepto': {
                            'id': plan_existente.id,
                            'empresa': plan_existente.empresa,
                            'rubro': plan_existente.rubro,
                            'cod_tarifa': plan_existente.cod_tarifa,
                            'tipocat': str(plan_existente.tipocat) if hasattr(plan_existente, 'tipocat') and plan_existente.tipocat is not None else '0',
                            'ano': str(plan_existente.ano),
                            'codigo': plan_existente.codigo,
                            'descripcion': plan_existente.descripcion,
                            'minimo': str(plan_existente.minimo),
                            'maximo': str(plan_existente.maximo),
                            'valor': str(plan_existente.valor)
                        },
                        'mensaje': f'Plan de arbitrio encontrado por código: {codigo}'
                    })
                else:
                    return JsonResponse({
                        'exito': True,
                        'existe': False,
                        'mensaje': f'No se encontró ningún plan de arbitrio con el código: {codigo}'
                    })
                    
            except Exception as e:
                return JsonResponse({
                    'exito': False,
                    'mensaje': f'Error en búsqueda por código: {str(e)}'
                })
        
        # Validar que todos los campos estén presentes para validación completa
        if not all([empresa, rubro, cod_tarifa, ano, codigo]):
            return JsonResponse({
                'exito': False,
                'mensaje': 'Todos los campos de la clave única son requeridos'
            })
        
        # Buscar el plan de arbitrio existente según la clave única planarbitio_idx1
        try:
            plan_existente = PlanArbitrio.objects.get(
                empresa=empresa,
                rubro=rubro,
                cod_tarifa=cod_tarifa,
                ano=ano,
                codigo=codigo
            )
            
            # Si existe, retornar los datos
            return JsonResponse({
                'exito': True,
                'existe': True,
                'concepto': {
                    'id': plan_existente.id,
                    'empresa': plan_existente.empresa,
                    'rubro': plan_existente.rubro,
                    'cod_tarifa': plan_existente.cod_tarifa,
                    'tipocat': str(plan_existente.tipocat) if hasattr(plan_existente, 'tipocat') and plan_existente.tipocat is not None else '0',
                    'ano': str(plan_existente.ano),
                    'codigo': plan_existente.codigo,
                    'descripcion': plan_existente.descripcion,
                    'minimo': str(plan_existente.minimo),
                    'maximo': str(plan_existente.maximo),
                    'valor': str(plan_existente.valor)
                },
                'mensaje': 'Plan de arbitrio existente encontrado'
            })
            
        except PlanArbitrio.DoesNotExist:
            # No existe, retornar que no se encontró
            return JsonResponse({
                'exito': True,
                'existe': False,
                'mensaje': 'No se encontró un plan de arbitrio con esos criterios'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'exito': False,
            'mensaje': 'Error al procesar los datos JSON'
        })
    except Exception as e:
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error interno: {str(e)}'
        })

