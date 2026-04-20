from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def buscar_actividad_ajax(request):
    """Vista AJAX para buscar actividad por empresa y código"""
    if request.method == 'GET':
        try:
            empresa = request.GET.get('empresa', '').strip()
            codigo = request.GET.get('codigo', '').strip()
            
            print(f"🔍 Buscando actividad: empresa={empresa}, codigo={codigo}")
            
            if not empresa or not codigo:
                print("❌ Empresa o código vacíos")
                return JsonResponse({
                    'exito': False,
                    'descripcion': '',
                    'mensaje': 'Empresa y código son obligatorios'
                })
            
            # Buscar en la tabla actividad
            try:
                from tributario.models import Actividad
                actividad = Actividad.objects.get(empresa=empresa, codigo=codigo)
                
                print(f"✅ Actividad encontrada: {actividad.descripcion}")
                
                return JsonResponse({
                    'exito': True,
                    'descripcion': actividad.descripcion,
                    'mensaje': 'Actividad encontrada'
                })
            except Actividad.DoesNotExist:
                print(f"❌ Actividad no encontrada: empresa={empresa}, codigo={codigo}")
                return JsonResponse({
                    'exito': False,
                    'descripcion': '',
                    'mensaje': 'Actividad no encontrada'
                })
                
        except Exception as e:
            print(f"❌ Error en búsqueda AJAX: {e}")
            return JsonResponse({
                'exito': False,
                'descripcion': '',
                'mensaje': f'Error en el servidor: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'descripcion': '',
        'mensaje': 'Método no permitido'
    })

@csrf_exempt
def buscar_oficina_ajax(request):
    """Vista AJAX para buscar oficina por empresa y código"""
    if request.method == 'GET':
        try:
            empresa = request.GET.get('empresa', '').strip()
            codigo = request.GET.get('codigo', '').strip()
            
            print(f"🔍 Buscando oficina: empresa={empresa}, codigo={codigo}")
            
            if not empresa or not codigo:
                print("❌ Empresa o código vacíos")
                return JsonResponse({
                    'exito': False,
                    'descripcion': '',
                    'mensaje': 'Empresa y código son obligatorios'
                })
            
            # Buscar en la tabla oficina
            try:
                from tributario.models import Oficina
                oficina = Oficina.objects.get(empresa=empresa, codigo=codigo)
                
                print(f"✅ Oficina encontrada: {oficina.descripcion}")
                
                return JsonResponse({
                    'exito': True,
                    'descripcion': oficina.descripcion,
                    'mensaje': 'Oficina encontrada'
                })
            except Oficina.DoesNotExist:
                print(f"❌ Oficina no encontrada: empresa={empresa}, codigo={codigo}")
                return JsonResponse({
                    'exito': False,
                    'descripcion': '',
                    'mensaje': 'Oficina no encontrada'
                })
                
        except Exception as e:
            print(f"❌ Error en búsqueda AJAX: {e}")
            return JsonResponse({
                'exito': False,
                'descripcion': '',
                'mensaje': f'Error en el servidor: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'descripcion': '',
        'mensaje': 'Método no permitido'
    })

@csrf_exempt
def cargar_actividades_ajax(request):
    """Vista AJAX para cargar actividades por empresa (municipio)"""
    if request.method == 'GET':
        try:
            empresa = request.GET.get('empresa', '').strip()
            
            print(f"🔍 Cargando actividades para empresa: {empresa}")
            
            if not empresa:
                print("❌ Empresa vacía")
                return JsonResponse({
                    'exito': False,
                    'actividades': [],
                    'mensaje': 'Empresa es obligatoria'
                })
            
            # Cargar actividades de la tabla actividad filtradas por empresa
            try:
                from tributario.models import Actividad
                actividades = Actividad.objects.filter(empresa=empresa).order_by('codigo')
                
                # Convertir a lista de diccionarios para JSON
                actividades_list = []
                for actividad in actividades:
                    actividades_list.append({
                        'codigo': actividad.codigo,
                        'descripcion': actividad.descripcion
                    })
                
                print(f"✅ Actividades cargadas: {len(actividades_list)} encontradas")
                
                return JsonResponse({
                    'exito': True,
                    'actividades': actividades_list,
                    'mensaje': f'{len(actividades_list)} actividades cargadas'
                })
            except Exception as e:
                print(f"❌ Error al cargar actividades: {e}")
                return JsonResponse({
                    'exito': False,
                    'actividades': [],
                    'mensaje': f'Error al cargar actividades: {str(e)}'
                })
                
        except Exception as e:
            print(f"❌ Error en carga AJAX: {e}")
            return JsonResponse({
                'exito': False,
                'actividades': [],
                'mensaje': f'Error en el servidor: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'actividades': [],
        'mensaje': 'Método no permitido'
    })

@csrf_exempt
def calcular_tasas_plan_arbitrio(request):
    """
    Vista AJAX TEMPORAL para calcular tasas según el plan de arbitrios.
    
    Proceso:
    1. Seleccionar tasas de tasasdecla según empresa, rtm, expe, ano, rubro, tipota
    2. Validación: Si tipota = "F":
       - Buscar valor en tabla tarifas por empresa, rubro, ano
       - Grabar valor en tasasdecla según empresa, rtm, expe, rubro, ano
    3. Validación: Si tipota = "V":
       - Buscar en planarbitrio por empresa, rubro, ano
       - Ordenar por codigo
       - Validar si existe un registro donde valorbase > minimo y valorbase < maximo
       - Tomar el valor del registro encontrado
       - Grabar en tasasdecla según empresa, rtm, expe, rubro, ano
    """
    if request.method == 'POST':
        try:
            from tributario.models import TasasDecla, Tarifas, PlanArbitrio, DeclaracionVolumen
            from decimal import Decimal
            
            data = request.POST if request.POST else {}
            empresa = data.get('empresa', '').strip()
            rtm = data.get('rtm', '').strip()
            expe = data.get('expe', '').strip()
            ano = data.get('ano', '').strip()
            rubro = data.get('rubro', '').strip()
            
            print(f"🔧 [CALCULAR TASAS] Parámetros: empresa={empresa}, rtm={rtm}, expe={expe}, ano={ano}, rubro={rubro}")
            
            # Validar parámetros mínimos
            if not empresa or not rtm or not expe:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Empresa, RTM y Expediente son obligatorios',
                    'tasas_actualizadas': []
                })
            
            tasas_actualizadas = []
            tasas_error = []
            
            # Obtener valorbase de la declaración (suma de todas las ventas)
            valorbase = Decimal('0.00')
            try:
                # Primero intentar obtener año y rubro de la declaración si no vienen
                if not ano or not rubro:
                    declara = DeclaracionVolumen.objects.filter(empresa=empresa, rtm=rtm, expe=expe).order_by('-ano', '-mes').first()
                    if declara:
                        ano = ano or str(int(declara.ano))
                        valorbase = (declara.ventai or Decimal('0.00')) + \
                                    (declara.ventac or Decimal('0.00')) + \
                                    (declara.ventas or Decimal('0.00')) + \
                                    (declara.valorexcento or Decimal('0.00')) + \
                                    (declara.controlado or Decimal('0.00'))
            except Exception as e:
                print(f"⚠️  [ADVERTENCIA] No se pudo obtener valorbase: {e}")
                valorbase = Decimal('0.00')
            
            print(f"💰 [VALORBASE] Valorbase calculado: {valorbase}")
            
            # Si no se proporcionó rubro, obtener todas las tasas del negocio
            if rubro:
                tasas_decla = TasasDecla.objects.filter(
                    empresa=empresa,
                    rtm=rtm,
                    expe=expe,
                    ano=Decimal(ano) if ano else None
                ).filter(rubro=rubro)
            else:
                # Sin rubro específico, procesar todas las tasas
                tasas_decla = TasasDecla.objects.filter(
                    empresa=empresa,
                    rtm=rtm,
                    expe=expe
                )
            
            # Si no se proporcionó año, usar todas las tasas
            if ano:
                tasas_decla = tasas_decla.filter(ano=Decimal(ano))
            
            total_tasas = tasas_decla.count()
            print(f"📊 [TASAS ENCONTRADAS] Total: {total_tasas}")
            
            for tasa in tasas_decla:
                try:
                    rubro_tasa = tasa.rubro or ''
                    ano_tasa = tasa.ano
                    
                    print(f"\n🔄 [PROCESANDO TASA] Rubro: {rubro_tasa}, Año: {ano_tasa}, Tipo: {tasa.tipota}")
                    
                    # VALIDACIÓN TIPO TASA "F" (FIJA)
                    if tasa.tipota == 'F':
                        print(f"✅ [TASA FIJA] Buscando en tabla tarifas...")
                        
                        # Buscar valor en tabla tarifas
                        try:
                            tarifa = Tarifas.objects.filter(
                                empresa=empresa,
                                rubro=rubro_tasa,
                                ano=ano_tasa
                            ).first()
                            
                            if tarifa and tarifa.valor:
                                tasa.valor = tarifa.valor
                                tasa.save()
                                tasas_actualizadas.append({
                                    'rubro': rubro_tasa,
                                    'ano': str(int(ano_tasa)),
                                    'tipo': 'F',
                                    'valor_anterior': 'N/A',
                                    'valor_nuevo': str(tarifa.valor),
                                    'mensaje': f'Tasa fija actualizada desde tarifas'
                                })
                                print(f"✅ [ACTUALIZADA] Tasa Fija: {tarifa.valor}")
                            else:
                                tasas_error.append({
                                    'rubro': rubro_tasa,
                                    'ano': str(int(ano_tasa)),
                                    'tipo': 'F',
                                    'error': 'No se encontró tarifa correspondiente en tabla tarifas'
                                })
                                print(f"⚠️  [NO ENCONTRADA] Tarifa para rubro {rubro_tasa}")
                        except Exception as e:
                            print(f"❌ [ERROR FIJA] {str(e)}")
                            tasas_error.append({
                                'rubro': rubro_tasa,
                                'ano': str(int(ano_tasa)),
                                'tipo': 'F',
                                'error': f'Error al buscar tarifa: {str(e)}'
                            })
                    
                    # VALIDACIÓN TIPO TASA "V" (VARIABLE)
                    elif tasa.tipota == 'V':
                        print(f"✅ [TASA VARIABLE] Buscando en planarbitrio...")
                        
                        # Obtener valorbase para esta tasa específica
                        valorbase_actual = valorbase
                        
                        # Si no hay valorbase, intentar obtenerlo de otra forma
                        if valorbase_actual == Decimal('0.00'):
                            try:
                                valorbase_actual = tasa.valor  # Usar el valor actual como base
                            except:
                                valorbase_actual = Decimal('0.00')
                        
                        print(f"📊 [VALORBASE VARIABLE] {valorbase_actual} para rubro {rubro_tasa}")
                        
                        try:
                            # Buscar en planarbitrio según empresa, rubro, ano
                            # Ordenar por codigo y validar si valorbase > minimo y valorbase < maximo
                            plan = PlanArbitrio.objects.filter(
                                empresa=empresa,
                                rubro=rubro_tasa,
                                ano=ano_tasa
                            ).order_by('codigo').filter(
                                minimo__lt=valorbase_actual,
                                maximo__gte=valorbase_actual
                            ).first()
                            
                            if plan and plan.valor:
                                tasa.valor = plan.valor
                                tasa.save()
                                tasas_actualizadas.append({
                                    'rubro': rubro_tasa,
                                    'ano': str(int(ano_tasa)),
                                    'tipo': 'V',
                                    'valor_anterior': 'N/A',
                                    'valor_nuevo': str(plan.valor),
                                    'mensaje': f'Tasa variable actualizada según plan de arbitrio (rango {plan.minimo}-{plan.maximo})'
                                })
                                print(f"✅ [ACTUALIZADA] Tasa Variable: {plan.valor} (rango {plan.minimo}-{plan.maximo})")
                            else:
                                # Si no encuentra con > y <, buscar donde valorbase esté en el rango
                                plan = PlanArbitrio.objects.filter(
                                    empresa=empresa,
                                    rubro=rubro_tasa,
                                    ano=ano_tasa
                                ).order_by('codigo').filter(
                                    minimo__lte=valorbase_actual,
                                    maximo__gte=valorbase_actual
                                ).first()
                                
                                if plan and plan.valor:
                                    tasa.valor = plan.valor
                                    tasa.save()
                                    tasas_actualizadas.append({
                                        'rubro': rubro_tasa,
                                        'ano': str(int(ano_tasa)),
                                        'tipo': 'V',
                                        'valor_anterior': 'N/A',
                                        'valor_nuevo': str(plan.valor),
                                        'mensaje': f'Tasa variable actualizada según plan de arbitrio (rango {plan.minimo}-{plan.maximo})'
                                    })
                                    print(f"✅ [ACTUALIZADA] Tasa Variable: {plan.valor} (rango {plan.minimo}-{plan.maximo})")
                                else:
                                    tasas_error.append({
                                        'rubro': rubro_tasa,
                                        'ano': str(int(ano_tasa)),
                                        'tipo': 'V',
                                        'error': f'No se encontró plan de arbitrio con rango que incluya {valorbase_actual}'
                                    })
                                    print(f"⚠️  [NO ENCONTRADO] Plan para valorbase {valorbase_actual}")
                        except Exception as e:
                            print(f"❌ [ERROR VARIABLE] {str(e)}")
                            tasas_error.append({
                                'rubro': rubro_tasa,
                                'ano': str(int(ano_tasa)),
                                'tipo': 'V',
                                'error': f'Error al buscar plan de arbitrio: {str(e)}'
                            })
                    
                    else:
                        print(f"⚠️  [TIPO DESCONOCIDO] Tipo de tasa: {tasa.tipota}")
                        
                except Exception as e:
                    print(f"❌ [ERROR PROCESANDO] Error al procesar tasa: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    tasas_error.append({
                        'rubro': 'N/A',
                        'ano': 'N/A',
                        'tipo': 'N/A',
                        'error': f'Error al procesar tasa: {str(e)}'
                    })
            
            return JsonResponse({
                'exito': True,
                'mensaje': f'Proceso completado. {len(tasas_actualizadas)} tasas actualizadas, {len(tasas_error)} con errores',
                'tasas_actualizadas': tasas_actualizadas,
                'tasas_error': tasas_error,
                'total_procesadas': total_tasas
            })
            
        except Exception as e:
            print(f"❌ [ERROR GENERAL] Error en calcular_tasas_plan_arbitrio: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error al calcular tasas: {str(e)}',
                'tasas_actualizadas': [],
                'tasas_error': []
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido',
        'tasas_actualizadas': [],
        'tasas_error': []
    })
