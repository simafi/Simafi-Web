# MODELO DJANGO CORREGIDO - models.py
# Cambiar 'cocontrolado' por 'controlado'

from django.db import models

class Declara(models.Model):
    id = models.AutoField(primary_key=True)
    idneg = models.IntegerField(default=0)
    rtm = models.CharField(max_length=20, default='')
    expe = models.CharField(max_length=10, blank=True, null=True)
    ano = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tipo = models.DecimalField(max_digits=1, decimal_places=0, default=0)
    mes = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    ventai = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    ventac = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    ventas = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    valorexcento = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    
    # CORREGIDO: usar 'controlado' en lugar de 'cocontrolado'
    controlado = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    
    unidad = models.DecimalField(max_digits=11, decimal_places=0, default=0)
    factor = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    fechssys = models.DateTimeField(blank=True, null=True)
    usuario = models.CharField(max_length=50, blank=True, null=True)
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    class Meta:
        db_table = 'declara'
        managed = False  # Django no gestiona esta tabla
        
    def __str__(self):
        return f"Declara {self.id} - RTM: {self.rtm}"
