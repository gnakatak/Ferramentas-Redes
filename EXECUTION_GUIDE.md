# Scripts de Execução - Guia Consolidado

## 🎯 Scripts Recomendados de Execução

### 1. `run_integrated.py` - PRINCIPAL (Recomendado)
- **Uso:** Executa apenas o sniffer integrado (Streamlit + PyShark)
- **Dependências:** Mínimas (`streamlit`, `pyshark`, `pandas`)
- **Comando:** `python run_integrated.py`
- **Vantagens:**
  - ✅ Mais simples e estável
  - ✅ Menos dependências
  - ✅ Mais rápido
  - ✅ Sem comunicação HTTP
  - ✅ Interface única e focada
- **Quando usar:** Para a maioria dos casos

### 2. `run_admin.py` - ADMINISTRADOR (Windows)
- **Uso:** Força execução como administrador e roda o sniffer
- **Plataforma:** Windows apenas
- **Comando:** `python run_admin.py`
- **Funcionalidades:**
  - ✅ Solicita privilégios administrativos automaticamente
  - ✅ Executa `run_integrated.py` como admin
  - ✅ Trata erros de privilégios
- **Quando usar:** No Windows, quando você não está como admin

### 3. `run_all.py` - ARQUITETURA COMPLETA
- **Uso:** Executa backend Flask + frontend Streamlit separados
- **Dependências:** Todas (`flask`, `streamlit`, etc.)
- **Comando:** `python run_all.py`
- **Funcionalidades:**
  - ⚠️ Executa servidor Flask backend
  - ⚠️ Executa cliente Streamlit frontend
  - ⚠️ Comunicação via HTTP entre eles
- **Quando usar:** Para arquitetura cliente-servidor completa

### 4. `run_all_improved.py` - VERSÃO MELHORADA
- **Uso:** Versão aprimorada do `run_all.py`
- **Dependências:** Todas (`flask`, `streamlit`, etc.)
- **Comando:** `python run_all_improved.py`
- **Vantagens sobre `run_all.py`:**
  - ✅ Melhor tratamento de erros
  - ✅ Monitoramento de processos
  - ✅ Cleanup automático
  - ✅ Logs mais informativos
- **Quando usar:** Se precisar da arquitetura completa com mais robustez

## 🚀 Recomendação de Uso

### Para a maioria dos usuários:
```bash
# Teste primeiro (opcional)
python test_pre_run.py

# Execute o sniffer integrado
python run_integrated.py
```

### No Windows sem privilégios admin:
```bash
# Força execução como admin
python run_admin.py
```

### Para desenvolvimento/arquitetura completa:
```bash
# Versão melhorada da arquitetura completa
python run_all_improved.py
```

## 📋 Comparação dos Scripts

| Script | Complexidade | Dependências | Estabilidade | Uso Recomendado |
|--------|-------------|-------------|-------------|----------------|
| `run_integrated.py` | ⭐ Simples | ⭐ Mínimas | ⭐⭐⭐ Alta | 🎯 Principal |
| `run_admin.py` | ⭐ Simples | ⭐ Mínimas | ⭐⭐⭐ Alta | 🔒 Windows Admin |
| `run_all.py` | ⭐⭐ Média | ⭐⭐⭐ Muitas | ⭐⭐ Média | 🏗️ Arquitetura básica |
| `run_all_improved.py` | ⭐⭐⭐ Alta | ⭐⭐⭐ Muitas | ⭐⭐⭐ Alta | 🚀 Arquitetura avançada |

## 🔧 Configuração de Dependências

### Para `run_integrated.py` (Recomendado):
```bash
pip install -r requirements_integrated.txt
```

### Para `run_all.py` ou `run_all_improved.py`:
```bash
pip install -r requirements.txt
```

## 🐛 Solução de Problemas

### Problema: "Erro de privilégios administrativos"
- **Solução:** Use `run_admin.py` no Windows ou `sudo` no Linux/Mac

### Problema: "PyShark não funciona"
- **Solução:** Instale Npcap (Windows) ou verifique permissões (Linux/Mac)

### Problema: "Frontend não conecta com backend"
- **Solução:** Use `run_integrated.py` em vez de `run_all.py`

### Problema: "Muitas dependências"
- **Solução:** Use `run_integrated.py` que tem dependências mínimas

## 📝 Notas de Implementação

1. **`run_integrated.py`** é o mais estável e recomendado
2. **`run_admin.py`** é específico para Windows
3. **`run_all.py`** mantido para compatibilidade
4. **`run_all_improved.py`** é a versão robusta da arquitetura completa

## 🎯 Decisão Rápida

**Novo no projeto?** → Use `run_integrated.py`
**Windows sem admin?** → Use `run_admin.py`
**Desenvolvimento?** → Use `run_all_improved.py`
**Demonstração?** → Use `run_integrated.py`
