# **Agentic Data Pipeline: An Architectural Overview**

<p align="center">
  <img src="demo/architecture.png" alt="Agentic Data Pipeline Architecture" width="800"/>
</p>

<p align="center">
    <a href="https://github.com/RauhanAhmed/AgenticDataPipeline"><img alt="GitHub Repo" src="https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge&logo=github"></a>
    <a href="https://agenticdatapipeline.lovable.app/"><img alt="Frontend" src="https://img.shields.io/badge/Live-Frontend-brightgreen?style=for-the-badge"></a>
    <a href="https://rauhan-agenticdatapipeline.hf.space/docs"><img alt="Backend" src="https://img.shields.io/badge/Live-Backend-orange?style=for-the-badge"></a>
</p>

---

## **1. Introduction & Project Philosophy**

Data today lives everywhere — PDFs, random wiki pages, internal documents, SQL databases, and of course, the web. Answering real questions often means pulling pieces of information from all of these places and trying to make sense of them together.

The **Agentic Data Pipeline** is my attempt to build a system that does exactly that. Instead of relying on one large model to magically know everything, the system uses **multiple small, focused agents**, each good at one job: document search, SQL, web search, or logical reasoning. Their outputs are then combined by a final “synthesizer” agent.

Think of it as a small team of specialists, each contributing what they’re best at.

This document walks through how the system works under the hood.

### **1.1. Live Demos**

* **Frontend:** Ask questions directly via the lovable.dev interface
  [https://agenticdatapipeline.lovable.app](https://agenticdatapipeline.lovable.app)
* **Backend (Swagger UI):** Explore the API
  [https://rauhan-agenticdatapipeline.hf.space/docs](https://rauhan-agenticdatapipeline.hf.space/docs)

---

## **2. System Architecture & Data Flow**

The system is implemented as a **stateful DAG** using **LangGraph**, and exposed through a FastAPI service.

### **2.1. The `AgentState`**

All agents share information through a single state object called `AgentState`.
Every agent reads from it and writes its output back into it.

```python
class AgentState(TypedDict):
    query: str
    ragResults: Optional[str]
    sqlResults: Optional[str]
    webResults: Optional[str]
    reasoningResults: Optional[str]
    finalAnswer: Optional[str]
```

### **2.2. How a Query Flows Through the System**

1. The FastAPI server receives a query on `/answerQuery`.
2. A clean `AgentState` is created with the query.
3. The state enters the LangGraph workflow.
4. Four agents run **in parallel**:

   * RAG agent
   * SQL agent
   * Web search agent
   * Reasoning agent
5. Each agent adds its results back into the state.
6. LangGraph waits for all four to finish.
7. The combined state is passed to the Synthesizer agent.
8. A final answer is generated and stored in `finalAnswer`.
9. The system returns that answer back through the API.

---

## **3. The Agent Roster**

Each agent uses a different model and toolset suited for its role.

### **3.2.1. RAG Agent (“The Librarian”)**

* **Model:** Llama 3.3 70B
* **Purpose:** Works with internal documents
* **Hybrid Retrieval:**

  * Dense search using BAAI/bge-large-en-v1.5 (embeddings stored in Qdrant)
  * Sparse search using BM25
* **Writes:** `ragResults`

### **3.2.2. PostgreSQL Agent (“The Data Whiz”)**

* **Model:** zai-glm-4.6
* **Purpose:** Converts natural language to SQL
* **Schema-aware** thanks to SQLAlchemy and langchain’s SQL toolkit
* **Writes:** `sqlResults`

### **3.2.3. Reasoning Agent (“The Thinker”)**

* **Model:** qwen-3-32b
* **Purpose:** Handles explanations, logic, and step-by-step reasoning
* **CoT prompting** is used here
* **Writes:** `reasoningResults`

### **3.2.4. Internet Search Agent (“The Web Surfer”)**

* **Uses:** Google Serper API
* **Purpose:** Fetches real-time context from the web
* **Writes:** `webResults`

### **3.2.5. Synthesizer Agent (“The Editor-in-Chief”)**

* **Model:** gpt-oss-120b
* **Purpose:** Combines all other agents’ outputs into one coherent answer
* **Rule hierarchy:**

  1. RAG + SQL = highest trust
  2. Web search = latest context
  3. Reasoning = explanations/definitions
* **Writes:** `finalAnswer`

---

## **4. Technology Stack**

| Layer               | Technology       | Why                                   |
| ------------------- | ---------------- | ------------------------------------- |
| API                 | FastAPI, Uvicorn | Fast, async, easy documentation       |
| Agent orchestration | LangGraph        | Built-in parallelism + state handling |
| Vector DB           | Qdrant           | Hybrid search support                 |
| SQL DB              | PostgreSQL       | Reliable and feature-rich             |
| Inference           | Cerebras         | Very fast LLM serving                 |
| Deployment          | Docker           | Portable and consistent               |

---

## **5. Visual Documentation**

(Diagrams and screenshots remain unchanged.)

---

## **6. Getting Started**

### **6.1. Requirements**

* Python 3.9+
* Docker

### **6.2. Installation**

Clone the repo:

```bash
git clone https://github.com/RauhanAhmed/AgenticDataPipeline.git
cd AgenticDataPipeline
```

Add a `.env` with your keys (Qdrant, PostgreSQL, Serper, Cerebras, etc.).

Create a venv and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Build and run with Docker:

```bash
docker build -t agentic-data-pipeline .
docker run -p 8000:8000 -d --env-file .env agentic-data-pipeline
```

### **6.3. Populate Data**

Run the notebooks:

* `VectorDBPopulator.ipynb` → fills Qdrant
* `SQLPoplulator.ipynb` → fills PostgreSQL

### **6.4. Test Query**

```bash
curl -X POST http://localhost:8000/answerQuery \
-H "Content-Type: application/json" \
-d '{"query": "How many data scientist jobs are available in California?"}'
```

---

## **7. Roadmap**

* [ ] Add Reciprocal Rank Fusion (RRF)
* [ ] Feedback-based fine-tuning loop
* [ ] More agents (filesystem, JIRA, etc.)
* [ ] Streamlit/Gradio UI

---

## **8. Author**

Built by **Rauhan Ahmed**.
Portfolio: [https://rauhanahmed.in](https://rauhanahmed.in)

Contributions are welcome — feel free to open issues or PRs.

---

## **9. License**

MIT License.

---