import openai
from typing import List
import os
import streamlit as st

MODEL = "gpt-4"

class GPT4Client:
    def __init__(self):
        ## get api key from os environ ['OPENAI_API_KEY']
        openai.api_key = st.secrets['OPENAI_API_KEY']


    def generate_patient_history(self, conversation: str) -> str:

        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Generate a medical history for this patient in SOAP Format based on the following conversation between a vet and a client."},
                {"role": "user", "content": conversation},
            ],
            temperature=1,
        )

        patient_output = response['choices'][0]['message']['content']
        return patient_output

    def generate_diagnoses(self, conversation: str) -> List[str]:

        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Generate a list of potential diagnoses based on the following conversation between a vet and a client. Format it so that each diagnoses is separated by a newline, and don't include any other information."},
                {"role": "user", "content": conversation},
            ],
            temperature=1,
        )

        diagnoses = response['choices'][0]['message']['content'].split("\n")
        return diagnoses

    def generate_treatment(self, diagnosis: str, conversation: str) -> str:

        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Generate a treatment plan based on the diagnosis and the following conversation between a vet and a client."},
                {"role": "user", "content": f"Diagnosis: {diagnosis};;; Conversation: {conversation}"},
            ],
            temperature=1,
        )

        diagnoses = response['choices'][0]['message']['content']
        return diagnoses
