"""
PDF Processing utilities for extracting text from medical records
Uses PyPDF2 and LangChain document loaders for efficient text extraction
"""

import os
import logging
from typing import List, Optional
from PyPDF2 import PdfReader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# Set up logging
logger = logging.getLogger(__name__)

class PDFProcessor:
    """
    Handles PDF text extraction and document processing for medical records
    """
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize PDF processor with text chunking parameters
        
        Args:
            chunk_size (int): Size of text chunks for processing
            chunk_overlap (int): Overlap between chunks to maintain context
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize text splitter for breaking documents into manageable chunks
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]  # Split on paragraphs, then lines, then words
        )
        
        logger.info(f"PDFProcessor initialized with chunk_size={chunk_size}, overlap={chunk_overlap}")
    
    def extract_text_pypdf2(self, pdf_path: str) -> str:
        """
        Extract text from PDF using PyPDF2 (fallback method)
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text content
            
        Raises:
            Exception: If PDF cannot be read or processed
        """
        try:
            logger.info(f"Extracting text from PDF: {pdf_path}")
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                text_content = ""
                
                # Extract text from each page
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text.strip():  # Only add non-empty pages
                            text_content += f"\n--- Page {page_num + 1} ---\n"
                            text_content += page_text + "\n"
                    except Exception as e:
                        logger.warning(f"Could not extract text from page {page_num + 1}: {str(e)}")
                        continue
                
                logger.info(f"Successfully extracted {len(text_content)} characters from {len(pdf_reader.pages)} pages")
                return text_content.strip()
                
        except Exception as e:
            logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def extract_text_langchain(self, pdf_path: str) -> List[Document]:
        """
        Extract text from PDF using LangChain PyPDFLoader (primary method)
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            List[Document]: List of LangChain Document objects with metadata
            
        Raises:
            Exception: If PDF cannot be loaded or processed
        """
        try:
            logger.info(f"Loading PDF with LangChain: {pdf_path}")
            
            # Use LangChain's PyPDFLoader for better text extraction
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            
            logger.info(f"Successfully loaded {len(documents)} pages using LangChain")
            
            # Add metadata to documents
            for i, doc in enumerate(documents):
                doc.metadata.update({
                    'source_file': os.path.basename(pdf_path),
                    'page_number': i + 1,
                    'total_pages': len(documents),
                    'document_type': 'medical_record'
                })
            
            return documents
            
        except Exception as e:
            logger.error(f"Error loading PDF with LangChain {pdf_path}: {str(e)}")
            raise Exception(f"Failed to load PDF with LangChain: {str(e)}")
    
    def process_pdf(self, pdf_path: str) -> List[Document]:
        """
        Main method to process PDF - extract text and split into chunks
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            List[Document]: List of processed document chunks ready for RAG
            
        Raises:
            Exception: If PDF processing fails
        """
        try:
            # Validate file exists
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
            logger.info(f"Processing PDF: {pdf_path}")
            
            # Try LangChain method first (better for structured documents)
            try:
                documents = self.extract_text_langchain(pdf_path)
                
                # Split documents into smaller chunks for better RAG performance
                all_chunks = []
                for doc in documents:
                    chunks = self.text_splitter.split_documents([doc])
                    all_chunks.extend(chunks)
                
                logger.info(f"Split into {len(all_chunks)} chunks for RAG processing")
                return all_chunks
                
            except Exception as e:
                logger.warning(f"LangChain method failed, trying PyPDF2 fallback: {str(e)}")
                
                # Fallback to PyPDF2 method
                text_content = self.extract_text_pypdf2(pdf_path)
                
                # Create a single document and split it
                document = Document(
                    page_content=text_content,
                    metadata={
                        'source_file': os.path.basename(pdf_path),
                        'document_type': 'medical_record',
                        'extraction_method': 'pypdf2_fallback'
                    }
                )
                
                chunks = self.text_splitter.split_documents([document])
                logger.info(f"Fallback method: Split into {len(chunks)} chunks")
                return chunks
                
        except Exception as e:
            logger.error(f"Failed to process PDF {pdf_path}: {str(e)}")
            raise Exception(f"PDF processing failed: {str(e)}")
    
    def extract_medical_info(self, documents: List[Document]) -> dict:
        """
        Extract key medical information from processed documents
        
        Args:
            documents (List[Document]): Processed document chunks
            
        Returns:
            dict: Extracted medical information categorized by type
        """
        try:
            logger.info("Extracting medical information from documents")
            
            # Combine all document content for analysis
            full_text = " ".join([doc.page_content for doc in documents]).lower()
            
            medical_info = {
                'conditions': [],
                'medications': [],
                'procedures': [],
                'symptoms': [],
                'demographics': {},
                'raw_text_length': len(full_text)
            }
            
            # Simple keyword-based extraction (can be enhanced with NLP)
            # Medical conditions keywords
            condition_keywords = ['diabetes', 'hypertension', 'surgery', 'operation', 'procedure', 
                                'diagnosis', 'condition', 'disease', 'disorder', 'syndrome']
            
            # Medication keywords
            medication_keywords = ['medication', 'drug', 'prescription', 'pill', 'tablet', 
                                 'capsule', 'dosage', 'mg', 'ml', 'treatment']
            
            # Procedure keywords
            procedure_keywords = ['surgery', 'operation', 'procedure', 'treatment', 'therapy',
                                'intervention', 'examination', 'test', 'scan', 'biopsy']
            
            # Extract information based on keywords (basic implementation)
            for keyword in condition_keywords:
                if keyword in full_text:
                    medical_info['conditions'].append(keyword)
            
            for keyword in medication_keywords:
                if keyword in full_text:
                    medical_info['medications'].append(keyword)
            
            for keyword in procedure_keywords:
                if keyword in full_text:
                    medical_info['procedures'].append(keyword)
            
            # Remove duplicates
            medical_info['conditions'] = list(set(medical_info['conditions']))
            medical_info['medications'] = list(set(medical_info['medications']))
            medical_info['procedures'] = list(set(medical_info['procedures']))
            
            logger.info(f"Extracted medical info: {len(medical_info['conditions'])} conditions, "
                       f"{len(medical_info['medications'])} medications, "
                       f"{len(medical_info['procedures'])} procedures")
            
            return medical_info
            
        except Exception as e:
            logger.error(f"Error extracting medical information: {str(e)}")
            return {
                'conditions': [],
                'medications': [],
                'procedures': [],
                'symptoms': [],
                'demographics': {},
                'error': str(e)
            }

# Utility function for easy access
def process_patient_pdf(pdf_path: str, chunk_size: int = 500) -> tuple:
    """
    Utility function to process a patient PDF and extract medical information
    
    Args:
        pdf_path (str): Path to the patient PDF file
        chunk_size (int): Size of text chunks for processing
        
    Returns:
        tuple: (processed_documents, medical_info)
    """
    processor = PDFProcessor(chunk_size=chunk_size)
    documents = processor.process_pdf(pdf_path)
    medical_info = processor.extract_medical_info(documents)
    
    return documents, medical_info
