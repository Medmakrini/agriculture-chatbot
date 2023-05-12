import openai
import speech_recognition as sr
import numpy as np
import os
import base64
from os import path
import tempfile

openai.api_key = "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"

#EN version Predect Plant
def Predict_Plant_En(temperature, humidity, ph, rainfall):
    prompt =f"As an agricultural specialist, your task is to provide a list of plant species that are best suited for a given set of environmental conditions : \n-Temperature:{temperature}\n-Humidity:{humidity}\n-PH:{ph}\n-Rainfall:{rainfall}\n.Your response should include one plant species that is most suitable for these conditions based on their known preferences and requirements.your answer Must be concise and accurat. \nAnswer: "
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
        presence_penalty=0.6,
        frequency_penalty=0.6,
    )

    answer = response.choices[0].text.strip()
    if not answer:
        answer = "I'm sorry, I don't know the answer to that. Can I help you with anything else?"

    return answer

#EN version agriculture expert

def ask_agriculture_expert_En(q):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Your name is Aggie. You are an agricultural specialist with vast expertise in farming and agriculture. Your task is to provide concise and accurate  answers answers solely related to agriculture ,farming , math or calculation. If a question pertains to a different topic, please accept our apologies, but you must refrain from answering. Focus solely on sharing your agricultural knowledge and insights."},
            {"role": "user", "content": q},
        ],
        max_tokens=150,
        temperature=0.7,
    )

    answer = response.choices[0].message.content
    if not answer:
        answer = "I'm sorry, I don't know the answer to that. Can I help you with anything else?"

    return answer

#EN version Audio
 
def recognize_audio_En(base64_audio, language='en-US'):
    r = sr.Recognizer()
    # Decode base64 audio data
    audio_data = base64.b64decode(base64_audio)
    
    # Save audio data as a temporary WAV file
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(audio_data)
        audio_file = f.name
    
    # Perform speech recognition on the audio file
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio, language=language)
        except sr.UnknownValueError:
            text = ''
    os.unlink(audio_file) # Delete the temporary WAV file
    
    return text































#EN version agriculture expert
# def ask_agriculture_expert_En(question):
#     prompt = f"Your name is Aggie. You are an agricultural specialist, your task is to provide concise and accurate answers related only to agriculture ,farming , math or calculation ,if the question is about something else apologies and you must not answer, this is your Question:{question}\nAnswer: "
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=200,
#         n=1,
#         stop=None,
#         temperature=0.7,
#         presence_penalty=0.6,
#         frequency_penalty=0.6
#     )

#     answer = response.choices[0].text.strip()
#     if not answer:
#         answer = "I'm sorry, I don't know the answer to that. Can I help you with anything else?"

#     return answer






