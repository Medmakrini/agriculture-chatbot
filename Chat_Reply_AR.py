import openai
import speech_recognition as sr
import os
import base64
from os import path
import tempfile

openai.api_key = "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"

#AR version Predect Plant
def Predire_Plante_AR(temperature, humidite, ph, pluie):
    prompt=f"كخبير زراعي، مهمتك هي توفير قائمة بأنواع النباتات التي تتناسب مع الظروف البيئية المحددة:  \n- درجة الحرارة: {temperature}\n- الرطوبة: {humidite}\n- الرقم الهيدروجيني (PH): {ph}\n- الهطول: {pluie}\n. يرجى تزويدي بنوع واحد من النباتات الأكثر ملاءمة لهذه الظروف، استنادًا إلى المتطلبات المعروفة للنباتات في هذه الظروف.يرجى ملاحظة أن إجابتك يجب أن تكون موجزة ودقيقة وقصيرة، حد اقصى 2 اسطر"
    reponse = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=250,
        n=1,
        stop=None,
        temperature=0.7,
        presence_penalty=0.6,
        frequency_penalty=0.6,
    )
    
    reponse_texte = reponse.choices[0].text.strip()
    if not reponse_texte:
        reponse_texte = "عذراً، لا أعرف الإجابة على هذا السؤال. هل يمكنني مساعدتك بأي شيء آخر؟"

    return reponse_texte

#FR version expert en agriculture
def demander_expert_agriculture_AR(q):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": ".اسمك اجي. أنت متخصص زراعي ذو خبرة واسعة في الزراعة. مهمتك هي تقديم إجابات موجزة ودقيقة تتعلق فقط بالزراعة أو الزراعة أو الرياضيات أو الحساب. إذا كان سؤال يتعلق بموضوع مختلف ، فيرجى قبول اعتذارنا ، ولكن يجب الامتناع عن الإجابة. ركز فقط على مشاركة المعرفة والأفكار الزراعية الخاصة بك"},
            {"role": "user", "content": q},
        ],
        max_tokens=200,
        temperature=0.7,
    )

    answer = response.choices[0].message.content
    if not answer:
        answer = "عذراً، لا أعرف الإجابة على هذا السؤال. هل يمكنني مساعدتك بأي شيء آخر؟"


    return answer

#AR version Audio

def reconnaitre_audio_AR(audio_base64, langue='ar-SA'):
    r = sr.Recognizer()
    # Décoder les données audio en base64
    donnees_audio = base64.b64decode(audio_base64)
    
    # Enregistrer les données audio sous forme de fichier WAV temporaire
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(donnees_audio)
        fichier_audio = f.name
    
    # Effectuer une reconnaissance vocale sur le fichier audio
    with sr.AudioFile(fichier_audio) as source:
        audio = r.record(source)
        try:
            texte = r.recognize_google(audio, language=langue)
        except sr.UnknownValueError:
            texte = ''
    os.unlink(fichier_audio) # Supprimer le fichier WAV temporaire
    
    return texte

