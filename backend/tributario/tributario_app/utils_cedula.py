"""
utils_cedula.py — Utilidades para leer la cédula de identidad hondureña
y determinar el grupo etario del contribuyente.

Formato de la cédula hondureña:
    XXXX - YYYYMMDD - NNNNN
    │        │  │      └── 5 dígitos orden
    │        │  └───────── 2 dígitos MES de nacimiento
    │        └──────────── 2 dígitos AÑO de nacimiento (últimos 2)
    └────────────────────── 4 dígitos municipio de registro

Ejemplo: 0318-19840307-00456
         03=municipio dep.3, 18=municipio cód.18, 84=año nac., 03=mes, 07=día, ...

En cédulas "antiguas"/nuevas sin guiones:
    031884030700456
    Posiciones (0-indexed):
        [0:4]  = municipio
        [4:6]  = año nac (AA)
        [6:8]  = mes nac
        [8:10] = día nac   ← a veces
    La nueva cédula usa formato con guiones: DDDD-AAMMDD-NNNNN

Notas:
- El año de dos dígitos (AA) se interpreta como:
    AA < 30 → 2000 + AA  (nacidos después del 2000)
    AA >= 30 → 1900 + AA  (nacidos entre 1930-1999)
- Si la cédula tiene formato nuevo (muchos dígitos pero no se puede leer el año)
  se debe registrar la fecha de nacimiento manualmente.
"""

from datetime import date
import re
from typing import Optional, Tuple


def _limpiar_cedula(cedula: str) -> str:
    """Quita guiones, espacios y caracteres no numéricos de la cédula."""
    return re.sub(r'[^0-9]', '', cedula or '')


def extraer_fecha_nacimiento_cedula(cedula: str) -> Optional[date]:
    """
    Intenta extraer la fecha de nacimiento de una cédula hondureña.

    Trabajando con el formato posicional:
        [0:4]  municipio  (4 dígitos)
        [4:6]  año nac   (AA — dos dígitos)
        [6:8]  mes nac
        [8:10] día nac

    Retorna datetime.date o None si no es posible determinarlo.
    """
    nums = _limpiar_cedula(cedula)

    if len(nums) < 8:
        return None

    # Formato legacy observado: DDDD-YYYY-NNNNN (13 dígitos)
    # Ejemplo: 0318-1960-01003  -> 0318196001003
    # Aquí solo se conoce el año (YYYY). Para permitir cálculo de edad,
    # se asume fecha 01/01/YYYY.
    if len(nums) == 13:
        try:
            yyyy = int(nums[4:8])
            if 1900 <= yyyy <= date.today().year:
                return date(yyyy, 1, 1)
        except Exception:
            pass

    try:
        aa  = int(nums[4:6])   # año: dos dígitos
        mm  = int(nums[6:8])   # mes
        dd  = int(nums[8:10]) if len(nums) >= 10 else 1  # día (opcional)

        # Determinar siglo
        if aa < 30:
            anio = 2000 + aa
        else:
            anio = 1900 + aa

        # Validar mes y día
        if not (1 <= mm <= 12):
            return None
        if not (1 <= dd <= 31):
            dd = 1

        return date(anio, mm, dd)
    except (ValueError, IndexError):
        return None


def calcular_edad(fecha_nac: date, fecha_referencia: date = None) -> int:
    """Calcula la edad en años cumplidos."""
    ref = fecha_referencia or date.today()
    edad = ref.year - fecha_nac.year
    # Ajustar si aún no ha cumplido años este año
    if (ref.month, ref.day) < (fecha_nac.month, fecha_nac.day):
        edad -= 1
    return edad


# ── Grupos etarios según legislación hondureña ────────────────────────────────
EDAD_TERCERA_EDAD_MIN = 60    # >= 60 y < 80 → Tercera Edad
EDAD_CUARTA_EDAD_MIN  = 80    # >= 80         → Cuarta Edad

DESCUENTO_TERCERA_EDAD = 25   # 25 % sobre impuestos y tasa T0001
DESCUENTO_CUARTA_EDAD  = 35   # 35 % sobre impuestos y tasa T0001


def determinar_grupo_etario(cedula: str, fecha_nacimiento_manual: date = None) -> Tuple[str, int, int]:
    """
    Determina el grupo etario del contribuyente a partir de la cédula
    (o de la fecha de nacimiento ingresada manualmente si la cédula no
    permite extraer el año correctamente).

    Retorna: (grupo, edad, descuento_porcentaje)
      - grupo: 'CE' = Cuarta Edad, 'TE' = Tercera Edad, '' = No aplica
      - edad: edad calculada (0 si no se pudo determinar)
      - descuento_porcentaje: 35, 25 o 0
    """
    fecha_nac = fecha_nacimiento_manual

    if not fecha_nac:
        fecha_nac = extraer_fecha_nacimiento_cedula(cedula)

    if not fecha_nac:
        return '', 0, 0

    edad = calcular_edad(fecha_nac)

    if edad >= EDAD_CUARTA_EDAD_MIN:
        return 'CE', edad, DESCUENTO_CUARTA_EDAD
    elif edad >= EDAD_TERCERA_EDAD_MIN:
        return 'TE', edad, DESCUENTO_TERCERA_EDAD
    else:
        return '', edad, 0


def info_cedula(cedula: str, fecha_nacimiento_manual: date = None) -> dict:
    """
    Retorna un diccionario con información completa derivada de la cédula:
    {
        'cedula_limpia': str,
        'fecha_nacimiento': date | None,
        'edad': int,
        'grupo': 'CE' | 'TE' | '',
        'descuento_porcentaje': int,
        'descuento_label': str,
        'fuente': 'cedula' | 'manual' | 'no_determinado'
    }
    """
    nums = _limpiar_cedula(cedula)

    fuente = 'no_determinado'
    fecha_nac = None

    if fecha_nacimiento_manual:
        fecha_nac = fecha_nacimiento_manual
        fuente = 'manual'
    else:
        fecha_nac = extraer_fecha_nacimiento_cedula(cedula)
        if fecha_nac:
            fuente = 'cedula'

    edad = calcular_edad(fecha_nac) if fecha_nac else 0
    grupo, _, desc = determinar_grupo_etario(cedula, fecha_nacimiento_manual)

    labels = {
        'CE': f'Cuarta Edad ({edad} años) — {DESCUENTO_CUARTA_EDAD}% de descuento',
        'TE': f'Tercera Edad ({edad} años) — {DESCUENTO_TERCERA_EDAD}% de descuento',
        '':   'No aplica descuento por edad',
    }

    return {
        'cedula_limpia':      nums,
        'fecha_nacimiento':   fecha_nac,
        'edad':               edad,
        'grupo':              grupo,
        'descuento_porcentaje': desc,
        'descuento_label':    labels.get(grupo, ''),
        'fuente':             fuente,
        'aplica_tercera_edad': grupo == 'TE',
        'aplica_cuarta_edad':  grupo == 'CE',
        'aplica_algun_descuento': grupo in ('TE', 'CE'),
    }
