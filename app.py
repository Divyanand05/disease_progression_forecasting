import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Disease Forecast", layout="wide")
st.title("🩺 Disease Progression Forecasting System")

# ----------------- Helper functions -----------------
def safe_get_json(url: str):
    try:
        r = requests.get(url)
        return r.status_code, r.json()
    except Exception as e:
        return 500, {"error": str(e)}

def safe_post_json(url: str, payload=None):
    try:
        r = requests.post(url, json=payload)
        return r.status_code, r.json()
    except Exception as e:
        return 500, {"error": str(e)}

def load_patients():
    code, data = safe_get_json(f"{API}/patients/")
    if code != 200 or not isinstance(data, list):
        return []
    return data

def get_patient_options(patients):
    # Dropdown: "1 - Ravi Kumar"
    return {f"{p['id']} - {p['name']}": p["id"] for p in patients}

# Sidebar menu
menu = st.sidebar.selectbox(
    "Menu",
    ["Home", "Patients", "Clinical Records", "Prediction",]
)

# Load patients globally for dropdown
patients = load_patients()
patient_options = get_patient_options(patients)

# ---------------- HOME ----------------
if menu == "Home":
    st.markdown(
        """
        <h1 style='text-align: center; font-size: 44px;'>
            🩺 Disease Progression Forecasting System
        </h1>
        <p style='text-align: center; font-size: 18px; color: grey;'>
            AI-powered forecasting with Database + ML Prediction 
        </p>
        """,
        unsafe_allow_html=True
    )

    # ---- Load dashboard data ----
    code_pat, pat_data = safe_get_json(f"{API}/patients/")
    total_patients = len(pat_data) if code_pat == 200 and isinstance(pat_data, list) else 0

    # To estimate totals, we fetch records/preds for each patient
    total_records = 0
    total_predictions = 0
    recent_preds = []

    if code_pat == 200 and isinstance(pat_data, list):
        for p in pat_data:
            pid = p["id"]

            # records count
            c1, recs = safe_get_json(f"{API}/records/{pid}")
            if c1 == 200 and isinstance(recs, list):
                total_records += len(recs)

            # predictions count + recent predictions
            c2, preds = safe_get_json(f"{API}/predict/history/{pid}")
            if c2 == 200 and isinstance(preds, list):
                total_predictions += len(preds)
                for pr in preds[:3]:  # take few recent
                    pr["patient_id"] = pid
                    pr["patient_name"] = p["name"]
                    recent_preds.append(pr)

    # sort recent predictions by id desc (latest first)
    if recent_preds and "id" in recent_preds[0]:
        recent_preds = sorted(recent_preds, key=lambda x: x.get("id", 0), reverse=True)

    # ---- Metrics Cards ----
    st.markdown("## 📌 Dashboard Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("👤 Total Patients", total_patients)
    c2.metric("📊 Total Records", total_records)
    c3.metric("🤖 Total Predictions", total_predictions)

    # ---- Recent Predictions Table ----
    st.markdown("## 🕒 Recent Predictions")

    if recent_preds:
        df = pd.DataFrame(recent_preds)

        # show only important columns
        show_cols = []
        for col in ["id", "patient_name", "patient_id", "predicted_score", "risk_level", "created_at"]:
            if col in df.columns:
                show_cols.append(col)

        st.dataframe(df[show_cols].head(10), use_container_width=True)
    else:
        st.info("No predictions found yet. Add record and run prediction first.")

# ---------------- PATIENTS ----------------
elif menu == "Patients":
    st.subheader("👤 Patient Management")

    col1, col2 = st.columns([1, 1])

    # Create Patient
    with col1:
        st.markdown("### ➕ Add Patient")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        if st.button("Create Patient"):
            payload = {"name": name, "age": int(age), "gender": gender}
            code, data = safe_post_json(f"{API}/patients/", payload)

            if code == 200:
                st.success("Patient Created ✅")
            else:
                st.error("Failed ❌")
            st.json(data)

            st.info("Refresh the page or switch menu to reload dropdown patient list.")

    # List Patients
    with col2:
        st.markdown("### 📋 Patient List")
        if patients:
            df = pd.DataFrame(patients)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No patients available. Create one first.")

# ---------------- RECORDS ----------------
elif menu == "Clinical Records":
    st.subheader("📊 Clinical Records")

    if not patients:
        st.warning("No patients found. Please create a patient first.")
        st.stop()

    selected_label = st.selectbox("Select Patient", list(patient_options.keys()))
    patient_id = patient_options[selected_label]

    st.markdown("### ➕ Add Clinical Record")
    col1, col2, col3 = st.columns(3)

    with col1:
        bmi = st.number_input("BMI", value=0.04)
        bp = st.number_input("BP", value=0.02)
        s1 = st.number_input("S1", value=-0.04)

    with col2:
        s2 = st.number_input("S2", value=-0.03)
        s3 = st.number_input("S3", value=-0.04)
        s4 = st.number_input("S4", value=-0.01)

    with col3:
        s5 = st.number_input("S5", value=0.01)
        s6 = st.number_input("S6", value=0.02)

    if st.button("Save Record"):
        payload = {
            "patient_id": int(patient_id),
            "bmi": float(bmi),
            "bp": float(bp),
            "s1": float(s1),
            "s2": float(s2),
            "s3": float(s3),
            "s4": float(s4),
            "s5": float(s5),
            "s6": float(s6),
        }
        code, data = safe_post_json(f"{API}/records/", payload)

        if code == 200:
            st.success("Record saved ✅")
        else:
            st.error("Failed ❌")
        st.json(data)

    st.markdown("### 📌 Patient Records")
    code, records = safe_get_json(f"{API}/records/{int(patient_id)}")
    if code == 200 and isinstance(records, list) and len(records) > 0:
        df = pd.DataFrame(records)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No records found for this patient.")

# ---------------- PREDICTION ----------------
elif menu == "Prediction":
    st.subheader("🤖 Disease Progression Prediction")

    if not patients:
        st.warning("No patients found. Please create a patient first.")
        st.stop()

    selected_label = st.selectbox("Select Patient", list(patient_options.keys()))
    patient_id = patient_options[selected_label]

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### ▶ Run Prediction")
        if st.button("Run Prediction ✅"):
            code, result = safe_post_json(f"{API}/predict/{int(patient_id)}", None)

            if code == 200 and "predicted_score" in result:
                st.success("Prediction Done ✅")
                st.metric("Predicted Score", f"{result['predicted_score']:.2f}")
                st.metric("Risk Level", result["risk_level"])
                st.json(result)
            else:
                st.error("Prediction failed ❌")
                st.json(result)

    with col2:
        st.markdown("### 📜 Prediction History")
        code, preds = safe_get_json(f"{API}/predict/history/{int(patient_id)}")

        if code == 200 and isinstance(preds, list) and len(preds) > 0:
            df = pd.DataFrame(preds)

            # ensure datetime parsing
            if "created_at" in df.columns:
                df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

            st.dataframe(df, use_container_width=True)

            # ---------- Graph ----------
            if "predicted_score" in df.columns and "created_at" in df.columns:
                chart_df = df[["created_at", "predicted_score"]].dropna()
                chart_df = chart_df.sort_values("created_at")
                chart_df = chart_df.set_index("created_at")
                st.markdown("### 📈 Progression Score Trend")
                st.line_chart(chart_df)
        else:
            st.info("No predictions found yet. Run prediction first.")

