@echo off
echo ========================================
echo   Iniciando Sistema de Atencion Alcaldia
echo ========================================
echo.

echo Verificando entorno virtual...
if not exist "venv\Scripts\activate.bat" (
    echo Creando entorno virtual...
    python -m venv venv
    echo Instalando dependencias...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

echo.
echo Inicializando base de datos...
python init_db.py

echo.
echo ¿Desea importar datos del respaldo? (sí/no)
set /p importar="> "

if /I "%importar%"=="sí" (
    if /I "%importar%"=="si" (
        python import_data.py
    )
)

echo.
echo ========================================
echo   Iniciando aplicacion en http://localhost:5000
echo ========================================
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python app.py

pause
