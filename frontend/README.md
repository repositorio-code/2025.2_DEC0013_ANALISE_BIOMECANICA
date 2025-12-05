# Interface Desktop de Análise Biomecânica 🏃‍♂️📊

![Status do Projeto](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green)

Uma aplicação desktop desenvolvida em Python (PyQt5) que atua como **frontend** para um sistema de análise biomecânica baseada em IA. O sistema orquestra a execução remota no **Google Colab**, gerencia o upload de vídeos, monitora o progresso da análise e visualiza os resultados processados.

## 📋 Funcionalidades

* **Automação de Boot (Colab):** Inicia automaticamente o notebook do Google Colab via Selenium (Modo Headless ou Interface Gráfica).
* **Conexão via API:** Conecta-se ao backend (geralmente tunelado via Ngrok) para envio de comandos.
* **Configuração de Análise:** Permite seleção de vídeo local e escolha da articulação alvo (Joelho, Quadril, Tornozelo, etc.).
* **Monitoramento em Tempo Real:** Barra de progresso e logs de sistema sincronizados com o status do servidor.
* **Galeria de Resultados:** Visualizador de imagens integrado (Carrossel) para inspecionar os gráficos gerados antes de baixar.
* **Exportação:** Download automático dos resultados completos em formato `.zip`.

## 🛠️ Pré-requisitos

Para executar este projeto, você precisará de:

* **Python 3.8** ou superior.
* Navegador **Google Chrome** instalado (para a automação do Colab).
* Bibliotecas Python listadas abaixo.


## 🚀 Como Usar
Execute o arquivo principal da interface:

```bash
python app.py
```
  
Passo a Passo na Interface:<br>
0. Servidor Remoto:
  - Clique em "LIGAR O COLAB". O sistema usará o Selenium para abrir o notebook definido e conectar ao runtime.
  - Nota: Selecione "Modo Login" se precisar inserir credenciais do Google manualmente.
<br>1. Conexão API:
  - Insira a URL gerada pelo Ngrok (exibida no notebook do Colab após a execução).
  - Clique em "Testar". A luz deve ficar Verde.

2. Configuração:
  - Clique em "Selecionar Vídeo" e escolha seu arquivo .mp4.
  - Selecione a articulação desejada no menu (ex: "Joelho").

3. Controle:
  - Clique em "INICIAR ANÁLISE".
  - Acompanhe o progresso na barra inferior e na aba "Logs do Sistema".

Visualização e Download:
  - Ao finalizar, as imagens de prévia aparecerão na aba "Galeria / Gráficos".
  - Clique em "BAIXAR ARQUIVOS GERADOS (ZIP)" para salvar o relatório completo.

enharia de Computação
