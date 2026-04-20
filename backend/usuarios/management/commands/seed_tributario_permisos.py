# -*- coding: utf-8 -*-
"""
Carga permisos del módulo Tributario y un rol con todos ellos.

Uso (desde c:\\simafiweb\\venv\\Scripts):
    python manage.py seed_tributario_permisos

Asigne el rol \"Tributario — acceso completo\" (o permisos parciales vía otros roles)
en Usuarios del sistema.
"""
from django.core.management.base import BaseCommand

from tributario.permisos_codigos import (
    ROL_TRIBUTARIO_COMPLETO_NOMBRE,
    TRIBUTARIO_PERMISOS_SEED,
)
from usuarios.models import Permiso, Rol


class Command(BaseCommand):
    help = "Inserta permisos de aplicación del módulo Tributario y un rol con acceso completo."

    def handle(self, *args, **options):
        creados = 0
        for codigo, nombre, modulo in TRIBUTARIO_PERMISOS_SEED:
            _, created = Permiso.objects.update_or_create(
                codigo=codigo,
                defaults={
                    "nombre": nombre,
                    "modulo": modulo,
                    "is_active": True,
                },
            )
            if created:
                creados += 1

        permisos = list(Permiso.objects.filter(codigo__in=[t[0] for t in TRIBUTARIO_PERMISOS_SEED]))
        rol, _ = Rol.objects.get_or_create(
            nombre=ROL_TRIBUTARIO_COMPLETO_NOMBRE,
            defaults={
                "descripcion": "Incluye todos los permisos del módulo Tributario.",
                "is_active": True,
            },
        )
        rol.permisos.set(permisos)
        rol.is_active = True
        rol.save(update_fields=["is_active", "updated_at"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Permisos Tributario: {len(TRIBUTARIO_PERMISOS_SEED)} en catálogo "
                f"({creados} nuevos, resto actualizados)."
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Rol \"{ROL_TRIBUTARIO_COMPLETO_NOMBRE}\" vinculado a esos permisos."
            )
        )
        self.stdout.write(
            "Asigne ese rol (u otros roles con subconjuntos) en «Usuarios del sistema»."
        )
