
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
