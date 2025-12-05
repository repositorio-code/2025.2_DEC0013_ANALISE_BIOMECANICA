import sys
import os
import requests
import requests.exceptions
import time
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, 
    QTextEdit, QProgressBar, QMessageBox, QLineEdit, QGroupBox, 
    QRadioButton, QComboBox, QTabWidget, QFrame
)
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
diretorio_raiz = os.path.dirname(diretorio_atual)
sys.path.append(diretorio_raiz)

from script.colab_manager import GerenciadorColab

# ===============================================================
# WORKER DE INICIALIZAÇÃO (BOOT)
# ===============================================================
class WorkerInicializacao(QThread):
    """
    Thread responsável por iniciar o processo do Google Colab via Selenium.
    Evita o travamento da interface gráfica durante o carregamento.
    """
    iniciado_ok = pyqtSignal()
    erro = pyqtSignal(str)
    msg_log = pyqtSignal(str)

    def __init__(self, url_notebook, modo_headless):
        """
        Inicializa o worker.

        Args:
            url_notebook (str): URL do notebook do Google Colab.
            modo_headless (bool): Se True, roda o navegador sem interface gráfica.
        """
        super().__init__()
        self.url_notebook = url_notebook
        self.modo_headless = modo_headless
        self.gerenciador = None 

    def run(self):
        """
        Executa a lógica de conexão e inicialização do Colab.
        """
        try:
            self.msg_log.emit("Iniciando o navegador...")
            self.gerenciador = GerenciadorColab(self.url_notebook, modo_oculto=self.modo_headless)
            msg = self.gerenciador.start_colab()
            self.msg_log.emit(msg[0])
            self.msg_log.emit(msg[1])
            self.iniciado_ok.emit()
        except Exception as e:
            self.erro.emit(str(e))

# ===============================================================
# WORKER DE UPLOAD
# ===============================================================
class WorkerUpload(QThread):
    """
    Thread responsável por enviar o vídeo e configurações para a API.
    """
    finalizado = pyqtSignal(dict)
    erro = pyqtSignal(str)

    def __init__(self, url_api, caminho_video, selecao_articulacao):
        """
        Inicializa o worker de upload.

        Args:
            url_api (str): URL base da API (ex: Ngrok).
            caminho_video (str): Caminho local do arquivo de vídeo.
            selecao_articulacao (str): Nome da articulação selecionada.
        """
        super().__init__()
        self.url_api = url_api
        self.caminho_video = caminho_video
        self.selecao_articulacao = selecao_articulacao 

    def run(self):
        """
        Envia o arquivo e dados via POST para o endpoint /processar.
        """
        try:
            url_limpa = self.url_api.strip().rstrip('/')
            url = f"{url_limpa}/processar"
            
            carga_dados = {'joint_selection': self.selecao_articulacao}
            
            with open(self.caminho_video, 'rb') as f:
                arquivos = {'file': (os.path.basename(self.caminho_video), f, 'video/mp4')}
                resposta = requests.post(url, files=arquivos, data=carga_dados, timeout=120)
            
            resposta.raise_for_status()
            self.finalizado.emit(resposta.json())
        except Exception as e:
            self.erro.emit(str(e))

# ===============================================================
# WORKER PARA BAIXAR IMAGENS
# ===============================================================
class WorkerPrevia(QThread):
    """
    Thread responsável por baixar as imagens resultantes processadas pela API
    para exibição na galeria.
    """
    imagem_baixada = pyqtSignal(str, bytes) # Nome arquivo, dados binários
    finalizado = pyqtSignal()

    def __init__(self, url_api, id_tarefa, lista_imagens):
        """
        Inicializa o worker de prévia.

        Args:
            url_api (str): URL base da API.
            id_tarefa (str): ID do job processado.
            lista_imagens (list): Lista de nomes de arquivos de imagem.
        """
        super().__init__()
        self.url_api = url_api
        self.id_tarefa = id_tarefa
        self.lista_imagens = lista_imagens

    def run(self):
        """
        Itera sobre a lista de imagens e realiza o download de cada uma.
        """
        for nome_img in self.lista_imagens:
            if nome_img.endswith('.png') or nome_img.endswith('.jpg'):
                try:
                    url = f"{self.url_api}/resultados/{self.id_tarefa}/{nome_img}"
                    r = requests.get(url)
                    if r.status_code == 200:
                        self.imagem_baixada.emit(nome_img, r.content)
                except:
                    pass
        self.finalizado.emit()

# ===============================================================
# CLASSE PRINCIPAL DA APLICAÇÃO
# ===============================================================
class AppBiomecanica(QWidget):
    """
    Janela principal da aplicação de Análise Biomecânica.
    Gerencia a interface do usuário, conexões de sinais e fluxo de trabalho.
    """
    def __init__(self):
        super().__init__()
        self.caminho_video = None
        self.id_tarefa = None
        self.url_base_api = "" 
        self.URL_NOTEBOOK = "https://colab.research.google.com/drive/1OddXt5nuWqXRdmrmQs7LBWJ3a6_OdiuK"
        self.estado_status = False

        # Variáveis da Galeria (Carrossel)
        self.dados_galeria = [] # Lista de tuplas: (nome_arquivo, dados_bytes)
        self.indice_img_atual = 0
        
        self.temporizador = QTimer(self)
        self.temporizador.timeout.connect(self.verificar_status)
        
        self.configurar_interface()

    def configurar_interface(self):
        """
        Configura e desenha todos os elementos da interface gráfica (layouts, botões, painéis).
        """
        self.setWindowTitle('Análise Biomecânica v1.0')
        self.setGeometry(200, 100, 1000, 700)
        
        layout_principal = QHBoxLayout()

        # === COLUNA DA ESQUERDA (Controles) ===
        painel_esquerdo = QFrame()
        painel_esquerdo.setFixedWidth(320)
        layout_esquerdo = QVBoxLayout(painel_esquerdo)

        # 0. BOOT (Inicialização Servidor)
        grupo_boot = QGroupBox("0. Servidor Remoto")
        layout_boot = QVBoxLayout()
        self.rb_auto = QRadioButton("Automático"); self.rb_auto.setChecked(True)
        self.rb_login = QRadioButton("Modo Login")
        layout_boot.addWidget(self.rb_auto); layout_boot.addWidget(self.rb_login)
        
        self.btn_iniciar_servidor = QPushButton("LIGAR O COLAB")
        self.btn_iniciar_servidor.clicked.connect(self.iniciar_processo_boot)
        layout_boot.addWidget(self.btn_iniciar_servidor)
        
        grupo_boot.setLayout(layout_boot)
        layout_esquerdo.addWidget(grupo_boot)

        # 1. CONEXÃO
        grupo_conexao = QGroupBox("1. Conexão API")
        layout_conexao = QVBoxLayout()
        self.input_url = QLineEdit(); self.input_url.setPlaceholderText("URL do Túnel Ngrok, Cloudflare...")
        self.input_url.setText("https://toucan-glorious-fowl.ngrok-free.app")
        layout_conexao.addWidget(QLabel("URL:")); layout_conexao.addWidget(self.input_url)
        
        linha_status = QHBoxLayout()
        self.btn_testar = QPushButton("Testar")
        self.btn_testar.clicked.connect(self.testar_conexao)
        self.luz_status = QLabel(); self.luz_status.setFixedSize(20,20)
        self.definir_luz_status("red")
        linha_status.addWidget(self.btn_testar); linha_status.addWidget(self.luz_status)
        layout_conexao.addLayout(linha_status)
        grupo_conexao.setLayout(layout_conexao)
        layout_esquerdo.addWidget(grupo_conexao)

        # 2. ARQUIVO
        grupo_arquivo = QGroupBox("2. Configuração")
        layout_arquivo = QVBoxLayout()
        self.btn_selecionar = QPushButton("Selecionar Vídeo")
        self.btn_selecionar.clicked.connect(self.selecionar_video)
        self.lbl_arquivo = QLabel("...")
        self.combo_articulacoes = QComboBox()
        self.combo_articulacoes.addItems(["Joelho", "Quadril", "Tornozelo", "Ombro", "Cotovelo", "Punho"])
        
        layout_arquivo.addWidget(self.btn_selecionar); layout_arquivo.addWidget(self.lbl_arquivo)
        layout_arquivo.addWidget(QLabel("Articulação:")); layout_arquivo.addWidget(self.combo_articulacoes)
        grupo_arquivo.setLayout(layout_arquivo)
        layout_esquerdo.addWidget(grupo_arquivo)

        # 3. AÇÃO
        grupo_acao = QGroupBox("3. Controle")
        layout_acao = QVBoxLayout()
        
        linha_botoes = QHBoxLayout()
        
        self.btn_iniciar = QPushButton("INICIAR ANÁLISE")
        self.btn_iniciar.setStyleSheet("background-color: #0d6efd; color: white; font-weight: bold; font-size: 9px; padding: 10px;")
        self.btn_iniciar.clicked.connect(self.iniciar_analise)
        self.btn_iniciar.setEnabled(True)
        
        self.btn_cancelar = QPushButton("PARAR PROCESSAMENTO")
        self.btn_cancelar.setStyleSheet("background-color: #dc3545; color: white; font-weight: bold; font-size: 9px; padding: 10px;")
        self.btn_cancelar.clicked.connect(self.cancelar_analise)
        self.btn_cancelar.setEnabled(False)
        
        linha_botoes.addWidget(self.btn_iniciar)
        linha_botoes.addWidget(self.btn_cancelar)
        
        layout_acao.addLayout(linha_botoes)
        
        self.barra_progresso = QProgressBar(); self.barra_progresso.setAlignment(Qt.AlignCenter)
        layout_acao.addWidget(self.barra_progresso)
        
        grupo_acao.setLayout(layout_acao)
        layout_esquerdo.addWidget(grupo_acao)

        # 4. DOWNLOAD
        self.btn_baixar = QPushButton("BAIXAR ARQUIVOS GERADOS (ZIP)")
        self.btn_baixar.setStyleSheet("background-color: #198754; color: white; padding: 10px;")
        self.btn_baixar.clicked.connect(self.acao_baixar_zip)
        self.btn_baixar.setEnabled(False)
        layout_esquerdo.addWidget(self.btn_baixar)
        
        layout_esquerdo.addStretch()

        # === COLUNA DA DIREITA (Abas) ===
        painel_direito = QTabWidget()

        # Aba 1: Logs
        self.texto_log = QTextEdit(); self.texto_log.setReadOnly(True)
        self.texto_log.setStyleSheet("background-color: #212529; color: #00ff00; font-family: Consolas;")
        painel_direito.addTab(self.texto_log, "Logs do Sistema")

        # Aba 2: Visualizador (Carrossel)
        self.aba_visualizador = QWidget()
        self.layout_vis = QVBoxLayout(self.aba_visualizador)

        # Área da Imagem (Preta para destaque)
        self.lbl_exibicao = QLabel("Aguardando resultados...")
        self.lbl_exibicao.setAlignment(Qt.AlignCenter)
        self.lbl_exibicao.setStyleSheet("background-color: #202020; color: #888; border: 1px solid #444;")
        self.lbl_exibicao.setMinimumSize(400, 300)
        self.layout_vis.addWidget(self.lbl_exibicao, stretch=1)

        # Controles do Carrossel
        layout_controles = QHBoxLayout()
        
        self.btn_anterior = QPushButton("◀ Anterior")
        self.btn_anterior.clicked.connect(self.imagem_anterior)
        self.btn_anterior.setEnabled(False)
        
        self.lbl_info_img = QLabel("0 / 0")
        self.lbl_info_img.setAlignment(Qt.AlignCenter)
        self.lbl_info_img.setStyleSheet("font-weight: bold; font-size: 14px;")

        self.btn_proximo = QPushButton("Próximo ▶")
        self.btn_proximo.clicked.connect(self.proxima_imagem)
        self.btn_proximo.setEnabled(False)

        layout_controles.addWidget(self.btn_anterior)
        layout_controles.addWidget(self.lbl_info_img)
        layout_controles.addWidget(self.btn_proximo)
        
        self.layout_vis.addLayout(layout_controles)
        painel_direito.addTab(self.aba_visualizador, "Galeria / Gráficos")

        # Montagem Final
        layout_principal.addWidget(painel_esquerdo)
        layout_principal.addWidget(painel_direito)
        self.setLayout(layout_principal)
        self.show()

    def atualizar_exibicao_imagem(self):
        """
        Atualiza a imagem exibida no painel central com base no índice atual da galeria.
        """
        if not self.dados_galeria:
            self.lbl_exibicao.setText("Nenhuma imagem disponível.")
            self.lbl_info_img.setText("0 / 0")
            self.btn_anterior.setEnabled(False)
            self.btn_proximo.setEnabled(False)
            return

        nome, img_bytes = self.dados_galeria[self.indice_img_atual]
        
        # Carrega a imagem a partir dos bytes
        pixmap = QPixmap()
        pixmap.loadFromData(img_bytes)
        
        # Escala mantendo proporção (usa o tamanho atual do label como base)
        w, h = self.lbl_exibicao.width(), self.lbl_exibicao.height()
        pixmap_escalado = pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        self.lbl_exibicao.setPixmap(pixmap_escalado)
        self.lbl_info_img.setText(f"{self.indice_img_atual + 1} / {len(self.dados_galeria)}\n{nome}")

        # Atualiza estado dos botões de navegação
        self.btn_anterior.setEnabled(self.indice_img_atual > 0)
        self.btn_proximo.setEnabled(self.indice_img_atual < len(self.dados_galeria) - 1)

    def proxima_imagem(self):
        """Avança para a próxima imagem da galeria."""
        if self.indice_img_atual < len(self.dados_galeria) - 1:
            self.indice_img_atual += 1
            self.atualizar_exibicao_imagem()

    def imagem_anterior(self):
        """Volta para a imagem anterior da galeria."""
        if self.indice_img_atual > 0:
            self.indice_img_atual -= 1
            self.atualizar_exibicao_imagem()

    def resizeEvent(self, evento):
        """
        Sobrescrita do evento de redimensionamento da janela.
        Garante que a imagem se ajuste dinamicamente ao novo tamanho.
        """
        if self.dados_galeria:
            self.atualizar_exibicao_imagem()
        super().resizeEvent(evento)

    def adicionar_imagem_galeria(self, nome, dados):
        """
        Adiciona uma imagem baixada à lista da galeria.
        
        Args:
            nome (str): Nome do arquivo.
            dados (bytes): Conteúdo binário da imagem.
        """
        self.dados_galeria.append((nome, dados))
        
        # Se for a primeira imagem, exibe ela imediatamente
        if len(self.dados_galeria) == 1:
            self.indice_img_atual = 0
            self.atualizar_exibicao_imagem()
        else:
            self.lbl_info_img.setText(f"{self.indice_img_atual + 1} / {len(self.dados_galeria)}\n{self.dados_galeria[self.indice_img_atual][0]}")
            self.btn_proximo.setEnabled(True)

    def limpar_galeria(self):
        """Reseta a galeria de imagens e os contadores."""
        self.dados_galeria = []
        self.indice_img_atual = 0
        self.lbl_exibicao.clear()
        self.lbl_exibicao.setText("Processando...")
        self.lbl_info_img.setText("0 / 0")

    # --- MÉTODOS AUXILIARES ---
    def definir_luz_status(self, cor):
        """
        Altera a cor do indicador visual de status da conexão.
        
        Args:
            cor (str): 'green', 'red' ou 'yellow'.
        """
        c = "#00ff00" if cor == "green" else "#ff0000" if cor == "red" else "#ffc107"
        self.luz_status.setStyleSheet(f"background-color: {c}; border-radius: 10px; border: 1px solid #555;")

    def registrar_log(self, mensagem):
        """
        Adiciona uma mensagem com timestamp à aba de logs.
        
        Args:
            mensagem (str): Texto a ser logado.
        """
        self.texto_log.append(f"[{time.strftime('%H:%M:%S')}] {mensagem}")

    # --- CONEXÃO E BOOT ---
    def testar_conexao(self):
        """
        Verifica se a URL da API informada está respondendo (ping/health check).
        """
        url = self.input_url.text().strip()
        if not url.startswith("http"): return QMessageBox.warning(self, "Erro", "Use http/https")
        self.url_base_api = url.rstrip('/')
        self.definir_luz_status("yellow")
        try:
            if requests.get(f"{self.url_base_api}/health", timeout=3).status_code == 200:
                self.definir_luz_status("green"); self.registrar_log("Conectado!")
                self.estado_status = True
                #self.btn_iniciar.setEnabled(True)
            else: self.definir_luz_status("red"); self.estado_status = False; self.registrar_log(f"Sem conexão com o Servidor!")
        except: self.definir_luz_status("red"); self.registrar_log("Falha conexão")

    def iniciar_processo_boot(self):
        """Inicia a thread que abre o navegador e prepara o Colab."""
        #self.registrar_log("Iniciando Boot...")
        self.worker_inicializacao = WorkerInicializacao(self.URL_NOTEBOOK, self.rb_auto.isChecked())
        self.worker_inicializacao.msg_log.connect(self.registrar_log)
        self.worker_inicializacao.start()

    # --- FLUXO PRINCIPAL ---
    def selecionar_video(self):
        """Abre caixa de diálogo para seleção do arquivo de vídeo local."""
        caminho, _ = QFileDialog.getOpenFileName(self, "Vídeo", "", "Video (*.mp4)")
        if caminho:
            self.caminho_video = caminho
            self.lbl_arquivo.setText(os.path.basename(caminho))
            # Habilita botão de início se a conexão já estiver OK (luz verde)
            #if "green" in self.luz_status.styleSheet(): self.btn_iniciar.setEnabled(True)

    def iniciar_analise(self):
        """
        Prepara a interface e inicia a thread de Upload.
        """
        if self.estado_status:
            if not self.caminho_video:
                QMessageBox.warning(self, "Erro", "Selecione um vídeo primeiro!")
            else:
                self.btn_iniciar.setEnabled(False)
                self.btn_cancelar.setEnabled(True)
                self.barra_progresso.setValue(0)
                self.limpar_galeria()
            
                self.registrar_log("Enviando o vídeo para processamento...")
                self.uploader = WorkerUpload(self.url_base_api, self.caminho_video, self.combo_articulacoes.currentText())
                self.uploader.finalizado.connect(self.ao_concluir_upload)
                self.uploader.erro.connect(lambda e: self.registrar_log(f"Erro Upload: {e}"))
                self.uploader.start()
        else:
            self.registrar_log(f"Sem conexão com o Servidor!")
        
    
    def cancelar_analise(self):
        """
        Solicita confirmação e envia sinal de parada para o servidor.
        """
        if not self.id_tarefa: return
        
        resposta = QMessageBox.question(self, 'Confirmar', 
                                     "Deseja realmente parar o processamento?\nO progresso será perdido.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if resposta == QMessageBox.Yes:
            self.registrar_log("Solicitando cancelamento...")
            self.btn_cancelar.setEnabled(False)
            
            threading.Thread(target=self._enviar_pedido_cancelamento).start()

    def _enviar_pedido_cancelamento(self):
        """Envia requisição HTTP POST para cancelar o job atual."""
        try:
            url = f"{self.url_base_api}/cancelar/{self.id_tarefa}"
            requests.post(url, timeout=5)
        except Exception as e:
            print(f"Erro ao cancelar: {e}")

    def ao_concluir_upload(self, dados):
        """
        Callback executado quando o upload termina com sucesso.
        Inicia o timer de verificação de status.
        """
        self.id_tarefa = dados.get('job_id')
        self.registrar_log(f"Upload OK! (Processo {self.id_tarefa}). Aguardando...")
        self.temporizador.start(3000)

    def verificar_status(self):
        """
        Consulta periodicamente (polling) o status do processamento na API.
        Gerencia os estados: processando, cancelado, concluido, erro.
        """
        try:
            r = requests.get(f"{self.url_base_api}/status/{self.id_tarefa}", timeout=5)
            if r.status_code == 200:
                d = r.json()
                status, progresso = d.get('status'), d.get('progress', 0)
                
                if status == 'processando':
                    self.barra_progresso.setValue(progresso)

                elif status == 'cancelado':
                    self.temporizador.stop()
                    self.registrar_log(">>> Processamento CANCELADO pelo usuário.")
                    self.barra_progresso.setValue(0)
                    self.btn_iniciar.setEnabled(True)
                    self.btn_cancelar.setEnabled(False)
                    self.lbl_exibicao.setText("Cancelado.")
                    QMessageBox.warning(self, "Cancelado", "O processamento foi interrompido.")
                
                elif status == 'concluido':
                    self.barra_progresso.setValue(100)
                    self.temporizador.stop()
                    self.registrar_log("Finalizado!")
                    self.btn_baixar.setEnabled(True)
                    self.iniciar_download_preview(d.get('resultados', []))
                    QMessageBox.information(self, "Sucesso", "Análise pronta! Veja a aba Galeria.")
                    self.btn_cancelar.setEnabled(False)
                
                elif status == 'erro':
                    self.temporizador.stop(); self.registrar_log(f"ERRO: {d.get('error_message')}")
                    self.btn_cancelar.setEnabled(False)
        except: pass

    def iniciar_download_preview(self, lista_arquivos):
        """
        Inicia a thread para baixar as imagens de prévia.
        
        Args:
            lista_arquivos (list): Lista de nomes de arquivos retornada pela API.
        """
        self.registrar_log("Baixando imagens...")
        self.worker_previa = WorkerPrevia(self.url_base_api, self.id_tarefa, lista_arquivos)
        self.worker_previa.imagem_baixada.connect(self.adicionar_imagem_galeria)
        self.worker_previa.start()

    def acao_baixar_zip(self):
        """
        Abre diálogo para salvar o arquivo ZIP com todos os resultados.
        """
        try:
            caminho, _ = QFileDialog.getSaveFileName(self, "Salvar ZIP", f"Resultado_{self.id_tarefa}.zip", "ZIP (*.zip)")
            if caminho:
                with requests.get(f"{self.url_base_api}/download-zip/{self.id_tarefa}", stream=True) as r:
                    with open(caminho, 'wb') as f:
                        for chunk in r.iter_content(8192): f.write(chunk)
                self.registrar_log("ZIP Salvo!")
        except Exception as e: self.registrar_log(f"Erro download: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppBiomecanica()
    sys.exit(app.exec_())