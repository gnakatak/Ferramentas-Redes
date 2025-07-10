@echo off
REM Script para executar backend + frontend no Windows
echo ============================================================
echo        FERRAMENTAS DE REDES - MODO SEPARADO
echo ============================================================
echo Backend (Flask): http://localhost:5000
echo Frontend (Streamlit): http://localhost:8501
echo ============================================================

REM Verifica se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado. Instale Python primeiro.
    pause
    exit /b 1
)

REM Verifica se as dependências estão instaladas
echo Verificando dependencias...
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Flask nao encontrado. Execute: pip install -r requirements.txt
    pause
    exit /b 1
)

python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Streamlit nao encontrado. Execute: pip install -r requirements.txt
    pause
    exit /b 1
)

echo Dependencias OK!

REM Inicia backend em background
echo Iniciando backend Flask...
start "Backend Flask" /MIN cmd /c "python backend\server.py"

REM Aguarda um pouco para o backend iniciar
timeout /t 3 /nobreak >nul

REM Inicia frontend
echo Iniciando frontend Streamlit...
echo Acesse: http://localhost:8501
streamlit run frontend\app.py --server.port=8501

REM Quando o frontend for fechado, tentamos parar o backend
echo Parando processos...
taskkill /F /IM python.exe >nul 2>&1
echo Finalizado!
pause
