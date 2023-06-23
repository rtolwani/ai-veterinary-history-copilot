import streamlit as st
from gpt4_client import GPT4Client

def main():
    def update_diagnosis():
        with col3:
            ## select multiple diagnoses
            diagnosis_name = st.multiselect("Step 3: Select a Differential for Treatment Plan. Change Selection for Another Plan.", st.session_state['diagnoses'])
            st.session_state['diagnosis_name'] = diagnosis_name
                
            gpt4_client = st.session_state['gpt4_client']
            diagnosis_name = st.session_state['diagnosis_name']
            conversation = st.session_state['conversation']

            if st.button("Step 4: Get Treatment Plan"):
                st.markdown(f"**Diagnosis:**\n\n{st.session_state['diagnosis_name']}")  # Use markdown for better formatting

                treatment = gpt4_client.generate_treatment(diagnosis_name, conversation)
                st.markdown(f"**Medical Summary**\n\n{treatment}")  # Use markdown for better formatting

            if st.button("Step 5: Get Patient Medical Summary with your Selected Differential"):
                st.markdown(f"**Diagnosis:**\n\n{st.session_state['diagnosis_name']}")  # Use markdown for better formatting

                treatment = gpt4_client.generate_record(diagnosis_name, conversation)
                st.markdown(f"**Medical Summary**\n\n{treatment}")  # Use markdown for better formatting

    st.title("AI Veterinarian CoPilot")
    col1, col2, col3 = st.columns([3, 1, 3]) # Create two columns

    with col1:
        conversation = st.text_area("Step 1: Enter Patient History. Modify to Update Patient History, SOAP and Differentials.", height=100)  # Increase textarea height

        if st.button("Step 2: Generate Patient SOAP"):
            ## add a loading spinner
            with st.spinner('Generating Patient SOAP... This will take about 30 seconds.'):
                gpt4_client = GPT4Client()
                patient_history = gpt4_client.generate_patient_history(conversation)

            with st.spinner('Generating Patient SOAP... This will take about 30 seconds.'):
                diagnoses = gpt4_client.generate_diagnoses(conversation)

            st.session_state['diagnoses'] = diagnoses
            st.session_state['patient_history'] = patient_history
            st.session_state['conversation'] = conversation
            st.session_state['gpt4_client'] = gpt4_client

        if 'patient_history' in st.session_state:
            # Split patient_history into sections
            sections = st.session_state['patient_history'].split('\n\n')

            for section in sections:
                # Split section into title and content
                title, content = section.split(':', 1)
                   
                # Make each section collapsible
                if st.expander(title.strip()).markdown(f"{content.strip()}"):
                    pass
                ## rerun the app with the new patient history
            update_diagnosis()

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
