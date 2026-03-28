# Workmerate Tax customer Support - AI Customer Service Agent

A **LangGraph-powered** AI customer service agent with real-time streaming responses, web search fallback, and a modern React chat interface.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)
![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react)
![LangGraph](https://img.shields.io/badge/LangGraph-Powered-orange)

---

## Features

- **Intelligent Routing** - Automatically routes queries to appropriate data sources (MongoDB, Vector DB, or Web)
- **Context-Aware Fallback** - If internal knowledge is insufficient, automatically searches the web via Tavily
- **Real-Time Streaming** - Token-by-token response streaming with "Thinking..." indicator
- **Formal Tax Advisory Persona** - Professional, formal tone suitable for financial/tax services
- **Security Built-In** - Prompt injection protection and input sanitization
- **Observability** - Langfuse integration for tracing and monitoring

---

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React Chat    │────▶│  FastAPI /ask   │────▶│   LangGraph     │
│    Frontend     │◀────│   (SSE Stream)  │◀────│    Workflow     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                        ┌───────────────────────────────┼───────────────────────────────┐
                        │                               │                               │
                        ▼                               ▼                               ▼
                ┌───────────────┐              ┌───────────────┐              ┌───────────────┐
                │   MongoDB     │              │  FAISS Vector │              │    Tavily     │
                │   (Orders)    │              │   DB (Docs)   │              │  (Web Search) │
                └───────────────┘              └───────────────┘              └───────────────┘
```

### LangGraph Workflow

```
START → Orchestrator → Tool Node → Generate → [Context Sufficient?]
                                                      │
                                                Yes → END
                                                No (retry=0) → Web Search → Orchestrator
                                                No (retry≥1) → Ask User → END
```

---

## Project Structure

```
customer_service_agent/
├── main.py                      # FastAPI entry point
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create from .env.template)
│
├── src/
│   ├── config.py                # Pydantic settings
│   ├── agent/
│   │   ├── graph.py             # LangGraph workflow definition
│   │   ├── state.py             # AgentState TypedDict
│   │   ├── tools.py             # Tool wrappers (order, search, web)
│   │   └── nodes/
│   │       ├── orchestrator.py  # Query routing
│   │       ├── tool_node.py     # Data retrieval execution
│   │       └── generate.py      # LLM response generation
│   └── database/
│       ├── vector_db.py         # FAISS wrapper
│       └── mongo_client.py      # MongoDB client
│
├── data/
│   ├── docs/                    # Source PDFs for ingestion
│   └── faiss_index/             # Persisted vector embeddings
│
└── frontend/                    # React + Vite chat UI
    ├── src/
    │   ├── components/
    │   │   ├── ChatWidget.jsx
    │   │   ├── MessageBubble.jsx
    │   │   └── ...
    │   └── api.js
    └── package.json
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB (cloud or local)
- API Keys: OpenAI-compatible LLM, Tavily, (optional) Langfuse

### 1. Clone and Install Backend

```bash
cd customer_service_agent
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.template .env
```

Edit `.env` with your credentials:

```env
OPENAI_API_KEY=your_openai_key
OPENAI_API_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY_AI_GRID=your_ai_grid_key  # Or same as above
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net
TAVILY_API_KEY=your_tavily_key

# Optional
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
```

### 3. Ingest Documents (Optional)

```bash
python -m src.scripts.ingest_docs
```

### 4. Run Backend

```bash
python main.py
```

Backend runs at `http://localhost:8000`

### 5. Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/ask` | POST | Query the agent (SSE streaming) |

### POST /ask

**Request:**
```json
{
  "question": "What is my order status?",
  "chat_history": []
}
```

**Response:** Server-Sent Events (SSE) stream with:
- `{type: "thinking", content: true}` - Processing started
- `{type: "metadata", content: {route, intent, needed_sources}}` - Routing info
- `{type: "status", content: "Searching..."}` - Status updates
- `{type: "token", content: "Dear"}` - Response tokens

---

## Testing

```bash
# Test individual components
python test_main.py
python test_security.py
python test_streaming.py
```

---

## Deployment

### Recommended VPS Specs

| Usage | CPU | RAM | Storage |
|-------|-----|-----|---------|
| Development/Demo | 4 vCPU | 8 GB | 75 GB |
| Production | 6+ vCPU | 12+ GB | 100 GB |

### Production Checklist

- [ ] Set `ENVIRONMENT=production` in `.env`
- [ ] Use a process manager (PM2, systemd, or Docker)
- [ ] Set up HTTPS with reverse proxy (nginx/Caddy)
- [ ] Configure CORS for your domain
- [ ] Enable Langfuse for monitoring

---

## Observability

The agent integrates with **Langfuse** for:
- Trace visualization
- Token usage tracking
- Latency monitoring
- Error tracking

Set `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` in `.env` to enable.

---

## Security

- **Prompt Injection Protection** - System prompts include explicit security constraints
- **Input Sanitization** - User inputs are validated before processing
- **Secret Management** - All API keys use Pydantic's `SecretStr`
- **Delimiter Protocol** - Context is wrapped in clear delimiters to prevent injection

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Tavily](https://tavily.com/) - Web search API
- [FAISS](https://github.com/facebookresearch/faiss) - Vector similarity search
