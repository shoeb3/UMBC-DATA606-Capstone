import streamlit as st
import joblib
import numpy as np

# Loading pkl files
xgb        = joblib.load('xgb_model.pkl')
scaler     = joblib.load('scaler.pkl')
enc_maps   = joblib.load('encoder_maps.pkl')
gm         = joblib.load('global_mean.pkl')
features   = joblib.load('feature_list.pkl')
ref        = joblib.load('ref_stats.pkl')

st.title("H-1B Visa Certification Predictor")
st.write("Fill in the petition details below to estimate approval likelihood.")

# Inputs
employer   = st.text_input("Employer Name", "Google LLC")
soc_title  = st.selectbox("Job Title (SOC)", ref['all_soc_titles'])
state      = st.selectbox("Employer State", ref['all_states'])
annual_wage = st.number_input("Offered Annual Wage ($)", min_value=20000, max_value=500000, value=120000, step=5000)
prev_wage  = st.number_input("DOL Prevailing Wage ($)", min_value=20000, max_value=500000, value=105000, step=5000)
is_full_time = st.radio("Position Type", ["Full-Time", "Part-Time"], horizontal=True) == "Full-Time"
quarter    = st.selectbox("Filing Quarter", [1, 2, 3, 4], index=1,
                          format_func=lambda x: {1:"Q1 (Oct-Dec)", 2:"Q2 (Jan-Mar)", 3:"Q3 (Apr-Jun)", 4:"Q4 (Jul-Sep)"}[x])

# Predict
if st.button("Predict"):

    # Encoding categorical features
    def encode(col, val):
        m = enc_maps.get(col, {})
        return m.get(str(val), gm)

    emp_enc   = encode('EMPLOYER_NAME',  employer)
    soc_enc   = encode('SOC_TITLE',      soc_title)
    state_enc = encode('EMPLOYER_STATE', state)

    # features added
    wage_capped  = np.clip(annual_wage,  ref['median_annual_wage'] * 0.3, ref['median_annual_wage'] * 3)
    pw_capped    = np.clip(prev_wage,    ref['median_annual_wage'] * 0.3, ref['median_annual_wage'] * 3)
    wage_diff    = wage_capped - pw_capped
    log_wage     = np.log1p(wage_capped)
    log_pw       = np.log1p(pw_capped)
    wage_above   = int(annual_wage > prev_wage)
    large_emp    = int(emp_enc > 0.95)
    emp_count    = 500 if large_emp else 10

    # building features vector
    feat_map = {
        'ANNUAL_WAGE_CAPPED':         wage_capped,
        'ANNUAL_PREVAILING_WAGE_CAP': pw_capped,
        'WAGE_ABOVE_PREVAILING':      wage_above,
        'IS_FULL_TIME':               int(is_full_time),
        'QUARTER':                    quarter,
        'WAGE_DIFF':                  wage_diff,
        'LOG_WAGE':                   log_wage,
        'LOG_PW':                     log_pw,
        'IS_LARGE_EMPLOYER':          large_emp,
        'EMP_PETITION_COUNT':         emp_count,
        'EMPLOYER_NAME_ENC':          emp_enc,
        'SOC_TITLE_ENC':              soc_enc,
        'EMPLOYER_STATE_ENC':         state_enc,
    }

    X = np.array([[feat_map.get(f, gm) for f in features]])
    X_sc = scaler.transform(X)

    prob = xgb.predict_proba(X_sc)[0][1]  # probability of Certified
    threshold = ref['best_threshold']
    prediction = "Certified" if prob >= threshold else "Not Certified"

    st.divider()
    if prediction == "Certified":
        st.success(f"Prediction: {prediction}")
    else:
        st.error(f"Prediction: {prediction}")

    st.metric("Certification Probability", f"{prob * 100:.1f}%")
    st.caption(f"Threshold used: {threshold:.3f} | Overall dataset certification rate: {ref['global_cert_rate']*100:.1f}%")
