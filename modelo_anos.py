
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
