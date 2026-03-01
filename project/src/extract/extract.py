import os
import zipfile
import kaggle
import logging

def extract_data() -> str:
    try:
        logging.info("Iniciando extração do dataset.")

        kaggle.api.authenticate()

        # Diretório onde os dados serão salvos
        raw_dir = os.path.join("data", "raw")
        os.makedirs(raw_dir, exist_ok=True)

        # Caminho do zip dentro da pasta raw
        zip_file = os.path.join(raw_dir, "animal-data.zip")

        # Faz o download se ainda não existir
        if not os.path.exists(zip_file):
            kaggle.api.dataset_download_files(
                "jinbonnie/animal-data",
                path=raw_dir,
                unzip=False
            )

        # Extrai os arquivos na mesma pasta raw
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(raw_dir)

        # Lê o CSV extraído
        csv_path = os.path.join(raw_dir, "animal-data.csv")

        logging.info("Extração concluída com sucesso.")
        return csv_path

    except Exception as e:
        logging.error(f"Erro ao extrair dados: {e}")
        raise