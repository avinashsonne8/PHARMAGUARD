import streamlit as st
import pandas as pd
import joblib
import requests
import re

from datetime import datetime


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="PHARMAGUARD",
    page_icon="💊",
    layout="centered"
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

</style>
<div class="pg-header">
<div class="pg-shield">🛡️</div>
<div class="pg-title">PHARMAGUARD</div>
<div class="pg-subtitle">AI-Assisted ADR Risk Prioritization System</div>
<div class="pg-tag">Pharmacovigilance • Proof of Concept</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# MODEL + GOOGLE SHEET
# =========================================================

MODEL_FILE = "PHARMAGUARD_RandomForest_Model.joblib"

GOOGLE_SHEET_URL = st.secrets["GOOGLE_SHEET_URL"]


# =========================================================
# LOAD ML MODEL
# =========================================================

try:
    model = joblib.load(MODEL_FILE)

except Exception as e:
    st.error("Model could not be loaded.")
    st.code(str(e))
    st.stop()


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
    "breathing difficulty",
    "breathing trouble",
    "trouble breathing",
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
    "persistent",
    "prolonged",
    "recurrent",
    "significant dizziness",
    "marked dizziness",
    "muscle pain and weakness",
    "muscle pain with weakness",
    "dehydration"
]


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

def load_from_google_sheet():

    try:

        response = requests.get(
            GOOGLE_SHEET_URL,
            timeout=15
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


def has_context_protection(text, serious_pattern):

    text = " ".join(
        str(text).lower().strip().split()
    )

    serious_pattern = str(serious_pattern).lower().strip()

    match = re.search(
        rf"(?<!\w){re.escape(serious_pattern)}(?!\w)",
        text
    )

    if not match:
        return False

    # Context before the serious phrase
    context_before = text[
        max(0, match.start() - 60):match.start()
    ]

    # Context after the serious phrase
    context_after = text[
        match.end():match.end() + 60
    ]

    # Check negation / ruled-out context BEFORE the phrase
    for pattern in NEGATION_PATTERNS:

        if re.search(
            rf"(?<!\w){re.escape(pattern)}(?!\w)",
            context_before
        ):
            return True

    # Check negation / ruled-out context AFTER the phrase
    for pattern in NEGATION_PATTERNS:

        if re.search(
            rf"(?<!\w){re.escape(pattern)}(?!\w)",
            context_after
        ):
            return True

    # Check history context BEFORE the phrase
    for pattern in HISTORY_PATTERNS:

        if re.search(
            rf"(?<!\w){re.escape(pattern)}(?!\w)",
            context_before
        ):
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
# PATIENT INPUT
# =========================================================

st.markdown('<div class="pg-section"><b>👤 Patient Information</b></div>', unsafe_allow_html=True)

patient_id = st.text_input(
    "Patient ID",
    placeholder="Example: PHG-0001",
    help="Enter a project patient identifier. Do not enter unnecessary personally identifiable information."
)

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
]


    moderate_hits = matches(
    adr,
    MODERATE_PATTERNS
)
    moderate_hits = [
    pattern
    for pattern in moderate_hits
    if not has_context_protection(adr, pattern)
    ]

  
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
    case_reference = "PHG-CASE-" + str(len(st.session_state.adr_history) + 1).zfill(3)
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
            if serious_hits
            else "Uncertain",

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

if st.session_state.get(
    "adr_history"
):

    st.markdown("---")

    st.markdown("""
    <div class="pg-dashboard-header">
        <div class="pg-dashboard-icon">📊</div>
        <div>
            <div class="pg-dashboard-title">PHARMAGUARD Dashboard</div>
            <div class="pg-dashboard-subtitle">ADR monitoring • Priority overview • Pharmacovigilance review support</div>
        </div>
    </div>
    <div class="pg-note">📌 Dashboard metrics are based on ADR cases currently available in the app session/database view.</div>
    """, unsafe_allow_html=True)


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
        st.write("**Reason:**", selected_row.get("Reason", ""))
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
