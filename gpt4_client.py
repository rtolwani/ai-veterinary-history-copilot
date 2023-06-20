import openai
from typing import List
import os
import streamlit as st

MODEL = "gpt-4"


class GPT4Client:
    def __init__(self):
        ## get api key from os environ ['OPENAI_API_KEY']
        ## first check if we can get it from os environ (running locally)
        if os.environ.get('OPENAI_API_KEY') is not None:
            openai.api_key = os.environ.get('OPENAI_API_KEY')
        else:
            openai.api_key = st.secrets['OPENAI_API_KEY']


    def call_openai_chat(system_message: str, user_message: str) -> str:

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
        
        system_message = "Generate a medical history for this patient in SOAP Format based on the following conversation between a vet and a client."
        user_message = conversation

        return self.call_openai_chat(system_message, user_message)

    def generate_diagnoses(self, conversation: str) -> List[str]:
        
        system_message = "Generate a list of potential diagnoses based on the following conversation between a vet and a client. Format it so that each diagnoses is separated by a newline, and don't include any other information."
        user_message = conversation

        return self.call_openai_chat(system_message, user_message).split("\n")

    def generate_treatment(self, diagnosis: str, conversation: str) -> str:
        
        system_message = "Generate a treatment plan based on the diagnosis and the following conversation between a vet and a client."
        user_message = f"Diagnosis: {diagnosis};;; Conversation: {conversation}"

        return self.call_openai_chat(system_message, user_message)
