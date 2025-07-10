# Scripts de Teste - Guia de Uso

## ✅ Scripts Recomendados

### 1. `test_comprehensive.py` - PRINCIPAL
- **Uso:** Teste abrangente de todo o projeto
- **Quando usar:** Para validar se tudo está funcionando
- **Comando:** `python test_comprehensive.py`
- **Funcionalidades:**
  - Testa imports e dependências
  - Verifica privilégios administrativos
  - Testa detecção de interfaces
  - Valida criação do sniffer
  - Verifica fallback subprocess
  - Testa estrutura do projeto
  - Opcionalmente testa backend e frontend

### 2. `test_pre_run.py` - PRÉ-EXECUÇÃO
- **Uso:** Validação rápida antes de executar o app
- **Quando usar:** Antes de rodar `run_integrated.py`
- **Comando:** `python test_pre_run.py`
- **Funcionalidades:**
  - Verifica sintaxe dos arquivos principais
  - Testa imports básicos
  - Validação pré-execução

### 3. `test_sniffer.py` - DEMO
- **Uso:** Demonstração das funcionalidades do sniffer
- **Quando usar:** Para ver exemplo de uso da API
- **Comando:** `python test_sniffer.py`
- **Funcionalidades:**
  - Exemplo prático de uso
  - Demonstra análise de pacotes
  - Mostra estatísticas e exportação

### 4. `test_final.py` - VALIDAÇÃO FINAL
- **Uso:** Teste final de integração
- **Quando usar:** Após configurar tudo
- **Comando:** `python test_final.py`
- **Funcionalidades:**
  - Teste de integração final
  - Valida pipeline completo

## 🚫 Scripts Removidos (eram redundantes)

- `test_backend.py` → Funcionalidade movida para `test_comprehensive.py`
- `test_backend_quick.py` → Redundante com `test_comprehensive.py`
- `test_capture_debug.py` → Funcionalidade incluída em `test_comprehensive.py`
- `test_eventloop.py` → Problema específico já corrigido
- `test_pyshark_direct.py` → Coberto por `test_comprehensive.py`
- `test_quick.py` → Muito básico, substituído por `test_pre_run.py`
- `test_sniffer_basic.py` → Redundante com `test_sniffer.py`

## 🎯 Recomendação de Uso

1. **Primeira execução:**
   ```bash
   python test_comprehensive.py --export
   ```

2. **Antes de executar o app:**
   ```bash
   python test_pre_run.py
   ```

3. **Se tudo estiver OK:**
   ```bash
   python run_integrated.py
   ```

4. **Para ver exemplo de uso da API:**
   ```bash
   python test_sniffer.py
   ```

## 🔍 Falsos Positivos de Lint

Os seguintes erros de lint são **FALSOS POSITIVOS** e podem ser ignorados:

1. **`Import "ferramentas.sniffer.sniffer" could not be resolved`**
   - **Motivo:** O lint não reconhece o path dinâmico adicionado em runtime
   - **Status:** ✅ Funciona corretamente em execução

2. **`Import "netifaces" could not be resolved from source`**
   - **Motivo:** Dependência opcional com fallback
   - **Status:** ✅ Funciona com fallback se não estiver instalado

3. **`os.geteuid()` only available on Unix**
   - **Motivo:** Código tem verificação de plataforma e fallback
   - **Status:** ✅ Funciona corretamente no Windows

4. **`flask.__version__` not found**
   - **Motivo:** Algumas versões do Flask podem não ter este atributo
   - **Status:** ✅ Código tem fallback com `getattr()`

## 📝 Notas

- Todos os scripts têm tratamento de erro robusto
- Scripts de teste não afetam o funcionamento do projeto principal
- Use `test_comprehensive.py` para diagnóstico completo
- Use `test_pre_run.py` para validação rápida
