import streamlit as st
import json
import random
import time
from session import init_session_state
from triage_utils import display_sar, red_flag_picker, process_decision
from certificate_utils import generate_certificate

PASSWORD = "GoAML4ever"
init_session_state()
st.set_page_config(page_title="AML Triage", layout="wide")

if not st.session_state.authenticated:
    st.title("🔐 AML Case Triage Login")
    pw = st.text_input("Enter password:", type="password")
    if st.button("Login") and pw == PASSWORD:
        st.session_state.authenticated = True
    st.stop()

# Officer name
if "player_name" not in st.session_state:
    st.title("🕵️ Enter Your Officer Name")
    name = st.text_input("Enter your name to begin:")
    if name and st.button("Start Simulation"):
        st.session_state.player_name = name
        st.session_state.start_time = time.time()
        with open("enhanced_sars_20.json", "r", encoding="utf-8") as f:
            all_sars = json.load(f)
            st.session_state.sars = random.sample(all_sars, 5)
            st.session_state.current_index = 0
            st.session_state.red_flag_choices = {}
            st.session_state.decisions = {}
            st.session_state.missed_flags = {}
    st.stop()

if "sars" not in st.session_state:
    st.warning("Please enter your name to begin.")
    st.stop()

# Process SARs
if st.session_state.current_index < len(st.session_state.sars):
    current_sar = st.session_state.sars[st.session_state.current_index]
    st.header(f"Case {st.session_state.current_index + 1} of {len(st.session_state.sars)}")
    display_sar(current_sar)
    red_flag_picker(current_sar)
    process_decision(current_sar)
else:
    st.success("✅ All SARs processed.")
    duration = time.time() - st.session_state.start_time
    cert_path = generate_certificate(
        name=st.session_state.player_name,
        decisions=st.session_state.decisions,
        red_flag_choices=st.session_state.red_flag_choices,
        missed_flags=st.session_state.missed_flags,
        sars=st.session_state.sars,
        time_taken=duration / 60
    )
    with open(cert_path, "rb") as f:
        st.download_button("📥 Download Your Certificate", f, file_name="AML_Certificate.pdf")
