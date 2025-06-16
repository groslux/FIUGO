
import streamlit as st

def display_sar(sar):
    st.subheader("🧾 SAR Summary")
    st.markdown(f"**Typology:** {sar['typology']}")
    st.markdown(f"**Reported by:** {sar['reporter']}")
    st.markdown(f"**Background:** {sar['background']}")
    st.markdown(f"**Disclaimer:** {sar['disclaimer']}")

    with st.expander("👤 KYC Information"):
        for k, v in sar['subject'].items():
            st.markdown(f"**{k.replace('_',' ').title()}**: {v}")

    with st.expander("💸 Transactions"):
        for t in sar['transactions']:
            st.markdown(f"- {t['date']}: {t['amount']} {t['currency']} from {t['from']} to {t['to']}")

    with st.expander("🏢 Entities Involved"):
        for e in sar['entities']:
            st.markdown(f"- {e['type'].title()}: {e['name']} ({e['country']})")

    if sar.get("incomplete", False):
        st.warning("⚠️ This SAR appears incomplete. You may request more information.")
        if sar['additional_info_response']['status'] == "available":
            st.info(sar['additional_info_response']['details'])
        else:
            st.info(sar['additional_info_response']['message'])

def red_flag_picker(sar):
    with st.expander("🚩 Select Red Flags You Observed"):
        with open("red_flags.json", "r", encoding="utf-8") as f:
            red_flag_list = f.read().splitlines()
        selected = st.multiselect("Choose red flags:", red_flag_list, key=f"flags_{sar['report_id']}")
        st.session_state.red_flag_choices[sar['report_id']] = selected

def process_decision(sar):
    st.markdown("---")
    st.subheader("💡 What action do you take?")
    choice = st.radio("Choose: ", ["Forward to Law Enforcement", "Request More Info", "Close Case"], key=f"decision_{sar['report_id']}")
    st.session_state.decisions[sar['report_id']] = choice

    if st.button("✅ Submit Decision", key=f"submit_{sar['report_id']}"):
        correct = (choice == sar['expected_action'])
        if not correct:
            st.error(f"❌ Not optimal. Correct action was: {sar['expected_action']}")
        else:
            st.success("✅ Correct action taken.")
        correct_flags = set(sar.get("red_flags", []))
        selected_flags = set(st.session_state.red_flag_choices.get(sar['report_id'], []))
        missed = list(correct_flags - selected_flags)
        st.session_state.missed_flags[sar['report_id']] = missed
        st.session_state.current_index += 1
        st.experimental_rerun()
