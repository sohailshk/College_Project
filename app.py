"""
Main Flask application for Patient Education Material Generator
This is the entry point of the web application that generates personalized
patient education materials using Gemini AI and RAG.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import json
from werkzeug.utils import secure_filename
import logging
from datetime import datetime

# Import our custom utilities
from utils.pdf_processor import process_patient_pdf
from utils.rag_system import rag_system
from utils.gemini_generator import gemini_generator
from config import Config

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Allowed file extensions for PDF uploads
ALLOWED_EXTENSIONS = {'pdf'}

# Set up logging
os.makedirs('logs', exist_ok=True)  # Create logs directory first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    """
    Check if uploaded file has allowed extension
    Args:
        filename (str): Name of the uploaded file
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """
    Home page route - displays the main upload form
    Returns:
        Rendered HTML template for the home page
    """
    logger.info("User accessed home page")
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and process patient medical records
    Returns:
        JSON response with processing results or error message
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            logger.warning("No file uploaded")
            return jsonify({'error': 'No file selected'}), 400
        
        file = request.files['file']
        education_type = request.form.get('education_type')
        
        # Validate inputs
        if file.filename == '':
            logger.warning("Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        if not education_type:
            logger.warning("No education type selected")
            return jsonify({'error': 'Please select education material type'}), 400
        
        # Check file extension
        if file and allowed_file(file.filename):
            # Create uploads directory if it doesn't exist
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # Save uploaded file securely
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            logger.info(f"File uploaded successfully: {filename}")
            logger.info(f"Education type selected: {education_type}")
            
            # Process the PDF and extract medical information
            try:
                logger.info("Processing PDF and extracting medical information...")
                patient_documents, medical_info = process_patient_pdf(filepath)
                
                # Add patient documents to RAG system
                logger.info("Adding patient documents to RAG system...")
                rag_system.add_patient_documents(patient_documents)
                
                # Get relevant context for generation
                logger.info("Retrieving relevant medical context...")
                medical_context = rag_system.get_context_for_generation(medical_info, education_type)
                
                # Generate personalized education material
                logger.info("Generating personalized education material...")
                education_material = gemini_generator.generate_education_material(
                    patient_info=medical_info,
                    medical_context=medical_context,
                    education_type=education_type
                )
                
                # Store results in session for display
                session['education_material'] = education_material
                session['patient_info'] = medical_info
                session['filename'] = filename
                session['education_type'] = education_type
                session['generation_time'] = datetime.now().isoformat()
                
                logger.info("Education material generated successfully")
                
                # Clean up uploaded file
                try:
                    os.remove(filepath)
                    logger.info(f"Cleaned up uploaded file: {filename}")
                except:
                    logger.warning(f"Could not remove uploaded file: {filename}")
                
                return jsonify({
                    'success': True, 
                    'message': 'Education material generated successfully!',
                    'redirect_url': '/results'
                })
                
            except Exception as processing_error:
                logger.error(f"Error processing PDF: {str(processing_error)}")
                
                # Clean up uploaded file on error
                try:
                    os.remove(filepath)
                except:
                    pass
                
                return jsonify({
                    'error': f'Error processing your medical records: {str(processing_error)}'
                }), 500
        
        else:
            logger.warning(f"Invalid file type: {file.filename}")
            return jsonify({'error': 'Only PDF files are allowed'}), 400
            
    except Exception as e:
        logger.error(f"Error in file upload: {str(e)}")
        return jsonify({'error': 'An error occurred during upload'}), 500

@app.route('/results')
def results():
    """
    Display generated education materials
    Returns:
        Rendered HTML template with education materials
    """
    try:
        # Get education material from session
        education_material = session.get('education_material')
        patient_info = session.get('patient_info')
        filename = session.get('filename')
        education_type = session.get('education_type')
        generation_time = session.get('generation_time')
        
        if not education_material:
            logger.warning("No education material found in session")
            return redirect(url_for('index'))
        
        logger.info("Displaying education material results")
        
        return render_template('results.html', 
                             education_material=education_material,
                             patient_info=patient_info,
                             filename=filename,
                             education_type=education_type,
                             generation_time=generation_time)
        
    except Exception as e:
        logger.error(f"Error displaying results: {str(e)}")
        return redirect(url_for('index'))

@app.route('/download')
def download_results():
    """
    Download education materials as JSON
    Returns:
        JSON file download
    """
    try:
        education_material = session.get('education_material')
        
        if not education_material:
            return jsonify({'error': 'No education material available'}), 404
        
        # Add download metadata
        education_material['download_info'] = {
            'downloaded_at': datetime.now().isoformat(),
            'filename': session.get('filename'),
            'education_type': session.get('education_type')
        }
        
        return jsonify(education_material)
        
    except Exception as e:
        logger.error(f"Error downloading results: {str(e)}")
        return jsonify({'error': 'Download failed'}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Initialize RAG system and medical knowledge base
    logger.info("Initializing RAG system and medical knowledge base...")
    try:
        # RAG system initialization is handled in the module import
        logger.info("RAG system initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing RAG system: {str(e)}")
        logger.warning("Continuing without RAG system - using fallback mode")
    
    # Run the Flask app in debug mode
    logger.info("Starting Patient Education Material Generator")
    app.run(debug=True, host='0.0.0.0', port=5000)
