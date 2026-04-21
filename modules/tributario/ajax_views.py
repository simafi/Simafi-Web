from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models

@csrf_exempt
def buscar_actividad_ajax(request):
    """Vista AJAX para buscar actividad por empresa y codigo (cuenta)"""
    if request.method != 'GET':
        return JsonResponse({
            'exito': False,
            'existe': False,
            'cuentarez': '',
            'cuentarec': '',
            'descripcion': '',
            'mensaje': 'Método no permitido'
        })
    
    # Obtener parámetros - depuración completa
    print(f"🔍 [DEBUG] request.method: {request.method}")
    print(f"🔍 [DEBUG] request.GET completo: {dict(request.GET)}")
    print(f"🔍 [DEBUG] request.GET.items(): {list(request.GET.items())}")
    print(f"🔍 [DEBUG] request.GET.get('empresa'): {repr(request.GET.get('empresa'))}")
    print(f"🔍 [DEBUG] request.GET.get('cuenta'): {repr(request.GET.get('cuenta'))}")
    print(f"🔍 [DEBUG] request.path: {request.path}")
    print(f"🔍 [DEBUG] request.get_full_path(): {request.get_full_path()}")
    
    # Intentar obtener parámetros de diferentes formas
    empresa = request.GET.get('empresa', '').strip()
    cuenta = request.GET.get('cuenta', '').strip()  # En formulario es "cuenta", en BD es "codigo"
    
    # Si no se encuentra 'cuenta', intentar 'codigo' como alternativa
    if not cuenta:
        cuenta = request.GET.get('codigo', '').strip()
        print(f"🔍 [DEBUG] Intentando 'codigo' como alternativa: {repr(cuenta)}")
    
    print(f"🔍 [DEBUG] Después de procesar - empresa: {repr(empresa)}, cuenta: {repr(cuenta)}")
    
    # Validar parámetros requeridos
    if not empresa or not cuenta:
        print(f"❌ [ERROR] Parámetros faltantes - empresa: {repr(empresa)}, cuenta: {repr(cuenta)}")
        return JsonResponse({
            'exito': False,
            'existe': False,
            'cuentarez': '',
            'cuentarec': '',
            'cuentaint': '',
            'descripcion': '',
            'mensaje': f'Empresa y cuenta son obligatorios (empresa={repr(empresa)}, cuenta={repr(cuenta)})'
        })
    
    # Importar modelo
    try:
        from tributario.models import Actividad
    except ImportError:
        try:
            from tributario.models import Actividad
        except ImportError:
            return JsonResponse({
                'exito': False,
                'existe': False,
                'cuentarez': '',
                'cuentarec': '',
                'cuentaint': '',
                'descripcion': '',
                'mensaje': 'Error: Modelo Actividad no encontrado'
            })
    
    # Buscar actividad
    try:
        actividad = Actividad.objects.get(empresa=empresa, codigo=cuenta)
        
        # Retornar datos encontrados
        return JsonResponse({
            'exito': True,
            'existe': True,
            'descripcion': str(actividad.descripcion or '').strip(),
            'cuentarez': str(actividad.cuentarez or '').strip(),
            'cuentarec': str(actividad.cuentarec or '').strip(),
            'cuentaint': str(actividad.cuentaint or '').strip(),
            'mensaje': 'Actividad encontrada'
        })
        
    except Actividad.DoesNotExist:
        return JsonResponse({
            'exito': True,
            'existe': False,
            'descripcion': '',
            'cuentarez': '',
            'cuentarec': '',
            'cuentaint': '',
            'mensaje': 'Actividad no encontrada'
        })
        
    except Exception as e:
        print(f"❌ Error en búsqueda de actividad: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'exito': False,
            'existe': False,
            'descripcion': '',
            'cuentarez': '',
            'cuentarec': '',
            'cuentaint': '',
            'mensaje': f'Error en la búsqueda: {str(e)}'
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
                return JsonResponse({
                    'exito': False,
                    'existe': False,
                    'descripcion': '',
                    'mensaje': 'Empresa y código son obligatorios'
                })
            
            # Buscar en la tabla oficina
            try:
                from tributario.models import Oficina
                oficina = Oficina.objects.get(empresa=empresa, codigo=codigo)
                
                return JsonResponse({
                    'exito': True,
                    'existe': True,
                    'descripcion': oficina.descripcion or '',
                    'mensaje': 'Oficina encontrada'
                })
            except Oficina.DoesNotExist:
                return JsonResponse({
                    'exito': True,
                    'existe': False,
                    'descripcion': '',
                    'mensaje': 'Oficina no encontrada'
                })
            except Exception as e:
                print(f"❌ Error en búsqueda de oficina: {e}")
                return JsonResponse({
                    'exito': False,
                    'existe': False,
                    'descripcion': '',
                    'mensaje': f'Error en la búsqueda: {str(e)}'
                })
        except Exception as e:
            print(f"❌ Error general en buscar_oficina_ajax: {e}")
            return JsonResponse({
                'exito': False,
                'existe': False,
                'descripcion': '',
                'mensaje': f'Error interno: {str(e)}'
            })
    else:
        return JsonResponse({
            'exito': False,
            'existe': False,
            'descripcion': '',
            'mensaje': 'Método no permitido'
        })

@csrf_exempt
def buscar_rubro_ajax(request):
    """Vista AJAX para buscar rubro por empresa y código"""
    if request.method == 'POST':
        try:
            # Importar el modelo al inicio
            from tributario.models import Rubro
            
            empresa = request.POST.get('empresa', '').strip()
            codigo = request.POST.get('codigo', '').strip()
            
            print(f"🔍 Buscando rubro: empresa={empresa}, codigo={codigo}")
            
            if not empresa or not codigo:
                print("❌ Empresa o código vacíos")
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Empresa y código son obligatorios'
                })
            
            # Buscar en la tabla rubros
            try:
                rubro = Rubro.objects.get(empresa=empresa, codigo=codigo)
                
                print(f"✅ Rubro encontrado: {rubro.descripcion}")
                
                return JsonResponse({
                    'exito': True,
                    'rubro': {
                        'codigo': rubro.codigo,
                        'descripcion': rubro.descripcion or '',
                        'tipo': rubro.tipo or '',
                        'cuenta': rubro.cuenta or '',
                        'cuentarez': rubro.cuentarez or ''
                    },
                    'mensaje': 'Rubro encontrado'
                })
            except Rubro.DoesNotExist:
                print(f"❌ Rubro no encontrado: empresa={empresa}, codigo={codigo}")
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Rubro no encontrado'
                })
                    
        except Exception as e:
            print(f"❌ Error en búsqueda AJAX: {e}")
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error en el servidor: {str(e)}'
            })
    
    return JsonResponse({
        'exito': False,
        'mensaje': 'Método no permitido'
    })

@csrf_exempt
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
                print(f"Error en búsqueda: {e}")
                return JsonResponse({
                    'exito': False,
                    'actividades': [],
                    'mensaje': f'Error: {str(e)}'
                })
        except Exception as e:
            print(f"Error general: {e}")
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

@csrf_exempt
def cargar_actividades_ajax(request):
    """Vista AJAX para cargar actividades por empresa"""
    return JsonResponse({
        'exito': False,
        'mensaje': 'Función no implementada aún'
    })

@csrf_exempt
def calcular_tasas_plan_arbitrio(request):
    """
    Vista AJAX TEMPORAL para calcular tasas según el plan de arbitrios.
    
    Proceso:
    1. Seleccionar tasas de tasasdecla según empresa, rtm, expe, ano, rubro, tipota
    2. Validación: Si tipota = "F":
       - Buscar valor en tabla tarifas por empresa, rubro, ano (nota: no hay cod_tarifa en tarifas según modelo)
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
                        # Nota: según el modelo, tarifas tiene empresa, rubro, cod_tarifa, ano, valor
                        # En tasasdecla tenemos empresa, rubro (equivalente a cod_tarifa?), ano
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
















