from fpdf import FPDF
from datetime import datetime

def generate_certificate(name, decisions, red_flag_choices, missed_flags, sars, time_taken):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "AML Triage Training Certificate", ln=1, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Officer: {name}", ln=1)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=1)
    pdf.cell(0, 10, f"Time Spent: {round(time_taken, 2)} minutes", ln=1)

    correct = 0
    total = len(sars)

    pdf.ln(5)
    for sar in sars:
        sar_id = sar["id"]
        decision = decisions.get(sar_id, {}).get("decision", "N/A")
        country = decisions.get(sar_id, {}).get("country", "")
        expected = sar["expected_decision"]
        correct_decision = decision in expected

        red_flags_selected = red_flag_choices.get(sar_id, [])
        missed = missed_flags.get(sar_id, [])
        flag_score = len(missed) == 0

        if decision == "Dissemination Abroad" and "Dissemination Abroad" in expected:
            expected_country = sar.get("dissemination_country", "").lower()
            from fuzzywuzzy import fuzz
            score = fuzz.partial_ratio(expected_country, country.lower()) if country else 0
            correct_decision = score >= 85

        if correct_decision and flag_score:
            correct += 1

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Case: {sar_id}", ln=1)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 7, f"Background: {sar['background']}")
        pdf.cell(0, 7, f"Your Decision: {decision} {'('+country+')' if country else ''}", ln=1)
        pdf.cell(0, 7, f"Expected: {', '.join(expected)}", ln=1)
        if "dissemination_country" in sar:
            pdf.cell(0, 7, f"Expected Country: {sar['dissemination_country']}", ln=1)
        pdf.cell(0, 7, f"Selected Red Flags: {', '.join(red_flags_selected)}", ln=1)
        pdf.cell(0, 7, f"Missed Red Flags: {', '.join(missed)}", ln=1)
        pdf.ln(4)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Final Score: {correct} / {total} SARs correctly handled", ln=1)

    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, "\nRecommendation: Review typologies on red flag identification and appropriate dissemination. Great effort! Stay sharp, officer.")

    output_path = f"/mnt/data/AML_Certificate_{name.replace(' ', '_')}.pdf"
    pdf.output(output_path)
    return output_path
