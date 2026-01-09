import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

# --- 1. PASSWORD PROTECTION LOGIC ---
def check_password():
    """Returns True if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Partnership Password", type="password", on_change=password_entered, key="password")
        st.info("Please enter your shared password to access the assessment.")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Partnership Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

# --- 2. START OF APP (ONLY IF PASSWORD CORRECT) ---
if check_password():
    
    # --- DATA STRUCTURES ---
    CATEGORIES = {
        "Household Management": ["Laundry", "Meal Planning", "Grocery Shopping", "Tidying", "Maintenance", "Schedules"],
        "Financial & Admin": ["Bills", "Saving", "Impulse Spending", "Filing", "Appointments", "Email"],
        "Emotional & Social": ["RSD (Rejection Sensitivity)", "Active Listening", "Social Battery", "Conflict Resolution", "Tone Awareness", "Sharing the Mic"],
        "Executive Function": ["Time Blindness", "Task Initiation", "Working Memory", "Transitions", "Hyperfocus", "Prioritization"],
        "Physical & Sensory": ["Sensory Overload", "Sleep Hygiene", "Exercise", "Dopamine Seeking", "Hygiene", "Morning Routine"]
    }

    STRATEGY_LIBRARY = {
        "Household Management": {
            "Struggle": "Low-dopamine tasks. Strategy: Use 'Body Doubling'—do chores together while listening to high-energy music.",
            "Complementary": "The Lead sets 'Low Friction' systems (e.g., lidless bins) to help the Support partner succeed."
        },
        "Financial & Admin": {
            "Struggle": "High executive load. Strategy: Automate EVERY bill. Use shared alerts to gamify savings.",
            "Complementary": "The Lead handles the 'Search' (info gathering), Support partner handles the 'Do' (execution)."
        },
        "Emotional & Social": {
            "Struggle": "Risk of RSD spirals. Strategy: Implement a '5-Minute Time Out' rule for heated discussions.",
            "Complementary": "The Lead acts as the 'Social Anchor,' monitoring the other's social battery."
        },
        "Executive Function": {
            "Struggle": "Time Blindness. Strategy: Visual timers in every room and a shared analog wall calendar.",
            "Complementary": "The Lead provides 'Gentle On-Ramping' (verbal reminders 10 mins before a transition)."
        },
        "Physical & Sensory": {
            "Struggle": "Sensory Overload. Strategy: Create a 'sensory sanctuary' for mutual resets.",
            "Complementary": "The Lead monitors 'Environmental Triggers' (noise/clutter) that may dysregulate the other."
        }
    }

    def get_deep_advice(cat, p1_avg, p2_avg):
        diff = abs(p1_avg - p2_avg)
        avg_total = (p1_avg + p2_avg) / 2
        if avg_total >= 4:
            return f"🚨 **Shared Struggle:** {STRATEGY_LIBRARY[cat]['Struggle']}"
        elif diff >= 1.5:
            lead = "Partner 1" if p1_avg < p2_avg else "Partner 2"
            return f"⚖️ **Lead/Support Dynamics:** {lead} is the 'Captain' here. {STRATEGY_LIBRARY[cat]['Complementary']}"
        else:
            return f"✅ **Balanced Zone:** You both navigate this well. Keep your current routines as a foundation."

    # --- UI LAYOUT ---
    st.set_page_config(page_title="ADHD Partner Harmony", layout="wide")
    st.title("⚡ ADHD Relationship Synergy Analyzer")

    # Scale Guidance
    st.sidebar.header("Rating Scale")
    st.sidebar.info("""
    **1 (No Struggle):** Easy/Automatic.
    **3 (Moderate):** Requires effort.
    **5 (Constant Struggle):** Overwhelming.
    """)

    # --- INPUT TABS ---
    p1_scores, p2_scores, notes = {}, {}, {}
    tabs = st.tabs(list(CATEGORIES.keys()))

    for i, (cat_name, attributes) in enumerate(CATEGORIES.items()):
        with tabs[i]:
            st.subheader(f"{cat_name} Assessment")
            st.write("---")
            for attr in attributes:
                c1, c2 = st.columns(2)
                p1_scores[attr] = c1.select_slider(f"P1: {attr}", options=[1,2,3,4,5], value=1, key=f"p1_{attr}")
                p2_scores[attr] = c2.select_slider(f"P2: {attr}", options=[1,2,3,4,5], value=1, key=f"p2_{attr}")
            notes[cat_name] = st.text_area(f"Private Notes for {cat_name}", key=f"note_{cat_name}")

    st.divider()

    # --- PRIVACY LOCK ---
    st.subheader("🔒 Reveal Results Handshake")
    col_a, col_b = st.columns(2)
    p1_done = col_a.checkbox("Partner 1: My assessment is complete")
    p2_done = col_b.checkbox("Partner 2: My assessment is complete")

    if p1_done and p2_done:
        if st.button("🚀 Reveal Results & Generate Strategy Report", use_container_width=True):
            st.balloons()
            
            # Calculations
            cat_labels = list(CATEGORIES.keys())
            p1_avgs = [sum(p1_scores[a] for a in CATEGORIES[c])/len(CATEGORIES[c]) for c in cat_labels]
            p2_avgs = [sum(p2_scores[a] for a in CATEGORIES[c])/len(CATEGORIES[c]) for c in cat_labels]

            # Radar Chart
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=p1_avgs, theta=cat_labels, fill='toself', name='Partner 1'))
            fig.add_trace(go.Scatterpolar(r=p2_avgs, theta=cat_labels, fill='toself', name='Partner 2'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), title="Cognitive Synergy Map")
            st.plotly_chart(fig)

            # Advice Sections
            for i, cat in enumerate(cat_labels):
                st.subheader(cat)
                st.info(get_deep_advice(cat, p1_avgs[i], p2_avgs[i]))
                if notes[cat]:
                    st.write(f"**Notes:** {notes[cat]}")
    else:
        st.warning("Both partners must check their completion boxes above to reveal the comparison and strategies.")

    # Reset Button in Sidebar
    if st.sidebar.button("🔄 Reset Assessment"):
        for key in st.session_state.keys():
            if key != "password_correct":
                del st.session_state[key]
        st.rerun()
