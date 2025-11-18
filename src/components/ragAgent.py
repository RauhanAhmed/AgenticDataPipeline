from langchain_qdrant import FastEmbedSparse, RetrievalMode
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from utils.initMethods import getConfig, readYaml
from langchain_qdrant import QdrantVectorStore
from utils.exceptions import CustomException
from langchain_cerebras import ChatCerebras
from qdrant_client import QdrantClient
from utils.logger import logger
import os

config = getConfig(os.path.join(os.getcwd(), "config.ini"))

modelName = config.get("RAGAGENT", "denseEmbeddings")
modelKwargs = {'device': 'cpu'}
encodeKwargs = {'normalize_embeddings': True}
embeddings = HuggingFaceEmbeddings(
    model_name=modelName,
    model_kwargs=modelKwargs,
    encode_kwargs=encodeKwargs
)

sparseEmbeddings = FastEmbedSparse(model_name=config.get("RAGAGENT", "sparseEmbeddings"))

class RAGAgent:
    def __init__(self) -> None:
        try:
            logger.info("INITIALIZING RAG AGENT")
            client = QdrantClient(
                url=os.environ.get("QDRANT_URL"),
                api_key=os.environ.get("QDRANT_API_KEY"),
            )
            vectorStore = QdrantVectorStore(
                client=client,
                collection_name="sampleCollection",
                embedding=embeddings,
                vector_name="semantic-search",
                sparse_vector_name="syntactic-search",
                retrieval_mode=RetrievalMode.SPARSE,
                sparse_embedding=sparseEmbeddings
            )
            promptTemplate = ChatPromptTemplate.from_template(readYaml(os.path.join(os.getcwd(), "prompts.yaml").get("ragTemplate")))
            retriever = vectorStore.as_retriever(search_kwargs = {"k": 5})
            llm = ChatCerebras(
                model = config.get("RAGAGENT", "modelName"),
                temperature = config.getint("RAGAGENT", "temperature"),
                max_tokens = config.getint("RAGAGENT", "maxTokens")
            )
            chain = {"query": RunnablePassthrough(), "context": RunnablePassthrough() | retriever} | promptTemplate | llm | StrOutputParser()
            self.chain = chain
        except Exception as e:
            exception = CustomException(e)
            logger.error(exception)
            raise exception

    def query(self, query) -> str:
        try:
            output = self.chain.invoke(query)
            return output
        except Exception as e:
            exception = CustomException(e)
            logger.error(exception)
            raise exception