# PHARMAGUARD Professional UI v32 — Dashboard Mobile Polish
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
   v32 — MOBILE-FIRST DASHBOARD GRID + RECENT CASE CARDS
   ========================================================= */
.pg-kpi-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; margin:4px 0 18px 0; }
.pg-kpi-grid-card { min-width:0; min-height:118px; padding:14px; border-radius:15px; background:var(--pg-surface,#fff); border:1px solid var(--pg-border,#dbe7ef); box-shadow:0 3px 12px rgba(30,60,90,.05); overflow:hidden; }
.pg-kpi-grid-icon { font-size:20px; line-height:1; }
.pg-kpi-grid-label { margin-top:8px; font-size:11px; font-weight:750; color:var(--pg-text,#657786); opacity:.78; }
.pg-kpi-grid-value { margin-top:2px; font-size:25px; line-height:1.15; font-weight:850; color:var(--pg-text,#102a43); }
.pg-kpi-grid-note { margin-top:5px; font-size:10px; line-height:1.3; color:var(--pg-text,#7b8794); opacity:.68; }
.pg-kpi-total { border-top:4px solid #7b8794; }
.pg-kpi-high { border-top:4px solid #d64545; }
.pg-kpi-moderate { border-top:4px solid #d49b00; }
.pg-kpi-low { border-top:4px solid #2f855a; }
.pg-recent-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; margin-top:4px; }
.pg-recent-card { min-width:0; padding:13px 14px; border-radius:14px; background:var(--pg-surface,#fff); border:1px solid var(--pg-border,#dbe7ef); box-shadow:0 2px 10px rgba(30,60,90,.04); overflow:hidden; }
.pg-recent-ref { font-size:11px; font-weight:800; color:var(--pg-text,#243b53); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.pg-recent-drug { margin-top:7px; font-size:13px; font-weight:750; color:var(--pg-text,#102a43); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.pg-recent-adr { margin-top:4px; min-height:18px; font-size:11px; line-height:1.35; color:var(--pg-text,#52606d); opacity:.78; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
.pg-recent-bottom { display:flex; align-items:center; justify-content:space-between; gap:8px; margin-top:10px; }
.pg-priority-badge { display:inline-flex; align-items:center; gap:3px; padding:4px 7px; border-radius:999px; font-size:10px; font-weight:800; white-space:nowrap; }
.pg-priority-high { background:rgba(214,69,69,.12); color:#a82f2f; }
.pg-priority-moderate { background:rgba(212,155,0,.14); color:#8b6700; }
.pg-priority-low { background:rgba(47,133,90,.13); color:#236b48; }
.pg-priority-unknown { background:rgba(123,135,148,.13); color:#65717d; }
.pg-recent-date { min-width:0; font-size:9px; color:var(--pg-text,#7b8794); opacity:.62; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
@media (max-width:700px) {
  .pg-kpi-grid { gap:9px; }
  .pg-kpi-grid-card { min-height:105px; padding:12px; }
  .pg-kpi-grid-value { font-size:23px; }
  .pg-recent-grid { grid-template-columns:1fr; gap:9px; }
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



/* v37 Professional ADR Priority Timeline */
.pg-timeline-summary{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:12px 0 16px}
.pg-timeline-stat{padding:13px 14px;border:1px solid #dbe5ec;border-radius:13px;background:#fff;box-shadow:0 2px 9px rgba(30,60,90,.035)}
.pg-timeline-stat-label{font-size:10px;font-weight:800;color:#71808b;text-transform:uppercase;letter-spacing:.55px}
.pg-timeline-stat-value{margin-top:4px;font-size:18px;font-weight:850;color:#17324d;word-break:break-word}
.pg-timeline-stat-note{margin-top:3px;font-size:10px;color:#7b8794}
.pg-timeline-track{margin:8px 0 4px;padding:2px 0}
.pg-timeline-item{position:relative;display:grid;grid-template-columns:28px minmax(0,1fr);gap:12px;padding:0 0 14px}
.pg-timeline-item:last-child{padding-bottom:0}
.pg-timeline-rail{position:relative;display:flex;justify-content:center}
.pg-timeline-rail:after{content:"";position:absolute;top:25px;bottom:-14px;width:2px;background:#d9e4eb}
.pg-timeline-item:last-child .pg-timeline-rail:after{display:none}
.pg-timeline-dot{position:relative;z-index:2;width:24px;height:24px;display:flex;align-items:center;justify-content:center;border-radius:50%;font-size:11px;font-weight:800;color:#fff;border:4px solid #fff;box-shadow:0 0 0 1px #d4e0e7}
.pg-timeline-dot-high{background:#d64545}.pg-timeline-dot-moderate{background:#d49b00}.pg-timeline-dot-low{background:#2f855a}.pg-timeline-dot-unknown{background:#7b8794}
.pg-timeline-card{min-width:0;padding:13px 14px;border:1px solid #dbe5ec;border-radius:14px;background:#fff;box-shadow:0 2px 10px rgba(30,60,90,.04)}
.pg-timeline-card-current{border-color:#bcd8e8;box-shadow:0 3px 13px rgba(43,111,159,.08)}
.pg-timeline-top{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap}
.pg-timeline-version{font-size:13px;font-weight:850;color:#17324d}
.pg-timeline-priority{display:inline-flex;padding:4px 8px;border-radius:999px;font-size:10px;font-weight:850}
.pg-timeline-priority-high{background:#fff0f0;color:#a61b1b;border:1px solid #f2c7c7}
.pg-timeline-priority-moderate{background:#fff7df;color:#8a5a00;border:1px solid #eed99b}
.pg-timeline-priority-low{background:#edf8f0;color:#246b37;border:1px solid #cce7d3}
.pg-timeline-priority-unknown{background:#f2f4f6;color:#59646e;border:1px solid #dce1e5}
.pg-timeline-date{margin-top:4px;font-size:10px;color:#7b8794}
.pg-timeline-section{margin-top:11px;padding-top:10px;border-top:1px solid #edf1f4}
.pg-timeline-label{font-size:9px;font-weight:850;color:#7a8793;text-transform:uppercase;letter-spacing:.65px}
.pg-timeline-value{margin-top:3px;font-size:12px;line-height:1.45;color:#334e68;overflow-wrap:anywhere}
.pg-timeline-current{display:inline-flex;margin-top:7px;padding:3px 7px;border-radius:999px;background:#eef7fc;color:#245a78;border:1px solid #d4e7f2;font-size:9px;font-weight:850}
.pg-timeline-change{margin:14px 0 4px;padding:12px 14px;border-radius:13px;background:#f4f9fc;border:1px solid #d6e6f1;color:#425466;font-size:12px;line-height:1.5}
.pg-timeline-change strong{color:#17324d}
@media(max-width:700px){.pg-timeline-summary{grid-template-columns:1fr 1fr}.pg-timeline-summary .pg-timeline-stat:first-child{grid-column:1/-1}.pg-timeline-item{grid-template-columns:25px minmax(0,1fr);gap:9px}.pg-timeline-card{padding:12px}}

/* Dynamic reassessment workspace polish */
.pg-expand-mini-summary{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:12px 0 14px}
.pg-expand-mini-summary>div{padding:11px 12px;border:1px solid rgba(128,128,128,.22);border-radius:10px;text-align:center}
.pg-expand-mini-summary strong{display:block;font-size:.92rem}
.pg-expand-mini-summary span{display:block;font-size:.72rem;opacity:.72;margin-top:3px;line-height:1.35}
.pg-reassess-result{padding:14px 16px;border:1px solid rgba(128,128,128,.22);border-radius:12px;margin:12px 0;line-height:1.65}
.pg-reassess-result-title{font-weight:800;margin-bottom:7px}
@media (max-width:640px){.pg-expand-mini-summary{grid-template-columns:1fr}.pg-expand-mini-summary>div{text-align:left}}
</style>
<style>
/* Case History expandable workspace */
.pg-expand-mini-summary{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:12px 0 14px}
.pg-expand-mini-summary>div{padding:11px 12px;border:1px solid rgba(128,128,128,.22);border-radius:10px;text-align:center}
.pg-expand-mini-summary strong{display:block;font-size:1rem}
.pg-expand-mini-summary span{display:block;font-size:.72rem;opacity:.72;margin-top:2px}
.pg-empty-state{padding:16px;border:1px dashed rgba(128,128,128,.35);border-radius:10px;text-align:center;margin:8px 0 4px;line-height:1.6}
@media (max-width:640px){.pg-expand-mini-summary{grid-template-columns:1fr 1fr}.pg-expand-mini-summary>div:last-child{grid-column:1/-1}}
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
   CASE REPORT — PROFESSIONAL REVIEW LAYOUT
   Presentation only; backend/scientific logic unchanged.
   ========================================================= */
.pg-report-hero {
    padding:18px;
    border-radius:18px;
    background:linear-gradient(135deg,#f5fbff,#ffffff);
    border:1px solid #d7e8f2;
    margin-bottom:14px;
}
.pg-report-kicker {
    font-size:10px; font-weight:850; letter-spacing:1.05px;
    text-transform:uppercase; color:#6b7d8b; margin-bottom:5px;
}
.pg-report-title { font-size:25px; font-weight:850; color:#102a43; line-height:1.15; }
.pg-report-sub { margin-top:5px; color:#687783; font-size:13px; line-height:1.5; }
.pg-report-overview {
    display:grid; grid-template-columns:1.5fr .7fr .7fr; gap:10px; margin:10px 0 16px;
}
.pg-report-stat { padding:12px 13px; border:1px solid #dbe5ec; border-radius:13px; background:#fff; }
.pg-report-stat-label { font-size:10px; font-weight:800; color:#71808b; text-transform:uppercase; letter-spacing:.5px; }
.pg-report-stat-value { margin-top:4px; font-size:14px; font-weight:800; word-break:break-word; }
.pg-report-section-title { margin:18px 0 7px; font-size:17px; font-weight:850; color:#243746; }
.pg-report-section-sub { color:#71808b; font-size:12px; margin:-2px 0 8px; line-height:1.4; }
.pg-report-decision { padding:15px; border-radius:15px; border:1px solid #dbe5ec; background:#fff; }
.pg-report-decision-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:9px; margin-top:10px; }
.pg-report-decision-item { padding:10px 11px; border-radius:10px; background:#f7fafc; border:1px solid #e5edf2; }
.pg-report-decision-label { font-size:10px; color:#71808b; font-weight:800; text-transform:uppercase; }
.pg-report-decision-value { margin-top:3px; font-size:13px; font-weight:750; word-break:break-word; }
.pg-report-why { padding:14px; border-radius:13px; background:#f8fbfd; border:1px solid #dbe8ef; line-height:1.55; }
.pg-report-action { padding:14px 15px; border-radius:13px; background:#eef8ff; border:1px solid #cfe6f5; line-height:1.5; }
@media (max-width:700px) {
    .pg-report-title{font-size:21px;}
    .pg-report-overview{grid-template-columns:1fr 1fr;}
    .pg-report-overview .pg-report-stat:first-child{grid-column:1/-1;}
    .pg-report-decision-grid{grid-template-columns:1fr;}
}

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
# V36 STABLE — STREAMLIT NATIVE DARK-MODE COMPATIBILITY
# Do not detect phone/OS theme. Streamlit controls the active theme.
# Only custom PHARMAGUARD surfaces are patched; backend/scientific logic is unchanged.
st.markdown("""
<style>
:root {
  --pg-bg: var(--background-color, #ffffff);
  --pg-surface: var(--secondary-background-color, #f7f9fb);
  --pg-text: var(--text-color, #1f2937);
  --pg-border: var(--border-color, #d9e2ea);
  --pg-primary: var(--primary-color, #2b6f9f);
}

/* Custom PHARMAGUARD surfaces */
.pg-header, .pg-dashboard-hero, .pg-hero, .pg-stat-card,
.pg-kpi-grid-card, .pg-recent-card, .pg-form-card, .pg-id-card,
.pg-analyze-box, .pg-result-hero, .pg-case-item, .pg-assessment-card,
.pg-signal-card, .pg-action-card, .pg-ui6-card, .pg-section-card,
.pg-case-card, .pg-dashboard-info, .pg-sidebar-note {
  background: var(--pg-surface) !important;
  border-color: var(--pg-border) !important;
  color: var(--pg-text) !important;
  box-shadow: none !important;
}

/* Text inside custom cards follows Streamlit's selected theme */
.pg-header *, .pg-dashboard-hero *, .pg-hero *, .pg-stat-card *,
.pg-kpi-grid-card *, .pg-recent-card *, .pg-form-card *, .pg-id-card *,
.pg-analyze-box *, .pg-result-hero *, .pg-case-item *, .pg-assessment-card *,
.pg-signal-card *, .pg-action-card *, .pg-ui6-card *, .pg-section-card *,
.pg-case-card *, .pg-dashboard-info *, .pg-sidebar-note * {
  color: var(--pg-text) !important;
}

/* Preserve semantic priority colors */
.pg-priority-high, .pg-priority-high *, .pg-high, .pg-high * { color: #d64545 !important; }
.pg-priority-moderate, .pg-priority-moderate *, .pg-moderate, .pg-moderate * { color: #d49b00 !important; }
.pg-priority-low, .pg-priority-low *, .pg-low, .pg-low * { color: #2f855a !important; }
.pg-priority-unknown, .pg-priority-unknown *, .pg-uncertain, .pg-uncertain * { color: #7b8794 !important; }

/* Native Streamlit controls remain theme-owned */
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea,
div[data-baseweb="select"] > div {
  color: var(--pg-text) !important;
  background: var(--pg-bg) !important;
  border-color: var(--pg-border) !important;
}

input::placeholder, textarea::placeholder {
  color: var(--pg-text) !important; opacity: .55 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: var(--pg-surface) !important;
  color: var(--pg-text) !important;
  border-color: var(--pg-border) !important;
}
section[data-testid="stSidebar"] div.stButton > button[kind="secondary"] {
  background: transparent !important;
  color: var(--pg-text) !important;
  border-color: transparent !important;
}
section[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {
  background: var(--pg-bg) !important;
  color: var(--pg-text) !important;
  border-color: var(--pg-border) !important;
}

/* Quick-action / ordinary buttons: readable in both Streamlit themes */
div.stButton > button[kind="secondary"] {
  background: var(--pg-surface) !important;
  color: var(--pg-text) !important;
  border-color: var(--pg-border) !important;
}
div.stButton > button[kind="secondary"]:hover,
div.stButton > button[kind="secondary"]:focus {
  background: var(--pg-bg) !important;
  color: var(--pg-text) !important;
  border-color: var(--pg-primary) !important;
}
div.stButton > button[kind="secondary"] * { color: inherit !important; }

/* Headings rendered by Streamlit */
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4 {
  color: var(--pg-text) !important;
}

/* No prefers-color-scheme: Streamlit theme is the single source of truth. */
</style>
""", unsafe_allow_html=True)

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
    "history",
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
                    "ADR Recorded", "Drug Recorded", "Reassessment Links", "Original Case Links",
                ],
                "Records": [
                    priority_recorded, decision_recorded, case_reference_recorded,
                    adr_recorded, drug_recorded, reassessment_links, original_links,
                ],
            }
        )
        st.dataframe(audit_df, use_container_width=True, hide_index=True)
        csv_bytes = audit_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Quality & Audit CSV",
            data=csv_bytes,
            file_name="PHARMAGUARD_Quality_Audit.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.caption("All analytics are descriptive prototype-record summaries. They do not represent clinical risk estimates, calibrated probabilities, model accuracy, or regulatory performance.")

def render_database_screen():
    """Professional, mobile-friendly database workspace. Presentation-only changes."""
    st.markdown(
        textwrap.dedent("""
        <div class="pg-db-hero">
            <div class="pg-db-hero-icon">☁️</div>
            <div>
                <div class="pg-db-hero-title">PHARMAGUARD Database</div>
                <div class="pg-db-hero-sub">Search, review and export saved ADR records from the project database.</div>
            </div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    df = pd.DataFrame(st.session_state.get("adr_history", []))
    counts = _priority_counts(df)
    loaded = bool(st.session_state.get("database_loaded"))

    # Compact database overview
    st.markdown(
        f'<div class="pg-db-summary">'
        f'<span><b>{len(df)}</b> records</span>'
        f'<span>🔴 {counts["HIGH"]} HIGH</span>'
        f'<span>🟡 {counts["MODERATE"]} MODERATE</span>'
        f'<span>🟢 {counts["LOW"]} LOW</span>'
        f'</div>',
        unsafe_allow_html=True
    )

    status_text = "DATABASE LOADED" if loaded else "DATABASE NOT LOADED"
    status_class = "pg-db-status-ok" if loaded else "pg-db-status-warn"
    st.markdown(
        textwrap.dedent(f"""
        <div class="pg-db-status {status_class}">
            <span>● {html.escape(status_text)}</span>
            <span>{len(df)} records available in this session</span>
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

    st.markdown("### 🔎 Find a Database Record")
    c1, c2 = st.columns([2, 1])
    with c1:
        q = st.text_input(
            "Database search",
            placeholder="Case ID, patient ID, drug or ADR...",
            label_visibility="collapsed",
            key="database_search_professional",
        ).strip().lower()
    with c2:
        priority_filter = st.selectbox(
            "Database priority",
            ["All", "HIGH", "MODERATE", "LOW"],
            label_visibility="collapsed",
            key="database_priority_professional",
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

    # -----------------------------------------------------
    # Recent database records — mobile-first cards
    # -----------------------------------------------------
    recent = filtered.copy()
    if "Date_Time" in recent.columns:
        recent["_sort_time"] = pd.to_datetime(recent["Date_Time"], errors="coerce")
        recent = recent.sort_values("_sort_time", ascending=False, na_position="last")
    else:
        recent = recent.sort_index(ascending=False)

    recent = recent.head(5)
    st.markdown("### 🗃️ Recent Database Records")

    if recent.empty:
        st.info("No database records match the current search or priority filter.")
    else:
        cards = []
        for _, item in recent.iterrows():
            ref = html.escape(str(item.get("Case_Reference", "Case")))
            drug = str(item.get("Drug", "") or "").strip()
            drug_display = html.escape(drug if drug else "Not reported")
            adr = html.escape(str(item.get("ADR", "") or "Not reported"))
            patient = html.escape(str(item.get("Patient_ID", "—")))
            date_time = html.escape(str(item.get("Date_Time", "—")))
            priority = str(item.get("Priority", "UNKNOWN") or "UNKNOWN").upper()
            pclass = {
                "HIGH": "pg-db-priority-high",
                "MODERATE": "pg-db-priority-moderate",
                "LOW": "pg-db-priority-low",
            }.get(priority, "pg-db-priority-unknown")
            source = html.escape(_display_decision_source(item))
            cards.append(
                f"""<div class="pg-db-card">
                    <div class="pg-db-card-top">
                        <div class="pg-db-ref">{ref}</div>
                        <span class="{pclass}">{html.escape(priority)}</span>
                    </div>
                    <div class="pg-db-drug">💊 {drug_display}</div>
                    <div class="pg-db-adr">{adr}</div>
                    <div class="pg-db-meta">
                        <span>👤 {patient}</span>
                        <span>🕒 {date_time}</span>
                    </div>
                    <div class="pg-db-source">Decision source: {source}</div>
                </div>"""
            )
        st.markdown("<div class='pg-db-card-list'>" + "".join(cards) + "</div>", unsafe_allow_html=True)

    if len(filtered) > 5:
        st.caption(
            f"Showing the {min(5, len(filtered))} most recent matching records above. "
            f"{len(filtered) - 5} additional records remain available in the table view."
        )

    # -----------------------------------------------------
    # Full database table — available on demand
    # -----------------------------------------------------
    with st.expander("🗂️ Full Table View", expanded=False):
        display_cols = [c for c in [
            "Case_Reference", "Patient_ID", "Age", "Sex", "Drug", "ADR",
            "Priority", "Seriousness", "Decision_Source", "Date_Time"
        ] if c in filtered.columns]
        table_df = filtered.copy()
        if "Date_Time" in table_df.columns:
            table_df["_sort_time"] = pd.to_datetime(table_df["Date_Time"], errors="coerce")
            table_df = table_df.sort_values("_sort_time", ascending=False, na_position="last").drop(columns=["_sort_time"])
        else:
            table_df = table_df.sort_index(ascending=False)
        st.dataframe(
            table_df[display_cols],
            use_container_width=True,
            hide_index=True,
        )

    # -----------------------------------------------------
    # Linked reassessment details — advanced workflow, collapsed
    # -----------------------------------------------------
    reassessment_candidates = filtered[
        filtered["Case_Reference"].astype(str).str.strip() != ""
    ].copy() if "Case_Reference" in filtered.columns else pd.DataFrame()

    if not reassessment_candidates.empty:
        with st.expander("🔄 Reassessment & Linked Timeline", expanded=False):
            st.caption(
                "Select a saved case version to review reassessment details and its linked ADR priority timeline."
            )
            case_options = reassessment_candidates["Case_Reference"].astype(str).tolist()
            selected_case_ref = st.selectbox(
                "Select Case Reference",
                case_options,
                key="database_reassessment_case_professional"
            )

            selected_rows = df[
                df["Case_Reference"].astype(str) == str(selected_case_ref)
            ] if "Case_Reference" in df.columns else pd.DataFrame()

            if not selected_rows.empty:
                selected_record = selected_rows.iloc[-1].to_dict()
                reassessment_of = str(selected_record.get("Reassessment_Of", "") or "").strip()
                original_ref = str(
                    selected_record.get("Original_Case_Reference", "")
                    or selected_record.get("Case_Reference", "")
                ).strip()
                reassessment_number = str(selected_record.get("Reassessment_Number", "") or "").strip()
                previous_priority = str(selected_record.get("Previous_Priority", "") or "").strip()
                follow_up_note = str(selected_record.get("Follow_Up_Note", "") or "").strip()
                is_reassessment = bool(reassessment_of)

                if is_reassessment:
                    st.success(
                        f"🔄 Reassessment {reassessment_number or '—'}: "
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
                    st.markdown(f"**Decision Source:** {_display_decision_source(selected_record)}")

                st.markdown("**Follow-up / New Clinical Information:**")
                if follow_up_note:
                    st.info(follow_up_note)
                else:
                    st.caption("No follow-up note recorded for this case version.")

                timeline_root = original_ref or str(selected_case_ref)
                linked = df.copy()
                if "Case_Reference" in linked.columns:
                    linked_root = linked.get(
                        "Original_Case_Reference",
                        pd.Series("", index=linked.index)
                    ).fillna("").astype(str).str.strip()
                    linked_case = linked["Case_Reference"].astype(str).str.strip()
                    timeline_mask = (linked_root == timeline_root) | (linked_case == timeline_root)
                    timeline = linked[timeline_mask].copy()
                else:
                    timeline = pd.DataFrame()

                if not timeline.empty:
                    st.markdown("#### 📈 Linked ADR Priority Timeline")
                    timeline_rows = []
                    for _, item in timeline.iterrows():
                        reassess_no = str(item.get("Reassessment_Number", "") or "").strip()
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
                        hide_index=True,
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
    """Central Cases workspace: history and professional case report review."""
    df=pd.DataFrame(st.session_state.get("adr_history",[])); counts=_priority_counts(df)
    st.markdown(textwrap.dedent("""
    <div class="pg-cases-hero"><div class="pg-cases-hero-icon">📂</div><div><div class="pg-cases-hero-title">Cases</div><div class="pg-cases-hero-sub">One workspace for saved ADR cases, detailed reports, reassessment and review workflow.</div></div></div>
    """).strip(),unsafe_allow_html=True)
    st.markdown(f'<div class="pg-cases-summary"><span><b>{len(df)}</b> saved cases</span><span>🔴 {counts["HIGH"]} HIGH</span><span>🟡 {counts["MODERATE"]} MODERATE</span><span>🟢 {counts["LOW"]} LOW</span></div>',unsafe_allow_html=True)
    tab_history,tab_report=st.tabs(["📋  Case History","📄  Case Report"])
    with tab_history: render_history_screen()
    with tab_report: render_case_reports_screen()

def render_project_info_screen():
    """Professional project/system workspace. Presentation-only changes."""
    st.markdown(
        textwrap.dedent("""
        <div class="pg-project-hero">
            <div class="pg-project-hero-icon">🛡️</div>
            <div>
                <div class="pg-project-hero-title">Project & System</div>
                <div class="pg-project-hero-sub">Understand PHARMAGUARD, review its methodology, and check important scientific usage information.</div>
            </div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

    tab_about, tab_status, tab_disclaimer = st.tabs([
        "ℹ️ About",
        "⚙️ Status",
        "⚠️ Disclaimer",
    ])

    with tab_about:
        render_about_screen()

    with tab_status:
        render_system_status_screen()

    with tab_disclaimer:
        render_scientific_disclaimer_screen()


def render_about_screen():
    st.markdown("### ℹ️ About PHARMAGUARD")
    st.caption("Project methodology, workflow and scientific scope.")

    st.markdown(
        textwrap.dedent("""
        <div class="pg-project-intro">
            <div class="pg-project-intro-title">🛡️ AI-Assisted ADR Risk Prioritization System</div>
            <div class="pg-project-intro-text">PHARMAGUARD is a pharmacovigilance proof-of-concept designed to prioritize ADR reports for review using a predefined Safety Gate with Random Forest prototype assistance.</div>
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
        ("6", "Database & Reports", "The case can be stored, searched and exported for project review."),
    ]
    for n, title, desc in steps:
        st.markdown(
            f'<div class="pg-method-step"><b>{html.escape(n)}. {html.escape(title)}</b><br><span>{html.escape(desc)}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("### 🧩 Core Components")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            textwrap.dedent("""
            <div class="pg-project-component">
                <div class="pg-project-component-title">💊 ADR</div>
                <div>An adverse drug reaction is a harmful or unintended response associated with the use of a medicinal product.</div>
            </div>
            """).strip(),
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            textwrap.dedent("""
            <div class="pg-project-component">
                <div class="pg-project-component-title">🧠 Random Forest</div>
                <div>The embedded model provides prototype ML assistance. Its output is not a clinical probability or a validated regulatory classification.</div>
            </div>
            """).strip(),
            unsafe_allow_html=True,
        )

    st.markdown(
        textwrap.dedent("""
        <div class="pg-project-component pg-project-safety">
            <div class="pg-project-component-title">🛡️ Safety Gate</div>
            <div>The Safety Gate screens for project-defined serious and moderate-review signals and protects selected serious signals from being downgraded by the ML model.</div>
        </div>
        """).strip(),
        unsafe_allow_html=True,
    )


def render_system_status_screen():
    df = pd.DataFrame(st.session_state.get("adr_history", []))
    counts = _priority_counts(df)
    loaded = bool(st.session_state.get("database_loaded"))

    st.markdown("### ⚙️ System Status")
    st.caption("Current project-state information available in this session.")

    status_rows = [
        ("Application", "PHARMAGUARD", "🛡️"),
        ("Database", "Loaded" if loaded else "Not loaded", "🟢" if loaded else "🟠"),
        ("Records available", str(len(df)), "📁"),
        ("High priority", str(counts["HIGH"]), "🔴"),
        ("Moderate priority", str(counts["MODERATE"]), "🟡"),
        ("Low priority", str(counts["LOW"]), "🟢"),
        ("Review engine", "Safety Gate + Random Forest prototype", "⚙️"),
    ]
    for label, value, icon in status_rows:
        st.markdown(
            f'<div class="pg-status-row"><div class="pg-status-icon">{icon}</div><div class="pg-status-main"><div class="pg-status-label">{html.escape(label)}</div><div class="pg-status-value">{html.escape(value)}</div></div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("### 📊 Priority Snapshot")
    st.markdown(
        f'<div class="pg-status-summary"><span><b>{counts["HIGH"]}</b><small>HIGH</small></span><span><b>{counts["MODERATE"]}</b><small>MODERATE</small></span><span><b>{counts["LOW"]}</b><small>LOW</small></span><span><b>{len(df)}</b><small>TOTAL</small></span></div>',
        unsafe_allow_html=True,
    )


def render_scientific_disclaimer_screen():
    st.markdown("### ⚠️ Scientific Disclaimer")
    st.caption("Important scope and appropriate-use information for the PHARMAGUARD prototype.")

    st.markdown(
        textwrap.dedent("""
        <div class="pg-scientific-card">
            <div class="pg-scientific-title">PHARMAGUARD is a pharmacovigilance proof-of-concept.</div>
            <div class="pg-scientific-text">The system provides project-defined review-priority outputs intended to support pharmacovigilance workflow. These outputs do not establish ADR causality, diagnosis, treatment, regulatory seriousness, or clinical decision-making.</div>
            <div class="pg-scientific-text">The Random Forest component is a prototype ML assistant and should not be interpreted as a calibrated clinical probability. Professional clinical and pharmacovigilance assessment remains necessary.</div>
        </div>
        """).strip(),
        unsafe_allow_html=True,
    )

    st.markdown("### 🔐 Data Note")
    st.info(
        "Use project identifiers rather than unnecessary personally identifiable information. "
        "The configured Google Sheets integration is used as the project database."
    )

    st.markdown(
        textwrap.dedent("""
        <div class="pg-scope-note">
            <b>Project scope:</b> PHARMAGUARD supports review prioritization. It is not a clinical diagnostic tool, causality assessment system, or replacement for professional judgment.
        </div>
        """).strip(),
        unsafe_allow_html=True,
    )


def render_settings_screen():
    """Backward-compatible wrapper for existing internal references."""
    render_system_status_screen()
    st.markdown("### ⚠️ Scientific Disclaimer")
    render_scientific_disclaimer_screen()


# =========================================================


st.markdown("""
<style>
/* =========================================================
   UI-10 — PROFESSIONAL DATABASE WORKSPACE
   Presentation-only: backend/database logic preserved.
   ========================================================= */
.pg-db-hero{display:flex;align-items:center;gap:13px;padding:17px 18px;margin:4px 0 10px;border-radius:18px;background:linear-gradient(135deg,#f3f9fd 0%,#fff 82%);border:1px solid #d7e7f0;box-shadow:0 4px 16px rgba(30,60,90,.04)}
.pg-db-hero-icon{width:43px;height:43px;display:flex;align-items:center;justify-content:center;border-radius:13px;background:#eaf4fb;font-size:22px;border:1px solid #d3e6f1}.pg-db-hero-title{font-size:24px;font-weight:850;color:#102a43;letter-spacing:-.15px}.pg-db-hero-sub{font-size:11px;color:#687887;line-height:1.5;margin-top:2px}
.pg-db-summary{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 8px;padding:8px 10px;border-radius:11px;background:#f8fbfd;border:1px solid #e0ebf2;color:#61717e;font-size:10px}.pg-db-summary span{padding:3px 7px;border-radius:999px;background:#fff;border:1px solid #e3ebf0}
.pg-db-status{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;padding:9px 11px;margin:0 0 15px;border-radius:10px;font-size:10px}.pg-db-status-ok{background:#f1faf4;border:1px solid #cfe8d6;color:#2b6d3c}.pg-db-status-warn{background:#fff8e8;border:1px solid #eedca7;color:#7c5a00}
.pg-db-card-list{display:flex;flex-direction:column;gap:8px;margin:4px 0 7px}.pg-db-card{padding:12px 13px;border-radius:13px;background:#fff;border:1px solid #dfe8ee;box-shadow:0 2px 9px rgba(30,60,90,.03)}.pg-db-card-top{display:flex;align-items:center;justify-content:space-between;gap:8px}.pg-db-ref{font-size:10px;font-weight:850;color:#526474;word-break:break-all}.pg-db-drug{font-size:14px;font-weight:800;color:#243b53;margin-top:6px}.pg-db-adr{font-size:11px;line-height:1.45;color:#667785;margin-top:3px}.pg-db-meta{display:flex;flex-wrap:wrap;gap:9px;margin-top:8px;padding-top:7px;border-top:1px solid #edf1f4;font-size:9px;color:#82909b}.pg-db-source{margin-top:7px;font-size:9px;color:#647887}
.pg-db-priority-high,.pg-db-priority-moderate,.pg-db-priority-low,.pg-db-priority-unknown{display:inline-block;padding:4px 8px;border-radius:999px;font-size:9px;font-weight:850;white-space:nowrap}.pg-db-priority-high{background:#fff0f0;color:#a61b1b;border:1px solid #f2c7c7}.pg-db-priority-moderate{background:#fff7df;color:#8a5a00;border:1px solid #eed99b}.pg-db-priority-low{background:#edf8f0;color:#246b37;border:1px solid #cce7d3}.pg-db-priority-unknown{background:#f2f4f6;color:#59646e;border:1px solid #dce1e5}
@media(max-width:700px){.pg-db-hero{padding:14px}.pg-db-hero-title{font-size:21px}.pg-db-hero-icon{width:39px;height:39px;font-size:20px}.pg-db-summary{gap:4px}.pg-db-status{display:block}.pg-db-status span{display:block}.pg-db-status span+span{margin-top:3px}.pg-db-card{padding:11px 12px}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* =========================================================
   UI-9 — PROFESSIONAL CASES WORKSPACE
   Presentation-only: no scoring, database or review logic changed.
   ========================================================= */
.pg-cases-hero{display:flex;align-items:center;gap:13px;padding:18px 19px;margin:4px 0 10px;border-radius:18px;background:linear-gradient(135deg,#f3f9fd 0%,#fff 82%);border:1px solid #d7e7f0;box-shadow:0 4px 16px rgba(30,60,90,.04)}
.pg-cases-hero-icon{width:45px;height:45px;display:flex;align-items:center;justify-content:center;border-radius:13px;background:#eaf4fb;font-size:23px;border:1px solid #d3e6f1}
.pg-cases-hero-title{font-size:26px;font-weight:850;color:#102a43;letter-spacing:-.2px}.pg-cases-hero-sub{font-size:12px;color:#687887;line-height:1.5;margin-top:2px}
.pg-cases-summary{display:flex;flex-wrap:wrap;gap:7px;margin:0 0 15px;padding:9px 11px;border-radius:11px;background:#f8fbfd;border:1px solid #e0ebf2;color:#61717e;font-size:10px}.pg-cases-summary span{padding:3px 7px;border-radius:999px;background:#fff;border:1px solid #e3ebf0}
.pg-cases-section-head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:2px 0 12px}.pg-cases-section-title{font-size:18px;font-weight:850;color:#243b53}.pg-cases-section-sub{font-size:11px;color:#7a8793;margin-top:2px}.pg-cases-section-chip{padding:5px 9px;border-radius:999px;background:#edf6fb;border:1px solid #d4e7f1;color:#38627e;font-size:9px;font-weight:800;white-space:nowrap}
.pg-case-kpi-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin:0 0 15px}.pg-case-kpi{padding:11px 10px;border-radius:12px;background:#fff;border:1px solid #dfe8ee;box-shadow:0 2px 8px rgba(30,60,90,.025)}.pg-case-kpi-icon{font-size:14px}.pg-case-kpi-label{font-size:9px;font-weight:800;color:#748290;text-transform:uppercase;letter-spacing:.45px;margin-top:2px}.pg-case-kpi-value{font-size:22px;font-weight:850;color:#17324d;line-height:1.05;margin-top:4px}.pg-case-kpi-note{font-size:9px;color:#8a96a0;margin-top:3px}.pg-case-kpi-high{border-left:3px solid #d94b4b}.pg-case-kpi-moderate{border-left:3px solid #d5a31a}.pg-case-kpi-low{border-left:3px solid #4c9a64}.pg-case-kpi-total{border-left:3px solid #5f89a6}
.pg-case-history-list{display:flex;flex-direction:column;gap:8px;margin:4px 0 10px}.pg-case-history-card{padding:12px 13px;border-radius:13px;background:#fff;border:1px solid #dfe8ee;box-shadow:0 2px 9px rgba(30,60,90,.03)}.pg-case-history-top{display:flex;align-items:center;justify-content:space-between;gap:8px}.pg-case-history-ref{font-size:11px;font-weight:850;color:#526474;word-break:break-all}.pg-case-history-drug{font-size:14px;font-weight:800;color:#243b53;margin-top:6px}.pg-case-history-adr{font-size:11px;line-height:1.45;color:#667785;margin-top:3px}.pg-case-history-meta{display:flex;flex-wrap:wrap;gap:10px;margin-top:8px;padding-top:7px;border-top:1px solid #edf1f4;font-size:9px;color:#82909b}
.pg-case-priority-high,.pg-case-priority-moderate,.pg-case-priority-low,.pg-case-priority-unknown{display:inline-block;padding:4px 8px;border-radius:999px;font-size:9px;font-weight:850;white-space:nowrap}.pg-case-priority-high{background:#fff0f0;color:#a61b1b;border:1px solid #f2c7c7}.pg-case-priority-moderate{background:#fff7df;color:#8a5a00;border:1px solid #eed99b}.pg-case-priority-low{background:#edf8f0;color:#246b37;border:1px solid #cce7d3}.pg-case-priority-unknown{background:#f2f4f6;color:#59646e;border:1px solid #dce1e5}
@media(max-width:700px){.pg-cases-hero{padding:15px 14px}.pg-cases-hero-title{font-size:22px}.pg-cases-hero-icon{width:40px;height:40px;font-size:20px}.pg-cases-summary{gap:5px}.pg-case-kpi-grid{grid-template-columns:1fr 1fr;gap:7px}.pg-case-kpi{padding:10px 9px}.pg-case-kpi-value{font-size:20px}.pg-cases-section-head{align-items:flex-start}.pg-cases-section-chip{margin-top:2px}}
</style>
""", unsafe_allow_html=True)

# UI-8 — PROFESSIONAL NEW ADR ANALYSIS POLISH
# Stable v36 backend/logic preserved.
# =========================================================
st.markdown("""
<style>
.pg-analysis-hero{position:relative;overflow:hidden;padding:22px 22px 20px;margin:4px 0 14px;border-radius:20px;background:linear-gradient(135deg,#eef7ff 0%,#fff 78%);border:1px solid #d5e6f2;box-shadow:0 5px 20px rgba(30,60,90,.06)}
.pg-analysis-hero:before{content:"🛡️";position:absolute;right:18px;top:13px;font-size:42px;opacity:.10}
.pg-analysis-title{font-size:27px;font-weight:850;color:#102a43;letter-spacing:-.2px;margin-bottom:5px}
.pg-analysis-subtitle{max-width:760px;color:#5d6d7c;font-size:13px;line-height:1.55}
.pg-stepbar{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:7px;margin:0 0 18px}
.pg-step{min-width:0;padding:9px 7px;border-radius:10px;background:#f7fafc;border:1px solid #dce7ee;color:#71808b;font-size:10px;font-weight:750;text-align:center}
.pg-step-active{background:#eaf4fb;border-color:#9fc5de;color:#174a6b;box-shadow:inset 0 -2px 0 #2b6f9f}
.pg-form-card{position:relative;padding:15px 16px 11px;margin:0 0 8px;border-radius:14px 14px 8px 8px;background:#fff;border:1px solid #dbe7ef;border-bottom:3px solid #e7f0f5;box-shadow:0 2px 10px rgba(30,60,90,.035)}
.pg-form-title{font-size:15px;font-weight:850;color:#243b53;letter-spacing:.05px}
.pg-form-subtitle{font-size:11px;color:#7a8793;margin-top:3px;margin-bottom:2px}
.pg-id-card{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 13px;margin:0 0 13px;border-radius:10px;background:#f5f9fc;border:1px solid #d9e8f2}
.pg-id-label{font-size:10px;font-weight:800;color:#70808d;text-transform:uppercase;letter-spacing:.6px}
.pg-id-value{margin-top:0;font-size:13px;font-weight:850;color:#17324d;word-break:break-word}
.pg-input-tip{padding:10px 12px;margin:8px 0 2px;border-radius:10px;background:#f7fbfd;border:1px solid #dceaf2;color:#607080;font-size:11px;line-height:1.5}
.pg-analyze-box{padding:15px 16px;margin:16px 0 8px;border-radius:15px;background:linear-gradient(135deg,#f2f8fc 0%,#fff 100%);border:1px solid #d6e6f0}
.pg-analyze-title{font-size:15px;font-weight:850;color:#17324d}.pg-analyze-subtitle{font-size:11px;color:#718096;margin-top:3px}
div[data-testid="stTextInput"],div[data-testid="stNumberInput"],div[data-testid="stSelectbox"],div[data-testid="stTextArea"]{margin-bottom:7px}
div[data-testid="stTextArea"] textarea{min-height:135px!important}
div.stButton>button[kind="primary"]{min-height:50px;border-radius:12px;font-size:14px;font-weight:850;letter-spacing:.25px}
@media(max-width:700px){.pg-analysis-hero{padding:17px 15px}.pg-analysis-title{font-size:22px}.pg-analysis-hero:before{font-size:32px;right:12px}.pg-stepbar{grid-template-columns:1fr 1fr;gap:6px}.pg-step:first-child{grid-column:1/-1}.pg-id-card{display:block}.pg-id-value{margin-top:4px}.pg-form-card{padding:13px 13px 9px}}
</style>
""", unsafe_allow_html=True)

# =========================================================
# =========================================================
# CASE REPORT COLLAPSED WORKFLOW POLISH
# Presentation-only: keep advanced review tools compact on mobile.
# =========================================================
st.markdown(
    """
    <style>
    div[data-testid="stExpander"] { margin-bottom: 0.55rem; }
    div[data-testid="stExpander"] summary { font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True
)



st.markdown("""
<style>
/* =========================================================
   UI-11 — PROFESSIONAL PROJECT & SYSTEM WORKSPACE
   Presentation-only: methodology/status/disclaimer logic preserved.
   ========================================================= */
.pg-project-hero{display:flex;align-items:center;gap:13px;padding:18px 18px;margin:4px 0 14px;border-radius:18px;background:linear-gradient(135deg,#f3f9fd 0%,#fff 82%);border:1px solid #d7e7f0;box-shadow:0 4px 16px rgba(30,60,90,.04)}
.pg-project-hero-icon{width:45px;height:45px;display:flex;align-items:center;justify-content:center;border-radius:13px;background:#eaf4fb;border:1px solid #d3e6f1;font-size:23px}.pg-project-hero-title{font-size:25px;font-weight:850;color:#102a43;letter-spacing:-.2px}.pg-project-hero-sub{font-size:11px;color:#687887;line-height:1.5;margin-top:2px}
.pg-project-intro{padding:15px 16px;margin:0 0 15px;border-radius:14px;background:#f7fbfd;border:1px solid #dceaf2;border-left:4px solid #5d9ac0}.pg-project-intro-title{font-size:15px;font-weight:850;color:#243b53}.pg-project-intro-text{font-size:11px;line-height:1.55;color:#667785;margin-top:5px}
.pg-project-component{padding:13px 14px;margin:0 0 9px;border-radius:13px;background:#fff;border:1px solid #dfe8ee;box-shadow:0 2px 9px rgba(30,60,90,.025);font-size:11px;line-height:1.5;color:#667785}.pg-project-component-title{font-size:14px;font-weight:850;color:#243b53;margin-bottom:3px}.pg-project-safety{margin-top:2px;border-left:4px solid #5d9ac0}
.pg-status-row{display:flex;align-items:center;gap:11px;padding:11px 12px;margin:0 0 7px;border-radius:12px;background:#fff;border:1px solid #dfe8ee}.pg-status-icon{width:28px;text-align:center;font-size:15px}.pg-status-main{min-width:0}.pg-status-label{font-size:9px;font-weight:800;color:#7a8793;text-transform:uppercase;letter-spacing:.45px}.pg-status-value{font-size:12px;font-weight:750;color:#243b53;margin-top:2px;word-break:break-word}
.pg-status-summary{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;margin-top:3px}.pg-status-summary span{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:10px 7px;border-radius:11px;background:#f8fbfd;border:1px solid #dfe8ee}.pg-status-summary b{font-size:19px;color:#17324d}.pg-status-summary small{font-size:8px;font-weight:800;color:#7a8793;letter-spacing:.4px;margin-top:2px}
.pg-scientific-card{padding:16px;margin:0 0 13px;border-radius:14px;background:#fffaf0;border:1px solid #eedda9;border-left:4px solid #d3a52c}.pg-scientific-title{font-size:14px;font-weight:850;color:#604c00}.pg-scientific-text{font-size:11px;line-height:1.55;color:#6e6240;margin-top:7px}.pg-scope-note{padding:11px 12px;border-radius:11px;background:#f7fbfd;border:1px solid #dceaf2;color:#607080;font-size:10px;line-height:1.5}
@media(max-width:700px){.pg-project-hero{padding:15px 14px}.pg-project-hero-title{font-size:22px}.pg-project-hero-icon{width:40px;height:40px;font-size:20px}.pg-status-summary{grid-template-columns:1fr 1fr}.pg-status-row{padding:10px 11px}}
</style>
""", unsafe_allow_html=True)


st.markdown("""<style>
/* =========================================================
   UI-11 — PROFESSIONAL EXPANDABLE WORKSPACES
   Presentation-only. Backend, calculations and navigation unchanged.
   ========================================================= */
.pg-expand-workspace-intro{
    padding:11px 13px;
    margin:2px 0 13px 0;
    border-radius:12px;
    background:linear-gradient(135deg,#f7fbfe 0%,#ffffff 100%);
    border:1px solid #dce8ef;
}
.pg-expand-workspace-title{
    font-size:14px;
    font-weight:850;
    color:#243b53;
    line-height:1.35;
}
.pg-expand-workspace-sub{
    margin-top:3px;
    font-size:11px;
    color:#71808b;
    line-height:1.45;
}
/* Native accordion shell */
div[data-testid="stExpander"]{
    border:1px solid #d9e5ec !important;
    border-radius:14px !important;
    background:#ffffff !important;
    box-shadow:0 2px 10px rgba(30,60,90,.035) !important;
    margin:9px 0 12px 0 !important;
    overflow:hidden !important;
}
div[data-testid="stExpander"] summary{
    padding:13px 15px !important;
    background:#f8fbfd !important;
    border-bottom:1px solid #e4edf2 !important;
    font-weight:800 !important;
    color:#243b53 !important;
}
div[data-testid="stExpander"] summary:hover{background:#f2f8fb !important;}
div[data-testid="stExpander"] > details > div{
    padding:14px 15px 16px 15px !important;
    background:#ffffff !important;
}
div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p{
    line-height:1.5;
}
div[data-testid="stExpander"] div[data-testid="stDataFrame"]{
    border:1px solid #e0e8ee;
    border-radius:10px;
    margin-top:8px;
}
div[data-testid="stExpander"] div[data-testid="stAlert"]{margin:9px 0 !important;}
div[data-testid="stExpander"] hr{margin:12px 0 !important;}
div[data-testid="stExpander"] label{font-weight:650 !important;}
div[data-testid="stExpander"] textarea{border-radius:10px !important;}
.pg-expand-status{
    display:inline-flex;
    align-items:center;
    gap:5px;
    padding:4px 8px;
    border-radius:999px;
    background:#eef6fa;
    border:1px solid #d8e8f0;
    color:#486581;
    font-size:10px;
    font-weight:800;
    margin-top:7px;
}
@media(max-width:700px){
    div[data-testid="stExpander"] summary{padding:12px 12px !important;}
    div[data-testid="stExpander"] > details > div{padding:12px 12px 14px !important;}
    .pg-expand-workspace-intro{padding:10px 11px;}
    .pg-expand-workspace-title{font-size:13px;}
}
</style>
</style>""", unsafe_allow_html=True)

# SCREEN ROUTING
# =========================================================

active_page = st.session_state.get("active_page", "🏠 Dashboard")

if active_page == "🏠 Dashboard":
    render_dashboard_screen()
    st.stop()

if active_page == "📂 Cases":
    render_cases_hub_screen()
    st.stop()

if active_page == "📊 Analytics":
    render_analytics_screen()
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
        <div class="pg-analysis-subtitle">Create a structured ADR report. PHARMAGUARD checks the predefined Safety Gate first, then uses the Random Forest prototype when appropriate.</div>
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
        <div class="pg-form-subtitle">Start with the minimum patient and case information needed for review prioritization.</div>
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
        <div class="pg-form-subtitle">Record the suspected or reported medicinal product associated with the ADR.</div>
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
        <div class="pg-form-subtitle">Describe the reported reaction using the clearest clinical information available.</div>
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
        <div class="pg-analyze-subtitle">Safety Gate  →  ML assistance  →  Final priority  →  Database</div>
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

    # Uncertainty context: retain conservative final priority for possible serious
    # symptoms, but explicitly mark the Safety Gate interpretation for human review.
    uncertainty_context = bool(re.search(
        r"\b(possible|possibly|suspected|疑|unclear|uncertain|uncertainty|unknown whether|not clear whether|cannot determine whether|could be|may be)\b",
        str(adr).lower()
    ))
    current_status_unclear = bool(re.search(
        r"(unclear whether|uncertain whether|unknown whether|not clear whether|cannot determine whether|whether the patient is currently|current status is unclear)",
        str(adr).lower()
    ))

    safety_gate_priority = "NONE"
    safety_gate_signal = "No predefined Safety Gate signal detected."
    if serious_hits and uncertainty_context and current_status_unclear:
        safety_gate_priority = "NEEDS REVIEW"
        safety_gate_signal = (
            "Potential serious signal with unclear current status: "
            + ", ".join(serious_hits)
        )
    elif serious_hits:
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

    if safety_gate_priority == "NEEDS REVIEW":
        st.warning(
            f"⚠️ Uncertain serious signal requires human review. Final PHARMAGUARD priority remains **{priority}** as a conservative safeguard; Random Forest output was **{rf_priority}**. Confirm current symptoms and urgency with a qualified clinician."
        )
    elif safety_gate_priority != "NONE" and rf_priority != safety_gate_priority:
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
# NEW ADR ANALYSIS — SCREEN BOUNDARY
# Keep Dashboard, Cases, Analytics and Database on their own routed screens.
# =========================================================
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

# Prevent legacy/other-screen content from rendering below New ADR Analysis.
st.stop()
