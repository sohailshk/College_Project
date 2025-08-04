"""
Gemini AI integration for generating personalized patient education materials
Uses LangChain with Google's Gemini API for content generation
"""

import logging
import json
from typing import Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser
from config import Config

# Set up logging
logger = logging.getLogger(__name__)

class PatientEducationOutputParser(BaseOutputParser):
    """
    Custom output parser for structured patient education materials
    """
    
    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parse LLM output into structured format
        
        Args:
            text (str): Raw LLM output
            
        Returns:
            Dict[str, Any]: Structured patient education material
        """
        try:
            # Try to extract structured content
            sections = {
                'title': '',
                'overview': '',
                'instructions': [],
                'important_notes': [],
                'warning_signs': [],
                'when_to_call_doctor': [],
                'additional_resources': []
            }
            
            # Split text into lines for processing
            lines = text.strip().split('\n')
            current_section = 'overview'
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check for section headers
                line_lower = line.lower()
                if any(keyword in line_lower for keyword in ['title', 'heading']):
                    sections['title'] = line.replace('Title:', '').replace('Heading:', '').strip()
                elif any(keyword in line_lower for keyword in ['overview', 'introduction', 'summary']):
                    current_section = 'overview'
                elif any(keyword in line_lower for keyword in ['instruction', 'step', 'guideline']):
                    current_section = 'instructions'
                elif any(keyword in line_lower for keyword in ['important', 'note', 'remember']):
                    current_section = 'important_notes'
                elif any(keyword in line_lower for keyword in ['warning', 'alert', 'danger']):
                    current_section = 'warning_signs'
                elif any(keyword in line_lower for keyword in ['call', 'contact', 'doctor', 'emergency']):
                    current_section = 'when_to_call_doctor'
                elif any(keyword in line_lower for keyword in ['resource', 'reference', 'link']):
                    current_section = 'additional_resources'
                else:
                    # Add content to current section
                    if current_section == 'overview':
                        sections['overview'] += line + ' '
                    else:
                        # Remove bullet points and numbers
                        clean_line = line.lstrip('•-*123456789. ').strip()
                        if clean_line:
                            sections[current_section].append(clean_line)
            
            # Clean up overview
            sections['overview'] = sections['overview'].strip()
            
            return sections
            
        except Exception as e:
            logger.warning(f"Error parsing output: {str(e)}")
            # Return raw text if parsing fails
            return {
                'title': 'Patient Education Material',
                'overview': text,
                'instructions': [],
                'important_notes': [],
                'warning_signs': [],
                'when_to_call_doctor': [],
                'additional_resources': []
            }

class GeminiEducationGenerator:
    """
    Generates personalized patient education materials using Google's Gemini API
    """
    
    def __init__(self):
        """
        Initialize Gemini education generator with API configuration
        """
        self.api_key = Config.GEMINI_API_KEY
        self.model_name = Config.GEMINI_MODEL
        
        # Initialize Gemini LLM
        self._initialize_llm()
        
        # Initialize prompts for different education types
        self._initialize_prompts()
        
        # Initialize output parser
        self.output_parser = PatientEducationOutputParser()
        
        logger.info("Gemini education generator initialized successfully")
    
    def _initialize_llm(self):
        """
        Initialize Google Gemini LLM with configuration
        """
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=self.model_name,
                google_api_key=self.api_key,
                temperature=0.3,  # Lower temperature for more factual, consistent output
                max_tokens=2048,  # Adequate for education materials
                top_p=0.8,       # Focus on most likely tokens
                top_k=40         # Consider top 40 tokens
            )
            
            logger.info(f"Gemini LLM initialized: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Error initializing Gemini LLM: {str(e)}")
            raise Exception(f"Failed to initialize Gemini LLM: {str(e)}")
    
    def _initialize_prompts(self):
        """
        Initialize prompt templates for different education material types
        """
        # Base prompt template
        base_prompt = """
You are a medical education specialist creating personalized patient education materials. 
Create clear, easy-to-understand, and actionable content based on the patient's medical information.

Patient Information:
{patient_info}

Medical Context:
{medical_context}

Education Type: {education_type}

Instructions:
1. Use simple, non-medical language that patients can easily understand
2. Provide specific, actionable steps and instructions
3. Include important safety information and warning signs
4. Personalize the content based on the patient's specific medical situation
5. Organize information in a clear, logical structure
6. Include when to contact healthcare providers

Generate a comprehensive patient education material with the following sections:
- Title: A clear, descriptive title
- Overview: Brief explanation of the condition/situation
- Step-by-step Instructions: Detailed, numbered instructions
- Important Notes: Key things to remember
- Warning Signs: Symptoms that require immediate attention
- When to Call Your Doctor: Specific situations requiring medical contact
- Additional Resources: Helpful tips and information

Make sure the content is:
- Medically accurate based on the provided context
- Easy to read and understand
- Specific to the patient's situation
- Actionable and practical
- Encouraging and supportive in tone
"""
        
        # Specific prompts for each education type
        self.prompts = {
            'post_operative': PromptTemplate(
                input_variables=['patient_info', 'medical_context', 'education_type'],
                template=base_prompt + """

Focus specifically on post-operative care including:
- Wound care and healing
- Pain management strategies
- Activity restrictions and gradual return to normal activities
- Medication management
- Signs of complications
- Follow-up care requirements
"""
            ),
            
            'medication_guide': PromptTemplate(
                input_variables=['patient_info', 'medical_context', 'education_type'],
                template=base_prompt + """

Focus specifically on medication guidance including:
- How to take medications correctly
- Timing and dosage instructions
- What to do if a dose is missed
- Potential side effects and how to manage them
- Drug interactions and precautions
- Storage and handling of medications
- When to refill prescriptions
"""
            ),
            
            'diet_plan': PromptTemplate(
                input_variables=['patient_info', 'medical_context', 'education_type'],
                template=base_prompt + """

Focus specifically on dietary guidance including:
- Recommended foods and nutrients
- Foods to avoid or limit
- Meal planning and preparation tips
- Hydration recommendations
- Special dietary considerations for the medical condition
- How diet supports healing and recovery
- Sample meal ideas and recipes
"""
            )
        }
        
        logger.info("Prompt templates initialized for all education types")
    
    def generate_education_material(self, patient_info: Dict[str, Any], 
                                  medical_context: str, 
                                  education_type: str) -> Dict[str, Any]:
        """
        Generate personalized patient education material
        
        Args:
            patient_info (Dict[str, Any]): Extracted patient information
            medical_context (str): Relevant medical context from RAG
            education_type (str): Type of education material to generate
            
        Returns:
            Dict[str, Any]: Generated education material in structured format
        """
        try:
            logger.info(f"Generating {education_type} education material")
            
            # Get appropriate prompt template
            prompt_template = self.prompts.get(education_type, self.prompts['post_operative'])
            
            # Create LLM chain
            chain = LLMChain(llm=self.llm, prompt=prompt_template)
            
            # Prepare input data
            input_data = {
                'patient_info': self._format_patient_info(patient_info),
                'medical_context': medical_context,
                'education_type': education_type.replace('_', ' ').title()
            }
            
            # Generate content
            logger.info("Calling Gemini API for content generation...")
            response = chain.run(input_data)
            
            # Parse and structure the output
            structured_output = self.output_parser.parse(response)
            
            # Add metadata
            structured_output['metadata'] = {
                'education_type': education_type,
                'generated_by': 'Gemini AI',
                'model': self.model_name,
                'patient_conditions': patient_info.get('conditions', []),
                'patient_medications': patient_info.get('medications', []),
                'patient_procedures': patient_info.get('procedures', [])
            }
            
            logger.info("Education material generated successfully")
            return structured_output
            
        except Exception as e:
            logger.error(f"Error generating education material: {str(e)}")
            
            # Return fallback content
            return self._generate_fallback_content(education_type, patient_info)
    
    def _format_patient_info(self, patient_info: Dict[str, Any]) -> str:
        """
        Format patient information for prompt input
        
        Args:
            patient_info (Dict[str, Any]): Patient information dictionary
            
        Returns:
            str: Formatted patient information string
        """
        formatted_parts = []
        
        if patient_info.get('conditions'):
            formatted_parts.append(f"Medical Conditions: {', '.join(patient_info['conditions'])}")
        
        if patient_info.get('medications'):
            formatted_parts.append(f"Current Medications: {', '.join(patient_info['medications'])}")
        
        if patient_info.get('procedures'):
            formatted_parts.append(f"Recent Procedures: {', '.join(patient_info['procedures'])}")
        
        if patient_info.get('symptoms'):
            formatted_parts.append(f"Reported Symptoms: {', '.join(patient_info['symptoms'])}")
        
        return '\n'.join(formatted_parts) if formatted_parts else "No specific medical information provided"
    
    def _generate_fallback_content(self, education_type: str, patient_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate fallback content when API fails
        
        Args:
            education_type (str): Type of education material
            patient_info (Dict[str, Any]): Patient information
            
        Returns:
            Dict[str, Any]: Fallback education material
        """
        fallback_content = {
            'post_operative': {
                'title': 'Post-Operative Care Instructions',
                'overview': 'These instructions will help you recover safely after your procedure.',
                'instructions': [
                    'Keep your surgical site clean and dry',
                    'Take prescribed medications as directed',
                    'Follow activity restrictions provided by your surgeon',
                    'Attend all follow-up appointments'
                ],
                'important_notes': [
                    'Rest is important for healing',
                    'Gradually increase activity as tolerated',
                    'Stay hydrated and eat nutritious foods'
                ],
                'warning_signs': [
                    'Increased pain, redness, or swelling at surgical site',
                    'Fever over 101.3°F (38.5°C)',
                    'Unusual drainage from incision'
                ],
                'when_to_call_doctor': [
                    'If you experience any warning signs',
                    'If pain is not controlled with prescribed medication',
                    'If you have questions about your recovery'
                ]
            },
            'medication_guide': {
                'title': 'Medication Guide',
                'overview': 'This guide will help you take your medications safely and effectively.',
                'instructions': [
                    'Take medications exactly as prescribed',
                    'Set up a regular schedule for taking medications',
                    'Use a pill organizer to avoid missed doses',
                    'Keep medications in original containers'
                ],
                'important_notes': [
                    'Never share medications with others',
                    'Check expiration dates regularly',
                    'Store medications in a cool, dry place'
                ],
                'warning_signs': [
                    'Allergic reactions (rash, difficulty breathing)',
                    'Severe side effects',
                    'Signs of medication overdose'
                ],
                'when_to_call_doctor': [
                    'If you experience side effects',
                    'If you miss multiple doses',
                    'Before stopping any medication'
                ]
            },
            'diet_plan': {
                'title': 'Nutritional Guidelines',
                'overview': 'These dietary recommendations will support your health and recovery.',
                'instructions': [
                    'Eat a balanced diet with fruits and vegetables',
                    'Stay hydrated with plenty of water',
                    'Choose lean proteins for healing',
                    'Limit processed foods and added sugars'
                ],
                'important_notes': [
                    'Small, frequent meals may be easier to digest',
                    'Include foods rich in vitamins and minerals',
                    'Follow any specific dietary restrictions'
                ],
                'warning_signs': [
                    'Persistent nausea or vomiting',
                    'Significant weight loss',
                    'Signs of dehydration'
                ],
                'when_to_call_doctor': [
                    'If you cannot keep food or fluids down',
                    'If you have questions about your diet',
                    'If you experience digestive problems'
                ]
            }
        }
        
        content = fallback_content.get(education_type, fallback_content['post_operative'])
        content['additional_resources'] = ['Contact your healthcare provider for personalized advice']
        content['metadata'] = {
            'education_type': education_type,
            'generated_by': 'Fallback System',
            'note': 'This is general information. Please consult your healthcare provider for personalized advice.'
        }
        
        logger.info(f"Generated fallback content for {education_type}")
        return content

# Global generator instance
gemini_generator = GeminiEducationGenerator()
