# Script PowerShell para executar backend + frontend
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "       FERRAMENTAS DE REDES - MODO SEPARADO" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Backend (Flask): http://localhost:5000" -ForegroundColor Green
Write-Host "Frontend (Streamlit): http://localhost:8501" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

# Verifica se Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERRO: Python não encontrado. Instale Python primeiro." -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Verifica dependências
Write-Host "🔍 Verificando dependências..." -ForegroundColor Yellow

$dependencies = @("flask", "streamlit", "pyshark")
$missing = @()

foreach ($dep in $dependencies) {
    try {
        python -c "import $dep" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $dep" -ForegroundColor Green
        } else {
            Write-Host "❌ $dep - não encontrado" -ForegroundColor Red
            $missing += $dep
        }
    } catch {
        Write-Host "❌ $dep - não encontrado" -ForegroundColor Red
        $missing += $dep
    }
}

if ($missing.Count -gt 0) {
    Write-Host "⚠️  Dependências faltando: $($missing -join ', ')" -ForegroundColor Yellow
    Write-Host "Execute: pip install -r requirements.txt" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host "✅ Todas as dependências estão instaladas!" -ForegroundColor Green

# Inicia backend
Write-Host "🚀 Iniciando backend Flask..." -ForegroundColor Yellow
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    python backend\server.py
}

# Aguarda um pouco para o backend iniciar
Start-Sleep -Seconds 3

# Verifica se backend iniciou corretamente
if ($backendJob.State -eq "Running") {
    Write-Host "✅ Backend iniciado com sucesso!" -ForegroundColor Green
} else {
    Write-Host "❌ Falha ao iniciar backend" -ForegroundColor Red
    Stop-Job $backendJob -Force
    Remove-Job $backendJob -Force
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Inicia frontend
Write-Host "🌐 Iniciando frontend Streamlit..." -ForegroundColor Yellow
Write-Host "🌐 Acesse: http://localhost:8501" -ForegroundColor Cyan

try {
    streamlit run frontend\app.py --server.port=8501
} finally {
    # Para o backend quando o frontend for fechado
    Write-Host "🛑 Parando backend..." -ForegroundColor Yellow
    Stop-Job $backendJob -Force
    Remove-Job $backendJob -Force
    
    Write-Host "✅ Aplicação finalizada!" -ForegroundColor Green
}
