# Ejecutar esto en: python manage.py shell < crear_datos_shell.py
from tributario.models import Identificacion, Negocio, Actividad, Municipio
from datetime import date

# Crear identificación
try:
    identificacion = Identificacion.objects.create(
        identidad='0801199012345',
        nombres='JUAN CARLOS',
        apellidos='PEREZ LOPEZ',
        fechanac=date(1990, 5, 15)
    )
    print(f"✅ Identificación creada: {identificacion.identidad}")
except:
    print("ℹ️  Identificación ya existe")

# Crear identificación representante
try:
    identificacion2 = Identificacion.objects.create(
        identidad='0801198523456',
        nombres='MARIA ELENA',
        apellidos='GARCIA MARTINEZ',
        fechanac=date(1985, 8, 20)
    )
    print(f"✅ Identificación 2 creada: {identificacion2.identidad}")
except:
    print("ℹ️  Identificación 2 ya existe")

# Crear negocio
try:
    negocio = Negocio.objects.create(
        empresa='0801',
        rtm='001',
        expe='00001',
        nombrenego='PULPERIA DON JUAN',
        comerciante='JUAN CARLOS PEREZ LOPEZ',
        identidad='0801199012345',
        representante='MARIA ELENA GARCIA MARTINEZ',
        identidadrep='0801198523456',
        actividad='001',
        direccion='BARRIO LA GRANJA, CASA 123',
        telefono='22123456',
        estatus='A'
    )
    print(f"✅ Negocio creado: {negocio.empresa}-{negocio.rtm}-{negocio.expe}")
except:
    print("ℹ️  Negocio ya existe")

print("\nDATOS PARA PRUEBA:")
print("DNI: 0801199012345 (JUAN CARLOS PEREZ LOPEZ)")
print("DNI Rep: 0801198523456 (MARIA ELENA GARCIA MARTINEZ)")
print("Negocio: 0801-001-00001")


























































