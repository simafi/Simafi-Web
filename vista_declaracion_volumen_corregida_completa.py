def declaracion_volumen(request):
    """Vista para declaración de volumen de ventas"""
    from .models import DeclaracionVolumen, Negocio, TarifasICS, Rubro
    
    # Inicializar TODAS las variables al inicio para evitar UnboundLocalError
    negocio = None
    declaraciones = []
    tarifas_ics = []
    mensaje = None
    exito = False
    municipio_codigo = request.session.get('municipio_codigo', '0301')
    
    # Obtener parámetros de la URL
    rtm = request.GET.get('rtm', '')
    expe = request.GET.get('expe', '')
    
    if rtm and expe:
        try:
            # Buscar el negocio
            negocio = Negocio.objects.get(rtm=rtm, expe=expe, municipio=municipio_codigo)
            
            # Buscar declaraciones existentes
            declaraciones = DeclaracionVolumen.objects.filter(
                rtm=rtm, 
                expe=expe
            ).order_by('-ano', '-mes')
            
            # Obtener tarifas ICS vinculadas al negocio
            try:
                tarifas_ics_raw = TarifasICS.obtener_tarifas_por_negocio(negocio.id)
                tarifas_ics = []
                
                for tarifa_ics in tarifas_ics_raw:
                    # Buscar información del rubro
                    try:
                        rubro_info = Rubro.objects.get(
                            codigo=tarifa_ics.cod_tarifa,
                            municipio=municipio_codigo
                        )
                        rubro_nombre = rubro_info.descripcion
                    except Rubro.DoesNotExist:
                        try:
                            rubro_info = Rubro.objects.filter(
                                codigo__icontains=tarifa_ics.cod_tarifa[:3],
                                municipio=municipio_codigo
                            ).first()
                            rubro_nombre = rubro_info.descripcion if rubro_info else f"Rubro {tarifa_ics.cod_tarifa}"
                        except:
                            rubro_nombre = f"Rubro {tarifa_ics.cod_tarifa}"
                    except Exception as e:
                        rubro_nombre = f"Rubro {tarifa_ics.cod_tarifa}"
                    
                    # Agregar información del rubro al objeto tarifa_ics
                    tarifa_ics.rubro_nombre = rubro_nombre
                    tarifas_ics.append(tarifa_ics)
                    
            except Exception as e:
                print(f"Error al cargar tarifas ICS: {e}")
                tarifas_ics = []
                
        except Negocio.DoesNotExist:
            mensaje = "No se encontró el negocio con el RTM y expediente proporcionados"
            exito = False
        except Exception as e:
            print(f"Error al cargar declaraciones: {e}")
            mensaje = f"Error al cargar datos: {str(e)}"
            exito = False
            declaraciones = []
            tarifas_ics = []

    from tributario_app.forms import DeclaracionVolumenForm
    initial_data = {}
    if negocio:
        initial_data = {'rtm': rtm, 'expe': expe}
    form = DeclaracionVolumenForm(initial=initial_data)

    return render(request, 'declaracion_volumen.html', {
        'form': form, 
        'negocio': negocio, 
        'declaraciones': declaraciones,
        'tarifas_ics': tarifas_ics,  # ← SIEMPRE inicializada
        'mensaje': mensaje, 
        'exito': exito, 
        'municipio_codigo': municipio_codigo,
        'modulo': 'Tributario', 
        'descripcion': 'Declaración de Volumen de Ventas'
    })