# Importar Django models
from django.db import models

# Importar modelos del sistema modular
from core.models import Municipio, Departamento
from usuarios.models import Usuario

# =============================================================================
# TODOS LOS MODELOS HAN SIDO MOVIDOS A tributario/models.py
# =============================================================================
# Para usar los modelos, importarlos directamente desde tributario.models:
# 
# from tributario.models import (
#     Identificacion, Actividad, Oficina, Negocio,
#     PagoVariosTemp, NoRecibos, Rubro, PlanArbitrio,
#     Tarifas, TarifasImptoics, DeclaracionVolumen,
#     AnoEmpreNu, TasasDecla, TarifasICS, Anos
# )
# =============================================================================


# =============================================================================
# IMPORTACIONES DE MODELOS PRINCIPALES - COMENTADO PARA EVITAR CONFLICTOS
# =============================================================================
# Los modelos principales se importan DIRECTAMENTE desde tributario.models
# NO importarlos aquí para evitar conflictos de registro de modelos
# =============================================================================

# # Importar modelos principales desde el archivo principal
# from tributario.models import (
#     Identificacion,
#     Actividad, 
#     Oficina,
#     Negocio,
#     PagoVariosTemp,
#     NoRecibos,
#     Rubro,
#     PlanArbitrio,
#     Tarifas
# )

# =============================================================================
# DOCUMENTACIÓN DE ESTRUCTURA
# =============================================================================
"""
ESTRUCTURA DE MODELOS ESTABLECIDA:

ARCHIVO PRINCIPAL: venv/Scripts/tributario/models.py
- Identificacion
- Actividad
- Oficina  
- Negocio
- PagoVariosTemp
- NoRecibos
- Rubro
- PlanArbitrio
- Tarifas

ARCHIVO SECUNDARIO: venv/Scripts/tributario/tributario_app/models.py
- TarifasICS (específico de la app)

REGLAS DE IMPORTACIÓN:
- Modelos principales: from tributario.models import Modelo
- Modelos específicos: from tributario_app.models import Modelo
- NUNCA definir modelos duplicados en ambos archivos
"""