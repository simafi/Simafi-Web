from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from datetime import datetime
from decimal import Decimal
from .models import TasasMunicipales, BDCata1
from .forms_tasas_municipales import TasasMunicipalesForm
from tributario.models import Tarifas, Rubro

# Clase auxiliar para agregar descripción del rubro a las tasas
class TasaConDescripcion:
    def __init__(self, tasa, rubro_descripcion=''):
        self.id = tasa.id
        self.rubro = tasa.rubro
        self.rubro_descripcion = rubro_descripcion
        self.cod_tarifa = tasa.cod_tarifa
        self.valor = tasa.valor
        self.cuenta = tasa.cuenta
        self.cuentarez = tasa.cuentarez

# Las funciones se decorarán en views.py para evitar dependencia circular

@csrf_exempt
@require_http_methods(["GET", "POST"])
def configurar_tasas_municipales(request):
    """Vista para configurar las tasas municipales de un bien inmueble específico"""
    
    # Obtener el municipio del usuario desde la sesión
    municipio_codigo = request.session.get('catastro_empresa') or request.session.get('empresa') or request.session.get('catastro_municipio_codigo') or '0301'
    
    # Obtener datos del bien inmueble desde la URL o POST
    clave = request.GET.get('clave') or request.POST.get('clave')
    empresa = request.GET.get('empresa') or request.POST.get('empresa') or municipio_codigo
    
    # Variables para el contexto
    bien_inmueble = None
    tasas_municipales = []
    mensaje = None
    exito = False
    
    # Buscar el bien inmueble
    if clave:
        try:
            bien_inmueble = BDCata1.objects.get(
                empresa=empresa,
                cocata1=clave
            )
        except BDCata1.DoesNotExist:
            mensaje = "Bien inmueble no encontrado"
            exito = False
        except Exception as e:
            mensaje = f"Error al buscar bien inmueble: {str(e)}"
            exito = False
    
    # Si no se encontró el bien inmueble, mostrar error
    if not bien_inmueble:
        try:
            form = TasasMunicipalesForm()
        except Exception:
            form = None
            
        return render(request, 'configurar_tasas_municipales.html', {
            'bien_inmueble': None,
            'form': form,
            'tasas_municipales': [],
            'mensaje': mensaje or "Debe especificar una clave catastral válida",
            'exito': False,
            'municipio_codigo': empresa,
            'modulo': 'Catastro',
            'descripcion': 'Configurar Tasas Municipales'
        })
    
    # Manejar solicitudes POST
    if request.method == 'POST':
        try:
            accion = request.POST.get('accion')
            
            if accion == 'agregar_tarifa':
                # Agregar nueva tasa municipal
                rubro = request.POST.get('rubro')
                tarifa_rubro = request.POST.get('tarifa_rubro')
                valor_personalizado = request.POST.get('valor_personalizado')
                cuenta = request.POST.get('cuenta', '')
                cuentarez = request.POST.get('cuentarez', '')
                
                if not rubro or not tarifa_rubro or not valor_personalizado:
                    mensaje = "Todos los campos son requeridos"
                    exito = False
                else:
                    try:
                        ano_vigente = datetime.now().year
                        
                        # Buscar la tarifa seleccionada para obtener su valor por defecto
                        tarifa = Tarifas.objects.get(
                            empresa=empresa,
                            rubro=rubro,
                            cod_tarifa=tarifa_rubro,
                            ano=ano_vigente,
                            tipomodulo='D'  # Solo tarifas domésticas
                        )
                        
                        # Usar el valor personalizado si se proporciona, sino usar el valor de la tarifa
                        valor_final = Decimal(valor_personalizado) if valor_personalizado else tarifa.valor
                        
                        # Verificar si ya existe una tasa para este rubro
                        tasa_existente = TasasMunicipales.objects.filter(
                            empresa=empresa,
                            clave=clave,
                            rubro=rubro
                        ).first()
                        
                        if tasa_existente:
                            # Actualizar la tasa existente
                            tasa_existente.cod_tarifa = tarifa_rubro
                            tasa_existente.valor = valor_final
                            tasa_existente.cuenta = cuenta
                            tasa_existente.cuentarez = cuentarez
                            tasa_existente.save()
                            mensaje = "Tasa actualizada exitosamente"
                        else:
                            # Crear nueva tasa municipal
                            tasa_municipal = TasasMunicipales(
                                empresa=empresa,
                                clave=clave,
                                rubro=rubro,
                                cod_tarifa=tarifa_rubro,
                                valor=valor_final,
                                cuenta=cuenta,
                                cuentarez=cuentarez
                            )
                            tasa_municipal.save()
                            mensaje = "Tasa agregada exitosamente"
                        
                        exito = True
                        
                    except Tarifas.DoesNotExist:
                        mensaje = "La tarifa seleccionada no existe"
                        exito = False
                    except Exception as e:
                        mensaje = f"Error al guardar tasa: {str(e)}"
                        exito = False
            
            elif accion == 'eliminar_tarifa':
                tarifa_id = request.POST.get('tarifa_id')
                if tarifa_id:
                    try:
                        tasa_municipal = TasasMunicipales.objects.get(id=tarifa_id)
                        tasa_municipal.delete()
                        mensaje = "Tasa eliminada exitosamente"
                        exito = True
                    except TasasMunicipales.DoesNotExist:
                        mensaje = "Tasa no encontrada"
                        exito = False
                    except Exception as e:
                        mensaje = f"Error al eliminar tasa: {str(e)}"
                        exito = False
                else:
                    mensaje = "ID de tasa no especificado"
                    exito = False
            
        except Exception as e:
            mensaje = f"Error al procesar la solicitud: {str(e)}"
            exito = False
    
    # Obtener las tasas municipales configuradas para este bien inmueble
    # y agregar la descripción del rubro para cada tasa
    tasas_municipales_con_descripcion = []
    try:
        if bien_inmueble:
            tasas_municipales = TasasMunicipales.objects.filter(
                empresa=empresa,
                clave=clave
            ).order_by('rubro', 'cod_tarifa')
            
            # Crear un diccionario cache para las descripciones de rubros
            rubros_cache = {}
            
            # Agregar descripción del rubro a cada tasa
            for tasa in tasas_municipales:
                # Obtener descripción del rubro desde cache o base de datos
                rubro_key = f"{empresa}_{tasa.rubro}"
                if rubro_key not in rubros_cache:
                    try:
                        rubro_obj = Rubro.objects.get(empresa=empresa, codigo=tasa.rubro)
                        rubros_cache[rubro_key] = rubro_obj.descripcion or ''
                    except Rubro.DoesNotExist:
                        rubros_cache[rubro_key] = ''
                
                # Crear objeto con descripción del rubro
                tasa_con_desc = TasaConDescripcion(tasa, rubros_cache[rubro_key])
                tasas_municipales_con_descripcion.append(tasa_con_desc)
        else:
            tasas_municipales_con_descripcion = []
    except Exception as e:
        tasas_municipales_con_descripcion = []
        if not mensaje:
            mensaje = f"Error al cargar tasas: {str(e)}"
            exito = False
    
    # Crear el formulario para agregar nuevas tasas
    try:
        form = TasasMunicipalesForm(initial={
            'empresa': empresa,
            'clave': clave
        })
    except Exception as e:
        form = None
        if not mensaje:
            mensaje = f"Error al crear formulario: {str(e)}"
            exito = False
    
    return render(request, 'configurar_tasas_municipales.html', {
        'bien_inmueble': bien_inmueble,
        'form': form,
        'tasas_municipales': tasas_municipales_con_descripcion,
        'mensaje': mensaje,
        'exito': exito,
        'municipio_codigo': empresa,
        'modulo': 'Catastro',
        'descripcion': 'Configurar Tasas Municipales'
    })

@csrf_exempt
@require_http_methods(["POST"])
def obtener_tarifas_rubro_bienes(request):
    """Vista AJAX para obtener las tarifas de un rubro específico para bienes inmuebles
    Filtra por: empresa, rubro, ano y tipomodulo='D' (doméstico)
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        rubro_codigo = request.POST.get('rubro', '').strip()
        municipio_codigo = request.session.get('catastro_empresa') or request.session.get('empresa') or request.session.get('catastro_municipio_codigo') or '0301'
        
        logger.info(f"[TARIFAS_RUBRO] Búsqueda iniciada - Rubro: {rubro_codigo}, Municipio: {municipio_codigo}")
        
        if not rubro_codigo:
            logger.warning("[TARIFAS_RUBRO] Código de rubro vacío")
            return JsonResponse({
                'exito': False,
                'mensaje': 'Código de rubro requerido'
            })
        
        # Convertir año a Decimal para comparación correcta en la BD
        ano_vigente = datetime.now().year
        ano_decimal = Decimal(str(ano_vigente))
        
        logger.info(f"[TARIFAS_RUBRO] Año vigente: {ano_vigente} (Decimal: {ano_decimal})")
        
        # Buscar tarifas del rubro con tipomodulo='D' (doméstico)
        tarifas = Tarifas.objects.filter(
            empresa=municipio_codigo,
            rubro=rubro_codigo,
            ano=ano_decimal,
            tipomodulo='D'  # Solo tarifas domésticas
        ).order_by('cod_tarifa')
        
        logger.info(f"[TARIFAS_RUBRO] Tarifas encontradas: {tarifas.count()}")
        
        # Si no hay tarifas con el año vigente, intentar buscar sin filtrar por año
        if tarifas.count() == 0:
            logger.info(f"[TARIFAS_RUBRO] No se encontraron tarifas para el año {ano_vigente}, buscando sin filtro de año...")
            tarifas = Tarifas.objects.filter(
                empresa=municipio_codigo,
                rubro=rubro_codigo,
                tipomodulo='D'  # Solo tarifas domésticas
            ).order_by('-ano', 'cod_tarifa')  # Ordenar por año descendente para tomar la más reciente
        
        logger.info(f"[TARIFAS_RUBRO] Total tarifas encontradas (con/sin año): {tarifas.count()}")
        
        # Convertir a lista de diccionarios
        tarifas_data = []
        for tarifa in tarifas:
            tarifas_data.append({
                'cod_tarifa': tarifa.cod_tarifa,
                'descripcion': tarifa.descripcion or '',
                'valor': float(tarifa.valor) if tarifa.valor else 0.0,
                'frecuencia': tarifa.frecuencia or '',
                'tipo': tarifa.tipo or '',
                'ano': str(tarifa.ano) if tarifa.ano else ''
            })
            logger.debug(f"[TARIFAS_RUBRO] Tarifa agregada: {tarifa.cod_tarifa} - {tarifa.descripcion}")
        
        logger.info(f"[TARIFAS_RUBRO] Retornando {len(tarifas_data)} tarifas")
        
        # Obtener información del rubro (cuenta y cuentarez)
        rubro_cuenta = ''
        rubro_cuentarez = ''
        rubro_descripcion = ''
        try:
            rubro = Rubro.objects.get(empresa=municipio_codigo, codigo=rubro_codigo)
            rubro_cuenta = rubro.cuenta or ''
            rubro_cuentarez = rubro.cuentarez or ''
            rubro_descripcion = rubro.descripcion or ''
            logger.info(f"[TARIFAS_RUBRO] Datos del rubro obtenidos - Cuenta: {rubro_cuenta}, CuentaRez: {rubro_cuentarez}")
        except Rubro.DoesNotExist:
            logger.warning(f"[TARIFAS_RUBRO] Rubro {rubro_codigo} no encontrado")
        except Exception as e:
            logger.error(f"[TARIFAS_RUBRO] Error al obtener datos del rubro: {str(e)}")
        
        if len(tarifas_data) == 0:
            logger.warning(f"[TARIFAS_RUBRO] No se encontraron tarifas para rubro {rubro_codigo} con tipomodulo='D'")
            return JsonResponse({
                'exito': True,
                'tarifas': [],
                'rubro': {
                    'cuenta': rubro_cuenta,
                    'cuentarez': rubro_cuentarez,
                    'descripcion': rubro_descripcion
                },
                'mensaje': f'No se encontraron tarifas domésticas (tipomodulo="D") para el rubro "{rubro_codigo}"'
            })
        
        return JsonResponse({
            'exito': True,
            'tarifas': tarifas_data,
            'rubro': {
                'cuenta': rubro_cuenta,
                'cuentarez': rubro_cuentarez,
                'descripcion': rubro_descripcion
            }
        })
        
    except Exception as e:
        logger.error(f"[TARIFAS_RUBRO] Error al obtener tarifas: {str(e)}", exc_info=True)
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error al obtener tarifas: {str(e)}'
        })

