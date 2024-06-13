import logging
import datetime


class Logger:
    def configurar_arquivo_log(self) -> None:
        """
        Configura arquivo de log
        """
        # Formato da data
        current_datetime = datetime.datetime.now()
        date_time_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

        # Caminho para salvar o log
        caminho_arquivo_log = f"Logs_{date_time_str}.log"

        print(f"Configurando o log para ser salvo em: {caminho_arquivo_log}")

        # Tratamento para evitar erros na geração do log
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # Configuração do arquivo de log
        logging.basicConfig(
            filename=caminho_arquivo_log,
            encoding="utf-8",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s: %(message)s",
        )

        print("Configuração de log concluída")
