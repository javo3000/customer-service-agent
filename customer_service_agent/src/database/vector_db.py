from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from src.config import settings
from typing import List
import os
import logging

logger = logging.getLogger(__name__)

class VectorDB:
    def __init__(self, index_name: str = "legal_docs_index"):
        """
        Initializes the FAISS vector store and embedding function.
        """
        # Ensure data directory exists
        self.persist_directory = os.path.join(os.getcwd(), "data", "faiss_index")
        os.makedirs(self.persist_directory, exist_ok=True)
        self.index_name = index_name
        
        try:
            self.embedding_function = OpenAIEmbeddings(
                api_key=settings.OPENAI_API_KEY.get_secret_value()
            )
            
            # Load existing index if it exists, otherwise initialize empty
            index_file_path = os.path.join(self.persist_directory, f"{self.index_name}.faiss")
            if os.path.exists(index_file_path):
                logger.info("Loading existing FAISS index...")
                self.vector_store = FAISS.load_local(
                    self.persist_directory, 
                    self.embedding_function, 
                    index_name=self.index_name,
                    allow_dangerous_deserialization=True # Safe since we created it
                )
            else:
                logger.info("Initializing new FAISS index...")
                # FAISS requires at least one document to initialize or a specific setup
                # We'll initialize it lazily or with a dummy doc if needed, 
                # but for now let's handle it by checking in add_documents
                self.vector_store = None
            
        except Exception as e:
            logger.error(f"Failed to initialize VectorDB: {e}")
            raise e

    def add_documents(self, documents: List[Document]):
        """
        Adds documents to the vector database.
        """
        if not documents:
            return

        try:
            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(
                    documents, 
                    self.embedding_function
                )
            else:
                self.vector_store.add_documents(documents)
            
            # Save index
            self.vector_store.save_local(self.persist_directory, index_name=self.index_name)
            logger.info(f"Added {len(documents)} documents to FAISS and saved.")
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise e

    def search(self, query: str, limit: int = 3) -> List[Document]:
        """
        Searches for documents relevant to the query.
        """
        if self.vector_store is None:
            logger.warning("Vector store is empty.")
            return []
            
        try:
            return self.vector_store.similarity_search(query, k=limit)
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
