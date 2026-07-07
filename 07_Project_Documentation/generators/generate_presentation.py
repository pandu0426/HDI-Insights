import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Define color constants (Premium Theme)
NAVY = RGBColor(30, 58, 138)       # #1e3a8a (Primary Dark)
TEAL = RGBColor(15, 118, 110)      # #0f766e (Secondary Accents)
DARK_GRAY = RGBColor(31, 41, 55)    # #1f2937 (Text Dark)
WHITE = RGBColor(255, 255, 255)
LIGHT_GRAY = RGBColor(243, 244, 246) # #f3f4f6 (Background Light)
LIGHT_BLUE = RGBColor(239, 246, 255) # #eff6ff (Callout box)

def set_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_slide_header(slide, title_text, dark_theme=False):
    # Standard header location
    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12.133), Inches(0.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = 'Helvetica'
    p.font.bold = True
    p.font.size = Pt(28)
    p.font.color.rgb = WHITE if dark_theme else NAVY
    
    # Subheader accent line (only for light theme)
    if not dark_theme:
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.25), Inches(12.133), Inches(0.04))
        shape.fill.solid()
        shape.fill.fore_color.rgb = TEAL
        shape.line.color.rgb = TEAL

def add_bullet_points(slide, points, left, top, width, height, font_size=15, dark_theme=False):
    tx_box = slide.shapes.add_textbox(left, top, width, height)
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    for i, pt_text in enumerate(points):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = pt_text
        p.font.name = 'Helvetica'
        p.font.size = Pt(font_size)
        p.font.color.rgb = WHITE if dark_theme else DARK_GRAY
        p.space_after = Pt(8)
        p.level = 0
        
        # Check if sub-bullet or bolding
        if pt_text.startswith("  - ") or pt_text.startswith("    "):
            p.level = 1
            p.font.size = Pt(font_size - 2.5)
            p.space_after = Pt(4)
            p.font.italic = True

def add_text_box(slide, text, left, top, width, height, font_size=13, bold=False, color=DARK_GRAY, align=PP_ALIGN.LEFT):
    tx_box = slide.shapes.add_textbox(left, top, width, height)
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    p.font.name = 'Helvetica'
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    return tx_box

def add_table(slide, rows, cols, left, top, width, height):
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    return table_shape.table

def format_table_cell(cell, text, bold=False, font_size=11, text_color=DARK_GRAY, bg_color=None):
    cell.text = text
    if bg_color:
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_color
    p = cell.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    p.font.name = 'Helvetica'
    p.font.bold = bold
    p.font.size = Pt(font_size)
    p.font.color.rgb = text_color

def build_presentation():
    prs = Presentation()
    # Set 16:9 widescreen layout standard
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # ----------------------------------------------------
    # SLIDE 1: Title Slide (Dark Navy)
    # ----------------------------------------------------
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide1, NAVY)
    
    # Large Title
    t_box = slide1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(1.5))
    tf = t_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "HDI INSIGHT AI"
    p.font.name = 'Helvetica'
    p.font.bold = True
    p.font.size = Pt(54)
    p.font.color.rgb = WHITE
    
    # Subtitle
    p2 = tf.add_paragraph()
    p2.text = "AI-Powered Human Development Analytics Platform using Machine Learning"
    p2.font.name = 'Helvetica'
    p2.font.size = Pt(20)
    p2.font.color.rgb = TEAL
    p2.space_before = Pt(10)
    
    # Submission Info
    info_points = [
        "Academic & Portfolio Review Submission deck",
        "Created by: Varigeti Karthikeya (Lead), Veera Ajay Kumar Adapa, Gulla Chandana,",
        "Ambati Krupa Jesudas, Mohammad Tayyab",
        "Socioeconomic Indicators Simulation • July 2026"
    ]
    add_bullet_points(slide1, info_points, Inches(0.8), Inches(4.5), Inches(11.733), Inches(2.2), font_size=13, dark_theme=True)
    
    # ----------------------------------------------------
    # SLIDE 2: Agenda (Light Theme)
    # ----------------------------------------------------
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide2, LIGHT_GRAY)
    add_slide_header(slide2, "Presentation Agenda")
    
    col1_pts = [
        "1. Context & Concept: Human Development Index",
        "2. Problem Statement: Current limitations in policy estimation",
        "3. System Objectives: Project goals and capabilities",
        "4. Technology Stack: Tools used for development",
        "5. System Architecture: Components design & database setup"
    ]
    col2_pts = [
        "6. Machine Learning Workflow: Raw data to final inference",
        "7. Model Performance: Benchmarking and final selection",
        "8. Web Portal Implementation: Live features visual gallery",
        "9. Quality Assurance & System Verification",
        "10. Project Summary, Future Scope & Team details"
    ]
    add_bullet_points(slide2, col1_pts, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.5), font_size=15)
    add_bullet_points(slide2, col2_pts, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.5), font_size=15)
    
    # ----------------------------------------------------
    # SLIDE 3: Context: What is HDI?
    # ----------------------------------------------------
    slide3 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide3, LIGHT_GRAY)
    add_slide_header(slide3, "Socioeconomic Context: What is HDI?")
    
    hdi_points = [
        "• Human Development Index (HDI) is a UN standard formulation for evaluating progress.",
        "• Dimensions measured by HDI:",
        "  - Healthy Life: Life expectancy at birth (target bounds: 20 to 100 years).",
        "  - Education: Expected years of schooling & Mean years of schooling.",
        "  - Standard of Living: Gross National Income (GNI) per Capita (PPP $).",
        "• HDI is a geometric mean of these normalized dimension indices.",
        "• Importance of predicting HDI:",
        "  - Policy Tuning: Allows simulating socioeconomic impact before funding programs.",
        "  - Resource Allocation: Guides healthcare budgets, school expansions, and job initiatives."
    ]
    add_bullet_points(slide3, hdi_points, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0), font_size=15)
    
    # ----------------------------------------------------
    # SLIDE 4: Problem Statement
    # ----------------------------------------------------
    slide4 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide4, LIGHT_GRAY)
    add_slide_header(slide4, "Problem Statement: Policy Simulation Limitations")
    
    ps_points = [
        "• Difficulty in analyzing development indicators manually:",
        "  - Complex calculations involve non-linear log transformations and geometric scales.",
        "• Retrospective Limitations of Existing Databases:",
        "  - Standard dashboards (UNDP databases) serve historical indicators but lack future simulations.",
        "• No local Explainable AI (XAI) mapping:",
        "  - Users see scores but cannot inspect which indicator has the largest impact on outcomes.",
        "• Decision Obstacles in Public Policy:",
        "  - Governments need objective, data-driven validation to allocate development funds.",
        "• Proposed AI Platform Solution:",
        "  - A portal where sliders simulate parameters, yielding predictions, explainable weights, and policy advice instantly."
    ]
    add_bullet_points(slide4, ps_points, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0), font_size=15)
    
    # ----------------------------------------------------
    # SLIDE 5: Project Objectives
    # ----------------------------------------------------
    slide5 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide5, LIGHT_GRAY)
    add_slide_header(slide5, "Project Objectives")
    
    obj_points = [
        "• High Inference Accuracy: Target >95% accuracy in classifying HDI category.",
        "• Companion Regression Model: Incorporate continuous scoring to estimate index value (0.000 to 1.000).",
        "• Expose Explainable AI: Formulate and plot local parameter contributions for trust and safety.",
        "• Policy Advice Generator: Program an advisor that compares inputs with world medians, highlighting focus investments.",
        "• Data Persistence Logging: Map SQLite schemas to save prediction histories securely.",
        "• Client-Ready Reporting: Render downloadable PDF summary reports on-the-fly."
    ]
    add_bullet_points(slide5, obj_points, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0), font_size=15)
    
    # ----------------------------------------------------
    # SLIDE 6: Tech Stack
    # ----------------------------------------------------
    slide6 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide6, LIGHT_GRAY)
    add_slide_header(slide6, "System Technology Stack")
    
    # Add Table
    tbl = add_table(slide6, 6, 3, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.5))
    headers = ["Layer", "Technology", "Primary Role & Application"]
    for c, h in enumerate(headers):
        format_table_cell(tbl.cell(0, c), h, bold=True, font_size=13, text_color=WHITE, bg_color=NAVY)
        
    stack_data = [
        ["Programming Language", "Python 3.11", "Back-end scripts, model processing, database logic, PDF compiler"],
        ["Backend Web", "Flask Framework", "HTTP routing, input validation filters, REST APIs, JSON outputs"],
        ["Machine Learning", "Scikit-Learn (SVM / Random Forest)", "Model training, pipeline benchmarks, model loading (.joblib)"],
        ["Database Layer", "SQLite3 Engine", "Persistent database tables logging prediction logs"],
        ["Frontend UI Portal", "HTML5, CSS3, ES6 Javascript, Chart.js", "Responsive layout grids, light/dark mode variables, dynamic log charts"]
    ]
    for r, row in enumerate(stack_data):
        bg = WHITE if r % 2 == 0 else LIGHT_GRAY
        for c, val in enumerate(row):
            format_table_cell(tbl.cell(r+1, c), val, bold=(c==0), font_size=11, text_color=DARK_GRAY, bg_color=bg)
            
    # ----------------------------------------------------
    # SLIDE 7: System Architecture
    # ----------------------------------------------------
    slide7 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide7, LIGHT_GRAY)
    add_slide_header(slide7, "System Architecture Mapping")
    
    arch_points = [
        "• Architectural Paradigm: Model-View-Controller (MVC) data separation.",
        "• Request Flow Path:",
        "  - 1. User Interface (Client): Sliders record socioeconomic parameters.",
        "  - 2. Flask Router (Backend API): Receives variables, runs input boundaries checks.",
        "  - 3. Machine Learning (Inference): Scaler transforms inputs; SVM Classifies class; RF Regresses continuous score.",
        "  - 4. Explainable AI & Advisor: Local weight logs mapped; Policy rules evaluated against world medians.",
        "  - 5. Database Logging: SQLite logs the run parameters dynamically.",
        "  - 6. View Render: JSON returned to update frontend gauges, charts, and recommendations.",
        "• Report Generation Engine: Backend reportlab module compiles the summary PDF on-the-fly."
    ]
    add_bullet_points(slide7, arch_points, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0), font_size=15)
    
    # ----------------------------------------------------
    # SLIDE 8: ML Workflow Pipeline
    # ----------------------------------------------------
    slide8 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide8, LIGHT_GRAY)
    add_slide_header(slide8, "Machine Learning Workflow Pipeline")
    
    workflow_pts = [
        "• 1. Dataset Collection: Global UNDP human development indicators dataset.",
        "• 2. Preprocessing & Cleaning:",
        "  - Remove duplicate rows.",
        "  - Missing value imputation: Fill missing variables using country medians first, then global medians.",
        "  - Outlier detection: Evaluated using Interquartile Range (IQR) methods.",
        "• 3. Feature Engineering:",
        "  - Log transform applied to Gross National Income (GNI) per capita (PPP $) to align scales.",
        "  - Feature centering & scaling using StandardScaler.",
        "• 4. Benchmarking Model Suite: Split 75% train, 25% test; evaluated 5 classifiers.",
        "• 5. Model Deployment: Best classifier (SVM) and companion RF Regressor compiled as joblib binaries."
    ]
    add_bullet_points(slide8, workflow_pts, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0), font_size=15)
    
    # ----------------------------------------------------
    # SLIDE 9: Model Benchmarking
    # ----------------------------------------------------
    slide9 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide9, LIGHT_GRAY)
    add_slide_header(slide9, "Model Benchmarking Results")
    
    # Table layout
    tbl_bench = add_table(slide9, 6, 6, Inches(0.8), Inches(1.8), Inches(11.733), Inches(3.8))
    headers_bench = ["Algorithm", "Test Accuracy", "Weighted Precision", "Weighted Recall", "Weighted F1", "Train Time (s)"]
    for c, h in enumerate(headers_bench):
        format_table_cell(tbl_bench.cell(0, c), h, bold=True, font_size=11, text_color=WHITE, bg_color=NAVY)
        
    bench_data = [
        ["Support Vector Machine", "98.9%", "99.0%", "98.9%", "98.9%", "0.050s"],
        ["Logistic Regression", "98.1%", "98.1%", "98.1%", "98.1%", "0.014s"],
        ["Random Forest", "97.5%", "97.5%", "97.5%", "97.5%", "0.144s"],
        ["K-Nearest Neighbors", "96.2%", "96.2%", "96.2%", "96.2%", "0.002s"],
        ["Decision Tree", "95.6%", "95.7%", "95.6%", "95.6%", "0.003s"]
    ]
    for r, row in enumerate(bench_data):
        bg = WHITE if r % 2 == 0 else LIGHT_GRAY
        is_best = (r == 0) # SVM is best
        text_col = NAVY if is_best else DARK_GRAY
        for c, val in enumerate(row):
            cell = tbl_bench.cell(r+1, c)
            format_table_cell(cell, val, bold=is_best, font_size=10, text_color=text_col, bg_color=bg)
            
    notes = [
        "• SVM achieves peak test accuracy of 98.9% and has a very compact file size (27.0 KB) compared to Random Forest (1,026.0 KB).",
        "• Training time and prediction latency benchmarks are minimal (all under 15ms), facilitating real-time response.",
        "• Companion Regressor: Deployed Random Forest Regressor for continuous scores (R-squared: 0.992)."
    ]
    add_bullet_points(slide9, notes, Inches(0.8), Inches(5.8), Inches(11.733), Inches(1.5), font_size=13)
    
    # ----------------------------------------------------
    # SLIDE 10: Selected Model details
    # ----------------------------------------------------
    slide10 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide10, LIGHT_GRAY)
    add_slide_header(slide10, "Selected Classifier Details: SVM")
    
    svm_pts = [
        "• Algorithm Details: Support Vector Classifier (SVC) with Radial Basis Function (RBF) kernel.",
        "• Confusion Matrix Breakdown on Test Set (476 records total):",
        "  - Low Class: 105 actual records | 105 predicted correctly (100% accuracy)",
        "  - Medium Class: 96 actual records | 93 predicted correctly (3 errors, misclassified as Low/High)",
        "  - High Class: 71 actual records | 69 predicted correctly (2 errors, misclassified as Medium/Very High)",
        "  - Very High Class: 204 actual records | 204 predicted correctly (100% accuracy)",
        "• Evaluation Synthesis:",
        "  - SVM demonstrates high separating boundaries on edge threshold values.",
        "  - Outliers show zero impact due to log-scaling of GNI and robust standardized scaling."
    ]
    add_bullet_points(slide10, svm_pts, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0), font_size=15)
    
    # ----------------------------------------------------
    # SLIDE 11: Core Features - 1
    # ----------------------------------------------------
    slide11 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide11, LIGHT_GRAY)
    add_slide_header(slide11, "Core Platform Features: Prediction & XAI")
    
    f1_pts = [
        "• Real-time Predictive Simulator:",
        "  - Responsive sliders capturing variables in natural units.",
        "  - Validations ensure out-of-bounds parameters are rejected.",
        "• Dual Prediction Output:",
        "  - Category: Deployed SVM classifier outputs Low, Medium, High, or Very High.",
        "  - Score: Deployed companion RF Regressor outputs continuous estimation (e.g. 0.785).",
        "• Interactive Confidence Gauge:",
        "  - Dial displays SVM probability confidence (0 - 100%) dynamically.",
        "• Local Explainable AI (XAI):",
        "  - Extracts and displays model feature contribution vectors, illustrating which socioeconomic indicator drove the prediction."
    ]
    add_bullet_points(slide11, f1_pts, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0), font_size=15)
    
    # ----------------------------------------------------
    # SLIDE 12: Core Features - 2
    # ----------------------------------------------------
    slide12 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide12, LIGHT_GRAY)
    add_slide_header(slide12, "Core Features: Policy Advisor & Country Compare")
    
    f2_pts = [
        "• Intelligent Development Advisor Recommendations:",
        "  - Dynamic rules parser matches user indicators against global medians.",
        "  - Recommends actionable reforms (e.g., healthcare funding if Life Expectancy is below 72.0 years).",
        "• Side-by-Side Country Comparison:",
        "  - Dropdown containing list of real-world countries.",
        "  - Select any nation to overlay your custom profile against their official UNDP benchmarks.",
        "• Trend Analytics Dashboard:",
        "  - Displays aggregate graphs: prediction categories distribution, history logs trends over time.",
        "• Sample Predictions Profile Templates:",
        "  - Preloads geographic profiles (Nordic region, Sub-Saharan Africa, East Asia) for quick simulator testing."
    ]
    add_bullet_points(slide12, f2_pts, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0), font_size=15)
    
    # ----------------------------------------------------
    # SLIDE 13: Core Features - 3
    # ----------------------------------------------------
    slide13 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide13, LIGHT_GRAY)
    add_slide_header(slide13, "Core Features: Exports & Style Themes")
    
    f3_pts = [
        "• Historical Simulation Log Database:",
        "  - Persistent SQLite table writes all simulator runs.",
        "  - Main interface lists recent runs, enabling easy review, search, or deletion.",
        "• Dynamic ReportLab PDF Exports:",
        "  - Single-click PDF generator compiles structured reports on the server side.",
        "  - Includes indicators, prediction outcomes, confidence score, XAI weights, and policy advice.",
        "• Local CSV Exporter:",
        "  - Allows exporting full historical simulation database tables to standard CSV format.",
        "• Light & Dark Theme Support:",
        "  - Seamless CSS variables implementation for modern night-time interface styling."
    ]
    add_bullet_points(slide13, f3_pts, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0), font_size=15)
    
    # ----------------------------------------------------
    # SLIDE 14: Screenshots Layout
    # ----------------------------------------------------
    slide14 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide14, LIGHT_GRAY)
    add_slide_header(slide14, "Interface Walkthrough & Screenshots")
    
    # Place placeholders for screens
    scr_pts = [
        "• A full gallery of screenshots is saved in the /Screenshots directory of the workspace.",
        "• Main Interface Areas:",
        "  - Home Dashboard View: Logs aggregate counts, recent runs list, and theme settings.",
        "  - Predict Simulator: Vertical/horizontal range sliders, Dial gauge, and XAI weights.",
        "  - Country Comparison: Selected benchmark overlays showing index indicator gaps.",
        "  - Model Performance: Displays comparative tables, latency scales, and confusion matrices.",
        "• All screens support responsive styling layouts adapting to tablet, mobile, and desktop views.",
        "• Dark Mode styling renders high-contrast teal indicators on charcoal backgrounds, ensuring visual comfort."
    ]
    add_bullet_points(slide14, scr_pts, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0), font_size=15)
    
    # ----------------------------------------------------
    # SLIDE 15: Quality Assurance & Testing
    # ----------------------------------------------------
    slide15 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide15, LIGHT_GRAY)
    add_slide_header(slide15, "Quality Assurance & Testing Framework")
    
    # Table layout for test cases
    tbl_tc = add_table(slide15, 6, 4, Inches(0.8), Inches(1.8), Inches(11.733), Inches(3.5))
    headers_tc = ["ID", "Test Case Description", "Expected Behavior / Result", "Status"]
    for c, h in enumerate(headers_tc):
        format_table_cell(tbl_tc.cell(0, c), h, bold=True, font_size=12, text_color=WHITE, bg_color=NAVY)
        
    tc_data = [
        ["TC-001", "Home rendering (GET /)", "HTTP 200, HTML page with layout form renders", "PASS"],
        ["TC-002", "Prediction success (POST /predict)", "HTTP 200, returns prediction and confidence variables", "PASS"],
        ["TC-003", "Validation limits Min (slider edge)", "Life: 20.0 (Min edge) results in class 'Low'", "PASS"],
        ["TC-004", "Validation limits Max (slider edge)", "Life: 100.0 (Max edge) results in class 'Very High'", "PASS"],
        ["TC-005", "Validation boundaries reject (out-of-bounds)", "Life: 15.0 (below Min limit) rejected with HTTP 400", "PASS"]
    ]
    for r, row in enumerate(tc_data):
        bg = WHITE if r % 2 == 0 else LIGHT_GRAY
        for c, val in enumerate(row):
            cell = tbl_tc.cell(r+1, c)
            text_col = TEAL if c == 3 else DARK_GRAY
            format_table_cell(cell, val, bold=(c==3), font_size=10, text_color=text_col, bg_color=bg)
            
    test_notes = [
        "• Testing Strategy: Implemented standard unit tests using Python's unittest module, verifying server route logic.",
        "• Boundary Testing: Simulator checks extrema limits (Min & Max slider boundaries) to ensure safe model inputs.",
        "• Regression Testing: Automated assertions check JSON schemas of API outputs."
    ]
    add_bullet_points(slide15, test_notes, Inches(0.8), Inches(5.6), Inches(11.733), Inches(1.5), font_size=13)
    
    # ----------------------------------------------------
    # SLIDE 16: Future Scope
    # ----------------------------------------------------
    slide16 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide16, LIGHT_GRAY)
    add_slide_header(slide16, "Future Enhancements Roadmap")
    
    fs_points = [
        "• 1. Dynamic Geographic Mapping:",
        "  - Implement Leaflet.js or D3.js to render color-coded world maps dynamically mapping simulated indicators.",
        "• 2. Time-Series Forecasting Modules:",
        "  - Add LSTM or ARIMA forecasting libraries to predict future HDI indicator paths over a 10-year period.",
        "• 3. Advanced Explainable AI (XAI) integration:",
        "  - Incorporate SHAP and LIME library diagnostics to output fine-grained visual feature contribution plots.",
        "• 4. User Security & Dashboards:",
        "  - Implement user authentication, role-based access, and cloud database storage.",
        "• 5. Policy Formulation AI Chatbot:",
        "  - Integrate a lightweight LLM chat bot to discuss custom country development plans dynamically."
    ]
    add_bullet_points(slide16, fs_points, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0), font_size=15)
    
    # ----------------------------------------------------
    # SLIDE 17: Team Details
    # ----------------------------------------------------
    slide17 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide17, LIGHT_GRAY)
    add_slide_header(slide17, "Project Team Roles & Contributions")
    
    # Table layout
    tbl_team = add_table(slide17, 6, 3, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.5))
    headers_team = ["Member Name", "Project Role", "Core Responsibilities"]
    for c, h in enumerate(headers_team):
        format_table_cell(tbl_team.cell(0, c), h, bold=True, font_size=12, text_color=WHITE, bg_color=NAVY)
        
    team_rows = [
        ["Varigeti Karthikeya", "Team Lead & Backend Lead", "Project scheduling, Flask route handlers, database integration, API controller logic."],
        ["Veera Ajay Kumar Adapa", "Machine Learning Engineer", "Preprocessing scripts, model benchmarking, tuning SVM & companion RF, saving binaries."],
        ["Gulla Chandana", "Frontend Designer", "Interactive UI layout, Light/Dark mode stylesheet variables, Chart.js implementation."],
        ["Ambati Krupa Jesudas", "QA & Test Engineer", "Unit tests creation, edge cases validation, UAT checklist design, test executions."],
        ["Mohammad Tayyab", "Technical Writer & DevOps", "Programmatic PDF reporting module, installation guides, user manuals, deployment."]
    ]
    for r, row in enumerate(team_rows):
        bg = WHITE if r % 2 == 0 else LIGHT_GRAY
        for c, val in enumerate(row):
            cell = tbl_team.cell(r+1, c)
            format_table_cell(cell, val, bold=(c==0), font_size=10, text_color=DARK_GRAY, bg_color=bg)
            
    # ----------------------------------------------------
    # SLIDE 18: Summary & Conclusion (Dark Navy)
    # ----------------------------------------------------
    slide18 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide18, NAVY)
    add_slide_header(slide18, "Summary & Conclusion", dark_theme=True)
    
    conc_pts = [
        "• Successful Platform Integration:",
        "  - Deployed a portfolio-ready web analytics portal matching standard UN HDI dimensions.",
        "• High Inference Accuracy:",
        "  - Deployed Support Vector Machine (SVM) achieving peak accuracy of 98.9% on test set.",
        "• Dual Analytical Scope:",
        "  - Companion Random Forest Regressor provides continuous index scores complementing categories.",
        "• User-Driven Value System:",
        "  - Explainable AI and dynamic policy advisor recommendations bridge the gap between ML outputs and user action.",
        "• Technical Viability:",
        "  - System is lightweight, fully tested (100% pass rates), and scalable for future development roadmap."
    ]
    add_bullet_points(slide18, conc_pts, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0), font_size=15, dark_theme=True)
    
    # ----------------------------------------------------
    # SLIDE 19: Thank You / Q&A Slide (Dark Navy)
    # ----------------------------------------------------
    slide19 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide19, NAVY)
    
    # Center text box
    ty_box = slide19.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.333), Inches(3.0))
    tf_ty = ty_box.text_frame
    tf_ty.word_wrap = True
    p_ty = tf_ty.paragraphs[0]
    p_ty.alignment = PP_ALIGN.CENTER
    p_ty.text = "THANK YOU!"
    p_ty.font.name = 'Helvetica'
    p_ty.font.bold = True
    p_ty.font.size = Pt(64)
    p_ty.font.color.rgb = WHITE
    
    p_qa = tf_ty.add_paragraph()
    p_qa.alignment = PP_ALIGN.CENTER
    p_qa.text = "Questions & Answers Session"
    p_qa.font.name = 'Helvetica'
    p_qa.font.size = Pt(24)
    p_qa.font.color.rgb = TEAL
    p_qa.space_before = Pt(12)
    
    p_lnk = tf_ty.add_paragraph()
    p_lnk.alignment = PP_ALIGN.CENTER
    p_lnk.text = "GitHub Repository: https://github.com/pandu0426/HDI-Insights"
    p_lnk.font.name = 'Helvetica'
    p_lnk.font.size = Pt(14)
    p_lnk.font.color.rgb = WHITE
    p_lnk.space_before = Pt(36)
    
    prs.save("07_Project_Documentation/Project_Presentation.pptx")
    print("Project_Presentation.pptx built successfully.")

if __name__ == "__main__":
    build_presentation()
