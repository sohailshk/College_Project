"""
Create sample medical PDF documents for testing the system
Generates mock patient medical records in PDF format
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

def create_sample_pdfs():
    """
    Create sample medical PDF documents for testing
    """
    
    # Create sample data directory
    os.makedirs('sample_data', exist_ok=True)
    
    # Sample 1: Post-operative care
    create_post_operative_pdf()
    
    # Sample 2: Medication management
    create_medication_pdf()
    
    # Sample 3: Diet plan
    create_diet_plan_pdf()
    
    print("Sample PDF documents created in 'sample_data' directory")

def create_post_operative_pdf():
    """
    Create a sample post-operative medical record
    """
    filename = 'sample_data/post_operative_record.pdf'
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        textColor=colors.blue
    )
    
    # Build content
    story = []
    
    # Title
    story.append(Paragraph("MEDICAL RECORD - POST-OPERATIVE CARE", title_style))
    story.append(Spacer(1, 12))
    
    # Patient Information
    story.append(Paragraph("PATIENT INFORMATION", styles['Heading2']))
    patient_data = [
        ['Patient Name:', 'John Smith'],
        ['Date of Birth:', 'January 15, 1975'],
        ['Medical Record #:', 'MR123456'],
        ['Date of Surgery:', 'March 15, 2024'],
        ['Surgeon:', 'Dr. Sarah Johnson, MD']
    ]
    
    patient_table = Table(patient_data, colWidths=[2*inch, 3*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(patient_table)
    story.append(Spacer(1, 20))
    
    # Procedure Information
    story.append(Paragraph("PROCEDURE PERFORMED", styles['Heading2']))
    story.append(Paragraph("Laparoscopic Cholecystectomy (Gallbladder Removal)", styles['Normal']))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("PROCEDURE DETAILS:", styles['Heading3']))
    procedure_text = """
    The patient underwent a successful laparoscopic cholecystectomy for symptomatic cholelithiasis. 
    The procedure was performed under general anesthesia without complications. Four small incisions 
    were made in the abdomen for the laparoscopic approach. The gallbladder was successfully removed 
    and sent to pathology for routine examination.
    
    OPERATIVE FINDINGS:
    - Inflamed gallbladder with multiple gallstones
    - No perforation or abscess formation
    - Normal liver appearance
    - No adhesions or complications
    """
    story.append(Paragraph(procedure_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Post-operative Instructions
    story.append(Paragraph("POST-OPERATIVE INSTRUCTIONS", styles['Heading2']))
    
    instructions_text = """
    WOUND CARE:
    - Keep incision sites clean and dry
    - You may shower after 24 hours, but avoid soaking in baths
    - Change dressings daily or if they become wet or soiled
    - Watch for signs of infection: increased redness, swelling, warmth, or drainage
    
    ACTIVITY:
    - Rest for the first 24-48 hours
    - Gradually increase activity as tolerated
    - No lifting objects heavier than 10 pounds for 2 weeks
    - Avoid strenuous exercise for 4-6 weeks
    - You may return to work in 1-2 weeks depending on your job requirements
    
    DIET:
    - Start with clear liquids and progress to regular diet as tolerated
    - Avoid fatty or greasy foods initially
    - Eat small, frequent meals
    - Stay well hydrated
    
    MEDICATIONS:
    - Take prescribed pain medication as directed
    - Continue taking your regular medications unless instructed otherwise
    - Take prescribed antibiotics if given
    """
    
    story.append(Paragraph(instructions_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Follow-up
    story.append(Paragraph("FOLLOW-UP CARE", styles['Heading2']))
    followup_text = """
    - Follow-up appointment scheduled for March 29, 2024 at 2:00 PM
    - Call the office if you experience severe pain, fever over 101.3°F, or signs of infection
    - Contact Dr. Johnson's office at (555) 123-4567 for any concerns
    - Emergency contact: City Hospital Emergency Department (555) 999-8888
    """
    story.append(Paragraph(followup_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)

def create_medication_pdf():
    """
    Create a sample medication management record
    """
    filename = 'sample_data/medication_record.pdf'
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        textColor=colors.blue
    )
    
    story = []
    
    # Title
    story.append(Paragraph("MEDICATION MANAGEMENT RECORD", title_style))
    story.append(Spacer(1, 12))
    
    # Patient Information
    story.append(Paragraph("PATIENT INFORMATION", styles['Heading2']))
    patient_data = [
        ['Patient Name:', 'Mary Johnson'],
        ['Date of Birth:', 'June 22, 1965'],
        ['Medical Record #:', 'MR789012'],
        ['Primary Care Physician:', 'Dr. Michael Brown, MD'],
        ['Date of Visit:', 'March 20, 2024']
    ]
    
    patient_table = Table(patient_data, colWidths=[2*inch, 3*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(patient_table)
    story.append(Spacer(1, 20))
    
    # Medical Conditions
    story.append(Paragraph("CURRENT MEDICAL CONDITIONS", styles['Heading2']))
    conditions_text = """
    1. Type 2 Diabetes Mellitus (E11.9) - well controlled
    2. Hypertension (I10) - stable on current medication
    3. Hyperlipidemia (E78.5) - improving with medication and diet
    4. Osteoarthritis, knees (M17.9) - mild symptoms
    """
    story.append(Paragraph(conditions_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Current Medications
    story.append(Paragraph("CURRENT MEDICATIONS", styles['Heading2']))
    
    medications_data = [
        ['Medication', 'Dosage', 'Frequency', 'Instructions'],
        ['Metformin', '500mg', 'Twice daily', 'Take with meals'],
        ['Lisinopril', '10mg', 'Once daily', 'Take in morning'],
        ['Atorvastatin', '20mg', 'Once daily', 'Take at bedtime'],
        ['Ibuprofen', '200mg', 'As needed', 'For joint pain, max 3 times daily'],
        ['Multivitamin', '1 tablet', 'Once daily', 'Take with breakfast']
    ]
    
    med_table = Table(medications_data, colWidths=[1.5*inch, 1*inch, 1.2*inch, 2*inch])
    med_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(med_table)
    story.append(Spacer(1, 20))
    
    # Medication Instructions
    story.append(Paragraph("MEDICATION MANAGEMENT INSTRUCTIONS", styles['Heading2']))
    med_instructions = """
    GENERAL GUIDELINES:
    - Take all medications exactly as prescribed
    - Set up a daily medication schedule using a pill organizer
    - Take medications at the same time each day
    - Do not skip doses or stop medications without consulting your doctor
    - Keep a current list of all medications with you at all times
    
    SPECIFIC INSTRUCTIONS:
    
    METFORMIN:
    - Take with food to reduce stomach upset
    - If you miss a dose, take it as soon as you remember
    - Do not double dose if you miss a dose
    - Monitor blood sugar levels as directed
    
    LISINOPRIL:
    - Take at the same time each morning
    - May cause dizziness initially - rise slowly from sitting or lying positions
    - Monitor blood pressure regularly
    - Contact doctor if you develop a persistent cough
    
    ATORVASTATIN:
    - Take at bedtime for best effectiveness
    - Avoid grapefruit and grapefruit juice
    - Report any muscle pain or weakness immediately
    - Annual liver function tests required
    
    MONITORING:
    - Blood pressure: Check weekly at home
    - Blood sugar: Check as directed by your diabetes educator
    - Lab work: Scheduled every 3 months
    - Next appointment: April 20, 2024
    """
    
    story.append(Paragraph(med_instructions, styles['Normal']))
    
    doc.build(story)

def create_diet_plan_pdf():
    """
    Create a sample diet plan record
    """
    filename = 'sample_data/diet_plan_record.pdf'
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        textColor=colors.blue
    )
    
    story = []
    
    # Title
    story.append(Paragraph("NUTRITIONAL ASSESSMENT & DIET PLAN", title_style))
    story.append(Spacer(1, 12))
    
    # Patient Information
    story.append(Paragraph("PATIENT INFORMATION", styles['Heading2']))
    patient_data = [
        ['Patient Name:', 'Robert Wilson'],
        ['Date of Birth:', 'September 10, 1955'],
        ['Medical Record #:', 'MR345678'],
        ['Nutritionist:', 'Sarah Davis, RD'],
        ['Date of Consultation:', 'March 18, 2024']
    ]
    
    patient_table = Table(patient_data, colWidths=[2*inch, 3*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(patient_table)
    story.append(Spacer(1, 20))
    
    # Medical History
    story.append(Paragraph("RELEVANT MEDICAL HISTORY", styles['Heading2']))
    history_text = """
    - Type 2 Diabetes (diagnosed 2018) - HbA1c: 8.2%
    - Hypertension (diagnosed 2015) - currently on medication
    - Obesity (BMI: 32.5) - 40 lb weight loss goal
    - High cholesterol (LDL: 145 mg/dL)
    - Family history of heart disease
    """
    story.append(Paragraph(history_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Current Diet Assessment
    story.append(Paragraph("CURRENT DIET ASSESSMENT", styles['Heading2']))
    assessment_text = """
    CURRENT EATING PATTERNS:
    - Skips breakfast frequently
    - Large portions at lunch and dinner
    - High intake of processed foods and refined carbohydrates
    - Limited vegetable and fruit consumption
    - High sodium intake from restaurant meals
    - Irregular meal timing
    - Limited water intake, high soda consumption
    
    NUTRITIONAL DEFICIENCIES IDENTIFIED:
    - Inadequate fiber intake
    - Low vitamin D levels
    - Insufficient omega-3 fatty acids
    - Poor protein distribution throughout the day
    """
    story.append(Paragraph(assessment_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Diet Plan
    story.append(Paragraph("PERSONALIZED DIET PLAN", styles['Heading2']))
    
    diet_plan_text = """
    DAILY NUTRITION GOALS:
    - Calories: 1,800-2,000 per day
    - Carbohydrates: 45-50% of total calories (focus on complex carbs)
    - Protein: 20-25% of total calories
    - Fat: 25-30% of total calories (emphasize healthy fats)
    - Fiber: 25-30 grams per day
    - Sodium: Less than 2,300mg per day
    - Water: 8-10 glasses per day
    
    MEAL TIMING:
    - Eat 3 balanced meals and 2 healthy snacks daily
    - Don't skip meals, especially breakfast
    - Space meals 3-4 hours apart
    - Last meal should be 2-3 hours before bedtime
    
    FOODS TO EMPHASIZE:
    - Non-starchy vegetables (aim for 5+ servings daily)
    - Lean proteins: fish, poultry, beans, tofu
    - Whole grains: brown rice, quinoa, whole wheat bread
    - Healthy fats: avocado, nuts, olive oil, fatty fish
    - Fresh fruits (2-3 servings daily)
    - Low-fat dairy or dairy alternatives
    
    FOODS TO LIMIT:
    - Refined sugars and sweets
    - Processed and packaged foods
    - Fried foods and high-fat meats
    - White bread, pasta, and rice
    - Sugary beverages and alcohol
    - High-sodium foods
    
    SAMPLE DAILY MEAL PLAN:
    
    BREAKFAST (350 calories):
    - 1 cup oatmeal with 1/2 cup berries and 1 tbsp chopped walnuts
    - 1 cup low-fat milk or unsweetened almond milk
    
    MORNING SNACK (150 calories):
    - 1 small apple with 1 tbsp almond butter
    
    LUNCH (450 calories):
    - Large salad with mixed greens, vegetables, 3 oz grilled chicken
    - 1 tbsp olive oil vinaigrette
    - 1 slice whole grain bread
    
    AFTERNOON SNACK (100 calories):
    - 1/4 cup hummus with raw vegetables
    
    DINNER (500 calories):
    - 4 oz baked salmon
    - 1 cup roasted vegetables
    - 1/2 cup brown rice
    
    EVENING SNACK (if needed, 100 calories):
    - 1 cup plain Greek yogurt with cinnamon
    """
    
    story.append(Paragraph(diet_plan_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Follow-up
    story.append(Paragraph("FOLLOW-UP AND MONITORING", styles['Heading2']))
    followup_text = """
    GOALS FOR NEXT 3 MONTHS:
    - Lose 8-12 pounds through healthy eating and portion control
    - Reduce HbA1c to below 7.5%
    - Improve blood pressure control
    - Establish consistent meal timing
    
    MONITORING:
    - Daily food diary for first 2 weeks
    - Weekly weight checks at home
    - Blood glucose monitoring as directed by physician
    - Follow-up nutrition appointment in 6 weeks
    
    RESOURCES:
    - Diabetes nutrition education classes available
    - MyPlate app for meal tracking
    - Local farmers market guide provided
    - Heart-healthy recipe collection included
    """
    story.append(Paragraph(followup_text, styles['Normal']))
    
    doc.build(story)

if __name__ == "__main__":
    create_sample_pdfs()
