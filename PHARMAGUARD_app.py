import streamlit as st
import pandas as pd
import joblib

MODEL_PATH = "PHARMAGUARD_RandomForest_Model.joblib"

st.set_page_config(
    page_title="PHARMAGUARD",
    page_icon="🛡️",
    layout="centered"
)

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

st.title("🛡️ PHARMAGUARD")
st.subheader("AI-Assisted ADR Risk Prioritization System")
st.caption("Pharmacovigilance review support • Proof-of-concept")

st.divider()

age = st.number_input("Patient Age", min_value=0, max_value=120, value=30, step=1)
sex = st.selectbox("Sex", ["M", "F", "Unknown"])
drug = st.text_input("Drug name", placeholder="e.g., Eliquis")
adr = st.text_area("Adverse Drug Reaction (ADR)", placeholder="e.g., Headache")

if st.button("🔍 ANALYZE ADR", use_container_width=True):
    if not drug.strip() or not adr.strip():
        st.warning("Please enter both Drug name and ADR.")
    else:
        row = pd.DataFrame([{
            "Age": age,
            "Sex": sex,
            "Drug": drug.strip().upper(),
            "ADR": adr.strip(),
            "Age_Missing": 0,
            "Drug_Missing": 0,
            "ADR_Missing": 0
        }])

        priority = str(model.predict(row)[0]).upper()

        st.divider()
        st.subheader("Risk Priority")

        if priority == "HIGH":
            st.error("🔴 HIGH PRIORITY")
            st.write("Prompt pharmacovigilance review is recommended.")
        elif priority == "MODERATE":
            st.warning("🟡 MODERATE PRIORITY")
            st.write("Pharmacovigilance review is recommended.")
        else:
            st.success("🟢 LOW PRIORITY")
            st.write("Routine review may be considered.")

        st.info(
            "This output is AI-assisted prioritization only. "
            "It is not a diagnosis, treatment recommendation, causality assessment, "
            "or regulatory decision. A qualified healthcare/pharmacovigilance "
            "professional must review the case."
        )

st.divider()
st.caption(
    "PHARMAGUARD • College project prototype • "
    "Model trained on a 200-case feasibility dataset with provisional labels."
)
