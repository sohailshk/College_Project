"""
Medical Knowledge Base for RAG system
Contains curated medical information for generating patient education materials
"""

import os
import json
import logging
from typing import List, Dict, Any
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Set up logging
logger = logging.getLogger(__name__)

class MedicalKnowledgeBase:
    """
    Manages medical knowledge base for RAG system
    Contains curated medical information for patient education
    """
    
    def __init__(self):
        """
        Initialize medical knowledge base with curated content
        """
        self.knowledge_base = {}
        self.documents = []
        
        # Initialize text splitter for knowledge base content
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,  # Smaller chunks for knowledge base
            chunk_overlap=30,
            separators=["\n\n", "\n", ". ", " "]
        )
        
        # Load medical knowledge
        self._initialize_knowledge_base()
        self._create_documents()
        
        logger.info(f"Medical knowledge base initialized with {len(self.documents)} documents")
    
    def _initialize_knowledge_base(self):
        """
        Initialize the medical knowledge base with curated content
        """
        self.knowledge_base = {
            "post_operative_care": {
                "general_instructions": [
                    "Keep the surgical site clean and dry to prevent infection.",
                    "Follow prescribed medication schedule exactly as directed by your healthcare provider.",
                    "Gradually increase activity levels as recommended by your surgical team.",
                    "Watch for signs of infection including increased redness, swelling, warmth, or discharge.",
                    "Attend all follow-up appointments to monitor healing progress.",
                    "Avoid lifting heavy objects or strenuous activities until cleared by your doctor.",
                    "Get adequate rest and sleep to support the healing process.",
                    "Stay hydrated by drinking plenty of water throughout the day.",
                    "Eat a balanced diet rich in protein and vitamins to promote healing.",
                    "Contact your healthcare provider immediately if you experience severe pain, fever, or unusual symptoms."
                ],
                "wound_care": [
                    "Gently clean the incision site with soap and water as instructed.",
                    "Pat the area dry with a clean towel - do not rub or scrub.",
                    "Apply prescribed ointments or dressings as directed by your healthcare team.",
                    "Change dressings regularly or when they become wet or soiled.",
                    "Keep the incision covered until your doctor says it's okay to leave it open.",
                    "Avoid soaking in baths, pools, or hot tubs until the incision is fully healed.",
                    "Watch for signs of healing including decreased swelling and pain over time.",
                    "Report any unusual drainage, increasing pain, or signs of infection immediately."
                ],
                "pain_management": [
                    "Take prescribed pain medications as directed - do not skip doses.",
                    "Use ice packs for 15-20 minutes at a time to reduce swelling and pain.",
                    "Apply heat therapy only if recommended by your healthcare provider.",
                    "Practice deep breathing exercises and relaxation techniques.",
                    "Maintain comfortable positioning and use pillows for support.",
                    "Gradually reduce pain medication as discomfort decreases.",
                    "Never exceed the recommended dosage of pain medications.",
                    "Contact your doctor if pain is not controlled with prescribed medications."
                ]
            },
            
            "medication_guidance": {
                "general_principles": [
                    "Always take medications exactly as prescribed by your healthcare provider.",
                    "Never share your medications with others or take someone else's medications.",
                    "Store medications in a cool, dry place away from direct sunlight.",
                    "Keep medications in their original containers with labels intact.",
                    "Check expiration dates regularly and dispose of expired medications safely.",
                    "Set up a medication schedule or use pill organizers to avoid missed doses.",
                    "Never stop taking prescribed medications without consulting your doctor first.",
                    "Keep an updated list of all medications including vitamins and supplements.",
                    "Inform all healthcare providers about all medications you are taking.",
                    "Report any side effects or allergic reactions to your healthcare provider immediately."
                ],
                "dosage_instructions": [
                    "Take medications at the same time each day to maintain consistent levels.",
                    "If you miss a dose, take it as soon as you remember unless it's almost time for the next dose.",
                    "Never double up on doses to make up for a missed dose.",
                    "Some medications should be taken with food, others on an empty stomach - follow specific instructions.",
                    "Use the measuring device provided with liquid medications for accurate dosing.",
                    "Do not crush, chew, or break extended-release tablets unless specifically instructed.",
                    "Complete the full course of antibiotics even if you feel better.",
                    "Contact your pharmacist or doctor if you have questions about dosing."
                ],
                "side_effects": [
                    "Common side effects may include nausea, dizziness, drowsiness, or mild stomach upset.",
                    "Most side effects are temporary and will improve as your body adjusts to the medication.",
                    "Serious side effects requiring immediate medical attention include difficulty breathing, chest pain, or severe allergic reactions.",
                    "Keep a diary of any side effects you experience and discuss them with your healthcare provider.",
                    "Some medications may interact with alcohol - follow your doctor's advice about alcohol consumption.",
                    "Certain medications may make you more sensitive to sunlight - use appropriate sun protection.",
                    "Birth control effectiveness may be reduced by some medications - discuss with your doctor.",
                    "Report persistent or worsening side effects to your healthcare provider promptly."
                ]
            },
            
            "diet_and_nutrition": {
                "general_nutrition": [
                    "Eat a balanced diet including fruits, vegetables, lean proteins, and whole grains.",
                    "Stay hydrated by drinking 8-10 glasses of water daily unless restricted by your doctor.",
                    "Limit processed foods, excessive sugar, and high-sodium foods.",
                    "Eat smaller, more frequent meals if you have digestive issues.",
                    "Include foods rich in vitamins C and D, zinc, and protein to support healing.",
                    "Choose lean proteins such as fish, poultry, beans, and tofu.",
                    "Incorporate colorful fruits and vegetables for essential vitamins and antioxidants.",
                    "Limit alcohol consumption as it can interfere with healing and medications.",
                    "Avoid smoking and tobacco products which impair healing.",
                    "Consult with a registered dietitian for personalized nutrition advice."
                ],
                "post_surgery_diet": [
                    "Start with clear liquids and gradually progress to solid foods as tolerated.",
                    "Eat soft, easy-to-digest foods initially to avoid digestive stress.",
                    "Increase fiber intake gradually to prevent constipation from pain medications.",
                    "Include probiotic-rich foods like yogurt to support digestive health.",
                    "Avoid spicy, fatty, or heavily seasoned foods that may cause nausea.",
                    "Eat protein-rich foods to support tissue repair and healing.",
                    "Take vitamin and mineral supplements if recommended by your healthcare provider.",
                    "Monitor your appetite and report significant changes to your doctor."
                ],
                "dietary_restrictions": [
                    "Follow any specific dietary restrictions provided by your healthcare team.",
                    "Read food labels carefully if you have allergies or dietary limitations.",
                    "Avoid foods that may interact with your medications.",
                    "Limit caffeine intake if it interferes with sleep or causes anxiety.",
                    "Choose low-sodium options if you have heart or kidney conditions.",
                    "Monitor blood sugar levels if you have diabetes and adjust diet accordingly.",
                    "Avoid alcohol if taking certain medications or if you have liver conditions.",
                    "Consult your healthcare provider before making significant dietary changes."
                ]
            },
            
            "warning_signs": {
                "emergency_symptoms": [
                    "Severe chest pain or pressure that doesn't improve with rest.",
                    "Difficulty breathing or shortness of breath that's getting worse.",
                    "Signs of severe allergic reaction including facial swelling, hives, or difficulty swallowing.",
                    "Severe bleeding that won't stop with direct pressure.",
                    "Signs of stroke including sudden weakness, confusion, or difficulty speaking.",
                    "Severe abdominal pain with vomiting or inability to keep fluids down.",
                    "High fever (over 101.3°F) with chills or rapid heart rate.",
                    "Sudden severe headache unlike any you've experienced before.",
                    "Loss of consciousness or severe confusion.",
                    "Any symptoms that seem life-threatening or are rapidly worsening."
                ],
                "infection_signs": [
                    "Increasing redness, warmth, or swelling around an incision or wound.",
                    "Pus or unusual discharge from a surgical site.",
                    "Red streaks extending from a wound or infection site.",
                    "Fever over 100.4°F (38°C) or chills.",
                    "Increasing pain rather than gradual improvement.",
                    "Foul-smelling drainage from wounds or surgical sites.",
                    "Delayed healing or wounds that aren't improving as expected.",
                    "Swollen lymph nodes near the affected area."
                ]
            }
        }
    
    def _create_documents(self):
        """
        Convert knowledge base content into LangChain documents for RAG
        """
        self.documents = []
        
        for category, subcategories in self.knowledge_base.items():
            for subcategory, content_list in subcategories.items():
                # Create a document for each subcategory
                content = "\n".join(content_list)
                
                document = Document(
                    page_content=content,
                    metadata={
                        'source': 'medical_knowledge_base',
                        'category': category,
                        'subcategory': subcategory,
                        'document_type': 'medical_knowledge',
                        'content_type': 'educational_material'
                    }
                )
                
                # Split into smaller chunks for better retrieval
                chunks = self.text_splitter.split_documents([document])
                self.documents.extend(chunks)
    
    def get_relevant_documents(self, education_type: str) -> List[Document]:
        """
        Get documents relevant to specific education type
        
        Args:
            education_type (str): Type of education material needed
            
        Returns:
            List[Document]: Relevant documents for the education type
        """
        education_mapping = {
            'post_operative': ['post_operative_care', 'warning_signs'],
            'medication_guide': ['medication_guidance', 'warning_signs'],
            'diet_plan': ['diet_and_nutrition', 'warning_signs']
        }
        
        relevant_categories = education_mapping.get(education_type, [])
        
        relevant_docs = []
        for doc in self.documents:
            if doc.metadata.get('category') in relevant_categories:
                relevant_docs.append(doc)
        
        logger.info(f"Found {len(relevant_docs)} relevant documents for {education_type}")
        return relevant_docs
    
    def get_all_documents(self) -> List[Document]:
        """
        Get all documents in the knowledge base
        
        Returns:
            List[Document]: All documents in the knowledge base
        """
        return self.documents
    
    def add_custom_knowledge(self, category: str, subcategory: str, content: List[str]):
        """
        Add custom knowledge to the knowledge base
        
        Args:
            category (str): Main category for the knowledge
            subcategory (str): Subcategory for organization
            content (List[str]): List of knowledge items to add
        """
        if category not in self.knowledge_base:
            self.knowledge_base[category] = {}
        
        self.knowledge_base[category][subcategory] = content
        
        # Recreate documents to include new knowledge
        self._create_documents()
        
        logger.info(f"Added custom knowledge: {category}.{subcategory} with {len(content)} items")
    
    def search_knowledge(self, query: str) -> List[Document]:
        """
        Search knowledge base for specific query
        
        Args:
            query (str): Search query
            
        Returns:
            List[Document]: Documents containing relevant information
        """
        query_lower = query.lower()
        matching_docs = []
        
        for doc in self.documents:
            if query_lower in doc.page_content.lower():
                matching_docs.append(doc)
        
        logger.info(f"Found {len(matching_docs)} documents matching query: {query}")
        return matching_docs

# Global instance for easy access
medical_knowledge = MedicalKnowledgeBase()
