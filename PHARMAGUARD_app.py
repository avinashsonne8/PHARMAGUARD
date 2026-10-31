# PHARMAGUARD — AI-assisted ADR review-priority prototype.
# Safety Gate rules take precedence over the Random Forest prototype output.
# Styling lives in styles.css (same folder as this file).
import html
import logging
import re
import textwrap
import uuid
from datetime import date, datetime
from pathlib import Path

import joblib
import pandas as pd
import requests
import streamlit as st

logger = logging.getLogger("pharmaguard")
BASE_DIR = Path(__file__).resolve().parent


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="PHARMAGUARD",
    page_icon="💊",
    layout="wide"
)


@st.cache_resource
def _read_stylesheet(filename="styles.css"):
    try:
        return (BASE_DIR / filename).read_text(encoding="utf-8")
    except OSError:
        logger.warning("Stylesheet %s not found; using default styling.", filename)
        return ""


_css_text = _read_stylesheet()
if _css_text:
    st.markdown(f"<style>{_css_text}</style>", unsafe_allow_html=True)
else:
    st.warning("styles.css was not found next to the app file; the interface will use default styling.")


# =========================================================
# PROFESSIONAL HEADER
# =========================================================

st.markdown("""


<div class="pg-appbar">
<div class="pg-brand-mini">🛡️ PHARMAGUARD</div>
<div class="pg-status">● Prototype Online</div>
</div>
<div class="pg-header">
<div class="pg-shield">🛡️</div>
<div class="pg-title">PHARMAGUARD</div>
<div class="pg-subtitle">AI-Assisted ADR Risk Prioritization System</div>
<div class="pg-tag">Pharmacovigilance • Proof of Concept</div>
</div>
<div class="pg-hero">
<div class="pg-hero-title">ADR Review Support, in One Workflow</div>
<div class="pg-hero-text">Enter the reported adverse drug reaction, review the predefined Safety Gate, and use the Random Forest prototype for additional priority assistance. Final priority is intended to support pharmacovigilance review.</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# CASE REPORTS / ABOUT / SETTINGS STYLES
# =========================================================


# =========================================================
# FINAL MOBILE POLISH
# =========================================================


# =========================================================
# APP NAVIGATION / PROJECT INFO
# =========================================================

# =========================================================
# CLEAN PROFESSIONAL SIDEBAR NAVIGATION
# =========================================================

def _navigate_to(page):
    st.session_state["active_page"] = page


LANGUAGE_TEXT = {
    "English": {
        "selector": "Language", "seizure": "Seizure", "chest_pain": "Severe chest pain", "patient": "👤 Patient Corner", "professional": "🩺 Healthcare Professional Corner",
        "patient_caption": "Report a possible medicine-related reaction for healthcare-professional review.",
        "emergency": "If you have difficulty breathing, throat/tongue swelling, collapse, or another severe symptom, seek emergency medical help now. Do not wait for this form.",
        "case_ref": "Case Reference", "age": "Age", "sex": "Sex", "age_known": "Age (if known)", "sex_known": "Sex (if known)", "choose_option": "Choose Option", "not_provided": "Not provided", "female": "Female", "male": "Male", "other": "Other",
        "medicine": "Medicine name *", "symptoms": "Reported symptoms / possible ADR *", "onset": "When did symptoms start?", "breathing": "Difficulty breathing", "swelling": "Throat or tongue swelling", "fainting": "Fainting or collapse", "bleeding": "Severe bleeding", "submit": "Submit ADR report",
        "urgent": "URGENT: Seek immediate emergency medical assessment. Do not delay care to submit this report.", "required": "Enter both the medicine name and symptoms.", "saved": "Report saved to the configured patient-safety database.", "not_saved": "Report was not confirmed as saved. ", "disclaimer": "This report is not a diagnosis or confirmation that a medicine caused the symptoms.",
        "pro_warning": "Check emergency warning signs first. This form does not replace clinical assessment or urgent care.", "flags": "Emergency warning signs reported", "no_flags": "No listed emergency flags selected; this does not rule out an emergency.", "case_id": "Patient / Case Reference ID *", "seriousness": "Seriousness review", "not_assessed": "Not assessed", "potentially_serious": "Potentially serious", "not_identified": "Not currently identified as serious", "needs_assessment": "Needs further assessment", "status": "Review status", "pending": "Pending", "under_review": "Under Review", "reviewed": "Reviewed", "notes": "Reviewer notes", "save_review": "Save case review", "required_pro": "Enter the case reference, medicine name, and reported symptoms.", "review_saved": "Case review saved to the configured patient-safety database.", "review_not_saved": "Case review was not confirmed as saved. ", "urgent_prefix": "URGENT: ", "urgent_suffix": ". Arrange immediate emergency assessment.", "no_flags_pro": "No emergency flags selected in this review", "role_patient": "Patient", "role_pro": "Healthcare Professional", "seriousness_value": "Needs healthcare professional assessment", "pending_value": "Pending", "no_flags_value": "No listed emergency flags selected", "urgent_value": "URGENT - emergency warning sign reported", "reviewer_onset": "Reported symptom onset: "
    },
    "मराठी": {
        "selector": "भाषा निवडा", "seizure": "झटका / आकडी", "chest_pain": "तीव्र छातीत दुखणे", "patient": "👤 रुग्ण विभाग", "professional": "🩺 आरोग्यसेवा व्यावसायिक विभाग",
        "patient_caption": "औषधामुळे झालेल्या संभाव्य त्रासाची नोंद आरोग्यसेवा व्यावसायिकांच्या तपासणीसाठी करा.",
        "emergency": "श्वास घेण्यास त्रास, घसा/जीभ सुजणे, बेशुद्ध पडणे किंवा इतर गंभीर लक्षणे असल्यास त्वरित आपत्कालीन वैद्यकीय मदत घ्या. हा फॉर्म भरण्यासाठी थांबू नका.",
        "case_ref": "केस संदर्भ क्रमांक", "age": "वय", "sex": "लिंग", "age_known": "वय (माहित असल्यास)", "sex_known": "लिंग (माहित असल्यास)", "choose_option": "पर्याय निवडा", "not_provided": "माहिती दिलेली नाही", "female": "स्त्री", "male": "पुरुष", "other": "इतर",
        "medicine": "औषधाचे नाव *", "symptoms": "नोंदवलेली लक्षणे / संभाव्य ADR *", "onset": "लक्षणे कधी सुरू झाली?", "breathing": "श्वास घेण्यास त्रास", "swelling": "घसा किंवा जीभ सुजणे", "fainting": "बेशुद्ध पडणे किंवा कोसळणे", "bleeding": "तीव्र रक्तस्राव", "submit": "ADR नोंद सबमिट करा",
        "urgent": "तातडीची सूचना: त्वरित आपत्कालीन वैद्यकीय तपासणी करून घ्या. नोंद भरण्यासाठी उपचार उशिरा करू नका.", "required": "औषधाचे नाव आणि लक्षणे दोन्ही भरा.", "saved": "अहवाल संबंधित patient-safety database मध्ये सेव्ह झाला.", "not_saved": "अहवाल सेव्ह झाल्याची पुष्टी मिळाली नाही. ", "disclaimer": "ही नोंद निदान नाही आणि औषधामुळेच लक्षणे झाली याची पुष्टीही नाही.",
        "pro_warning": "आधी आपत्कालीन लक्षणे तपासा. हा फॉर्म वैद्यकीय तपासणी किंवा तातडीच्या उपचारांचा पर्याय नाही.", "flags": "नोंदवलेली आपत्कालीन लक्षणे", "no_flags": "यादीतील आपत्कालीन लक्षणे निवडलेली नाहीत; तरीही आपत्कालीन स्थिती नसल्याची खात्री होत नाही.", "case_id": "रुग्ण / केस संदर्भ क्रमांक *", "seriousness": "गंभीरतेचे मूल्यांकन", "not_assessed": "मूल्यांकन केलेले नाही", "potentially_serious": "संभाव्यतः गंभीर", "not_identified": "सध्या गंभीर म्हणून ओळखलेले नाही", "needs_assessment": "अधिक मूल्यांकन आवश्यक", "status": "तपासणीची स्थिती", "pending": "प्रलंबित", "under_review": "तपासणी सुरू", "reviewed": "तपासणी पूर्ण", "notes": "तपासणी करणाऱ्याच्या नोंदी", "save_review": "केस तपासणी सेव्ह करा", "required_pro": "केस संदर्भ क्रमांक, औषधाचे नाव आणि लक्षणे भरा.", "review_saved": "केस तपासणी सेव्ह झाली.", "review_not_saved": "केस तपासणी सेव्ह झाल्याची पुष्टी मिळाली नाही. ", "urgent_prefix": "तातडीची सूचना: ", "urgent_suffix": ". त्वरित आपत्कालीन वैद्यकीय तपासणी करा.", "no_flags_pro": "या तपासणीत आपत्कालीन लक्षणे निवडलेली नाहीत", "role_patient": "रुग्ण", "role_pro": "आरोग्यसेवा व्यावसायिक", "seriousness_value": "आरोग्यसेवा व्यावसायिकांचे मूल्यांकन आवश्यक", "pending_value": "प्रलंबित", "no_flags_value": "यादीतील आपत्कालीन लक्षणे निवडलेली नाहीत", "urgent_value": "तातडीचे - आपत्कालीन लक्षण नोंदवले", "reviewer_onset": "लक्षणे सुरू झाल्याची तारीख: "
    },
    "हिंदी": {
        "selector": "भाषा चुनें", "seizure": "दौरा", "chest_pain": "तेज सीने में दर्द", "patient": "👤 रोगी विभाग", "professional": "🩺 स्वास्थ्य सेवा पेशेवर विभाग",
        "patient_caption": "दवा से हुई संभावित प्रतिक्रिया को स्वास्थ्य सेवा पेशेवर की समीक्षा के लिए दर्ज करें।",
        "emergency": "सांस लेने में परेशानी, गले/जीभ में सूजन, बेहोशी या अन्य गंभीर लक्षण हों तो तुरंत आपातकालीन चिकित्सा सहायता लें। इस फॉर्म के लिए प्रतीक्षा न करें।",
        "case_ref": "केस संदर्भ संख्या", "age": "उम्र", "sex": "लिंग", "age_known": "उम्र (यदि पता हो)", "sex_known": "लिंग (यदि पता हो)", "choose_option": "विकल्प चुनें", "not_provided": "नहीं दिया गया", "female": "महिला", "male": "पुरुष", "other": "अन्य",
        "medicine": "दवा का नाम *", "symptoms": "दर्ज लक्षण / संभावित ADR *", "onset": "लक्षण कब शुरू हुए?", "breathing": "सांस लेने में परेशानी", "swelling": "गले या जीभ में सूजन", "fainting": "बेहोशी या गिर जाना", "bleeding": "गंभीर रक्तस्राव", "submit": "ADR रिपोर्ट जमा करें",
        "urgent": "तत्काल: तुरंत आपातकालीन चिकित्सा जांच कराएं। रिपोर्ट जमा करने के लिए उपचार में देरी न करें।", "required": "दवा का नाम और लक्षण दोनों भरें।", "saved": "रिपोर्ट patient-safety database में सेव हो गई।", "not_saved": "रिपोर्ट सेव होने की पुष्टि नहीं हुई। ", "disclaimer": "यह रिपोर्ट निदान नहीं है और यह पुष्टि नहीं करती कि लक्षण दवा के कारण ही हुए।",
        "pro_warning": "पहले आपातकालीन चेतावनी संकेत जांचें। यह फॉर्म चिकित्सकीय जांच या तत्काल उपचार का विकल्प नहीं है।", "flags": "दर्ज आपातकालीन चेतावनी संकेत", "no_flags": "सूची के आपातकालीन संकेत नहीं चुने गए; इससे आपातकाल न होने की पुष्टि नहीं होती।", "case_id": "रोगी / केस संदर्भ संख्या *", "seriousness": "गंभीरता की समीक्षा", "not_assessed": "मूल्यांकन नहीं हुआ", "potentially_serious": "संभावित रूप से गंभीर", "not_identified": "अभी गंभीर नहीं पहचाना गया", "needs_assessment": "आगे मूल्यांकन आवश्यक", "status": "समीक्षा स्थिति", "pending": "लंबित", "under_review": "समीक्षा जारी", "reviewed": "समीक्षा पूरी", "notes": "समीक्षक की टिप्पणियां", "save_review": "केस समीक्षा सेव करें", "required_pro": "केस संदर्भ, दवा का नाम और लक्षण भरें।", "review_saved": "केस समीक्षा सेव हो गई।", "review_not_saved": "केस समीक्षा सेव होने की पुष्टि नहीं हुई। ", "urgent_prefix": "तत्काल: ", "urgent_suffix": ". तुरंत आपातकालीन जांच कराएं।", "no_flags_pro": "इस समीक्षा में कोई आपातकालीन संकेत नहीं चुना गया", "role_patient": "रोगी", "role_pro": "स्वास्थ्य सेवा पेशेवर", "seriousness_value": "स्वास्थ्य सेवा पेशेवर का मूल्यांकन आवश्यक", "pending_value": "लंबित", "no_flags_value": "सूची के आपातकालीन संकेत नहीं चुने गए", "urgent_value": "तत्काल - आपातकालीन संकेत दर्ज", "reviewer_onset": "लक्षण शुरू होने की तारीख: "
    }
}

st.session_state.setdefault("pg_language", "English")

with st.sidebar:
    st.selectbox("Language / भाषा / भाषा निवडा", ["English", "मराठी", "हिंदी"], key="pg_language")

with st.sidebar:
    if "active_page" not in st.session_state:
        st.session_state["active_page"] = "🏠 Dashboard"

    current_page = st.session_state["active_page"]

    st.markdown(
        """
        <div class="pg-sidebar-brand">
            <div class="pg-sidebar-brand-row">
                <div class="pg-sidebar-logo">🛡️</div>
                <div>
                    <div class="pg-sidebar-name">PHARMAGUARD</div>
                    <div class="pg-sidebar-subtitle">ADR Risk Prioritization</div>
                </div>
            </div>
            <div class="pg-sidebar-status">● Prototype • Active</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="pg-sidebar-section">MAIN</div>', unsafe_allow_html=True)
    main_items = [
        ("🏠 Dashboard", "Dashboard"),
        ("🔍 New ADR Analysis", "New Analysis"),
    ]
    for page, _label in main_items:
        st.button(
            page,
            key=f"nav_{page}",
            use_container_width=True,
            type="primary" if current_page == page else "secondary",
            on_click=_navigate_to,
            args=(page,)
        )

    st.markdown('<div class="pg-sidebar-section">CASES</div>', unsafe_allow_html=True)
    case_items = [
        ("📂 Cases", "Cases"),
        ("☁️ Database", "Database"),
    ]
    for page, _label in case_items:
        st.button(
            page,
            key=f"nav_{page}",
            use_container_width=True,
            type="primary" if current_page == page else "secondary",
            on_click=_navigate_to,
            args=(page,)
        )

    st.markdown('<div class="pg-sidebar-section">INSIGHTS</div>', unsafe_allow_html=True)
    analytics_page = "📊 Analytics"
    st.button(
        analytics_page,
        key="nav_analytics",
        use_container_width=True,
        type="primary" if current_page == analytics_page else "secondary",
        on_click=_navigate_to,
        args=(analytics_page,)
    )

    st.markdown('<div class="pg-sidebar-section">PATIENT SAFETY</div>', unsafe_allow_html=True)
    for page in ("👤 Patient Corner", "🩺 Healthcare Professional Corner"):
        st.button(
            page,
            key=f"nav_{page}",
            use_container_width=True,
            type="primary" if current_page == page else "secondary",
            on_click=_navigate_to,
            args=(page,)
        )

    st.markdown('<div class="pg-sidebar-section">PROJECT</div>', unsafe_allow_html=True)
    project_page = "ℹ️ Project Info"
    st.button(
        project_page,
        key="nav_project_info",
        use_container_width=True,
        type="primary" if current_page == project_page else "secondary",
        on_click=_navigate_to,
        args=(project_page,)
    )

    st.markdown('<div class="pg-sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="pg-sidebar-note">
            <div class="pg-sidebar-note-title">Safety-first workflow</div>
            <div class="pg-sidebar-note-text">
                Review-priority support only. Not a diagnostic, causality or regulatory assessment tool.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# STREAMLIT NATIVE DARK-MODE COMPATIBILITY
# Do not detect phone/OS theme. Streamlit controls the active theme.
# Only custom PHARMAGUARD surfaces are patched; backend/scientific logic is unchanged.

# MODEL + GOOGLE SHEET
# =========================================================

MODEL_FILE = str(BASE_DIR / "PHARMAGUARD_RandomForest_Model.joblib")

try:
    GOOGLE_SHEET_URL = st.secrets["GOOGLE_SHEET_URL"]
except Exception:
    GOOGLE_SHEET_URL = ""
    st.error("GOOGLE_SHEET_URL is missing from Streamlit Secrets. Add it under Settings → Secrets before using database features.")


# =========================================================
# LOAD ML MODEL
# =========================================================

@st.cache_resource
def load_ml_model():

    try:
        return joblib.load(MODEL_FILE)

    except Exception as e:
        st.error("Random Forest model could not be loaded.")
        st.info("Make sure PHARMAGUARD_RandomForest_Model.joblib is uploaded in the same repository folder as this app file.")
        st.code(str(e))
        st.stop()


model = load_ml_model()


# =========================================================
# SERIOUS ADR PATTERNS
# =========================================================

SERIOUS_PATTERNS = [
    # Anaphylaxis / severe allergic reaction
    "anaphylaxis",
    "anaphylactic",
    "severe allergic reaction",
    "anaphylactic shock",
    "airway swelling",

    # Severe cutaneous adverse reactions: Stevens-Johnson syndrome
    # Include ASCII hyphen, Unicode en dash (–), em dash (—), and no-dash variants.
    "stevens-johnson syndrome",
    "stevens–johnson syndrome",
    "stevens—johnson syndrome",
    "stevens johnson syndrome",
    "stevens-johnson",
    "stevens–johnson",
    "stevens—johnson",
    "stevens johnson",
    "sjs",

    # Severe cutaneous adverse reaction: toxic epidermal necrolysis (TEN)
    "toxic epidermal necrolysis",
    "toxic epidermal necrolysis (ten)",
    "toxic epidermal necrolysis ten",
    "epidermal necrolysis",
    "ten",
    "lyell syndrome",
    "lyell's syndrome",

    # Severe breathing problems
    "difficulty breathing",
    "breathing problem",
    "breathing problems",
    "difficulty in breathing",
    "difficulty with breathing",
    "difficulty to breathe",
    "breathing difficulty",
    "breathing trouble",
    "trouble breathing",
    "trouble with breathing",
    "shortness of breath",
    "short of breath",
    "breathlessness",
    "unable to breathe",
    "cannot breathe",
    "could not breathe",
    "respiratory distress",
    "respiratory failure",
    "acute respiratory failure",
    "respiratory insufficiency",
    # Explicit respiratory emergencies missing from the uploaded pattern list
    "respiratory arrest",
    "acute respiratory arrest",
    "respiratory depression",
    "respiratory paralysis",
    "respiratory collapse",
    "apnea",
    "apnoea",
    "breathing stopped",
    "stopped breathing",

    # Life-threatening events
    "life threatening",
    "life-threatening",
    "life-threatening event",
    "life-threatening reaction",
    "life-threatening condition",
    "life was at risk",

    # Cardiac emergencies
    "cardiac arrest",
    "cardiorespiratory arrest",
    "heart stopped",
    "heart stopped beating",
    "cardiac collapse",
    "cardiovascular collapse",
    "circulatory collapse",
    "ventricular fibrillation",
    "ventricular tachycardia",
    "torsades de pointes",
    "torsade de pointes",
    "torsades",
    "pulseless electrical activity",
    "myocardial infarction",
    "myocarditis",
    "complete av block",
    "atrioventricular block",

    # Cerebrovascular / severe bleeding emergencies
    # Include both British and American spellings and common variants.
    "haemorrhagic infarction",
    "hemorrhagic infarction",
    "haemorrhagic stroke",
    "hemorrhagic stroke",
    "intracerebral haemorrhage",
    "intracerebral hemorrhage",
    "intracranial haemorrhage",
    "intracranial hemorrhage",
    "subarachnoid haemorrhage",
    "subarachnoid hemorrhage",

    # Retroperitoneal / severe internal bleeding signals
    "retroperitoneal haemorrhage",
    "retroperitoneal hemorrhage",
    "retroperitoneal bleeding",
    "retroperitoneal bleed",

    # Gastrointestinal / severe bleeding signals (British and American spellings)
    "gastrointestinal haemorrhage",
    "gastrointestinal hemorrhage",
    "gastrointestinal bleeding",
    "gi haemorrhage",
    "gi hemorrhage",
    "gi bleeding",
    "severe bleeding",
    "major bleeding",

    # Neurological emergencies
    "loss of consciousness",
    "lost consciousness",
    "unconscious",
    "became unconscious",
    "unresponsive",
    "became unresponsive",
    "coma",
    "comatose",
    "seizure",
    "seizures",
    "convulsion",
    "convulsions",
    "convulsive seizure",
    # Status epilepticus: explicit serious neurological emergency terms
    "status epilepticus",
    "status-epilepticus",
    "epileptic status",

    # Shock
    "shock",
    "circulatory shock",
    "cardiogenic shock",
    "hypovolemic shock",
    "septic shock",
    "anaphylactic shock",

    # Death / fatal outcomes
    "death",
    "died",
    "fatal",
    "fatal outcome",
    "fatal reaction",

    # Disability / incapacity
    "persistent disability",
    "significant disability",
    "permanent disability",
    "incapacity",

    # Congenital / birth outcomes
    "congenital anomaly",
    "birth defect",
    "congenital malformation",

    # Critical-care / important medical-event signals
    "intensive care",
    "icu admission",
    "admitted to intensive care",
    "emergency room treatment",

    # Hospitalization
    "hospitalization",
    "hospitalized",
    "hospital admission",
    "admitted to hospital",
    "inpatient admission",
    "required hospitalization",
    "required hospital admission",
    "prolonged hospitalization",
    "prolonged hospital stay",
    "extended hospital stay",

    # ---- Safety Gate additions (reviewed gaps found when testing against the RF model) ----
    # Suicide / intentional self-harm
    "completed suicide",
    "suicide attempt",
    "attempted suicide",
    "intentional self-injury",
    "intentional self-harm",
    "intentional overdose",
    "deliberate overdose",
    "intentional product misuse overdose",

    # Infection / sepsis
    "sepsis",
    "septicaemia",
    "septicemia",
    "neutropenic sepsis",

    # Thromboembolic events
    "pulmonary embolism",
    "pulmonary embolus",
    "deep vein thrombosis",
    "deep venous thrombosis",
    "venous thromboembolism",
    "thromboembolism",

    # Stroke
    "stroke",
    "cerebrovascular accident",
    "ischaemic stroke",
    "ischemic stroke",
    "cva",

    # Kidney / liver failure
    "acute kidney injury",
    "acute renal failure",
    "renal failure",
    "kidney failure",
    "liver failure",
    "hepatic failure",
    "acute liver failure",
    "drug-induced liver injury",
    "liver injury",
    "hepatic necrosis",

    # Cardiac
    "cardiac failure",
    "heart failure",
    "cardiomyopathy",
    "unstable angina",
    "aortic dissection",

    # Pancreas / blood
    "pancreatitis",
    "febrile neutropenia",
    "agranulocytosis",
    "pancytopenia",
    "aplastic anaemia",
    "aplastic anemia",

    # General haemorrhage (British and American spellings)
    "haemorrhage",
    "hemorrhage",

    # Allergic airway swelling
    "angioedema",
    "laryngeal oedema",
    "laryngeal edema",
    "throat swelling",
    "tongue swelling",

    # Severe metabolic / lung
    "severe hypoglycaemia",
    "severe hypoglycemia",
    "interstitial lung disease",
    "pulmonary fibrosis"
]
# =========================================================
# CONTEXT PROTECTION PATTERNS
# =========================================================

NEGATION_PATTERNS = [
    "no",
    "not",
    "without",
    "denies",
    "denied",
    "did not",
    "does not",
    "doesn't",
    "didn't",
    "ruled out",
    "no evidence of"
]

HISTORY_PATTERNS = [
    "history of",
    "past history of",
    "previous history of",
    "previous",
    "prior",
    "history",
    "past",
    "in the past",
    "last year",
    "last month",
    "last week",
    "years ago",
    "months ago",
    "weeks ago",
    "days ago",
    "previously",
    "formerly",
    "earlier"
]


# =========================================================
# MODERATE REVIEW PATTERNS
# =========================================================

MODERATE_PATTERNS = [
    "requiring medical attention",
    "required medical attention",
    "medical attention",
    "requiring monitoring",
    "required monitoring",
    "under monitoring",
    "requiring evaluation",
    "required evaluation",
    "needs evaluation",
    "significant dizziness",
    "marked dizziness",
    "muscle pain and weakness",
    "muscle pain with weakness",
    "dehydration",

    # ---- Safety Gate additions: clinically meaningful, review recommended ----
    "overdose",
    "suicidal ideation",
    "suicidal thoughts",
    "self-harm",
    "self harm",
    "atrial fibrillation",
    "arrhythmia",
    "pneumonia",
    "hypoglycaemia",
    "hypoglycemia",
    "jaundice",
    "hepatotoxicity",
    "renal impairment",
    "osteonecrosis",
    "hip fracture",
    "thrombocytopenia",
    "neutropenia"
]

# Contextual moderate-review patterns.
# The terms persistent/prolonged/recurrent alone are intentionally
# not sufficient to assign MODERATE priority.
MODERATE_CONTEXT_PATTERNS = [
    "persistent stomach pain",
    "persistent vomiting",
    "persistent diarrhea",
    "persistent abdominal pain",
    "persistent muscle pain",
    "prolonged nausea",
    "prolonged dizziness",
    "prolonged vomiting",
    "recurrent dizziness",
    "recurrent abdominal pain",
    "recurrent vomiting",
    "recurrent diarrhea",
]


# =========================================================
# ADR INPUT VALIDATION
# =========================================================

# Common ADR/medical terms used in this project.
# These are used only to flag possible spelling/entry issues;
# the system does not silently correct the user's ADR text.
ADR_TERM_SUGGESTIONS = {
    "hepatotoxicity": ["hepatotoxcity", "hepatotoxicty", "hepatotoxity"],
    "neurotoxicity": ["neurotoxicty", "neurotoxcity", "neurotoxity"],
    "nephrotoxicity": ["nephrotoxicty", "nephrotoxcity", "nephrotoxity"],
    "cardiotoxicity": ["cardiotoxcity", "cardiotoxicty", "cardiotoxity"],
    "anaphylaxis": ["anaphylaxisx", "anaphylaxsis", "anaphylaxix"],
    "anaphylactic": ["anaphylactc", "anaphylacticc"],
    "respiratory distress": ["respiratory distres", "respiratory distrss"],
    "difficulty breathing": ["difficulty brething", "difficulty breathng"],
}


def validate_adr_input(adr_text):
    """
    Validate ADR text before safety screening and ML prediction.

    Returns:
        status: VALID, POSSIBLE_TYPO, or UNKNOWN
        suggestion: suggested medical term when available
        message: user-facing validation message

    The function does not silently modify the original ADR text.
    """
    text = " ".join(str(adr_text).lower().strip().split())

    if not text:
        return (
            "UNKNOWN",
            "",
            "ADR entry is empty. Please enter the reported adverse reaction."
        )

    # Exact recognized terms/patterns already used by PHARMAGUARD.
    recognized_patterns = SERIOUS_PATTERNS + MODERATE_PATTERNS
    for term in recognized_patterns:
        if re.search(rf"(?<!\w){re.escape(term.lower())}(?!\w)", text):
            return ("VALID", "", "ADR term recognized. Continue with analysis.")

    # Known possible spelling mistakes.
    for correct_term, typo_list in ADR_TERM_SUGGESTIONS.items():
        for typo in typo_list:
            if re.search(rf"(?<!\w){re.escape(typo)}(?!\w)", text):
                return (
                    "POSSIBLE_TYPO",
                    correct_term,
                    f"Possible spelling/medical-term error detected. Did you mean '{correct_term}'?"
                )

    # -----------------------------------------------------
    # NORMAL / UNKNOWN ADR
    # -----------------------------------------------------

    # Do not block a new or previously unseen ADR term.
    # The original ADR text is passed to the Safety Gate and ML model.

    return (
        "VALID",
        "",
        "ADR input accepted. Continue with analysis."
    )


def assess_information_completeness(patient_id, age, sex, drug, adr):
    """Check whether core ADR-report inputs are sufficiently populated.

    This is an information-quality alert only. It does not change
    Safety Gate or Random Forest priority.
    """
    missing = []

    if not str(patient_id).strip():
        missing.append("Patient ID")

    age_text = str(age).strip().lower()
    if age_text in {"", "nan", "none", "unknown"}:
        missing.append("Age")

    sex_text = str(sex).strip().lower()
    if sex_text in {"", "unknown", "nan", "none"}:
        missing.append("Sex")

    drug_text = str(drug).strip().lower()
    if drug_text in {"", "unknown", "nan", "none"}:
        missing.append("Suspected/reported drug")

    adr_text = " ".join(str(adr).strip().split())
    if not adr_text or adr_text.lower() in {"unknown", "none", "nan"}:
        missing.append("ADR description")

    return missing


# =========================================================
# SAVE DATA TO GOOGLE SHEET
# =========================================================

def _json_safe(value):
    """Convert pandas/NumPy scalar values into standard JSON-safe Python values."""
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if hasattr(value, "item"):
        try:
            return _json_safe(value.item())
        except Exception:
            pass
    return value


def save_to_google_sheet(data, return_details=False):
    """POST one record to the database endpoint; True only if it was really accepted."""

    def _result(ok, status=None, text=""):
        return (ok, status, text[:500]) if return_details else ok

    if not GOOGLE_SHEET_URL:
        return _result(False, None, "GOOGLE_SHEET_URL is not configured.")

    try:
        response = requests.post(
            GOOGLE_SHEET_URL,
            json=_json_safe(data),
            timeout=15,
        )
        ok = response.status_code in {200, 201}

        # Apps Script often answers HTTP 200 even when the script failed,
        # so also honour an explicit failure flag in the JSON body.
        if ok:
            try:
                body = response.json()
                if isinstance(body, dict) and (
                    body.get("success") is False or body.get("error")
                ):
                    ok = False
            except ValueError:
                pass  # plain-text reply: HTTP status is all we have

        if not ok:
            logger.warning("Database save rejected: HTTP %s", response.status_code)
        return _result(ok, response.status_code, response.text or "")

    except requests.RequestException as exc:
        logger.warning("Database save failed: %s", exc)
        return _result(False, None, str(exc))


def make_case_reference(now=None):
    """Collision-resistant case reference (timestamp + random suffix)."""
    now = now or datetime.now()
    return f"PHG-CASE-{now.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8].upper()}"


# =========================================================
# LOAD DATA FROM GOOGLE SHEET
# =========================================================

@st.cache_data(ttl=60, show_spinner=False)
def _fetch_sheet_records():
    """Cached raw fetch. Raises on failure so errors are never cached as 'empty'."""
    response = requests.get(GOOGLE_SHEET_URL, timeout=8)
    response.raise_for_status()
    return response.json()


def load_from_google_sheet():
    """Return the database as a DataFrame; failures are recorded, not hidden."""
    st.session_state["sheet_load_error"] = ""
    if not GOOGLE_SHEET_URL:
        st.session_state["sheet_load_error"] = "Database URL is not configured."
        return pd.DataFrame()
    try:
        df = pd.DataFrame(_fetch_sheet_records())
        # Sheets return numeric-looking IDs as numbers; keep IDs as text so
        # mixed int/str columns don't trigger Arrow conversion errors.
        for id_col in ("Patient_ID", "Case_Reference"):
            if id_col in df.columns:
                df[id_col] = df[id_col].astype(str)
        return df
    except Exception as exc:
        logger.warning("Database load failed: %s", exc)
        st.session_state["sheet_load_error"] = (
            "The case database could not be reached, so saved cases may be missing."
        )
        return pd.DataFrame()


def invalidate_sheet_cache():
    """Drop only the database cache (not every cache in the app)."""
    try:
        _fetch_sheet_records.clear()
    except Exception:
        pass


# =========================================================
# TEXT MATCHING FUNCTION
# =========================================================

def matches(text, patterns):

    text = " ".join(
        str(text).lower().strip().split()
    )

    matched_patterns = []

    for pattern in patterns:

        pattern = str(pattern).lower().strip()

        if re.search(
            rf"(?<!\w){re.escape(pattern)}(?!\w)",
            text
        ):
            matched_patterns.append(pattern)

    return matched_patterns


def prioritize_specific_moderate_hits(hits):

    # Prefer contextual clinical phrases over generic review phrases.
    # This changes only the explanation text, not the priority decision.
    generic = {
        "medical attention",
        "requiring monitoring",
        "required monitoring",
        "under monitoring",
        "requiring evaluation",
        "required evaluation",
        "needs evaluation",
    }

    hits = list(dict.fromkeys(hits))

    specific = [
        pattern
        for pattern in hits
        if pattern not in generic
    ]

    return specific if specific else hits


def remove_redundant_hits(hits):

    # Keep the most specific matched phrase when one matched
    # phrase is fully contained inside a longer matched phrase.
    # Example: "anaphylactic shock" + "shock" ->
    # "anaphylactic shock" only.
    ordered = sorted(
        list(dict.fromkeys(hits)),
        key=len,
        reverse=True
    )

    filtered = []

    for pattern in ordered:

        if not any(
            pattern != existing
            and re.search(
                rf"(?<!\w){re.escape(pattern)}(?!\w)",
                existing
            )
            for existing in filtered
        ):
            filtered.append(pattern)

    # Restore original detection order while removing exact duplicates.
    return list(dict.fromkeys(
        pattern
        for pattern in hits
        if pattern in filtered
    ))


def has_nonmedical_shock_context(text):

    text = " ".join(
        str(text).lower().strip().split()
    )

    # The generic word "shock" can occur in non-medical contexts.
    # These phrases should not create a pharmacovigilance HIGH signal.
    nonmedical_patterns = [
        "shell shock",
        "shock-like",
        "shock like",
        "electric shock",
        "electrical shock",
        "emotional shock",
        "psychological shock",
        "shock absorber",
        "shock wave",
        "shockwave",
    ]

    return any(
        re.search(
            rf"(?<!\w){re.escape(pattern)}(?!\w)",
            text
        )
        for pattern in nonmedical_patterns
    )


def has_death_causality_protection(text, serious_pattern):

    # Death/fatality terms may describe an unrelated event, an
    # underlying disease, an accident, or another non-drug cause.
    # Protect these contexts while preserving genuine ADR risk signals.
    pattern = str(serious_pattern).lower().strip()

    death_patterns = {
        "death",
        "died",
        "fatal",
        "fatal outcome",
        "fatal reaction",
    }

    if pattern not in death_patterns:
        return False

    text = " ".join(
        str(text).lower().strip().split()
    )

    unrelated_patterns = [
        # Explicitly unrelated to the medicinal product.
        r"\b(?:death|died|fatal(?:\s+outcome|\s+reaction)?)\b.{0,80}\b(?:unrelated|not\s+related|not\s+due)\b.{0,40}\b(?:drug|treatment|medication|therapy|adr)\b",
        r"\b(?:unrelated|not\s+related|not\s+due)\b.{0,40}\b(?:drug|treatment|medication|therapy|adr)\b.{0,80}\b(?:death|died|fatal(?:\s+outcome|\s+reaction)?)\b",

        # Death attributed to an underlying/non-drug cause.
        r"\b(?:death|died)\b.{0,50}\b(?:from|due\s+to|caused\s+by)\b.{0,50}\b(?:underlying|pre[-\s]?existing)\s+(?:disease|condition|illness)\b",
        r"\b(?:death|died)\b.{0,70}\b(?:from|due\s+to|caused\s+by)\b.{0,70}\b(?:myocardial\s+infarction|heart\s+attack|stroke|accident|trauma|injury|infection|sepsis)\b",
        r"\b(?:cause|reason)\s+of\s+death\b.{0,80}\b(?:unrelated|not\s+related|not\s+due)\b.{0,40}\b(?:drug|treatment|medication|therapy|adr)\b",

        # Fatal event explicitly unrelated to treatment.
        r"\bfatal(?:\s+outcome|\s+reaction)?\b.{0,80}\b(?:unrelated|not\s+related|not\s+due)\b.{0,40}\b(?:drug|treatment|medication|therapy|adr)\b",

        # Accident/trauma deaths unrelated to treatment.
        r"\b(?:died|death)\b.{0,60}\b(?:traffic|road|motor\s+vehicle|vehicle)\s+accident\b.{0,60}\b(?:unrelated|not\s+related)\b",
    ]

    return any(
        re.search(pattern, text)
        for pattern in unrelated_patterns
    )


def has_context_protection(text, serious_pattern):

    text = " ".join(
        str(text).lower().strip().split()
    )

    serious_pattern = str(serious_pattern).lower().strip()

    # -----------------------------------------------------
    # CONTEXT PROTECTION — MULTIPLE-OCCURRENCE SAFE VERSION
    # -----------------------------------------------------
    # Evaluate every occurrence of the serious phrase.
    # This prevents a historical occurrence from suppressing
    # a later current occurrence in the same ADR report.
    # Example:
    #   "History of seizure; patient developed seizure"
    # The first seizure is historical, but the second is current.
    # Therefore the overall signal must remain detectable.
    # -----------------------------------------------------

    clauses = re.split(
        r"(?<=[.!?;,])\s+|\s+(?:but|however|although|though|yet|except)\s+",
        text
    )

    found_occurrence = False
    protected_occurrence = False

    for clause in clauses:

        clause = clause.strip()

        for match in re.finditer(
            rf"(?<!\w){re.escape(serious_pattern)}(?!\w)",
            clause
        ):

            found_occurrence = True

            before = clause[:match.start()].strip()
            after = clause[match.end():].strip()

            before_tokens = before.split()
            after_tokens = after.split()

            nearby_before = " ".join(before_tokens[-10:])
            nearby_after = " ".join(after_tokens[:10])

            is_protected = False

            # Negation / ruled-out context before the phrase.
            for pattern in NEGATION_PATTERNS:
                if re.search(
                    rf"(?<!\w){re.escape(pattern)}(?!\w)",
                    nearby_before
                ):
                    is_protected = True
                    break

            # Negation / ruled-out context after the phrase.
            if not is_protected:
                for pattern in NEGATION_PATTERNS:
                    if re.search(
                        rf"(?<!\w){re.escape(pattern)}(?!\w)",
                        nearby_after
                    ):
                        is_protected = True
                        break

            # Historical / previous-event context before or after the phrase.
            # Temporal phrases such as "last year", "in the past", and "years ago"
            # are treated as historical context for this safety-gate occurrence.
            if not is_protected:
                for pattern in HISTORY_PATTERNS:
                    if re.search(
                        rf"(?<!\w){re.escape(pattern)}(?!\w)",
                        nearby_before
                    ) or re.search(
                        rf"(?<!\w){re.escape(pattern)}(?!\w)",
                        nearby_after
                    ):
                        is_protected = True
                        break

            if is_protected:
                protected_occurrence = True
            else:
                # At least one current/unprotected occurrence exists.
                return False

    if found_occurrence and protected_occurrence:
        return True

    return False


# =========================================================
# MACHINE LEARNING PREDICTION
# =========================================================

@st.cache_data(show_spinner=False, max_entries=1024)
def model_predict(age, sex, drug, adr):
    """Random Forest prototype prediction (cached: same inputs -> same output)."""
    X = pd.DataFrame([{
        "Age": age,
        # The model was trained on upper-case drug names and sex codes (FAERS style)
        "Sex": str(sex).strip().upper() or "UNKNOWN",
        "Drug": str(drug).strip().upper(),
        "ADR": adr,
        "Age_Missing": int(pd.isna(age)),
        "Drug_Missing": int(not str(drug).strip()),
        "ADR_Missing": int(not str(adr).strip()),
    }])

    # Model package with a separate preprocessor
    if isinstance(model, dict):
        estimator = model.get("model") or model.get("estimator")
        preprocessor = model.get("preprocessor")
        if estimator is not None and preprocessor is not None:
            try:
                return str(estimator.predict(preprocessor.transform(X))[0]).upper()
            except Exception:
                logger.exception("Packaged model prediction failed; trying direct predict.")

    # Direct model prediction
    try:
        return str(model.predict(X)[0]).upper()
    except Exception:
        logger.exception("Model prediction failed; returning UNKNOWN.")
        return "UNKNOWN"


# =========================================================
# INNOVATION 1 — SAFETY-FIRST PRIORITY ENGINE
# =========================================================

def evaluate_adr_priority(age, sex, drug, adr):
    """Run the same PHARMAGUARD priority engine for new or reassessed cases."""
    serious_matches = matches(adr, SERIOUS_PATTERNS)
    serious_hits = [
        pattern for pattern in serious_matches
        if not has_context_protection(adr, pattern)
        and not has_death_causality_protection(adr, pattern)
        and not (
            pattern == "shock"
            and has_nonmedical_shock_context(adr)
        )
    ]
    serious_hits = remove_redundant_hits(serious_hits)

    moderate_matches = matches(adr, MODERATE_PATTERNS)
    moderate_context_matches = matches(adr, MODERATE_CONTEXT_PATTERNS)
    moderate_hits = [
        pattern
        for pattern in (moderate_matches + moderate_context_matches)
        if not has_context_protection(adr, pattern)
    ]
    moderate_hits = remove_redundant_hits(moderate_hits)
    moderate_hits = prioritize_specific_moderate_hits(moderate_hits)

    if serious_hits:
        priority = "HIGH"
        flag = "Potentially serious medical event signal"
        reason = "Serious ADR indicator detected: " + ", ".join(serious_hits)
        recommendation = "Priority pharmacovigilance review required."
        decision_source = "Safety Gate — serious signal"
    elif moderate_hits:
        priority = "MODERATE"
        flag = "Non-serious but clinically meaningful review signal"
        reason = (
            "Project-defined moderate-review indicator detected: "
            + ", ".join(moderate_hits)
        )
        recommendation = (
            "Pharmacovigilance review and clinical assessment recommended."
        )
        decision_source = "Safety Gate — moderate signal"
    else:
        priority = model_predict(age, sex, drug, adr)
        if priority not in {"LOW", "MODERATE", "HIGH"}:
            priority = "UNKNOWN"
        flag = "No predefined serious signal detected"
        reason = "Priority assigned by the Random Forest prototype."
        recommendation = (
            "Routine pharmacovigilance review according to the project workflow."
        )
        decision_source = "Random Forest prototype"

    return (
        priority,
        flag,
        reason,
        recommendation,
        decision_source,
        serious_hits,
        moderate_hits,
    )

# =========================================================
# SESSION HISTORY
# =========================================================

if "adr_history" not in st.session_state:

    st.session_state.adr_history = []


# =========================================================
# LOAD PERMANENT DATABASE ONCE
# =========================================================

def _retry_database_load():
    invalidate_sheet_cache()
    st.session_state.pop("database_loaded", None)


if "database_loaded" not in st.session_state:

    database_df = load_from_google_sheet()

    if not database_df.empty:

        st.session_state.adr_history = (
            database_df.to_dict("records")
        )

    st.session_state.database_loaded = True

if st.session_state.get("sheet_load_error"):
    st.sidebar.warning(st.session_state["sheet_load_error"])
    st.sidebar.button("🔄 Retry database load", on_click=_retry_database_load)


# =========================================================
# SCREEN RENDERERS
# =========================================================

def _priority_counts(df):
    if df.empty or "Priority" not in df.columns:
        return {"HIGH": 0, "MODERATE": 0, "LOW": 0}
    s = df["Priority"].astype(str).str.upper()
    return {
        "HIGH": int((s == "HIGH").sum()),
        "MODERATE": int((s == "MODERATE").sum()),
        "LOW": int((s == "LOW").sum())
    }


def render_dashboard_screen():
    """Clean mobile-first dashboard: actions, compact KPIs and recent case cards."""
    df = pd.DataFrame(st.session_state.get("adr_history", []))
    counts = _priority_counts(df)

    # =====================================================
    # QUICK ACTIONS
    # =====================================================
    st.markdown("### Quick Actions")
    q1, q2, q3 = st.columns(3)

    with q1:
        if st.button("➕  New ADR Analysis", use_container_width=True):
            st.session_state["active_page"] = "🔍 New ADR Analysis"
            st.rerun()

    with q2:
        if st.button("📂  View Cases", use_container_width=True):
            st.session_state["active_page"] = "📂 Cases"
            st.rerun()

    with q3:
        if st.button("📊  View Analytics", use_container_width=True):
            st.session_state["active_page"] = "📊 Analytics"
            st.rerun()

    # =====================================================
    # CASE OVERVIEW — TRUE 2 x 2 RESPONSIVE GRID
    # =====================================================
    st.markdown("### Case Overview")
    overview_cards = [
        ("📋", "Total Cases", len(df), "Recorded ADR reports", "total"),
        ("🔴", "High Priority", counts["HIGH"], "Priority review", "high"),
        ("🟡", "Moderate", counts["MODERATE"], "Clinical review signal", "moderate"),
        ("🟢", "Low Priority", counts["LOW"], "Routine review", "low"),
    ]
    cards_html = []
    for icon, label, value, note, kind in overview_cards:
        cards_html.append(f'''<div class="pg-kpi-grid-card pg-kpi-{kind}">
<div class="pg-kpi-grid-icon">{icon}</div>
<div class="pg-kpi-grid-label">{html.escape(str(label))}</div>
<div class="pg-kpi-grid-value">{html.escape(str(value))}</div>
<div class="pg-kpi-grid-note">{html.escape(str(note))}</div>
</div>''')
    st.markdown(
        '<div class="pg-kpi-grid">' + "".join(cards_html) + '</div>',
        unsafe_allow_html=True,
    )

    # =====================================================
    # RECENT CASES — MOBILE-FRIENDLY CARDS, NO HORIZONTAL SCROLL
    # =====================================================
    if df.empty:
        st.markdown(
            """<div class="pg-empty-state">
<div class="pg-empty-icon">📭</div>
<div class="pg-empty-title">No ADR Reports Yet</div>
<div class="pg-empty-text">Start a new ADR analysis to create your first PHARMAGUARD case.</div>
</div>""",
            unsafe_allow_html=True,
        )
        return

    st.markdown("### 🕐 Recent Cases")
    recent_cols = [c for c in ["Case_Reference", "Drug", "ADR", "Priority", "Date_Time"] if c in df.columns]
    recent_df = df[recent_cols].tail(3).iloc[::-1].copy()

    priority_class = {"HIGH": "pg-priority-high", "MODERATE": "pg-priority-moderate", "LOW": "pg-priority-low"}
    priority_icon = {"HIGH": "🔴", "MODERATE": "🟡", "LOW": "🟢"}
    recent_cards = []
    for _, row in recent_df.iterrows():
        case_ref = html.escape(str(row.get("Case_Reference", "—")))
        drug_raw = row.get("Drug", "")
        drug_text = str(drug_raw).strip()
        drug = html.escape(drug_text if drug_text and drug_text.lower() not in {"nan", "none", "null"} else "Not reported")
        adr = html.escape(str(row.get("ADR", "—")))
        priority = str(row.get("Priority", "UNKNOWN")).upper().strip()
        pclass = priority_class.get(priority, "pg-priority-unknown")
        picon = priority_icon.get(priority, "⚪")
        dt = html.escape(str(row.get("Date_Time", "")))
        recent_cards.append(f'''<div class="pg-recent-card">
<div class="pg-recent-ref" title="{case_ref}">{case_ref}</div>
<div class="pg-recent-drug">💊 {drug}</div>
<div class="pg-recent-adr">{adr}</div>
<div class="pg-recent-bottom">
<span class="pg-priority-badge {pclass}">{picon} {html.escape(priority)}</span>
<span class="pg-recent-date">{dt}</span>
</div>
</div>''')

    st.markdown('<div class="pg-recent-grid">' + "".join(recent_cards) + '</div>', unsafe_allow_html=True)

    if st.button("📂 View All Cases →", use_container_width=True, key="dashboard_view_all_cases"):
        st.session_state["active_page"] = "📂 Cases"
        st.rerun()

    st.markdown(
        """<div class="pg-dashboard-info">
<div class="pg-info-title">🛡️ Safety-first review support</div>
<div class="pg-info-text">PHARMAGUARD combines a predefined Safety Gate with a Random Forest prototype to support pharmacovigilance review prioritization.</div>
<div class="pg-info-note">Review priority only • Proof of Concept</div>
</div>""",
        unsafe_allow_html=True,
    )

def render_history_screen():
    """Professional, mobile-first case history view. Backend and saved records are unchanged."""
    df = pd.DataFrame(st.session_state.get("adr_history", []))
    st.markdown(textwrap.dedent("""
    <div class="pg-cases-section-head">
        <div><div class="pg-cases-section-title">📋 Case History</div><div class="pg-cases-section-sub">Search, filter and open saved ADR cases for detailed review.</div></div>
        <div class="pg-cases-section-chip">Saved records</div>
    </div>
    """).strip(), unsafe_allow_html=True)
    if df.empty:
        st.markdown(textwrap.dedent("""
        <div class="pg-empty-state"><div class="pg-empty-icon">📭</div><div class="pg-empty-title">No ADR cases available</div><div class="pg-empty-text">Completed ADR analyses will appear here after they are saved.</div></div>
        """).strip(), unsafe_allow_html=True)
        return
    counts=_priority_counts(df)
    overview=[("📋","Total",len(df),"All saved cases","total"),("🔴","HIGH",counts["HIGH"],"Priority review","high"),("🟡","MODERATE",counts["MODERATE"],"Clinical review","moderate"),("🟢","LOW",counts["LOW"],"Routine review","low")]
    cards=[]
    for icon,label,value,note,kind in overview:
        cards.append(f'<div class="pg-case-kpi pg-case-kpi-{kind}"><div class="pg-case-kpi-icon">{icon}</div><div class="pg-case-kpi-label">{html.escape(str(label))}</div><div class="pg-case-kpi-value">{html.escape(str(value))}</div><div class="pg-case-kpi-note">{html.escape(str(note))}</div></div>')
    st.markdown('<div class="pg-case-kpi-grid">'+''.join(cards)+'</div>',unsafe_allow_html=True)
    st.markdown("### 🔎 Find a Case")
    c1,c2=st.columns([2,1])
    with c1:
        q=st.text_input("Search cases",placeholder="Case ID, patient ID, drug, ADR or priority...",label_visibility="collapsed",key="cases_history_search").strip().lower()
    with c2:
        priority_filter=st.selectbox("Priority filter",["All","HIGH","MODERATE","LOW"],label_visibility="collapsed",key="cases_history_priority")
    filtered=df.copy()
    if q:
        mask=pd.Series(False,index=filtered.index)
        for col in ["Case_Reference","Patient_ID","Drug","ADR","Priority"]:
            if col in filtered.columns:
                mask=mask | filtered[col].astype(str).str.lower().str.contains(re.escape(q),na=False)
        filtered=filtered[mask]
    if priority_filter!="All" and "Priority" in filtered.columns:
        filtered=filtered[filtered["Priority"].astype(str).str.upper()==priority_filter]
    st.caption(f"Showing {len(filtered)} of {len(df)} cases")
    if filtered.empty:
        st.info("No cases match the current search or priority filter.")
    else:
        priority_class={"HIGH":"pg-case-priority-high","MODERATE":"pg-case-priority-moderate","LOW":"pg-case-priority-low"}
        priority_icon={"HIGH":"🔴","MODERATE":"🟡","LOW":"🟢"}
        cards=[]
        for idx,row in filtered.sort_index(ascending=False).head(5).iterrows():
            ref=html.escape(str(row.get("Case_Reference",f"Case {idx+1}")))
            patient=html.escape(str(row.get("Patient_ID","—")))
            drug_raw=str(row.get("Drug","")).strip(); drug=html.escape(drug_raw if drug_raw and drug_raw.lower() not in {"nan","none","null"} else "Not reported")
            adr=html.escape(str(row.get("ADR","—")))
            priority=str(row.get("Priority","UNKNOWN")).upper().strip(); badge=priority_class.get(priority,"pg-case-priority-unknown"); icon=priority_icon.get(priority,"⚪")
            dt=html.escape(str(row.get("Date_Time","—")))
            cards.append(f'<div class="pg-case-history-card"><div class="pg-case-history-top"><div class="pg-case-history-ref">{ref}</div><span class="{badge}">{icon} {html.escape(priority)}</span></div><div class="pg-case-history-drug">💊 {drug}</div><div class="pg-case-history-adr">{adr}</div><div class="pg-case-history-meta"><span>👤 {patient}</span><span>🕒 {dt}</span></div></div>')
        st.markdown('<div class="pg-case-history-list">'+''.join(cards)+'</div>',unsafe_allow_html=True)
        if len(filtered)>5:
            st.caption(f"Showing the 5 most recent matching cases above. {len(filtered)-5} additional cases remain available in the table view.")
        with st.expander("📑 Full Table View",expanded=False):
            st.markdown("""<div class="pg-expand-workspace-intro"><div class="pg-expand-workspace-title">Complete Case History</div><div class="pg-expand-workspace-sub">Browse the complete filtered record set in a structured review table. Use this workspace when you need case-level detail beyond the five recent cards.</div><span class="pg-expand-status">CASE HISTORY • FULL RECORDS</span></div>""", unsafe_allow_html=True)

            table_df = filtered.copy()
            display_cols=[c for c in ["Case_Reference","Patient_ID","Drug","ADR","Priority","Seriousness","Decision_Source","Date_Time"] if c in table_df.columns]

            st.markdown(
                f"""<div class="pg-expand-mini-summary">
                    <div><strong>{len(table_df):,}</strong><span>Filtered records</span></div>
                    <div><strong>{len(display_cols)}</strong><span>Visible fields</span></div>
                    <div><strong>Read-only</strong><span>Review workspace</span></div>
                </div>""",
                unsafe_allow_html=True
            )

            if table_df.empty:
                st.markdown("""<div class="pg-empty-state"><strong>📭 No matching records</strong><br>Adjust the search or priority filter to view available ADR cases.</div>""", unsafe_allow_html=True)
            else:
                st.caption("Tip: use Search and Priority Filter above to narrow the table before detailed review.")
                st.dataframe(
                    table_df[display_cols].sort_index(ascending=False),
                    use_container_width=True,
                    hide_index=True
                )
    st.download_button("⬇️ Export Filtered CSV",data=filtered.to_csv(index=False).encode("utf-8"),file_name="PHARMAGUARD_Filtered_ADR_History.csv",mime="text/csv",use_container_width=True,key="cases_history_export")

def _display_decision_source(row):
    """Return a readable decision source, including a safe fallback for legacy records."""
    source = str(row.get("Decision_Source", "") or "").strip()
    if source:
        return source

    reason = str(row.get("Reason", "") or "").strip().lower()
    if "serious adr indicator detected" in reason:
        return "Safety Gate — serious signal"
    if "project-defined moderate-review indicator detected" in reason:
        return "Safety Gate — moderate signal"
    if "priority assigned by the random forest prototype" in reason:
        return "Random Forest prototype"

    return "Not recorded"


def render_case_reports_screen():
    st.markdown(
        textwrap.dedent("""
        <div class="pg-report-hero">
            <div class="pg-report-kicker">PHARMAGUARD • CASE REVIEW</div>
            <div class="pg-report-title">📄 Case Report</div>
            <div class="pg-report-sub">Review one saved ADR case in a structured format. The original database record remains unchanged while reassessments are stored as linked versions.</div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    df = pd.DataFrame(st.session_state.get("adr_history", []))

    if df.empty:
        st.markdown(
            textwrap.dedent("""
            <div class="pg-section-card">
                <h4>📭 No case reports available</h4>
                <div>Analyze and save an ADR case first. The saved case will appear here for report generation.</div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )
        return

    labels = []
    for idx, row in df.iterrows():
        ref = str(row.get("Case_Reference", f"Case {idx + 1}"))
        drug_name = str(row.get("Drug", "Unknown"))
        adr_text = str(row.get("ADR", ""))
        labels.append((idx, f"{ref} | {drug_name} | {adr_text[:55]}"))

    selected_label = st.selectbox(
        "Select case to review",
        [x[1] for x in labels],
        help="Select the ADR case for report preview and export."
    )
    selected_idx = next(i for i, label in labels if label == selected_label)
    row = df.loc[selected_idx]

    priority = str(row.get("Priority", "UNKNOWN")).upper()
    seriousness = str(row.get("Seriousness", "Uncertain"))
    decision_source = _display_decision_source(row)
    reason = str(row.get("Reason", ""))
    recommendation = {
        "HIGH": "Priority pharmacovigilance review required.",
        "MODERATE": "Pharmacovigilance review and clinical assessment recommended.",
        "LOW": "Routine pharmacovigilance review according to the project workflow."
    }.get(priority, "Additional information or professional review may be required.")

    badge_class = {
        "HIGH": "pg-high",
        "MODERATE": "pg-moderate",
        "LOW": "pg-low"
    }.get(priority, "pg-uncertain")

    st.markdown(
        textwrap.dedent(f"""
        <div class="pg-case-card">
            <div class="pg-case-ref">CASE REFERENCE • {html.escape(str(row.get("Case_Reference", "")))}</div>
            <div class="pg-case-title">{html.escape(str(row.get("Drug", "Not reported")))} — ADR Review</div>
            <div style="margin-top:10px;">
                <span class="pg-priority {badge_class}">{html.escape(priority)} PRIORITY</span>
            </div>
            <div class="pg-case-grid">
                <div class="pg-case-field"><div class="pg-case-label">Patient / Project ID</div><div class="pg-case-value">{html.escape(str(row.get("Patient_ID", "—")))}</div></div>
                <div class="pg-case-field"><div class="pg-case-label">Reported ADR</div><div class="pg-case-value">{html.escape(str(row.get("ADR", "—")))}</div></div>
                <div class="pg-case-field"><div class="pg-case-label">Date & Time</div><div class="pg-case-value">{html.escape(str(row.get("Date_Time", "—")))}</div></div>
                <div class="pg-case-field"><div class="pg-case-label">Age / Sex</div><div class="pg-case-value">{html.escape(str(row.get("Age", "—")))} / {html.escape(str(row.get("Sex", "—")))}</div></div>
            </div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    st.markdown("### 💊 ADR Information")
    st.markdown('<div class="pg-report-section-sub">The reported medicinal product and reaction recorded for this case.</div>', unsafe_allow_html=True)
    st.markdown(
        textwrap.dedent(f"""
        <div class="pg-section-card">
            <div class="pg-case-label">Reported Drug</div>
            <div class="pg-case-title">{html.escape(str(row.get("Drug", "")))}</div>
            <div style="margin-top:12px;"><div class="pg-case-label">Reported ADR</div><div class="pg-case-value">{html.escape(str(row.get("ADR", "")))}</div></div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    st.markdown("### 🧠 Priority Decision")
    st.markdown('<div class="pg-report-section-sub">A transparent summary of how PHARMAGUARD assigned the review priority.</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            textwrap.dedent(f"""
            <div class="pg-report-decision">
                <h4>🔎 PHARMAGUARD Assessment</h4>
                <div class="pg-report-decision-grid">
                    <div class="pg-report-decision-item"><div class="pg-report-decision-label">Priority</div><div class="pg-report-decision-value">{html.escape(priority)}</div></div>
                    <div class="pg-report-decision-item"><div class="pg-report-decision-label">Seriousness</div><div class="pg-report-decision-value">{html.escape(seriousness)}</div></div>
                    <div class="pg-report-decision-item"><div class="pg-report-decision-label">Decision Source</div><div class="pg-report-decision-value">{html.escape(decision_source)}</div></div>
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            textwrap.dedent(f"""
            <div class="pg-report-why">
                <h4>🧠 Why this priority?</h4>
                <div>{html.escape(reason) if reason else "No reason recorded."}</div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

    st.markdown(
        textwrap.dedent(f"""
        <div class="pg-report-action">
            <h4>📌 Recommended Action</h4>
            <div>{html.escape(recommendation)}</div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    # =====================================================
    # INNOVATION 2 — PHARMACIST REVIEW CHECKLIST
    # =====================================================
    with st.expander("🧑‍⚕️ Pharmacist Review Checklist", expanded=False):
        st.markdown("""<div class="pg-expand-workspace-intro"><div class="pg-expand-workspace-title">Structured Pharmacist Review</div><div class="pg-expand-workspace-sub">Complete the key review checks before pharmacovigilance follow-up. This workspace records review progress only; it does not replace professional or regulatory assessment.</div><span class="pg-expand-status">CASE REVIEW • SESSION WORKSPACE</span></div>""", unsafe_allow_html=True)

        checklist_items = [
            ("patient_info", "Patient information reviewed"),
            ("drug_verified", "Suspected / reported drug verified"),
            ("adr_description", "ADR description reviewed"),
            ("seriousness_checked", "Seriousness criteria checked"),
            ("outcome_assessed", "Patient outcome assessed"),
            ("medical_info", "Relevant medical / clinical information reviewed"),
            ("follow_up", "Follow-up information required / considered"),
        ]

        checklist_state_key = f"review_checklist_{selected_idx}"
        if checklist_state_key not in st.session_state:
            st.session_state[checklist_state_key] = {key: False for key, _ in checklist_items}

        checklist_state = st.session_state[checklist_state_key]

        review_status_key = f"review_status_{selected_idx}"
        if review_status_key not in st.session_state:
            st.session_state[review_status_key] = "Not Started"

        completed_count = sum(bool(checklist_state.get(key, False)) for key, _ in checklist_items)
        total_count = len(checklist_items)
        progress_pct = round((completed_count / total_count) * 100) if total_count else 0
        current_review_status = st.session_state.get(review_status_key, "Not Started")
        st.markdown(f"""<div class="pg-expand-mini-summary"><div><strong>{completed_count}/{total_count}</strong><span>Checks completed</span></div><div><strong>{progress_pct}%</strong><span>Review progress</span></div><div><strong>{html.escape(current_review_status)}</strong><span>Workflow status</span></div></div>""", unsafe_allow_html=True)

        review_status = st.selectbox(
            "📝 Pharmacist Review Status",
            ["Not Started", "In Progress", "Completed"],
            key=review_status_key,
            help="Session-only workflow status for this prototype case."
        )

        if priority == "HIGH":
            st.warning(
                "🔴 HIGH-priority case: review the Safety Gate signal and complete the pharmacist checklist before follow-up."
            )
        elif priority == "MODERATE":
            st.info(
                "🟠 MODERATE-priority case: review the clinical context and complete the pharmacist checklist."
            )

        checklist_cols = st.columns(2)
        for i, (item_key, item_label) in enumerate(checklist_items):
            with checklist_cols[i % 2]:
                checklist_state[item_key] = st.checkbox(
                    item_label,
                    value=checklist_state.get(item_key, False),
                    key=f"{checklist_state_key}_{item_key}"
                )

        completed_count = sum(bool(checklist_state.get(key, False)) for key, _ in checklist_items)
        total_count = len(checklist_items)

        if completed_count == total_count and review_status != "Completed":
            st.caption("💡 All checklist items are complete. You can mark the review status as Completed.")
        reviewer_note = st.text_area(
            "Reviewer comments (optional)",
            key=f"reviewer_note_{selected_idx}",
            placeholder="Example: Seriousness reviewed; additional clinical follow-up may be required."
        )

        if completed_count == total_count:
            st.success(f"✅ Review checklist complete — {completed_count}/{total_count} items")
        else:
            st.info(f"📋 Review checklist progress — {completed_count}/{total_count} items completed")

        st.caption(
            "Prototype note: review status, checklist status and reviewer comments are maintained for the current app session and are not added to the Google Sheet database."
        )

        # =====================================================
    # INNOVATION 1 — DYNAMIC ADR RISK REASSESSMENT
    # =====================================================
    with st.expander("🔄 Dynamic ADR Risk Reassessment", expanded=False):
        st.markdown(
            """<div class="pg-expand-workspace-intro">
                <div class="pg-expand-workspace-title">Dynamic ADR Risk Reassessment</div>
                <div class="pg-expand-workspace-sub">Record new clinical information as a linked case version while preserving the original assessment and review history.</div>
                <span class="pg-expand-status">CASE REPORT • FOLLOW-UP WORKSPACE</span>
            </div>""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """<div class="pg-expand-mini-summary">
                <div><strong>Linked version</strong><span>Original case remains unchanged</span></div>
                <div><strong>Safety-first review</strong><span>Same PHARMAGUARD engine</span></div>
                <div><strong>Audit trail</strong><span>Previous and updated priorities retained</span></div>
            </div>""",
            unsafe_allow_html=True,
        )
        st.markdown(
        """
        <div class="pg-section-card">
            <h4>When should you reassess?</h4>
            <div>Use this workspace when follow-up information changes the clinical description of the ADR. PHARMAGUARD creates a new linked version instead of overwriting the original case.</div>
        </div>
        """,
        unsafe_allow_html=True
        )

        st.caption(
            "Example: an initial rash may later be followed by facial swelling or difficulty breathing. Enter the updated ADR information below."
        )
        reassessment_adr = st.text_area(
            "Updated ADR / new clinical information",
            value="",
            key=f"reassessment_adr_{selected_idx}",
            placeholder="Example: Rash progressed to facial swelling and difficulty breathing."
        )
        reassessment_note = st.text_input(
            "Follow-up note (optional)",
            key=f"reassessment_note_{selected_idx}",
            placeholder="Example: Follow-up information received from the clinical team."
        )

        if st.button(
            "🔄 Reassess & Create New Version",
            key=f"reassess_button_{selected_idx}",
            use_container_width=True,
            type="primary"
        ):
            if not reassessment_adr.strip():
                st.warning("Please enter the updated ADR / new clinical information.")
            else:
                validation_status, suggestion, validation_message = validate_adr_input(
                    reassessment_adr
                )

                if validation_status == "POSSIBLE_TYPO":
                    st.warning(validation_message)
                elif validation_status == "UNKNOWN":
                    st.warning(validation_message)
                else:
                    (
                        new_priority,
                        new_flag,
                        new_reason,
                        new_recommendation,
                        new_decision_source,
                        _,
                        _,
                    ) = evaluate_adr_priority(
                        row.get("Age", ""),
                        row.get("Sex", "Unknown"),
                        row.get("Drug", ""),
                        reassessment_adr,
                    )

                    previous_reference = str(
                        row.get("Case_Reference", "")
                    )
                    original_reference = str(
                        row.get("Original_Case_Reference", "")
                        or previous_reference
                    )

                    existing_records = st.session_state.get(
                        "adr_history", []
                    )
                    reassessment_count = sum(
                        str(item.get("Original_Case_Reference", ""))
                        == original_reference
                        for item in existing_records
                    )
                    if str(row.get("Original_Case_Reference", "")) == original_reference:
                        reassessment_number = reassessment_count + 1
                    else:
                        reassessment_number = 1

                    reassess_now = datetime.now()
                    new_case_reference = make_case_reference(reassess_now)

                    new_record = {
                        "Date_Time": reassess_now.strftime("%Y-%m-%d %H:%M:%S"),
                        "Patient_ID": row.get("Patient_ID", ""),
                        "Age": row.get("Age", ""),
                        "Sex": row.get("Sex", "Unknown"),
                        "Drug": row.get("Drug", ""),
                        "ADR": reassessment_adr.strip(),
                        "Seriousness": (
                            "Yes" if new_priority == "HIGH"
                            else "No" if new_priority in {"MODERATE", "LOW"}
                            else "Uncertain"
                        ),
                        "Decision_Source": new_decision_source,
                        "Priority": new_priority,
                        "Reason": new_reason,
                        "Case_Reference": new_case_reference,
                        "Reassessment_Of": previous_reference,
                        "Original_Case_Reference": original_reference,
                        "Reassessment_Number": reassessment_number,
                        "Previous_Priority": priority,
                        "Follow_Up_Note": reassessment_note.strip(),
                    }

                    # Show the reassessment result independently of database saving.
                    # This prevents a database/API failure from hiding the Safety Gate result.
                    st.markdown(
                        f"""<div class="pg-reassess-result">
                            <div class="pg-reassess-result-title">📋 Reassessment Result</div>
                            <div><b>Previous priority:</b> {html.escape(str(priority))} &nbsp;→&nbsp; <b>Updated priority:</b> {html.escape(str(new_priority))}</div>
                            <div><b>Decision source:</b> {html.escape(str(new_decision_source))}</div>
                            <div><b>Detected signal:</b> {html.escape(str(new_reason))}</div>
                            <div><b>Recommended action:</b> {html.escape(str(new_recommendation))}</div>
                        </div>""",
                        unsafe_allow_html=True,
                    )

                    saved, save_status, save_response = save_to_google_sheet(
                        new_record,
                        return_details=True
                    )

                    if saved:
                        invalidate_sheet_cache()

                        st.session_state.adr_history.append(new_record.copy())

                        st.success(
                            f"✅ Reassessment saved. {previous_reference} → "
                            f"{new_case_reference} ({priority} → {new_priority})"
                        )

                        if priority != new_priority:
                            st.warning(
                                f"🔺 Review priority changed from **{priority}** to "
                                f"**{new_priority}** based on the updated information."
                            )
                        else:
                            st.info(
                                f"Priority remains **{new_priority}** after reassessment."
                            )

                    else:
                        st.error(
                            "❌ Reassessment was analyzed, but the database save failed."
                        )
                        if save_status is not None:
                            st.caption(f"Database response status: HTTP {save_status}")
                        if save_response:
                            st.code(save_response)
                        st.info(
                            "The reassessment result above is still the PHARMAGUARD engine result. "
                            "Only the database save failed. Use the HTTP response above to identify the server-side issue."
                        )

    with st.expander("📈 ADR Priority Timeline", expanded=False):
        st.markdown(
            """<div class="pg-expand-workspace-intro">
            <div class="pg-expand-workspace-title">Priority Decision Timeline</div>
            <div class="pg-expand-workspace-sub">A professional version-by-version view of how the recorded ADR priority evolved during reassessment.</div>
            <span class="pg-expand-status">CASE HISTORY • VERSION CONTROL</span>
            </div>""",
            unsafe_allow_html=True,
        )

        root_reference = str(
            row.get("Original_Case_Reference", "")
            or row.get("Case_Reference", "")
        ).strip()

        timeline_records = []
        for item in st.session_state.get("adr_history", []):
            item_original = str(item.get("Original_Case_Reference", "") or "").strip()
            item_case = str(item.get("Case_Reference", "") or "").strip()
            if root_reference and (
                item_original == root_reference or item_case == root_reference
            ):
                timeline_records.append(item)

        if timeline_records:
            timeline_records = sorted(
                timeline_records,
                key=lambda x: str(x.get("Date_Time", ""))
            )

            def _timeline_priority(value):
                p = str(value or "UNKNOWN").strip().upper()
                return p if p in {"HIGH", "MODERATE", "LOW"} else "UNKNOWN"

            def _timeline_version(item, index):
                reassess_no = str(item.get("Reassessment_Number", "") or "").strip()
                reassessment_of = str(item.get("Reassessment_Of", "") or "").strip()
                if reassess_no:
                    return f"Reassessment {reassess_no}"
                if reassessment_of:
                    return f"Reassessment {index}"
                return "Initial Report"

            priorities = [_timeline_priority(x.get("Priority")) for x in timeline_records]
            initial_priority = priorities[0] if priorities else "UNKNOWN"
            current_priority = priorities[-1] if priorities else "UNKNOWN"

            # Prefer explicit reassessment metadata. If old records lack it,
            # only the first linked record is treated as Initial Report.
            version_labels = []
            for idx, item in enumerate(timeline_records):
                if idx == 0:
                    version_labels.append("Initial Report")
                else:
                    reassess_no = str(item.get("Reassessment_Number", "") or "").strip()
                    version_labels.append(
                        f"Reassessment {reassess_no or idx}"
                    )

            st.markdown(
                f"""
                <div class="pg-timeline-summary">
                    <div class="pg-timeline-stat">
                        <div class="pg-timeline-stat-label">Recorded Versions</div>
                        <div class="pg-timeline-stat-value">{len(timeline_records)}</div>
                        <div class="pg-timeline-stat-note">Linked records for this case</div>
                    </div>
                    <div class="pg-timeline-stat">
                        <div class="pg-timeline-stat-label">Initial Priority</div>
                        <div class="pg-timeline-stat-value">{html.escape(initial_priority)}</div>
                        <div class="pg-timeline-stat-note">First recorded assessment</div>
                    </div>
                    <div class="pg-timeline-stat">
                        <div class="pg-timeline-stat-label">Current Priority</div>
                        <div class="pg-timeline-stat-value">{html.escape(current_priority)}</div>
                        <div class="pg-timeline-stat-note">Latest recorded assessment</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            note = (
                "Priority changed across the recorded case history."
                if initial_priority != current_priority
                else "No priority change is recorded across the linked versions shown below."
            )
            st.markdown(
                f"""<div class="pg-timeline-change">
                🔄 <strong>Priority trajectory:</strong>
                {html.escape(initial_priority)} &nbsp;→&nbsp;
                <strong>{html.escape(current_priority)}</strong><br>
                <span>{html.escape(note)}</span>
                </div>""",
                unsafe_allow_html=True,
            )

            st.markdown("### 🧾 Version-by-Version Record")

            # Native Streamlit renderer.
            # The previous dynamic HTML was being displayed literally on
            # some Streamlit/Android renders, so the timeline cards are now
            # built with native Streamlit containers and columns.
            for idx, item in enumerate(timeline_records):
                priority = _timeline_priority(item.get("Priority"))
                is_current = idx == len(timeline_records) - 1
                decision_source = str(
                    item.get("Decision_Source", "")
                    or item.get("Reason", "")
                    or "Not recorded"
                )

                with st.container(border=True):
                    left, right = st.columns([3.2, 1.0])

                    with left:
                        st.markdown(f"**{version_labels[idx]}**")

                    with right:
                        if priority == "HIGH":
                            st.error("HIGH", icon="🔴")
                        elif priority == "MODERATE":
                            st.warning("MODERATE", icon="🟡")
                        elif priority == "LOW":
                            st.success("LOW", icon="🟢")
                        else:
                            st.info("UNKNOWN", icon="⚪")

                    st.caption(f"🕒 {str(item.get('Date_Time', '') or '—')}")

                    if is_current:
                        st.info("CURRENT VERSION", icon="📌")

                    st.markdown("**ADR / New Information**")
                    st.write(str(item.get("ADR", "") or "—"))

                    st.markdown("**Decision Source**")
                    st.write(decision_source)

                    st.markdown("**Case Reference**")
                    st.code(
                        str(item.get("Case_Reference", "") or "—"),
                        language=None
                    )

                if idx < len(timeline_records) - 1:
                    st.markdown(
                        "<div style='text-align:center;font-size:20px;"
                        "line-height:1;margin:4px 0 8px;'>↓</div>",
                        unsafe_allow_html=True,
                    )

        else:
            st.info("No linked reassessment records are available for this case yet.")

    with st.expander("🔗 Longitudinal ADR Case Timeline", expanded=False):
        st.markdown("""<div class="pg-expand-workspace-intro"><div class="pg-expand-workspace-title">Longitudinal Case Timeline</div><div class="pg-expand-workspace-sub">Follow the complete case history across the initial report and linked reassessment versions.</div><span class="pg-expand-status">PHARMAGUARD WORKSPACE</span></div>""", unsafe_allow_html=True)
        # =========================================================
        # INNOVATION 3 — LONGITUDINAL ADR CASE TIMELINE
        # =========================================================
        # This summarizes the complete linked case journey without changing
        # any priority or clinical decision logic.
        if timeline_records:
            st.markdown("### 🔗 Longitudinal ADR Case Timeline")
            st.caption(
                "A version-by-version view of the same ADR case from the original report "
                "through reassessment. This is a record-tracking view, not a clinical outcome prediction."
            )

            first_record = timeline_records[0]
            latest_record = timeline_records[-1]
            first_priority = str(first_record.get("Priority", "UNKNOWN"))
            latest_priority = str(latest_record.get("Priority", "UNKNOWN"))

            tl1, tl2, tl3 = st.columns(3)
            with tl1:
                st.metric("📌 Versions", len(timeline_records))
            with tl2:
                st.metric("Initial Priority", first_priority)
            with tl3:
                st.metric("Current Priority", latest_priority)

            timeline_display = []
            for position, item in enumerate(timeline_records, start=1):
                reassessment_no = str(item.get("Reassessment_Number", "")).strip()
                version_label = "Initial Report" if not reassessment_no else f"Reassessment {reassessment_no}"
                timeline_display.append({
                    "Step": position,
                    "Version": version_label,
                    "Priority": item.get("Priority", "UNKNOWN"),
                    "ADR / New Information": item.get("ADR", ""),
                    "Decision Source": item.get("Decision_Source", ""),
                    "Date & Time": item.get("Date_Time", ""),
                })

            st.dataframe(
                pd.DataFrame(timeline_display),
                use_container_width=True,
                hide_index=True
            )

            if first_priority != latest_priority:
                st.info(
                    f"🔄 Priority changed across recorded versions: "
                    f"**{first_priority} → {latest_priority}**. "
                    "The change reflects the reassessment record and does not modify the original case version."
                )
            else:
                st.info(
                    f"ℹ️ Priority remained **{latest_priority}** across the recorded versions."
                )

    st.markdown("### 📥 Export Report")

    report_text = f"""PHARMAGUARD ADR CASE REPORT
========================================

AI-Assisted ADR Risk Prioritization System
Pharmacovigilance • Proof of Concept

1. CASE INFORMATION
----------------------------------------
Case Reference: {row.get("Case_Reference", "")}
Patient / Project ID: {row.get("Patient_ID", "")}
Age: {row.get("Age", "")}
Sex: {row.get("Sex", "")}
Date & Time: {row.get("Date_Time", "")}

2. DRUG / ADR INFORMATION
----------------------------------------
Drug: {row.get("Drug", "")}
ADR: {row.get("ADR", "")}

3. PHARMAGUARD ASSESSMENT
----------------------------------------
Priority: {priority}
Seriousness: {seriousness}
Decision Source: {decision_source}
Reason: {reason}

4. RECOMMENDED ACTION
----------------------------------------
{recommendation}

IMPORTANT DISCLAIMER
----------------------------------------
PHARMAGUARD is a proof-of-concept AI-assisted pharmacovigilance
review-prioritization system. It does not establish causality,
diagnosis, treatment, regulatory seriousness, or clinical
decision-making.

========================================
Generated by PHARMAGUARD
========================================
"""

    e1, e2 = st.columns(2)
    with e1:
        st.download_button(
            "⬇️ Download TXT Report",
            data=report_text,
            file_name=f"PHARMAGUARD_{row.get('Case_Reference', 'Case')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with e2:
        try:
            from io import BytesIO
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.enums import TA_CENTER
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

            pdf_buffer = BytesIO()
            pdf_doc = SimpleDocTemplate(
                pdf_buffer, pagesize=A4,
                rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
            )
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                "PGUI5Title", parent=styles["Title"],
                alignment=TA_CENTER, fontSize=18, spaceAfter=8
            )
            sub_style = ParagraphStyle(
                "PGUI5Sub", parent=styles["Normal"],
                alignment=TA_CENTER, fontSize=9, textColor=colors.grey, spaceAfter=14
            )
            normal = ParagraphStyle(
                "PGUI5Normal", parent=styles["BodyText"],
                fontSize=9, leading=12
            )

            def P(value):
                return Paragraph(html.escape(str(value)).replace("\n", "<br/>"), normal)

            story = [
                Paragraph("PHARMAGUARD ADR CASE REPORT", title_style),
                Paragraph("AI-Assisted ADR Risk Prioritization System • Pharmacovigilance Proof of Concept", sub_style)
            ]
            data = [
                ["Case Reference", row.get("Case_Reference", "")],
                ["Patient / Project ID", row.get("Patient_ID", "")],
                ["Age", row.get("Age", "")],
                ["Sex", row.get("Sex", "")],
                ["Date & Time", row.get("Date_Time", "")],
                ["Drug", row.get("Drug", "")],
                ["ADR", row.get("ADR", "")],
                ["Priority", priority],
                ["Seriousness", seriousness],
                ["Decision Source", decision_source],
                ["Reason", reason],
                ["Recommended Action", recommendation]
            ]
            table = Table([[P(a), P(b)] for a, b in data], colWidths=[135, 365])
            table.setStyle(TableStyle([
                ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
                ("BACKGROUND", (0,0), (0,-1), colors.whitesmoke),
                ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
                ("VALIGN", (0,0), (-1,-1), "TOP"),
                ("FONTSIZE", (0,0), (-1,-1), 8.5),
                ("PADDING", (0,0), (-1,-1), 6)
            ]))
            story += [
                table,
                Spacer(1, 14),
                P("Disclaimer: PHARMAGUARD is a proof-of-concept AI-assisted pharmacovigilance review-prioritization system. It does not establish causality, diagnosis, treatment, regulatory seriousness, or replace professional clinical judgment.")
            ]
            pdf_doc.build(story)
            pdf_buffer.seek(0)

            st.download_button(
                "📥 Download PDF Report",
                data=pdf_buffer,
                file_name=f"PHARMAGUARD_{row.get('Case_Reference', 'Case')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.warning(f"PDF report generation is unavailable: {e}")

def render_analytics_screen():
    """Centralized, mobile-friendly Safety & Priority Analytics view."""
    df = pd.DataFrame(st.session_state.get("adr_history", []))

    st.markdown(
        """
        <div class="pg-dashboard-hero">
            <div class="pg-dashboard-icon">📊</div>
            <div class="pg-dashboard-copy">
                <div class="pg-dashboard-title">Safety & Priority Analytics</div>
                <div class="pg-dashboard-subtitle">Organized project-record insights for priority, ADR, drug, safety and audit review</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df.empty:
        st.info("No ADR records are currently available for analytics.")
        return

    counts = _priority_counts(df)

    with st.expander("📌 Overview", expanded=True):
        overview_cards = [
            ("📋", "Total Cases", len(df), "Recorded reports", "total"),
            ("🔴", "HIGH", counts["HIGH"], "Priority review", "high"),
            ("🟡", "MODERATE", counts["MODERATE"], "Clinical review", "moderate"),
            ("🟢", "LOW", counts["LOW"], "Routine review", "low"),
        ]
        cards_html = []
        for icon, label, value, note, kind in overview_cards:
            card = (
                f'<div class="pg-kpi-grid-card pg-kpi-{kind}">'
                f'<div class="pg-kpi-grid-icon">{icon}</div>'
                f'<div class="pg-kpi-grid-label">{html.escape(str(label))}</div>'
                f'<div class="pg-kpi-grid-value">{html.escape(str(value))}</div>'
                f'<div class="pg-kpi-grid-note">{html.escape(str(note))}</div>'
                f'</div>'
            )
            cards_html.append(card)
        st.markdown(
            '<div class="pg-kpi-grid analytics-overview-grid">' + "".join(cards_html) + '</div>',
            unsafe_allow_html=True,
        )
        st.caption("Recorded project priorities only; these are descriptive summaries, not clinical risk estimates.")

    with st.expander("🎯 Priority Analytics", expanded=False):
        st.markdown("""<div class="pg-expand-workspace-intro"><div class="pg-expand-workspace-title">Priority Analytics</div><div class="pg-expand-workspace-sub">Explore priority distribution and descriptive patterns by selected demographic view.</div><span class="pg-expand-status">PHARMAGUARD WORKSPACE</span></div>""", unsafe_allow_html=True)
        st.caption("Choose one view at a time for better mobile readability.")
        priority_view = st.selectbox(
            "Priority view",
            ["Priority Distribution", "Priority by Sex", "Priority by Age Group"],
            key="analytics_priority_view",
        )

        if priority_view == "Priority Distribution":
            priority_df = pd.DataFrame(
                {"Priority": ["HIGH", "MODERATE", "LOW"], "Cases": [counts["HIGH"], counts["MODERATE"], counts["LOW"]]}
            ).set_index("Priority")
            st.bar_chart(priority_df, use_container_width=True, height=280)
        elif priority_view == "Priority by Sex":
            sex_df = df.copy()
            sex_df["Sex"] = sex_df.get("Sex", "Unknown").astype(str).str.upper().replace("", "UNKNOWN")
            sex_table = pd.crosstab(sex_df["Sex"], sex_df["Priority"]).reindex(columns=["HIGH", "MODERATE", "LOW"], fill_value=0)
            st.bar_chart(sex_table, use_container_width=True, height=300)
        else:
            age_df = df.copy()
            age_df["Age"] = pd.to_numeric(age_df.get("Age"), errors="coerce")
            age_df["Age Group"] = pd.cut(
                age_df["Age"],
                bins=[-1, 17, 30, 45, 60, 120],
                labels=["0–17", "18–30", "31–45", "46–60", "61–120"],
            )
            age_table = pd.crosstab(age_df["Age Group"], age_df["Priority"]).reindex(columns=["HIGH", "MODERATE", "LOW"], fill_value=0)
            st.bar_chart(age_table, use_container_width=True, height=300)

    with st.expander("💊 ADR & Drug Analytics", expanded=False):
        st.markdown("""<div class="pg-expand-workspace-intro"><div class="pg-expand-workspace-title">ADR & Drug Analytics</div><div class="pg-expand-workspace-sub">Explore reported drugs, ADR frequency and priority patterns using descriptive record summaries.</div><span class="pg-expand-status">PHARMAGUARD WORKSPACE</span></div>""", unsafe_allow_html=True)
        st.caption("Select one insight at a time. Top-10 views are descriptive record summaries.")
        adr_drug_view = st.selectbox(
            "ADR & drug view",
            [
                "Most Reported Drugs",
                "Most Frequent ADRs",
                "Drug-wise Priority — Top 10",
                "ADR-wise Priority — Top 10",
            ],
            key="analytics_adr_drug_view",
        )

        if adr_drug_view == "Most Reported Drugs":
            drug_frequency = (
                df.get("Drug", pd.Series(dtype=str))
                .astype(str).str.strip().replace("", "Unknown").value_counts().head(10)
            )
            st.bar_chart(drug_frequency.rename("Cases").to_frame(), use_container_width=True, height=320, horizontal=True)
        elif adr_drug_view == "Most Frequent ADRs":
            adr_frequency = (
                df.get("ADR", pd.Series(dtype=str))
                .astype(str).str.strip().replace("", "Unknown").value_counts().head(10)
            )
            st.bar_chart(adr_frequency.rename("Cases").to_frame(), use_container_width=True, height=320, horizontal=True)
        elif adr_drug_view == "Drug-wise Priority — Top 10":
            drug_df = df.copy()
            drug_df["Drug"] = drug_df.get("Drug", "Unknown").astype(str).str.strip().replace("", "Unknown")
            drug_table = pd.crosstab(drug_df["Drug"], drug_df["Priority"]).reindex(columns=["HIGH", "MODERATE", "LOW"], fill_value=0)
            drug_table["TOTAL"] = drug_table[["HIGH", "MODERATE", "LOW"]].sum(axis=1)
            drug_table = drug_table.sort_values("TOTAL", ascending=False).head(10).drop(columns="TOTAL")
            st.bar_chart(drug_table, use_container_width=True, height=340)
        else:
            adr_df = df.copy()
            adr_df["ADR"] = adr_df.get("ADR", "Unknown").astype(str).str.strip().replace("", "Unknown")
            adr_table = pd.crosstab(adr_df["ADR"], adr_df["Priority"]).reindex(columns=["HIGH", "MODERATE", "LOW"], fill_value=0)
            adr_table["TOTAL"] = adr_table[["HIGH", "MODERATE", "LOW"]].sum(axis=1)
            adr_table = adr_table.sort_values("TOTAL", ascending=False).head(10).drop(columns="TOTAL")
            st.bar_chart(adr_table, use_container_width=True, height=340)

    with st.expander("🛡️ Safety Intelligence", expanded=False):
        st.markdown("""<div class="pg-expand-workspace-intro"><div class="pg-expand-workspace-title">Safety Intelligence</div><div class="pg-expand-workspace-sub">Review serious-signal, seriousness and review-priority patterns available in the project database.</div><span class="pg-expand-status">PHARMAGUARD WORKSPACE</span></div>""", unsafe_allow_html=True)
        st.caption("Recorded workflow indicators only; not calibrated clinical risk or regulatory performance.")
        source = df.get("Decision_Source", pd.Series(dtype=str)).astype(str).str.strip()
        s1, s2 = st.columns(2)
        with s1:
            st.metric("Safety Gate", int(source.str.startswith("Safety Gate", na=False).sum()))
            st.metric("Reassessments", int(df.get("Reassessment_Of", pd.Series(dtype=str)).astype(str).str.strip().ne("").sum()))
        with s2:
            st.metric("RF-Assisted", int((source == "Random Forest prototype").sum()))
            st.metric("Linked Cases", int(df.get("Original_Case_Reference", pd.Series(dtype=str)).astype(str).str.strip().ne("").sum()))

        seriousness = (
            df.get("Seriousness", pd.Series(dtype=str))
            .astype(str).str.strip().str.upper().replace("", "UNKNOWN").value_counts()
        )
        st.markdown("**Seriousness Distribution**")
        st.bar_chart(seriousness.rename("Cases").to_frame(), use_container_width=True, height=280)

    with st.expander("🔎 Quality & Audit", expanded=False):
        st.markdown("""<div class="pg-expand-workspace-intro"><div class="pg-expand-workspace-title">Quality & Audit</div><div class="pg-expand-workspace-sub">Review record completeness and data-quality indicators for the current dataset.</div><span class="pg-expand-status">PHARMAGUARD WORKSPACE</span></div>""", unsafe_allow_html=True)
        priority_recorded = int(df.get("Priority", pd.Series(dtype=str)).astype(str).str.strip().ne("").sum())
        decision_recorded = int(df.get("Decision_Source", pd.Series(dtype=str)).astype(str).str.strip().ne("").sum())
        case_reference_recorded = int(df.get("Case_Reference", pd.Series(dtype=str)).astype(str).str.strip().ne("").sum())
        adr_recorded = int(df.get("ADR", pd.Series(dtype=str)).astype(str).str.strip().ne("").sum())
        drug_recorded = int(df.get("Drug", pd.Series(dtype=str)).astype(str).str.strip().ne("").sum())
        reassessment_links = int(df.get("Reassessment_Of", pd.Series(dtype=str)).astype(str).str.strip().ne("").sum())
        original_links = int(df.get("Original_Case_Reference", pd.Series(dtype=str)).astype(str).str.strip().ne("").sum())

        q1, q2 = st.columns(2)
        with q1:
            st.metric("Priority Recorded", priority_recorded)
            st.metric("Case References", case_reference_recorded)
            st.metric("Drug Recorded", drug_recorded)
            st.metric("Reassessment Links", reassessment_links)
        with q2:
            st.metric("Decision Source", decision_recorded)
            st.metric("ADR Recorded", adr_recorded)
            st.metric("Original Case Links", original_links)

        audit_df = pd.DataFrame(
            {
                "Audit Field": [
                    "Priority Recorded", "Decision Source Recorded", "Case Reference Recorded",
                    "ADR Recorded", "Drug Recorded", "Reassessm
