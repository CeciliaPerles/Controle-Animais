import os
import pandas as pd
import logging
import datetime
from sqlalchemy import create_engine

def save_to_mysql(df: pd.DataFrame, table_name:str) -> None:
    try:
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        host = os.getenv("MYSQL_HOST")
        port = os.getenv("MYSQL_PORT")
        db = os.getenv("MYSQL_DATABASE")

        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")
        df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)
        logging.info("Tabela salva no MySQL.")

    except Exception as e:
        logging.error(f"Erro ao salvar no MySQL: {e}")
        raise e


def save_to_parquet(df: pd.DataFrame, output_dir: str, file_name: str) -> None:
    try:
        os.makedirs(output_dir, exist_ok=True)
        logging.info(f"Diretório de saída: {output_dir}")

        if df.empty:
            logging.warning("DataFrame está vazio. Nenhum arquivo será salvo.")
            return

        # Converte colunas do tipo object para string
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype(str)

        file_path = os.path.join(output_dir, f"{file_name.lower()}.parquet")
        df.to_parquet(file_path, index=False)

        logging.info(f"Arquivo salvo.")

    except PermissionError:
        logging.error(f"Sem permissão para escrever em: {output_dir}")
        raise

    except Exception as e:
        logging.error(f"Erro ao salvar arquivo Parquet: {e}")
        raise

def save_to_csv(df: pd.DataFrame, output_dir: str, file_name: str) -> None:
    try:
        os.makedirs(output_dir, exist_ok=True)
        logging.info(f"Diretório de saída: {output_dir}")

        if df.empty:
            logging.warning("DataFrame está vazio. Nenhum arquivo será salvo.")
            return

        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype(str)

        file_path = os.path.join(output_dir, f"{file_name.lower()}.csv")
        df.to_csv(file_path, index=False)

        logging.info(f"Arquivo salvo.")

    except PermissionError:
        logging.error(f"Sem permissão para escrever em: {output_dir}")
        raise

    except Exception as e:
        logging.error(f"Erro ao salvar arquivo CSV: {e}")
        raise


def load_data() -> None:
    domain_names = [
        "dados_performance",
        "dados_pessoais",
        "dados_profissionais"
    ]

    base_transform_dir = os.path.join("data", "transform")

    for name in domain_names:
        parquet_path = os.path.join(base_transform_dir, f"{name}.parquet")

        if not os.path.exists(parquet_path):
            logging.warning(f"Arquivo não encontrado: {parquet_path}")
            continue

        df = pd.read_parquet(parquet_path)

        save_to_csv(df, "data/output/csv", name)
        save_to_parquet(df, "data/output/parquet", name)
        save_to_mysql(df, name)