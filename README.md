# Análise Biomecânica
> Aplicação de Análise Biomecânica Remota via Visão Computacional 
> <br>Solução híbrida Client-Server para processamento de marcha e cinemática utilizando Google Colab e Interface Desktop.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-Finalizado-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

## 📋 Visão Geral Sobre o Projeto

Este projeto foi desenvolvido no contexto acadêmico de Engenharia de Computação (UFSC) na disciplina de **Projeto Integrador I**. Consiste em uma **aplicação desktop (GUI)** que atua como *frontend* para um notebook de análise biomecânica de alto desempenho hospedado no **Google Colab**. 

O objetivo é democratizar o acesso a algoritmos avançados de visão computacional e biomecânica, encapsulando a complexidade do código Python em uma interface amigável, permitindo que usuários com computadores modestos utilizem o poder de processamento (GPUs) do Google Colab. A comunicação é realizada via API REST, utilizando um túnel de conexão para ligar a máquina local ao ambiente de nuvem. usuários com computadores modestos utilizem o poder de processamento (GPUs) do Google Colab.

## 🎯 O Problema

Notebooks Python (Jupyter/Colab) são ferramentas excelentes para desenvolvimento e pesquisa, mas apresentam uma **alta barreira de entrada** para usuários finais, como fisioterapeutas e profissionais de educação física.

A necessidade de rodar células de código, configurar ambientes e gerenciar dependências torna o uso prático inviável em um ambiente clínico.

## 🚀 A Solução

Desenvolvemos uma arquitetura híbrida (**Desktop + Colab**):
1.  **Backend (Google Colab):** Onde ocorre o processamento pesado (Machine Learning/Visão Computacional). O notebook expõe endpoints via API.
2.  **Túnel (Ngrok/Cloudflared):** Expõe a porta do Colab para a internet segura.
3.  **Frontend (Desktop App):** Uma aplicação executável (.exe) onde o usuário carrega vídeos, clica em "Analisar" e visualiza os relatórios.

> **Resultado:** O profissional tem o poder da nuvem com a simplicidade de um software nativo.

## 🎯 Funcionalidades Principais

- ✅ Processamento em Nuvem: Executa algoritmos pesados (MeTRAbs, JAX, MuJoCo) em GPUs T4 no Google Colab.
- ✅ Cliente Desktop Amigável: Interface local em PyQt5 para gerenciamento de tarefas.
- ✅ Automação Total: Script Selenium (undetected-chromedriver) que liga e configura o servidor Colab automaticamente.
- ✅ Análise Flexível: Seleção dinâmica de articulações (Joelho, Quadril, Tornozelo, Membros Superiores).
- ✅ Relatórios Completos: Gera gráficos de ângulos, fases da marcha, erro de Kalman e vídeo com overlay do esqueleto.

## 🏗️ Arquitetura do Sistema

O sistema opera em uma arquitetura híbrida Cliente-Servidor via túnel HTTP seguro (ngrok por padão).

<img width="480" height="280" alt="image (1)" src="https://github.com/user-attachments/assets/dd0bfeb2-e0ad-4293-939c-f4487950c8a6" />

## Estrutura do Código

```
2025.2_DEC0013_ANALISE_BIOMECANICA/
├── 📁 backend/                 # Código do lado do Servidor (Nuvem)
│   └── 📄 server.ipynb         # Notebook Colab (FastAPI + AI Models)
├── 📁 frontend/                # Aplicação Desktop (Local)
│   ├── 📄 main.py              # Interface Gráfica (PyQt5)
├── 📁 script/                  # Código do lado do Servidor (Nuvem)
│   ├── 📄 colab_manager.py     # Automação do Browser (Selenium)
├── 📄 requirements.txt         # Dependências locais
└── 📄 README.md                # Documentação
```

## Configuração do Ambiente

1. Preparação Inicial (Cliente)
```bash
# Clonar o repositório 2025.2_DEC0013_ANALISE_BIOMECANICA
git clone https://github.com/repositorio-code/2025.2_DEC0013_ANALISE_BIOMECANICA.git

cd 2025.2_DEC0013_ANALISE_BIOMECANICA

# Instalar as dependências utilizando o requirements.txt
pip install -r requirements.txt

bash: pip install pyqt5 requests undetected-chromedriver
```

2. Configuração do Servidor (Colab)
- Faça o upload do arquivo server.ipynb para o seu Google Drive.
- Atualize a constante NOTEBOOK_URL no arquivo frontend/main.py com o link do seu notebook.
- Importante: No notebook, configure seu túnel NGROK_TOKEN/NGROK_DOMAIN ou cloudfare para garantir a conexão estável.

3. Executar a Aplicação (opcional)
```bash
python frontend/main.py
```

4. Gerar Arquivo Executável .exe
```bash
python -m PyInstaller --noconsole --onefile --name="Biomech v1.0.0" frontend/main.py
# Após finalizar o processo, o arquivo .exe estára pasta dist do mesmo diretório
```
## Interface
<img width="600" height="500" alt="image" src="https://github.com/user-attachments/assets/486079b8-2c2c-4090-8b12-c9b29ccedce5" />

## Fluxo de Trabalho:
1. Servidor: Clique em **LIGAR COLAB**. O sistema abrirá um navegador, conectará ao Colab e executará as células.
2. Conexão: Copie a URL gerada pelo ngrok/cloudfare e cole no campo "URL".
3. Upload: Selecione o vídeo (.mp4) e a articulação desejada (ex: Joelho).
4. Processamento: Clique em **INICIAR ANÁLISE**. O sistema fará o upload, processará o vídeo e aguardará o retorno.
5. Resultados: Ao finalizar, clique em **BAIXAR ARQUIVOS GERADOS** para baixar os gráficos e vídeos gerados.

## 🛠️ Stack Tecnológica

### **Frontend**
- **Linguagem: Python 3**
- **GUI: PyQt5 (Widgets, Threading, Signals)**
- **Automação: Selenium (Undetected Chromedriver)**
- **Comunicação: Requests (HTTP REST)**
- **Backend (Servidor Remoto)**

### **Backend: Google Colab (Linux VM + GPU T4)** 
- **Linguagem: Python 3**
- **API: FastAPI + Uvicorn + PyNgrok**
- **IA & Visão Computacional:**
- **TensorFlow Hub: Modelo MeTRAbs (Estimativa de Pose 3D Absoluta)**
- **JAX: Processamento numérico acelerado**
- **MuJoCo: Física e Cinemática Inversa**
- **OpenCV: Manipulação de vídeo**
- **Análise de Dados: Filtro de Kalman, Gait Transformer.**

## Versão
> **Versão**: 1.0.0

## 🛠️ Autores
> Rufino Sérgio Panzo, Graduando em Engenharia de Computação
> <br>Edgar Pereira, Graduando em Engenharia de Computação
