import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Draw header (on all pages except page 1)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor('#1e3a8a'))
            self.drawString(54, 750, "HDI INSIGHT AI — INSTALLATION & DEPLOYMENT GUIDE")
            self.setStrokeColor(colors.HexColor('#d1d5db'))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Draw footer (on all pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#4b5563'))
        self.setStrokeColor(colors.HexColor('#e5e7eb'))
        self.setLineWidth(0.5)
        self.line(54, 50, 558, 50)
        
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 35, page_text)
        self.drawString(54, 35, "HDI Insight AI • Technical Documentation • Confidential")
        self.restoreState()

def make_code_block(command_text, body_style):
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=body_style,
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#111827')
    )
    # Replace spaces with non-breaking spaces and newlines with break tags
    clean_text = command_text.replace(' ', '&nbsp;').replace('\n', '<br/>')
    p = Paragraph(clean_text, code_style)
    t = Table([[p]], colWidths=[504])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f9fafb')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return t

def make_callout(text, title, body_style, callout_type="info"):
    title_style = ParagraphStyle(
        'CalloutTitle',
        parent=body_style,
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#1e3a8a') if callout_type == "info" else colors.HexColor('#9a3412')
    )
    content_style = ParagraphStyle(
        'CalloutContent',
        parent=body_style,
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1f2937')
    )
    
    story = [Paragraph(title, title_style), Spacer(1, 4), Paragraph(text, content_style)]
    t = Table([[story]], colWidths=[504])
    bg_color = '#eff6ff' if callout_type == "info" else '#fff7ed'
    border_color = '#3b82f6' if callout_type == "info" else '#f97316'
    
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
        ('LINELEFT', (0,0), (-1,-1), 3.0, colors.HexColor(border_color)),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return t

def build_pdf():
    output_path = "07_Project_Documentation/Installation_Guide.pdf"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0f766e'),
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#1e3a8a'),
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#0f766e'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=4
    )

    story = []
    
    # Title Block
    story.append(Spacer(1, 10))
    story.append(Paragraph("HDI INSIGHT AI", title_style))
    story.append(Paragraph("TECHNICAL INSTALLATION & DEPLOYMENT GUIDE", subtitle_style))
    
    # Meta Info block
    meta_data = [
        [Paragraph("<b>Target Environment:</b> Local / Server", body_style), Paragraph("<b>Software Version:</b> v1.0.0", body_style)],
        [Paragraph("<b>Dependencies:</b> Python 3.10+", body_style), Paragraph("<b>Document Classification:</b> Public", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[252, 252])
    meta_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#d1d5db')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))
    
    # Section 1: Overview
    story.append(Paragraph("1. System Overview & Requirements", h1_style))
    story.append(Paragraph(
        "This guide outlines the system specifications and step-by-step setup instructions to install, initialize, and deploy the "
        "<b>HDI Insight AI (Human Development Analytics Platform)</b> codebase. The application is built using a Flask backend, "
        "SQLite database, and scikit-learn machine learning binaries, making it highly portable and standard-compliant.",
        body_style
    ))
    
    story.append(Paragraph("Hardware Requirements:", h2_style))
    story.append(Paragraph("• <b>CPU:</b> Dual-core 2.0 GHz or higher (x86/x64 or Apple Silicon)", bullet_style))
    story.append(Paragraph("• <b>RAM:</b> 4 GB minimum (8 GB recommended for model training)", bullet_style))
    story.append(Paragraph("• <b>Disk Space:</b> 100 MB free space (excluding training datasets)", bullet_style))
    
    story.append(Paragraph("Software Dependencies & Prerequisites:", h2_style))
    story.append(Paragraph("• <b>Python Version:</b> Python 3.10 or 3.11 is recommended. Validate with <code>python --version</code>.", bullet_style))
    story.append(Paragraph("• <b>Database Engine:</b> SQLite3 (Standard library, no external server required).", bullet_style))
    story.append(Paragraph("• <b>Web Browser:</b> Google Chrome, Mozilla Firefox, or Microsoft Edge (recent versions).", bullet_style))
    
    story.append(Spacer(1, 10))
    
    # Section 2: Step-by-Step Installation
    story.append(Paragraph("2. Step-by-Step Installation", h1_style))
    
    story.append(Paragraph("Step 1: Obtain the Codebase", h2_style))
    story.append(Paragraph("Clone the repository from GitHub or extract the project source files to your local system:", body_style))
    story.append(make_code_block("git clone https://github.com/pandu0426/HDI-Insights.git\ncd HDI-Insights/05_Project_Development", body_style))
    
    story.append(Paragraph("Step 2: Create a Python Virtual Environment", h2_style))
    story.append(Paragraph(
        "It is strongly recommended to isolate the project dependencies within a local virtual environment. Run the following command inside the project development folder:", 
        body_style
    ))
    story.append(make_code_block("python -m venv venv", body_style))
    
    story.append(Paragraph("Step 3: Activate the Virtual Environment", h2_style))
    story.append(Paragraph("Select and run the appropriate activation command for your Operating System's shell environment:", body_style))
    story.append(Paragraph("<b>Windows (PowerShell):</b>", bullet_style))
    story.append(make_code_block("venv\\Scripts\\Activate.ps1", body_style))
    story.append(Paragraph("<b>Windows (Command Prompt):</b>", bullet_style))
    story.append(make_code_block("venv\\Scripts\\activate.bat", body_style))
    story.append(Paragraph("<b>macOS / Linux (Bash/Zsh):</b>", bullet_style))
    story.append(make_code_block("source venv/bin/activate", body_style))
    
    story.append(Spacer(1, 10))
    
    # Force page break for remaining steps to look clean
    story.append(Paragraph("Step 4: Install Required Packages", h2_style))
    story.append(Paragraph(
        "Install the compiled web application dependencies, including Flask, Pandas, NumPy, Scikit-Learn, Joblib, and ReportLab:", 
        body_style
    ))
    story.append(make_code_block("pip install -r requirements.txt", body_style))
    
    story.append(Paragraph("Step 5: Train and Serialize ML Models", h2_style))
    story.append(Paragraph(
        "Run the machine learning preprocessing, training, and benchmarking pipeline. This cleans the raw UNDP dataset, performs log transforms, trains the classifier and regressor companion models, outputs comparative JSON stats, and serializes the <code>.joblib</code> models:",
        body_style
    ))
    story.append(make_code_block("python train_model.py", body_style))
    
    story.append(Paragraph("Step 6: Start the Flask Application Server", h2_style))
    story.append(Paragraph(
        "Initialize the SQLite history database and launch the WSGI development web server:",
        body_style
    ))
    story.append(make_code_block("python app.py", body_style))
    
    # Section 3: Verification & Test Executions
    story.append(Paragraph("3. Verification and Testing", h1_style))
    story.append(Paragraph(
        "Once the Flask server is running, you should verify its operation by executing the following procedures:",
        body_style
    ))
    story.append(Paragraph("1. Open your web browser and navigate to: <b>http://localhost:5000/</b>.", bullet_style))
    story.append(Paragraph("2. Verify that the homepage dashboard renders without errors and displaying the historical chart logs.", bullet_style))
    story.append(Paragraph("3. Open another terminal panel, activate your environment, and execute the automated unit test suite:", bullet_style))
    story.append(make_code_block("python -m unittest test_app.py", body_style))
    
    story.append(Spacer(1, 8))
    
    # Troubleshooting block
    story.append(Paragraph("4. Troubleshooting Common Issues", h1_style))
    story.append(make_callout(
        "If you encounter a 'ModuleNotFoundError', ensure your virtual environment is actively running in the current terminal window. Run 'pip list' to confirm the installed dependencies.",
        "Error: Missing Dependencies / Libraries",
        body_style,
        "warning"
    ))
    story.append(Spacer(1, 8))
    story.append(make_callout(
        "If Flask crashes with a bind error (port already in use), another server is running on port 5000. You can change the port in the app run settings inside app.py, or run: python app.py --port=5001.",
        "Error: Address already in use (Port 5000)",
        body_style,
        "warning"
    ))
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Installation_Guide.pdf built successfully.")

if __name__ == "__main__":
    build_pdf()
