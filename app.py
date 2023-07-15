import streamlit as st
from gpt4_client import GPT4Client
from email_client import send_email
from langchain.document_loaders import PyPDFLoader
import tempfile
import os
import json

def main():
    st.title("AI Veterinarian Laboratory CoPilot")
    col1, col2, col3 = st.columns([3, 1, 3]) # Create two columns

    with col1:
        
        ## add a file upload for lab results
        uploaded_file = st.file_uploader("Step 1: Upload IDEXX or Antech Lab Results", type=['pdf'])
        if uploaded_file is not None:
            st.write("File uploaded successfully!")
            ## save the file to a temp directory
            with tempfile.NamedTemporaryFile(delete=False) as fp:
                fp.write(uploaded_file.read())
                st.session_state['file_path'] = fp.name

            loader = PyPDFLoader(fp.name)
            docs = loader.load()
            pdf_string = "".join(docs[i].page_content for i in range(len(docs)))

            st.session_state['pdf_string'] = pdf_string 
            os.unlink(fp.name)

        conversation = st.text_area("(Optional) Enter Patient Signalment and History. Modify to Update Differentials.", height=100)  # Increase textarea height

        if st.button("Step 2: Click to Generate Potential Differentials"):
            gpt4_client = GPT4Client()

            # ## add a loading spinner
            with st.spinner('Generating Patient Differentials... This will take about 30 seconds.'):

                if 'pdf_string' in st.session_state:
                    diagnoses = gpt4_client.generate_diagnoses_with_pdf(conversation, st.session_state['pdf_string'])
                else:
                    diagnoses = gpt4_client.generate_diagnoses(conversation)

            st.session_state['diagnoses'] = diagnoses
            ## diagnoses is a string in JSON-type format

            # # Store necessary states
            st.session_state['conversation'] = conversation
            st.session_state['gpt4_client'] = gpt4_client

            ## parse this json and display it in collapsible sections using st.expander
            diagnoses = json.loads(diagnoses)

            ## the diagnoses should be the title and the justification should be the content

            print(diagnoses)
            st.session_state['diagnoses'] = diagnoses

            if 'diagnoses' in st.session_state:
                st.write("Here are the potential differentials for your patient:")
                for diag in st.session_state['diagnoses']:
                    with st.expander(diag['diagnosis']):
                        st.write(diag['justification'])

    with col3:
        if 'diagnoses' in st.session_state:
            ## select multiple diagnoses
            ## get just the diagnoses from the JSON
            diagnoses_no_justification = [diag['diagnosis'] for diag in st.session_state['diagnoses']]

            diagnosis_name = st.multiselect("Step 3: Select One or More Differential(s). Revise to Modify Medical Chart.", diagnoses_no_justification)
            st.session_state['chosen_diagnoses'] = diagnosis_name
                
            gpt4_client = st.session_state['gpt4_client']
            conversation = st.session_state['conversation']

            if st.button("Step 4: Click to get Medical Chart"):
                st.markdown("**Potential Diagnoses:**\n\n")  # Use markdown for better formatting
                for i, diagnosis in enumerate(diagnosis_name):
                    st.markdown(f"{i+1}. {diagnosis}")
                
                with st.spinner('Generating Medical Summary... This will take 30 seconds.'):
                    if 'pdf_string' in st.session_state:
                        medical_summary = gpt4_client.generate_record(diagnosis_name, conversation, st.session_state['pdf_string'])
                    else:
                        ## pass in none for the pdf string
                        medical_summary = gpt4_client.generate_record(diagnosis_name, conversation, None)
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
