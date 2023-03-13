import streamlit as st

st.set_page_config(
    page_title="ML Apps",
    page_icon="🚝",
)

st.markdown("### Select an AI App from the sidebar:")
st.markdown("1. Querybot: Run Natural Language Queries on your data")
st.markdown("2. Chatbot: Chat with GPT-3.5 turbo")
st.markdown("3. Plotting Demo: Plotting a time-series dataset")
st.markdown("\n")
st.markdown(
    "- built with [Streamlit](https://streamlit.io), [FastAPI](https://fastapi.tiangolo.com) and [Phidata](https://phidata.com)"  # noqa: E501
)

st.sidebar.success("Select an App from above")
