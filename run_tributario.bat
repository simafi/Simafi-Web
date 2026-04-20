@echo off
REM Script para ejecutar el proyecto Django Tributario
REM Aplicación renombrada de 'hola' a 'tributario_app'
cd /d "C:\simafiweb\venv\Scripts\tributario"
call "C:\simafiweb\venv\Scripts\activate.bat"
python manage.py runserver 8080
pause 