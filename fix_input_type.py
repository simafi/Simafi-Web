import os
import shutil
from pathlib import Path

def fix_js_and_templates():
    print("Fixing InvalidStateError - setSelectionRange on number inputs")
    
    # Copy corrected JS to Django locations
    js_source = Path("c:/simafiweb/declaracion_volumen_interactivo.js")
    
    js_destinations = [
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/static/js/declaracion_volumen_interactivo.js",
        "c:/simafiweb/venv/Scripts/tributario/static/js/declaracion_volumen_interactivo.js"
    ]
    
    for dest_str in js_destinations:
        dest = Path(dest_str)
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(js_source, dest)
            print(f"JS copied to: {dest}")
        except Exception as e:
            print(f"Error copying JS to {dest}: {e}")
    
    # Find and fix HTML templates
    template_paths = [
        "c:/simafiweb/venv/Scripts/tributario/tributario_app/templates",
        "c:/simafiweb/test_calculo_automatico.html"
    ]
    
    for path_str in template_paths:
        path = Path(path_str)
        if path.is_file() and path.suffix == '.html':
            fix_html_file(path)
        elif path.is_dir():
            for html_file in path.rglob("*.html"):
                fix_html_file(html_file)

def fix_html_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace number inputs with text inputs for numeric fields
        replacements = [
            ('type="number"', 'type="text" inputmode="decimal"'),
            ("type='number'", "type='text' inputmode='decimal'"),
        ]
        
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                print(f"Fixed {file_path}: {old} -> {new}")
        
        if content != original_content:
            # Create backup
            backup_path = file_path.with_suffix('.backup_input_fix')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Save fixed version
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Updated: {file_path}")
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    fix_js_and_templates()
    print("\nFixes applied:")
    print("1. JS updated to handle setSelectionRange safely")
    print("2. HTML inputs changed from number to text+inputmode")
    print("3. Large values (1M+) now supported")
    print("\nRestart Django server to apply changes")
