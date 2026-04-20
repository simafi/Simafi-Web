#!/usr/bin/env python3
"""
Script para mejorar el diseño del formulario de tarifas
Aplicando un estilo más moderno, vistoso y gerencial
"""

import os
import shutil
from pathlib import Path

def aplicar_diseno_gerencial_tarifas():
    """Aplicar diseño gerencial moderno al formulario de tarifas"""
    
    template_path = "venv/Scripts/tributario/tributario_app/templates/formulario_tarifas.html"
    
    if not os.path.exists(template_path):
        print("❌ Template de tarifas no encontrado")
        return False
    
    # Crear backup
    backup_path = template_path + ".backup_gerencial"
    shutil.copy2(template_path, backup_path)
    print(f"✅ Backup creado: {backup_path}")
    
    # Leer el contenido actual
    with open(template_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Estilos gerenciales modernos
    estilos_gerenciales = """
        /* Estilos gerenciales modernos para formulario de tarifas */
        
        /* Header gerencial mejorado */
        .header-gerencial {
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #3b82f6 100%);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 40px;
            box-shadow: 
                0 20px 40px rgba(30, 58, 138, 0.3),
                0 10px 20px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .header-gerencial::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="%23ffffff" fill-opacity="0.1" d="M0,96L48,112C96,128,192,160,288,186.7C384,213,480,235,576,213.3C672,192,768,128,864,128C960,128,1056,192,1152,208C1248,224,1344,192,1392,176L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
            background-size: cover;
            background-position: center;
        }
        
        .header-gerencial h1 {
            font-size: 3.5rem;
            margin-bottom: 20px;
            font-weight: 900;
            text-shadow: 
                3px 3px 6px rgba(0, 0, 0, 0.4),
                0 0 30px rgba(255, 255, 255, 0.3);
            position: relative;
            background: linear-gradient(45deg, #fff, #f0f8ff, #e6f3ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: glow 3s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { 
                text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.4), 0 0 30px rgba(255, 255, 255, 0.3);
                filter: brightness(1);
            }
            to { 
                text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.4), 0 0 40px rgba(255, 255, 255, 0.6);
                filter: brightness(1.1);
            }
        }
        
        .header-gerencial .subtitle {
            font-size: 1.6rem;
            opacity: 0.95;
            max-width: 900px;
            margin: 0 auto;
            position: relative;
            font-weight: 400;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            letter-spacing: 0.8px;
            line-height: 1.4;
        }
        
        /* Card gerencial mejorada */
        .card-gerencial {
            background: rgba(255, 255, 255, 0.98);
            border-radius: 25px;
            box-shadow: 
                0 25px 50px rgba(0, 0, 0, 0.15),
                0 15px 30px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.9);
            padding: 45px;
            margin-bottom: 40px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(15px);
            position: relative;
            overflow: hidden;
        }
        
        .card-gerencial::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #1e3a8a, #1e40af, #3b82f6, #60a5fa);
            border-radius: 25px 25px 0 0;
        }
        
        .card-gerencial:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 
                0 35px 70px rgba(0, 0, 0, 0.2),
                0 20px 40px rgba(0, 0, 0, 0.15),
                inset 0 1px 0 rgba(255, 255, 255, 0.9);
        }
        
        /* Título del formulario gerencial */
        .titulo-formulario-gerencial {
            font-size: 2.2rem;
            color: #1e3a8a;
            margin-bottom: 35px;
            font-weight: 800;
            text-align: center;
            position: relative;
            padding-bottom: 20px;
        }
        
        .titulo-formulario-gerencial::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 4px;
            background: linear-gradient(90deg, #1e3a8a, #3b82f6);
            border-radius: 2px;
            box-shadow: 0 2px 8px rgba(30, 58, 138, 0.3);
        }
        
        /* Formulario gerencial */
        .formulario-gerencial {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 
                0 15px 30px rgba(0, 0, 0, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 0.8);
            border: 1px solid rgba(226, 232, 240, 0.8);
            position: relative;
        }
        
        .formulario-gerencial::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 20%, rgba(59, 130, 246, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(30, 58, 138, 0.05) 0%, transparent 50%);
            border-radius: 20px;
            pointer-events: none;
        }
        
        /* Grid gerencial mejorado */
        .form-grid-gerencial {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 35px;
        }
        
        /* Form groups gerenciales */
        .form-group-gerencial {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 16px;
            box-shadow: 
                0 8px 20px rgba(0, 0, 0, 0.06),
                0 4px 10px rgba(0, 0, 0, 0.04);
            padding: 25px;
            margin-bottom: 0;
            border: 1px solid rgba(226, 232, 240, 0.6);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .form-group-gerencial::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, #1e3a8a, #3b82f6);
            border-radius: 16px 16px 0 0;
        }
        
        .form-group-gerencial:hover {
            transform: translateY(-3px);
            box-shadow: 
                0 12px 25px rgba(0, 0, 0, 0.1),
                0 6px 15px rgba(0, 0, 0, 0.06);
            border-color: rgba(59, 130, 246, 0.3);
        }
        
        /* Labels gerenciales */
        .label-gerencial {
            display: block !important;
            margin-bottom: 15px !important;
            font-weight: 800 !important;
            color: #1e3a8a !important;
            font-size: 1.1rem !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            position: relative !important;
            padding-left: 35px !important;
        }
        
        .label-gerencial::before {
            content: '' !important;
            position: absolute !important;
            left: 0 !important;
            top: 50% !important;
            transform: translateY(-50%) !important;
            width: 8px !important;
            height: 25px !important;
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
            border-radius: 4px !important;
            box-shadow: 0 3px 6px rgba(30, 58, 138, 0.4) !important;
        }
        
        .label-gerencial::after {
            content: '' !important;
            position: absolute !important;
            bottom: -5px !important;
            left: 35px !important;
            width: 40px !important;
            height: 3px !important;
            background: linear-gradient(90deg, #1e3a8a, #3b82f6) !important;
            border-radius: 2px !important;
        }
        
        /* Inputs gerenciales */
        .input-gerencial {
            width: 100% !important;
            padding: 18px 25px !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 14px !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
            box-shadow: 
                0 4px 12px rgba(0, 0, 0, 0.06),
                inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
            color: #1e293b !important;
        }
        
        .input-gerencial:focus {
            outline: none !important;
            border-color: #3b82f6 !important;
            box-shadow: 
                0 0 0 5px rgba(59, 130, 246, 0.15),
                0 8px 20px rgba(59, 130, 246, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
            background: #ffffff !important;
            transform: translateY(-2px) !important;
        }
        
        .input-gerencial:hover {
            border-color: #93c5fd !important;
            box-shadow: 
                0 6px 16px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
        }
        
        /* Selects gerenciales */
        .select-gerencial {
            cursor: pointer !important;
            background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath fill='none' stroke='%231e3a8a' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m2 5 6 6 6-6'/%3E%3C/svg%3E") !important;
            background-repeat: no-repeat !important;
            background-position: right 15px center !important;
            background-size: 18px 14px !important;
            padding-right: 45px !important;
            appearance: none !important;
        }
        
        .select-gerencial:focus {
            background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath fill='none' stroke='%233b82f6' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m2 5 6 6 6-6'/%3E%3C/svg%3E") !important;
        }
        
        /* Textos de ayuda gerenciales */
        .texto-ayuda-gerencial {
            color: #64748b !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            display: block !important;
            margin-top: 12px !important;
            padding: 12px 16px !important;
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%) !important;
            border-radius: 10px !important;
            border-left: 4px solid #3b82f6 !important;
            box-shadow: 
                0 2px 6px rgba(0, 0, 0, 0.06),
                inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
            position: relative;
        }
        
        .texto-ayuda-gerencial::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, #1e3a8a, #3b82f6);
            border-radius: 10px 0 0 10px;
        }
        
        .texto-ayuda-gerencial i {
            color: #3b82f6 !important;
            margin-right: 8px !important;
            font-size: 1rem !important;
        }
        
        /* Botones gerenciales */
        .btn-gerencial {
            padding: 16px 32px;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            min-width: 140px;
            justify-content: center;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            position: relative;
            overflow: hidden;
        }
        
        .btn-gerencial::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s;
        }
        
        .btn-gerencial:hover::before {
            left: 100%;
        }
        
        .btn-gerencial-success {
            background: linear-gradient(135deg, #059669 0%, #10b981 100%);
            color: white;
        }
        
        .btn-gerencial-success:hover {
            background: linear-gradient(135deg, #047857 0%, #059669 100%);
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 20px rgba(5, 150, 105, 0.4);
        }
        
        .btn-gerencial-warning {
            background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%);
            color: white;
        }
        
        .btn-gerencial-warning:hover {
            background: linear-gradient(135deg, #b45309 0%, #d97706 100%);
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 20px rgba(217, 119, 6, 0.4);
        }
        
        .btn-gerencial-secondary {
            background: linear-gradient(135deg, #475569 0%, #64748b 100%);
            color: white;
        }
        
        .btn-gerencial-secondary:hover {
            background: linear-gradient(135deg, #334155 0%, #475569 100%);
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 20px rgba(71, 85, 105, 0.4);
        }
        
        /* Acciones del formulario gerencial */
        .form-actions-gerencial {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 40px;
            flex-wrap: wrap;
        }
        
        /* Responsive gerencial */
        @media (max-width: 768px) {
            .header-gerencial h1 {
                font-size: 2.5rem;
            }
            
            .header-gerencial .subtitle {
                font-size: 1.2rem;
            }
            
            .form-grid-gerencial {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            .form-actions-gerencial {
                flex-direction: column;
                align-items: center;
            }
            
            .btn-gerencial {
                width: 100%;
                max-width: 300px;
            }
        }
    """
    
    # Buscar la sección de estilos y agregar los nuevos
    inicio_estilos = contenido.find('<style>')
    fin_estilos = contenido.find('</style>')
    
    if inicio_estilos != -1 and fin_estilos != -1:
        contenido_antes = contenido[:inicio_estilos + 7]
        contenido_despues = contenido[fin_estilos:]
        estilos_existentes = contenido[inicio_estilos + 7:fin_estilos]
        
        nuevos_estilos = estilos_existentes + estilos_gerenciales
        contenido_nuevo = contenido_antes + nuevos_estilos + contenido_despues
        
        # Escribir el archivo actualizado
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(contenido_nuevo)
        
        print("✅ Estilos gerenciales aplicados al formulario de tarifas")
        return True
    else:
        print("❌ No se encontró la sección de estilos")
        return False

def actualizar_html_gerencial():
    """Actualizar el HTML del formulario con clases gerenciales"""
    
    template_path = "venv/Scripts/tributario/tributario_app/templates/formulario_tarifas.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Reemplazar el header con versión gerencial
    header_antiguo = '''        <header>
            <h1><i class="fas fa-dollar-sign"></i> Gestión de Tarifas</h1>
            <p class="subtitle">Configure las tarifas municipales para los diferentes rubros y servicios</p>
        </header>'''
    
    header_gerencial = '''        <header class="header-gerencial">
            <h1><i class="fas fa-chart-line"></i> Gestión Ejecutiva de Tarifas</h1>
            <p class="subtitle">Sistema de administración y control gerencial de tarifas municipales</p>
        </header>'''
    
    contenido = contenido.replace(header_antiguo, header_gerencial)
    
    # Reemplazar la card del formulario
    card_antigua = '''        <!-- Formulario de Tarifas -->
        <div class="card">
            <h2><i class="fas fa-edit"></i> Formulario de Tarifas</h2>
            <form method="post" id="tarifas-form" style="background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">'''
    
    card_gerencial = '''        <!-- Formulario de Tarifas Gerencial -->
        <div class="card-gerencial">
            <h2 class="titulo-formulario-gerencial"><i class="fas fa-cogs"></i> Panel de Configuración Gerencial</h2>
            <form method="post" id="tarifas-form" class="formulario-gerencial">'''
    
    contenido = contenido.replace(card_antigua, card_gerencial)
    
    # Actualizar el grid del formulario
    grid_antiguo = '''                <div class="form-grid" style="display: grid; grid-template-columns: 1fr 3fr; gap: 20px; margin-bottom: 25px;">'''
    
    grid_gerencial = '''                <div class="form-grid-gerencial">'''
    
    contenido = contenido.replace(grid_antiguo, grid_gerencial)
    
    # Actualizar form groups
    contenido = contenido.replace('class="form-group form-group-empresa"', 'class="form-group-gerencial"')
    contenido = contenido.replace('class="form-group form-group-rubro"', 'class="form-group-gerencial"')
    contenido = contenido.replace('class="form-group form-group-ano"', 'class="form-group-gerencial"')
    contenido = contenido.replace('class="form-group form-group-codigo"', 'class="form-group-gerencial"')
    contenido = contenido.replace('class="form-group form-group-descripcion"', 'class="form-group-gerencial"')
    contenido = contenido.replace('class="form-group form-group-valor"', 'class="form-group-gerencial"')
    contenido = contenido.replace('class="form-group form-group-frecuencia"', 'class="form-group-gerencial"')
    contenido = contenido.replace('class="form-group form-group-tipo"', 'class="form-group-gerencial"')
    contenido = contenido.replace('class="form-group form-group-categoria"', 'class="form-group-gerencial"')
    
    # Actualizar labels
    contenido = contenido.replace('style="display: block !important; margin-bottom: 10px !important; font-weight: 700 !important; color: #1e40af !important; font-size: 1rem !important; text-transform: uppercase !important; letter-spacing: 0.5px !important;"', 'class="label-gerencial"')
    
    # Actualizar inputs
    contenido = contenido.replace('{{ form.empresa }}', '{{ form.empresa|add_class:"input-gerencial" }}')
    contenido = contenido.replace('{{ form.rubro }}', '{{ form.rubro|add_class:"input-gerencial select-gerencial" }}')
    contenido = contenido.replace('{{ form.ano }}', '{{ form.ano|add_class:"input-gerencial" }}')
    contenido = contenido.replace('{{ form.cod_tarifa }}', '{{ form.cod_tarifa|add_class:"input-gerencial" }}')
    contenido = contenido.replace('{{ form.descripcion }}', '{{ form.descripcion|add_class:"input-gerencial" }}')
    contenido = contenido.replace('{{ form.valor }}', '{{ form.valor|add_class:"input-gerencial" }}')
    contenido = contenido.replace('{{ form.frecuencia }}', '{{ form.frecuencia|add_class:"input-gerencial select-gerencial" }}')
    contenido = contenido.replace('{{ form.tipo }}', '{{ form.tipo|add_class:"input-gerencial select-gerencial" }}')
    contenido = contenido.replace('{{ form.categoria }}', '{{ form.categoria|add_class:"input-gerencial select-gerencial" }}')
    
    # Actualizar textos de ayuda
    contenido = contenido.replace('style="color: #64748b !important; font-size: 0.875rem !important; font-weight: 500 !important; display: block !important; margin-top: 8px !important; padding: 8px 12px !important; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important; border-radius: 6px !important; border-left: 3px solid #3b82f6 !important; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;"', 'class="texto-ayuda-gerencial"')
    
    # Actualizar botones
    contenido = contenido.replace('class="form-actions"', 'class="form-actions-gerencial"')
    contenido = contenido.replace('class="btn btn-success"', 'class="btn-gerencial btn-gerencial-success"')
    contenido = contenido.replace('class="btn btn-warning"', 'class="btn-gerencial btn-gerencial-warning"')
    contenido = contenido.replace('class="btn btn-secondary"', 'class="btn-gerencial btn-gerencial-secondary"')
    
    # Escribir el archivo actualizado
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print("✅ HTML actualizado con clases gerenciales")
    return True

def main():
    """Función principal"""
    print("🎨 APLICANDO DISEÑO GERENCIAL MODERNO AL FORMULARIO DE TARIFAS")
    print("=" * 70)
    
    # Aplicar estilos gerenciales
    if aplicar_diseno_gerencial_tarifas():
        print("✅ Estilos gerenciales aplicados")
        
        # Actualizar HTML
        if actualizar_html_gerencial():
            print("✅ HTML actualizado con clases gerenciales")
            
            print("\n🎉 DISEÑO GERENCIAL APLICADO EXITOSAMENTE")
            print("El formulario de tarifas ahora tiene un diseño:")
            print("• Más moderno y profesional")
            print("• Vistoso con gradientes y efectos")
            print("• Gerencial con elementos ejecutivos")
            print("• Responsive y accesible")
            
        else:
            print("❌ Error al actualizar HTML")
    else:
        print("❌ Error al aplicar estilos gerenciales")

if __name__ == "__main__":
    main()














