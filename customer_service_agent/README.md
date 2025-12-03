# Customer Service Agent

## Setup

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Set up environment variables:
    - Copy `.env.template` to `.env`
    - Fill in your API keys in `.env`

3.  Run the agent:
    ```bash
    python main.py
    ```

## Structure

- `data/`: Knowledge base documents
- `src/`: Source code
    - `agent/`: LangGraph agent logic
    - `database/`: Database connections
    - `utils/`: Helper functions
    - `frontend/`: React frontend application

## Frontend Setup

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Run the development server:
    ```bash
    npm run dev
    ```

4.  Build for production:
    ```bash
    npm run build
    ```

The frontend will be available at `http://localhost:5173` (by default). It proxies API requests to `http://localhost:8000`.
