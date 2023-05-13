import openai
import speech_recognition as sr
import numpy as np
from os import path

openai.api_key = "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"

#FR version Prédire la Plante
def Predire_Plante_Fr(temperature, humidite, ph, pluie):
    prompt =f"En tant que spécialiste de l'agriculture, votre tâche consiste à fournir une liste d'espèces végétales qui conviennent le mieux à un ensemble de conditions environnementales : \n-Température : {temperature}\n-Humidité : {humidite}\n-PH : {ph}\n-Précipitations : {pluie}\n.Votre réponse doit inclure une espèce végétale la plus adaptée à ces conditions en fonction de leurs préférences et exigences connues. Veuillez noter que votre réponse doit être concise et précise et courte. \nRéponse : "
    reponse = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
        presence_penalty=0.6,
        frequency_penalty=0.6,
    )

    reponse_texte = reponse.choices[0].text.strip()
    if not reponse_texte:
        reponse_texte = "Je suis désolé, je ne connais pas la réponse à cela. Puis-je vous aider avec autre chose ?"

    return reponse_texte

#FR version expert en agriculture
def demander_expert_agriculture_Fr(q):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Votre nom est Aggie. Vous êtes un spécialiste agricole. Votre tâche est de fournir des réponses concises et précises uniquement liées à l'agriculturenaux ou au mathématiques.Si une question porte sur un sujet différent,veuillez accepter nos excuses,mais vous devez vous abstenir d'y répondre. Concentrez-vous uniquement sur le partage de vos connaissances et de vos connaissances agricoles."},
            {"role": "user", "content": q},
        ],
        max_tokens=250,
        temperature=0.7,
    )

    answer = response.choices[0].message.content
    if not answer:
        answer = "Je suis désolé, je ne connais pas la réponse à cela. Puis-je vous aider avec autre chose ?"

    return answer

#FR version Audio

def reconnaitre_audio_Fr(wav_path):
        r = sr.Recognizer()
        with sr.WavFile(wav_path) as source:  # use "test.wav" as the audio source
            audio = r.record(source)  # extract audio data from the file
            try:
                text = r.recognize_google(audio, language='fr-FR')  # generate a list of possible transcription#
            except sr.UnknownValueError:
                return "Pardon je n'ai pas bien compris, réessaye"
            except r.RequestError:
                return "Pardon je n'ai pas bien compris, réessaye"
            return text
