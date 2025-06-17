import streamlit as st

def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "player_name" not in st.session_state:
        st.session_state.player_name = ""
    if "sars" not in st.session_state:
        st.session_state.sars = []
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "red_flag_choices" not in st.session_state:
        st.session_state.red_flag_choices = {}
    if "decisions" not in st.session_state:
        st.session_state.decisions = {}
    if "missed_flags" not in st.session_state:
        st.session_state.missed_flags = {}
    if "start_time" not in st.session_state:
        st.session_state.start_time = 0
