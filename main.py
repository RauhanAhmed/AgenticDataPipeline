from api.models import FlagOutput, WorkflowQuery
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from api.services import FastAPIService
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

service = FastAPIService()
app = FastAPI(title="Agentic Data Pipeline Endpoints")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/answerQuery")
async def answerQuery(queryModel: WorkflowQuery):
    try:
        response = service.answerQuery(workflowQueryModel=queryModel)
        return JSONResponse(status_code=200, content={"response": response})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/flag")
async def flagOutput(flagModel: FlagOutput):
    try:
        response = service.flagResponse(likedOrFlaggedModel=flagModel)
        return JSONResponse(status_code=200, content={"response": response})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))