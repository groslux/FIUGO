
from fpdf import FPDF

def generate_certificate(name, decisions, red_flag_choices, missed_flags, sars, time_taken):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_title("AML Triage Certificate")

    pdf.cell(200, 10, txt="AML Case Triage Completion Certificate", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Officer: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Time Taken: {round(time_taken, 2)} minutes", ln=True)
    pdf.ln(5)

    for sar in sars:
        rid = sar['report_id']
        pdf.set_font("Arial", style="B", size=11)
        pdf.cell(200, 8, txt=f"{rid} - {sar['typology']}", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 6, txt=f"Background: {sar['background']}")
        pdf.cell(200, 6, txt=f"Your Decision: {decisions.get(rid)} | Expected: {sar['expected_action']}", ln=True)
        pdf.cell(200, 6, txt=f"Red Flags Missed: {', '.join(missed_flags.get(rid, [])) or 'None'}", ln=True)
        pdf.ln(3)

    pdf.ln(5)
    pdf.cell(200, 10, txt="Thank you for completing this FIU simulation.", ln=True)

    path = f"certificate_{name.replace(' ', '_')}.pdf"
    pdf.output(path)
    return path
