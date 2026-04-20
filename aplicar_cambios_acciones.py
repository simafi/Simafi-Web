#!/usr/bin/env python
# -*- coding: utf-8 -*-

archivo = r"venv\Scripts\tributario\tributario_app\templates\actividad.html"

print("Aplicando cambios en sección de acciones...")

with open(archivo, 'r', encoding='utf-8') as f:
    content = f.read()

# Cambiar ancho de columna acciones de 200px a 250px
content = content.replace(
    'text-align: center;\n        width: 200px;',
    'text-align: center;\n        width: 250px;'
)

# Cambiar separación entre botones de 5px a 8px
content = content.replace(
    'margin-right: 5px;',
    'margin-right: 8px;'
)

# Aumentar tamaño de botones pequeños
content = content.replace(
    'padding: 6px 10px;\n        font-size: 0.8rem;\n        min-width: 60px;',
    'padding: 7px 12px;\n        font-size: 0.85rem;\n        min-width: 75px;'
)

with open(archivo, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("✅ Cambios aplicados:")
print("   - Ancho columna acciones: 200px → 250px")
print("   - Separación botones: 5px → 8px")
print("   - Tamaño botones: más grandes y legibles")
print("\n🔄 Recarga el navegador: Ctrl + Shift + F5")





















































