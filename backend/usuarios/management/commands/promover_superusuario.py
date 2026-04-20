# -*- coding: utf-8 -*-
"""
Marca un usuario existente como superusuario (puede usar /menu/usuarios-sistema/).

Uso (desde c:\\simafiweb\\venv\\Scripts):
    python manage.py promover_superusuario demo_simafi 0301

El login modular pide usuario, municipio y contraseña del usuario.
"""
from django.core.management.base import BaseCommand, CommandError

from usuarios.models import Usuario


class Command(BaseCommand):
    help = "Activa es_superusuario=1 para un usuario ya existente (empresa = codigo de municipio)."

    def add_arguments(self, parser):
        parser.add_argument("usuario", type=str, help="Nombre de usuario (columna usuario)")
        parser.add_argument("empresa", type=str, help="Código de empresa, ej. 0301")

    def handle(self, *args, **options):
        usu = (options["usuario"] or "").strip()
        emp = (options["empresa"] or "").strip()
        if not usu or not emp:
            raise CommandError("Indique usuario y empresa.")

        try:
            u = Usuario.objects.get(usuario=usu, empresa=emp)
        except Usuario.DoesNotExist:
            raise CommandError(
                f"No existe usuario={usu!r} con empresa={emp!r}. "
                f"Cree el registro antes o ejecute: python manage.py create_demo_users"
            )

        if u.es_superusuario:
            self.stdout.write(self.style.WARNING(f"Ya era superusuario: {u.usuario} ({u.empresa})"))
            return

        u.es_superusuario = True
        u.save(update_fields=["es_superusuario"])
        self.stdout.write(
            self.style.SUCCESS(
                f"Listo. Entre al menú modular con usuario {u.usuario!r} y el municipio "
                f"que corresponda a empresa {u.empresa}, luego abra /menu/usuarios-sistema/"
            )
        )
