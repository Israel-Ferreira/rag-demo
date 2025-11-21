from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import CSVLoader

from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore, RetrievalMode

from src.exceptions import LoadCsvException

class LangchainService:

    def __init__(self, model: str, qdrant_url: str):
        self.__embedding_llm =  GoogleGenerativeAIEmbeddings(model=model)
        self.__qdrant_url = qdrant_url

    def load_csv_in_vector_db(self, url_csv):
        try:
            csv_loader = CSVLoader(file_path=url_csv)
            pages = [page for page in csv_loader.load()]

            print(pages)

            collection_name = "bairros_sp"

            qdrant_vector_store = QdrantVectorStore.from_existing_collection(
                collection_name=collection_name,
                url=self.__qdrant_url,
                embedding=self.__embedding_llm,
                retrieval_mode=RetrievalMode.DENSE,
                vector_name="embedding"
            )


            qdrant_vector_store.add_documents(pages)

        except Exception as e:
            raise LoadCsvException(e)

        
    def load_wikipedia_info(self):
        pass