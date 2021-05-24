from flask import Flask, render_template, request, Markup
import requests
import config
import pickle
import io
import numpy as np

model_path = 'model\XGBoost.pkl'
model = pickle.load(open(model_path, 'rb'))

def get_city(city):                                                      
    
    api_key = config.weather_api_key
    base_url = "https://pro.openweathermap.org/data/2.5/forecast/climate?"            

    complete_url = base_url + "q=" + city + "&appid=" + api_key
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["list"]
        z =y[0].temp.day
        q =y[0].temp.night

        temp = round(( ((z+q)/2) - 273.15), 2)
        humi = y[0].humidity
        return temp, humi
    else:
        return None



app = Flask(__name__)

# render home page


@ app.route('/')
def home():
    title = 'Harvestify - Home'
    return render_template('index.html', title=title)

# render crop recommendation form page


@ app.route('/crop-recommend')
def crop_recommend():
    title = 'Harvestify - Crop Recommendation'
    return render_template('crop.html', title=title)



@ app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    title = 'Harvestify - Crop Recommendation'

    if request.method == 'POST':
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['pottasium'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        # state = request.form.get("stt")
        city = request.form.get("city")

        if fetch(city) != None:
            temperature, humidity = fetch(city)
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            my_prediction = model.predict(data)
            final_prediction = my_prediction[0]

            return render_template('crop-result.html', prediction=final_prediction, title=title)

        else:

            return render_template('try_again.html', title=title)



