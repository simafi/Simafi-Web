from django.core.management.base import BaseCommand
from modules.usuarios.models import Usuario
import hashlib

class Command(BaseCommand):
    help = 'Actualiza la contraseña del usuario tributario'

    def handle(self, *args, **options):
        try:
            # Buscar usuario tributario
            user = Usuario.objects.get(usuario='tributario', municipio_id=2)
            self.stdout.write(f'Usuario encontrado: {user.usuario}')
            self.stdout.write(f'Empresa: {user.empresa}')
            self.stdout.write(f'Municipio: {user.municipio_id}')
            
            # Generar hash SHA256 para admin123
            correct_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            self.stdout.write(f'Hash SHA256 de admin123: {correct_hash}')
            
            # Actualizar contraseña
            user.password = correct_hash
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS('✅ Contraseña actualizada correctamente')
            )
            
            # Verificar
            user.refresh_from_db()
            if user.password == correct_hash:
                self.stdout.write(
                    self.style.SUCCESS('✅ Verificación exitosa')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Error en verificación')
                )
            
        except Usuario.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('❌ Usuario tributario no encontrado')
            )
            # Mostrar usuarios disponibles
            for u in Usuario.objects.all():
                self.stdout.write(f'  - {u.usuario} (empresa: {u.empresa}, municipio: {u.municipio_id})')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {e}')
            )
