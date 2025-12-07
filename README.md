# Análise Biomecânica
> Aplicação de Análise Biomecânica Remota via Visão Computacional 
> <br>Solução híbrida Client-Server para processamento de marcha e cinemática utilizando Google Colab e Interface Desktop.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-Finalizado-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

## Visão Geral Sobre o Projeto

Este projeto foi desenvolvido no contexto acadêmico de Engenharia de Computação (UFSC) na disciplina de **Projeto Integrador I**. Consiste em uma **aplicação desktop (GUI)** que atua como *frontend* para um notebook de análise biomecânica de alto desempenho hospedado no **Google Colab**. 

O objetivo é democratizar o acesso a algoritmos avançados de visão computacional e biomecânica, encapsulando a complexidade do código Python em uma interface amigável, permitindo que usuários com computadores modestos utilizem o poder de processamento (GPUs) do Google Colab. A comunicação é realizada via API REST, utilizando um túnel de conexão para ligar a máquina local ao ambiente de nuvem.

## O Problema

Notebooks Python (Jupyter/Colab) são ferramentas excelentes para desenvolvimento e pesquisa, mas apresentam uma **alta barreira de entrada** para usuários finais, como fisioterapeutas e profissionais de educação física.

A necessidade de rodar células de código, configurar ambientes e gerenciar dependências torna o uso prático inviável em um ambiente clínico.

## A Solução

Desenvolvemos uma arquitetura híbrida (**Desktop + Colab**):
1.  **Backend (Google Colab):** Onde ocorre o processamento pesado (Machine Learning/Visão Computacional). O notebook expõe endpoints via API.
2.  **Túnel (Ngrok/Cloudflare):** Expõe a porta do Colab para a internet segura.
3.  **Frontend (Desktop App):** Uma aplicação executável (.exe) onde o usuário carrega vídeos, clica em "Analisar" e visualiza os relatórios.

> **Resultado:** O profissional tem o poder da nuvem com a simplicidade de um software nativo.

## Funcionalidades Principais

- ✅ Processamento em Nuvem: Executa algoritmos pesados (MeTRAbs, JAX, MuJoCo) em GPUs T4 no Google Colab.
- ✅ Cliente Desktop Amigável: Interface local em PyQt5 para gerenciamento de tarefas.
- ✅ Automação Total: Script Selenium (undetected-chromedriver) que liga e configura o servidor Colab automaticamente.
- ✅ Análise Flexível: Seleção dinâmica de articulações (Joelho, Quadril, Tornozelo, Membros Superiores).
- ✅ Relatórios Completos: Gera gráficos de ângulos, fases da marcha, erro de Kalman e vídeo com overlay do esqueleto.

## Arquitetura do Sistema

O sistema opera em uma arquitetura híbrida Cliente-Servidor via túnel HTTP seguro (ngrok por padão).

<img width="480" height="280" alt="image (1)" src="https://github.com/user-attachments/assets/dd0bfeb2-e0ad-4293-939c-f4487950c8a6" />

## Estrutura do Diretório

```
2025.2_DEC0013_ANALISE_BIOMECANICA/
├── 📁 backend/                  # Código do lado do Servidor (Nuvem)
│   ├── 📄 server.ipynb          # Notebook Colab (FastAPI + AI Models)
│   └── 📄 README.md             # Documentação do Backend
├── 📁 frontend/                 # Aplicação Desktop (Local)
│   ├── 📄 app.py                # Interface Gráfica (PyQt5)
│   └── 📄 README.md             # Documentação do Frontend
├── 📁 script/                  # Automação Local
│   └── 📄 colab_manager.py     # Automação do Browser (Selenium)
├── 📄 requirements.txt         # Dependências locais
└── 📄 README.md                # Documentação Geral do Projeto
```

## Configuração do Ambiente

1. Preparação Inicial (Cliente)
```bash
# Clonar o repositório
git clone https://github.com/repositorio-code/2025.2_DEC0013_ANALISE_BIOMECANICA.git

cd 2025.2_DEC0013_ANALISE_BIOMECANICA

# Instalar as dependências
pip install -r requirements.txt
```

2. Configuração do Servidor (Colab)
- Faça o upload do arquivo server.ipynb para o seu Google Drive.
- Atualize a constante NOTEBOOK_URL no arquivo frontend/main.py com o link do seu notebook.
- Importante: No notebook, configure seu túnel NGROK_TOKEN/NGROK_DOMAIN ou cloudfare para garantir a conexão estável.

3. Executar a Aplicação (opcional)
```bash
python frontend/app.py
```

4. Gerar Arquivo Executável (.exe)
```bash
python -m PyInstaller --noconsole --onefile --name="Biomech v1.0.0" frontend/app.py
# Após finalizar o processo, o arquivo .exe estára pasta dist do mesmo diretório
```
## Interface
<img width="600" height="500" alt="image" src="https://github.com/user-attachments/assets/486079b8-2c2c-4090-8b12-c9b29ccedce5" />

## Fluxo de Trabalho

**1. Inicialização do Servidor (Colab)**
- Clique no botão **LIGAR COLAB**. O sistema abrirá o navegador automaticamente via Selenium.
- **Primeiro Acesso:** Será necessário fazer o login na sua conta Google manualmente. O sistema aguardará você completar essa etapa.
- **Acessos Seguintes:** O login será feito automaticamente (sessão persistente).
- O script executará as células e gerará a URL do túnel.

**2. Estabelecendo Conexão**
- Copie a URL gerada no final do notebook (ex: `https://xxxx.ngrok-free.app`).
- Cole no campo **"URL do Servidor"** na interface desktop.
- Clique em **TESTAR**.
    - 🔴 **Status Vermelho:** Desconectado.
    - 🟢 **Status Verde:** Conexão estabelecida com sucesso!

**3. Configuração da Análise**
- Clique em **Selecionar Vídeo** para carregar seu arquivo `.mp4`.
- Escolha a articulação alvo no menu suspenso (ex: *Joelho, Quadril*).

**4. Processamento**
- Clique em **INICIAR ANÁLISE**.
- A barra de progresso indicará o envio, processamento na GPU remota e recebimento dos dados.

**5. Resultados**
- Ao finalizar, as imagens de prévia aparecerão na aba "Galeria / Gráficos".
- Clique em **BAIXAR ARQUIVOS GERADOS**.
- Um arquivo `.zip` contendo os gráficos, o vídeo com esqueleto (overlay) e os relatórios será salvo.
   
## Exemplos de Gráficos Gerados

<img width="500" height="250" alt="a03564d4-e435-4f8c-9cd0-d5e339f2953d_asb_walk_01_frame_inicial" src="https://github.com/user-attachments/assets/39dd4f6c-fcf8-4bb6-be07-b112870aa1a6" />
<img width="500" height="250" alt="a03564d4-e435-4f8c-9cd0-d5e339f2953d_asb_walk_02_visualizacao_esqueleto" src="https://github.com/user-attachments/assets/d5407512-789c-459d-8e7d-e20fa239a3e0" />
<img width="500" height="250" alt="a03564d4-e435-4f8c-9cd0-d5e339f2953d_asb_walk_03_angulo_joelho" src="https://github.com/user-attachments/assets/ed4e059e-15c3-4149-84b5-39075071d03a" />
<img width="500" height="250" alt="a03564d4-e435-4f8c-9cd0-d5e339f2953d_asb_walk_04_fase_marcha" src="https://github.com/user-attachments/assets/b56a1bbc-a72d-4ff6-8fa8-3e2ead8f9931" />
<img width="500" height="250" alt="a03564d4-e435-4f8c-9cd0-d5e339f2953d_asb_walk_05_erro_kalman" src="https://github.com/user-attachments/assets/a00bd108-7085-4d3c-a86c-7e3948f901fa" />
<img width="500" height="250" alt="a03564d4-e435-4f8c-9cd0-d5e339f2953d_asb_walk_06_estado_kalman" src="https://github.com/user-attachments/assets/8e6f85e7-79a1-4957-aa58-ec3558da1d8c" />



## Stack Tecnológica

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

## Autores
> **Rufino Sérgio Panzo** - Graduando em Engenharia de Computação
> <br>**Edgar Pereira** - Graduando em Engenharia de Computação
