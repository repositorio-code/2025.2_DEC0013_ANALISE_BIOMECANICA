# 🤖 Automação do Google Colab (Selenium)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-Finalizado-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

Este diretório contém o módulo responsável pela orquestração automática do ambiente de execução no Google Colab. O script colab_manager.py utiliza técnicas de automação de navegador para iniciar, autenticar e executar notebooks remotamente, atuando como o "motor" que liga o servidor backend.

## Sobre o Script
O GerenciadorColab foi desenhado para resolver a fricção de ter que abrir o navegador manualmente, logar e clicar em "Executar tudo". Ele utiliza o undetected-chromedriver, uma versão modificada do Selenium Driver otimizada para evitar a detecção de bots por serviços do Google (Cloudflare/recaptcha).

## Principais Funcionalidades
- Detecção Automática do Chrome (Windows): Verifica o registro do Windows para identificar a versão instalada do Google Chrome e baixar o driver compatível automaticamente.
- Persistência de Sessão: Cria e mantém uma pasta local (chrome_profile_auth) para salvar cookies e dados de sessão.
- Benefício: Você só precisa fazer login na primeira vez. Nas próximas, o sistema entra automaticamente.
- Bypass de Pop-ups: Utiliza injeção de comandos de teclado (TAB + TAB + ENTER) para aceitar automaticamente avisos como "Este notebook não é de autoria do Google" ou "Executar mesmo assim".
- Execução Remota: Envia o atalho CTRL + F9 para o navegador para disparar a execução de todas as células.

## Dependências
O script depende das seguintes bibliotecas (já incluídas no requirements.txt raiz):

```bash
pip install undetected-chromedriver selenium
```
> Requisito do Sistema: É obrigatório ter o navegador Google Chrome instalado na máquina.

Como Utilizar
Este módulo é importado e instanciado pelo app.py principal, mas pode ser testado isoladamente:

```Python
from colab_manager import GerenciadorColab

# URL do seu notebook (backend)
url = "https://colab.research.google.com/drive/SEU_ID_DO_NOTEBOOK"

# Instancia o gerenciador (modo_oculto=False para ver o navegador)
bot = GerenciadorColab(colab_url=url, modo_oculto=False)

try:
    # Inicia o processo
    mensagens = bot.start_colab()
    print(mensagens)
except Exception as e:
    print(f"Erro: {e}")
```

## Comportamento do Script
- Primeiro Acesso: O navegador abrirá e pedirá login no Google. Faça o login manualmente. O script aguardará.
- Sessão Salva: O script cria uma pasta chrome_profile_auth localmente. Nas próximas vezes, o login será automático.
- Execução: O script envia o comando de "Executar Tudo" e tenta fechar automaticamente os avisos de "Notebook não autoral" ou "Executar assim mesmo".

## Detalhes Técnicos de Implementação

### 1. Perfil de Usuário (`chrome_profile_auth`)
O script cria uma pasta no diretório de execução para armazenar o perfil do Chrome, garantindo a persistência da sessão.

> **⚠️ SEGURANÇA:** Esta pasta contém **cookies de autenticação sensíveis**.
> <br>Nunca suba esta pasta para o GitHub. Certifique-se de adicionar `chrome_profile_auth/` ao seu arquivo `.gitignore`.

### 2. A Lógica do "Teclado Cego"
Para clicar no botão *"Executar assim mesmo"* (que aparece em pop-ups dinâmicos do Google, difíceis de mapear via seletores CSS), o script utiliza a biblioteca `ActionChains` para simular a navegação física:

1.  ⏳ **Aguardar:** O script pausa para o pop-up carregar.
2.  Start **TAB:** Foca no primeiro elemento (geralmente "Cancelar").
3.  Start **TAB:** Move o foco para o botão de confirmação.
4.  Start **ENTER:** Confirma a ação.

### 3. Tratamento de Versão (Windows Registry)
O método interno `_obter_versao_chrome_instalada` previne erros de driver varrendo chaves específicas do registro do Windows:

- **Chave:** `Software\Google\Chrome\BLBeacon`
- **Objetivo:** Garante que o `undetected-chromedriver` utilize a versão exata do binário correspondente ao Chrome instalado na máquina, evitando falhas de incompatibilidade.

## Solução de Problemas Comuns

| Problema | Causa Provável | Solução |
| :--- | :--- | :--- |
| **Navegador abre e fecha rápido** | Versão do Chrome incompatível ou erro de driver. | Atualize seu Google Chrome para a última versão disponível. |
| **Login pede confirmação 2FA** | Primeira execução na máquina ou IP novo. | Realize o login manualmente na janela que abrir. O script aguardará você terminar. |
| **Pop-up não fecha** | O Google mudou o layout do aviso/botão. | Pode ser necessário ajustar a sequência de `TABs` no código (`ActionChains`). |
| **Erro "Chrome not reachable"** | O processo do Chrome travou em background. | Finalize todas as tarefas do Chrome no **Gerenciador de Tarefas** e tente novamente. |
