# -*- coding: utf-8 -*-
"""
Crea o actualiza usuarios de prueba para desarrollo local.

Uso (desde venv/Scripts/tributario):
    python manage.py create_demo_users

Requiere que exista el municipio con código 0301 (COMAYAGUA) en la tabla `municipio`.
"""
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from core.models import Municipio
from usuarios.models import Usuario

# Credenciales fijas solo para entornos de desarrollo / prueba
DEMO = (
    {
        "usuario": "demo_simafi",
        "password_plain": "SimafiDemo2026!",
        "nombre": "Usuario demostración SIMAFI",
        "empresa": "0301",
        "es_superusuario": True,
    },
    {
        "usuario": "SIMAFI",
        "password_plain": "MESR",
        "nombre": "Superusuario SIMAFI global",
        "empresa": "",
        "es_superusuario": True,
        "sin_municipio": True,
    },
    {
        "usuario": "tributario",
        "password_plain": "123",
        "nombre": "Tributario prueba",
        "empresa": "0301",
        "es_superusuario": False,
    },
)


class Command(BaseCommand):
    help = "Crea o actualiza usuarios de prueba (municipio 0301)."

    def handle(self, *args, **options):
        try:
            municipio = Municipio.objects.get(codigo="0301")
        except Municipio.DoesNotExist:
            self.stderr.write(
                self.style.ERROR(
                    "No existe municipio con codigo=0301. Cargue la tabla `municipio` antes."
                )
            )
            return

        for row in DEMO:
            pwd_hash = make_password(row["password_plain"])
            if row.get("sin_municipio"):
                emp = ""
                mun_fk = None
            else:
                emp = row["empresa"]
                mun_fk = municipio
            u, created = Usuario.objects.update_or_create(
                usuario=row["usuario"],
                empresa=emp,
                defaults={
                    "password": pwd_hash,
                    "nombre": row["nombre"],
                    "municipio": mun_fk,
                    "is_active": True,
                    "es_superusuario": row.get("es_superusuario", False),
                },
            )
            action = "Creado" if created else "Actualizado"
            extra = " [global, sin municipio]" if row.get("sin_municipio") else f" municipio={municipio}"
            self.stdout.write(
                self.style.SUCCESS(
                    f"{action}: usuario={row['usuario']} empresa={emp!r}{extra}"
                )
            )

        self.stdout.write("")
        self.stdout.write(self.style.WARNING("=== Credenciales de prueba (SOLO desarrollo) ==="))
        self.stdout.write(
            "  Login (/login/): usuario y contraseña; municipio obligatorio salvo superusuario global único."
        )
        self.stdout.write(
            "  SIMAFI global: deje municipio vacío. demo_simafi y tributario: municipio 0301."
        )
        for row in DEMO:
            sup = " [SUPERUSUARIO — configura usuarios del sistema]" if row.get("es_superusuario") else ""
            self.stdout.write(
                f"  Usuario: {row['usuario']}  (clave interna/guardada: {row['password_plain']}){sup}"
            )
        self.stdout.write(
            self.style.SUCCESS(
                "  Use demo_simafi para entrar a /menu/usuarios-sistema/ y gestionar usuarios."
            )
        )
        self.stdout.write("")
