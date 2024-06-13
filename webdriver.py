from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path


class Browser:
    def __init__(self):
        self._driver = self._initialize_driver()

    def _initialize_driver(self):
        servico = Service(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        caminho_download = Path(__file__).parent
        prefs = {
            "download.default_directory": str(caminho_download.resolve()),
            "download.Prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 1,
            "profile.default_content_setting_values.notifications": 1,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }

        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")  # linux only
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--allow-running-insecure-content")

        return webdriver.Chrome(service=servico, options=chrome_options)

    def driver(self):
        return self._driver
