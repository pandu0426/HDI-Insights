import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, Image
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
            self.setFillColor(colors.HexColor('#0f766e'))
            self.drawString(54, 750, "HDI INSIGHT AI — USER MANUAL & VISUAL WALKTHROUGH")
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
        self.drawString(54, 35, "HDI Insight AI • End-User Documentation • Version 1.0")
        self.restoreState()

def add_screenshot_flowable(screenshot_name, caption_text, body_style):
    # Relative path from 07_Project_Documentation
    path = os.path.join("..", "Screenshots", screenshot_name)
    elements = []
    
    if os.path.exists(path):
        try:
            img = Image(path, width=400, height=225)
            elements.append(img)
            elements.append(Spacer(1, 4))
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            
    caption_style = ParagraphStyle(
        'ImageCaption',
        parent=body_style,
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        alignment=1, # Center
        textColor=colors.HexColor('#4b5563')
    )
    elements.append(Paragraph(f"Figure: {caption_text}", caption_style))
    elements.append(Spacer(1, 10))
    
    t = Table([[elements]], colWidths=[420])
    t.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f9fafb')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    return t

def build_pdf():
    output_path = "07_Project_Documentation/User_Manual.pdf"
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
        textColor=colors.HexColor('#0f766e'),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0f766e'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#1e3a8a'),
        spaceBefore=8,
        spaceAfter=4,
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
    
    # Title Page Info
    story.append(Spacer(1, 10))
    story.append(Paragraph("HDI INSIGHT AI", title_style))
    story.append(Paragraph("SYSTEM USER MANUAL & INTERFACE GUIDE", subtitle_style))
    
    meta_data = [
        [Paragraph("<b>Author:</b> Mohammad Tayyab", body_style), Paragraph("<b>Software Version:</b> v1.0.0", body_style)],
        [Paragraph("<b>Target Audience:</b> Policy Advisors & Researchers", body_style), Paragraph("<b>Release Date:</b> July 2026", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[252, 252])
    meta_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#d1d5db')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))
    
    # Section 1: Introduction
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(Paragraph(
        "Welcome to the <b>HDI Insight AI</b> Human Development Analytics Platform. This system is an AI-powered portal "
        "designed to predict, analyze, and advise on human development indicator performance. By mapping four essential socioeconomic "
        "parameters, the platform provides real-time estimates of a country's Human Development Index (HDI) category "
        "along with policy recommendations to improve societal indicators. This document provides step-by-step guidance "
        "to operate all integrated user features.",
        body_style
    ))
    
    # Section 2: Launching
    story.append(Paragraph("2. Accessing the Application", h1_style))
    story.append(Paragraph(
        "Once installed and initialized according to the Installation Guide, launch your modern web browser (Chrome, Firefox, or Edge) "
        "and navigate to the host port address: <b>http://localhost:5000/</b>.",
        body_style
    ))
    story.append(Paragraph(
        "You will be greeted with the main interactive analytics interface. The portal uses clean CSS variables "
        "allowing you to instantly toggle between light and dark modes via the toggle in the navigation bar.",
        body_style
    ))
    
    # Section 3: Interactive Features
    story.append(Paragraph("3. Interactive Features & Guide", h1_style))
    
    story.append(Paragraph("HDI Prediction Simulator", h2_style))
    story.append(Paragraph(
        "Navigate to the main form to run a new simulation. Modify the input sliders representing the four key indicators: "
        "Life Expectancy at birth (years), Expected years of schooling, Mean years of schooling, and Gross National Income (GNI) per capita (PPP $). "
        "Click the <b>Predict HDI</b> button to submit. The system will display the predicted HDI category (Low, Medium, High, or Very High) "
        "on the confidence gauge, along with the continuous score estimation.",
        body_style
    ))
    
    story.append(Paragraph("Explainable AI & Recommendations", h2_style))
    story.append(Paragraph(
        "The model automatically generates local explainability (XAI) diagnostics, plotting the relative weight "
        "of each feature on the prediction outcome. Additionally, the intelligent advisor engine provides active development policy advice "
        "by comparing your profile variables against standard world medians, highlighting critical focus areas for national investment.",
        body_style
    ))
    
    story.append(Paragraph("Country Comparisons", h2_style))
    story.append(Paragraph(
        "Click on the <b>Country Comparison</b> tab. Select any real-world country from the dropdown to compare your simulated "
        "socioeconomic profile side-by-side with official global datasets. Comparison bar charts will highlight gaps in healthcare, "
        "education, and income index factors.",
        body_style
    ))
    
    story.append(Paragraph("Exporting Reports & History", h2_style))
    story.append(Paragraph(
        "The system records all successful runs. You can view, search, and delete entries from the prediction log history. "
        "Click <b>Download PDF</b> on any prediction block to generate a clean, stylized, single-page summary report. "
        "Click <b>Export CSV</b> at the top of the history list to save the full simulation history database locally.",
        body_style
    ))
    
    story.append(Spacer(1, 10))
    
    # Section 4: Interface Screenshots
    story.append(Paragraph("4. Screen Gallery & Walkthrough", h1_style))
    
    # Home Page Screenshot
    story.append(Paragraph("Home Landing Portal", h2_style))
    story.append(Paragraph("The home page displays the dashboard dashboard, historical logs, and shortcuts to launch a new simulator run.", body_style))
    story.append(add_screenshot_flowable("Home.png", "Home Dashboard Interface Overview", body_style))
    story.append(Spacer(1, 10))
    
    # Prediction Page Screenshot
    story.append(Paragraph("Prediction Simulator Panel", h2_style))
    story.append(Paragraph("The simulator page features range input sliders, the primary confidence gauge, and companion regressor outputs.", body_style))
    story.append(add_screenshot_flowable("Prediction.png", "Simulation Form and Live Gauge Output", body_style))
    story.append(Spacer(1, 10))
    
    # Dashboard Screenshot
    story.append(Paragraph("Interactive Dashboard", h2_style))
    story.append(Paragraph("Analytical views displaying summary charts of prediction records and distribution frequencies.", body_style))
    story.append(add_screenshot_flowable("Dashboard.png", "Dashboard Visualizations Panel", body_style))
    story.append(Spacer(1, 10))
    
    # Country Comparison Screenshot
    story.append(Paragraph("Country Comparison Tool", h2_style))
    story.append(Paragraph("This panel plots comparative charts matching user-defined profiles against real-world countries.", body_style))
    story.append(add_screenshot_flowable("CountryComparison.png", "Comparing Simulated Parameters with Benchmarks", body_style))
    story.append(Spacer(1, 10))
    
    # Model Performance Screenshot
    story.append(Paragraph("Model Performance Dashboard", h2_style))
    story.append(Paragraph("Displays performance metrics tables, model training times, and confusion matrices for all algorithms.", body_style))
    story.append(add_screenshot_flowable("ModelPerformance.png", "Algorithm Benchmarking and Calibration Panel", body_style))
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print("User_Manual.pdf built successfully.")

if __name__ == "__main__":
    build_pdf()
