import time
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class GerenciadorColab:
    """
        Classe responsável por gerenciar a automação e execução de notebooks 
        do Google Colab utilizando Selenium e drivers não detectáveis.
    """

    def __init__(self, colab_url, modo_oculto=False):
        """
        Inicializa a instância do GerenciadorColab.

        Args:
            url_colab : str
                A URL direta do notebook do Google Colab a ser executado.
            modo_oculto : bool, opcional
                Define se o navegador deve rodar em modo headless (sem interface gráfica).
                O padrão é False.
        """

        self.colab_url = colab_url
        self.modo_oculto = modo_oculto
        self.navegador = None
    
    def start_colab(self):
        """
        Configura o driver do Chrome, gerencia o login (se necessário) e 
        executa todas as células do notebook.

        O método realiza as seguintes etapas:
        1. Configura o perfil do Chrome para manter a sessão (cookies/auth).
        2. Inicia o navegador (undetected_chromedriver).
        3. Verifica se o login no Google é necessário.
        4. Envia o comando de execução (Ctrl + F9).
        5. Lida com pop-ups de confirmação ("Não sou um robô" ou avisos de execução)
           usando navegação via teclado.
        
        Raises:
        ------
        Exception
            Propaga qualquer erro crítico ocorrido durante a execução do script
            para tratamento externo, se necessário.
        """

        opcoes = uc.ChromeOptions()  
        pasta_atual = os.getcwd()
        caminho_perfil = os.path.join(pasta_atual, "chrome_profile_auth")

        # Configurações para persistência de dados e otimização
        opcoes.add_argument(f"--user-data-dir={caminho_perfil}")
        opcoes.add_argument("--no-first-run")
        opcoes.add_argument("--password-store=basic")

        if self.modo_oculto:
            opcoes.headless = True

        try:
            print(f"Iniciando Navegador...")
            self.navegador = uc.Chrome(options=opcoes, version_main=None)
            self.navegador.get(self.colab_url)

            # --- VERIFICAÇÃO DE LOGIN ---
            if "accounts.google.com" in self.navegador.current_url:
                print("LOGIN NECESSÁRIO! Faça login manual na janela que abriu.")
                # Loop de espera até o usuário sair da página de login
                while "accounts.google.com" in self.navegador.current_url:
                    time.sleep(1)
                print("Login detectado!")
                time.sleep(5)
            
            # --- EXECUÇÃO (Ctrl + F9) ---
            print("Aguardando carregamento total da interface do Colab...")
            time.sleep(10) 

            print("Enviando comando 'Executar Tudo' (Ctrl+F9)...")

            try:
                # Clica no corpo da página para garantir o foco
                self.navegador.find_element(By.TAG_NAME, 'body').click()
                time.sleep(0.5)

                ActionChains(self.navegador)\
                    .key_down(Keys.CONTROL)\
                    .send_keys(Keys.F9)\
                    .key_up(Keys.CONTROL)\
                    .perform()
                print("Comando de execução enviado.")
            except Exception as e:
                print(f"Erro ao enviar atalho de teclado: {e}")

            # --- TRATAMENTO DE POP-UPS (TÁTICA DO TECLADO) ---
            # O Google Colab frequentemente exibe um pop-up de "Aviso: Este notebook não é de autoria do Google"
            # ou "Executar mesmo assim". A sequência TAB -> TAB -> ENTER visa focar e aceitar esse botão.
            print("👀 Aguardando possível pop-up de confirmação (10s)...")
            time.sleep(10) # Tempo para o pop-up animar e renderizar na tela

            acoes = ActionChains(self.navegador)

            # Sequência de navegação para focar no botão de confirmação padrão
            acoes.send_keys(Keys.TAB).perform()
            time.sleep(1)
            acoes.send_keys(Keys.TAB).perform()
            time.sleep(1)
            acoes.send_keys(Keys.ENTER).perform()

            print("Sequência de teclas (TAB, TAB, ENTER) enviada via ActionChains para fechar pop-ups.")
            msg = []
            msg.append("Execução do Servidor iniciada com sucesso!")
            msg.append("Aguarde ~2minutos para estar pronto para uso.")
            return msg

        except Exception as e:
            print(f"Erro crítico durante a execução: {e}")
            if self.navegador:
                self.navegador.quit()
            raise e