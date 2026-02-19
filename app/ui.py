import streamlit as st
from app.pipeline.cti_pipeline import CTIPipeline

st.set_page_config(page_title="CTI STIX Generator", layout="wide")
st.title("🛡️ CTI to STIX 2.1 Generator")

pipeline = CTIPipeline()

input_type = st.radio("Select Input Type", ["Text", "PDF", "URL"])

source = None

if input_type == "Text":
    source = st.text_area("Paste Threat Intelligence Text")

elif input_type == "PDF":
    source = st.file_uploader("Upload PDF", type=["pdf"])

elif input_type == "URL":
    source = st.text_input("Enter URL")

if st.button("Generate STIX Bundle"):
    if source:
        bundle = pipeline.process(source, input_type.lower())

        st.success("STIX 2.1 Bundle Generated")

        with st.expander("View STIX JSON"):
            st.json(bundle.serialize(pretty=True))

        st.download_button(
            label="Download STIX Bundle",
            data=bundle.serialize(pretty=True),
            file_name="stix_bundle.json",
            mime="application/json"
        )
    else:
        st.warning("Please provide input.")
