import streamlit as st
from gpt4_client import GPT4Client

def main():
    st.title("Vet Diagnosis Assistant")
    col1, col2 = st.columns(2)  # Create two columns

    with col1:
        conversation = st.text_area("Enter the conversation between vet and client:")
        if st.button("Generate Diagnoses"):
            gpt4_client = GPT4Client()
            diagnoses = gpt4_client.generate_diagnoses(conversation)
            patient_history = gpt4_client.generate_patient_history(conversation)
            diagnosis_name = st.selectbox("Select a diagnosis:", diagnoses)

            st.session_state['patient_history'] = patient_history
            st.session_state['diagnosis_name'] = diagnosis_name
            st.session_state['conversation'] = conversation
            st.session_state['gpt4_client'] = gpt4_client

        if 'patient_history' in st.session_state:
            st.markdown(f"**Patient History:**\n\n{st.session_state['patient_history']}")  # Use markdown for better formatting


    with col2:

        if 'diagnosis_name' in st.session_state:
            gpt4_client = st.session_state['gpt4_client']
            diagnosis_name = st.session_state['diagnosis_name']
            conversation = st.session_state['conversation']

            if st.button("Get Diagnostic and Treatment Plans"):
                treatment = gpt4_client.generate_treatment(diagnosis_name, conversation)
                st.markdown(f"**Treatment Plan:**\n\n{treatment}")  # Use markdown for better formatting

        if 'diagnosis_name' in st.session_state:
            st.markdown(f"**Diagnosis:**\n\n{st.session_state['diagnosis_name']}")  # Use markdown for better formatting

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
