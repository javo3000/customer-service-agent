"""
Generate node for creating final responses.
Uses formal tax advisory tone with LLM-based response generation.
"""
import logging
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.agent.state import AgentState
from src.config import settings

logger = logging.getLogger(__name__)

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3, # Low temperature for consistent, formal tone
    api_key=settings.OPENAI_API_KEY
)

# System prompt for the Tax Advisory persona
SYSTEM_PROMPT = """You are an elite AI Customer Service Agent for "AlFin Support", a premium financial and tax advisory service.

YOUR PERSONA:
- Tone: Highly formal, professional, polite, and authoritative (Tax Advisory style).
- Vocabulary: Use precise, elevated language (e.g., "regarding", "aforementioned", "kindly be advised", "regrettably").
- Structure: Clear, concise, and well-formatted with appropriate spacing.
- Signature: Always sign off with "Respectfully yours,\nCustomer Service Division".

YOUR INSTRUCTIONS:
1. Answer the user's question based ONLY on the provided CONTEXT (Order Data and/or Policy Documents).
2. If the context contains the answer, provide it clearly.
3. If the context is empty or does not contain the answer, politely apologize and state that you cannot retrieve the information based on the provided details.
4. If there is an error in the data, apologize and ask the user to contact support.
5. CITATIONS: If you use information from Policy Documents, cite the source at the end (e.g., "Source: Refund Policy").

CONTEXT:
{context}

USER QUESTION:
{question}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "{question}")
])

chain = prompt | llm | StrOutputParser()

def generate(state: AgentState) -> Dict:
    """
    Generates final answer using LLM with formal tax advisory tone.
    
    Args:
        state: Current agent state
        
    Returns:
        Dictionary with final_answer field
    """
    question = state.get("question", "")
    mongo_data = state.get("mongo_data", [])
    documents = state.get("documents", [])
    
    # Prepare context string
    context_str = _prepare_context(mongo_data, documents)
    
    try:
        # Generate response
        response = chain.invoke({
            "context": context_str,
            "question": question
        })
        
        return {"final_answer": response}
        
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return {
            "final_answer": "Dear Valued Client,\n\nWe regret to inform you that we are currently experiencing a technical issue processing your request. Please try again later.\n\nRespectfully yours,\nCustomer Service Division"
        }


def _prepare_context(mongo_data: List[dict], documents: List) -> str:
    """
    Format retrieved data into a single context string for the LLM.
    """
    context_parts = []
    
    # Format Order Data
    if mongo_data:
        for data in mongo_data:
            if "error" in data:
                context_parts.append(f"ORDER SYSTEM ERROR: {data['error']}")
            elif "result" in data:
                context_parts.append(f"ORDER DATA:\n{data['result']}")
    
    # Format Policy Documents
    if documents:
        context_parts.append("POLICY DOCUMENTS:")
        for i, doc in enumerate(documents, 1):
            content = doc.page_content
            source = doc.metadata.get("source", "Unknown Source")
            context_parts.append(f"Document {i} (Source: {source}):\n{content}")
            
    if not context_parts:
        return "NO DATA FOUND. The system could not retrieve any order details or policy documents."
        
    return "\n\n".join(context_parts)
