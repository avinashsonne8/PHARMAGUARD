
import streamlit as st
import uuid
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from datetime import date

st.set_page_config(
    page_title="PHARMAGUARD 2.0",
    page_icon="🛡️",
    layout="wide",
)

def save_case_to_google_sheets(payload):
    """
    Save a case through the PHARMAGUARD 2.0 Apps Script web app.
    Configure these in Streamlit Cloud -> Settings -> Secrets:
      PHARMAGUARD_API_URL = "your deployed Apps Script /exec URL"
      PHARMAGUARD_API_TOKEN = "same token as Apps Script Script Properties"
    Never hardcode the token in this file.
    """
    try:
        api_url = st.secrets.get("PHARMAGUARD_API_URL", "").strip()
        api_token = st.secrets.get("PHARMAGUARD_API_TOKEN", "").strip()

        if not api_url or not api_token:
            return False, (
                "Google Sheets integration is not configured yet. "
                "Add PHARMAGUARD_API_URL and PHARMAGUARD_API_TOKEN to "
                "Streamlit Cloud Secrets after deploying the Apps Script web app."
            )

        payload = dict(payload)
        payload["api_token"] = api_token

        request = Request(
            api_url,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=20) as response:
            body = response.read().decode("utf-8")
            result = json.loads(body)

        if result.get("success") is True:
            return True, result.get("message", "Case saved successfully.")

        return False, result.get("message", "The API did not save the case.")

    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        return False, (
            "Could not save the case to Google Sheets. "
            "Check the deployment URL, access settings, and API configuration."
        )
    except Exception:
        return False, "Could not save the case. Check the API configuration."


LANGUAGES = {
    "मराठी": {
        "subtitle": "रुग्ण-केंद्रित औषध सुरक्षा प्रणाली",
        "notice": "स्वतंत्र Prototype — PHARMAGUARD 1.0 अपरिवर्तित आहे.",
        "role": "तुम्ही कोण आहात?",
        "patient": "रुग्ण (Patient)",
        "professional": "आरोग्यसेवा व्यावसायिक",
        "report": "औषधाच्या दुष्परिणामाची नोंद करा",
        "pid": "Patient Reference ID",
        "name": "नाव (ऐच्छिक)",
        "age": "वय",
        "medicine": "औषधाचे नाव",
        "symptoms": "काय त्रास किंवा लक्षणे झाली?",
        "onset": "लक्षणे कधी सुरू झाली?",
        "emergency": "गंभीर लक्षणे आहेत का?",
        "breathing": "श्वास घेण्यास त्रास",
        "swelling": "घसा किंवा जीभ सुजणे",
        "fainting": "बेशुद्ध पडणे किंवा कोसळणे",
        "submit": "नोंद तपासा",
        "required": "औषधाचे नाव आणि लक्षणे भरणे आवश्यक आहे.",
        "urgent": "तातडीची सूचना: श्वास घेण्यास त्रास, घसा/जीभ सुजणे किंवा बेशुद्ध पडणे असल्यास त्वरित आपत्कालीन वैद्यकीय मदत घ्या. फॉर्म भरण्यासाठी थांबू नका.",
        "review": "फॉर्मची प्राथमिक तपासणी पूर्ण. ही नोंद फक्त या prototype session मध्ये आहे; सुरक्षित database मध्ये save केलेली नाही.",
        "professional_welcome": "आरोग्यसेवा व्यावसायिक विभाग",
        "professional_note": "केस-रिव्ह्यू Prototype",
        "disclaimer": "हा prototype वैद्यकीय निदान किंवा उपचाराचा पर्याय नाही.",
    },
    "हिंदी": {
        "subtitle": "रोगी-केंद्रित दवा सुरक्षा प्रणाली",
        "notice": "स्वतंत्र Prototype — PHARMAGUARD 1.0 अपरिवर्तित है।",
        "role": "आप कौन हैं?",
        "patient": "रोगी (Patient)",
        "professional": "स्वास्थ्य सेवा पेशेवर",
        "report": "दवा की प्रतिकूल प्रतिक्रिया दर्ज करें",
        "pid": "Patient Reference ID",
        "name": "नाम (वैकल्पिक)",
        "age": "उम्र",
        "medicine": "दवा का नाम",
        "symptoms": "क्या परेशानी या लक्षण हुए?",
        "onset": "लक्षण कब शुरू हुए?",
        "emergency": "क्या गंभीर लक्षण हैं?",
        "breathing": "सांस लेने में परेशानी",
        "swelling": "गले या जीभ में सूजन",
        "fainting": "बेहोशी या गिर जाना",
        "submit": "प्रविष्टि जाँचें",
        "required": "दवा का नाम और लक्षण भरना आवश्यक है।",
        "urgent": "तत्काल सूचना: सांस लेने में परेशानी, गले/जीभ में सूजन या बेहोशी होने पर तुरंत आपातकालीन चिकित्सा सहायता लें। फॉर्म भरने के लिए प्रतीक्षा न करें।",
        "review": "प्रारंभिक जाँच पूरी। यह प्रविष्टि केवल इस prototype session में है; सुरक्षित database में save नहीं हुई है।",
        "professional_welcome": "स्वास्थ्य सेवा पेशेवर विभाग",
        "professional_note": "केस-रिव्यू Prototype",
        "disclaimer": "यह prototype चिकित्सा निदान या उपचार का विकल्प नहीं है।",
    },
    "English": {
        "subtitle": "Patient-Centric Medication Safety System",
        "notice": "Independent development prototype. PHARMAGUARD 1.0 remains unchanged.",
        "role": "Who are you?",
        "patient": "Patient",
        "professional": "Healthcare Professional",
        "report": "Report a Possible Adverse Drug Reaction",
        "pid": "Patient Reference ID",
        "name": "Name (optional)",
        "age": "Age",
        "medicine": "Medicine name",
        "symptoms": "What symptoms or reaction occurred?",
        "onset": "When did the symptoms start?",
        "emergency": "Are any emergency warning signs present?",
        "breathing": "Difficulty breathing",
        "swelling": "Throat or tongue swelling",
        "fainting": "Fainting or collapse",
        "submit": "Review report",
        "required": "Medicine name and symptoms are required.",
        "urgent": "URGENT: If there is difficulty breathing, throat/tongue swelling, or fainting, seek emergency medical help immediately. Do not wait to complete this form.",
        "review": "Initial form check complete. This report exists only in this prototype session; it has NOT been saved to a secure database.",
        "professional_welcome": "Healthcare Professional section",
        "professional_note": "Case Review Prototype",
        "disclaimer": "This prototype is not a substitute for medical diagnosis or treatment.",
    },
}

EMERGENCY_SIGNS = [
    "Difficulty breathing",
    "Throat or tongue swelling",
    "Fainting or collapse",
    "Severe bleeding",
    "Seizure",
    "Severe chest pain",
]

st.session_state.setdefault("language", "मराठी")

language = st.selectbox(
    "Language / भाषा",
    list(LANGUAGES.keys()),
    key="app_language",
)
t = LANGUAGES[language]

st.title("🛡️ PHARMAGUARD 2.0")
st.subheader(t["subtitle"])
st.info(t["notice"])

role = st.radio(
    t["role"],
    [t["patient"], t["professional"]],
    key="user_role",
)

if role == t["patient"]:
    st.header(t["report"])

    if "patient_reference" not in st.session_state:
        st.session_state["patient_reference"] = (
            "PHG2-" + uuid.uuid4().hex[:8].upper()
        )

    st.caption(
        f'{t["pid"]}: {st.session_state["patient_reference"]}'
    )

    with st.form("patient_adr_report"):
        name = st.text_input(t["name"])
        age = st.number_input(
            t["age"], min_value=1, max_value=120, value=30
        )
        medicine = st.text_input(t["medicine"])
        symptoms = st.text_area(t["symptoms"])
        onset = st.date_input(
            t["onset"],
            value=date.today(),
            max_value=date.today(),
        )

        st.markdown(f'**{t["emergency"]}**')
        breathing = st.checkbox(t["breathing"])
        swelling = st.checkbox(t["swelling"])
        fainting = st.checkbox(t["fainting"])

        submitted = st.form_submit_button(t["submit"])

    if breathing or swelling or fainting:
        st.error(t["urgent"])

    if submitted:
        if not medicine.strip() or not symptoms.strip():
            st.warning(t["required"])
        else:
            patient_flags = []
            if breathing:
                patient_flags.append(t["breathing"])
            if swelling:
                patient_flags.append(t["swelling"])
            if fainting:
                patient_flags.append(t["fainting"])

            patient_emergency_status = (
                "URGENT - emergency warning sign reported"
                if patient_flags
                else "No listed emergency flags selected"
            )

            saved, save_message = save_case_to_google_sheets({
                "case_id": st.session_state["patient_reference"],
                "role": "Patient",
                "age": int(age),
                "sex": "Not provided",
                "medicine": medicine.strip(),
                "adr": symptoms.strip(),
                "emergency_flags": patient_flags,
                "emergency_status": patient_emergency_status,
                "seriousness": "Needs healthcare professional assessment",
                "review_status": "Pending",
                "reviewer_notes": (
                    "Reported symptom onset: " + str(onset)
                    + ("; Optional name provided by patient."
                       if name.strip() else "")
                ),
            })

            st.write(
                f'**{t["pid"]}:** '
                f'{st.session_state["patient_reference"]}'
            )
            st.write(f'**{t["age"]}:** {age}')
            st.write(f'**{t["medicine"]}:** {medicine}')
            st.write(f'**{t["symptoms"]}:** {symptoms}')
            st.write(f'**{t["onset"]}:** {onset}')

            if saved:
                st.success("Report saved to the PHARMAGUARD 2.0 database.")
            else:
                st.warning("Report was not saved to the database. " + save_message)

            if patient_flags:
                st.error(t["urgent"])

else:
    st.header(t["professional_welcome"])
    st.info(t["professional_note"])

    st.subheader("Emergency Safety Review")
    st.warning(
        "Check for urgent warning signs before routine review. "
        "Do not delay emergency medical care for this form."
    )

    emergency_flags = st.multiselect(
        "Emergency warning signs reported",
        EMERGENCY_SIGNS,
        key="professional_emergency_flags",
    )

    if emergency_flags:
        st.error(
            "URGENT: Emergency warning sign(s) reported: "
            + ", ".join(emergency_flags)
        )
        st.error(
            "Seek immediate emergency medical assessment. "
            "Do not delay urgent care for this form."
        )
    else:
        st.info(
            "No emergency warning signs selected. "
            "This does not rule out a medical emergency."
        )

    st.divider()
    st.subheader("Case Review")

    with st.form("professional_case_review"):
        case_id = st.text_input("Patient / Case Reference ID")
        medicine_review = st.text_input("Medicine name")
        adr_review = st.text_area("Reported ADR / Symptoms")

        onset_review = st.date_input(
            "Symptom onset date",
            value=date.today(),
            max_value=date.today(),
            key="professional_onset",
        )

        seriousness = st.selectbox(
            "Seriousness review",
            [
                "Not assessed",
                "Potentially serious",
                "Not currently identified as serious",
                "Needs further assessment",
            ],
        )

        review_status = st.selectbox(
            "Review status",
            ["Pending", "Under Review", "Reviewed"],
        )

        reviewer_notes = st.text_area("Reviewer notes")

        review_submitted = st.form_submit_button("Review Case")

    if review_submitted:
        if not case_id.strip():
            st.warning("Enter a Patient / Case Reference ID.")
        elif not medicine_review.strip():
            st.warning("Enter the medicine name.")
        elif not adr_review.strip():
            st.warning("Enter the reported ADR / symptoms.")
        else:
            st.subheader("Case Review Summary")

            if emergency_flags:
                st.error("EMERGENCY STATUS: URGENT")
                st.write(
                    "**Emergency warning signs reported:** "
                    + ", ".join(emergency_flags)
                )
                st.error(
                    "Immediate emergency medical assessment is needed. "
                    "Do not delay urgent care for routine case review."
                )
            else:
                st.info(
                    "EMERGENCY STATUS: No emergency flags selected "
                    "in this review. This does not rule out an emergency."
                )
                st.write("**Emergency warning signs reported:** None selected")

            st.divider()
            st.write("**Case ID:**", case_id)
            st.write("**Medicine:**", medicine_review)
            st.write("**Reported ADR:**", adr_review)
            st.write("**Symptom onset:**", onset_review)
            st.write("**Seriousness review:**", seriousness)
            st.write("**Review status:**", review_status)
            st.write("**Reviewer notes:**", reviewer_notes)

            professional_emergency_status = (
                "URGENT - emergency warning sign reported"
                if emergency_flags
                else "No emergency flags selected in this review"
            )

            saved, save_message = save_case_to_google_sheets({
                "case_id": case_id.strip(),
                "role": "Healthcare Professional",
                "medicine": medicine_review.strip(),
                "adr": adr_review.strip(),
                "emergency_flags": emergency_flags,
                "emergency_status": professional_emergency_status,
                "seriousness": seriousness,
                "review_status": review_status,
                "reviewer_notes": (
                    "Symptom onset: " + str(onset_review)
                    + ("; " + reviewer_notes.strip()
                       if reviewer_notes.strip() else "")
                ),
            })

            if saved:
                st.success("Case review saved to the PHARMAGUARD 2.0 database.")
            else:
                st.warning("Case review was not saved to the database. " + save_message)

            st.caption(
                "Prototype support only. This summary does not establish "
                "diagnosis, drug causality, or a final clinical decision."
            )

st.caption(t["disclaimer"])
