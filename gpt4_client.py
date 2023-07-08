import openai
from typing import List
import os
import streamlit as st
from langchain.chains import ChatVectorDBChain
from langchain.llms import OpenAI

MODEL = "gpt-4"


class GPT4Client:
    def __init__(self):
        ## get api key from os environ ['OPENAI_API_KEY']
        ## first check if we can get it from os environ (running locally)
        if os.environ.get('OPENAI_API_KEY') is not None:
            openai.api_key = os.environ.get('OPENAI_API_KEY')
        else:
            openai.api_key = st.secrets['OPENAI_API_KEY']


    def call_openai_chat(self, system_message: str, user_message: str) -> str:

        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=1,
        )

        return response['choices'][0]['message']['content']
        
    def generate_patient_history(self, conversation: str) -> str:
        
        system_message = "Generate a medical history for this patient in SOAP Format based on the pet's patient history. It should be formatted so that each section is separated by a newline, and the title of each section is followed by a colon. Don't include any other information."
        user_message = conversation

        return self.call_openai_chat(system_message, user_message)

    def generate_diagnoses_with_pdf(self, medical_history: str, lab_record: str) -> List[str]:
        """
        Args:

        Returns:
            List[str]: List of potential diagnoses        
        """
        SYSTEM_MESSAGE = """/
        Read the medical history and blood panel lab record for a pet and generate a list of potential diagnoses and justification based on the lab results.

        Format it in JSON as follows:

        [
            {
                "diagnosis": "anemia",
                "justification": "The patient has been feeling symptoms of anemia for the past 2 weeks./
                They have a low hematocrit level of 20%, which is below the normal range of 37-55% and indicates anemia./
                They also have a low hemoglobin level of 7.0 g/dL, which is below the normal range of 12-18 g/dL and indicates anemia."
            },
            {
                "diagnosis": "bacterial infection",
                "justification": "The patient has been feeling symptoms of lethargy and fever for the past 2 weeks.
                They have a high white blood cell count of 20,000 cells/mcL, which is above the normal range of 4,000-11,000 cells/mcL and indicates a bacterial infection."
            }
        ]
        """
        USER_MESSAGE = f"""LAB_RECORD: 
        ```
        {lab_record}
        ```
        MEDICAL_HISTORY:
        ``` 
        {medical_history}
        ```
        """

        return self.call_openai_chat(SYSTEM_MESSAGE, USER_MESSAGE)


    def generate_diagnoses(self, conversation: str) -> List[str]:
        
        SYSTEM_MESSAGE = """/
        Read the medical history for a pet and generate a list of potential diagnoses and justification based on the lab results.

        Format it in JSON as follows:

        [
            {
                "diagnosis": "anemia",
                "justification": "The patient has been feeling symptoms of anemia for the past 2 weeks./
                They have a low hematocrit level of 20%, which is below the normal range of 37-55% and indicates anemia./
                They also have a low hemoglobin level of 7.0 g/dL, which is below the normal range of 12-18 g/dL and indicates anemia."
            },
            {
                "diagnosis": "bacterial infection",
                "justification": "The patient has been feeling symptoms of lethargy and fever for the past 2 weeks.
                They have a high white blood cell count of 20,000 cells/mcL, which is above the normal range of 4,000-11,000 cells/mcL and indicates a bacterial infection."
            }
        ]
        """
        USER_MESSAGE = f"""
        MEDICAL_HISTORY:
        ``` 
        {conversation}
        ```
        """

        return self.call_openai_chat(SYSTEM_MESSAGE, USER_MESSAGE)
    
    def generate_treatment(self, diagnosis: list[str], conversation: str) -> str:
        
        system_message = "Generate a veterinary treatment plan based upon the following potential diagnoses and pet's history. Generate one plan per diagnosis. Just include the treatment plan."
        user_message = ""
        for diagnosis in diagnosis:
            user_message += f"Diagnosis: {diagnosis};;;"

        user_message += f"Pet History: {conversation}"

        return self.call_openai_chat(system_message, user_message)

    def generate_record(self, diagnosis: list[str], conversation: str, lab_pdf: str) -> str:
        
        system_message = "Generate a medical record that includes summary of pet's patient history, potential differentials, selected diagnosis and treatment plan."
        user_message = ""

        user_message += f"Pet History: {conversation}"
        if lab_pdf:
            user_message += f"Lab PDF: {lab_pdf}"
        for diagnosis in diagnosis:
            user_message += f"Veterinary selected diagnoses: {diagnosis};;;"

        return self.call_openai_chat(system_message, user_message)
