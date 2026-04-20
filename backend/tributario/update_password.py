#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tributario.settings')
django.setup()

from modules.usuarios.models import Usuario
import hashlib

# Actualizar contraseña del usuario tributario
user = Usuario.objects.get(usuario='tributario', municipio_id=2)
correct_hash = hashlib.sha256('admin123'.encode()).hexdigest()
user.password = correct_hash
user.save()

print('✅ Contraseña actualizada correctamente')
print(f'Hash aplicado: {correct_hash}')
