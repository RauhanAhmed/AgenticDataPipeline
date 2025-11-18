from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from utils.exceptions import CustomException
from langchain_cerebras import ChatCerebras
from langchain.agents import create_agent
from utils.initMethods import getConfig
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine
from langchain_classic import hub
from utils.logger import logger
import os

promptTemplate = hub.pull("langchain-ai/sql-agent-system-prompt")
systemMessage = promptTemplate.format(dialect="PostgreSQL", top_k=5)

class PostgreSQLAgent:
    def __init__(self) -> None:
        try:
            logger.info("INITIALIZING SQL AGENT")
            self.config = getConfig(os.path.join(os.getcwd(), "config.ini"))
            self.engine = create_engine(os.environ.get("POSTGRE_CONNECTION_STRING"), poolclass = StaticPool)
            db = SQLDatabase(self.engine)
            llm = ChatCerebras(
                model = self.config.get("SQLAGENT", "modelName"),
                temperature = self.config.getfloat("SQLAGENT", "temperature"),
                max_tokens = self.config.getint("SQLAGENT", "maxTokens")
            )
            self.toolkit = SQLDatabaseToolkit(db = db, llm = llm)
            self.agent = create_agent(llm, self.toolkit.get_tools(), system_prompt=systemMessage)
        except Exception as e:
            exception = CustomException(e)
            logger.error(exception)
            raise exception

    def query(self, query) -> str:
        try:
            response = self.agent.invoke(
                {"messages": [("user", query)]}
            )
            return response["messages"][-1].content
        except Exception as e:
            exception = CustomException(e)
            logger.error(exception)
            raise exception