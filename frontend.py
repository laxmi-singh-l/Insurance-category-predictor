# import streamlit as st
# import requests
# import os

# # Default to the local API port used when running the app via uvicorn here
# API_URL = os.environ.get("API_URL", "http://127.0.0.1:8001/predict")

# st.set_page_config(layout="wide")

# st.title("Insurance  Premium category prediction")

# st.markdown("Enter your details below:")

# # input fields

# age = st.number_input("Age", value=0)
# weight = st.number_input("Weight",  value=30)
# height = st.number_input("Height", value=1.7)
# income_lpa = st.number_input("Income",  value=0)
# smoker = st.selectbox("Smoker", options=[True, False])
# city = st.text_input("City", value= "Mumbai")
# occupation = st.selectbox("Occupation", options=['retired', 'unemployed', 'business owner', 'government job', 'student', 'freelancer', 'private job'])

# if st.button("predict premium category"):
#     input_data = {
#         "age": age,
#         "weight": weight,
#         "height": height,
#         "income_lpa": income_lpa,
#         "smoker": smoker,
#         "city": city,
#         "occupation": occupation
#     }

#     try:
#         response = requests.post(API_URL, json=input_data, timeout=5)
#         if not response.ok:
#             st.error(f"Request failed: {response.status_code} - {response.text}")
#         else:
#             # parse JSON and handle different possible key names from the API
#             try:
#                 result_data = response.json()
#             except ValueError:
#                 st.error("API returned invalid JSON")
#             else:
#                 prediction = (
#                     result_data.get("predicted_category")
#                     or result_data.get("predicted category")
#                     or result_data.get("prediction")
#                     or result_data.get("predicted")
#                 )
#                 if prediction is None:
#                     st.error(f"Unexpected API response: {result_data}")
#                 else:
#                     st.success(f"Predicted category: {prediction}")
#     except Exception as e:
#         st.error(f"Request failed: {e}")


#  there are twq saparate codes
# the first one is the original code and the second one is the improved code with better UI and error handling. I have added comments to explain the changes made in the improved code.





import streamlit as st
import requests
import os

# Default to the local API port used when running the app via uvicorn here
API_URL = os.environ.get("API_URL", "http://127.0.0.1:8001/predict")

# 1. Page Config with an icon and centered layout for a cleaner form look
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🛡️",
    layout="centered" 
)

# 2. Modern App Header
st.title("🛡️ Insurance Premium Category Prediction")
st.markdown("Provide the individual's details below to predict their risk and premium category.")
st.write("---")

# 3. Form Container to group elements nicely
with st.container(border=True):
    st.subheader("📋 Personal & Demographics Data")
    
    # Use columns to distribute fields evenly
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=0, max_value=120, value=0)
        height = st.number_input("Height (in meters)", min_value=0.0, max_value=3.0, value=1.7)
        city = st.text_input("City", value="Mumbai")

    with col2:
        weight = st.number_input("Weight (in kg)", min_value=0, max_value=300, value=30)
        income_lpa = st.number_input("Income (LPA)", min_value=0, value=0)
        occupation = st.selectbox("Occupation", options=['retired', 'unemployed', 'business owner', 'government job', 'student', 'freelancer', 'private job'])
    
    # Lifestyle section
    st.markdown("---")
    smoker = st.selectbox("Smoker Status", options=[True, False], format_func=lambda x: "Yes" if x else "No")

st.write("") # Spacer

# 4. Full-width, distinct action button
if st.button("Predict Premium Category", use_container_width=True, type="primary"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=input_data, timeout=5)
        if not response.ok:
            st.error(f"Request failed: {response.status_code} - {response.text}")
        else:
            # parse JSON and handle different possible key names from the API
            try:
                result_data = response.json()
            except ValueError:
                st.error("API returned invalid JSON")
            else:
                prediction = (
                    result_data.get("predicted_category")
                    or result_data.get("predicted category")
                    or result_data.get("prediction")
                    or result_data.get("predicted")
                )
                if prediction is None:
                    st.error(f"Unexpected API response: {result_data}")
                else:
                    # 5. Styled Output Presentation Card
                    st.write("") 
                    with st.container(border=True):
                        st.success(f"### 🎉 Prediction Result: **{str(prediction).upper()}**")
                        st.caption("This prediction is generated based on the statistical modeling of historical premium segments.")
                        
    except Exception as e:
        st.error(f"Request failed: {e}")
