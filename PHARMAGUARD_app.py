# PHARMAGUARD Professional UI v2
# Dashboard HTML rendering fix — backend/Safety Gate/ML/database logic preserved.
import streamlit as st
import pandas as pd
import joblib
import requests
import re
import uuid
import textwrap
from pathlib import Path

from datetime import datetime


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="PHARMAGUARD",
    page_icon="💊",
    layout="wide"
)


# =========================================================
# PROFESSIONAL HEADER
# =========================================================

st.markdown("""
<style>
.pg-header { text-align:center; padding:18px 12px 16px 12px; border-radius:16px; background:linear-gradient(135deg,#eef7ff 0%,#f7fbff 100%); border:1px solid #d7e7f5; margin-bottom:18px; }
.pg-shield { font-size:42px; line-height:1; margin-bottom:4px; }
.pg-title { font-size:34px; font-weight:800; letter-spacing:1px; margin:0; }
.pg-subtitle { font-size:16px; margin:5px 0 3px 0; }
.pg-tag { display:inline-block; padding:5px 12px; border-radius:999px; font-size:12px; font-weight:700; background:#e8f1f8; }
.pg-section { margin-top:14px; padding:10px 14px; border-left:5px solid #2b6f9f; background:#f7fafc; border-radius:8px; }
.pg-note { font-size:13px; color:#5b6570; padding:7px 10px; background:#f7f7f7; border-radius:7px; }
.pg-result-card { display:flex; align-items:center; gap:14px; padding:16px 18px; border-radius:14px; margin:8px 0 16px 0; border:1px solid #d9e2ea; }
.pg-result-high { background:#fff1f1; border-left:7px solid #c62828; }
.pg-result-moderate { background:#fff8e6; border-left:7px solid #d99000; }
.pg-result-low { background:#eef9f1; border-left:7px solid #2e7d32; }
.pg-result-unknown { background:#f4f5f6; border-left:7px solid #7b8794; }
.pg-result-icon { font-size:30px; line-height:1; }
.pg-result-label { font-size:22px; font-weight:800; letter-spacing:.4px; }
.pg-result-message { font-size:14px; margin-top:3px; color:#4f5963; }
.pg-result-detail { padding:14px 16px; border:1px solid #dfe6ec; border-radius:12px; background:#ffffff; margin:10px 0 12px 0; }
.pg-detail-title { font-size:16px; font-weight:800; margin-bottom:9px; }
.pg-detail-row { display:flex; gap:12px; padding:7px 0; border-top:1px solid #edf0f2; font-size:14px; }
.pg-detail-row b { min-width:180px; }
@media (max-width: 700px) { .pg-result-label { font-size:19px; } .pg-detail-row { display:block; } .pg-detail-row b { display:block; margin-bottom:3px; } }
.pg-dashboard-header { display:flex; align-items:center; gap:12px; padding:14px 16px; margin:10px 0 12px 0; border-radius:14px; background:#f5f9fc; border:1px solid #dbe8f1; }
.pg-dashboard-icon { font-size:30px; line-height:1; }
.pg-dashboard-title { font-size:25px; font-weight:800; letter-spacing:.2px; }
.pg-dashboard-subtitle { font-size:13px; color:#65717d; margin-top:2px; }
.pg-kpi { padding:14px 12px; min-height:112px; border-radius:14px; background:#f7fafc; border:1px solid #dbe6ee; box-shadow:0 2px 8px rgba(40,70,90,.05); }
.pg-kpi-high { border-left:5px solid #c94b4b; }
.pg-kpi-moderate { border-left:5px solid #d69a22; }
.pg-kpi-low { border-left:5px solid #4f9b67; }
.pg-kpi-label { font-size:13px; font-weight:700; color:#56616c; }
.pg-kpi-value { font-size:30px; font-weight:800; margin-top:7px; line-height:1.05; }
.pg-kpi-foot { font-size:11px; color:#7a848d; margin-top:7px; }
.pg-appbar { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:10px 14px; margin:0 0 14px 0; border:1px solid #dbe8f1; border-radius:12px; background:#ffffff; box-shadow:0 2px 10px rgba(30,60,90,.04); }
.pg-brand-mini { font-weight:800; letter-spacing:.5px; font-size:16px; }
.pg-status { display:inline-flex; align-items:center; gap:6px; padding:5px 10px; border-radius:999px; background:#eef8f1; color:#236b3a; font-size:12px; font-weight:700; }
.pg-hero { padding:18px; border-radius:16px; background:linear-gradient(135deg,#f4faff 0%,#ffffff 70%); border:1px solid #d8e8f4; margin-bottom:16px; }
.pg-hero-title { font-size:25px; font-weight:800; margin-bottom:5px; }
.pg-hero-text { color:#5f6d78; font-size:14px; line-height:1.55; }
/* =========================================================
   PHARMAGUARD PROFESSIONAL DASHBOARD
   ========================================================= */

.pg-dashboard-hero {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 20px;
    margin-bottom: 18px;
    border-radius: 18px;
    background: linear-gradient(
        135deg,
        #eef7ff 0%,
        #ffffff 100%
    );
    border: 1px solid #d7e7f3;
    box-shadow: 0 4px 18px rgba(30,60,90,.06);
}

.pg-dashboard-icon {
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 15px;
    background: #0b1f33;
    font-size: 27px;
}

.pg-dashboard-title {
    font-size: 24px;
    font-weight: 800;
    color: #102a43;
}

.pg-dashboard-copy {
    min-width: 0;
}

.pg-dashboard-subtitle {
    margin-top: 3px;
    font-size: 13px;
    color: #657786;
}

.pg-stat-card {
    min-height: 145px;
    padding: 17px;
    margin-bottom: 12px;
    border-radius: 16px;
    background: #ffffff;
    border: 1px solid #dbe7ef;
    box-shadow: 0 3px 14px rgba(30,60,90,.06);
}

.pg-stat-icon {
    font-size: 22px;
    margin-bottom: 8px;
}

.pg-stat-label {
    font-size: 12px;
    font-weight: 700;
    color: #657786;
}

.pg-stat-value {
    margin-top: 3px;
    font-size: 28px;
    font-weight: 800;
    color: #102a43;
}

.pg-stat-note {
    margin-top: 4px;
    font-size: 11px;
    color: #7b8794;
}

.pg-high-card {
    border-top: 4px solid #d64545;
}

.pg-moderate-card {
    border-top: 4px solid #d49b00;
}

.pg-low-card {
    border-top: 4px solid #2f855a;
}

.pg-empty-state {
    text-align: center;
    padding: 35px 20px;
    margin-top: 12px;
    border-radius: 16px;
    background: #f8fbfd;
    border: 1px dashed #cbd9e3;
}

.pg-empty-icon {
    font-size: 34px;
}

.pg-empty-title {
    margin-top: 8px;
    font-size: 18px;
    font-weight: 800;
    color: #243b53;
}

.pg-empty-text {
    margin-top: 5px;
    font-size: 13px;
    color: #718096;
}

.pg-dashboard-info {
    margin-top: 20px;
    padding: 16px 18px;
    border-radius: 15px;
    background: #f4f9fc;
    border: 1px solid #d9e8f1;
}

.pg-info-title {
    font-size: 15px;
    font-weight: 800;
    color: #102a43;
}

.pg-info-text {
    margin-top: 5px;
    font-size: 13px;
    line-height: 1.5;
    color: #52606d;
}

.pg-info-note {
    margin-top: 8px;
    font-size: 11px;
    font-weight: 700;
    color: #6b7c8c;
}

@media (max-width: 700px) {

    .pg-dashboard-title {
        font-size: 20px;
    }

    .pg-dashboard-subtitle {
        font-size: 12px;
    }

    .pg-stat-card {
        min-height: 125px;
    }

    .pg-stat-value {
        font-size: 25px;
    }

}

.pg-disclaimer { margin-top:22px; padding:12px 14px; border-radius:10px; background:#f7f8fa; border:1px solid #e1e5e9; color:#66717b; font-size:12px; line-height:1.5; }
div.stButton > button { border-radius:10px; font-weight:700; min-height:44px; }
@media (max-width: 700px) { .pg-appbar { padding:9px 10px; } .pg-hero-title { font-size:21px; } .pg-title { font-size:29px; } .pg-subtitle { font-size:14px; } }

</style>
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
# APP NAVIGATION / PROJECT INFO
# =========================================================

with st.sidebar:
    st.markdown("## 🛡️ PHARMAGUARD")
    st.caption("AI-Assisted ADR Risk Prioritization")
    st.markdown("### Navigation")
    active_page = st.radio(
        "Open screen",
        [
            "🏠 Dashboard",
            "🔍 New ADR Analysis",
            "📚 ADR History",
            "📄 Case Reports",
            "☁️ Database",
            "ℹ️ About / Methodology"
        ],
        index=0,
        label_visibility="collapsed"
    )
    st.divider()
    st.info(
        "Prototype: review-priority support only. "
        "It does not replace clinical, causality, or regulatory assessment."
    )


# =========================================================
# MODEL + GOOGLE SHEET
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
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
    "extended hospital stay"
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
    "history"
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
    "dehydration"
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
# STEP 96B — ADR INPUT VALIDATION
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


# =========================================================
# SAVE DATA TO GOOGLE SHEET
# =========================================================

def save_to_google_sheet(data):

    try:

        response = requests.post(
            GOOGLE_SHEET_URL,
            json=data,
            timeout=15
        )

        return response.status_code == 200

    except Exception:

        return False


# =========================================================
# LOAD DATA FROM GOOGLE SHEET
# =========================================================

@st.cache_data(ttl=60, show_spinner=False)
def load_from_google_sheet():

    try:

        response = requests.get(
            GOOGLE_SHEET_URL,
            timeout=5
        )

        if response.status_code == 200:

            return pd.DataFrame(response.json())

        return pd.DataFrame()

    except Exception:

        return pd.DataFrame()


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

            nearby_before = " ".join(before_tokens[-6:])
            nearby_after = " ".join(after_tokens[:6])

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

            # Historical / previous-event context before the phrase.
            if not is_protected:
                for pattern in HISTORY_PATTERNS:
                    if re.search(
                        rf"(?<!\w){re.escape(pattern)}(?!\w)",
                        nearby_before
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

def model_predict(age, sex, drug, adr):

    X = pd.DataFrame([{

        "Age": age,

        "Sex": sex,

        "Drug": drug,

        "ADR": adr,

        "Age_Missing": 0,

        "Drug_Missing": int(
            not str(drug).strip()
        ),

        "ADR_Missing": int(
            not str(adr).strip()
        )

    }])


    # Model package with preprocessor
    if isinstance(model, dict):

        estimator = (
            model.get("model")
            or model.get("estimator")
        )

        preprocessor = model.get(
            "preprocessor"
        )

        if (
            estimator is not None
            and preprocessor is not None
        ):

            try:

                return str(
                    estimator.predict(
                        preprocessor.transform(X)
                    )[0]
                ).upper()

            except Exception:

                pass


    # Direct model prediction
    try:

        return str(
            model.predict(X)[0]
        ).upper()

    except Exception:

        return "UNKNOWN"


# =========================================================
# SESSION HISTORY
# =========================================================

if "adr_history" not in st.session_state:

    st.session_state.adr_history = []


# =========================================================
# LOAD PERMANENT DATABASE ONCE
# =========================================================

if "database_loaded" not in st.session_state:

    database_df = load_from_google_sheet()

    if not database_df.empty:

        st.session_state.adr_history = (
            database_df.to_dict("records")
        )

    st.session_state.database_loaded = True


# =========================================================
# V29 SCREEN RENDERERS
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

    df = pd.DataFrame(
        st.session_state.get("adr_history", [])
    )

    counts = _priority_counts(df)

    # =====================================================
    # PROFESSIONAL DASHBOARD HEADER
    # =====================================================

    # Render the dashboard header as HTML through st.markdown.
    # Do not use st.write() for this block, because the HTML must be
    # explicitly enabled for Streamlit to render it.
    st.markdown(
        """<div class="pg-dashboard-hero">
<div class="pg-dashboard-icon">🛡️</div>
<div class="pg-dashboard-copy">
<div class="pg-dashboard-title">Pharmacovigilance Dashboard</div>
<div class="pg-dashboard-subtitle">Monitor ADR reports and review-priority signals</div>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # =====================================================
    # QUICK ACTION
    # =====================================================

    st.markdown("### Quick Action")

    if st.button(
        "➕  Start New ADR Analysis",
        use_container_width=True
    ):
        st.session_state["active_page"] = "🔍 New ADR Analysis"
        st.rerun()

    # =====================================================
    # SUMMARY CARDS
    # =====================================================

    st.markdown("### ADR Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="pg-stat-card">
                <div class="pg-stat-icon">📋</div>
                <div class="pg-stat-label">Total ADR Cases</div>
                <div class="pg-stat-value">{len(df)}</div>
                <div class="pg-stat-note">All recorded cases</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="pg-stat-card pg-high-card">
                <div class="pg-stat-icon">🔴</div>
                <div class="pg-stat-label">High Priority</div>
                <div class="pg-stat-value">{counts["HIGH"]}</div>
                <div class="pg-stat-note">Priority review</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="pg-stat-card pg-moderate-card">
                <div class="pg-stat-icon">🟡</div>
                <div class="pg-stat-label">Moderate</div>
                <div class="pg-stat-value">{counts["MODERATE"]}</div>
                <div class="pg-stat-note">Clinical review signal</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="pg-stat-card pg-low-card">
                <div class="pg-stat-icon">🟢</div>
                <div class="pg-stat-label">Low Priority</div>
                <div class="pg-stat-value">{counts["LOW"]}</div>
                <div class="pg-stat-note">Routine review</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # PRIORITY DISTRIBUTION
    # =====================================================

    st.markdown("### Priority Distribution")

    chart = pd.DataFrame(
        {
            "Priority": [
                "HIGH",
                "MODERATE",
                "LOW"
            ],
            "Cases": [
                counts["HIGH"],
                counts["MODERATE"],
                counts["LOW"]
            ]
        }
    ).set_index("Priority")

    st.bar_chart(
        chart,
        use_container_width=True
    )

    # =====================================================
    # RECENT CASES
    # =====================================================

    if df.empty:

        st.markdown(
            """
            <div class="pg-empty-state">

                <div class="pg-empty-icon">📭</div>

                <div class="pg-empty-title">
                    No ADR Reports Yet
                </div>

                <div class="pg-empty-text">
                    Start a new ADR analysis to create your
                    first PHARMAGUARD case.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        return

    st.markdown("### 🕐 Recent ADR Reports")

    recent_cols = [
        c for c in [
            "Case_Reference",
            "Drug",
            "ADR",
            "Priority",
            "Decision_Source",
            "Date_Time"
        ]
        if c in df.columns
    ]

    recent_df = (
        df[recent_cols]
        .tail(8)
        .iloc[::-1]
        .copy()
    )

    st.dataframe(
        recent_df,
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # DASHBOARD INFORMATION
    # =====================================================

    st.markdown(
        textwrap.dedent(
            """
            <div class="pg-dashboard-info">
                <div class="pg-info-title">
                    🛡️ PHARMAGUARD Review Support
                </div>
                <div class="pg-info-text">
                    PHARMAGUARD combines a predefined Safety Gate
                    with a Random Forest prototype to support
                    pharmacovigilance review prioritization.
                </div>
                <div class="pg-info-note">
                    Review priority only • Proof of Concept
                </div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True
    )

def render_history_screen():
    st.markdown("## 📚 ADR History")
    df = pd.DataFrame(st.session_state.get("adr_history", []))

    if df.empty:
        st.info("No ADR cases are currently available.")
        return

    q = st.text_input(
        "Search",
        placeholder="Search by case ID, drug, ADR or priority..."
    ).strip().lower()

    filtered = df.copy()
    if q:
        mask = pd.Series(False, index=filtered.index)
        for col in ["Case_Reference", "Patient_ID", "Drug", "ADR", "Priority"]:
            if col in filtered.columns:
                mask = mask | filtered[col].astype(str).str.lower().str.contains(
                    re.escape(q), na=False
                )
        filtered = filtered[mask]

    priority_filter = st.selectbox(
        "Priority",
        ["All", "HIGH", "MODERATE", "LOW"]
    )
    if priority_filter != "All" and "Priority" in filtered.columns:
        filtered = filtered[
            filtered["Priority"].astype(str).str.upper() == priority_filter
        ]

    display_cols = [c for c in [
        "Case_Reference", "Patient_ID", "Drug", "ADR",
        "Priority", "Seriousness", "Decision_Source", "Date_Time"
    ] if c in filtered.columns]

    st.caption(f"Showing {len(filtered)} of {len(df)} cases")
    st.dataframe(
        filtered[display_cols].sort_index(ascending=False),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇️ Export Filtered CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="PHARMAGUARD_Filtered_ADR_History.csv",
        mime="text/csv",
        use_container_width=True
    )


def render_case_reports_screen():
    st.markdown("## 📄 Case Reports")
    df = pd.DataFrame(st.session_state.get("adr_history", []))

    if df.empty:
        st.info("Analyze at least one ADR case to generate a case report.")
        return

    labels = []
    for idx, row in df.iterrows():
        ref = str(row.get("Case_Reference", f"Case {idx + 1}"))
        drug_name = str(row.get("Drug", "Unknown"))
        adr_text = str(row.get("ADR", ""))
        labels.append((idx, f"{ref} | {drug_name} | {adr_text[:50]}"))

    selected_label = st.selectbox(
        "Select case",
        [x[1] for x in labels]
    )
    selected_idx = next(i for i, label in labels if label == selected_label)
    row = df.loc[selected_idx]

    priority = str(row.get("Priority", "UNKNOWN")).upper()
    seriousness = str(row.get("Seriousness", "Uncertain"))
    recommendation = {
        "HIGH": "Priority pharmacovigilance review required.",
        "MODERATE": "Pharmacovigilance review and clinical assessment recommended.",
        "LOW": "Routine pharmacovigilance review according to the project workflow."
    }.get(priority, "Additional information or professional review may be required.")

    st.markdown(f"### {priority} PRIORITY")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Case Reference:**", row.get("Case_Reference", ""))
        st.write("**Patient / Project ID:**", row.get("Patient_ID", ""))
        st.write("**Age:**", row.get("Age", ""))
        st.write("**Sex:**", row.get("Sex", ""))
    with c2:
        st.write("**Drug:**", row.get("Drug", ""))
        st.write("**ADR:**", row.get("ADR", ""))
        st.write("**Seriousness:**", seriousness)
        st.write("**Decision Source:**", row.get("Decision_Source", ""))

    st.info(f"**Reason:** {row.get('Reason', '')}")
    st.write("**Recommended Action:**", recommendation)

    report = f"""PHARMAGUARD ADR CASE REPORT

Case Reference: {row.get("Case_Reference", "")}
Patient / Project ID: {row.get("Patient_ID", "")}
Age: {row.get("Age", "")}
Sex: {row.get("Sex", "")}
Drug: {row.get("Drug", "")}
ADR: {row.get("ADR", "")}
Priority: {priority}
Seriousness: {seriousness}
Decision Source: {row.get("Decision_Source", "")}
Reason: {row.get("Reason", "")}
Recommended Action: {recommendation}

DISCLAIMER:
PHARMAGUARD is a proof-of-concept AI-assisted pharmacovigilance
review-prioritization system. It does not establish causality,
diagnosis, treatment, regulatory seriousness, or clinical
decision-making.
"""
    st.download_button(
        "⬇️ Download Case Report (TXT)",
        data=report,
        file_name=f"PHARMAGUARD_{row.get('Case_Reference', 'Case')}.txt",
        mime="text/plain",
        use_container_width=True
    )

    # Generate a compact PDF directly from the selected case.
    try:
        from io import BytesIO
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors

        pdf_buffer = BytesIO()
        pdf_doc = SimpleDocTemplate(
            pdf_buffer, pagesize=A4,
            rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
        )
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "PGTitle", parent=styles["Title"], alignment=TA_CENTER, fontSize=18, spaceAfter=8
        )
        sub_style = ParagraphStyle(
            "PGSub", parent=styles["Normal"], alignment=TA_CENTER, fontSize=9, textColor=colors.grey, spaceAfter=14
        )
        normal = styles["BodyText"]
        normal.fontSize = 9
        normal.leading = 12

        story = [
            Paragraph("PHARMAGUARD ADR CASE REPORT", title_style),
            Paragraph("AI-Assisted ADR Risk Prioritization System • Pharmacovigilance Proof of Concept", sub_style)
        ]
        data = [
            ["Case Reference", str(row.get("Case_Reference", ""))],
            ["Patient / Project ID", str(row.get("Patient_ID", ""))],
            ["Age", str(row.get("Age", ""))],
            ["Sex", str(row.get("Sex", ""))],
            ["Date & Time", str(row.get("Date_Time", ""))],
            ["Drug", str(row.get("Drug", ""))],
            ["ADR", str(row.get("ADR", ""))],
            ["Priority", priority],
            ["Seriousness", seriousness],
            ["Decision Source", str(row.get("Decision_Source", ""))],
            ["Reason", str(row.get("Reason", ""))],
            ["Recommended Action", recommendation],
        ]
        table = Table(data, colWidths=[135, 365])
        table.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
            ("BACKGROUND", (0,0), (0,-1), colors.whitesmoke),
            ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("FONTSIZE", (0,0), (-1,-1), 8.5),
            ("LEADING", (0,0), (-1,-1), 11),
            ("PADDING", (0,0), (-1,-1), 6),
        ]))
        story += [table, Spacer(1, 14), Paragraph(
            "Disclaimer: PHARMAGUARD is a proof-of-concept AI-assisted pharmacovigilance review-prioritization system. It does not establish causality, diagnosis, treatment, regulatory seriousness, or replace professional clinical judgment.",
            normal
        )]
        pdf_doc.build(story)
        pdf_buffer.seek(0)
        st.download_button(
            "📥 Download Case Report (PDF)",
            data=pdf_buffer,
            file_name=f"PHARMAGUARD_{row.get('Case_Reference', 'Case')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.warning(f"PDF report generation is unavailable: {e}")


def render_database_screen():
    st.markdown("## ☁️ Database")
    df = pd.DataFrame(st.session_state.get("adr_history", []))

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Records in current database view", len(df))
    with c2:
        st.metric("Database status", "Loaded" if st.session_state.get("database_loaded") else "Not loaded")

    st.caption(
        "The app uses the configured Google Sheets integration as its project database. "
        "The count below reflects records currently loaded into the app."
    )

    if not df.empty:
        st.dataframe(df.tail(20).iloc[::-1], use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Download Database CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="PHARMAGUARD_Database.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("No database records are currently loaded.")


def render_about_screen():
    st.markdown("## ℹ️ About PHARMAGUARD")
    st.markdown("### 🛡️ AI-Assisted ADR Risk Prioritization System")
    st.write(
        "PHARMAGUARD is a pharmacovigilance proof-of-concept designed to "
        "prioritize ADR reports for review."
    )

    with st.expander("What is an ADR?"):
        st.write(
            "An adverse drug reaction is a harmful or unintended response "
            "associated with the use of a medicinal product."
        )

    with st.expander("How PHARMAGUARD works"):
        st.write(
            "ADR report → Input validation → Safety Gate → Random Forest "
            "assistance when no predefined signal is detected → Final review priority → Database."
        )

    with st.expander("Safety Gate"):
        st.write(
            "The Safety Gate screens for project-defined serious and moderate-review "
            "signals and protects selected serious signals from being downgraded by the ML model."
        )

    with st.expander("Random Forest"):
        st.write(
            "The embedded Random Forest model provides prototype ML assistance. "
            "Its output is not a clinical probability or a validated regulatory classification."
        )

    with st.expander("Project limitations"):
        st.write(
            "The current prototype has not established clinical validity or real-world "
            "regulatory performance. Independent evaluation with an appropriately labeled "
            "dataset would be required for such claims."
        )

    st.warning(
        "PHARMAGUARD supports pharmacovigilance review. It does not replace "
        "professional clinical judgment, causality assessment, diagnosis, treatment, "
        "or regulatory assessment."
    )


# =========================================================
# SCREEN ROUTING
# =========================================================

if active_page == "🏠 Dashboard":
    render_dashboard_screen()
    st.stop()

if active_page == "📚 ADR History":
    render_history_screen()
    st.stop()

if active_page == "📄 Case Reports":
    render_case_reports_screen()
    st.stop()

if active_page == "☁️ Database":
    render_database_screen()
    st.stop()

if active_page == "ℹ️ About / Methodology":
    render_about_screen()
    st.stop()


# =========================================================
# NEW ADR ANALYSIS
# =========================================================

st.markdown("## 🔍 New ADR Analysis")
st.caption("1. Enter report → 2. Safety Gate → 3. Random Forest assistance → 4. Final priority → 5. Database")


# =========================================================
# PATIENT INPUT
# =========================================================

st.markdown('<div class="pg-section"><b>👤 Patient / Case Information</b></div>', unsafe_allow_html=True)

if "current_patient_id" not in st.session_state:
    st.session_state.current_patient_id = f"PHG-{uuid.uuid4().hex[:8].upper()}"

patient_id = st.text_input(
    "Patient / Project ID",
    value=st.session_state.current_patient_id,
    key="patient_id_input",
    help="A project identifier is generated automatically. Avoid unnecessary personally identifiable information."
)
st.session_state.current_patient_id = patient_id

age = st.number_input(
    "Patient Age",
    min_value=0,
    max_value=120,
    value=30,
    step=1
)

sex = st.selectbox(
    "Sex",
    ["M", "F", "Unknown"]
)

st.markdown('<div class="pg-section"><b>💊 Drug Information</b></div>', unsafe_allow_html=True)

drug = st.text_input(
    "Drug Name",
    placeholder="Example: Amoxicillin"
)

st.markdown('<div class="pg-section"><b>⚠️ ADR Report</b></div>', unsafe_allow_html=True)

adr = st.text_area(
    "Adverse Drug Reaction (ADR)",
    placeholder="Example: Anaphylaxis with difficulty breathing",
    height=140,
    help="Describe the reported adverse event as clearly as possible."
)

st.markdown('<div class="pg-note">💡 <b>Tip:</b> Include clinically relevant details available in the report, such as the reported reaction, severity-related information, or relevant outcome information.</div>', unsafe_allow_html=True)


# =========================================================
# ANALYZE ADR
# =========================================================

st.caption("Safety Gate → ML Assistance → Priority + Reason → Database")

if st.button(
    "🔍 ANALYZE ADR REPORT",
    use_container_width=True
):

    # -----------------------------------------------------
    # INPUT VALIDATION
    # -----------------------------------------------------

    if not patient_id.strip():

        st.warning(
            "Please enter a Patient ID."
        )

        st.stop()


    if not adr.strip():

        st.warning(
            "Please enter an ADR."
        )

        st.stop()
        
    # -----------------------------------------------------
    # STEP 96B: ADR MEDICAL-TERM VALIDATION
    # -----------------------------------------------------

    validation_status, suggestion, validation_message = validate_adr_input(adr)

    if validation_status == "POSSIBLE_TYPO":

        st.warning(validation_message)

        st.stop()

    if validation_status == "UNKNOWN":

        st.warning(validation_message)

        st.stop()

    # -----------------------------------------------------
    # FIND SERIOUS + MODERATE SIGNALS
    # -----------------------------------------------------

    serious_matches = matches(
    adr,
    SERIOUS_PATTERNS
)

    serious_hits = [
    pattern
    for pattern in serious_matches
    if not has_context_protection(adr, pattern)
    and not has_death_causality_protection(adr, pattern)
    and not (
        pattern == "shock"
        and has_nonmedical_shock_context(adr)
    )
]

    # Keep only the most specific serious signal in the reason.
    serious_hits = remove_redundant_hits(serious_hits)


    moderate_matches = matches(
        adr,
        MODERATE_PATTERNS
    )

    moderate_context_matches = matches(
        adr,
        MODERATE_CONTEXT_PATTERNS
    )

    moderate_hits = [
    pattern
    for pattern in (
        moderate_matches + moderate_context_matches
    )
    if not has_context_protection(adr, pattern)
    ]

    # Keep the most specific moderate signal in the reason.
    moderate_hits = remove_redundant_hits(moderate_hits)

    # Prefer specific clinical/contextual signals over generic phrases
    # when both are present. This changes explanation text only.
    moderate_hits = prioritize_specific_moderate_hits(moderate_hits)

  
    # -----------------------------------------------------
    # PRIORITY LOGIC
    # -----------------------------------------------------

    if serious_hits:

        priority = "HIGH"

        flag = (
            "Potentially serious medical event signal"
        )

        reason = (
            "Serious ADR indicator detected: "
            + ", ".join(serious_hits)
        )

        recommendation = (
            "Priority pharmacovigilance review required."
        )

        decision_source = "Safety Gate — serious signal"


    elif moderate_hits:

        priority = "MODERATE"

        flag = (
            "Non-serious but clinically meaningful "
            "review signal"
        )

        reason = (
            "Project-defined moderate-review "
            "indicator detected: "
            + ", ".join(moderate_hits)
        )

        recommendation = (
            "Pharmacovigilance review and clinical "
            "assessment recommended."
        )

        decision_source = "Safety Gate — moderate signal"


    else:

        priority = model_predict(
            age,
            sex,
            drug,
            adr
        )


        if priority not in {
            "LOW",
            "MODERATE",
            "HIGH"
        }:

            priority = "UNKNOWN"


        flag = (
            "No predefined serious signal detected"
        )

        reason = (
            "Priority assigned by the "
            "Random Forest prototype."
        )

        recommendation = (
            "Routine pharmacovigilance review "
            "according to the project workflow."
        )

        decision_source = "Random Forest prototype"


    # =====================================================
    # DISPLAY RESULT — STEP 96 PART 2
    # =====================================================

    st.divider()
    st.subheader("📋 ADR Analysis Result")

    priority_meta = {
        "HIGH": {
            "icon": "🚨",
            "label": "HIGH PRIORITY",
            "class_name": "pg-result-high",
            "message": "Immediate pharmacovigilance review recommended."
        },
        "MODERATE": {
            "icon": "⚠️",
            "label": "MODERATE PRIORITY",
            "class_name": "pg-result-moderate",
            "message": "Clinical and pharmacovigilance review recommended."
        },
        "LOW": {
            "icon": "✅",
            "label": "LOW PRIORITY",
            "class_name": "pg-result-low",
            "message": "Routine pharmacovigilance review."
        },
        "UNKNOWN": {
            "icon": "❓",
            "label": "PRIORITY UNCERTAIN",
            "class_name": "pg-result-unknown",
            "message": "Additional information or professional review may be required."
        }
    }

    meta = priority_meta.get(priority, priority_meta["UNKNOWN"])

    st.markdown(f"""
    <div class="pg-result-card {meta['class_name']}">
        <div class="pg-result-icon">{meta['icon']}</div>
        <div>
            <div class="pg-result-label">{meta['label']}</div>
            <div class="pg-result-message">{meta['message']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    result_col1, result_col2, result_col3 = st.columns(3)
    with result_col1:
        st.metric("Patient ID", str(patient_id))
    with result_col2:
        st.metric("Age", str(age))
    with result_col3:
        st.metric("Sex", str(sex))

    st.markdown(
        f"""
        <div class="pg-result-detail">
            <div class="pg-detail-title">⚕️ Review Assessment</div>
            <div class="pg-detail-row"><b>Seriousness / Review Flag</b><span>{flag}</span></div>
            <div class="pg-detail-row"><b>Reason</b><span>{reason}</span></div>
            <div class="pg-detail-row"><b>Recommendation</b><span>{recommendation}</span></div>
            <div class="pg-detail-row"><b>Decision source</b><span>{decision_source}</span></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "PHARMAGUARD provides AI-assisted priority support for pharmacovigilance review; it does not establish ADR causality or replace professional clinical/regulatory assessment."
    )

    # =====================================================
    # CREATE DATABASE RECORD
    # =====================================================
    # Generate a collision-resistant Case Reference.
    # A UUID suffix avoids duplicate references when multiple sessions/users
    # save cases at nearly the same time.
    case_reference = (
        f"PHG-CASE-{datetime.now().strftime('%Y%m%d-%H%M%S')}-"
        f"{uuid.uuid4().hex[:8].upper()}"
    )
    database_record = {

        "Date_Time":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "Patient_ID":
            patient_id,

        "Age":
            age,

        "Sex":
            sex,

        "Drug":
            drug,

        "ADR":
            adr,

        "Seriousness":
            "Yes"
            if priority == "HIGH"
            else "No"
            if priority in {"MODERATE", "LOW"}
            else "Uncertain",

        "Decision_Source":
            decision_source,

        "Priority":
            priority,

        "Reason":
            reason,
        "Case_Reference":
    case_reference
    }


    # =====================================================
    # SAVE TO GOOGLE SHEET
    # =====================================================

    saved = save_to_google_sheet(
        database_record
    )


    if saved:

        # Invalidate cached Google Sheet data so the next database refresh
        # can retrieve the newly saved row instead of stale data.
        try:
            st.cache_data.clear()
        except Exception:
            pass

        st.success(
            "✅ ADR saved to PHARMAGUARD Database"
        )

    else:

        st.warning(
            "⚠️ Analysis completed, but ADR "
            "could not be saved to database."
        )


    # =====================================================
    # ADD TO CURRENT SESSION HISTORY
    # =====================================================

    # Keep the current-session record schema identical to the Google Sheet schema.
    st.session_state.adr_history.append(
        database_record.copy()
    )


# =========================================================
# DASHBOARD
# =========================================================

if active_page == "🔍 New ADR Analysis" and st.session_state.get(
    "adr_history"
):

    st.markdown("---")

    st.markdown(
        textwrap.dedent(
            """
            <div class="pg-dashboard-header">
                <div class="pg-dashboard-icon">📊</div>
                <div>
                    <div class="pg-dashboard-title">PHARMAGUARD Dashboard</div>
                    <div class="pg-dashboard-subtitle">ADR monitoring • Priority overview • Pharmacovigilance review support</div>
                </div>
            </div>
            <div class="pg-note">📌 Dashboard metrics are based on ADR cases currently available in the app session/database view.</div>
            """
        ).strip(),
        unsafe_allow_html=True
    )


    dashboard_df = pd.DataFrame(
        st.session_state.adr_history
    )


    priority_counts = (

        dashboard_df["Priority"]
        .astype(str)
        .str.upper()
        .value_counts()
        .reindex(
            [
                "HIGH",
                "MODERATE",
                "LOW"
            ],
            fill_value=0
        )

    )


    total_cases = len(
        dashboard_df
    )

    high_cases = int(
        priority_counts["HIGH"]
    )

    moderate_cases = int(
        priority_counts["MODERATE"]
    )

    low_cases = int(
        priority_counts["LOW"]
    )


    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f"""<div class="pg-kpi"><div class="pg-kpi-label">Total ADR Cases</div><div class="pg-kpi-value">{total_cases}</div><div class="pg-kpi-foot">Reports available</div></div>""", unsafe_allow_html=True)

    with m2:
        st.markdown(f"""<div class="pg-kpi pg-kpi-high"><div class="pg-kpi-label">🔴 High Priority</div><div class="pg-kpi-value">{high_cases}</div><div class="pg-kpi-foot">Needs review</div></div>""", unsafe_allow_html=True)

    with m3:
        st.markdown(f"""<div class="pg-kpi pg-kpi-moderate"><div class="pg-kpi-label">🟡 Moderate</div><div class="pg-kpi-value">{moderate_cases}</div><div class="pg-kpi-foot">Monitor / review</div></div>""", unsafe_allow_html=True)

    with m4:
        st.markdown(f"""<div class="pg-kpi pg-kpi-low"><div class="pg-kpi-label">🟢 Low</div><div class="pg-kpi-value">{low_cases}</div><div class="pg-kpi-foot">Lower priority</div></div>""", unsafe_allow_html=True)


    st.markdown(
        "#### Priority Distribution"
    )


    chart_df = (
        priority_counts
        .rename("Cases")
        .reset_index()
    )


    chart_df.columns = [
        "Priority",
        "Cases"
    ]


    st.bar_chart(
        chart_df.set_index(
            "Priority"
        )
    )
    # =====================================================
    # MOST REPORTED DRUGS
    # =====================================================

    st.markdown(
        "#### 💊 Most Reported Drugs"
    )

    drug_counts = (
        dashboard_df["Drug"]
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
        .value_counts()
        .head(10)
    )

    drug_chart_df = (
        drug_counts
        .rename("Cases")
        .reset_index()
    )

    drug_chart_df.columns = [
        "Drug",
        "Cases"
    ]

    st.bar_chart(
        drug_chart_df.set_index(
            "Drug"
        ),
        horizontal=True
        )
        # =====================================================
    # MOST FREQUENT ADRs
    # =====================================================

    st.markdown(
        "#### ⚠️ Most Frequent ADRs"
    )

    adr_counts = (
        dashboard_df["ADR"]
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
        .value_counts()
        .head(10)
    )

    adr_chart_df = (
        adr_counts
        .rename("Cases")
        .reset_index()
    )

    adr_chart_df.columns = [
        "ADR",
        "Cases"
    ]

    st.bar_chart(
        adr_chart_df.set_index(
            "ADR"
        ),
        horizontal=True
    )
        # =====================================================
    # RECENT ADR REPORTS
    # =====================================================

    st.markdown(
        "#### 🕐 Recent ADR Reports"
    )

    recent_df = dashboard_df.copy()

    if "Date_Time" in recent_df.columns:

        recent_df["Date_Time"] = pd.to_datetime(
            recent_df["Date_Time"],
            errors="coerce"
        )

        recent_df = (
            recent_df
            .sort_values(
                "Date_Time",
                ascending=False
            )
            .head(10)
        )

        recent_df["Date_Time"] = (
            recent_df["Date_Time"]
            .dt.strftime(
                "%Y-%m-%d %H:%M"
            )
        )

    else:

        recent_df = recent_df.head(10)

    st.dataframe(
        recent_df,
        use_container_width=True,
        hide_index=True
        )
        # =====================================================
    # SEX DISTRIBUTION
    # =====================================================

    st.markdown(
        "#### 👥 Sex Distribution"
    )

    sex_counts = (
        dashboard_df["Sex"]
        .astype(str)
        .str.upper()
        .replace("", "UNKNOWN")
        .value_counts()
    )

    sex_chart_df = (
        sex_counts
        .rename("Cases")
        .reset_index()
    )

    sex_chart_df.columns = [
        "Sex",
        "Cases"
    ]

    st.bar_chart(
    sex_chart_df.set_index("Sex"),
    horizontal=True
    )
        # =====================================================
    # AGE GROUP DISTRIBUTION
    # =====================================================

    st.markdown(
        "#### 📈 Age Group Distribution"
    )

    age_data = pd.to_numeric(
        dashboard_df["Age"],
        errors="coerce"
    )

    age_groups = pd.cut(
        age_data,
        bins=[
            -1,
            17,
            30,
            45,
            60,
            120
        ],
        labels=[
            "0–17",
            "18–30",
            "31–45",
            "46–60",
            "61–120"
        ]
    )

    age_counts = (
        age_groups
        .value_counts()
        .sort_index()
    )

    age_chart_df = (
        age_counts
        .rename("Cases")
        .reset_index()
    )

    age_chart_df.columns = [
        "Age Group",
        "Cases"
    ]

    st.bar_chart(
        age_chart_df.set_index(
            "Age Group"
        )
    )
        # =====================================================
    # PRIORITY-WISE AGE DISTRIBUTION
    # =====================================================

    st.markdown(
        "#### 🎯 Priority-wise Age Distribution"
    )

    priority_age_df = dashboard_df.copy()

    priority_age_df["Age"] = pd.to_numeric(
        priority_age_df["Age"],
        errors="coerce"
    )

    priority_age_df["Age Group"] = pd.cut(
        priority_age_df["Age"],
        bins=[
            -1,
            17,
            30,
            45,
            60,
            120
        ],
        labels=[
            "0–17",
            "18–30",
            "31–45",
            "46–60",
            "61–120"
        ]
    )

    priority_age_table = pd.crosstab(
        priority_age_df["Age Group"],
        priority_age_df["Priority"]
    )

    priority_age_table = priority_age_table.reindex(
        columns=[
            "HIGH",
            "MODERATE",
            "LOW"
        ],
        fill_value=0
    )

    st.bar_chart(
        priority_age_table
    )
        # =====================================================
    # PRIORITY-WISE SEX DISTRIBUTION
    # =====================================================

    st.markdown(
        "#### 👥 Priority-wise Sex Distribution"
    )

    priority_sex_df = dashboard_df.copy()

    priority_sex_df["Sex"] = (
        priority_sex_df["Sex"]
        .astype(str)
        .str.upper()
        .replace("", "UNKNOWN")
    )

    priority_sex_table = pd.crosstab(
        priority_sex_df["Sex"],
        priority_sex_df["Priority"]
    )

    priority_sex_table = priority_sex_table.reindex(
        columns=[
            "HIGH",
            "MODERATE",
            "LOW"
        ],
        fill_value=0
    )

    st.bar_chart(
        priority_sex_table
    )
        # =====================================================
    # DRUG-WISE PRIORITY DISTRIBUTION
    # =====================================================

    st.markdown(
        "#### 💊 Drug-wise Priority Distribution"
    )

    drug_priority_df = dashboard_df.copy()

    drug_priority_df["Drug"] = (
        drug_priority_df["Drug"]
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
    )

    drug_priority_table = pd.crosstab(
        drug_priority_df["Drug"],
        drug_priority_df["Priority"]
    )

    drug_priority_table = drug_priority_table.reindex(
        columns=[
            "HIGH",
            "MODERATE",
            "LOW"
        ],
        fill_value=0
    )

    # Show top 10 drugs by total reports
    drug_priority_table["TOTAL"] = (
        drug_priority_table[
            ["HIGH", "MODERATE", "LOW"]
        ].sum(axis=1)
    )

    drug_priority_table = (
        drug_priority_table
        .sort_values(
            "TOTAL",
            ascending=False
        )
        .head(10)
        .drop(columns="TOTAL")
    )

    st.bar_chart(
        drug_priority_table
    )
        # =====================================================
    # ADR-WISE PRIORITY DISTRIBUTION
    # =====================================================

    st.markdown(
        "#### ⚠️ ADR-wise Priority Distribution"
    )

    adr_priority_df = dashboard_df.copy()

    adr_priority_df["ADR"] = (
        adr_priority_df["ADR"]
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
    )

    adr_priority_table = pd.crosstab(
        adr_priority_df["ADR"],
        adr_priority_df["Priority"]
    )

    adr_priority_table = adr_priority_table.reindex(
        columns=[
            "HIGH",
            "MODERATE",
            "LOW"
        ],
        fill_value=0
    )

    # Show top 10 ADRs by total reports
    adr_priority_table["TOTAL"] = (
        adr_priority_table[
            ["HIGH", "MODERATE", "LOW"]
        ].sum(axis=1)
    )

    adr_priority_table = (
        adr_priority_table
        .sort_values(
            "TOTAL",
            ascending=False
        )
        .head(10)
        .drop(columns="TOTAL")
    )

    st.bar_chart(
        adr_priority_table
    )
        # =====================================================
    # SERIOUSNESS DISTRIBUTION
    # =====================================================

    st.markdown(
        "#### 🚨 Seriousness Distribution"
    )

    seriousness_counts = (
        dashboard_df["Seriousness"]
        .astype(str)
        .str.strip()
        .str.upper()
        .replace("", "UNKNOWN")
        .value_counts()
    )

    seriousness_chart_df = (
        seriousness_counts
        .rename("Cases")
        .reset_index()
    )

    seriousness_chart_df.columns = [
        "Seriousness",
        "Cases"
    ]

    st.bar_chart(
        seriousness_chart_df.set_index(
            "Seriousness"
        )
    )


        # =====================================================
    # ADR HISTORY
    # =====================================================

    st.subheader(
        "📚 ADR Report History"
    )

    df = pd.DataFrame(
        st.session_state.adr_history
    )

    search_text = st.text_input(
        "🔎 Search ADR History",
        placeholder="Search Patient ID, Drug, or ADR"
    )

    priority_filter = st.selectbox(
        "🎯 Filter by Priority",
        ["ALL", "HIGH", "MODERATE", "LOW"]
    )

    if search_text.strip():
        search_mask = (
            df.astype(str)
            .apply(
                lambda row: row.str.contains(
                    search_text,
                    case=False,
                    na=False,
                    regex=False
                ).any(),
                axis=1
            )
        )

        filtered_df = df[search_mask]

    else:
        filtered_df = df

    if priority_filter != "ALL":
        filtered_df = filtered_df[
            filtered_df["Priority"]
            .astype(str)
            .str.upper()
            == priority_filter
        ]

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )
    if not filtered_df.empty:
        st.markdown("### 🔍 ADR Case Details")

        # Use the unique Case_Reference when available so duplicate
        # Patient ID / Drug / ADR combinations cannot select the wrong row.
        if "Case_Reference" in filtered_df.columns:
            case_options = filtered_df["Case_Reference"].astype(str)
        else:
            case_options = (
                filtered_df["Patient_ID"].astype(str)
                + " | "
                + filtered_df["Drug"].astype(str)
                + " | "
                + filtered_df["ADR"].astype(str)
            )

        selected_case = st.selectbox(
            "Select a Case",
            case_options.tolist()
        )

        selected_index = case_options[
            case_options == selected_case
        ].index[0]

        selected_row = filtered_df.loc[selected_index]

        st.write("**Patient ID:**", selected_row.get("Patient_ID", ""))
        st.write("**Age:**", selected_row.get("Age", ""))
        st.write("**Sex:**", selected_row.get("Sex", ""))
        st.write("**Drug:**", selected_row.get("Drug", ""))
        st.write("**ADR:**", selected_row.get("ADR", ""))
        st.write("**Seriousness:**", selected_row.get("Seriousness", ""))
        st.write("**Priority:**", selected_row.get("Priority", ""))
        st.write("**Decision Source:**", selected_row.get("Decision_Source", ""))
        st.write("**Reason:**", selected_row.get("Reason", ""))
        st.write("**Case Reference:**", selected_row.get("Case_Reference", ""))
        st.write("**Date & Time:**", selected_row.get("Date_Time", ""))
        # =====================================================
# STEP 62.2 — ADR CASE REPORT
# =====================================================

# selected_row only exists when ADR history contains at least one case.
# Disable report generation when no case is available.
selected_row = locals().get("selected_row", None)

st.markdown("---")
st.markdown("### 📄 ADR Case Report")

if st.button(
    "📄 Generate ADR Case Report",
    use_container_width=True,
    disabled=selected_row is None
):

    # Get seriousness safely
    case_seriousness = selected_row.get(
        "Seriousness",
        selected_row.get(
            "Seriousness_Flag",
            "Uncertain"
        )
    )

    # Get priority safely
    case_priority = str(
        selected_row.get(
            "Priority",
            "UNKNOWN"
        )
    ).upper()

    # Recommendation
    if case_priority == "HIGH":
        recommendation = (
            "Immediate pharmacovigilance review recommended."
        )

    elif case_priority == "MODERATE":
        recommendation = (
            "Clinical and pharmacovigilance review recommended."
        )

    elif case_priority == "LOW":
        recommendation = (
            "Routine pharmacovigilance review."
        )

    else:
        recommendation = (
            "Additional information or professional review "
            "may be required."
        )

    # Report Header
    st.markdown(
        "## 🛡️ PHARMAGUARD"
    )

    st.caption(
        "AI-Assisted ADR Risk Prioritization System"
    )

    st.caption(
        "Pharmacovigilance • Proof of Concept"
    )

    # -------------------------------------------------
    # 1. CASE INFORMATION
    # -------------------------------------------------

    st.markdown("### 1. Case Information")
    
    st.write(
    "**Case Reference:**",
    selected_row.get("Case_Reference", "")
        )

    st.write(
        "**Patient ID:**",
        selected_row.get("Patient_ID", "")
    )

    st.write(
        "**Age:**",
        selected_row.get("Age", "")
    )

    st.write(
        "**Sex:**",
        selected_row.get("Sex", "")
    )

    st.write(
        "**Date & Time:**",
        selected_row.get("Date_Time", "")
    )

    # -------------------------------------------------
    # 2. DRUG INFORMATION
    # -------------------------------------------------

    st.markdown("### 2. Drug Information")

    st.write(
        "**Drug Name:**",
        selected_row.get("Drug", "")
    )

    # -------------------------------------------------
    # 3. ADR INFORMATION
    # -------------------------------------------------

    st.markdown("### 3. ADR Information")

    st.write(
        "**Reported ADR:**",
        selected_row.get("ADR", "")
    )

    # -------------------------------------------------
    # 4. PHARMAGUARD ASSESSMENT
    # -------------------------------------------------

    st.markdown(
        "### 4. PHARMAGUARD Assessment"
    )

    st.write(
        "**Seriousness:**",
        case_seriousness
    )

    st.write(
        "**Risk Priority:**",
        case_priority
    )

    st.write(
        "**Reason:**",
        selected_row.get("Reason", "")
    )

    # -------------------------------------------------
    # 5. RECOMMENDED ACTION
    # -------------------------------------------------

    st.markdown(
        "### 5. Recommended Action"
    )

    if case_priority == "HIGH":
        st.error(
            "🚨 HIGH PRIORITY\n\n"
            + recommendation
        )

    elif case_priority == "MODERATE":
        st.warning(
            "⚠️ MODERATE PRIORITY\n\n"
            + recommendation
        )

    elif case_priority == "LOW":
        st.success(
            "✅ LOW PRIORITY\n\n"
            + recommendation
        )

    else:
        st.info(
            "❓ PRIORITY UNCERTAIN\n\n"
            + recommendation
        )

    # -------------------------------------------------
    # 6. IMPORTANT DISCLAIMER
    # -------------------------------------------------

    st.markdown(
        "### 6. Important Disclaimer"
    )

    st.info(
        "PHARMAGUARD is an AI-assisted pharmacovigilance "
        "prioritization prototype. It does not establish "
        "causality, provide diagnosis or treatment, or "
        "replace professional clinical judgment."
    )

    st.caption(
        "Generated by PHARMAGUARD • "
        "Pharmacovigilance Proof of Concept"
    )
    # =====================================================
# STEP 62.3 — DOWNLOAD ADR CASE REPORT
# =====================================================

    report_text = f"""
PHARMAGUARD ADR CASE REPORT
========================================

AI-Assisted ADR Risk Prioritization System
Pharmacovigilance • Proof of Concept


1. CASE INFORMATION
----------------------------------------
Patient ID: {selected_row.get("Patient_ID", "")}
Age: {selected_row.get("Age", "")}
Sex: {selected_row.get("Sex", "")}
Date & Time: {selected_row.get("Date_Time", "")}


2. DRUG INFORMATION
----------------------------------------
Drug Name: {selected_row.get("Drug", "")}


3. ADR INFORMATION
----------------------------------------
Reported ADR: {selected_row.get("ADR", "")}


4. PHARMAGUARD ASSESSMENT
----------------------------------------
Seriousness: {case_seriousness}
Risk Priority: {case_priority}
Reason: {selected_row.get("Reason", "")}


5. RECOMMENDED ACTION
----------------------------------------
{recommendation}


6. IMPORTANT DISCLAIMER
----------------------------------------
PHARMAGUARD is an AI-assisted pharmacovigilance
prioritization prototype.

It does not establish causality, provide diagnosis
or treatment, or replace professional clinical judgment.


========================================
Generated by PHARMAGUARD
Pharmacovigilance Proof of Concept
========================================
"""

    st.download_button(
        label="⬇️ Download ADR Case Report",
        data=report_text,
        file_name=(
            f"PHARMAGUARD_ADR_Report_"
            f"{selected_row.get('Patient_ID', 'Case')}.txt"
        ),
        mime="text/plain",
        use_container_width=True
    )
    # =====================================================
# STEP 62.4 — PROFESSIONAL PDF ADR CASE REPORT
# =====================================================

    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle
    )
    from io import BytesIO

    pdf_buffer = BytesIO()

    pdf_doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "PHARMAGUARDTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "PHARMAGUARDSubtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=13,
        spaceBefore=10,
        spaceAfter=6
    )

    normal_style = ParagraphStyle(
        "NormalText",
        parent=styles["Normal"],
        fontSize=10,
        leading=14
    )

    pdf_content = []

    # Header
    pdf_content.append(
        Paragraph(
            "🛡️ PHARMAGUARD",
            title_style
        )
    )

    pdf_content.append(
        Paragraph(
            "AI-Assisted ADR Risk Prioritization System",
            subtitle_style
        )
    )

    pdf_content.append(
        Paragraph(
            "Pharmacovigilance • Proof of Concept",
            subtitle_style
        )
    )

    # Case Information
    pdf_content.append(
        Paragraph(
            "1. Case Information",
            heading_style
        )
    )

    case_data = [
        ["Case Reference", str(
    selected_row.get("Case_Reference", "")
)],
        ["Patient ID", str(
            selected_row.get("Patient_ID", "")
        )],
        ["Age", str(
            selected_row.get("Age", "")
        )],
        ["Sex", str(
            selected_row.get("Sex", "")
        )],
        ["Date & Time", str(
            selected_row.get("Date_Time", "")
        )]
    ]

    case_table = Table(
        case_data,
        colWidths=[130, 350]
    )

    case_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    pdf_content.append(case_table)

    # Drug Information
    pdf_content.append(
        Paragraph(
            "2. Drug Information",
            heading_style
        )
    )

    drug_data = [
        ["Drug Name", str(
            selected_row.get("Drug", "")
        )]
    ]

    drug_table = Table(
        drug_data,
        colWidths=[130, 350]
    )

    drug_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    pdf_content.append(drug_table)

    # ADR Information
    pdf_content.append(
        Paragraph(
            "3. ADR Information",
            heading_style
        )
    )

    adr_data = [
        ["Reported ADR", str(
            selected_row.get("ADR", "")
        )]
    ]

    adr_table = Table(
        adr_data,
        colWidths=[130, 350]
    )

    adr_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    pdf_content.append(adr_table)

    # PHARMAGUARD Assessment
    pdf_content.append(
        Paragraph(
            "4. PHARMAGUARD Assessment",
            heading_style
        )
    )

    assessment_data = [
        ["Seriousness", str(case_seriousness)],
        ["Risk Priority", str(case_priority)],
        ["Reason", str(
            selected_row.get("Reason", "")
        )]
    ]

    assessment_table = Table(
        assessment_data,
        colWidths=[130, 350]
    )

    assessment_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    pdf_content.append(assessment_table)

    # Recommended Action
    pdf_content.append(
        Paragraph(
            "5. Recommended Action",
            heading_style
        )
    )

    pdf_content.append(
        Paragraph(
            recommendation,
            normal_style
        )
    )

    # Disclaimer
    pdf_content.append(
        Paragraph(
            "6. Important Disclaimer",
            heading_style
        )
    )

    pdf_content.append(
        Paragraph(
            "PHARMAGUARD is an AI-assisted "
            "pharmacovigilance prioritization prototype. "
            "It does not establish causality, provide "
            "diagnosis or treatment, or replace professional "
            "clinical judgment.",
            normal_style
        )
    )

    pdf_content.append(Spacer(1, 20))

    pdf_content.append(
        Paragraph(
            "Generated by PHARMAGUARD • "
            "Pharmacovigilance Proof of Concept",
            subtitle_style
        )
    )

    pdf_doc.build(pdf_content)

    pdf_buffer.seek(0)

    st.download_button(
        label="📥 Download Professional PDF Report",
        data=pdf_buffer,
        file_name=(
            f"PHARMAGUARD_ADR_Report_"
            f"{selected_row.get('Patient_ID', 'Case')}.pdf"
        ),
        mime="application/pdf",
        use_container_width=True
    )

    st.download_button(
        "⬇️ Download ADR History (CSV)",
        data=df.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="PHARMAGUARD_ADR_History.csv",
        mime="text/csv",
        use_container_width=True
    )
        # =====================================================
    # DASHBOARD SUMMARY REPORT
    # =====================================================

    st.markdown(
        "#### 📄 Dashboard Summary Report"
    )

    summary_report = pd.DataFrame({
        "Metric": [
            "Total ADR Cases",
            "High Priority Cases",
            "Moderate Priority Cases",
            "Low Priority Cases",
            "Serious Cases",
            "Uncertain Seriousness Cases"
        ],
        "Count": [
            total_cases,
            high_cases,
            moderate_cases,
            low_cases,
            int(
                (
                    dashboard_df["Seriousness"]
                    .astype(str)
                    .str.upper()
                    == "YES"
                ).sum()
            ),
            int(
                (
                    dashboard_df["Seriousness"]
                    .astype(str)
                    .str.upper()
                    == "UNCERTAIN"
                ).sum()
            )
        ]
    })

    st.dataframe(
        summary_report,
        use_container_width=True,
        hide_index=True
    )

    summary_csv = summary_report.to_csv(
        index=False
    )

    st.download_button(
        label="⬇️ Download Dashboard Summary",
        data=summary_csv,
        file_name="PHARMAGUARD_Dashboard_Summary.csv",
        mime="text/csv",
        use_container_width=True
        )

    if st.button(
        "🗑️ Clear Current Session History",
        use_container_width=True
    ):
        st.session_state.adr_history = []
        st.rerun()


st.markdown("""
<div class="pg-disclaimer">
<b>Scientific disclaimer:</b> PHARMAGUARD is a proof-of-concept AI-assisted pharmacovigilance review-prioritization system. Its HIGH/MODERATE/LOW outputs are project-defined review priorities and do not establish ADR causality, diagnosis, treatment, regulatory seriousness, or clinical decision-making.
</div>
""", unsafe_allow_html=True)
