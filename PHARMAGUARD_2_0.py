
import streamlit as st

st.set_page_config(
    page_title="PHARMAGUARD 2.0",
    page_icon="🛡️",
    layout="wide",
)

LANGUAGES = {
    "मराठी": {
        "title": "PHARMAGUARD 2.0",
        "subtitle": "रुग्ण-केंद्रित औषध सुरक्षा प्रणाली",
        "language": "भाषा निवडा",
        "role": "तुम्ही कोण आहात?",
        "patient": "रुग्ण (Patient)",
        "professional": "आरोग्यसेवा व्यावसायिक (Healthcare Professional)",
        "welcome_patient": "रुग्ण विभागात आपले स्वागत आहे.",
        "welcome_professional": "आरोग्यसेवा व्यावसायिक विभागात आपले स्वागत आहे.",
        "notice": "हा स्वतंत्र विकास prototype आहे. PHARMAGUARD 1.0 बदललेला नाही.",
        "disclaimer": "Prototype only — वैद्यकीय निदान किंवा उपचाराचा पर्याय नाही.",
    },
    "हिंदी": {
        "title": "PHARMAGUARD 2.0",
        "subtitle": "रोगी-केंद्रित दवा सुरक्षा प्रणाली",
        "language": "भाषा चुनें",
        "role": "आप कौन हैं?",
        "patient": "रोगी (Patient)",
        "professional": "स्वास्थ्य सेवा पेशेवर",
        "welcome_patient": "रोगी विभाग में आपका स्वागत है।",
        "welcome_professional": "स्वास्थ्य सेवा पेशेवर विभाग में आपका स्वागत है।",
        "notice": "यह स्वतंत्र विकास prototype है। PHARMAGUARD 1.0 में बदलाव नहीं किया गया है।",
        "disclaimer": "केवल prototype — चिकित्सा निदान या उपचार का विकल्प नहीं।",
    },
    "English": {
        "title": "PHARMAGUARD 2.0",
        "subtitle": "Patient-Centric Medication Safety System",
        "language": "Choose language",
        "role": "Who are you?",
        "patient": "Patient",
        "professional": "Healthcare Professional",
        "welcome_patient": "Welcome to the Patient section.",
        "welcome_professional": "Welcome to the Healthcare Professional section.",
        "notice": "Independent development prototype. PHARMAGUARD 1.0 remains unchanged.",
        "disclaimer": "Prototype only — not a substitute for medical diagnosis or treatment.",
    },
}

st.session_state.setdefault("language", "मराठी")
st.session_state.setdefault("role", None)

language = st.selectbox(
    "Language / भाषा / भाषा",
    list(LANGUAGES.keys()),
    key="language",
)

t = LANGUAGES[language]

st.title(f"🛡️ {t['title']}")
st.subheader(t["subtitle"])
st.info(t["notice"])

st.divider()
st.markdown(f"### {t['role']}")

role = st.radio(
    t["role"],
    [t["patient"], t["professional"]],
    horizontal=False,
    key=f"role_{language}",
)

if role == t["patient"]:
    st.success(t["welcome_patient"])
else:
    st.success(t["welcome_professional"])

st.caption(t["disclaimer"])
