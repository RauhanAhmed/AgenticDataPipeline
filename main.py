from api.models import FlagOutput, WorkflowQuery
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from api.services import FastAPIService
from fastapi import FastAPI

service = FastAPIService()
app = FastAPI(title = "Agentic Data Pipeline Endpoints")

@app.post("/answerQuery")
async def answerQuery(queryModel: WorkflowQuery):
    try:
        response = service.answerQuery(workflowQueryModel = queryModel)
        return JSONResponse(status_code = 200, content = {"response": response})
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    
@app.post("/flag")
async def flagOutput(flagModel: WorkflowQuery):
    try:
        response = service.flagResponse(likedOrFlaggedModel = flagModel)
        return JSONResponse(status_code = 200, content = {"response": response})
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))