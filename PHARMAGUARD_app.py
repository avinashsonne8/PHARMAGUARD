# PHARMAGUARD Professional UI v27 — Clean Professional Navigation
# Dashboard HTML rendering fix — backend/Safety Gate/ML/database logic preserved.
import streamlit as st
import pandas as pd
import joblib
import requests
import re
import uuid
import textwrap
import html
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


/* =========================================================
   UI-3 — PROFESSIONAL ANALYSIS RESULT
   ========================================================= */
.pg-result-hero {
    padding: 20px;
    margin: 8px 0 16px 0;
    border-radius: 18px;
    border: 1px solid #dbe7ef;
    background: linear-gradient(135deg,#f7fbff 0%,#ffffff 100%);
    box-shadow: 0 4px 16px rgba(30,60,90,.05);
}
.pg-result-kicker {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 5px;
}
.pg-result-main {
    display: flex;
    align-items: center;
    gap: 15px;
}
.pg-result-main-icon {
    width: 58px;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    font-size: 30px;
    flex: 0 0 58px;
}
.pg-result-main-label {
    font-size: 27px;
    font-weight: 850;
    line-height: 1.1;
    color: #102a43;
}
.pg-result-main-message {
    margin-top: 5px;
    color: #52606d;
    font-size: 13px;
    line-height: 1.45;
}
.pg-result-high-main { background: #fff0f0; border: 1px solid #f2caca; }
.pg-result-moderate-main { background: #fff8e8; border: 1px solid #f0ddb0; }
.pg-result-low-main { background: #eef9f1; border: 1px solid #cce5d2; }
.pg-result-unknown-main { background: #f4f6f8; border: 1px solid #dce2e7; }
.pg-result-high-icon { background: #ffe0e0; }
.pg-result-moderate-icon { background: #ffedbf; }
.pg-result-low-icon { background: #dff2e3; }
.pg-result-unknown-icon { background: #e7ebee; }

.pg-case-strip {
    display: grid;
    grid-template-columns: 1.4fr 0.7fr 0.7fr;
    gap: 10px;
    margin: 0 0 16px 0;
}
.pg-case-item {
    padding: 12px 14px;
    border: 1px solid #dfe7ed;
    border-radius: 12px;
    background: #ffffff;
}
.pg-case-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: .7px;
    color: #7a8793;
    font-weight: 800;
}
.pg-case-value {
    margin-top: 4px;
    font-size: 14px;
    font-weight: 750;
    color: #263746;
    word-break: break-word;
}

.pg-assessment-card {
    padding: 16px;
    border: 1px solid #dfe7ed;
    border-radius: 15px;
    background: #ffffff;
    margin: 0 0 14px 0;
    box-shadow: 0 2px 10px rgba(30,60,90,.035);
}
.pg-assessment-title {
    font-size: 16px;
    font-weight: 800;
    color: #17324d;
    margin-bottom: 11px;
}
.pg-assessment-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}
.pg-assessment-item {
    padding: 11px 12px;
    border-radius: 10px;
    background: #f7fafc;
    border: 1px solid #e5edf2;
}
.pg-assessment-label {
    font-size: 10px;
    color: #7a8793;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .6px;
}
.pg-assessment-value {
    margin-top: 4px;
    font-size: 13px;
    color: #334e68;
    line-height: 1.45;
    word-break: break-word;
}
.pg-signal-card {
    padding: 14px 15px;
    border-radius: 13px;
    background: #f7fafc;
    border: 1px solid #dfe7ed;
    margin: 0 0 14px 0;
}
.pg-signal-title {
    font-size: 12px;
    font-weight: 800;
    color: #486581;
    text-transform: uppercase;
    letter-spacing: .6px;
}
.pg-signal-text {
    margin-top: 6px;
    font-size: 14px;
    line-height: 1.5;
    color: #243b53;
}
.pg-action-card {
    padding: 15px 16px;
    border-radius: 14px;
    background: #f4f9fd;
    border: 1px solid #d6e6f1;
    margin: 0 0 14px 0;
}
.pg-action-title {
    font-size: 15px;
    font-weight: 800;
    color: #17324d;
    margin-bottom: 5px;
}
.pg-action-text {
    font-size: 13px;
    line-height: 1.5;
    color: #52606d;
}
.pg-result-disclaimer {
    font-size: 11px;
    line-height: 1.5;
    color: #6b7785;
    padding: 10px 12px;
    border-radius: 10px;
    background: #f8fafb;
    border: 1px solid #e3e8ec;
    margin-top: 12px;
}
@media (max-width: 700px) {
    .pg-result-main-label { font-size: 23px; }
    .pg-result-main-icon { width: 50px; height: 50px; flex-basis: 50px; font-size: 26px; }
    .pg-case-strip { grid-template-columns: 1fr; }
    .pg-assessment-grid { grid-template-columns: 1fr; }
}

\n.pg-db-status { display:flex; justify-content:space-between; gap:12px; padding:12px 14px; margin:10px 0 18px 0; border:1px solid #dbe8f1; border-radius:12px; background:#f7fbff; color:#536575; font-size:13px; }\n.pg-db-status span:first-child { font-weight:800; color:#236b3a; }\n@media (max-width: 700px) { .pg-db-status { display:block; } .pg-db-status span { display:block; margin:3px 0; } }\n.pg-disclaimer { margin-top:22px; padding:12px 14px; border-radius:10px; background:#f7f8fa; border:1px solid #e1e5e9; color:#66717b; font-size:12px; line-height:1.5; }
div.stButton > button { border-radius:10px; font-weight:700; min-height:44px; }
@media (max-width: 700px) { .pg-appbar { padding:9px 10px; } .pg-hero-title { font-size:21px; } .pg-title { font-size:29px; } .pg-subtitle { font-size:14px; } }


/* =========================================================
   UI-2 — PROFESSIONAL NEW ADR ANALYSIS
   ========================================================= */
.pg-analysis-hero {
    padding: 20px;
    margin: 8px 0 16px 0;
    border-radius: 18px;
    background: linear-gradient(135deg,#f1f8ff 0%,#ffffff 100%);
    border: 1px solid #d7e7f3;
    box-shadow: 0 4px 16px rgba(30,60,90,.05);
}
.pg-analysis-title {
    font-size: 25px;
    font-weight: 800;
    color: #102a43;
    margin-bottom: 4px;
}
.pg-analysis-subtitle {
    color: #657786;
    font-size: 13px;
    line-height: 1.5;
}
.pg-stepbar {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin: 0 0 18px 0;
}
.pg-step {
    flex: 1 1 150px;
    padding: 9px 11px;
    border-radius: 10px;
    background: #f7fafc;
    border: 1px solid #dbe6ee;
    color: #52606d;
    font-size: 12px;
    font-weight: 700;
    text-align: center;
}
.pg-step-active {
    background: #eaf4fb;
    border-color: #b9d5e8;
    color: #174a6b;
}
.pg-form-card {
    padding: 16px;
    margin: 0 0 14px 0;
    border-radius: 16px;
    background: #ffffff;
    border: 1px solid #dbe7ef;
    box-shadow: 0 3px 12px rgba(30,60,90,.045);
}
.pg-form-title {
    font-size: 16px;
    font-weight: 800;
    color: #243b53;
    margin-bottom: 3px;
}
.pg-form-subtitle {
    font-size: 12px;
    color: #7b8794;
    margin-bottom: 10px;
}
.pg-id-card {
    padding: 12px 14px;
    border-radius: 12px;
    background: #f5f9fc;
    border: 1px solid #d9e8f2;
    margin: 0 0 12px 0;
}
.pg-id-label {
    font-size: 11px;
    font-weight: 700;
    color: #657786;
    text-transform: uppercase;
    letter-spacing: .4px;
}
.pg-id-value {
    margin-top: 3px;
    font-size: 15px;
    font-weight: 800;
    color: #102a43;
    word-break: break-word;
}
.pg-input-tip {
    padding: 10px 12px;
    margin: 8px 0 0 0;
    border-radius: 10px;
    background: #f8fbfd;
    border: 1px solid #e1ebf2;
    color: #607080;
    font-size: 12px;
    line-height: 1.5;
}
.pg-analyze-box {
    padding: 14px;
    margin-top: 14px;
    border-radius: 16px;
    background: linear-gradient(135deg,#f7fbfe 0%,#ffffff 100%);
    border: 1px solid #d8e7f1;
}
.pg-analyze-title {
    font-size: 15px;
    font-weight: 800;
    color: #243b53;
    margin-bottom: 4px;
}
.pg-analyze-subtitle {
    font-size: 12px;
    color: #718096;
    margin-bottom: 10px;
}
div.stButton > button[kind="primary"] {
    min-height: 48px;
    border-radius: 12px;
    font-weight: 800;
    letter-spacing: .2px;
}
@media (max-width: 700px) {
    .pg-analysis-title { font-size: 21px; }
    .pg-analysis-hero { padding: 16px; }
    .pg-step { flex-basis: 100%; }
    .pg-form-card { padding: 13px; }
}

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
# UI-5 — CASE REPORTS / ABOUT / SETTINGS STYLES
# =========================================================
st.markdown(textwrap.dedent("""
<style>
.pg-ui5-hero { padding:18px; border-radius:16px; background:linear-gradient(135deg,#f4faff,#ffffff); border:1px solid #d8e8f4; margin-bottom:16px; }
.pg-ui5-title { font-size:25px; font-weight:800; margin-bottom:4px; }
.pg-ui5-sub { color:#65727d; font-size:14px; line-height:1.5; }
.pg-case-card { padding:18px; border:1px solid #dbe5ec; border-radius:16px; background:#fff; margin:10px 0 16px 0; box-shadow:0 2px 10px rgba(30,60,90,.04); }
.pg-case-ref { font-size:12px; color:#687682; font-weight:700; letter-spacing:.3px; }
.pg-case-title { font-size:20px; font-weight:800; margin-top:4px; }
.pg-case-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; margin-top:14px; }
.pg-case-field { padding:10px 12px; background:#f7fafc; border-radius:10px; border:1px solid #e6edf2; }
.pg-case-label { font-size:11px; color:#71808b; font-weight:700; text-transform:uppercase; }
.pg-case-value { font-size:14px; font-weight:600; margin-top:3px; word-break:break-word; }
.pg-priority { display:inline-block; padding:7px 13px; border-radius:999px; font-weight:800; font-size:13px; }
.pg-high { background:#fff0f0; color:#a61b1b; border:1px solid #f2c7c7; }
.pg-moderate { background:#fff7df; color:#8a5a00; border:1px solid #eed99b; }
.pg-low { background:#edf8f0; color:#246b37; border:1px solid #cce7d3; }
.pg-uncertain { background:#f2f4f6; color:#59646e; border:1px solid #dce1e5; }
.pg-section-card { padding:16px; border:1px solid #dbe5ec; border-radius:14px; background:#fff; margin:10px 0; }
.pg-section-card h4 { margin:0 0 6px 0; }
.pg-method-step { padding:12px 14px; border-left:4px solid #2b6f9f; background:#f7fafc; border-radius:8px; margin:7px 0; }
.pg-disclaimer-box { padding:16px; border-radius:14px; background:#fff8e8; border:1px solid #ead9a7; line-height:1.55; }
.pg-setting-row { padding:13px 14px; border-bottom:1px solid #e8edf1; }
.pg-setting-label { font-size:12px; color:#71808b; font-weight:700; }
.pg-setting-value { font-size:15px; font-weight:700; margin-top:2px; }
@media (max-width:700px) { .pg-ui5-title{font-size:21px;} .pg-case-grid{grid-template-columns:1fr;} .pg-case-card{padding:14px;} }

/* =========================================================
   UI-7 — PROFESSIONAL SIDEBAR NAVIGATION
   ========================================================= */
section[data-testid="stSidebar"] {
    background: #f8fbfd;
    border-right: 1px solid #dce7ee;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.1rem;
}

.pg-sidebar-brand {
    padding: 4px 2px 14px 2px;
}

.pg-sidebar-brand-row {
    display: flex;
    align-items: center;
    gap: 10px;
}

.pg-sidebar-logo {
    width: 42px;
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 13px;
    background: #102a43;
    font-size: 22px;
    box-shadow: 0 5px 14px rgba(16,42,67,.12);
}

.pg-sidebar-name {
    font-size: 17px;
    font-weight: 850;
    letter-spacing: .35px;
    color: #102a43;
}

.pg-sidebar-subtitle {
    margin-top: 2px;
    font-size: 10px;
    font-weight: 650;
    color: #71808b;
}

.pg-sidebar-status {
    display: inline-block;
    margin-top: 10px;
    padding: 4px 9px;
    border-radius: 999px;
    background: #eaf6ef;
    border: 1px solid #cfe8d8;
    color: #276749;
    font-size: 10px;
    font-weight: 750;
}

.pg-sidebar-section {
    margin: 16px 2px 6px 2px;
    font-size: 9px;
    line-height: 1.2;
    font-weight: 850;
    letter-spacing: 1.15px;
    color: #8292a2;
}

section[data-testid="stSidebar"] div.stButton > button {
    min-height: 42px;
    margin: 2px 0;
    padding: 0 12px;
    border-radius: 10px;
    border: 1px solid transparent;
    text-align: left;
    justify-content: flex-start;
    font-size: 13px;
    font-weight: 700;
    box-shadow: none;
}

section[data-testid="stSidebar"] div.stButton > button[kind="secondary"] {
    background: transparent;
    color: #425466;
}

section[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {
    background: #edf4f8;
    border-color: #d8e5ec;
    color: #102a43;
}

section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background: #102a43;
    border-color: #102a43;
    color: #ffffff;
    box-shadow: 0 4px 12px rgba(16,42,67,.14);
}

section[data-testid="stSidebar"] div.stButton > button[kind="primary"]:hover {
    background: #173d5f;
    border-color: #173d5f;
}

.pg-sidebar-divider {
    height: 1px;
    margin: 18px 2px 12px 2px;
    background: #dce7ee;
}

.pg-sidebar-note {
    padding: 12px;
    border-radius: 12px;
    background: #ffffff;
    border: 1px solid #dce7ee;
}

.pg-sidebar-note-title {
    font-size: 11px;
    font-weight: 800;
    color: #243b53;
}

.pg-sidebar-note-text {
    margin-top: 4px;
    font-size: 10px;
    line-height: 1.45;
    color: #71808b;
}

@media (max-width: 700px) {
    .pg-sidebar-name { font-size: 16px; }
    .pg-sidebar-section { margin-top: 13px; }
    section[data-testid="stSidebar"] div.stButton > button {
        min-height: 44px;
    }
}


.pg-sidebar-section { margin-top: 12px; margin-bottom: 6px; font-size: 10px; letter-spacing: 1.2px; font-weight: 800; color: #7a8793; }
.pg-sidebar-note-text { font-size: 11px; line-height: 1.45; color: #71808b; }
button[data-baseweb="tab"] { font-weight: 700; }
</style>
""").strip(), unsafe_allow_html=True)



# =========================================================
# UI-6 — FINAL MOBILE POLISH
# =========================================================
st.markdown(textwrap.dedent("""
<style>
.block-container { padding-top: 1rem; padding-bottom: 2.5rem; }

@media (max-width: 700px) {
    .block-container {
        padding-left: 0.75rem;
        padding-right: 0.75rem;
        padding-top: 0.65rem;
    }
    h1 { font-size: 1.55rem !important; }
    h2 { font-size: 1.30rem !important; }
    h3 { font-size: 1.10rem !important; }
    p, li, label, .stMarkdown { line-height: 1.45; }
}

.pg-ui6-card {
    padding: 15px 16px;
    margin: 0 0 13px 0;
    border: 1px solid #dce6ed;
    border-radius: 15px;
    background: #ffffff;
    box-shadow: 0 2px 10px rgba(30,60,90,.04);
}

.pg-ui6-title {
    font-size: 15px;
    font-weight: 800;
    color: #17324d;
}

.pg-ui6-text {
    margin-top: 4px;
    font-size: 12px;
    line-height: 1.5;
    color: #62717d;
}

section[data-testid="stSidebar"] {
    border-right: 1px solid #dbe6ee;
}

section[data-testid="stSidebar"] .stRadio label {
    font-size: 13px;
}

@media (max-width: 700px) {
    section[data-testid="stSidebar"] .stRadio label { font-size: 14px; }

    div.stButton > button,
    div.stDownloadButton > button {
        min-height: 46px;
        width: 100%;
    }

    .pg-result-hero { padding: 15px; }

    .pg-result-main { align-items: flex-start; }

    .pg-result-main-message { font-size: 12px; }
}

div.stButton > button,
div.stDownloadButton > button {
    min-height: 44px;
    border-radius: 11px;
    font-weight: 750;
}

div[data-baseweb="input"] input,
div[data-baseweb="select"] > div,
textarea {
    border-radius: 10px !important;
}

textarea { min-height: 105px !important; }

.pg-result-main-label,
.pg-case-title,
.pg-stat-value,
.pg-case-value,
.pg-assessment-value,
.pg-signal-text,
.pg-action-text {
    overflow-wrap: anywhere;
}

div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

div[data-testid="stAlert"] { border-radius: 12px; }

hr {
    margin-top: 0.8rem;
    margin-bottom: 0.8rem;
}

.pg-ui6-footer {
    margin-top: 24px;
    padding: 11px 13px;
    border-radius: 11px;
    background: #f7fafc;
    border: 1px solid #e1e8ed;
    text-align: center;
    font-size: 11px;
    line-height: 1.45;
    color: #71808b;
}
</style>
""").strip(), unsafe_allow_html=True)


# =========================================================
# APP NAVIGATION / PROJECT INFO
# =========================================================

# =========================================================
# CLEAN PROFESSIONAL SIDEBAR NAVIGATION
# =========================================================

def _navigate_to(page):
    st.session_state["active_page"] = page


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

    try:
        safe_data = _json_safe(data)

        response = requests.post(
            GOOGLE_SHEET_URL,
            json=safe_data,
            timeout=15
        )

        ok = response.status_code in {200, 201}

        if return_details:
            return (
                ok,
                response.status_code,
                response.text[:500] if response.text else ""
            )

        return ok

    except Exception as exc:

        if return_details:
            return False, None, str(exc)[:500]

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

if "database_loaded" not in st.session_state:

    database_df = load_from_google_sheet()

    if not database_df.empty:

        st.session_state.adr_history = (
            database_df.to_dict("records")
        )

    st.session_state.database_loaded = True


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
        # Change only the application page state here.
        # navigation_page is a Streamlit widget key, so it must NOT be
        # modified after the radio widget has been created. On the next
        # rerun, the sidebar syncs navigation_page from active_page.
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
    # V20 — SAFETY INTELLIGENCE SUMMARY
    # =====================================================
    # Descriptive project-record summary only; not a clinical risk estimate.
    source_series = (
        df["Decision_Source"].astype(str).str.strip()
        if "Decision_Source" in df.columns
        else pd.Series(dtype=str)
    )

    safety_gate_cases = int(
        source_series.str.startswith("Safety Gate", na=False).sum()
    )
    rf_assisted_cases = int(
        (source_series == "Random Forest prototype").sum()
    )
    reassessment_cases = int(
        df["Reassessment_Of"].astype(str).str.strip().ne("").sum()
        if "Reassessment_Of" in df.columns
        else 0
    )
    linked_cases = int(
        df["Original_Case_Reference"].astype(str).str.strip().ne("").sum()
        if "Original_Case_Reference" in df.columns
        else 0
    )

    with st.expander("🛡️ Safety Intelligence", expanded=False):
        st.markdown("### 🛡️ PHARMAGUARD Safety Intelligence")
        st.caption(
            "Descriptive summary of how the prototype review architecture is represented in stored ADR records."
        )

        si1, si2, si3, si4 = st.columns(4)
        with si1:
            st.metric("🛡️ Safety Gate", safety_gate_cases)
        with si2:
            st.metric("🤖 RF-Assisted", rf_assisted_cases)
        with si3:
            st.metric("🔄 Reassessments", reassessment_cases)
        with si4:
            st.metric("🔗 Linked Cases", linked_cases)

        st.info(
            "The counts above use the stored Decision Source and reassessment fields. "
            "Historical Safety Gate-vs-Random Forest conflicts are not counted because the database does not store the separate RF output for every case. "
            "Use the live comparison panel on the Analysis Result screen to demonstrate Safety Gate precedence."
        )

    # =====================================================
    # V25 — QUALITY & AUDIT DASHBOARD
    # =====================================================
    # Descriptive prototype audit indicators only; not clinical performance metrics.
    qa_total = int(len(df))

    if qa_total > 0:
        qa_priority_known = int(
            df["Priority"].astype(str).str.upper().isin(
                ["HIGH", "MODERATE", "LOW"]
            ).sum()
            if "Priority" in df.columns else 0
        )
        qa_source_known = int(
            df["Decision_Source"].astype(str).str.strip().ne("").sum()
            if "Decision_Source" in df.columns else 0
        )
        qa_case_ref_known = int(
            df["Case_Reference"].astype(str).str.strip().ne("").sum()
            if "Case_Reference" in df.columns else 0
        )
        qa_adr_known = int(
            df["ADR"].astype(str).str.strip().ne("").sum()
            if "ADR" in df.columns else 0
        )
        qa_drug_known = int(
            df["Drug"].astype(str).str.strip().ne("").sum()
            if "Drug" in df.columns else 0
        )
    else:
        qa_priority_known = qa_source_known = qa_case_ref_known = 0
        qa_adr_known = qa_drug_known = 0

    qa_reassessment_linked = int(
        df["Reassessment_Of"].astype(str).str.strip().ne("").sum()
        if "Reassessment_Of" in df.columns else 0
    )
    qa_original_linked = int(
        df["Original_Case_Reference"].astype(str).str.strip().ne("").sum()
        if "Original_Case_Reference" in df.columns else 0
    )

    with st.expander("🧪 Quality & Audit", expanded=False):
        st.markdown("### 🧪 PHARMAGUARD Quality & Audit Dashboard")
        st.caption(
            "Descriptive audit indicators for the prototype records currently available in the app. "
            "These indicators do not represent clinical validation, model accuracy, or regulatory performance."
        )

        qa1, qa2, qa3, qa4 = st.columns(4)
        with qa1:
            st.metric("📋 Total Records", qa_total)
        with qa2:
            st.metric("🎯 Priority Recorded", qa_priority_known)
        with qa3:
            st.metric("🧭 Decision Source", qa_source_known)
        with qa4:
            st.metric("🔗 Reassessment Links", qa_reassessment_linked)

        qa5, qa6, qa7, qa8 = st.columns(4)
        with qa5:
            st.metric("🆔 Case References", qa_case_ref_known)
        with qa6:
            st.metric("⚠️ ADR Recorded", qa_adr_known)
        with qa7:
            st.metric("💊 Drug Recorded", qa_drug_known)
        with qa8:
            st.metric("🧬 Original Links", qa_original_linked)

        if qa_total:
            completeness = round(
                (qa_priority_known + qa_source_known + qa_case_ref_known + qa_adr_known + qa_drug_known)
                / (5 * qa_total) * 100,
                1
            )
            st.progress(
                min(completeness / 100, 1.0),
                text=f"Core record-field coverage: {completeness}%"
            )

        qa_audit = pd.DataFrame({
            "Audit Indicator": [
                "Priority recorded",
                "Decision source recorded",
                "Case reference recorded",
                "ADR recorded",
                "Drug recorded",
                "Reassessment-linked records"
            ],
            "Count": [
                qa_priority_known,
                qa_source_known,
                qa_case_ref_known,
                qa_adr_known,
                qa_drug_known,
                qa_reassessment_linked
            ]
        })

        st.dataframe(
            qa_audit,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            label="⬇️ Download Quality & Audit Summary",
            data=qa_audit.to_csv(index=False),
            file_name="PHARMAGUARD_Quality_Audit_Summary.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.info(
            "Audit indicators are intended to support prototype documentation and demonstration. "
            "They should not be interpreted as evidence of clinical validity or model performance."
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
    st.caption("Search, filter and review previously recorded ADR cases")

    df = pd.DataFrame(st.session_state.get("adr_history", []))

    if df.empty:
        st.markdown(
            textwrap.dedent("""
            <div class="pg-empty-state">
                <div class="pg-empty-icon">📚</div>
                <div class="pg-empty-title">No ADR cases available</div>
                <div class="pg-empty-text">Completed ADR analyses will appear here.</div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )
        return

    counts = _priority_counts(df)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Cases", len(df))
    with m2:
        st.metric("🔴 High", counts["HIGH"])
    with m3:
        st.metric("🟡 Moderate", counts["MODERATE"])
    with m4:
        st.metric("🟢 Low", counts["LOW"])

    st.markdown("### 🔎 Find a Case")
    c1, c2 = st.columns([2, 1])
    with c1:
        q = st.text_input(
            "Search cases",
            placeholder="Case ID, patient ID, drug, ADR or priority...",
            label_visibility="collapsed"
        ).strip().lower()
    with c2:
        priority_filter = st.selectbox(
            "Priority filter",
            ["All", "HIGH", "MODERATE", "LOW"],
            label_visibility="collapsed"
        )

    filtered = df.copy()
    if q:
        mask = pd.Series(False, index=filtered.index)
        for col in ["Case_Reference", "Patient_ID", "Drug", "ADR", "Priority"]:
            if col in filtered.columns:
                mask = mask | filtered[col].astype(str).str.lower().str.contains(
                    re.escape(q), na=False
                )
        filtered = filtered[mask]

    if priority_filter != "All" and "Priority" in filtered.columns:
        filtered = filtered[
            filtered["Priority"].astype(str).str.upper() == priority_filter
        ]

    st.caption(f"Showing {len(filtered)} of {len(df)} cases")

    display_cols = [c for c in [
        "Case_Reference", "Patient_ID", "Drug", "ADR",
        "Priority", "Seriousness", "Decision_Source", "Date_Time"
    ] if c in filtered.columns]

    if filtered.empty:
        st.info("No cases match the current search/filter.")
    else:
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
    st.markdown(
        textwrap.dedent("""
        <div class="pg-ui5-hero">
            <div class="pg-ui5-title">📄 ADR Case Reports</div>
            <div class="pg-ui5-sub">Review a saved ADR case and generate a professional report without changing the original database record.</div>
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
        "Select saved case",
        [x[1] for x in labels],
        help="Select the ADR case for report preview and export."
    )
    selected_idx = next(i for i, label in labels if label == selected_label)
    row = df.loc[selected_idx]

    priority = str(row.get("Priority", "UNKNOWN")).upper()
    seriousness = str(row.get("Seriousness", "Uncertain"))
    decision_source = str(row.get("Decision_Source", ""))
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
            <div class="pg-case-ref">{html.escape(str(row.get("Case_Reference", "")))}</div>
            <div class="pg-case-title">{html.escape(str(row.get("Drug", "Unknown")))} — ADR Review</div>
            <div style="margin-top:10px;">
                <span class="pg-priority {badge_class}">{html.escape(priority)} PRIORITY</span>
            </div>
            <div class="pg-case-grid">
                <div class="pg-case-field"><div class="pg-case-label">Patient / Project ID</div><div class="pg-case-value">{html.escape(str(row.get("Patient_ID", "")))}</div></div>
                <div class="pg-case-field"><div class="pg-case-label">Date & Time</div><div class="pg-case-value">{html.escape(str(row.get("Date_Time", "")))}</div></div>
                <div class="pg-case-field"><div class="pg-case-label">Age / Sex</div><div class="pg-case-value">{html.escape(str(row.get("Age", "")))} / {html.escape(str(row.get("Sex", "")))}</div></div>
                <div class="pg-case-field"><div class="pg-case-label">Seriousness</div><div class="pg-case-value">{html.escape(seriousness)}</div></div>
            </div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    st.markdown("### 💊 ADR Information")
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

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            textwrap.dedent(f"""
            <div class="pg-section-card">
                <h4>🔎 PHARMAGUARD Assessment</h4>
                <div><b>Priority:</b> {html.escape(priority)}</div>
                <div style="margin-top:7px;"><b>Seriousness:</b> {html.escape(seriousness)}</div>
                <div style="margin-top:7px;"><b>Decision Source:</b> {html.escape(decision_source)}</div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            textwrap.dedent(f"""
            <div class="pg-section-card">
                <h4>🧠 Why this priority?</h4>
                <div>{html.escape(reason) if reason else "No reason recorded."}</div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

    st.markdown(
        textwrap.dedent(f"""
        <div class="pg-section-card">
            <h4>📌 Recommended Action</h4>
            <div>{html.escape(recommendation)}</div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    # =====================================================
    # INNOVATION 2 — PHARMACIST REVIEW CHECKLIST
    # =====================================================
    st.markdown("### 🧑‍⚕️ Pharmacist Review Checklist")
    st.markdown(
        """
        <div class="pg-section-card">
            <h4>Structured review before pharmacovigilance follow-up</h4>
            <div>
                Use this checklist to document the key review steps for the selected ADR case.
                Checklist completion does not replace professional or regulatory assessment.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

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
    st.markdown("### 🔄 Dynamic ADR Risk Reassessment")
    st.markdown(
        """
        <div class="pg-section-card">
            <h4>Update the case when new clinical information becomes available</h4>
            <div>
                Reassessment creates a new linked case version rather than silently
                changing the original record. This preserves the review history.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("🔄 Reassess this ADR case", expanded=False):
        st.caption(
            "Example: an initial rash may later be followed by facial swelling or "
            "difficulty breathing. Enter the updated ADR information here."
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

                    new_case_reference = (
                        f"PHG-CASE-{datetime.now().strftime('%Y%m%d-%H%M%S')}-"
                        f"{uuid.uuid4().hex[:8].upper()}"
                    )

                    new_record = {
                        "Date_Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
                        f"**Previous:** {priority}  →  **Updated:** {new_priority}"
                    )
                    st.markdown(
                        f"**Decision Source:** {new_decision_source}"
                    )
                    st.markdown(
                        f"**Detected signal:** {new_reason}"
                    )
                    st.markdown(
                        f"**Recommended action:** {new_recommendation}"
                    )

                    saved, save_status, save_response = save_to_google_sheet(
                        new_record,
                        return_details=True
                    )

                    if saved:
                        try:
                            st.cache_data.clear()
                        except Exception:
                            pass

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

    # Linked reassessment timeline for the selected case.
    root_reference = str(
        row.get("Original_Case_Reference", "")
        or row.get("Case_Reference", "")
    )
    timeline_records = []
    for item in st.session_state.get("adr_history", []):
        item_root = str(
            item.get("Original_Case_Reference", "")
            or item.get("Case_Reference", "")
        )
        if item_root == root_reference:
            timeline_records.append(item)

    if timeline_records:
        timeline_records = sorted(
            timeline_records,
            key=lambda x: str(x.get("Date_Time", ""))
        )
        st.markdown("### 📈 ADR Priority Timeline")
        timeline_rows = []
        for item in timeline_records:
            timeline_rows.append({
                "Version": "Initial" if not item.get("Reassessment_Of") else f"Reassessment {item.get('Reassessment_Number', '')}",
                "Date & Time": item.get("Date_Time", ""),
                "Priority": item.get("Priority", "UNKNOWN"),
                "ADR / New Information": item.get("ADR", ""),
                "Case Reference": item.get("Case_Reference", ""),
            })
        st.dataframe(
            pd.DataFrame(timeline_rows),
            use_container_width=True,
            hide_index=True
        )

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

def render_database_screen():
    st.markdown("## ☁️ PHARMAGUARD Database")
    st.caption("Project database • Google Sheets integration • Loaded records")

    df = pd.DataFrame(st.session_state.get("adr_history", []))
    counts = _priority_counts(df)
    loaded = bool(st.session_state.get("database_loaded"))

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Records", len(df))
    with m2:
        st.metric("🔴 High", counts["HIGH"])
    with m3:
        st.metric("🟡 Moderate", counts["MODERATE"])
    with m4:
        st.metric("🟢 Low", counts["LOW"])

    status_text = "● DATABASE LOADED" if loaded else "○ DATABASE NOT LOADED"
    st.markdown(
        textwrap.dedent(f"""
        <div class="pg-db-status">
            <span>{html.escape(status_text)}</span>
            <span>Records currently available in the app: <b>{len(df)}</b></span>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    if df.empty:
        st.markdown(
            textwrap.dedent("""
            <div class="pg-empty-state">
                <div class="pg-empty-icon">☁️</div>
                <div class="pg-empty-title">Database is empty</div>
                <div class="pg-empty-text">Saved ADR cases will appear here after they are loaded into the app.</div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )
        return

    st.markdown("### 🔎 Database Search & Filter")
    c1, c2 = st.columns([2, 1])
    with c1:
        q = st.text_input(
            "Database search",
            placeholder="Search case ID, drug, ADR or patient ID...",
            label_visibility="collapsed"
        ).strip().lower()
    with c2:
        priority_filter = st.selectbox(
            "Database priority",
            ["All", "HIGH", "MODERATE", "LOW"],
            label_visibility="collapsed"
        )

    filtered = df.copy()
    if q:
        mask = pd.Series(False, index=filtered.index)
        for col in ["Case_Reference", "Patient_ID", "Drug", "ADR"]:
            if col in filtered.columns:
                mask = mask | filtered[col].astype(str).str.lower().str.contains(
                    re.escape(q), na=False
                )
        filtered = filtered[mask]

    if priority_filter != "All" and "Priority" in filtered.columns:
        filtered = filtered[
            filtered["Priority"].astype(str).str.upper() == priority_filter
        ]

    st.caption(f"Showing {len(filtered)} of {len(df)} database records")

    display_cols = [c for c in [
        "Case_Reference", "Patient_ID", "Age", "Sex", "Drug", "ADR",
        "Priority", "Seriousness", "Decision_Source", "Date_Time"
    ] if c in filtered.columns]

    st.dataframe(
        filtered[display_cols].sort_index(ascending=False),
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # V17: REASSESSMENT DETAILS
    # Keep the main database table compact, while exposing
    # longitudinal reassessment fields for the selected case.
    # -----------------------------------------------------
    reassessment_candidates = filtered[
        filtered["Case_Reference"].astype(str).str.strip() != ""
    ].copy() if "Case_Reference" in filtered.columns else pd.DataFrame()

    if not reassessment_candidates.empty:
        st.markdown("### 🔄 Reassessment Details")
        st.caption(
            "Select a case to view linked reassessment/version information. "
            "The main database table remains unchanged."
        )

        case_options = reassessment_candidates["Case_Reference"].astype(str).tolist()
        selected_case_ref = st.selectbox(
            "Select Case Reference",
            case_options,
            key="database_reassessment_case"
        )

        selected_rows = df[
            df["Case_Reference"].astype(str) == str(selected_case_ref)
        ] if "Case_Reference" in df.columns else pd.DataFrame()

        if not selected_rows.empty:
            selected_record = selected_rows.iloc[-1].to_dict()

            reassessment_of = str(selected_record.get("Reassessment_Of", "")).strip()
            original_ref = str(
                selected_record.get("Original_Case_Reference", "")
                or selected_record.get("Case_Reference", "")
            ).strip()
            reassessment_number = str(selected_record.get("Reassessment_Number", "")).strip()
            previous_priority = str(selected_record.get("Previous_Priority", "")).strip()
            follow_up_note = str(selected_record.get("Follow_Up_Note", "")).strip()

            is_reassessment = bool(reassessment_of)

            if is_reassessment:
                st.success(
                    f"🔄 This is Reassessment {reassessment_number or '—'}: "
                    f"{previous_priority or 'UNKNOWN'} → "
                    f"{selected_record.get('Priority', 'UNKNOWN')}"
                )
            else:
                st.info("🟢 This is the initial ADR case version.")

            d1, d2 = st.columns(2)
            with d1:
                st.markdown(f"**Previous Priority:** {previous_priority or '—'}")
                st.markdown(f"**Reassessment Of:** {reassessment_of or '—'}")
                st.markdown(f"**Reassessment Number:** {reassessment_number or 'Initial'}")
            with d2:
                st.markdown(f"**Original Case Reference:** {original_ref or '—'}")
                st.markdown(f"**Current Priority:** {selected_record.get('Priority', 'UNKNOWN')}")
                st.markdown(f"**Decision Source:** {selected_record.get('Decision_Source', '—')}")

            st.markdown("**Follow-up / New Clinical Information:**")
            if follow_up_note:
                st.info(follow_up_note)
            else:
                st.caption("No follow-up note recorded for this case version.")

            # Show the complete linked timeline from the loaded database.
            timeline_root = original_ref or str(selected_case_ref)
            linked = df.copy()
            if "Case_Reference" in linked.columns:
                linked_root = linked.get("Original_Case_Reference", pd.Series("", index=linked.index)).fillna("").astype(str).str.strip()
                linked_case = linked["Case_Reference"].astype(str).str.strip()
                timeline_mask = (linked_root == timeline_root) | (linked_case == timeline_root)
                timeline = linked[timeline_mask].copy()
            else:
                timeline = pd.DataFrame()

            if not timeline.empty:
                st.markdown("#### 📈 Linked ADR Priority Timeline")
                timeline_rows = []
                for _, item in timeline.sort_values("Date_Time" if "Date_Time" in timeline.columns else timeline.index).iterrows():
                    reassess_no = str(item.get("Reassessment_Number", "")).strip()
                    timeline_rows.append({
                        "Version": f"Reassessment {reassess_no}" if reassess_no else "Initial",
                        "Date & Time": item.get("Date_Time", ""),
                        "Priority": item.get("Priority", "UNKNOWN"),
                        "ADR / New Information": item.get("ADR", ""),
                        "Case Reference": item.get("Case_Reference", ""),
                    })
                st.dataframe(
                    pd.DataFrame(timeline_rows),
                    use_container_width=True,
                    hide_index=True
                )

    st.markdown("### 📤 Export Database")
    st.download_button(
        "⬇️ Download Database CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="PHARMAGUARD_Database.csv",
        mime="text/csv",
        use_container_width=True
    )

def render_cases_hub_screen():
    st.markdown(
        textwrap.dedent("""
        <div class="pg-ui5-hero">
            <div class="pg-ui5-title">📂 Cases</div>
            <div class="pg-ui5-sub">Find saved ADR cases, review case reports, reassess cases and track their timeline.</div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    tab_history, tab_report = st.tabs(["📋 Case History", "📄 Case Report"])
    with tab_history:
        render_history_screen()
    with tab_report:
        render_case_reports_screen()


def render_project_info_screen():
    st.markdown(
        textwrap.dedent("""
        <div class="pg-ui5-hero">
            <div class="pg-ui5-title">ℹ️ Project Info</div>
            <div class="pg-ui5-sub">Methodology, system status and scientific disclaimer.</div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    tab_method, tab_status = st.tabs(["🔬 Methodology", "⚙️ Status & Disclaimer"])
    with tab_method:
        render_about_screen()
    with tab_status:
        render_settings_screen()


def render_about_screen():
    st.markdown(
        textwrap.dedent("""
        <div class="pg-ui5-hero">
            <div class="pg-ui5-title">ℹ️ About PHARMAGUARD</div>
            <div class="pg-ui5-sub">Project methodology, workflow and scientific scope.</div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    st.markdown(
        textwrap.dedent("""
        <div class="pg-section-card">
            <h4>🛡️ AI-Assisted ADR Risk Prioritization System</h4>
            <div>PHARMAGUARD is a pharmacovigilance proof-of-concept designed to prioritize ADR reports for review using a predefined Safety Gate with Random Forest prototype assistance.</div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    st.markdown("### 🔬 How PHARMAGUARD Works")
    steps = [
        ("1", "ADR Report", "Enter the reported drug, patient/project information and ADR description."),
        ("2", "Input Validation", "The report is checked for required ADR information and selected terminology issues."),
        ("3", "Safety Gate", "Project-defined serious and moderate-review signals are screened before ML assistance."),
        ("4", "Random Forest", "When no predefined signal is detected, the embedded Random Forest provides prototype priority assistance."),
        ("5", "Final Review Priority", "PHARMAGUARD records HIGH, MODERATE, LOW or UNKNOWN according to the project workflow."),
        ("6", "Database & Reports", "The case can be stored, searched and exported for project review.")
    ]
    for n, title, desc in steps:
        st.markdown(
            f'<div class="pg-method-step"><b>{n}. {html.escape(title)}</b><br><span>{html.escape(desc)}</span></div>',
            unsafe_allow_html=True
        )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            textwrap.dedent("""
            <div class="pg-section-card">
                <h4>💊 What is an ADR?</h4>
                <div>An adverse drug reaction is a harmful or unintended response associated with the use of a medicinal product.</div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            textwrap.dedent("""
            <div class="pg-section-card">
                <h4>🧠 Random Forest</h4>
                <div>The embedded model provides prototype ML assistance. Its output is not a clinical probability or a validated regulatory classification.</div>
            </div>
            """).strip(),
            unsafe_allow_html=True
        )

    st.markdown(
        textwrap.dedent("""
        <div class="pg-section-card">
            <h4>🛡️ Safety Gate</h4>
            <div>The Safety Gate screens for project-defined serious and moderate-review signals and protects selected serious signals from being downgraded by the ML model.</div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    st.markdown("### ⚠️ Project Scope & Limitations")
    st.markdown(
        textwrap.dedent("""
        <div class="pg-disclaimer-box">
        PHARMAGUARD is a proof-of-concept project. Its HIGH/MODERATE/LOW outputs are project-defined review priorities. The prototype does not establish ADR causality, diagnosis, treatment, clinical validity, or regulatory seriousness, and it does not replace professional clinical judgment.
        </div>
        """).strip(),
        unsafe_allow_html=True
    )


def render_settings_screen():
    st.markdown(
        textwrap.dedent("""
        <div class="pg-ui5-hero">
            <div class="pg-ui5-title">⚙️ Settings & Scientific Disclaimer</div>
            <div class="pg-ui5-sub">Project status and important usage information.</div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    df = pd.DataFrame(st.session_state.get("adr_history", []))
    counts = _priority_counts(df)
    loaded = bool(st.session_state.get("database_loaded"))

    st.markdown("### 📊 Project Status")
    status_rows = [
        ("Application", "PHARMAGUARD"),
        ("Database", "Loaded" if loaded else "Not loaded"),
        ("Records available", str(len(df))),
        ("High priority", str(counts["HIGH"])),
        ("Moderate priority", str(counts["MODERATE"])),
        ("Low priority", str(counts["LOW"])),
        ("Review engine", "Safety Gate + Random Forest prototype")
    ]
    for label, value in status_rows:
        st.markdown(
            f'<div class="pg-setting-row"><div class="pg-setting-label">{html.escape(label)}</div><div class="pg-setting-value">{html.escape(value)}</div></div>',
            unsafe_allow_html=True
        )

    st.markdown("### ⚠️ Scientific Disclaimer")
    st.markdown(
        textwrap.dedent("""
        <div class="pg-disclaimer-box">
        <b>PHARMAGUARD is a pharmacovigilance proof-of-concept.</b><br><br>
        The system provides project-defined review-priority outputs intended to support pharmacovigilance workflow. These outputs do not establish ADR causality, diagnosis, treatment, regulatory seriousness, or clinical decision-making.<br><br>
        The Random Forest component is a prototype ML assistant and should not be interpreted as a calibrated clinical probability. Professional clinical and pharmacovigilance assessment remains necessary.
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    st.markdown("### 🔐 Data Note")
    st.info(
        "Use project identifiers rather than unnecessary personally identifiable information. "
        "The configured Google Sheets integration is used as the project database."
    )


# =========================================================
# SCREEN ROUTING
# =========================================================

active_page = st.session_state.get("active_page", "🏠 Dashboard")

if active_page == "🏠 Dashboard":
    render_dashboard_screen()
    st.stop()

if active_page == "📂 Cases":
    render_cases_hub_screen()
    st.stop()

if active_page == "☁️ Database":
    render_database_screen()
    st.stop()

if active_page == "ℹ️ Project Info":
    render_project_info_screen()
    st.stop()


# =========================================================
# NEW ADR ANALYSIS — UI-2
# =========================================================

st.markdown(
    textwrap.dedent("""
    <div class="pg-analysis-hero">
        <div class="pg-analysis-title">🔍 New ADR Analysis</div>
        <div class="pg-analysis-subtitle">Enter the ADR report details below. PHARMAGUARD will apply its predefined Safety Gate first and use the Random Forest prototype when appropriate.</div>
    </div>
    """).strip(),
    unsafe_allow_html=True
)

st.markdown(
    textwrap.dedent("""
    <div class="pg-stepbar">
        <div class="pg-step pg-step-active">1 · Report Details</div>
        <div class="pg-step">2 · Safety Gate</div>
        <div class="pg-step">3 · ML Assistance</div>
        <div class="pg-step">4 · Final Priority</div>
        <div class="pg-step">5 · Database</div>
    </div>
    """).strip(),
    unsafe_allow_html=True
)

# =========================================================
# PATIENT INPUT
# =========================================================

st.markdown(
    textwrap.dedent("""
    <div class="pg-form-card">
        <div class="pg-form-title">👤 Patient / Case Information</div>
        <div class="pg-form-subtitle">Basic report information used by the prioritization workflow.</div>
    </div>
    """).strip(),
    unsafe_allow_html=True
)

if "current_patient_id" not in st.session_state:
    st.session_state.current_patient_id = f"PHG-{uuid.uuid4().hex[:8].upper()}"

patient_id = st.text_input(
    "Patient / Project ID",
    value=st.session_state.current_patient_id,
    key="patient_id_input",
    help="A project identifier is generated automatically. Avoid unnecessary personally identifiable information."
)
st.session_state.current_patient_id = patient_id

st.markdown(
    textwrap.dedent(f"""
    <div class="pg-id-card">
        <div class="pg-id-label">Current case identifier</div>
        <div class="pg-id-value">{patient_id if patient_id else 'Not entered'}</div>
    </div>
    """).strip(),
    unsafe_allow_html=True
)

col_age, col_sex = st.columns(2)
with col_age:
    age = st.number_input(
        "Patient Age",
        min_value=0,
        max_value=120,
        value=30,
        step=1
    )

with col_sex:
    sex = st.selectbox(
        "Sex",
        ["M", "F", "Unknown"]
    )

# =========================================================
# DRUG INPUT
# =========================================================

st.markdown(
    textwrap.dedent("""
    <div class="pg-form-card">
        <div class="pg-form-title">💊 Drug Information</div>
        <div class="pg-form-subtitle">Enter the suspected or reported medicinal product.</div>
    </div>
    """).strip(),
    unsafe_allow_html=True
)

drug = st.text_input(
    "Drug Name",
    placeholder="Example: Amoxicillin"
)

# =========================================================
# ADR INPUT
# =========================================================

st.markdown(
    textwrap.dedent("""
    <div class="pg-form-card">
        <div class="pg-form-title">⚠️ Adverse Drug Reaction Report</div>
        <div class="pg-form-subtitle">Describe the reported reaction as clearly and specifically as possible.</div>
    </div>
    """).strip(),
    unsafe_allow_html=True
)

adr = st.text_area(
    "Adverse Drug Reaction (ADR)",
    placeholder="Example: Anaphylaxis with difficulty breathing",
    height=150,
    help="Describe the reported adverse event as clearly as possible."
)

st.markdown(
    textwrap.dedent("""
    <div class="pg-input-tip">💡 <b>Reporting tip:</b> Include clinically relevant details available in the report, such as the reported reaction, medical attention, hospitalization, outcome, or other important context.</div>
    """).strip(),
    unsafe_allow_html=True
)

# =========================================================
# ANALYZE ADR
# =========================================================

st.markdown(
    textwrap.dedent("""
    <div class="pg-analyze-box">
        <div class="pg-analyze-title">🛡️ PHARMAGUARD Review Engine</div>
        <div class="pg-analyze-subtitle">Safety Gate → Random Forest assistance → Final review priority → Database</div>
    </div>
    """).strip(),
    unsafe_allow_html=True
)

if st.button(
    "🔍 ANALYZE ADR REPORT",
    use_container_width=True,
    type="primary"
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

    # =====================================================
    # V22 — ADR INFORMATION COMPLETENESS CHECK
    # =====================================================
    information_gaps = assess_information_completeness(
        patient_id,
        age,
        sex,
        drug,
        adr,
    )

    if information_gaps:
        st.warning(
            "⚠️ Information Gap Detected — "
            "additional information may be needed before completing pharmacovigilance review."
        )
        st.markdown(
            "**Missing / unspecified core information:** "
            + ", ".join(information_gaps)
        )
        st.caption(
            "This alert does not change the Safety Gate or Random Forest priority. "
            "It is a reviewer-support information-quality check."
        )
    else:
        st.success(
            "✅ Core ADR information appears complete for this prototype review."
        )

    # -----------------------------------------------------
    # RUN THE SHARED SAFETY-FIRST PRIORITY ENGINE
    # -----------------------------------------------------

    (
        priority,
        flag,
        reason,
        recommendation,
        decision_source,
        serious_hits,
        moderate_hits,
    ) = evaluate_adr_priority(age, sex, drug, adr)

    # =====================================================
    # V19 — SAFETY GATE vs RANDOM FOREST LIVE COMPARISON
    # =====================================================
    rf_priority = model_predict(age, sex, drug, adr)
    if rf_priority not in {"LOW", "MODERATE", "HIGH"}:
        rf_priority = "UNKNOWN"

    safety_gate_priority = "NONE"
    safety_gate_signal = "No predefined Safety Gate signal detected."
    if serious_hits:
        safety_gate_priority = "HIGH"
        safety_gate_signal = "Serious signal: " + ", ".join(serious_hits)
    elif moderate_hits:
        safety_gate_priority = "MODERATE"
        safety_gate_signal = "Moderate-review signal: " + ", ".join(moderate_hits)

    st.markdown("### 🛡️ Safety Gate vs 🤖 Random Forest")
    st.markdown("This panel shows how the predefined Safety Gate and the Random Forest prototype responded to the same ADR report.")
    compare_c1, compare_c2 = st.columns(2)
    with compare_c1:
        st.markdown(f"**🛡️ Safety Gate**\n\n**Result:** {safety_gate_priority}\n\n**Signal:** {safety_gate_signal}")
    with compare_c2:
        st.markdown(f"**🤖 Random Forest Prototype**\n\n**Model output:** {rf_priority}\n\nPrototype ML assistance only; not a calibrated clinical probability.")

    if safety_gate_priority != "NONE" and rf_priority != safety_gate_priority:
        st.info(f"🛡️ Safety Gate precedence: Final PHARMAGUARD priority is **{priority}**. The prototype Random Forest output was **{rf_priority}**.")
    elif safety_gate_priority != "NONE":
        st.success(f"🛡️ Safety Gate detected a {safety_gate_priority} signal and the Random Forest output was also {rf_priority}.")
    else:
        st.info(f"No predefined Safety Gate signal was detected; final priority uses the Random Forest prototype: **{priority}**.")

    # =====================================================
    # DISPLAY RESULT — UI-3 PROFESSIONAL RESULT
    # =====================================================

    priority_meta = {
        "HIGH": {
            "icon": "🚨",
            "label": "HIGH PRIORITY",
            "main_class": "pg-result-high-main",
            "icon_class": "pg-result-high-icon",
            "message": "Immediate pharmacovigilance review recommended."
        },
        "MODERATE": {
            "icon": "⚠️",
            "label": "MODERATE PRIORITY",
            "main_class": "pg-result-moderate-main",
            "icon_class": "pg-result-moderate-icon",
            "message": "Clinical and pharmacovigilance review recommended."
        },
        "LOW": {
            "icon": "✅",
            "label": "LOW PRIORITY",
            "main_class": "pg-result-low-main",
            "icon_class": "pg-result-low-icon",
            "message": "Routine pharmacovigilance review."
        },
        "UNKNOWN": {
            "icon": "❓",
            "label": "PRIORITY UNCERTAIN",
            "main_class": "pg-result-unknown-main",
            "icon_class": "pg-result-unknown-icon",
            "message": "Additional information or professional review may be required."
        }
    }

    meta = priority_meta.get(priority, priority_meta["UNKNOWN"])

    safe_patient_id = html.escape(str(patient_id))
    safe_age = html.escape(str(age))
    safe_sex = html.escape(str(sex))
    safe_drug = html.escape(str(drug))
    safe_adr = html.escape(str(adr))
    safe_flag = html.escape(str(flag))
    safe_reason = html.escape(str(reason))
    safe_source = html.escape(str(decision_source))
    safe_recommendation = html.escape(str(recommendation))

    st.markdown(
        textwrap.dedent(
            f"""
            <div class="pg-result-hero {meta['main_class']}">
                <div class="pg-result-kicker">PHARMAGUARD • ANALYSIS COMPLETE</div>
                <div class="pg-result-main">
                    <div class="pg-result-main-icon {meta['icon_class']}">{meta['icon']}</div>
                    <div>
                        <div class="pg-result-main-label">{meta['label']}</div>
                        <div class="pg-result-main-message">{meta['message']}</div>
                    </div>
                </div>
            </div>

            <div class="pg-case-strip">
                <div class="pg-case-item">
                    <div class="pg-case-label">Patient / Case ID</div>
                    <div class="pg-case-value">{safe_patient_id}</div>
                </div>
                <div class="pg-case-item">
                    <div class="pg-case-label">Age</div>
                    <div class="pg-case-value">{safe_age}</div>
                </div>
                <div class="pg-case-item">
                    <div class="pg-case-label">Sex</div>
                    <div class="pg-case-value">{safe_sex}</div>
                </div>
            </div>

            <div class="pg-assessment-card">
                <div class="pg-assessment-title">⚕️ Review Assessment</div>
                <div class="pg-assessment-grid">
                    <div class="pg-assessment-item">
                        <div class="pg-assessment-label">Drug</div>
                        <div class="pg-assessment-value">{safe_drug}</div>
                    </div>
                    <div class="pg-assessment-item">
                        <div class="pg-assessment-label">Reported ADR</div>
                        <div class="pg-assessment-value">{safe_adr}</div>
                    </div>
                    <div class="pg-assessment-item">
                        <div class="pg-assessment-label">Seriousness / Review Flag</div>
                        <div class="pg-assessment-value">{safe_flag}</div>
                    </div>
                    <div class="pg-assessment-item">
                        <div class="pg-assessment-label">Decision Source</div>
                        <div class="pg-assessment-value">{safe_source}</div>
                    </div>
                </div>
            </div>

            <div class="pg-signal-card">
                <div class="pg-signal-title">🔎 Why this priority was assigned</div>
                <div class="pg-signal-text">{safe_reason}</div>
            </div>

            <div class="pg-action-card">
                <div class="pg-action-title">📌 Recommended Action</div>
                <div class="pg-action-text">{safe_recommendation}</div>
            </div>
            """
        ),
        unsafe_allow_html=True
    )

    st.markdown(
        textwrap.dedent(
            """
            <div class="pg-result-disclaimer">
                <b>Review-priority support only:</b> PHARMAGUARD is a proof-of-concept
                AI-assisted pharmacovigilance system. The displayed priority does not
                establish ADR causality, diagnosis, treatment, regulatory seriousness,
                or clinical decision-making.
            </div>
            """
        ),
        unsafe_allow_html=True
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

# =====================================================
# EXPLAINABLE DECISION SUMMARY — v24
# =====================================================
st.markdown("### 🧠 Explainable Decision Summary")

if selected_row is not None:
    _exp_priority = str(selected_row.get("Priority", "UNKNOWN")).upper()
    _exp_source = str(selected_row.get("Decision_Source", "Not available"))
    _exp_reason = str(selected_row.get("Reason", "Not available"))
    _exp_seriousness = str(selected_row.get("Seriousness", "Uncertain"))
    _exp_adr = str(selected_row.get("ADR", ""))

    if _exp_source == "Safety Gate — serious signal":
        _exp_path = "Safety Gate detected a predefined serious-signal pattern before ML assistance."
    elif _exp_source == "Safety Gate — moderate signal":
        _exp_path = "Safety Gate detected a project-defined moderate review signal before ML assistance."
    elif _exp_source == "Random Forest prototype":
        _exp_path = "No predefined Safety Gate signal was detected; the Random Forest prototype supplied the review priority."
    else:
        _exp_path = "Decision pathway information is limited for this record."

    st.info(
        "This explanation describes the PHARMAGUARD prototype decision pathway. "
        "It is not a clinical causality assessment or regulatory seriousness determination."
    )

    _explain_col1, _explain_col2 = st.columns(2)
    with _explain_col1:
        st.markdown("**🏁 Assigned Review Priority**")
        st.markdown(f"### {_exp_priority}")
        st.markdown(f"**⚕️ Seriousness:** {_exp_seriousness}")
    with _explain_col2:
        st.markdown("**🔎 Decision Source**")
        st.write(_exp_source)
        st.markdown("**🧭 Decision Pathway**")
        st.write(_exp_path)

    st.markdown("**⚠️ Reported ADR**")
    st.write(_exp_adr)

    st.markdown("**💡 Why was this priority assigned?**")
    st.write(_exp_reason)

    if _exp_source.startswith("Safety Gate"):
        st.success(
            "Safety Gate precedence applied: a predefined Safety Gate signal is not downgraded by the prototype Random Forest output."
        )
    elif _exp_source == "Random Forest prototype":
        st.warning(
            "This priority comes from the prototype Random Forest and should be interpreted as review-priority assistance, not a calibrated clinical probability."
        )
else:
    st.caption("Select a saved ADR case above to view its explainable decision summary.")

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
<div class="pg-ui6-footer">
🛡️ <b>PHARMAGUARD</b> • AI-Assisted ADR Risk Prioritization System<br>
Pharmacovigilance • Proof of Concept • Review-priority support only
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="pg-disclaimer">
<b>Scientific disclaimer:</b> PHARMAGUARD is a proof-of-concept AI-assisted pharmacovigilance review-prioritization system. Its HIGH/MODERATE/LOW outputs are project-defined review priorities and do not establish ADR causality, diagnosis, treatment, regulatory seriousness, or clinical decision-making.
</div>
""", unsafe_allow_html=True)
