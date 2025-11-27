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
