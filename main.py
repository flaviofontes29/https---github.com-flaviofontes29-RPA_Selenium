from function import Function
from time import sleep
from logger import Logger
import seletor
import logging
import pandas as pd
from pathlib import Path
from datetime import datetime
import urllib3

def main():
    caminho_arquivos = Path(__file__).parent
    meus_downloads = Path.home() / "Downloads"

    data_atual = datetime.now()
    data_formatada = data_atual.strftime("%d-%m-%Y")
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

    data = {"Round": [], "Status": [], "Data": []}
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
        return
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
            log.info(f"Digitando E-mail: {row['Email']}")
            browser.digitar(row["Email"], elemento=email)

            log.info(f"Digitando Phone Number: {row['Phone Number']}")
            browser.digitar(row["Phone Number"], elemento=telefone)

            log.info(f"Digitando Address: {row['Address']}")
            browser.digitar(row["Address"], elemento=endereco)

            log.info(f"Digitando First Name: {row['First Name']}")
            browser.digitar(row["First Name"], elemento=primeiro_nome)

            log.info(f"Digitando Last Name: {row['Last Name ']}")
            browser.digitar(row["Last Name "], elemento=sobrenome)

            log.info(f"Digitando Company Name: {row['Company Name']}")
            browser.digitar(row["Company Name"], elemento=empresa)

            log.info(f"Digitando Role in Company: {row['Role in Company']}")
            browser.digitar(row["Role in Company"], elemento=funcao)

            browser.click(enviar)
            log.info("Enviado com sucesso")
            data["Round"].append(index +1)
            data["Status"].append("Sucesso")
            data["Data"].append(data_formatada)
        except KeyError as ex:
            log.error(f"Ocorreu um erro mapeado: {ex}")
            email.clear()
            telefone.clear()
            endereco.clear()
            primeiro_nome.clear()
            sobrenome.clear()
            empresa.clear()
            funcao.clear()
            data["Round"].append(index+1)
            data["Status"].append(f"Ocorreu um erro mapeado: {ex}")
            data["Data"].append(data_formatada)
        except Exception as ex:
            log.error(f"Ocorreu um erro não esperado: {ex}")
            email.clear()
            telefone.clear()
            endereco.clear()
            primeiro_nome.clear()
            sobrenome.clear()
            empresa.clear()
            funcao.clear()
            data["Round"].append(index+1)
            data["Status"].append(f"Ocorreu um erro mapeado: {ex}")
            data["Data"].append(data_formatada)
        except urllib3.exceptions.NewConnectionError as ex:
            log.critical(f"Ocorreu um erro grave: {ex}")
    sleep(3)
    browser.driver.quit()

    df = pd.DataFrame(data=data)
    try:
        
        df.to_excel(
            f"{meus_downloads}\Relatório-{data_formatada}.xlsx",
            index=False,
            sheet_name="Relatório",
        )
        log.info(f"Relatório salvo em {meus_downloads / f'Relatório_{data_formatada}.xlsx'}")
    except EnvironmentError as ex:
        log.error(f"Caminho não encontrado: {ex}")