# SOLUCIÓN 2: Modificar modelo Django
# Archivo: models.py

class Declara(models.Model):
    # Campos existentes...
    ventai = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    ventac = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    ventas = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    valorexcento = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    
    # OPCIÓN A: Agregar campo cocontrolado si no existe
    # cocontrolado = models.DecimalField(max_digits=16, decimal_places=2, default=0.00, null=True, blank=True)
    
    # OPCIÓN B: Usar property para mapear a campo existente
    @property
    def cocontrolado(self):
        # Mapear a otro campo existente o retornar 0
        return getattr(self, 'valorexcento', 0.00)
    
    @cocontrolado.setter
    def cocontrolado(self, value):
        # Opcional: guardar en otro campo
        pass

# SOLUCIÓN 3: Modificar la vista para evitar el campo
# En views.py, remover referencias a 'cocontrolado' temporalmente
