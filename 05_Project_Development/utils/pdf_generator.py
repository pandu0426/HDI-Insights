import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(data):
    """
    Generates a professional PDF report for the HDI prediction results.
    data format:
    {
        'country': str,
        'timestamp': str,
        'inputs': {
            'Life_Expectancy': float,
            'Expected_Schooling': float,
            'Mean_Schooling': float,
            'GNI_Per_Capita': float
        },
        'prediction': float,  # Estimated HDI Score
        'category': str,  # Predicted HDI Category
        'confidence': float,  # Confidence %
        'explanation': str,  # Plain text explanation
        'recommendations': list of str,
        'feature_importance': dict of {feature: importance_value}
    }
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Styles for Premium Look
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1e3a8a'), # Deep Navy
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#4b5563'), # Gray
        spaceAfter=15
    )
    
    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0f766e'), # Teal
        spaceBefore=15,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=6
    )
    
    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        alignment=1, # Center
        textColor=colors.white
    )
    
    story = []
    
    # Header Banner
    story.append(Paragraph("HDI INSIGHT AI", title_style))
    story.append(Paragraph(f"Human Development Analytics Platform • Prediction Report • Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subtitle_style))
    story.append(Spacer(1, 10))
    
    # Horizontal rule
    story.append(Table([['']], colWidths=[532], rowHeights=[2], style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#3b82f6')), # Blue Line
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0)
    ])))
    story.append(Spacer(1, 15))
    
    # Summary Table Section
    country_name = data.get('country') or 'Custom Socioeconomic Profile'
    hdi_score = data.get('prediction', 0.0)
    category = data.get('category', 'Unknown')
    confidence = data.get('confidence', 0.0)
    
    # Determine Category Color
    bg_color = '#ef4444' # Low (Red)
    if category == 'Very High':
        bg_color = '#0072ff' # Blue
    elif category == 'High':
        bg_color = '#10b981' # Green
    elif category == 'Medium':
        bg_color = '#f59e0b' # Orange
        
    summary_data = [
        [Paragraph(f"<b>Target Subject:</b> {country_name}", body_style), Paragraph(f"<b>Estimated HDI Score:</b> {hdi_score:.3f}", body_style)],
        [Paragraph(f"<b>Prediction Confidence:</b> {confidence:.1f}%", body_style), Table([[Paragraph(category, badge_style)]], colWidths=[100], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))]
    ]
    
    summary_table = Table(summary_data, colWidths=[266, 266])
    summary_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 15))
    
    # Inputs Details Table
    story.append(Paragraph("Socioeconomic Indicators Profile", h2_style))
    inputs = data.get('inputs', {})
    
    indicators_data = [
        ["Indicator Name", "Value", "Benchmark/Unit"],
        ["Life Expectancy at Birth", f"{inputs.get('Life_Expectancy', 0.0):.1f}", "Years"],
        ["Expected Years of Schooling", f"{inputs.get('Expected_Schooling', 0.0):.1f}", "Years"],
        ["Mean Years of Schooling", f"{inputs.get('Mean_Schooling', 0.0):.1f}", "Years"],
        ["GNI per Capita (PPP $)", f"${inputs.get('GNI_Per_Capita', 0.0):,.2f}", "USD"],
    ]
    
    ind_table = Table(indicators_data, colWidths=[220, 120, 192])
    ind_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#374151')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 9),
    ]))
    story.append(ind_table)
    story.append(Spacer(1, 15))
    
    # Explainable AI Details
    story.append(Paragraph("Model Prediction Rationale (XAI)", h2_style))
    story.append(Paragraph(data.get('explanation', ''), body_style))
    story.append(Spacer(1, 10))
    
    # Feature Importance table
    feat_data = [["Feature Name", "Model Weight (Importance %)", "Bar"]]
    imp = data.get('feature_importance', {})
    
    # Normalizing weights to percent
    tot = sum(imp.values()) if sum(imp.values()) > 0 else 1.0
    for feat, val in sorted(imp.items(), key=lambda x: x[1], reverse=True):
        pct = (val / tot) * 100
        # Draw inline bar representation
        bar_len = int(pct * 1.5) # Scale factor for visual width
        bar_text = "█" * (bar_len // 10)
        feat_data.append([feat.replace('_', ' '), f"{pct:.1f}%", bar_text])
        
    feat_table = Table(feat_data, colWidths=[200, 150, 182])
    feat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f3f4f6')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('TEXTCOLOR', (2,1), (2,-1), colors.HexColor('#3b82f6')),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(feat_table)
    story.append(Spacer(1, 15))
    
    # Recommendations (Development Advisor)
    story.append(Paragraph("Intelligent Advisor Recommendations", h2_style))
    recs = data.get('recommendations', [])
    for rec in recs:
        story.append(Paragraph(f"• {rec}", body_style))
        
    story.append(Spacer(1, 25))
    story.append(Table([['']], colWidths=[532], rowHeights=[0.5], style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#d1d5db')),
    ])))
    story.append(Spacer(1, 8))
    
    # Disclaimer
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#9ca3af'),
        alignment=1
    )
    story.append(Paragraph("This document is an AI-generated analysis based on standard UNDP indicators. It is intended for educational, research, and analysis portfolios and does not constitute official United Nations declarations.", disclaimer_style))
    
    # Build Document
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
