from flask_ngrok import run_with_ngrok
from flask import Flask, jsonify
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open("logmodel.pkl", "rb"))

run_with_ngrok(app) ##starts ngrok when the app is running
@app.route("/<int:Age>/<int:SibSp>/<int:Parch>/<float:Fare>/<Gender>/<int:PClass>/<Place>")

def home(Age, SibSp, Parch, Fare, Gender, PClass, Place):
    p = []
    p += [Age, SibSp, Parch, Fare]
    if Gender.casefold() == "m":
        p+=[1]
    else:
        p+=[0]
    
    if PClass == 2:
        p+=[1,0]
    elif PClass == 3:
        p+=[0,1]
    else:
        p+=[0,0]

    if Place.casefold() == "queenstown":
        p+=[1,0]
    elif Place.casefold() == "southampton":
        p+=[0,1]
    else:
     p+=[0,0]

    arr = np.array([p])
    predict = model.predict(arr)

    if predict == [1]:
        result = {"result":"Survived"}
    else:
        result = {"result":"Not Survived"}

    return jsonify(result)

app.run()
