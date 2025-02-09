import streamlit as st
import pandas as pd
from datetime import datetime

# Load dataset
@st.cache
def load_data(uploaded_file):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    return None

# Define category and state mappings
CATEGORY_MAPPING = {
    0: "Entertainment", 1: "Food Dining", 2: "Gas Transport", 3: "Grocery NET", 4: "Grocery POS",
    5: "Health Fitness", 6: "Home", 7: "Kids Pets", 8: "Miscellaneous NET", 9: "Miscellaneous POS",
    10: "Personal Care", 11: "Shopping NET", 12: "Shopping POS", 13: "Travel"
}

STATE_MAPPING = {
    0: "Andhra Pradesh", 1: "Arunachal Pradesh", 2: "Assam", 3: "Bihar", 4: "Chhattisgarh",
    5: "Goa", 6: "Gujarat", 7: "Haryana", 8: "Jharkhand", 9: "Himachal Pradesh",
    10: "Karnataka", 11: "Kerala", 12: "Madhya Pradesh", 13: "Maharashtra", 14: "Manipur",
    15: "Meghalaya", 16: "Mizoram", 17: "Nagaland", 18: "Odisha", 19: "Punjab",
    20: "Rajasthan", 21: "Sikkim", 22: "Tamil Nadu", 23: "Telangana", 24: "Tripura",
    25: "Uttar Pradesh", 26: "Uttarakhand", 27: "West Bengal", 28: "Andaman and Nicobar Islands",
    29: "Chandigarh", 30: "Dadra and Nagar Haveli and Daman and Diu", 31: "Delhi", 32: "Jammu and Kashmir",
    33: "Ladakh", 34: "New York", 35: "Lakshadweep", 36: "Puducherry", 37: "Oregon", 38: "Pennsylvania",
    39: "Rhode Island", 40: "London", 41: "South Dakota", 42: "Tennessee", 43: "Texas", 44: "Utah",
    45: "Virginia", 46: "Singapore", 47: "Washington", 48: "New York", 49: "West Virginia", 50: "Maldives"
}

# Streamlit UI
st.title("UPI Fraud Detection System")

# File Upload
uploaded_file = st.file_uploader("Upload UPI Fraud Dataset (CSV)", type=["csv"])
df = load_data(uploaded_file)

if df is not None:
    st.success("Dataset Loaded Successfully!")
    st.write(df.head())  # Show dataset preview

    # Form for user input
    st.header("Enter Transaction Details")
    upi_number = st.text_input("UPI Number")
    amount = st.number_input("Transaction Amount", min_value=1.0)
    state_code = st.selectbox("State", options=list(STATE_MAPPING.keys()), format_func=lambda x: STATE_MAPPING[x])
    zip_code = st.text_input("ZIP Code")
    transaction_date = st.date_input("Transaction Date")
    year = transaction_date.year
    category_code = st.selectbox("Category", options=list(CATEGORY_MAPPING.keys()), format_func=lambda x: CATEGORY_MAPPING[x])

    if st.button("Check Fraud Risk"):
        # Check if transaction exists in dataset
        match = df[(df['trans_amount'] == amount) &
                   (df['state'] == state_code) &
                   (df['zip'] == int(zip_code)) &
                   (df['trans_year'] == year) &
                   (df['category'] == category_code) &
                   (df['upi_number'] == int(upi_number))]

        if not match.empty:
            fraud_label = match.iloc[0]['fraud_risk']
            if fraud_label == 1:
                st.error("⚠️ Fraudulent Transaction Detected! ⚠️")
            else:
                st.success("✅ Transaction is Valid")
        else:
            st.warning("⚠️ No exact match found in dataset. Use additional checks!")
