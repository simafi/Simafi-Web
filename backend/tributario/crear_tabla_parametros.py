"""Script puntual para crear la tabla parametros_tributarios en la base de datos."""
import django, os, sys

sys.path.insert(0, r'c:\simafiweb\venv\Scripts\tributario')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario_app.settings')
django.setup()

from django.db import connection

sql = """
CREATE TABLE IF NOT EXISTS `parametros_tributarios` (
    `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `empresa` varchar(4) NOT NULL DEFAULT 'GLOB',
    `tipo_parametro` varchar(2) NOT NULL,
    `ano_vigencia` int NOT NULL,
    `descripcion` varchar(200) NOT NULL DEFAULT '',
    `numero_decreto` varchar(50) NOT NULL DEFAULT '',
    `fecha_inicio` date NULL,
    `fecha_fin` date NULL,
    `fecha_corte` date NULL,
    `aplica_recargos` tinyint(1) NOT NULL DEFAULT 0,
    `aplica_intereses` tinyint(1) NOT NULL DEFAULT 0,
    `aplica_saldo_impuesto` tinyint(1) NOT NULL DEFAULT 0,
    `porcentaje_condonacion` decimal(5,2) NOT NULL DEFAULT 100.00,
    `porcentaje_descuento_saldo` decimal(5,2) NOT NULL DEFAULT 0.00,
    `meses_anticipacion` int NOT NULL DEFAULT 4,
    `porcentaje_descuento_anual` decimal(5,2) NOT NULL DEFAULT 0.00,
    `tasa_recargo_mensual` decimal(7,4) NOT NULL DEFAULT 0.0000,
    `recargo_maximo_porcentaje` decimal(7,2) NOT NULL DEFAULT 0.00,
    `activo` tinyint(1) NOT NULL DEFAULT 1,
    `usuario_crea` varchar(50) NOT NULL DEFAULT '',
    `fecha_crea` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `usuario_modifica` varchar(50) NOT NULL DEFAULT '',
    `fecha_modifica` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
"""

index_sqls = [
    "CREATE INDEX idx_paramtrib_emp_tipo_ano ON parametros_tributarios (empresa, tipo_parametro, ano_vigencia);",
    "CREATE INDEX idx_paramtrib_activo ON parametros_tributarios (activo);",
]

try:
    with connection.cursor() as cursor:
        cursor.execute(sql)
        print("✅ Tabla 'parametros_tributarios' creada (o ya existia).")
        for idx_sql in index_sqls:
            try:
                cursor.execute(idx_sql)
                print(f"✅ Índice creado: {idx_sql[:60]}...")
            except Exception as ie:
                print(f"⚠️  Índice ya existe o error: {ie}")
except Exception as e:
    print(f"❌ Error al crear tabla: {e}")
