from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

import os


load_dotenv()

collection_name = "bairros_sp"

embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")



vector_store = QdrantVectorStore.from_existing_collection(
    url=os.getenv("QDRANT_URL"),
    collection_name=collection_name,
    embedding=embedding_model
)

retriever = vector_store.as_retriever()



prompt_template = """
Você é um assistente especializado em bairros e distritos da cidade de São Paulo.
Ao perguntarem sobre um determinado bairro, especificamente sobre qual subprefeitura ele está contido, você deve responder de forma concisa
informativa e gentil.

Qualquer pergunta fora do tema, deve ser respondida com um 'Não sei a resposta para esse contexto';

Context: {context}
Question: {question}
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


resposta_cadeia = chain.invoke("Quais distritos estão associados com a subprefeitura de santana ?")
print(resposta_cadeia)

