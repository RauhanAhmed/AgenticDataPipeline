from api.models import FlagOutput, WorkflowQuery
from src.workflows.workflow import workflow
from sqlalchemy import create_engine, text
import os

class FastAPIService:
    def __init__(self):
        self.engine = create_engine(
            os.environ.get("POSTGRE_CONNECTION_STRING")
        )
    
    def answerQuery(self, workflowQueryModel: WorkflowQuery) -> str:
        return workflow.run(workflowQueryModel.query)
    
    def flagResponse(self, likedOrFlaggedModel: FlagOutput) -> str:
        with self.engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO feedback (query, response, flag, feedback)
                    VALUES (:query, :response, :flag, :feedback)
                """),
                {
                    "query": likedOrFlaggedModel.query,
                    "response": likedOrFlaggedModel.response,
                    "flag": likedOrFlaggedModel.flag,
                    "feedback": likedOrFlaggedModel.feedback
                }
            )
            conn.commit()
        return "Data inserted successfully"