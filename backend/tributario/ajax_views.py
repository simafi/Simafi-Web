from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def buscar_actividad_ajax(request):
    """Vista AJAX para buscar actividad por empresa y código (cuenta)"""
    # Importar el modelo al inicio para evitar problemas de scope
    try:
        from tributario.models import Actividad
    except ImportError:
        try:
            from tributario.models import Actividad
        except ImportError:
            return JsonResponse({
                'exito': False,
                'existe': False,
                'descripcion': '',
                'cuentarez': '',
                'cuentarec': '',
                'mensaje': 'Error: No se pudo importar el modelo Actividad'
            })
    
    if request.method == 'GET':
        try:
            # Obtener parámetros - aceptar tanto 'cuenta' como 'codigo' para compatibilidad
            empresa = request.GET.get('empresa', '').strip()
            cuenta = request.GET.get('cuenta', '').strip()  # Parámetro del formulario
            codigo = request.GET.get('codigo', '').strip()  # Parámetro alternativo
            
            # Usar 'cuenta' si está disponible, sino usar 'codigo'
            codigo_busqueda = cuenta if cuenta else codigo
            
            print(f"🔍 [DEBUG] Buscando actividad:")
            print(f"   - empresa: {repr(empresa)}")
            print(f"   - cuenta (parámetro): {repr(cuenta)}")
            print(f"   - codigo (parámetro): {repr(codigo)}")
            print(f"   - codigo_busqueda (usado): {repr(codigo_busqueda)}")
            print(f"   - request.GET completo: {dict(request.GET)}")
            
            if not empresa or not codigo_busqueda:
                print("❌ Empresa o código/cuenta vacíos")
                return JsonResponse({
                    'exito': False,
                    'existe': False,
                    'descripcion': '',
                    'cuentarez': '',
                    'cuentarec': '',
                    'mensaje': f'Empresa y cuenta son obligatorios (empresa={repr(empresa)}, cuenta={repr(codigo_busqueda)})'
                })
            
            # Normalizar empresa y codigo para la búsqueda (trim espacios)
            empresa_clean = empresa.strip()
            codigo_clean = codigo_busqueda.strip()
            
            print(f"🔍 Búsqueda normalizada: empresa='{empresa_clean}', codigo='{codigo_clean}'")
            
            # Para campos CHAR en MySQL, usar TRIM en SQL para comparar correctamente
            # Esto maneja el caso donde los campos CHAR tienen espacios de relleno
            from django.db.models.functions import Trim
            
            # Buscar actividad con TRIM para manejar espacios de relleno
            actividad = Actividad.objects.annotate(
                empresa_trim=Trim('empresa'),
                codigo_trim=Trim('codigo')
            ).filter(
                empresa_trim=empresa_clean,
                codigo_trim=codigo_clean
            ).first()
            
            # Si no se encuentra con TRIM, intentar búsqueda directa
            if not actividad:
                actividad = Actividad.objects.filter(
                    empresa=empresa_clean,
                    codigo=codigo_clean
                ).first()
            
            if actividad:
                # Obtener valores de manera segura, manejando None y strings vacíos
                descripcion_val = str(getattr(actividad, 'descripcion', '') or '').strip()
                cuentarez_val = str(getattr(actividad, 'cuentarez', '') or '').strip()
                cuentarec_val = str(getattr(actividad, 'cuentarec', '') or '').strip()
                
                print(f"✅ Actividad encontrada:")
                print(f"   - ID: {actividad.id}")
                print(f"   - descripcion: {repr(descripcion_val)}")
                print(f"   - cuentarez: {repr(cuentarez_val)}")
                print(f"   - cuentarec: {repr(cuentarec_val)}")
                
                return JsonResponse({
                    'exito': True,
                    'existe': True,
                    'descripcion': descripcion_val,
                    'cuentarez': cuentarez_val,
                    'cuentarec': cuentarec_val,
                    'mensaje': 'Actividad encontrada'
                })
            else:
                # Verificar si existe con otros criterios para debug
                try:
                    count_total = Actividad.objects.filter(empresa=empresa_clean).count()
                    print(f"❌ Actividad no encontrada. Total actividades para empresa '{empresa_clean}': {count_total}")
                    
                    # Listar algunos códigos disponibles para debug
                    codigos_ejemplo = Actividad.objects.filter(empresa=empresa_clean).values_list('codigo', flat=True)[:5]
                    print(f"📋 Códigos ejemplo para empresa '{empresa_clean}': {list(codigos_ejemplo)}")
                except Exception as debug_error:
                    print(f"⚠️ Error en debug: {debug_error}")
                
                return JsonResponse({
                    'exito': True,
                    'existe': False,
                    'descripcion': '',
                    'cuentarez': '',
                    'cuentarec': '',
                    'mensaje': 'Actividad no encontrada'
                })
                
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"❌ Error en búsqueda AJAX: {e}")
            print(f"📋 Traceback completo:\n{error_detail}")
            return JsonResponse({
                'exito': False,
                'existe': False,
                'descripcion': '',
                'cuentarez': '',
                'cuentarec': '',
                'mensaje': f'Error en el servidor: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'existe': False,
        'descripcion': '',
        'cuentarez': '',
        'cuentarec': '',
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

@csrf_exempt
def simular_cargar_tasas(request):
    """
    Vista AJAX para SIMULAR la carga de tasas desde tarifasics hacia tasasdecla.
    Este proceso ejecuta la misma lógica que se ejecuta al guardar la declaración,
    pero sin guardar la declaración misma.
    
    Parámetros requeridos:
    - empresa: Código de empresa
    - rtm: RTM del negocio
    - expe: Número de expediente
    - ano: Año de la declaración
    - valorbase: Valor base calculado (suma de ventas)
    """
    if request.method == 'POST':
        try:
            import json
            from tributario.models import TasasDecla, Tarifas, PlanArbitrio, Rubro, DeclaracionVolumen, AnoEmpreNu, TarifasICS
            from decimal import Decimal
            
            # Leer datos JSON si están disponibles
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                except:
                    data = {}
            else:
                data = request.POST if request.POST else {}
            
            empresa = data.get('empresa', '').strip()
            rtm = data.get('rtm', '').strip()
            expe = data.get('expe', '').strip()
            ano = data.get('ano', '').strip()
            valorbase_str = data.get('valorbase', '0')
            
            print("\n")
            print("="*100)
            print("[SIMULAR CARGAR TASAS] ⚡⚡⚡ INICIANDO SIMULACIÓN DE CARGA DE TASAS ⚡⚡⚡")
            print("="*100)
            print(f"[SIMULAR CARGAR TASAS] Parámetros recibidos:")
            print(f"   - Empresa: {empresa}")
            print(f"   - RTM: {rtm}")
            print(f"   - EXPE: {expe}")
            print(f"   - Año: {ano}")
            print(f"   - Valorbase: {valorbase_str}")
            print("="*100)
            print()
            
            # Validar parámetros
            if not empresa or not rtm or not expe or not ano:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Empresa, RTM, EXPE y Año son obligatorios',
                    'tasas_creadas': [],
                    'tasas_calculadas': [],
                    'tasas_error': []
                })
            
            # Convertir valorbase a Decimal
            try:
                valorbase = Decimal(str(valorbase_str).replace(',', ''))
            except:
                valorbase = Decimal('0.00')
            
            # Obtener idneg del negocio
            idneg = 0
            try:
                from tributario.models import Negocio
                negocio = Negocio.objects.filter(rtm=rtm, expe=expe).first()
                if negocio:
                    idneg = negocio.id or 0
            except:
                pass
            
            # Obtener nodecla si existe declaración
            nodecla = None
            try:
                declaracion_existente = DeclaracionVolumen.objects.filter(
                    empresa=empresa,
                    rtm=rtm,
                    expe=expe,
                    ano=Decimal(ano)
                ).first()
                if declaracion_existente and declaracion_existente.nodecla:
                    nodecla = declaracion_existente.nodecla
            except:
                pass
            
            # Si no hay nodecla, generar uno temporal para la simulación
            if not nodecla:
                try:
                    ano_emprenu, created = AnoEmpreNu.objects.get_or_create(
                        empresa=empresa,
                        ano=Decimal(ano),
                        defaults={'nudecla': Decimal('0')}
                    )
                    nudecla_temp = ano_emprenu.nudecla + Decimal('1')
                    nodecla = f"{str(int(nudecla_temp)).zfill(11)}-{ano}"
                except:
                    nodecla = f"00000000000-{ano}"
            
            print(f"[SIMULAR CARGAR TASAS] IDNeg obtenido: {idneg}")
            print(f"[SIMULAR CARGAR TASAS] Nodecla: {nodecla}")
            print(f"[SIMULAR CARGAR TASAS] Valorbase: {valorbase}")
            
            tasas_creadas = []
            tasas_calculadas = []
            tasas_error = []
            
            # PASO 1: Obtener rubros registrados en tarifasics
            print(f"\n[SIMULAR CARGAR TASAS] {'='*90}")
            print(f"[SIMULAR CARGAR TASAS] PASO 1: Buscar TarifasICS")
            print(f"[SIMULAR CARGAR TASAS] {'='*90}")
            
            rubros_registrados = []
            try:
                tarifas_ics = TarifasICS.objects.filter(
                    empresa=empresa,
                    rtm=rtm,
                    expe=expe
                )
                
                if not tarifas_ics.exists():
                    tarifas_ics = TarifasICS.objects.filter(
                        rtm=rtm,
                        expe=expe
                    )
                
                print(f"[SIMULAR CARGAR TASAS] 📊 TarifasICS encontradas: {tarifas_ics.count()}")
                
                for tarifa_ics in tarifas_ics:
                    rubro_cod = tarifa_ics.rubro or ''
                    if rubro_cod and rubro_cod.strip():
                        idneg_tarifa = tarifa_ics.idneg if (tarifa_ics.idneg and tarifa_ics.idneg > 0) else idneg
                        rubros_registrados.append({
                            'rubro': rubro_cod,
                            'cod_tarifa': tarifa_ics.cod_tarifa or '',
                            'valor_default': tarifa_ics.valor or Decimal('0.00'),
                            'cuenta': tarifa_ics.cuenta or '',
                            'cuentarez': tarifa_ics.cuentarez or '',
                            'idneg': idneg_tarifa
                        })
                        print(f"[SIMULAR CARGAR TASAS] ✅ Agregado: Rubro={rubro_cod}, Cod_Tarifa={tarifa_ics.cod_tarifa}, IDNeg={idneg_tarifa}")
                
                print(f"[SIMULAR CARGAR TASAS] 📊 TOTAL Rubros registrados: {len(rubros_registrados)}")
            except Exception as e:
                print(f"[SIMULAR CARGAR TASAS] ❌ Error obteniendo tarifasics: {e}")
                import traceback
                traceback.print_exc()
            
            # PASO 2: Crear tasas faltantes en TasasDecla
            print(f"\n[SIMULAR CARGAR TASAS] {'='*90}")
            print(f"[SIMULAR CARGAR TASAS] PASO 2: Crear tasas desde TarifasICS")
            print(f"[SIMULAR CARGAR TASAS] {'='*90}")
            
            ano_decimal = Decimal(str(ano))
            tasas_creadas_count = 0
            tasas_existentes_count = 0
            
            for rubro_info in rubros_registrados:
                rubro_cod = rubro_info['rubro']
                cod_tarifa = rubro_info['cod_tarifa']
                idneg_tasa = rubro_info.get('idneg', idneg) or idneg
                
                print(f"[SIMULAR CARGAR TASAS] 🔍 Verificando tasa: Rubro={rubro_cod}, Cod_Tarifa={cod_tarifa}")
                
                # Verificar si ya existe
                # IMPORTANTE: Usar select_for_update() para evitar condiciones de carrera si se ejecuta simultáneamente con otro proceso
                # Sin embargo, MyISAM no soporta row locking, así que usamos una verificación optimista
                tasa_existente = TasasDecla.objects.filter(
                    empresa=empresa,
                    rtm=rtm,
                    expe=expe,
                    ano=ano_decimal,
                    rubro=rubro_cod
                ).first()
                
                if tasa_existente:
                    print(f"[SIMULAR CARGAR TASAS] ⚠️ Tasa ya existe: ID={tasa_existente.id}, Rubro={rubro_cod}")
                    print(f"[SIMULAR CARGAR TASAS] ⚠️ Esta tasa probablemente ya fue procesada por el backend al guardar la declaración")
                    tasas_existentes_count += 1
                    # Actualizar idneg y cod_tarifa si es necesario (sin conflictos porque ya existe)
                    actualizado = False
                    if tasa_existente.idneg != idneg_tasa:
                        tasa_existente.idneg = idneg_tasa
                        actualizado = True
                    if tasa_existente.cod_tarifa != cod_tarifa and cod_tarifa:
                        tasa_existente.cod_tarifa = cod_tarifa
                        actualizado = True
                    if actualizado:
                        tasa_existente.save()
                        print(f"[SIMULAR CARGAR TASAS] ✅ Tasa existente actualizada: ID={tasa_existente.id}")
                    continue  # Saltar la creación ya que la tasa existe
                else:
                    try:
                        # Obtener información del rubro
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
                                    print(f"[SIMULAR CARGAR TASAS] 📅 Frecuencia obtenida desde Tarifas: {frecuencia} para empresa={empresa}, rubro={rubro_cod}")
                                
                                # Obtener tipo desde Tarifas (tarifas.tipo → tasasdecla.tipota)
                                if tarifa_info.tipo:
                                    tipota = tarifa_info.tipo.upper()
                                    print(f"[SIMULAR CARGAR TASAS] 🏷️  Tipo obtenido desde Tarifas: {tipota} para empresa={empresa}, rubro={rubro_cod}")
                            else:
                                print(f"[SIMULAR CARGAR TASAS] ⚠️ No se encontró tarifa para empresa={empresa}, rubro={rubro_cod}, cod_tarifa={cod_tarifa}, usando valores por defecto")
                        except Exception as e:
                            print(f"[SIMULAR CARGAR TASAS] ⚠️ Error obteniendo info desde Tarifas: {e}, usando valores por defecto")
                        
                        # Si no se obtuvo el tipo desde Tarifas, usar el del Rubro como fallback
                        if tipota == 'F' and rubro_obj:
                            if hasattr(rubro_obj, 'tipo') and rubro_obj.tipo:
                                tipo_str = str(rubro_obj.tipo).upper()
                                if 'V' in tipo_str or 'VARIABLE' in tipo_str:
                                    tipota = 'V'
                                    print(f"[SIMULAR CARGAR TASAS] 🏷️  Tipo obtenido desde Rubro (fallback): {tipota}")
                        
                        cuenta = rubro_info.get('cuenta', '') or ''
                        cuentarez = rubro_info.get('cuentarez', '') or ''
                        
                        if not cuenta and rubro_obj:
                            cuenta = getattr(rubro_obj, 'cuenta', '') or ''
                        if not cuenta:
                            cuenta = '11.7.1.01.09.00'
                        
                        if not cuentarez and rubro_obj:
                            cuentarez = getattr(rubro_obj, 'cuntarez', '') or getattr(rubro_obj, 'cuentarez', '') or ''
                        if not cuentarez:
                            cuentarez = '11.7.1.98.01.00'
                        
                        # Crear nueva tasa
                        nueva_tasa = TasasDecla.objects.create(
                            empresa=empresa,
                            idneg=idneg_tasa,
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
                            'valor': float(rubro_info['valor_default']),
                            'id': nueva_tasa.id
                        })
                        tasas_creadas_count += 1
                        print(f"[SIMULAR CARGAR TASAS] ✅ [{tasas_creadas_count}] Tasa creada: Rubro={rubro_cod}, Tipo={tipota}, Frecuencia={frecuencia}, Valor={rubro_info['valor_default']}, ID={nueva_tasa.id}")
                    except Exception as e:
                        print(f"[SIMULAR CARGAR TASAS] ❌ Error creando tasa para rubro {rubro_cod}: {e}")
                        import traceback
                        traceback.print_exc()
                        tasas_error.append({
                            'rubro': rubro_cod,
                            'error': f'Error creando tasa: {str(e)}'
                        })
            
            # PASO 3: Calcular valores de tasas (Fijas y Variables)
            print(f"\n[SIMULAR CARGAR TASAS] {'='*90}")
            print(f"[SIMULAR CARGAR TASAS] PASO 3: Calcular valores de tasas (Fijas y Variables)")
            print(f"[SIMULAR CARGAR TASAS] {'='*90}")
            
            tasas_decla_calc = TasasDecla.objects.filter(
                empresa=empresa,
                rtm=rtm,
                expe=expe,
                ano=ano_decimal
            )
            
            total_tasas = tasas_decla_calc.count()
            print(f"[SIMULAR CARGAR TASAS] 📊 Total de tasas encontradas: {total_tasas}")
            
            for tasa_calc in tasas_decla_calc:
                try:
                    rubro_tasa_calc = tasa_calc.rubro or ''
                    
                    # TASA FIJA
                    if tasa_calc.tipota == 'F':
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
                                print(f"[SIMULAR CARGAR TASAS] 📅 Frecuencia actualizada desde Tarifas: {tarifa.frecuencia.upper()}")
                            # Actualizar tipo (tipota) desde Tarifas si está disponible
                            if tarifa.tipo:
                                tasa_calc.tipota = tarifa.tipo.upper()
                                print(f"[SIMULAR CARGAR TASAS] 🏷️  Tipo actualizado desde Tarifas: {tarifa.tipo.upper()}")
                            tasa_calc.save()
                            tasas_calculadas.append({
                                'rubro': rubro_tasa_calc,
                                'tipo': 'F',
                                'valor': str(tarifa.valor),
                                'frecuencia': tarifa.frecuencia.upper() if tarifa.frecuencia else 'A',
                                'mensaje': 'Tasa fija actualizada desde tarifas'
                            })
                            print(f"[SIMULAR CARGAR TASAS] ✅ Tasa Fija: {rubro_tasa_calc} = {tarifa.valor}, Frecuencia: {tarifa.frecuencia.upper() if tarifa.frecuencia else 'A'}, Tipo: {tarifa.tipo.upper() if tarifa.tipo else 'F'}")
                    
                    # TASA VARIABLE
                    elif tasa_calc.tipota == 'V':
                        plan = PlanArbitrio.objects.filter(
                            empresa=empresa,
                            rubro=rubro_tasa_calc,
                            ano=ano_decimal
                        ).order_by('codigo').filter(
                            minimo__lte=valorbase,
                            maximo__gte=valorbase
                        ).first()
                        
                        if plan and plan.valor:
                            tasa_calc.valor = plan.valor
                            tasa_calc.save()
                            tasas_calculadas.append({
                                'rubro': rubro_tasa_calc,
                                'tipo': 'V',
                                'valor': str(plan.valor),
                                'mensaje': f'Tasa variable actualizada según plan de arbitrio (rango {plan.minimo}-{plan.maximo})'
                            })
                            print(f"[SIMULAR CARGAR TASAS] ✅ Tasa Variable: {rubro_tasa_calc} = {plan.valor}")
                        else:
                            tasas_error.append({
                                'rubro': rubro_tasa_calc,
                                'error': f'No se encontró plan de arbitrio con rango que incluya {valorbase}'
                            })
                            print(f"[SIMULAR CARGAR TASAS] ⚠️ No se encontró plan para {rubro_tasa_calc}")
                except Exception as e:
                    print(f"[SIMULAR CARGAR TASAS] ❌ Error procesando tasa: {e}")
                    import traceback
                    traceback.print_exc()
                    tasas_error.append({
                        'rubro': 'N/A',
                        'error': str(e)
                    })
            
            print(f"\n[SIMULAR CARGAR TASAS] {'='*100}")
            print(f"[SIMULAR CARGAR TASAS] ✅✅✅ PROCESO COMPLETADO ✅✅✅")
            print(f"[SIMULAR CARGAR TASAS] {'='*100}")
            print(f"[SIMULAR CARGAR TASAS]   📊 Tasas creadas: {len(tasas_creadas)}")
            print(f"[SIMULAR CARGAR TASAS]   🔢 Tasas calculadas: {len(tasas_calculadas)}")
            print(f"[SIMULAR CARGAR TASAS]   ⚠️  Errores: {len(tasas_error)}")
            print(f"[SIMULAR CARGAR TASAS] {'='*100}")
            print()
            
            return JsonResponse({
                'exito': True,
                'mensaje': f'Simulación completada. {len(tasas_creadas)} tasas creadas, {len(tasas_calculadas)} tasas calculadas',
                'tasas_creadas': tasas_creadas,
                'tasas_calculadas': tasas_calculadas,
                'tasas_error': tasas_error,
                'total_creadas': len(tasas_creadas),
                'total_calculadas': len(tasas_calculadas),
                'total_errores': len(tasas_error)
            })
            
        except Exception as e:
            print(f"[SIMULAR CARGAR TASAS] ❌❌❌ ERROR GENERAL: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error en simulación: {str(e)}',
                'tasas_creadas': [],
                'tasas_calculadas': [],
                'tasas_error': []
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido',
        'tasas_creadas': [],
        'tasas_calculadas': [],
        'tasas_error': []
    })


@csrf_exempt
def buscar_actividades_por_descripcion_ajax(request):
    """
    Busca actividades en la tabla 'actividad' para asignar código a campos cuentarez o cuentarec
    
    Busca por:
    - Campo empresa (filtro obligatorio)
    - Campo codigo (coincidencia parcial)
    - Campo descripcion (coincidencia parcial)
    
    Retorna el código de la actividad encontrada para asignarlo al campo correspondiente.
    """
    import logging
    import sys
    from django.db import models
    
    logger = logging.getLogger(__name__)
    
    print("=" * 80, file=sys.stderr)
    print("🔵 EJECUTANDO: buscar_actividades_por_descripcion_ajax", file=sys.stderr)
    print(f"🔵 Method: {request.method}", file=sys.stderr)
    print(f"🔵 URL: {request.path}", file=sys.stderr)
    print(f"🔵 GET params: {dict(request.GET)}", file=sys.stderr)
    print("=" * 80, file=sys.stderr)
    
    logger.info(f"🔍 buscar_actividades_por_descripcion_ajax - Method: {request.method}")
    logger.info(f"🔍 URL: {request.path}")
    logger.info(f"🔍 GET params: {dict(request.GET)}")
    
    if request.method == 'GET':
        try:
            empresa = request.GET.get('empresa', '').strip()
            termino = request.GET.get('termino', '').strip()
            limite = int(request.GET.get('limite', 10))
            
            logger.info(f"🔍 Parámetros recibidos - empresa: {empresa}, termino: {termino}, limite: {limite}")
            
            if not empresa:
                return JsonResponse({
                    'exito': False,
                    'actividades': [],
                    'mensaje': 'Empresa es obligatoria'
                })
            
            if not termino or len(termino) < 1:
                return JsonResponse({
                    'exito': True,
                    'actividades': [],
                    'mensaje': 'Ingrese código o nombre para buscar'
                })
            
            try:
                # Intentar importar desde diferentes ubicaciones
                try:
                    from tributario.models import Actividad
                except ImportError:
                    try:
                        from tributario.models import Actividad
                    except ImportError:
                        return JsonResponse({
                            'exito': False,
                            'actividades': [],
                            'mensaje': 'Error: Modelo Actividad no encontrado'
                        })
                
                # Buscar en tabla actividad por empresa, código o descripción
                actividades = Actividad.objects.filter(
                    empresa=empresa
                ).filter(
                    models.Q(codigo__icontains=termino) | 
                    models.Q(descripcion__icontains=termino)
                ).order_by('codigo')[:limite]
                
                resultados = []
                for actividad in actividades:
                    resultados.append({
                        'codigo': actividad.codigo or '',
                        'descripcion': actividad.descripcion or ''
                    })
                
                logger.info(f"✅ Se encontraron {len(resultados)} actividades")
                
                return JsonResponse({
                    'exito': True,
                    'actividades': resultados,
                    'total': len(resultados),
                    'mensaje': f'Se encontraron {len(resultados)} actividades'
                })
            except Exception as e:
                print(f"Error en búsqueda: {e}", file=sys.stderr)
                logger.error(f"Error en búsqueda: {e}")
                return JsonResponse({
                    'exito': False,
                    'actividades': [],
                    'mensaje': f'Error: {str(e)}'
                })
        except Exception as e:
            print(f"Error general: {e}", file=sys.stderr)
            logger.error(f"Error general: {e}")
            return JsonResponse({
                'exito': False,
                'actividades': [],
                'mensaje': f'Error: {str(e)}'
            })
    else:
        return JsonResponse({
            'exito': False,
            'actividades': [],
            'mensaje': 'Método no permitido'
        })
