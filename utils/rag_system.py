"""
RAG (Retrieval-Augmented Generation) system using FAISS and LangChain
Combines patient medical records with medical knowledge base for personalized education
"""

import os
import pickle
import logging
from typing import List, Dict, Any, Optional
import numpy as np
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from utils.medical_knowledge import medical_knowledge

# Set up logging
logger = logging.getLogger(__name__)

class RAGSystem:
    """
    Retrieval-Augmented Generation system for medical education materials
    Uses FAISS vector store and BM25 retrieval for optimal document retrieval
    """
    
    def __init__(self, embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize RAG system with embeddings model and vector store
        
        Args:
            embeddings_model (str): HuggingFace model for text embeddings
        """
        self.embeddings_model = embeddings_model
        self.embeddings = None
        self.vector_store = None
        self.bm25_retriever = None
        self.ensemble_retriever = None
        
        # Paths for saving/loading vector store
        self.vector_store_path = "data/vector_store"
        self.bm25_path = "data/bm25_retriever.pkl"
        
        # Initialize components
        self._initialize_embeddings()
        self._initialize_vector_store()
        
        logger.info("RAG system initialized successfully")
    
    def _initialize_embeddings(self):
        """
        Initialize HuggingFace embeddings model
        """
        try:
            logger.info(f"Loading embeddings model: {self.embeddings_model}")
            
            # Use HuggingFace sentence transformers for embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embeddings_model,
                model_kwargs={'device': 'cpu'},  # Use CPU for compatibility
                encode_kwargs={'normalize_embeddings': True}  # Normalize for better similarity
            )
            
            logger.info("Embeddings model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading embeddings model: {str(e)}")
            logger.warning("Trying alternative embedding setup...")
            try:
                # Fallback to basic setup
                self.embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )
                logger.info("Fallback embeddings model loaded successfully")
            except Exception as fallback_error:
                logger.error(f"Fallback embeddings also failed: {str(fallback_error)}")
                raise Exception(f"Failed to load any embeddings model: {str(e)}")
    
    def _initialize_vector_store(self):
        """
        Initialize FAISS vector store with medical knowledge base
        """
        try:
            # Create data directory if it doesn't exist
            os.makedirs("data", exist_ok=True)
            
            # Try to load existing vector store
            if os.path.exists(self.vector_store_path):
                logger.info("Loading existing vector store...")
                self.vector_store = FAISS.load_local(
                    self.vector_store_path, 
                    self.embeddings,
                    allow_dangerous_deserialization=True  # Required for FAISS loading
                )
                logger.info("Existing vector store loaded successfully")
            else:
                logger.info("Creating new vector store with medical knowledge base...")
                self._create_vector_store()
            
            # Initialize BM25 retriever
            self._initialize_bm25_retriever()
            
        except Exception as e:
            logger.error(f"Error initializing vector store: {str(e)}")
            # If loading fails, create new vector store
            logger.info("Creating new vector store due to loading error...")
            self._create_vector_store()
    
    def _create_vector_store(self):
        """
        Create new FAISS vector store from medical knowledge base
        """
        try:
            # Get all documents from medical knowledge base
            documents = medical_knowledge.get_all_documents()
            
            if not documents:
                raise Exception("No documents found in medical knowledge base")
            
            logger.info(f"Creating vector store with {len(documents)} documents")
            
            # Create FAISS vector store
            self.vector_store = FAISS.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            
            # Save vector store
            self.vector_store.save_local(self.vector_store_path)
            
            logger.info("Vector store created and saved successfully")
            
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            raise Exception(f"Failed to create vector store: {str(e)}")
    
    def _initialize_bm25_retriever(self):
        """
        Initialize BM25 retriever for keyword-based search
        """
        try:
            # Try to load existing BM25 retriever
            if os.path.exists(self.bm25_path):
                logger.info("Loading existing BM25 retriever...")
                with open(self.bm25_path, 'rb') as f:
                    self.bm25_retriever = pickle.load(f)
            else:
                logger.info("Creating new BM25 retriever...")
                self._create_bm25_retriever()
            
            # Create ensemble retriever combining FAISS and BM25
            self._create_ensemble_retriever()
            
        except Exception as e:
            logger.warning(f"Error with BM25 retriever: {str(e)}")
            # Continue without BM25 if it fails
            logger.info("Continuing with FAISS-only retrieval")
    
    def _create_bm25_retriever(self):
        """
        Create new BM25 retriever from medical knowledge base
        """
        try:
            documents = medical_knowledge.get_all_documents()
            
            # Create BM25 retriever
            self.bm25_retriever = BM25Retriever.from_documents(documents)
            self.bm25_retriever.k = 5  # Return top 5 documents
            
            # Save BM25 retriever
            with open(self.bm25_path, 'wb') as f:
                pickle.dump(self.bm25_retriever, f)
            
            logger.info("BM25 retriever created and saved successfully")
            
        except Exception as e:
            logger.error(f"Error creating BM25 retriever: {str(e)}")
            self.bm25_retriever = None
    
    def _create_ensemble_retriever(self):
        """
        Create ensemble retriever combining FAISS and BM25
        """
        try:
            if self.vector_store and self.bm25_retriever:
                # Create FAISS retriever
                faiss_retriever = self.vector_store.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 5}
                )
                
                # Create ensemble retriever
                self.ensemble_retriever = EnsembleRetriever(
                    retrievers=[faiss_retriever, self.bm25_retriever],
                    weights=[0.6, 0.4]  # Favor semantic search over keyword search
                )
                
                logger.info("Ensemble retriever created successfully")
            
        except Exception as e:
            logger.warning(f"Error creating ensemble retriever: {str(e)}")
            self.ensemble_retriever = None
    
    def add_patient_documents(self, patient_documents: List[Document]):
        """
        Add patient medical record documents to the vector store
        
        Args:
            patient_documents (List[Document]): Patient medical record documents
        """
        try:
            if not patient_documents:
                logger.warning("No patient documents provided")
                return
            
            logger.info(f"Adding {len(patient_documents)} patient documents to vector store")
            
            # Add documents to existing vector store
            if self.vector_store:
                self.vector_store.add_documents(patient_documents)
            else:
                # Create vector store with patient documents
                self.vector_store = FAISS.from_documents(
                    documents=patient_documents,
                    embedding=self.embeddings
                )
            
            # Update BM25 retriever with new documents
            if self.bm25_retriever:
                # Recreate BM25 with all documents
                all_documents = medical_knowledge.get_all_documents() + patient_documents
                self.bm25_retriever = BM25Retriever.from_documents(all_documents)
                self.bm25_retriever.k = 5
                
                # Recreate ensemble retriever
                self._create_ensemble_retriever()
            
            logger.info("Patient documents added successfully")
            
        except Exception as e:
            logger.error(f"Error adding patient documents: {str(e)}")
            raise Exception(f"Failed to add patient documents: {str(e)}")
    
    def retrieve_relevant_documents(self, query: str, education_type: str, k: int = 10) -> List[Document]:
        """
        Retrieve relevant documents for a given query and education type
        
        Args:
            query (str): Search query
            education_type (str): Type of education material
            k (int): Number of documents to retrieve
            
        Returns:
            List[Document]: Retrieved relevant documents
        """
        try:
            logger.info(f"Retrieving documents for query: '{query}', type: {education_type}")
            
            # Enhance query with education type context
            enhanced_query = f"{query} {education_type} patient education medical guidance"
            
            retrieved_docs = []
            
            # Try ensemble retriever first (best performance)
            if self.ensemble_retriever:
                try:
                    retrieved_docs = self.ensemble_retriever.get_relevant_documents(enhanced_query)
                    logger.info(f"Retrieved {len(retrieved_docs)} documents using ensemble retriever")
                except Exception as e:
                    logger.warning(f"Ensemble retriever failed: {str(e)}")
            
            # Fallback to FAISS only
            if not retrieved_docs and self.vector_store:
                try:
                    retrieved_docs = self.vector_store.similarity_search(
                        enhanced_query, 
                        k=k,
                        filter=None  # Can add metadata filtering here
                    )
                    logger.info(f"Retrieved {len(retrieved_docs)} documents using FAISS")
                except Exception as e:
                    logger.warning(f"FAISS retriever failed: {str(e)}")
            
            # Get education type specific documents if no retrieval worked
            if not retrieved_docs:
                logger.info("Using fallback: education type specific documents")
                retrieved_docs = medical_knowledge.get_relevant_documents(education_type)
            
            # Limit results and add diversity
            retrieved_docs = self._diversify_results(retrieved_docs, k)
            
            logger.info(f"Final retrieval: {len(retrieved_docs)} documents")
            return retrieved_docs
            
        except Exception as e:
            logger.error(f"Error in document retrieval: {str(e)}")
            # Return education type specific documents as last resort
            return medical_knowledge.get_relevant_documents(education_type)[:k]
    
    def _diversify_results(self, documents: List[Document], k: int) -> List[Document]:
        """
        Ensure diversity in retrieved documents by category and content
        
        Args:
            documents (List[Document]): Retrieved documents
            k (int): Maximum number of documents to return
            
        Returns:
            List[Document]: Diversified document list
        """
        if len(documents) <= k:
            return documents
        
        # Group by category to ensure diversity
        category_groups = {}
        for doc in documents:
            category = doc.metadata.get('category', 'unknown')
            if category not in category_groups:
                category_groups[category] = []
            category_groups[category].append(doc)
        
        # Select documents from different categories
        diversified = []
        max_per_category = max(1, k // len(category_groups))
        
        for category, docs in category_groups.items():
            diversified.extend(docs[:max_per_category])
            if len(diversified) >= k:
                break
        
        return diversified[:k]
    
    def get_context_for_generation(self, patient_info: dict, education_type: str) -> str:
        """
        Get context string for content generation
        
        Args:
            patient_info (dict): Extracted patient information
            education_type (str): Type of education material
            
        Returns:
            str: Context string for LLM generation
        """
        try:
            # Create query from patient information
            query_parts = []
            
            if patient_info.get('conditions'):
                query_parts.append(" ".join(patient_info['conditions']))
            
            if patient_info.get('procedures'):
                query_parts.append(" ".join(patient_info['procedures']))
            
            if patient_info.get('medications'):
                query_parts.append(" ".join(patient_info['medications']))
            
            query = " ".join(query_parts) if query_parts else education_type
            
            # Retrieve relevant documents
            relevant_docs = self.retrieve_relevant_documents(query, education_type)
            
            # Create context string
            context_parts = [
                f"Patient Information: {patient_info}",
                f"Education Type: {education_type}",
                "Relevant Medical Guidelines:"
            ]
            
            for i, doc in enumerate(relevant_docs, 1):
                context_parts.append(f"\n{i}. {doc.page_content}")
            
            context = "\n".join(context_parts)
            
            logger.info(f"Generated context with {len(relevant_docs)} documents")
            return context
            
        except Exception as e:
            logger.error(f"Error generating context: {str(e)}")
            return f"Patient Information: {patient_info}\nEducation Type: {education_type}"

# Global RAG system instance
rag_system = RAGSystem()
