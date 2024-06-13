from function import Function
from time import sleep
from logger import Logger
import seletor
import logging
import pandas as pd
from pathlib import Path

caminho_arquivos = Path(__file__).parent


for file_path in caminho_arquivos.glob(f"*.xlsx"):
    try:
        file_path.unlink()  # Deleta o arquivo
        print(f"{file_path} deletado com sucesso")
    except Exception as e:
        print(f"Erro ao deletar {file_path}: {e}")

for file_path in caminho_arquivos.glob(f"*.log"):
    try:
        file_path.unlink()  # Deleta o arquivo
        print(f"{file_path} deletado com sucesso")
    except Exception as e:
        print(f"Erro ao deletar {file_path}: {e}")

# Criar uma instância da classe Logger
logger_instance = Logger()

# Configurar o arquivo de log
logger_instance.configurar_arquivo_log()

# Teste para verificar se o log está funcionando
log = logging.getLogger(__name__)


if __name__ == "__main__":

    browser = Function()

    browser.url("https://rpachallenge.com/")
    download = browser.xpath(
        10, "/html/body/app-root/div[2]/app-rpa1/div/div[1]/div[6]/a"
    )
    start = browser.xpath(
        10, "/html/body/app-root/div[2]/app-rpa1/div/div[1]/div[6]/button"
    )
    browser.click(download)

    

    pause: bool = True

    while pause:
        espera_download = browser.check_downloaded(caminho_arquivos, ".xlsx")
        if espera_download == True:
            pause = False
        else:
            pause = True
    try:

        data_frame = pd.read_excel("challenge.xlsx", engine="openpyxl")
    except TimeoutError as e:
        log.error(f"Falha no download do arquivo: {e}")

    browser.click(start)
    for index, row in data_frame.iterrows():
        email = browser.xpath(10, seletor.EMAIL)
        telefone = browser.xpath(10, seletor.PHONE)
        endereco = browser.xpath(10, seletor.ADDRESS)
        primeiro_nome = browser.xpath(10, seletor.FIRST_NAME)
        sobrenome = browser.xpath(10, seletor.LAST_NAME)
        empresa = browser.xpath(10, seletor.COMPANY_NAME)
        funcao = browser.xpath(10, seletor.ROLE_IN_COMPANY)
        enviar = browser.xpath(
            10, "/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/input"
        )
        try:
            log.info("Digitando E-mail")
            browser.digitar(row["Email"], elemento=email)

            log.info("Digitando Phone Number")
            browser.digitar(row["Phone Number"], elemento=telefone)

            log.info("Digitando Address")
            browser.digitar(row["Address"], elemento=endereco)

            log.info("Digitando First Name")
            browser.digitar(row["First Name"], elemento=primeiro_nome)

            log.info("Digitando Last Name")
            browser.digitar(row["Last Name "], elemento=sobrenome)

            log.info("Digitando Company Name")
            browser.digitar(row["Company Name"], elemento=empresa)

            log.info(f"Digitando Role in Company: {row["Role in Company"]}")
            browser.digitar(row["Role in Company"], elemento=funcao)

            browser.click(enviar)
            log.info("Enviado com sucesso")
        except Exception as ex:
            log.error(f"Erro no processo: {ex}")
    sleep(10)
    browser.driver.quit()
