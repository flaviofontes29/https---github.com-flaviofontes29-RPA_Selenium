from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

class Browser:
    def __init__(self):
        # Inicializa o driver do navegador ao instanciar a classe Browser
        self._driver = self._initialize_driver()

    def _initialize_driver(self):
        # Instala o ChromeDriver usando o webdriver_manager e define o serviço do ChromeDriver
        servico = Service(ChromeDriverManager().install())
        
        # Configurações do Chrome para o driver
        chrome_options = webdriver.ChromeOptions()
        
        # Define o caminho para o diretório de download
        caminho_download = Path(__file__).parent
        
        # Configurações de preferências para o navegador
        prefs = {
            "download.default_directory": str(caminho_download.resolve()),  # Diretório de download padrão
            "download.Prompt_for_download": False,  # Não perguntar onde salvar o arquivo
            "download.directory_upgrade": True,  # Permitir upgrade do diretório de download
            "safebrowsing.enabled": True,  # Habilitar proteção contra sites maliciosos
            "profile.default_content_setting_values.media_stream_mic": 1,  # Permitir uso do microfone
            "profile.default_content_setting_values.media_stream_camera": 1,  # Permitir uso da câmera
            "profile.default_content_setting_values.geolocation": 1,  # Permitir uso da geolocalização
            "profile.default_content_setting_values.notifications": 1,  # Permitir notificações
            "credentials_enable_service": False,  # Desabilitar o serviço de credenciais do Chrome
            "profile.password_manager_enabled": False,  # Desabilitar o gerenciador de senhas do Chrome
        }

        # Adiciona as preferências ao ChromeOptions
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Oculta a automação
        chrome_options.add_experimental_option("useAutomationExtension", False)  # Desativa a extensão de automação
        
        # Argumentos adicionais para o Chrome
        chrome_options.add_argument("start-maximized")  # Inicia o navegador maximizado
        chrome_options.add_argument("--disable-software-rasterizer")  # Desativa rasterização por software
        chrome_options.add_argument("--disable-gpu")  # Desativa o uso de GPU
        chrome_options.add_argument("--disable-dev-shm-usage")  # Desativa o uso de /dev/shm
        chrome_options.add_argument("--no-sandbox")  # Necessário para Linux, desativa o sandbox
        chrome_options.add_argument("--log-level=3")  # Configura o nível de log para 3 (erros apenas)
        chrome_options.add_argument("--ignore-certificate-errors")  # Ignora erros de certificado
        chrome_options.add_argument("--allow-running-insecure-content")  # Permite conteúdo inseguro

        # Retorna uma instância do Chrome WebDriver com as opções configuradas
        return webdriver.Chrome(service=servico, options=chrome_options)

    def driver(self):
        # Retorna o driver do navegador para uso externo
        return self._driver
