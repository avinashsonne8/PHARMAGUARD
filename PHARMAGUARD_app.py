import streamlit as st
import joblib
import pandas as pd
from datetime import datetime

# =========================
# STEP 51 — PROFESSIONAL BRANDING
# =========================
st.set_page_config(page_title="PHARMAGUARD | ADR Prioritization", page_icon="🛡️", layout="centered")

st.markdown("""
<style>
.pg-header{text-align:center;padding:.25rem 0 .7rem}
.pg-logo{font-size:2.2rem;font-weight:800;letter-spacing:.4px}
.pg-subtitle{font-size:.95rem;margin-top:-.15rem}
.pg-badge{display:inline-block;padding:.22rem .65rem;border-radius:999px;font-size:.76rem;font-weight:600;margin-top:.4rem}
.pg-flow{text-align:center;font-size:.82rem;padding:.65rem .25rem;border-radius:.6rem;margin:.45rem 0 1rem}
</style>
<div class="pg-header">
<div class="pg-logo">🛡️ PHARMAGUARD</div>
<div class="pg-subtitle">AI-Assisted ADR Risk Prioritization System</div>
<div class="pg-badge">Pharmacovigilance • Proof of Concept</div>
</div>
<div class="pg-flow"><b>ADR Input</b> → <b>Seriousness Safety Gate</b> → <b>Moderate Review Gate</b> → <b>AI Model</b> → <b>Priority</b></div>
""")


st.title("💊 PHARMAGUARD")
st.caption("Pharmacovigilance review support • Proof-of-concept")

MODEL_FILE = "PHARMAGUARD_RandomForest_Model.joblib"
try:
    model = joblib.load(MODEL_FILE)
except Exception as e:
    st.error("Model could not be loaded.")
    st.code(str(e))
    st.stop()

if "adr_history" not in st.session_state:
    st.session_state.adr_history = []

SERIOUS_PATTERNS = [
    "anaphylaxis","anaphylactic","difficulty breathing","breathing difficulty",
    "respiratory distress","respiratory failure","life threatening",
    "life-threatening","cardiac arrest","cardiorespiratory arrest",
    "severe allergic reaction","airway obstruction","loss of consciousness",
    "coma","shock","convulsion","seizure"
]

MODERATE_PATTERNS = [
    "requiring medical attention","required medical attention",
    "medical attention","requiring monitoring","required monitoring",
    "under monitoring","requiring evaluation","required evaluation",
    "needs evaluation","persistent","prolonged","recurrent",
    "significant dizziness","marked dizziness","muscle pain and weakness",
    "muscle pain with weakness","dehydration"
]

def matches(text, patterns):
    text = " ".join(str(text).lower().strip().split())
    return [x for x in patterns if x in text]

def model_predict(age, sex, drug, adr):
    X = pd.DataFrame([{
        "Age": age, "Sex": sex, "Drug": drug, "ADR": adr,
        "Age_Missing": 0,
        "Drug_Missing": int(not str(drug).strip()),
        "ADR_Missing": int(not str(adr).strip())
    }])
    if isinstance(model, dict):
        estimator = model.get("model") or model.get("estimator")
        preprocessor = model.get("preprocessor")
        if estimator is not None and preprocessor is not None:
            try:
                return str(estimator.predict(preprocessor.transform(X))[0]).upper()
            except Exception:
                pass
    try:
        return str(model.predict(X)[0]).upper()
    except Exception:
        return "UNKNOWN"

patient_id = st.text_input("Patient ID", placeholder="Example: PHG-0001")
age = st.number_input("Patient Age", min_value=0, max_value=120, value=30, step=1)
sex = st.selectbox("Sex", ["M", "F", "Unknown"])
drug = st.text_input("Drug Name", placeholder="Example: Amoxicillin")
adr = st.text_area("Adverse Drug Reaction (ADR)",
                   placeholder="Example: Anaphylaxis with difficulty breathing",
                   height=120)

if st.button("🔍 ANALYZE ADR", use_container_width=True):
    if not patient_id.strip():
        st.warning("Please enter a Patient ID.")
        st.stop()
    if not adr.strip():
        st.warning("Please enter an ADR.")
        st.stop()

    serious_hits = matches(adr, SERIOUS_PATTERNS)
    moderate_hits = matches(adr, MODERATE_PATTERNS)

    if serious_hits:
        priority = "HIGH"
        flag = "Potentially serious medical event signal"
        reason = "Serious ADR indicator detected: " + ", ".join(serious_hits)
        recommendation = "Priority pharmacovigilance review required."
    elif moderate_hits:
        priority = "MODERATE"
        flag = "Non-serious but clinically meaningful review signal"
        reason = "Project-defined moderate-review indicator detected: " + ", ".join(moderate_hits)
        recommendation = "Pharmacovigilance review and clinical assessment recommended."
    else:
        priority = model_predict(age, sex, drug, adr)
        if priority not in {"LOW", "MODERATE", "HIGH"}:
            priority = "UNKNOWN"
        flag = "No predefined serious signal detected"
        reason = "Priority assigned by the Random Forest prototype."
        recommendation = "Routine pharmacovigilance review according to the project workflow."

    st.divider()
    st.subheader("📋 ADR Analysis Result")
    st.write(f"**Patient ID:** {patient_id}")
    if priority == "HIGH":
        st.error("🔴 HIGH PRIORITY")
    elif priority == "MODERATE":
        st.warning("🟡 MODERATE PRIORITY")
    elif priority == "LOW":
        st.success("🟢 LOW PRIORITY")
    else:
        st.info("⚪ PRIORITY UNCERTAIN")
    st.write(f"**Seriousness / Review Flag:** {flag}")
    st.write(f"**Reason:** {reason}")
    st.write(f"**Recommendation:** {recommendation}")

    st.session_state.adr_history.append({
        "Date_Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Patient_ID": patient_id, "Age": age, "Sex": sex,
        "Drug": drug, "ADR": adr, "Priority": priority,
        "Seriousness_Flag": flag, "Reason": reason
    })

if st.session_state.adr_history:
    st.divider()

# =========================
# STEP 50 — ADR DASHBOARD
# =========================
if st.session_state.get("adr_history"):
    st.markdown("---")
    st.subheader("📊 PHARMAGUARD Dashboard")
    st.caption("Dashboard shows only ADR cases analyzed in the current app session.")

    dashboard_df = pd.DataFrame(st.session_state.adr_history)
    priority_counts = (
        dashboard_df["Priority"]
        .astype(str)
        .str.upper()
        .value_counts()
        .reindex(["HIGH", "MODERATE", "LOW"], fill_value=0)
    )

    total_cases = len(dashboard_df)
    high_cases = int(priority_counts["HIGH"])
    moderate_cases = int(priority_counts["MODERATE"])
    low_cases = int(priority_counts["LOW"])

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total ADR Cases", total_cases)
    m2.metric("🔴 High", high_cases)
    m3.metric("🟡 Moderate", moderate_cases)
    m4.metric("🟢 Low", low_cases)

    st.markdown("#### Priority Distribution")
    chart_df = priority_counts.rename("Cases").reset_index()
    chart_df.columns = ["Priority", "Cases"]
    st.bar_chart(chart_df.set_index("Priority"))

    st.subheader("📚 ADR Report History")
    df = pd.DataFrame(st.session_state.adr_history)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button("⬇️ Download ADR History (CSV)",
                       data=df.to_csv(index=False).encode("utf-8"),
                       file_name="PHARMAGUARD_ADR_History.csv",
                       mime="text/csv", use_container_width=True)
    if st.button("🗑️ Clear Current Session History", use_container_width=True):
        st.session_state.adr_history = []
        st.rerun()

st.divider()
st.caption("⚠️ AI-assisted prioritization only. This prototype is not a diagnosis, treatment recommendation, causality assessment, or regulatory decision. A qualified healthcare/pharmacovigilance professional must review the case.")
