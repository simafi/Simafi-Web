from django.core.management.base import BaseCommand
from modules.usuarios.models import Usuario
import hashlib

class Command(BaseCommand):
    help = 'Resetea todas las contraseñas a admin123'

    def handle(self, *args, **options):
        self.stdout.write("=== RESETEO DE CONTRASEÑAS ===")
        self.stdout.write("Estableciendo todas las contraseñas a: admin123")
        self.stdout.write("")
        
        # Hash SHA256 de admin123
        password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        self.stdout.write(f"Hash SHA256 de admin123: {password_hash}")
        self.stdout.write("")
        
        try:
            # Obtener todos los usuarios
            usuarios = Usuario.objects.all()
            self.stdout.write(f"Usuarios encontrados: {usuarios.count()}")
            self.stdout.write("")
            
            for user in usuarios:
                self.stdout.write(f"Reseteando contraseña para:")
                self.stdout.write(f"  - Usuario: {user.usuario}")
                self.stdout.write(f"  - Empresa: {user.empresa}")
                self.stdout.write(f"  - Municipio: {user.municipio_id}")
                self.stdout.write(f"  - Nombre: {user.nombre}")
                
                # Actualizar contraseña
                user.password = password_hash
                user.save()
                
                self.stdout.write(
                    self.style.SUCCESS("  ✅ Contraseña actualizada")
                )
                self.stdout.write("")
            
            self.stdout.write("=== VERIFICACIÓN ===")
            self.stdout.write("Verificando que todas las contraseñas funcionan...")
            
            for user in usuarios:
                user.refresh_from_db()
                if user.password == password_hash:
                    self.stdout.write(
                        self.style.SUCCESS(f"✅ {user.usuario} - Contraseña correcta")
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f"❌ {user.usuario} - Error en contraseña")
                    )
            
            self.stdout.write("")
            self.stdout.write("=== CREDENCIALES DE ACCESO ===")
            self.stdout.write("Ahora puedes acceder con:")
            self.stdout.write("")
            
            for user in usuarios:
                municipio_codigo = "0301" if user.municipio_id == 2 else "001"
                self.stdout.write(f"Usuario: {user.usuario}")
                self.stdout.write(f"Contraseña: admin123")
                self.stdout.write(f"Municipio: {municipio_codigo}")
                modulo = "Tributario" if user.usuario == "tributario" else "Catastro" if user.usuario == "catastro" else "Otros"
                self.stdout.write(f"Módulo: {modulo}")
                self.stdout.write("-" * 40)
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error: {e}")
            )





