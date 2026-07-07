import os
import sys
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
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
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        # Suppress on page 1 (Title cover page)
        if self._pageNumber == 1:
            return
            
        self.saveState()
        
        # Header decoration
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor('#1e3a8a')) # Deep Navy
        self.drawString(54, 750, "HDI INSIGHT AI — COMPREHENSIVE PROJECT FINAL REPORT")
        self.setStrokeColor(colors.HexColor('#d1d5db'))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)
        
        # Footer decoration
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#4b5563')) # Gray
        self.setStrokeColor(colors.HexColor('#e5e7eb'))
        self.setLineWidth(0.5)
        self.line(54, 50, 558, 50)
        
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 35, page_text)
        self.drawString(54, 35, "HDI Insight AI • Academic Portfolio Submission • Department of Software Engineering")
        
        self.restoreState()

def add_screenshot_flowable(screenshot_name, caption_text, body_style):
    path = os.path.join("..", "Screenshots", screenshot_name)
    elements = []
    if os.path.exists(path):
        try:
            img = Image(path, width=320, height=180)
            elements.append(img)
            elements.append(Spacer(1, 4))
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            
    caption_style = ParagraphStyle(
        'ImageCaption',
        parent=body_style,
        fontName='Helvetica-Oblique',
        fontSize=8,
        alignment=1,
        textColor=colors.HexColor('#4b5563')
    )
    elements.append(Paragraph(f"Figure: {caption_text}", caption_style))
    elements.append(Spacer(1, 8))
    
    t = Table([[elements]], colWidths=[340])
    t.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f9fafb')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    return t

def build_pdf():
    output_path = "07_Project_Documentation/Final_Report.pdf"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=colors.HexColor('#1e3a8a'),
        alignment=1,
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0f766e'),
        alignment=1,
        spaceAfter=40
    )
    
    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
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
        spaceAfter=5,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
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
    
    header_table_style = ParagraphStyle(
        'HeaderTable',
        parent=body_style,
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=colors.white
    )

    story = []
    
    # ==================== PAGE 1: TITLE COVER ====================
    story.append(Spacer(1, 40))
    # Icon/Deco banner representation
    deco_table = Table([['']], colWidths=[504], rowHeights=[6])
    deco_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1e3a8a')),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(deco_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("HDI INSIGHT AI", title_style))
    story.append(Paragraph("AI-Powered Human Development Analytics Platform using Machine Learning", subtitle_style))
    
    story.append(Spacer(1, 60))
    
    # Author details cover table
    team_cover_data = [
        [Paragraph("<b>Prepared By:</b>", body_style), Paragraph("", body_style)],
        [Paragraph("1. Varigeti Karthikeya (Team Lead)", body_style), Paragraph("Project Planning & Backend Architect", body_style)],
        [Paragraph("2. Veera Ajay Kumar Adapa", body_style), Paragraph("Machine Learning Engineering Pipeline", body_style)],
        [Paragraph("3. Gulla Chandana", body_style), Paragraph("Frontend Design & Charting Visualizations", body_style)],
        [Paragraph("4. Ambati Krupa Jesudas", body_style), Paragraph("Quality Assurance & Unit Testing Framework", body_style)],
        [Paragraph("5. Mohammad Tayyab", body_style), Paragraph("DevOps, PDF Reporting & Technical Writing", body_style)],
        [Paragraph("<b>Submitted For:</b> Academic & Internship Evaluation", body_style), Paragraph("<b>Submission Date:</b> July 2026", body_style)]
    ]
    t_cover = Table(team_cover_data, colWidths=[252, 252])
    t_cover.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor('#1e3a8a')),
        ('LINEBELOW', (0,-2), (-1,-2), 1, colors.HexColor('#1e3a8a')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_cover)
    story.append(PageBreak())
    
    # ==================== PAGE 2: ABSTRACT & TABLE OF CONTENTS ====================
    story.append(Paragraph("Abstract", h1_style))
    story.append(Paragraph(
        "The Human Development Index (HDI) is a composite index formulated by the United Nations Development Programme (UNDP) "
        "to evaluate long-term progress in three basic dimensions of human development: a long and healthy life, access to knowledge, "
        "and a decent standard of living. Evaluating and predicting changes in HDI category based on developmental inputs is essential "
        "for governmental policy, academic analysis, and budget prioritization. However, manual estimation is highly complex and error-prone "
        "due to multi-variable indexing dependencies. This project presents <b>HDI Insight AI</b>, a premium analytical system that integrates "
        "Machine Learning (ML) pipeline benchmarking with a modern interactive Flask application. Using a trained Support Vector Machine (SVM) "
        "classifier, the system achieves a **98.9% prediction accuracy** in determining HDI categories, companion regressor score estimates, "
        "local Explainable AI (XAI) feature diagnostics, and automated developmental recommendations. The project demonstrates the viability "
        "of deploying machine learning modules to guide policy planning and accelerate socioeconomic growth.",
        body_style
    ))
    
    story.append(Spacer(1, 10))
    
    # Table of Contents placeholder
    story.append(Paragraph("Table of Contents", h1_style))
    toc_data = [
        ["1. Introduction & Abstract", "Page 2"],
        ["2. Problem Statement & System Scope", "Page 3"],
        ["3. Project Objectives & Intended Benefits", "Page 3"],
        ["4. System Architecture & Component Mapping", "Page 4"],
        ["5. Machine Learning Engineering Pipeline", "Page 4"],
        ["6. Model Performance Benchmarking & Selection", "Page 5"],
        ["7. Functional Features Implementation", "Page 6"],
        ["8. System Verification & Test Cases", "Page 7"],
        ["9. Future Scope & Architectural Extensions", "Page 8"],
        ["10. Conclusion & Team Contribution Roles", "Page 8"]
    ]
    t_toc = Table(toc_data, colWidths=[400, 104])
    t_toc.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_toc)
    story.append(PageBreak())
    
    # ==================== PAGE 3: PROBLEM STATEMENT & OBJECTIVES ====================
    story.append(Paragraph("1. Problem Statement", h1_style))
    story.append(Paragraph(
        "Modern human development analysis involves processing multi-dimensional, sparse datasets containing hundreds of socioeconomic indicators. "
        "Policymakers and researchers face significant bottlenecks:",
        body_style
    ))
    story.append(Paragraph("• <b>Complexity of Index Calculation:</b> Mathematical calculation of dimensional indices requires rigid normalization scales, making instant feedback simulation impossible.", bullet_style))
    story.append(Paragraph("• <b>Lack of Predictive Power:</b> Existing UNDP databases present historical records but lack the ability to model hypothetical scenarios (e.g., 'What happens if life expectancy increases by 3 years?').", bullet_style))
    story.append(Paragraph("• <b>Black-Box Analytical Gaps:</b> Standard spreadsheets do not output explainable diagnostics or link predictions directly to policy guidelines.", bullet_style))
    story.append(Paragraph("• <b>Data-Driven Policy Obstacles:</b> Governments require structured, validated recommendations to justify budget allocations toward healthcare, education, or GNI improvements.", bullet_style))
    story.append(Paragraph(
        "<b>Proposed Solution:</b> HDI Insight AI addresses these issues by offering an intelligent, real-time prediction simulator. The platform "
        "exposes localized ML predictions, illustrates feature weights, and outputs automated development advice, converting dry data logs into actionable knowledge.",
        body_style
    ))
    
    story.append(Paragraph("2. Objectives", h1_style))
    story.append(Paragraph("The system is engineered to satisfy the following primary technical objectives:", body_style))
    story.append(Paragraph("• <b>Inference Precision:</b> Deliver over 95% accuracy in classifying the four target HDI categories (Low, Medium, High, Very High).", bullet_style))
    story.append(Paragraph("• <b>Local Explainability:</b> Expose real-time feature contributions to explain why a specific category was classified.", bullet_style))
    story.append(Paragraph("• <b>Auto-Advisory Engine:</b> Design rules matching simulated inputs to global medians to provide relevant policy guidelines.", bullet_style))
    story.append(Paragraph("• <b>Dual Modeling Framework:</b> Incorporate a classifier (for Category) and companion regressor (for continuous HDI index) in a unified interface.", bullet_style))
    story.append(Paragraph("• <b>Professional Documentation:</b> Output client-ready PDF prediction report sheets and CSV history exports dynamically.", bullet_style))
    story.append(PageBreak())
    
    # ==================== PAGE 4: ARCHITECTURE & ML WORKFLOW ====================
    story.append(Paragraph("3. System Architecture & Component Mapping", h1_style))
    story.append(Paragraph(
        "HDI Insight AI follows a classic client-server MVC model with specialized machine learning modules. The data flow follows a secure pipeline:",
        body_style
    ))
    
    # Architecture Diagram Description Table
    arch_data = [
        [Paragraph("<b>Component</b>", header_table_style), Paragraph("<b>Technology</b>", header_table_style), Paragraph("<b>Function / Role</b>", header_table_style)],
        ["User Interface", "HTML5, CSS3, JS, Bootstrap, Chart.js", "Provides slider inputs, plots confidence gauges, comparison charts, and displays recommendations."],
        ["Backend Core", "Python, Flask Framework", "Handles route mappings, input validation, calls prediction models, queries DB, and invokes PDF generator."],
        ["ML Inference Engine", "Scikit-Learn (SVM + RF Joblib)", "Computes predictions, continuous score index, and extracts localized feature contributions (XAI)."],
        ["Database Layer", "SQLite3 Database (hdi_history.db)", "Maintains persistent logs of past simulations for historical audit and dashboard stats."],
        ["Reporting Module", "ReportLab Engine", "Compiles prediction summaries into professional, single-page downloadable PDFs."]
    ]
    t_arch = Table(arch_data, colWidths=[120, 130, 254])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d1d5db')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f9fafb')]),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
    ]))
    story.append(t_arch)
    
    story.append(Paragraph("4. Machine Learning Engineering Pipeline", h1_style))
    story.append(Paragraph(
        "The modeling pipeline contains robust components for data cleaning, transformation, scaling, and companion scoring:",
        body_style
    ))
    story.append(Paragraph("1. <b>Imputation:</b> Missing indicator values are imputed first using country-specific medians, then global medians to preserve data distribution.", bullet_style))
    story.append(Paragraph("2. <b>Scaling:</b> GNI per capita exhibits a highly right-skewed distribution. Applying a logarithmic transform stabilizes variance. Features are then normalized using standard scaling (zero mean, unit variance).", bullet_style))
    story.append(Paragraph("3. <b>companion Modeling:</b> The system saves a Support Vector Machine classifier (SVC with RBF kernel) for categories, and a Random Forest Regressor to compute continuous index values.", bullet_style))
    story.append(PageBreak())
    
    # ==================== PAGE 5: MODEL PERFORMANCE ====================
    story.append(Paragraph("5. Model Performance Benchmarking & Selection", h1_style))
    story.append(Paragraph(
        "Five popular classifiers were trained and evaluated on a 75/25 split of the cleaned UNDP dataset. The comparative performance metrics are detailed below:",
        body_style
    ))
    
    # Model metrics table
    metrics_data = [
        [Paragraph("<b>Algorithm</b>", header_table_style), Paragraph("<b>Test Accuracy</b>", header_table_style), Paragraph("<b>Weighted F1-Score</b>", header_table_style), Paragraph("<b>Training Time</b>", header_table_style), Paragraph("<b>File Size</b>", header_table_style)],
        ["Support Vector Machine", "98.9%", "98.9%", "0.050s", "27.0 KB"],
        ["Logistic Regression", "98.1%", "98.1%", "0.014s", "1.0 KB"],
        ["Random Forest", "97.5%", "97.5%", "0.144s", "1,026.0 KB"],
        ["K-Nearest Neighbors", "96.2%", "96.2%", "0.002s", "118.8 KB"],
        ["Decision Tree", "95.6%", "95.6%", "0.003s", "12.2 KB"]
    ]
    t_metrics = Table(metrics_data, colWidths=[160, 90, 110, 80, 64])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d1d5db')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f9fafb')]),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('TEXTCOLOR', (0,1), (0,1), colors.HexColor('#1e3a8a')), # bold SVM
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Confusion Matrix (Support Vector Machine):", h2_style))
    story.append(Paragraph(
        "Out of 476 test records, the SVM classifier correctly predicted 471 records. The confusion matrix breakdown shows high separation "
        "across all categories: Low (105/105), Medium (93/96), High (69/71), Very High (204/204). The companion Random Forest Regressor "
        "achieves a Mean Squared Error (MSE) of 0.0012, confirming high predictive reliability.",
        body_style
    ))
    
    story.append(Paragraph("Selected Model Rationale:", h2_style))
    story.append(Paragraph(
        "The Support Vector Machine (RBF Kernel) was chosen for deployment. It provides the highest accuracy and F1-score (98.9%), "
        "has a highly compact serialized footprint (27.0 KB), and exhibits excellent generalization capabilities on boundary edge thresholds "
        "compared to other algorithms.",
        body_style
    ))
    story.append(PageBreak())
    
    # ==================== PAGE 6: FUNCTIONAL FEATURES ====================
    story.append(Paragraph("6. Functional Features Implementation", h1_style))
    story.append(Paragraph(
        "HDI Insight AI implements a robust, client-ready set of analysis and reporting tools:",
        body_style
    ))
    
    story.append(Paragraph("1. 🔮 Prediction Simulator", h2_style))
    story.append(Paragraph(
        "Allows dynamic entry of Life Expectancy, Expected Schooling, Mean Schooling, and GNI per Capita through sliders. "
        "Outputs predicted category and continuous score simultaneously.",
        body_style
    ))
    
    story.append(Paragraph("2. 🧠 Local Explainable AI (XAI)", h2_style))
    story.append(Paragraph(
        "Exposes local explanation weights calculating features' positive or negative force on the predicted class, "
        "letting developers and researchers trust the model logic.",
        body_style
    ))
    
    story.append(Paragraph("3. 📋 Automated Development Advisor", h2_style))
    story.append(Paragraph(
        "A rules engine that compares input indicators against standard global benchmarks and recommends target policies "
        "(e.g., recommend GNI focus if GNI is below world median).",
        body_style
    ))
    
    story.append(Paragraph("4. 🔍 Country Comparison tab", h2_style))
    story.append(Paragraph(
        "Users can compare simulated socioeconomic scenarios side-by-side with historical records of other countries from a global DB.",
        body_style
    ))
    
    story.append(Paragraph("5. 📄 Professional Document Exporter", h2_style))
    story.append(Paragraph(
        "Enables dynamically compiling predictions as beautifully styled PDF summaries on the server side and exporting history to CSV formats.",
        body_style
    ))
    
    # Screenshot display block
    story.append(Spacer(1, 10))
    story.append(add_screenshot_flowable("Prediction.png", "Prediction Portal showing Confidence Gauge & XAI", body_style))
    story.append(PageBreak())
    
    # ==================== PAGE 7: TESTING & QA ====================
    story.append(Paragraph("7. System Verification & Test Cases", h1_style))
    story.append(Paragraph(
        "The system has been verified using a multi-tiered testing plan: Unit Testing, Integration Testing, and User Acceptance testing.",
        body_style
    ))
    
    story.append(Paragraph("Unit & Integration Testing (test_app.py):", h2_style))
    story.append(Paragraph(
        "Automated unit tests assert the validity of endpoints, test prediction boundary conditions (Min and Max slider edges), "
        "and check data inputs validation filters (e.g. negative schooling values must be rejected with HTTP 400).",
        body_style
    ))
    
    story.append(Paragraph("Sample Execution Test Cases:", h2_style))
    
    # Test case table layout representation
    tc_data = [
        [Paragraph("<b>ID</b>", header_table_style), Paragraph("<b>Test Scope</b>", header_table_style), Paragraph("<b>Inputs</b>", header_table_style), Paragraph("<b>Expected Output</b>", header_table_style), Paragraph("<b>Status</b>", header_table_style)],
        ["TC-001", "Home page rendering", "GET /", "HTTP 200, HTML page with forms", "PASS"],
        ["TC-002", "Predict Valid inputs", "Life: 75.5, GNI: 25k", "HTTP 200, category predicted", "PASS"],
        ["TC-003", "Validation boundaries Min", "Life: 20.0 (Min limit)", "HTTP 200, category is 'Low'", "PASS"],
        ["TC-004", "Validation boundaries Max", "Life: 100.0 (Max limit)", "HTTP 200, category 'Very High'", "PASS"],
        ["TC-005", "Validation boundary reject", "Life: 15.0 (Out of bounds)", "HTTP 400, validation errors JSON", "PASS"],
        ["TC-006", "Report download API", "GET /download_pdf/1", "HTTP 200, application/pdf blob", "PASS"]
    ]
    t_tc = Table(tc_data, colWidths=[54, 120, 130, 150, 50])
    t_tc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d1d5db')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f9fafb')]),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('TEXTCOLOR', (4,1), (4,-1), colors.HexColor('#0f766e')), # pass green
    ]))
    story.append(t_tc)
    
    # Dashboard Screenshot display
    story.append(Spacer(1, 10))
    story.append(add_screenshot_flowable("Dashboard.png", "Interactive Prediction Logs Dashboard", body_style))
    story.append(PageBreak())
    
    # ==================== PAGE 8: FUTURE SCOPE, CONCLUSION & TEAM DETAILS ====================
    story.append(Paragraph("8. Future Scope & Architectural Extensions", h1_style))
    story.append(Paragraph(
        "To expand the utility of the HDI Insight AI platform for national-scale policy modeling, several future scope expansions are outlined:",
        body_style
    ))
    story.append(Paragraph("• <b>Deep Learning Models:</b> Integrating multi-layer perceptron (MLP) networks to model non-linear indicator interactions.", bullet_style))
    story.append(Paragraph("• <b>World Map Analytics:</b> Visualizing simulated profiles using Leaflet.js map components color-coded dynamically.", bullet_style))
    story.append(Paragraph("• <b>Time-Series Forecasting:</b> Adding LSTM recurrent neural networks to forecast a country's indicator trends for the next 10 years.", bullet_style))
    story.append(Paragraph("• <b>Advanced XAI:</b> Incorporating SHAP and LIME library diagnostics directly in the UI dashboard.", bullet_style))
    story.append(Paragraph("• <b>Chatbot Advisory:</b> Deploying a lightweight LLM chat agent to discuss policy implementations based on simulated metrics.", bullet_style))
    
    story.append(Paragraph("9. Conclusion", h1_style))
    story.append(Paragraph(
        "The HDI Insight AI platform successfully demonstrates the integration of robust machine learning pipelines with user-friendly "
        "analytics dashboards. By using standard python-based technologies (Flask, Scikit-Learn, SQLite, and ReportLab), we built a "
        "highly scalable, lightweight application. Benchmarks confirm that the Support Vector Machine classifier provides a reliable, "
        "efficient prediction framework, achieving a 98.9% F1-score. The application is well-suited for academic demonstrations, "
        "professional portfolios, and public policy ideation, showing the strength of data-driven decision tools.",
        body_style
    ))
    
    story.append(Paragraph("10. Project Team & Roles", h1_style))
    team_data = [
        [Paragraph("<b>Member Name</b>", header_table_style), Paragraph("<b>Project Role</b>", header_table_style), Paragraph("<b>Key Responsibilities / Contributions</b>", header_table_style)],
        ["Varigeti Karthikeya", "Team Lead & Backend Lead", "Project scheduling, Flask route handlers, database integration, API controller logic."],
        ["Veera Ajay Kumar Adapa", "Machine Learning Engineer", "Preprocessing scripts, model benchmarking, tuning SVM & companion RF, saving binaries."],
        ["Gulla Chandana", "Frontend Designer", "Interactive UI layout, Light/Dark mode stylesheet variables, Chart.js implementation."],
        ["Ambati Krupa Jesudas", "QA & Test Engineer", "Unit tests creation, edge cases validation, UAT checklist design, test executions."],
        ["Mohammad Tayyab", "Technical Writer & DevOps", "Programmatic PDF reporting module, installation guides, user manuals, deployment."]
    ]
    t_team = Table(team_data, colWidths=[130, 130, 244])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d1d5db')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f9fafb')]),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
    ]))
    story.append(t_team)
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Final_Report.pdf built successfully.")

if __name__ == "__main__":
    build_pdf()
