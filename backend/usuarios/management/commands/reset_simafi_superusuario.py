# -*- coding: utf-8 -*-
"""
Crea o actualiza el superusuario global SIMAFI (sin municipio / empresa vacía) con contraseña MESR.

Uso (desde c:\\simafiweb\\venv\\Scripts):
    python manage.py reset_simafi_superusuario

Desactiva otras filas SIMAFI ligadas a un municipio para que el login sin desplegable encuentre una sola cuenta.
"""
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from usuarios.models import Usuario


class Command(BaseCommand):
    help = "Garantiza SIMAFI como superusuario global (empresa vacía); clave MESR."

    def handle(self, *args, **options):
        pwd_hash = make_password("MESR")

        # Una sola cuenta global: desactivar SIMAFI duplicados por empresa/municipio
        Usuario.objects.filter(usuario="SIMAFI").exclude(empresa="").update(is_active=False)

        u, created = Usuario.objects.update_or_create(
            usuario="SIMAFI",
            empresa="",
            defaults={
                "password": pwd_hash,
                "nombre": "Superusuario SIMAFI",
                "municipio": None,
                "is_active": True,
                "es_superusuario": True,
            },
        )
        action = "Creado" if created else "Actualizado (contraseña y datos)"
        self.stdout.write(self.style.SUCCESS(f"{action}: usuario=SIMAFI superusuario global (sin municipio)"))
        self.stdout.write("")
        self.stdout.write("Inicie sesión en /login/ con:")
        self.stdout.write("  Usuario: SIMAFI")
        self.stdout.write("  Contraseña: MESR")
        self.stdout.write("  Municipio: deje la primera opción (vacía) — no aplica a superusuario global")
        self.stdout.write("")
