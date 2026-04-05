import streamlit as st
from groq import Groq
import model_engine as me
import ai_engine as ae
import logic_config as config
import os
st.set_page_config(page_title="AI Loan Underwriter", layout="wide", page_icon="🏦")
api_key = os.environ.get("GROQ_API_KEY") 

# --- ASSET LOADING ---
@st.cache_resource
def init_connection():
    model, features = me.load_ml_assets()
    client = Groq(api_key=api_key)
    return model, features, client

model, features, client = init_connection()

# --- SIDEBAR ---
st.sidebar.header("Institutional Strategy")
appetite = st.sidebar.select_slider("Lending Appetite", options=[0.1, 0.3, 0.5, 0.7, 0.9], value=0.5)
st.sidebar.info(f"Current Mode: **{config.get_strategy_label(appetite)}**")

rules = config.get_thresholds(appetite)
# --- SIDEBAR: DYNAMIC THRESHOLDS ---
st.sidebar.header("Live Model Logic")

# Calculate the actual bars from the config logic
current_decline = 0.35 - (appetite * 0.30)
current_approve = 0.85 - (appetite * 0.30)
current_pass_grade = 0.60 - (appetite * 0.20)

# 1. Strategy Description
if appetite <= 0.3:
    strat_desc = "**Safety First:** Prioritizing capital preservation. High bars for entry."
elif appetite >= 0.7:
    strat_desc = "**Aggressive Growth:** Lowering barriers to capture market share."
else:
    strat_desc = "**Balanced:** Standard risk-to-reward ratio."

st.sidebar.markdown(strat_desc)

# 2. Hard Decision Rules
st.sidebar.subheader("Mathematical Rules")
st.sidebar.write(f"**Auto-Decline:** Math Score < {current_decline:.0%}")
st.sidebar.write(f"**Auto-Approve:** Math Score > {current_approve:.0%}")
st.sidebar.write(f"**Grey Area Pass:** Blended Score > {current_pass_grade:.0%}")

# 3. AI Override Rules (The Veto & Mercy)
st.sidebar.subheader("AI Safety Overrides")
st.sidebar.write(f"**VETO:** If Character < 30% (Even with 99% Math)")
st.sidebar.write(f"**MERCY:** If Character > 85% (Escapes Auto-Decline)")

st.sidebar.divider()
st.sidebar.caption(
    f"**Blended Formula:** (0.6 * Math) + (0.4 * AI). "
    "This creates a 'Character-Adjusted' risk profile for applicants in the middle ground."
)

# --- MAIN UI ---
st.title("The Lending Decision Engine")
col1, col2 = st.columns([1, 1.2])

with col1:
    with st.form("loan_form"):
        score = st.number_input("Risk Score", 300, 850, 650)
        dti = st.slider("DTI %", 0, 100, 25)
        amt = st.number_input("Loan Amount ($)", 1000, 100000, 15000)
        yemp = st.number_input("Years Employed", 0, 50, 5)
        purpose = st.text_area("Loan Purpose")
        submitted = st.form_submit_button("Run Analysis")

if submitted:
    ml_prob = me.get_ml_prediction(model, features, [score, dti, amt, yemp])
    ai_score, ai_reason = ae.get_ai_character_assessment(client, purpose, score, dti, amt, yemp)

    with col2:
        # Inject Alert CSS if needed
        if ml_prob >= 0.90 or ai_score >= 0.90:
            st.markdown("<style>div[data-testid='stMetricValue'] {color: #ff4b4b !important;}</style>", unsafe_allow_html=True)
            st.warning("CRITICAL LEVEL REACHED")

        m1, m2 = st.columns(2)
        m1.metric("Math Prob.", f"{ml_prob:.1%}", help="Probabilistic XGBoost score.")
        m2.metric("Character Score", f"{ai_score:.1%}", help="Qualitative AI assessment.")

        # Logic Matrix
# --- 🛡️ ENHANCED DECISION MATRIX (With Veto & Mercy) ---
        if ml_prob < rules['decline_bar']:
            # THE MERCY RULE: If math is low, but AI score is elite (>85%)
            if ai_score > 0.85:
                decision, color, icon = "🟡 PENDING REVIEW (AI Mercy)", "orange", "⏳"
            else:
                decision, color, icon = "❌ AUTO-DECLINED", "red", "✖️"
                
        elif ml_prob > rules['approve_bar']:
            # THE VETO RULE: If math is high, but AI sees risk (<30%)
            if ai_score < 0.30:
                decision, color, icon = "🚫 VETOED (Intent Risk)", "red", "⛔"
            else:
                decision, color, icon = "✅ AUTO-APPROVED", "green", "✔️"
                
        else:
            # THE GREY AREA: Blended Math (60%) and AI (40%)
            blended = (ml_prob * 0.6) + (ai_score * 0.4)
            if blended > rules['pass_grade']:
                decision, color, icon = f"✅ APPROVED (Blended: {blended:.1%})", "green", "🤝"
            else:
                decision, color, icon = f"❌ DECLINED (Low Blended: {blended:.1%})", "red", "📉"

        # Final Visual Result
        st.markdown(f"### {icon} Decision: :{color}[{decision}]")
        st.write(f"**AI Justification:** {ai_reason}")
        st.progress(float(ml_prob), text="Math Probability")
        st.progress(ai_score, text="Character Score")