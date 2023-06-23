import streamlit as st
from gpt4_client import GPT4Client
from email_client import send_email


def main():
    st.title("AI Veterinarian CoPilot")
    col1, col2, col3 = st.columns([3, 1, 3]) # Create two columns

    with col1:
        conversation = st.text_area("Step 1: Enter Patient History. Modify to Update Patient History, SOAP and Differentials.", height=100)  # Increase textarea height

        if st.button("Step 2: Generate Patient SOAP"):
            gpt4_client = GPT4Client()

            ## add a loading spinner
            with st.spinner('Generating Patient SOAP... This will take about 30 seconds.'):
                patient_history = gpt4_client.generate_patient_history(conversation)

            # Store necessary states
            st.session_state['conversation'] = conversation
            st.session_state['gpt4_client'] = gpt4_client

            # Immediately display patient history after it's generated
            # Split patient_history into sections
            sections = patient_history.split('\n\n')

            for section in sections:
                # Split section into title and content
                title, content = section.split(':', 1)
                   
                # Make each section collapsible
                if st.expander(title.strip()).markdown(f"{content.strip()}"):
                    pass
            
            # Now generate diagnoses and display it on col3
            with col3:
                with st.spinner('SOAP Generated! Generating Differentials...'):
                    diagnoses = gpt4_client.generate_diagnoses(conversation)

            st.session_state['diagnoses'] = diagnoses

    with col3:
        if 'diagnoses' in st.session_state:
            ## select multiple diagnoses
            diagnosis_name = st.multiselect("Step 3: Select a Differential for Treatment Plan. Change Selection for Another Plan.", st.session_state['diagnoses'])
            st.session_state['chosen_diagnoses'] = diagnosis_name
                
            gpt4_client = st.session_state['gpt4_client']
            conversation = st.session_state['conversation']

            if st.button("Step 4: Get Patient Medical Summary with your Selected Differential"):
                st.markdown("**Potential Diagnoses:**\n\n")  # Use markdown for better formatting
                for i, diagnosis in enumerate(diagnosis_name):
                    st.markdown(f"{i+1}. {diagnosis}")
                
                with st.spinner('Generating Medical Summary... This will take 30 seconds.'):
                    medical_summary = gpt4_client.generate_record(diagnosis_name, conversation)
                
                st.markdown(f"**Medical Summary**\n\n{medical_summary}")  # Use markdown for better formatting

                st.session_state['medical_summary'] = medical_summary

    with col3:
        if "medical_summary" in st.session_state:
            email = st.text_input("Email address to send the report to:")
            if st.button("Email Report"):
                response = send_email(email, "Your AI Veterinarian Report", st.session_state['medical_summary'])
                if response == 202:
                    st.success("Report sent successfully!")
                else:
                    st.error(f"An error occurred: {response}")

        
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
