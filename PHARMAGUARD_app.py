import streamlit as st
import pandas as pd
import joblib
import re

MODEL_PATH = "PHARMAGUARD_RandomForest_Model.joblib"

st.set_page_config(
    page_title="PHARMAGUARD",
    page_icon="ðŸ›¡ï¸",
    layout="centered"
)

# Project-defined safety gate based on recognized seriousness concepts.
# This is NOT a diagnostic or causality engine and does not replace professional review.
SERIOUS_PATTERNS = [
    r"anaphylaxis",
    r"anaphylactic",
    r"difficulty\s+breathing",
    r"breathing\s+difficulty",
    r"respiratory\s+distress",
    r"respiratory\s+failure",
    r"airway\s+obstruction",
    r"cardiac\s+arrest",
    r"cardiopulmonary\s+arrest",
    r"seizure",
    r"convulsion",
    r"shock",
    r"life[-\s]?threatening",
    r"severe\s+allergic\s+reaction",
    r"angioedema.*(airway|breath|throat)",
    r"throat\s+swelling.*(breath|airway)",
]


def seriousness_safety_check(adr_text: str):
    """Return a project-defined safety flag when ADR text contains a strong serious signal."""
    text = re.sub(r"\s+", " ", adr_text.strip().lower())
    for pattern in SERIOUS_PATTERNS:
        if re.search(pattern, text):
            return True, "Potentially serious medical event signal detected in ADR text."
    return False, "No strong serious signal detected by the safety gate."


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


model = load_model()

st.title("ðŸ›¡ï¸ PHARMAGUARD")
st.subheader("AI-Assisted ADR Risk Prioritization System")
st.caption("Pharmacovigilance review support â€¢ Proof-of-concept")

st.divider()

patient_id = st.text_input(
    "Patient ID",
    value="PHG-0001",
    placeholder="e.g., PHG-0001",
    help="Use an anonymous project ID. Do not enter the patient's name, Aadhaar number, mobile number, or other direct identifiers."
)

age = st.number_input("Patient Age", min_value=0, max_value=120, value=30, step=1)
sex = st.selectbox("Sex", ["M", "F", "Unknown"])
drug = st.text_input("Drug name", placeholder="e.g., Eliquis")
adr = st.text_area(
    "Adverse Drug Reaction (ADR)",
    placeholder="e.g., Headache"
)

if st.button("ðŸ” ANALYZE ADR", use_container_width=True):
    if not patient_id.strip():
        st.warning("Please enter a Patient ID.")
    elif not drug.strip() or not adr.strip():
        st.warning("Please enter both Drug name and ADR.")
    else:
        patient_id_clean = patient_id.strip().upper()
        drug_clean = drug.strip().upper()
        adr_clean = adr.strip()

        # Layer 1: Seriousness safety gate
        serious_flag, serious_reason = seriousness_safety_check(adr_clean)

        # Layer 2: AI priority model for cases without a strong serious signal
        row = pd.DataFrame([{
            "Age": age,
            "Sex": sex,
            "Drug": drug_clean,
            "ADR": adr_clean,
            "Age_Missing": 0,
            "Drug_Missing": 0,
            "ADR_Missing": 0
        }])

        if serious_flag:
            priority = "HIGH"
            result_reason = serious_reason
        else:
            priority = str(model.predict(row)[0]).upper()
            result_reason = "Priority assigned by the Random Forest proof-of-concept model."

        st.divider()
        st.subheader("ADR Review Result")
        st.write(f"**Patient ID:** {patient_id_clean}")

        if priority == "HIGH":
            st.error("ðŸ”´ HIGH PRIORITY")
            st.write("Prompt pharmacovigilance review is recommended.")
        elif priority == "MODERATE":
            st.warning("ðŸŸ¡ MODERATE PRIORITY")
            st.write("Pharmacovigilance review is recommended.")
        else:
            st.success("ðŸŸ¢ LOW PRIORITY")
            st.write("Routine review may be considered.")

        if serious_flag:
            st.warning("âš ï¸ Seriousness Safety Flag: Potentially serious medical event")
        else:
            st.info("Seriousness Safety Flag: No strong serious signal detected by the project safety gate.")

        st.caption(f"Reason: {result_reason}")

        st.info(
            "This output is AI-assisted prioritization only. "
            "It is not a diagnosis, treatment recommendation, causality assessment, "
            "or regulatory decision. A qualified healthcare/pharmacovigilance "
            "professional must review the case."
        )

st.divider()
st.caption(
    "PHARMAGUARD â€¢ College project prototype â€¢ "
    "Model trained on a 200-case feasibility dataset with provisional labels."
)
