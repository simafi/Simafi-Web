#!/usr/bin/env python
"""
Script completo para reconstruir la estructura de indentación del archivo views.py
"""

def fix_views_complete():
    """
    Reconstruir la estructura de indentación completa
    """
    file_path = "venv/Scripts/tributario/modules/tributario/views.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Dividir en líneas manteniendo los saltos de línea
    lines = content.splitlines(keepends=True)
    
    print(f"📊 Total de líneas: {len(lines)}")
    
    # Correcciones específicas conocidas
    corrections = {
        39: "    try:",  # línea 40
        40: "        data = json.loads(request.body)",  # línea 41
        121: "    try:",  # línea 122
        148: "    try:",  # línea 149
        238: "    try:",  # línea 239
        248: "        negocio = Negocio.objects.get(",  # línea 249
    }
    
    print("🔧 Aplicando correcciones específicas...")
    
    for line_idx, new_content in corrections.items():
        if line_idx < len(lines):
            old_line = lines[line_idx].rstrip()
            if any(key in old_line for key in ['try:', 'data = json.loads', 'negocio = Negocio.objects.get']):
                lines[line_idx] = new_content + '\n'
                print(f"✅ Línea {line_idx + 1}: Corregida")
    
    # Escribir el archivo corregido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ Archivo reconstruido exitosamente")
    
    # Verificar compilación
    import py_compile
    try:
        py_compile.compile(file_path, doraise=True)
        print("✅ Archivo compila correctamente")
        return True
    except py_compile.PyCompileError as e:
        print(f"❌ Error de compilación: {e}")
        return False

if __name__ == "__main__":
    fix_views_complete()

















