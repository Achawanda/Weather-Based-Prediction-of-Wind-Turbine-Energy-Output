# -*- coding: utf-8 -*-
import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import requests

app=Flask(__name__)
model=joblib.load('power_prediction.sav')

@app.route('/')
def home():
    return render_template('intro.html')

@app.route('/predict',methods=["GET","POST"])
def predict():
    if request.method == "POST":
        wind_speed = request.form["wind_speed"]
        temperature = request.form["temperature"]
        humidity = request.form["humidity"]
        pressure = request.form["pressure"]

        # prediction logic here
        #return "Prediction done"

    return render_template('predict.html')

@app.route('/windapi', methods=['POST'])
def windapi():
    city = request.form.get('city')
    apikey = "a6889edb39de1df32e6633dcef24c7d9"
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + apikey
    resp = requests.get(url)
    resp = resp.json()
    temp = str(resp["main"]["temp"]) + "°C"
    humid = str(resp["main"]["humidity"]) + " %"
    pressure = str(resp["main"]["pressure"]) + " mmHG"
    speed = str(resp["wind"]["speed"]) + " m/s"
    return render_template('predict.html',temp=temp,humid=humid,pressure=pressure,speed=speed)

@app.route('/y_predict', methods=['POST'])
def y_predict():

    try:
        wind_speed = float(request.form.get("wind_speed", 0))
        temperature = float(request.form.get("temperature", 0))
        humidity = float(request.form.get("humidity", 0))
        pressure = float(request.form.get("pressure", 0))

        x_test = [[wind_speed, temperature, humidity, pressure]]

        prediction = model.predict(x_test)
        output = round(prediction[0], 2)

        return render_template(
            'predict.html',
            prediction_text=f"Predicted Energy: {output} kWh"
        )

    except Exception as e:
        return render_template(
            'predict.html',
            prediction_text="⚠️ Please enter all input values correctly")

       
if __name__ =="__main__":
    app.run(debug=True)

