import streamlit as st
from gpt4_client import GPT4Client

def main():
    def update_diagnosis():
        with col3:
            diagnosis_name = st.selectbox("Select a differential from the list below:", st.session_state['diagnoses'])
            st.session_state['diagnosis_name'] = diagnosis_name
                
            gpt4_client = st.session_state['gpt4_client']
            diagnosis_name = st.session_state['diagnosis_name']
            conversation = st.session_state['conversation']

            if st.button("Get Treatment Plan Based on Diagnosis"):
                st.markdown(f"**Diagnosis:**\n\n{st.session_state['diagnosis_name']}")  # Use markdown for better formatting

                treatment = gpt4_client.generate_treatment(diagnosis_name, conversation)
                st.markdown(f"**Treatment Plan:**\n\n{treatment}")  # Use markdown for better formatting

    st.title("GPTVet: The AI-Powered Vet Assistant")
    col1, col2, col3 = st.columns([3, 1, 3]) # Create two columns

    with col1:
        conversation = st.text_area("Enter patient history", height=250)  # Increase textarea height
        if st.button("Generate Patient SOAP"):
            gpt4_client = GPT4Client()
            diagnoses = gpt4_client.generate_diagnoses(conversation)
            patient_history = gpt4_client.generate_patient_history(conversation)

            st.session_state['diagnoses'] = diagnoses
            st.session_state['patient_history'] = patient_history
            st.session_state['conversation'] = conversation
            st.session_state['gpt4_client'] = gpt4_client

        if 'patient_history' in st.session_state:
            # Split patient_history into sections
            sections = st.session_state['patient_history'].split('\n\n')

            for section in sections:
                # Split section into title and content
                print(section)
                title, content = section.split(':', 1)
                
                # Make each section collapsible
                if st.expander(title.strip()).markdown(f"{content.strip()}"):
                    pass
                ## rerun the app with the new patient history
            update_diagnosis()

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
