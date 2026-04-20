"""
Script de prueba para verificar la tabla tasasdecla usando SQL directo
"""
try:
    import pymysql as mysql_lib
    mysql_lib.install_as_MySQLdb()
    connection_type = "pymysql"
except ImportError:
    try:
        import MySQLdb as mysql_lib
        connection_type = "MySQLdb"
    except ImportError:
        print("ERROR: No se encontró ningún driver de MySQL (pymysql o MySQLdb)")
        exit(1)

print("=" * 80)
print("TEST DE CONSULTA A TABLA TASASDECLA (SQL DIRECTO)")
print("=" * 80)

# Parámetros de prueba
empresa = '0301'
rtm = '114-03-23'
expe = '1151'

print(f"\n📋 Parámetros de búsqueda:")
print(f"   Empresa: {empresa}")
print(f"   RTM: {rtm}")
print(f"   EXPE: {expe}")
print("-" * 80)

try:
    # Conectar a la base de datos
    print(f"\n🔌 Conectando a la base de datos usando {connection_type}...")
    connection = mysql_lib.connect(
        host='localhost',
        port=3307,
        database='bdsimafipy',
        user='root',
        password='sandres',
        charset='latin1'
    )
    
    if connection:
        print("   ✅ Conexión exitosa")
        cursor = connection.cursor()
        
        # Test 1: Verificar total de registros
        print("\n🔍 Test 1: Total de registros en tasasdecla")
        cursor.execute("SELECT COUNT(*) FROM tasasdecla")
        total = cursor.fetchone()[0]
        print(f"   Total de registros: {total}")
        
        # Test 2: Estructura de la tabla
        print("\n🔍 Test 2: Estructura de la tabla")
        cursor.execute("DESCRIBE tasasdecla")
        columns = cursor.fetchall()
        print("   Columnas:")
        for col in columns:
            print(f"      {col[0]}: {col[1]}")
        
        # Test 3: Buscar por RTM solamente
        print(f"\n🔍 Test 3: Buscar por RTM = '{rtm}'")
        query = "SELECT * FROM tasasdecla WHERE rtm = %s LIMIT 5"
        cursor.execute(query, (rtm,))
        rows = cursor.fetchall()
        print(f"   Registros encontrados: {len(rows)}")
        for row in rows[:3]:
            print(f"   - ID={row[0]}, empresa='{row[1]}', rtm={row[3]}, expe={row[4]}, ano={row[6]}")
        
        # Test 4: Buscar por RTM y EXPE
        print(f"\n🔍 Test 4: Buscar por RTM = '{rtm}' y EXPE = '{expe}'")
        query = "SELECT * FROM tasasdecla WHERE rtm = %s AND expe = %s"
        cursor.execute(query, (rtm, expe))
        rows = cursor.fetchall()
        print(f"   Registros encontrados: {len(rows)}")
        
        if len(rows) > 0:
            print("\n   📊 Detalles de los registros:")
            for i, row in enumerate(rows, 1):
                print(f"\n   Registro {i}:")
                print(f"      ID: {row[0]}")
                print(f"      Empresa: '{row[1]}' (longitud: {len(row[1]) if row[1] else 0})")
                print(f"      IDNEG: {row[2]}")
                print(f"      RTM: {row[3]}")
                print(f"      EXPE: {row[4]}")
                print(f"      NoDECLA: {row[5]}")
                print(f"      Año: {row[6]}")
                print(f"      Rubro: {row[7]}")
                print(f"      Cod_Tarifa: {row[8]}")
                print(f"      Frecuencia: {row[9]}")
                print(f"      Valor: {row[10]}")
                print(f"      Cuenta: {row[11]}")
                print(f"      CuentaRez: {row[12]}")
        else:
            print("   ⚠️ No se encontraron registros")
        
        # Test 5: Buscar por empresa, RTM y EXPE
        print(f"\n🔍 Test 5: Buscar por EMPRESA = '{empresa}', RTM = '{rtm}' y EXPE = '{expe}'")
        query = "SELECT * FROM tasasdecla WHERE empresa = %s AND rtm = %s AND expe = %s"
        cursor.execute(query, (empresa, rtm, expe))
        rows = cursor.fetchall()
        print(f"   Registros encontrados: {len(rows)}")
        
        if len(rows) > 0:
            print("\n   ✅ Registros encontrados con empresa, rtm y expe:")
            for i, row in enumerate(rows, 1):
                print(f"\n   Registro {i}:")
                print(f"      ID: {row[0]}")
                print(f"      Empresa: '{row[1]}'")
                print(f"      RTM: {row[3]}")
                print(f"      EXPE: {row[4]}")
                print(f"      Año: {row[6]}")
                print(f"      Rubro: {row[7]}")
                print(f"      Valor: L. {row[10]}")
        else:
            print("   ⚠️ No se encontraron registros con estos filtros")
            
            # Verificar valores de empresa que existen para este RTM/EXPE
            print("\n   🔍 Verificando valores de 'empresa' existentes:")
            query = """
                SELECT DISTINCT empresa, COUNT(*) as total 
                FROM tasasdecla 
                WHERE rtm = %s AND expe = %s 
                GROUP BY empresa
            """
            cursor.execute(query, (rtm, expe))
            empresas = cursor.fetchall()
            
            if empresas:
                print("   Valores de 'empresa' encontrados para este RTM/EXPE:")
                for emp_row in empresas:
                    emp_val = emp_row[0]
                    emp_count = emp_row[1]
                    emp_repr = repr(emp_val)
                    print(f"      - empresa={emp_repr} (total: {emp_count} registros)")
                    
                print(f"\n   💡 Comparación:")
                print(f"      Buscando: empresa='{empresa}' (longitud: {len(empresa)})")
                print(f"      Encontrado: empresa={repr(empresas[0][0])} (longitud: {len(empresas[0][0]) if empresas[0][0] else 0})")
        
        # Test 6: Mostrar algunos registros de ejemplo
        print("\n🔍 Test 6: Primeros 5 registros de la tabla (cualquiera)")
        cursor.execute("SELECT * FROM tasasdecla LIMIT 5")
        rows = cursor.fetchall()
        print(f"   Mostrando {len(rows)} registros de ejemplo:")
        for i, row in enumerate(rows, 1):
            print(f"   {i}. empresa='{row[1]}', rtm={row[3]}, expe={row[4]}, ano={row[6]}")
        
        cursor.close()

except Exception as e:
    print(f"\n❌ Error general: {e}")
    import traceback
    traceback.print_exc()
finally:
    try:
        if connection:
            connection.close()
            print("\n🔌 Conexión cerrada")
    except:
        pass

print("\n" + "=" * 80)
print("FIN DEL TEST")
print("=" * 80)

