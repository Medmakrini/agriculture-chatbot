import openai
import speech_recognition as sr
import numpy as np
from os import path
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

#print(ask_agriculture_expert_En('gi'))
#EN version Audio


def recognize_audio_En(wav_path):
      
        r = sr.Recognizer()
        with sr.WavFile(wav_path) as source:  # use "test.wav" as the audio source
            audio = r.record(source)  # extract audio data from the file
            try:
                text = r.recognize_google(audio, language='en-IN')  # generate a list of possible transcription#
            except sr.UnknownValueError:
                 return 'Voice not clear'
            except r.RequestError:
                 return "Sorry, I didn't quite understand, please try again!"
             
            return text
