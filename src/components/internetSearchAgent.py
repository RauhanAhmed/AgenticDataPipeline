from langchain_community.utilities import GoogleSerperAPIWrapper
from utils.exceptions import CustomException
from utils.logger import logger
import os

class InternetSearchAgent:
    def __init__(self) -> None:
        logger.info("INITIALIZING INTERNET SEARCH AGENT")
        self.search = GoogleSerperAPIWrapper(serper_api_key=os.environ.get("SERPER_API_KEY"))

    def query(self, query) -> str:
        try:
            output = self.search.run(query)
            return output
        except Exception as e:
            exception = CustomException(e)
            logger.error(exception)
            raise exception