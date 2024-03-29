from flask import Flask, request , json
from Chat_Reply_EN import Predict_Plant_En , ask_agriculture_expert_En ,recognize_audio_En
from Chat_Reply_FR import Predire_Plante_Fr , demander_expert_agriculture_Fr ,reconnaitre_audio_Fr
from Chat_Reply_AR import Predire_Plante_AR , demander_expert_agriculture_AR ,reconnaitre_audio_AR
import base64
from tensorflow import keras
import numpy as np
import cv2 
import os
from os import path
import ffmpeg
import base64
import subprocess

model =keras.models.load_model('MN_TL.h5')

# Initialize Flask app
app = Flask(__name__)


# Define endpoint for chatbot
@app.route("/chatbot", methods=["POST","GET"])
def chatbot():
    user_input = request.json["text"]
    lang = request.json["languge"]
    print(user_input)
    print(lang)
    if(lang=='en'):
        response = ask_agriculture_expert_En(user_input)
        return {"response": response}
    if(lang=='fr'):
        response = demander_expert_agriculture_Fr(user_input)
        return {"response": response}
    if(lang=='ar'):
        response = demander_expert_agriculture_AR(user_input)
        return {"response": response}
    else:
        return {"response": "sorry no network"}




# Define endpoint for chatbotPred
@app.route("/chatbotPred", methods=["POST","GET"])
def chatbotPred():
    lang = request.json["languge"]
    temperature = request.json["temperature"]
    humidity = request.json["humidity"]
    ph = request.json["ph"]
    rainfall = request.json["rainfall"]

    if(lang=='en'):
        response = Predict_Plant_En(temperature, humidity, ph, rainfall)
        return {"Predection": response}
    if(lang=='fr'):
        response = Predire_Plante_Fr(temperature, humidity, ph, rainfall)
        return {"Predection": response}
    if(lang=='ar'):
        response = Predire_Plante_AR(temperature, humidity, ph, rainfall)
        return {"Predection": response}




def decode_base64_string(encoded_string):
    current_dir = path.dirname(path.realpath(__file__))

    audio_path = path.join(current_dir, 'last.3gp')
    wav_path = path.join(current_dir, 'last.wav')

    # Decode the base64 string and write it to the 3GP file
    with open(audio_path, 'wb') as audio_file:
        decode_string = base64.b64decode(encoded_string)
        audio_file.write(decode_string)

    # Convert the 3GP file to WAV using FFmpeg
    cmd = ['ffmpeg', '-i', audio_path, '-f', 'wav', '-acodec', 'pcm_s16le', '-ar', '22050', '-ac', '1', wav_path]
    subprocess.run(cmd, check=True)  # Run the FFmpeg command
    print(" wav_path --------------> ",wav_path)
    return wav_path



# Define endpoint for chatbotAud
@app.route("/chatbotAudio", methods=["POST","GET"])
def chatbotAudio():
    lang = request.json["languge"]
    audio = request.json['string']
    audio_base64 =decode_base64_string(audio)
    if(lang=='en'):
        response = recognize_audio_En(audio_base64)
        print("text recooo===>",response)
        os.remove(path.join(path.dirname(path.realpath(__file__)), 'last.3gp'))
        os.remove('last.wav')
        return {"response": response}
    if(lang=='fr'):
        response = reconnaitre_audio_Fr(audio_base64)
        print("text recooo===>",response)
        os.remove(path.join(path.dirname(path.realpath(__file__)), 'last.3gp'))
        os.remove('last.wav')
        return {"response": response}
    if(lang=='ar'):
        response = reconnaitre_audio_AR(audio_base64)
        print("text recooo===>",response)
        os.remove(path.join(path.dirname(path.realpath(__file__)), 'last.3gp'))
        os.remove('last.wav')
        return {"response": response}



list=["Apple Scab", "Apple Black rot", "Apple Cedar apple rust", 
      "Apple Healthy", "Apple Cedar apple rust", "Blueberry Healthy",
      "Cherry (including sour) Powdery mildew", "Cherry (including sour) Healthy",
      "Corn(maize) Cercospora leaf spot Gray leaf spot", "Corn(maize) Common rust", "Corn(maize) Northern leaf Blight",
      "Corn(maize) Healthy", "Grape Black rot", "Grape Esca (Black Measles)", "Grape Leaf blight (Isariopsis leaf spot)", "Grape Healthy",
      "Orange Huanglongbing (Citrus greening)", "Peach Bacterial spot", "Peach Healthy", "Bell pepper Bacterial pot", "Bell pepper Healthy",
      "Potato Early blight", "Potato Late blight", "Potato Healthy", "Raspberry Healthy", "Soybean Healthy",
      "Squash Powdery mildew", "Strawberry Leaf scorch", "Tomato Bacterial spot", "Tomato Early blight", "Tomato Late blight",
      "Tomato Leaf Mold", "Tomato Septoria leaf spot", "Tomato Spider mites Two spotted spider mite", "'Tomato Target spot'",
      "Tomato Yellow Leaf Curl Virus", "Tomato Mosaic virus", "Tomato Healthy"]

@app.route('/image' ,methods=['POST'])
def image():
    image=request.json['image']
    imgdata = base64.b64decode(image)
    with open("imageToSave.png", "wb") as fh:
        fh.write(imgdata)
    img = cv2.imread("imageToSave.png")
    img = cv2.resize(img,(224,224))
    img = np.reshape(img,[1,224,224,3])

    if model:
        classes = model.predict(img)
        arg = np.argmax(classes,axis=1)
        conf=classes[0][arg]
        classes = np.argmax(classes,axis=1)
        res=list[classes[0]]
        print(conf[0])
        print(res)

        json_str = json.dumps({'res': res,'conf':conf.tolist()})
        os.remove('imageToSave.png')
        return json_str
    else:
        os.remove('imageToSave.png')
        return True




if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))