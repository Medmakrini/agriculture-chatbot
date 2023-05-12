from flask import Flask, request , json
from Chat_Reply_EN import Predict_Plant_En , ask_agriculture_expert_En ,recognize_audio_En
from Chat_Reply_FR import Predire_Plante_Fr , demander_expert_agriculture_Fr ,reconnaitre_audio_Fr
from Chat_Reply_AR import Predire_Plante_AR , demander_expert_agriculture_AR ,reconnaitre_audio_AR
import base64
from tensorflow import keras
import numpy as np
import cv2 
import os
model =keras.models.load_model('MN_TL.h5')

# Initialize Flask app
app = Flask(__name__)


# Define endpoint for chatbot
@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_input = request.json["text"]
    lang = request.json["languge"]
    if(lang=='en'):
        response = ask_agriculture_expert_En(user_input)
    if(lang=='fr'):
        response = demander_expert_agriculture_Fr(user_input)
    if(lang=='ar'):
        response = demander_expert_agriculture_AR(user_input)

    return {"response": response}



# Define endpoint for chatbotPred
@app.route("/chatbotPred", methods=["POST"])
def chatbotPred():
    lang = request.json["languge"]
    temperature = request.json["temperature"]
    humidity = request.json["humidity"]
    ph = request.json["ph"]
    rainfall = request.json["rainfall"]

    if(lang=='en'):
        response = Predict_Plant_En(temperature, humidity, ph, rainfall)
    if(lang=='fr'):
        response = Predire_Plante_Fr(temperature, humidity, ph, rainfall)
    if(lang=='ar'):
        response = Predire_Plante_AR(temperature, humidity, ph, rainfall)

    return {"Predection": response}

# Define endpoint for chatbotAud
@app.route("/chatbotAudio", methods=["POST"])
def chatbotAudio():
    lang = request.json["languge"]
    audio_base64 = request.json['string']

    if(lang=='en'):
        text = recognize_audio_En(audio_base64)
        response = ask_agriculture_expert_En(text)

    if(lang=='fr'):
        text = reconnaitre_audio_Fr(audio_base64)
        response = demander_expert_agriculture_Fr(text)
    if(lang=='ar'):
        text = reconnaitre_audio_AR(audio_base64)
        response = demander_expert_agriculture_AR(text)

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