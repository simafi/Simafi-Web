"""
Utilidades para conversión de coordenadas entre Lat/Lng y UTM
"""
import logging

logger = logging.getLogger(__name__)

try:
    from pyproj import Transformer
    PYPROJ_AVAILABLE = True
    # Verificar que Transformer funciona (solo si logger está disponible)
    try:
        test_transformer = Transformer.from_crs("EPSG:4326", "EPSG:32616", always_xy=True)
        test_result = test_transformer.transform(-87.0, 15.0)
        if logger:
            logger.info("pyproj está disponible y funcionando correctamente")
    except Exception as test_err:
        if logger:
            logger.warning(f"Error al verificar Transformer: {test_err}")
except ImportError as e:
    PYPROJ_AVAILABLE = False
    if logger:
        logger.warning(f"pyproj no está instalado: {e}. Instale con: pip install pyproj")
except Exception as e:
    PYPROJ_AVAILABLE = False
    if logger:
        logger.error(f"Error al verificar pyproj: {e}")

# Zona UTM para Honduras (zona 16N)
UTM_ZONE = 16
UTM_NORTH = True


def latlng_to_utm(lat, lng):
    """
    Convierte coordenadas de latitud/longitud (WGS84) a UTM (zona 16N para Honduras)
    
    Args:
        lat: Latitud en grados decimales
        lng: Longitud en grados decimales
    
    Returns:
        tuple: (easting, northing) en metros UTM, o (None, None) si hay error
    """
    global PYPROJ_AVAILABLE
    try:
        # Verificar que pyproj esté disponible
        if not PYPROJ_AVAILABLE:
            try:
                from pyproj import Transformer
                # Si podemos importar, actualizar la variable global
                PYPROJ_AVAILABLE = True
            except ImportError:
                if logger:
                    logger.error("pyproj no está disponible. No se puede convertir a UTM.")
                return None, None
        
        if lat is None or lng is None:
            return None, None
        
        # Convertir a float si es necesario
        lat = float(lat)
        lng = float(lng)
        
        # Validar rango de coordenadas
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            if logger:
                logger.warning(f"Coordenadas fuera de rango: lat={lat}, lng={lng}")
            return None, None
        
        # Crear transformer de WGS84 a UTM
        # EPSG:4326 = WGS84 (lat/lng)
        # EPSG:32616 = UTM zona 16N (Honduras)
        from pyproj import Transformer
        transformer = Transformer.from_crs("EPSG:4326", f"EPSG:326{UTM_ZONE}", always_xy=True)
        
        # Transformar coordenadas (lng, lat) -> (easting, northing)
        easting, northing = transformer.transform(lng, lat)
        
        if logger:
            logger.info(f"Conversión UTM: ({lat}, {lng}) -> ({easting:.2f}, {northing:.2f})")
        return easting, northing
        
    except ImportError as e:
        if logger:
            logger.error(f"Error al importar pyproj: {str(e)}")
        return None, None
    except Exception as e:
        if logger:
            logger.error(f"Error al convertir a UTM: {str(e)}", exc_info=True)
        return None, None


def utm_to_latlng(easting, northing, zone=UTM_ZONE):
    """
    Convierte coordenadas UTM a latitud/longitud (WGS84)
    
    Args:
        easting: Coordenada X UTM en metros
        northing: Coordenada Y UTM en metros
        zone: Zona UTM (default: 16 para Honduras)
    
    Returns:
        tuple: (lat, lng) en grados decimales, o (None, None) si hay error
    """
    global PYPROJ_AVAILABLE
    try:
        # Verificar que pyproj esté disponible
        if not PYPROJ_AVAILABLE:
            try:
                from pyproj import Transformer
                # Si podemos importar, actualizar la variable global
                PYPROJ_AVAILABLE = True
            except ImportError:
                if logger:
                    logger.error("pyproj no está disponible. No se puede convertir de UTM.")
                return None, None
        
        if easting is None or northing is None:
            return None, None
        
        # Convertir a float si es necesario
        easting = float(easting)
        northing = float(northing)
        
        # Crear transformer de UTM a WGS84
        from pyproj import Transformer
        transformer = Transformer.from_crs(f"EPSG:326{zone}", "EPSG:4326", always_xy=True)
        
        # Transformar coordenadas (easting, northing) -> (lng, lat)
        lng, lat = transformer.transform(easting, northing)
        
        if logger:
            logger.info(f"Conversión desde UTM: ({easting:.2f}, {northing:.2f}) -> ({lat:.7f}, {lng:.7f})")
        return lat, lng
        
    except ImportError as e:
        if logger:
            logger.error(f"Error al importar pyproj: {str(e)}")
        return None, None
    except Exception as e:
        if logger:
            logger.error(f"Error al convertir desde UTM: {str(e)}", exc_info=True)
        return None, None

