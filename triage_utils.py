import streamlit as st
import json
from fuzzywuzzy import fuzz

def display_sar(sar):
    st.subheader("📄 SAR Background")
    st.markdown(f"**Reporting Entity:** {sar['reporting_entity']}")
    st.markdown(f"**Submission Date:** {sar['submission_date']}")
    st.markdown(f"**Internal Reference:** {sar['internal_ref']}")
    st.info(sar["background"])

    st.divider()
    st.subheader("🏷️ Subjects & KYC")
    for subject in sar["subjects"]:
        with st.expander(subject["name"]):
            for k, v in subject.items():
                if k != "name":
                    st.markdown(f"**{k.replace('_', ' ').title()}:** {v}")
            st.caption("⚠️ All names and data are fictitious and for training purposes only.")

    st.divider()
    st.subheader("💸 Transactions")
    if sar["transactions"]:
        for tx in sar["transactions"]:
            st.markdown(f"- **{tx['date']}** | {tx['type']} | {tx['amount']} {tx['currency']} | {tx.get('origin', '') or tx.get('destination', '')}")
    else:
        st.write("No transactions recorded.")

    st.divider()
    st.subheader("📤 Additional Info")
    if st.button("Request Additional Info"):
        st.session_state.additional_info_revealed = True

    if st.session_state.get("additional_info_revealed"):
        st.success(sar.get("additional_info_response", "No additional information available."))

def red_flag_picker(sar):
    with open("red_flags.json", "r", encoding="utf-8") as f:
        red_flag_list = json.load(f)

    selected = st.multiselect("Select the red flags you believe apply:", red_flag_list, key=sar["id"])
    st.session_state.red_flag_choices[sar["id"]] = selected

def process_decision(sar):
    st.subheader("📌 Final Decision")
    decision = st.selectbox("What action should be taken?", ["Forward to Law Enforcement", "Close Case", "Dissemination Abroad"], key=sar["id"] + "_decision")

    if decision == "Dissemination Abroad":
        user_input = st.text_input("Enter the country to disseminate to:", key=sar["id"] + "_country")
    else:
        user_input = None

    if st.button("Submit Case to Head of Division", key=sar["id"] + "_submit"):
        st.session_state.decisions[sar["id"]] = {
            "decision": decision,
            "country": user_input
        }

        expected = sar["expected_decision"]
        correct = decision in expected

        missed = list(set(sar["red_flags"]) - set(st.session_state.red_flag_choices.get(sar["id"], [])))
        st.session_state.missed_flags[sar["id"]] = missed

        if decision == "Dissemination Abroad" and "Dissemination Abroad" in expected:
            correct_country = sar.get("dissemination_country", "").lower()
            score = fuzz.partial_ratio(correct_country, user_input.lower()) if user_input else 0
            if score >= 85:
                correct = True
            else:
                correct = False

        st.session_state.current_index += 1
        st.experimental_rerun()
