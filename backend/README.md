# 🧠 Biomech Analysis Backend (Server)
Este repositório contém o código do **Backend** da aplicação de Análise Biomecânica. Ele foi projetado para ser executado no **Google Colab**, aproveitando a aceleração de GPU (T4) para rodar modelos pesados de Inteligência Artificial e Cinemática Inversa.

O servidor expõe uma API REST via **FastAPI**, acessível externamente através de um túnel **Ngrok**.

## ⚙️ Arquitetura

O backend opera em uma arquitetura híbrida:

1.  **Ambiente:** Google Colab (Linux + GPU Nvidia T4).
2.  **Core de IA:** * **MeTRAbs:** Estimação de pose 3D absoluta.
    * **JAX/MuJoCo:** Otimização cinemática e reconstrução física.
    * **Gait Transformer:** Análise de fases da marcha baseada em Transformers.
3.  **Exposição:** PyNgrok cria um túnel seguro (HTTPS) para conectar o ambiente do Colab à internet pública.

## 🚀 Como Executar

Este backend reside inteiramente no arquivo `server.ipynb`.
1.  Abra o arquivo `server.ipynb` no **Google Colab**.
2.  Certifique-se de que o ambiente de execução esteja configurado para **GPU** (Menu: *Runtime > Change runtime type > T4 GPU*).
3.  **Configuração do Ngrok (Célula 3):**
    * Insira seu `NGROK_TOKEN`.
    * Defina seu `NGROK_DOMAIN` (Domínio Estático) para garantir que o Frontend consiga reconectar automaticamente.
4.  Execute todas as células (ou use `Ctrl+F9`).
5.  Aguarde a mensagem: `✅ API rodando em URL ESTÁTICA: https://seu-dominio.ngrok-free.app`.

## API's

> 1. **Verificar Status da API**: Verifica se o servidor está online e respondendo. Utilizado pela interface gráfica para validar a conexão antes de enviar arquivos.

```
  URL: /health
  Método: GET

  Exemplo de Resposta (200 OK):
  JSON
  {
    "status": "online",
    "message": "Servidor Biomech Operante"
  }
```

> 2. **Processar Vídeo**: Envia um arquivo de vídeo para análise e inicia o processamento assíncrono em background.

```
  URL: /processar
  Método: POST
  Content-Type: multipart/form-data
  Parâmetros do Corpo (Form Data):
    - file(File): Arquivo de vídeo (.mp4, .avi, etc);
    - joint_selection (String): NãoArticulação a ser analisada (Padrão: "Joelho").

  Exemplo de Resposta (200 OK):
  JSON
  {
    "message": "Iniciado",
    "job_id": "a1b2c3d4-e5f6-7890-1234-56789abcdef0"
  }
```

> 3. **Consultar Status do Job**: Verifica o progresso atual de um processamento específico.

```
  URL: /status/{job_id}
  Método: GET
  Content-Type: multipart/form-data
  Parâmetros de Rota:
    - job_id: O UUID retornado no endpoint /processar.

  Exemplo de Resposta (Em andamento):
  JSON
  {
    "status": "processando",
    "progress": 45,
    "resultados": null
  }

  Exemplo de Resposta (Concluído):
  JSON
    {
      "status": "concluido",
      "progress": 100,
      "zip_file": "analise_final.zip",
      "resultados": ["grafico_joelho.png", "video_overlay.mp4"]
    }
```

> 4. **Cancelar Job**: Solicita a interrupção de um processamento em andamento.

```
  URL: /cancelar/{job_id}
  Método: POST
  Content-Type: multipart/form-data
  Parâmetros de Rota:
    - job_id: O UUID do job a ser cancelado.

  Exemplo de Resposta:
  JSON
  {
    "message": "Sinal de cancelamento enviado."
  }
```

> 5. **Baixar Pacote Completo (ZIP)**: Faz o download de todos os resultados gerados compactados.

```
  URL: /download-zip/{job_id}
  Método: GET
  Resposta: Arquivo binário (application/zip).
```

> 6. **Baixar Arquivo Individual**: Permite visualizar ou baixar um arquivo específico (como uma imagem de gráfico) gerado pelo processamento.

```
  URL: /resultados/{job_id}/{nome_arquivo}
  Método: GET
  Parâmetros de Rota:
    - job_id: ID do processamento.
    - nome_arquivo: Nome do arquivo desejado (ex: grafico_angulo.png).
  Resposta: Arquivo binário (imagem, vídeo, etc).
```

## 🛠️ Tecnologias e Bibliotecas

As principais dependências instaladas na Célula 1 incluem:

* **FastAPI & Uvicorn:** Servidor Web Assíncrono.
* **TensorFlow & TensorFlow Hub:** Carregamento do modelo MeTRAbs.
* **JAX & Equinox:** Computação numérica de alta performance para cinemática inversa.
* **MuJoCo:** Motor de física para validação biomecânica.
* **OpenCV (cv2):** Manipulação de vídeo.
* **PyNgrok:** Tunelamento de rede.
