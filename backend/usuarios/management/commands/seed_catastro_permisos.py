# -*- coding: utf-8 -*-
"""
Carga el catálogo de permisos de Catastro y un rol con todos ellos.

Uso (desde c:\\simafiweb\\venv\\Scripts):
    python manage.py seed_catastro_permisos

Luego asigne el rol \"Catastro — acceso completo\" (o permisos sueltos) a usuarios
en Usuarios del sistema. Sin filas en mod_usuarios_permiso para modulo=catastro,
el código no exige roles (modo compatibilidad).
"""
from django.core.management.base import BaseCommand

from catastro.permisos_codigos import (
    CATASTRO_PERMISOS_SEED,
    ROL_CATASTRO_COMPLETO_NOMBRE,
)
from usuarios.models import Permiso, Rol


class Command(BaseCommand):
    help = "Inserta permisos de aplicación del módulo Catastro y un rol con acceso completo."

    def handle(self, *args, **options):
        creados = 0
        for codigo, nombre, modulo in CATASTRO_PERMISOS_SEED:
            obj, created = Permiso.objects.update_or_create(
                codigo=codigo,
                defaults={
                    "nombre": nombre,
                    "modulo": modulo,
                    "is_active": True,
                },
            )
            if created:
                creados += 1

        permisos = list(Permiso.objects.filter(codigo__in=[t[0] for t in CATASTRO_PERMISOS_SEED]))
        rol, rcreated = Rol.objects.get_or_create(
            nombre=ROL_CATASTRO_COMPLETO_NOMBRE,
            defaults={
                "descripcion": "Incluye todos los permisos del módulo Catastro.",
                "is_active": True,
            },
        )
        rol.permisos.set(permisos)
        rol.is_active = True
        rol.save(update_fields=["is_active", "updated_at"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Permisos Catastro: {len(CATASTRO_PERMISOS_SEED)} en catálogo "
                f"({creados} creados, resto actualizados)."
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Rol \"{ROL_CATASTRO_COMPLETO_NOMBRE}\" vinculado a esos permisos."
            )
        )
        self.stdout.write(
            "Asigne ese rol a los usuarios en el menú «Usuarios del sistema»."
        )
