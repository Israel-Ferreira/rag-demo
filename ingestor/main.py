import os

import logging

from dotenv import load_dotenv

from src.services import LangchainService, download_csv

logging.basicConfig(level=logging.INFO)


load_dotenv()

logger = logging.getLogger(__name__)



if "GOOGLE_API_KEY" not in os.environ or os.getenv("GOOGLE_API_KEY") == "":
    logger.error("Erro: A Váriavel de ambiente GOOGLE_API_KEY não está definida")
    exit(1)

if "QDRANT_URL" not in os.environ or os.getenv("QDRANT_URL") == "":
    logger.info("Erro: a váriavel de ambiente QDRANT_URL não está definida")
    exit(1)


if not os.path.exists("data"):
    os.mkdir("data")

if __name__ == "__main__":
    qdrant_url = os.getenv("QDRANT_URL")
    embedded_model = "models/gemini-embedding-001"

    try:
        url = "https://raw.githubusercontent.com/codigourbano/distritos-sp/refs/heads/master/distritos-sp.csv"
        csv_filename = "distritos-sp.csv"


        if not os.path.exists(f"data/{csv_filename}"):
            download_csv(url, csv_filename)



        
        lc_service = LangchainService(
            model=embedded_model,
            qdrant_url=qdrant_url
        )

        lc_service.load_csv_in_vector_db(f"data/{csv_filename}")
        

        logger.info("Executando o script")
        print("This script is being run directly.")
    except Exception as e:
        logger.error("Erro ao executar o loader: {e}")