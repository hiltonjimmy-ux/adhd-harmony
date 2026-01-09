import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO

# --- 1. INITIALIZE GLOBAL STATE ---
# We use keys to track all sliders and text areas so we can clear them at once
if 'wins' not in st.session_state:
    st.session_state.wins = []

def reset_app():
    # This loop clears every slider and text area registered in the app
    for key in st.session_state.keys():
        if key != 'wins': # We keep the wins for the session, but clear everything else
            del st.session_state[key]
    st.rerun()

# --- 2. DATA STRUCTURES ---
CATEGORIES = {
    "Household Management": ["Laundry", "Meal Planning", "Grocery Shopping", "Tidying", "Maintenance", "Schedules"],
    "Financial & Admin": ["Bills", "Saving", "Impulse Spending", "Filing", "Appointments", "Email"],
    "Emotional & Social": ["RSD", "Listening", "Social Battery", "Conflict", "Tone", "Sharing"],
    "Executive Function": ["Time Blindness", "Initiation", "Memory", "Transitions", "Hyperfocus", "Priorities"],
    "Physical & Sensory": ["Sensory", "Sleep", "Exercise", "Dopamine", "Hygiene", "Morning"]
}

# [get_deep_advice function logic from previous turn...]

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="ADHD Synergy", layout="wide")

with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🔄 Reset All Assessments", type="primary"):
        reset_app()
    
    st.divider()
    st.header("🏆 Dopamine Win Tracker")
    win_desc = st.text_input("New Win", placeholder="e.g. Paid the electricity bill early!", key="win_input")
    if st.button("Log Win"):
        if win_desc:
            st.session_state.wins.append(win_desc)
            st.toast("Success logged!")

st.title("⚡ ADHD Relationship Synergy Analyzer")

# --- 4. THE INPUT TABS ---
p1_scores, p2_scores, notes = {}, {}, {}
tabs = st.tabs(list(CATEGORIES.keys()))

for i, (cat_name, attributes) in enumerate(CATEGORIES.items()):
    with tabs[i]:
        for attr in attributes:
            c1, c2 = st.columns(2)
            # Assigning unique keys to sliders for reset functionality
            p1_scores[attr] = c1.select_slider(f"P1: {attr}", options=[1,2,3,4,5], value=3, key=f"p1_s_{attr}")
            p2_scores[attr] = c2.select_slider(f"P2: {attr}", options=[1,2,3,4,5], value=3, key=f"p2_s_{attr}")
        
        notes[cat_name] = st.text_area(f"Notes for {cat_name}", key=f"note_area_{cat_name}")

# --- 5. GENERATE REPORT ---
if st.button("Generate Deep Analysis Report", use_container_width=True):
    # Logic to calculate averages, display Plotly chart, and show advice...
    # (Same as previous implementation)
    st.success("Analysis updated! Check the bottom of the page for your PDF export.")