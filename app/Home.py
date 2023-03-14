import streamlit as st

st.set_page_config(
    page_title="AI Apps",
    page_icon="🚝",
)

st.markdown("### Select an App from the sidebar:")
st.markdown("1. Stock Prediction: Predict stock price using time series forecasting")
st.markdown("2. Querybot: Run Natural Language Queries on your data")
st.markdown("3. Chatbot: Chat with GPT-3.5 turbo")
st.markdown("4. Plotting Demo: Plotting a time-series dataset")
st.markdown("\n")
st.markdown(
    "- built with [Streamlit](https://streamlit.io), [FastAPI](https://fastapi.tiangolo.com) and [Phidata](https://phidata.com)"  # noqa: E501
)

st.sidebar.success("Select an App from above")
