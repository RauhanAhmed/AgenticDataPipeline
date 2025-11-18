from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from utils.initMethods import readYaml, getConfig
from utils.exceptions import CustomException
from langchain_cerebras import ChatCerebras
from utils.logger import logger
import os

config = getConfig(os.path.join(os.getcwd(), "config.ini"))
prompts = readYaml(os.path.join(os.getcwd(), "prompts.yaml"))

class SynthesizerAgent:
    def __init__(self) -> None:
        try:
            logger.info("INITIALIZING SYNTHESIZER AGENT")
            promptTemplate = ChatPromptTemplate.from_template(prompts.get("synthesizerTemplate"))
            llm = ChatCerebras(
                model = config.get("SYNTHESIZERAGENT", "modelName"),
                temperature = config.getfloat("SYNTHESIZERAGENT", "temperature"),
                max_tokens = config.getint("SYNTHESIZERAGENT", "maxTokens")
            )
            chain = RunnablePassthrough() | promptTemplate | llm | StrOutputParser()
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