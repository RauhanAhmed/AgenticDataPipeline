from src.components.internetSearchAgent import InternetSearchAgent
from src.components.synthesizerAgent import SynthesizerAgent
from src.components.reasoningAgent import ReasoningAgent
from src.components.sqlAgent import PostgreSQLAgent
from langgraph.graph import START, END, StateGraph
from utils.exceptions import CustomException
from src.components.ragAgent import RAGAgent
from utils.logger import logger
from typing import TypedDict

class AgentState(TypedDict):
    internetResults: str
    reasoningResults: str
    sqlResults: str
    ragResults: str
    query: str
    finalAnswer: str

class Workflow:
    def __init__(self) -> None:
        self.internetSearchAgentObj = InternetSearchAgent()
        self.reasoningAgentObj = ReasoningAgent()
        self.ragAgentObj = RAGAgent()
        self.sqlAgentObj = PostgreSQLAgent()
        self.synthesizerAgentObj = SynthesizerAgent()

    def _internetSearchAgent(self, state: AgentState) -> dict:
        return {"internetResults": self.internetSearchAgentObj.query(query=state.get("query"))}

    def _reasoningAgent(self, state: AgentState) -> dict:
        return {"reasoningResults": self.reasoningAgentObj.query(query=state.get("query"))}

    def _ragAgent(self, state: AgentState) -> dict:
        return {"ragResults": self.ragAgentObj.query(query=state.get("query"))}

    def _sqlAgent(self, state: AgentState) -> dict:
        return {"sqlResults": self.sqlAgentObj.query(query=state.get("query"))}

    def _synthesizerAgent(self, state: AgentState) -> dict:
        return {"finalAnswer": self.synthesizerAgentObj.query({"query": state["query"], "reasoningOutput": state["reasoningResults"], "webOutput": state["internetResults"], "ragOutput": state["ragResults"], "sqlOutput": state["sqlResults"]})}

    def createWorkflow(self) -> None:
        try:
            logger.info("INITIALIZING LANGGRAPH WORKFLOW")
            graph = StateGraph(AgentState)
            graph.add_node("internetSearchAgent", self._internetSearchAgent, )
            graph.add_node("reasoningAgent", self._reasoningAgent,)
            graph.add_node("ragAgent", self._ragAgent)
            graph.add_node("sqlAgent", self._sqlAgent)
            graph.add_node("synthesizerAgent", self._synthesizerAgent, defer = True)
            graph.add_edge(START, "internetSearchAgent")
            graph.add_edge(START, "reasoningAgent")
            graph.add_edge(START, "ragAgent")
            graph.add_edge(START, "sqlAgent")
            graph.add_edge("internetSearchAgent", "synthesizerAgent")
            graph.add_edge("reasoningAgent", "synthesizerAgent")
            graph.add_edge("ragAgent", "synthesizerAgent")
            graph.add_edge("sqlAgent", "synthesizerAgent")
            graph.add_edge("synthesizerAgent", END)
            self.graph = graph.compile()
            return
        except Exception as e:
            exception = CustomException(e)
            logger.error(exception)
            raise exception

    def run(self, query: str) -> str:
        return self.graph.invoke({"query": query})["finalAnswer"]
    
workflow = Workflow()
workflow.createWorkflow()