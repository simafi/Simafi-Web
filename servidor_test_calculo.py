#!/usr/bin/env python
"""
Servidor simple para probar el cálculo automático ICS
"""

import http.server
import socketserver
import os
import webbrowser
from urllib.parse import urlparse

class TestCalculoHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Servir archivos estáticos
        if self.path == '/':
            self.path = '/test_calculo_automatico.html'
        elif self.path == '/test':
            self.path = '/test_calculo_automatico.html'
        
        return super().do_GET()

def iniciar_servidor_test():
    """
    Inicia servidor de prueba para el cálculo automático
    """
    print("🧪 INICIANDO SERVIDOR TEST CÁLCULO AUTOMÁTICO")
    print("=" * 50)
    
    # Cambiar al directorio del proyecto
    os.chdir(r'c:\simafiweb')
    
    # Configurar servidor
    PORT = 8888
    
    try:
        with socketserver.TCPServer(("", PORT), TestCalculoHandler) as httpd:
            print(f"✅ Servidor iniciado en puerto {PORT}")
            print(f"🌐 URL de prueba: http://localhost:{PORT}/test")
            print()
            print("📋 FUNCIONALIDADES DEL TEST:")
            print("   • Formulario con campos de ventas")
            print("   • Cálculo automático al escribir valores")
            print("   • Campo 'impuesto' mapeado a tabla 'declara'")
            print("   • Casos de prueba predefinidos")
            print("   • Log de cálculos en tiempo real")
            print("   • Desglose por tipos de venta")
            print()
            print("🎯 CASOS DE PRUEBA INCLUIDOS:")
            print("   1. Rango Bajo: $500,000")
            print("   2. Rango Medio: $7,500,000") 
            print("   3. Rango Alto: $25,000,000")
            print()
            print("⚡ INSTRUCCIONES:")
            print("   1. Abra http://localhost:8888/test en su navegador")
            print("   2. Ingrese valores en campos verdes")
            print("   3. Observe el cálculo automático")
            print("   4. Verifique que el campo 'impuesto' se actualiza")
            print()
            print("🛑 Presione Ctrl+C para detener el servidor")
            print("=" * 50)
            
            # Intentar abrir navegador automáticamente
            try:
                webbrowser.open(f'http://localhost:{PORT}/test')
                print("🌐 Navegador abierto automáticamente")
            except:
                print("⚠️  Abra manualmente: http://localhost:8888/test")
            
            # Servir indefinidamente
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error al iniciar servidor: {e}")
        print("💡 Verifique que el puerto 8888 esté disponible")

if __name__ == "__main__":
    iniciar_servidor_test()
