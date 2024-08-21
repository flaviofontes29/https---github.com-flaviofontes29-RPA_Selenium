from webdriver import Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import glob

class Function:
    def __init__(self) -> None:
        # Inicializa o browser e o driver, e prepara as ações do mouse/teclado (ActionChains)
        self.browser = Browser()
        self.driver = self.browser.driver()
        self.action = ActionChains(driver=self.driver)

    def url(self, url: str):
        # Carrega a página web especificada pela URL
        self._url = self.driver.get(url=url)

    def xpath(self, time: int, name: str):
        # Aguarda até que o elemento identificado pelo XPath esteja presente na página e o retorna
        self.elemento = WebDriverWait(self.driver, int(time)).until(
            EC.presence_of_element_located((By.XPATH, name))
        )
        return self.elemento

    def css(self, time: int, name: str):
        # Aguarda até que o elemento identificado pelo seletor CSS esteja presente na página e o retorna
        self.elemento = WebDriverWait(self.driver, int(time)).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, name))
        )
        return self.elemento

    def tag(self, time: int, name: str):
        # Aguarda até que o elemento identificado pelo nome da tag esteja presente na página e o retorna
        self.elemento = WebDriverWait(self.driver, int(time)).until(
            EC.presence_of_element_located((By.TAG_NAME, name))
        )
        return self.elemento

    def class_name(self, time: int, name: str):
        # Aguarda até que o elemento identificado pelo nome da classe esteja presente na página e o retorna
        self.elemento = WebDriverWait(self.driver, int(time)).until(
            EC.presence_of_element_located((By.CLASS_NAME, name))
        )
        return self.elemento

    def digitar(self, texto: str, elemento):
        # Simula a digitação de texto em um elemento usando ActionChains
        self.action.move_to_element(elemento)
        self.action.click(elemento)
        self.action.send_keys(texto)
        self.action.perform()

    def digitar_js(self, texto: str, elemento):
        # Insere texto em um elemento usando JavaScript
        self.driver.execute_script(f"arguments[0].value='{texto}';", elemento)

    def click(self, elemento):
        # Simula um clique em um elemento usando ActionChains
        self.action.move_to_element(elemento)
        self.action.click(elemento)
        self.action.perform()

    def click_js(self, elemento):
        # Simula um clique em um elemento usando JavaScript
        self.driver.execute_script("arguments[0].click();", elemento)

    def check_downloaded(self, download_dir: str, extension: str) -> bool:
        # Verifica se há arquivos baixados com a extensão especificada no diretório de downloads
        files = glob.glob(f"{download_dir}/*{extension}")
        return len(files) > 0  # Retorna True se encontrar arquivos, caso contrário, False