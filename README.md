# **Agentic Data Pipeline: An Architectural Overview**

<p align="center">
  <img src="demo/workflowDiagram.png" alt="Agentic Data Pipeline Architecture" width="800"/>
</p>

<p align="center">
    <a href="https://github.com/RauhanAhmed/AgenticDataPipeline"><img alt="GitHub Repo" src="https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge&logo=github"></a>
    <a href="https://agenticdatapipeline.lovable.app/"><img alt="Frontend" src="https://img.shields.io/badge/Live-Frontend-brightgreen?style=for-the-badge"></a>
    <a href="https://rauhan-agenticdatapipeline.hf.space/docs"><img alt="Backend" src="https://img.shields.io/badge/Live-Backend-orange?style=for-the-badge"></a>
</p>

---

# **1. Introduction & Project Philosophy**

Working with data usually means dealing with scattered sources: PDFs, wiki pages, SQL databases, CSVs, and the internet. Answering a real question often means pulling something from each of them, understanding the context, and then combining it all into a clear answer.

The **Agentic Data Pipeline** is built around this idea. Instead of relying on a single “super model,” the system uses **multiple small, focused AI agents**, each good at one thing—document retrieval, SQL queries, web search, or reasoning. Their outputs are combined by a final synthesizer agent that produces a single coherent answer.

The goal is simple:
**Break the problem into specialized steps, run them in parallel, and combine the results intelligently.**

This README explains the entire architecture in a practical, developer-friendly way.

### **1.1. Live Demonstrations**

* **Frontend UI:** [https://agenticdatapipeline.lovable.app](https://agenticdatapipeline.lovable.app)
* **Backend API (Swagger):** [https://rauhan-agenticdatapipeline.hf.space/docs](https://rauhan-agenticdatapipeline.hf.space/docs)

---

# **2. System Architecture & Data Flow**

The system is implemented as a **stateful Directed Acyclic Graph (DAG)** using **LangGraph**, with **FastAPI** as the public-facing interface.

## **2.1. AgentState**

All agents exchange information through a shared state object:

```python
class AgentState(TypedDict):
    query: str
    ragResults: Optional[str]
    sqlResults: Optional[str]
    webResults: Optional[str]
    reasoningResults: Optional[str]
    finalAnswer: Optional[str]
```

Each agent reads from the state, performs its task, and writes back to it.

## **2.2. End-to-End Flow**

1. A query comes into the `/answerQuery` API endpoint.
2. A fresh `AgentState` is created with the user query.
3. The state enters the LangGraph workflow.
4. The system fans out into **four parallel agents**:

   * RAG (internal docs)
   * PostgreSQL (structured DB)
   * Internet Search (real-time info)
   * Reasoning (general logic)
5. Each agent updates its portion of the state.
6. LangGraph waits until all four have finished.
7. A final **Synthesizer Agent** combines everything.
8. The API returns the answer from `finalAnswer`.

---

# **3. Agent Details**

Each agent is built around a specific model and set of tools suited to its job.

## **3.1. RAG Agent (“The Librarian”)**

* **Model:** Llama 3.3 70B
* **Purpose:** Works with your internal PDFs, wikis, and documents.
* **Retrieval:**

  * Dense search via `BAAI/bge-large-en-v1.5` embeddings in **Qdrant**
  * Sparse search via **BM25**
* The agent reads `query` and writes to `ragResults`.

## **3.2. PostgreSQL Agent (“The Data Whiz”)**

* **Model:** zai-glm-4.6
* Converts natural language into SQL queries.
* Uses SQLAlchemy + LangChain SQL toolkit for schema understanding.
* Reads the user query → writes SQL results to `sqlResults`.

## **3.3. Reasoning Agent (“The Thinker”)**

* **Model:** qwen-3-32b
* Handles questions requiring logic or explanation rather than external data.
* Uses Chain-of-Thought prompting.
* Writes its output to `reasoningResults`.

## **3.4. Internet Search Agent (“The Web Surfer”)**

* Uses Google Serper for realtime search.
* Lightweight wrapper around the Serper API.
* Writes results to `webResults`.

## **3.5. Synthesizer Agent (“The Editor-in-Chief”)**

* **Model:** gpt-oss-120b
* Combines results from all other agents.
* Follows a strict information priority:

  1. Internal documents + SQL (highest trust)
  2. Internet search (live context)
  3. Reasoning agent (explanations, logic)
* Writes the final unified response into `finalAnswer`.

---

# **4. Technology Stack**

| Layer       | Technology       | Reason                                  |
| ----------- | ---------------- | --------------------------------------- |
| API         | FastAPI, Uvicorn | Fast, async, clean docs                 |
| Workflow    | LangGraph        | Native state handling & parallel agents |
| VectorDB    | Qdrant           | Supports dense + sparse hybrid search   |
| DB          | PostgreSQL       | Solid relational backend                |
| LLM Hosting | Cerebras         | Fast and cost-effective inference       |
| Containers  | Docker           | Easy deployment and reproducibility     |

---

# **5. Visual Documentation**

### **5.1. Sample Outputs**

These screenshots show how the system responds to different user queries.

<p align="center">
  <img src="demo/demo1.png" width="800"/><br>
  <img src="demo/demo2.png" width="800"/><br>
  <img src="demo/demo3.png" width="800"/><br>
  <img src="demo/demo4.png" width="800"/><br>
  <img src="demo/demo5.png" width="800"/>
</p>


### **5.2. Frontend & API**

<p align="center">
  <b>Frontend Interface</b><br>
  <img src="demo/frontend.png" width="800"/>
</p>

<p align="center">
  <b>FastAPI Swagger UI</b><br>
  <img src="demo/fastapiSwaggerUI.png" width="800"/>
</p>

### **5.3. Workflow & Architecture**

<p align="center">
  <b>Workflow Diagram</b><br>
  <img src="demo/workflowDiagram.png" width="800"/>
</p>

<p align="center">
  <b>LangGraph Mermaid Export</b><br>
  <img src="demo/langgrapphMermaidExport.png" width="800"/>
</p>

### **5.4. Storage & Retrieval Layers**

<p align="center">
  <b>Qdrant VectorDB</b><br>
  <img src="demo/qdrantVectoDB.png" width="800"/>
</p>

<p align="center">
  <b>PostgreSQL Agent Data</b><br>
  <img src="demo/postgreSQLAgentData.png" width="800"/>
</p>

### **5.5. Monitoring & Tracing**

<p align="center">
  <b>LangSmith Dashboard</b><br>
  <img src="demo/langsmithDashboard.png" width="800"/>
</p>

<p align="center">
  <b>LangSmith Tracing</b><br>
  <img src="demo/langsmithTracing.png" width="800"/>
</p>

---

# **6. Local Installation Guide**

## **6.1. Requirements**

* Python 3.12+
* Docker Engine

## **6.2. Installation Steps**

### **1. Clone the repo**

```bash
git clone https://github.com/RauhanAhmed/AgenticDataPipeline.git
cd AgenticDataPipeline
```

### **2. Create a `.env` file**

You’ll need keys for:

* QDRANT_API_KEY
* QDRANT_URL
* POSTGRE_CONNECTION_STRING
* CEREBRAS_API_KEY
* SERPER_API_KEY
  (and any LLM keys from your config)

### **3. Create a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### **4. Build & run the Docker image**

```bash
docker build -t agentic-data-pipeline .
docker run -p 7860:7860 -d --env-file .env agentic-data-pipeline
```

## **6.3. Populate Data**

### **Vector Database (Qdrant)**

Run:

```
notebooks/VectorDBPopulator.ipynb
```

### **PostgreSQL Database**

Run:

```
notebooks/SQLPoplulator.ipynb
```

## **6.4. Test the Pipeline**

```bash
curl -X POST http://localhost:7860/answerQuery \
-H "Content-Type: application/json" \
-d '{"query": "How many data scientist jobs are available in California?"}'
```

---

# **7. Roadmap**

* [ ] Add Reciprocal Rank Fusion (RRF) for improved retrieval merge
* [ ] Build a feedback-driven fine-tuning loop
* [ ] Introduce more specialized agents (filesystem, JIRA, etc.)
* [ ] Optional Streamlit/Gradio UI

---

# **8. Author**

Built by **Rauhan Ahmed**
Portfolio: [https://rauhanahmed.in](https://rauhanahmed.in)

Contributions are welcome — feel free to open an issue or PR.

---

# **9. License**

MIT License. See the `LICENSE` file.