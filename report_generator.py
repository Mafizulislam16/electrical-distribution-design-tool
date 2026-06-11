from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
import time


def header(canvas, doc):
    canvas.saveState()
    width, height = doc.pagesize

    # Logo
    logo_path = os.path.join("assets", "logo.png")
    try:
        from reportlab.lib.utils import ImageReader
        logo = ImageReader(logo_path)
        canvas.drawImage(logo, 40, height - 90, width=70, height=40, mask="auto")
    except:
        pass

    # Title
    canvas.setFont("Helvetica-Bold", 16)
    canvas.setFillColor(colors.HexColor("#1f4e79"))
    canvas.drawCentredString(width / 2, height - 70, "Voltage Drop Analysis Report")
    
    # Line
    canvas.setStrokeColor(colors.HexColor("#1f4e79"))
    canvas.line(40, height - 105, width - 40, height - 105)
    
    canvas.restoreState()


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(doc.pagesize[0] - 40, 20, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def generate_pdf(results):
        # Fixed filename + cleanup old files
    file_name = "Voltage_Drop_Report.pdf"
    
    # Delete old timestamped reports
    import glob
    for old_file in glob.glob("Voltage_Drop_Report_*.pdf"):
        try:
            if old_file != file_name:
                os.remove(old_file)
                print(f"🗑️ Deleted old report: {old_file}")
        except:
            pass
    
    doc = SimpleDocTemplate(
        file_name,
        rightMargin=40,
        leftMargin=40,
        topMargin=120,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    elements = []

    # ==================== COVER PAGE ====================
    elements.append(Paragraph("Voltage Drop Calculation Report", styles["Title"]))
    elements.append(Spacer(1, 40))

    for key, value in [
        ("Project", results.get('project_name', 'N/A')),
        ("Project Number", results.get('project_number', 'N/A')),
        ("Client", results.get('client', 'N/A')),
        ("Engineer", results.get('engineer', 'N/A')),
        ("Date", results.get('date', 'N/A'))
    ]:
        elements.append(Paragraph(f"<b>{key}:</b> {value}", 
                                styles["Heading2"] if key == "Project" else styles["BodyText"]))

    elements.append(PageBreak())

    # ==================== CALCULATION SUMMARY ====================
    elements.append(Paragraph("Calculation Summary", styles["Heading1"]))
    
    status_color = colors.lightgreen if results.get('vd_percent', 0) <= 5 else colors.pink

    summary_data = [
        ["PROJECT STATUS"],
        [f"Voltage Drop: {results.get('vd_percent', 0):.2f}%"],
        ["IEC Limit: 5.00%"],
        [f"Overall Result: {results.get('status', 'N/A')}"],
        [f"Recommended Cable: {results.get('cable', 'N/A')} mm²"],
        [f"Recommended Breaker: {results.get('breaker', 'N/A')} A"],
        [""],
        ["TRANSFORMER ANALYSIS"],
        [f"Calculated Load: {results.get('kva', 0):.2f} kVA"],
        [f"Design Load (25% margin): {results.get('kva_design', 0):.2f} kVA"],
        [f"Selected Transformer: {results.get('transformer_size', 0)} kVA"],
        [f"Transformer Loading: {results.get('transformer_loading', 0):.1f}%"],
        [f"Loading Status: {results.get('loading_status', 'N/A')}"]
    ]

    summary_table = Table(summary_data, colWidths=[320])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (0, 5), status_color),
        ("BACKGROUND", (0, 7), (0, -1), colors.HexColor("#1f4e79")),
        ("TEXTCOLOR", (0, 7), (0, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 7), (0, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(summary_table)

    elements.append(Spacer(1, 20))

    # ==================== DETAILED PARAMETERS TABLE (with better styling) ====================
    normal_style = styles["Normal"]
    normal_style.fontSize = 9
    normal_style.leading = 11

    data = [
        ["Parameter", "Value"],
        ["Power (kW)", f"{results.get('power', 0)}"],
        ["Voltage (V)", f"{results.get('voltage', 0)}"],
        ["Power Factor", f"{results.get('pf', 0)}"],
        ["Length (m)", f"{results.get('length', 0)}"],
        ["Phase", results.get("phase", "N/A")],
        ["Cable Material", results.get("material", "N/A")],
        ["Installation Method", results.get("installation", "N/A")],
        ["Current (A)", f"{results.get('current', 0):.2f}"],
        ["Voltage Drop (V)", f"{results.get('vd', 0):.2f}"],
        ["Voltage Drop (%)", f"{results.get('vd_percent', 0):.2f}%"],
        ["Recommended Cable", f"{results.get('cable', 'N/A')} mm²"],
        ["Recommended Breaker", f"{results.get('breaker', 'N/A')} A"],
        ["Status", results.get("status", "N/A")],
        ["Design Check", Paragraph(str(results.get("design_check", "N/A")), normal_style)]
    ]

    table = Table(data, colWidths=[220, 280], repeatRows=1)

    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        # Body
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("ALIGN", (1, 0), (1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),

        # Alternating rows
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),

        # Design Check row specific styling
        ("FONTSIZE", (1, -1), (1, -1), 9),
        ("LEADING", (1, -1), (1, -1), 11),
    ]))
    elements.append(table)

        # ==================== GAUGE CHART ====================
    elements.append(PageBreak())
    elements.append(Paragraph("Voltage Drop Compliance Gauge", styles["Heading1"]))
    
    gauge_file = "voltage_drop_gauge.png"
    if os.path.exists(gauge_file):
        elements.append(Spacer(1, 15))
        elements.append(Image(gauge_file, width=450, height=320))  # Balanced size
    else:
        elements.append(Paragraph("Gauge image not found.\nPlease click 'Create Chart' first.", styles["BodyText"]))

    # ==================== RECOMMENDATION ====================
    elements.append(PageBreak())
    elements.append(Paragraph("Engineering Recommendation", styles["Heading1"]))

    vd = results.get('vd_percent', 0)
    if vd <= 3:
        rec = "Excellent design margin available. Voltage drop is significantly below IEC limit."
    elif vd <= 5:
        rec = "Design is compliant with IEC recommendations. No corrective action required."
    else:
        rec = "Voltage drop exceeds IEC recommendation. Consider increasing cable size or reducing length."

    elements.append(Paragraph(rec, styles["BodyText"]))

    # ==================== ENGINEERING CALCULATIONS ====================
    elements.append(PageBreak())
    elements.append(Paragraph("Engineering Calculations", styles["Heading1"]))

    calc_text = f"""
    <b>Current Calculation</b><br/><br/>
    Formula: I = P × 1000 / (√3 × V × PF)<br/><br/>
    Substitution: I = {results.get('power', 0)} × 1000 / (√3 × {results.get('voltage', 0)} × {results.get('pf', 0)})<br/><br/>
    Result: I = {results.get('current', 0):.2f} A

    <br/><br/><b>Voltage Drop Calculation</b><br/><br/>
    Formula: VD = 1.732 × I × R × L / 1000<br/><br/>
    Result: VD = {results.get('vd', 0):.2f} V<br/><br/>
    Voltage Drop Percentage: {results.get('vd_percent', 0):.2f}%
    """

    elements.append(Paragraph(calc_text, styles["BodyText"]))

    # ==================== ENGINEERING NOTES ====================
    elements.append(PageBreak())
    elements.append(Paragraph("Engineering Notes", styles["Heading1"]))

    notes = """
    • Voltage drop should normally be less than 5% for main circuits.<br/>
    • Cable sizing recommendation is indicative only.<br/>
    • Final cable sizing shall be verified according to full IEC standards.<br/>
    • Installation method, ambient temperature and grouping factors must be checked.<br/>
    • Final design approval remains the responsibility of the engineer.
    """
    elements.append(Paragraph(notes, styles["BodyText"]))

    # ==================== BUILD PDF ====================
    doc.build(
        elements,
        onFirstPage=header,
        onLaterPages=footer
    )

    return os.path.abspath(file_name)