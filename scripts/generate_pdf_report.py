#!/usr/bin/env python3
"""
BingeBear Executive CMO PDF Generator
Generates a beautiful, board-ready PDF report of BingeBear's marketing health.
"""
import sys
import json
from datetime import datetime
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.colors import HexColor, white
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
except ImportError:
    print("Please run: pip install reportlab")
    sys.exit(1)

def generate_report(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle("Title", parent=styles["Title"], fontSize=24, textColor=HexColor("#FF6B35"))
    h2_style = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=16, textColor=HexColor("#1B2A4A"))
    body = styles["Normal"]
    
    elements =[]
    
    # Title
    elements.append(Paragraph("BingeBear.tv - CMO Growth Audit", title_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d')}", body))
    elements.append(Spacer(1, 30))
    
    # Executive Summary (Hardcoded to your bottleneck)
    elements.append(Paragraph("Executive Summary: The €250 Lifetime Push", h2_style))
    elements.append(Paragraph("Data shows a Trial-to-Paid rate of 19.4% (Excellent). However, 28 out of 30 leads drop off during the TV Setup phase. Fixing this WhatsApp setup process is our #1 revenue priority this week.", body))
    elements.append(Spacer(1, 20))
    
    # Action Plan
    elements.append(Paragraph("Immediate Action Plan (Next 48 Hours)", h2_style))
    actions =[
        "1. Send a text-only WhatsApp to the 264 leads stuck in 'Nurture' offering Setup help.",
        "2. Launch FB Ads targeting GAA/Rugby fans anchoring the €250 Lifetime against Sky TV.",
        "3. Offer a €150/€100 Split Pay Lifetime upgrade to the 28 active paying users."
    ]
    for action in actions:
        elements.append(Paragraph(action, body))
        elements.append(Spacer(1, 10))

    doc.build(elements)
    print(f"Success! PDF Report generated at: {output_path}")

if __name__ == "__main__":
    generate_report("BINGEBEAR_CMO_REPORT.pdf")
