# 🖥️ Frontend - Aplicação Desktop de Análise Biomecânica

![Status do Projeto](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green)

Uma aplicação desktop desenvolvida em Python (PyQt5) que atua como **frontend** para um sistema de análise biomecânica baseada em IA. A aplicação serve como a interface de controle para o usuário, permitindo execução remota no **Google Colab**, o upload de vídeos, configuração da análise e visualização dos resultados processados na nuvem.

## Funcionalidades

* **Automação de Browser:** Utiliza `undetected-chromedriver` (Selenium) para realizar login e interagir com o Google Colab automaticamente, sem que o usuário precise manipular o notebook manualmente.
* **Conexão via API:** Conecta-se ao backend (geralmente tunelado via Ngrok/Cloudflare) para envio de vídeos e configurações para o servidor via requisições HTTP (`requests`) e recebe os JSONs de resposta.
* **Configuração de Análise:** Permite seleção de vídeo local e escolha da articulação alvo (Joelho, Quadril, Tornozelo, etc.).
* **Monitoramento em Tempo Real:** Barra de progresso e logs de sistema sincronizados com o status do servidor.
* **Galeria de Resultados:** Visualizador de imagens integrado (Carrossel) para inspecionar os gráficos gerados antes de baixar.
* **Exportação:** Download automático dos resultados completos em formato `.zip`.

## Pré-requisitos

Para executar este projeto, você precisará de:

* **Python 3.8** ou superior.
* Navegador **Google Chrome** instalado (para a automação do Colab).
* Bibliotecas Python listadas abaixo:
  - `PyQt5`: Framework da interface gráfica.
  - `requests`: Para comunicação REST com o backend.
  - `undetected-chromedriver`: Para automação do navegador (bypass de detecção de bot do Google).


## Como Usar

### Como Executar a Aplicação
Certifique-se de estar na raiz do projeto antes de rodar o comando:

```bash
python frontend/app.py
```

### Como Gerar Executável (.exe)
Para distribuir a aplicação sem exigir que o usuário final tenha Python instalado:

```bash
python -m pyinstaller --noconsole --onefile --name="Biomech v1.0.0" frontend/app.py
```

### Passo a Passo na Interface

**1. Servidor Remoto**
- Clique em **"LIGAR O COLAB"**. O sistema usará o Selenium para abrir o notebook definido e conectar ao runtime.
- *Nota:* Selecione a opção **"Modo Login"** caso precise inserir suas credenciais do Google manualmente.

**2. Conexão API**
- Insira a URL do túnel gerada pelo Ngrok/Cloudflare (exibida no notebook do Colab após a execução).
- Clique em **"Testar"**. O indicador de status deve ficar **Verde**.

**3. Configuração**
- Clique em **"Selecionar Vídeo"** e escolha seu arquivo `.mp4`.
- Selecione a articulação desejada no menu suspenso (ex: "Joelho").

**4. Controle**
- Clique em **"INICIAR ANÁLISE"**.
- Acompanhe o progresso na barra inferior e na aba **"Logs do Sistema"**.

**5. Visualização e Download**
- Ao finalizar, as imagens de prévia aparecerão na aba **"Galeria / Gráficos"**.
- Clique em **"BAIXAR ARQUIVOS GERADOS (ZIP)"** para salvar o relatório completo.
