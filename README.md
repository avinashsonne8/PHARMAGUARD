# 💊 PHARMAGUARD

## AI-Assisted ADR Risk Prioritization System for Pharmacovigilance

PHARMAGUARD is a proof-of-concept pharmacovigilance support system designed to assist in the prioritization of Adverse Drug Reaction (ADR) reports for review.

The system combines a Machine Learning model with rule-based safety screening to identify potentially serious ADR signals and prioritize cases as Low, Moderate, or High.

---

## 🎯 Aim

To develop an AI-assisted system for prioritizing ADR reports according to potential risk and seriousness to support pharmacovigilance review.

---

## 🔬 Objectives

1. To identify and organize important information from ADR reports.
2. To analyze risk-related characteristics of ADR cases.
3. To develop a structured ADR prioritization framework.
4. To evaluate the feasibility of Machine Learning for ADR priority classification.
5. To develop a user-friendly PHARMAGUARD prototype.
6. To provide an explainable review-support output.

---

## ❓ Problem Statement

Pharmacovigilance systems may receive a large number of ADR reports. Reviewing every report with the same urgency can be time-consuming.

PHARMAGUARD is designed to assist reviewers by highlighting potentially serious cases and prioritizing ADR reports for further pharmacovigilance review.

---

## 💡 Key Features

- 🆔 Anonymous Patient ID / Case ID
- 👤 Patient age and sex
- 💊 Drug name entry
- ⚠️ ADR description
- 🛡️ Seriousness Safety Gate
- 🟡 Moderate Review Gate
- 🤖 Random Forest Machine Learning model
- 📋 ADR analysis result
- 📚 Session-based ADR history
- ⬇️ CSV export of ADR history
- 📝 Explanation/reason for prioritization

---

## ⚙️ System Workflow

Patient Information  
↓  
Drug + ADR Input  
↓  
Seriousness Safety Gate  
↓  
Potentially Serious Signal?  
→ YES → HIGH PRIORITY  
↓ NO  
Moderate Review Gate  
↓  
Moderate Review Signal?  
→ YES → MODERATE PRIORITY  
↓ NO  
Random Forest Model  
↓  
LOW / MODERATE / HIGH

---

## 🛡️ Seriousness Safety Gate

The system contains a project-defined safety screening layer.

Examples of serious indicators include:

- Anaphylaxis
- Difficulty breathing
- Respiratory distress
- Cardiac arrest
- Seizure/convulsion
- Shock
- Life-threatening reaction
- Severe allergic reaction

When a strong serious signal is detected, the system prioritizes the case as:

**HIGH PRIORITY**

This safety gate is designed to prevent the Machine Learning model from incorrectly assigning a low priority to an obvious serious signal.

---

## 🟡 Moderate Review Gate

A project-defined moderate-review layer is used for non-obviously-serious cases containing contextual indicators such as:

- Requiring medical attention
- Requiring monitoring
- Requiring evaluation
- Persistent symptoms
- Prolonged symptoms
- Recurrent symptoms
- Clinically meaningful dehydration

Example:

**ADR:** Persistent stomach pain requiring medical attention

Output:

**MODERATE PRIORITY**

The Moderate category is a project-defined review-priority category and is NOT an official FDA or WHO classification.

---

## 🤖 Machine Learning

The prototype uses a Random Forest Machine Learning model.

### Feature processing

- Numerical feature: Age
- Categorical features: Sex and Drug
- Text feature: ADR description
- Text representation: TF-IDF
- Categorical encoding: One-Hot Encoding
- Missing-value indicators

The Machine Learning model is used after the safety and moderate-review screening layers.

---

## 📊 Dataset

The project uses data derived from the FDA Adverse Event Reporting System (FAERS/AEMS) public data.

The dataset contains information such as:

- Case ID
- Patient demographic information
- Drug information
- ADR/reaction information
- Outcome information

FDA adverse-event reports are spontaneous reports and do not by themselves establish that a particular drug caused an event.

---

## 🧪 Model Development

A provisional labeled dataset was prepared for proof-of-concept model development.

Models evaluated during development included:

- Logistic Regression
- Random Forest

Random Forest showed better cross-validation performance than Logistic Regression in the current prototype evaluation.

### Important

The current labels were produced using a single-reviewer, project-defined labeling approach and should be considered provisional.

Therefore, current model performance represents a **proof-of-concept evaluation** and not clinical or regulatory validation.

---

## 📱 Application

PHARMAGUARD is implemented as a Streamlit web application.

### User enters:

1. Patient ID
2. Age
3. Sex
4. Drug Name
5. ADR

The system then provides:

- Risk Priority
- Seriousness/Review Flag
- Reason
- Review Recommendation

---

## 📚 ADR History

The application can display analyzed cases during the current session.

Users can download the current ADR history as a CSV file for project documentation and analysis.

---

## ⚠️ Limitations

1. The current prototype is not clinically validated.
2. The current labeled dataset is provisional.
3. The project uses a single-reviewer labeling approach.
4. The system does not establish drug-event causality.
5. Spontaneous-report data cannot be used directly to calculate true incidence.
6. The Moderate Priority category is project-defined.
7. The safety rules are screening rules and do not replace clinical judgment.
8. The current history is session-based and is not a permanent clinical database.

---

## 🔐 Privacy

Only anonymous study/case identifiers should be used in the prototype.

Do NOT enter:

- Patient name
- Aadhaar number
- Mobile number
- Address
- Hospital registration number
- Other directly identifying information

---

## ⚕️ Safety Disclaimer

PHARMAGUARD is an AI-assisted pharmacovigilance review-support prototype.

It is NOT:

- A diagnostic tool
- A treatment recommendation system
- A drug-event causality assessment tool
- A substitute for a pharmacist or physician
- A regulatory decision system

Final assessment must be performed by a qualified healthcare or pharmacovigilance professional.

---

## 🎓 Academic Project

**Project:** PHARMAGUARD  
**Domain:** Pharmacovigilance + Artificial Intelligence + Machine Learning  
**Program:** Bachelor of Pharmacy (B.Pharm)

---

## 🔭 Future Scope

Future versions may include:

- Permanent database storage
- Larger and independently validated datasets
- Multi-reviewer labeling
- Inter-rater agreement assessment
- Advanced NLP/transformer models
- Explainable AI methods
- ADR trend dashboards
- Drug-wise ADR analysis
- Automated report generation
- Role-based access and privacy controls
- External validation on independent datasets

---

## 👨‍💻 Project Status

**Current status: Proof-of-concept prototype**

The system is intended for academic research and demonstration purposes.
