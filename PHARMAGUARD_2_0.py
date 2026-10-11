
import streamlit as st

st.set_page_config(
    page_title="PHARMAGUARD 2.0",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ PHARMAGUARD 2.0")
st.subheader("Patient-Centric Medication Safety System")

st.info(
    "Independent development prototype. "
    "PHARMAGUARD 1.0 remains unchanged."
)

language = st.selectbox(
    "Choose Language / भाषा निवडा",
    ["मराठी", "हिंदी", "English"],
)

messages = {
    "मराठी": "PHARMAGUARD 2.0 मध्ये आपले स्वागत आहे!",
    "हिंदी": "PHARMAGUARD 2.0 में आपका स्वागत है!",
    "English": "Welcome to PHARMAGUARD 2.0!",
}

st.success(messages[language])

st.caption(
    "Prototype only — not for clinical decision-making."
)
