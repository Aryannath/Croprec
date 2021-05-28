from re import search
from flask import Flask, render_template, request 
import requests
import config
import pickle
import io
import numpy as np

model_path = 'model\XGBoost.pkl'             # 'model\XGBoost.pkl'
model = pickle.load(open(model_path, 'rb'))

def get_city(city):                                                      
    
    api_key = config.weather_api_key
    base_url = "https://api.openweathermap.org/data/2.5/forecast?"            

    complete_url = base_url + "q=" + city + "&appid=" + api_key        #city
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["list"]
        t1 =  ((y[7].main.temp + y[14].main.temp + y[21].main.temp + y[28].main.temp+y[35].main.temp)/5)
        h1 =  ((y[7].main.humidity+ y[14].main.humidity + y[21].main.humidity + y[28].main.humidity+y[35].main.humidity)/5)

        temp = round (( t1 - 273.15), 2)
        humi = h1
        return temp, humi
    else:
        return None

 

 
 

app = Flask(__name__)



# render home page


@ app.route('/')
def home():
    title = 'SoilUp Home page'
    return render_template('index.html', title=title) #this title can be used in the front end from here the backend

# render crop recommendation form page


@ app.route('/city', methods=['GET','POST']) #maybe a herf should be used 
def city():
        #if request.method == "GET": 
         cityy = request.args.get("city")   #state = request.form.get("stt") ,,this is not used because we don't need home state
        # return render_template('test.html' , ci=cityy) 
         return render_template('city.html' ,ci=cityy)  

@ app.route('/crop-recommend', methods=['POST']) #this slash is like the slash we have in an web URL
def crop_recommend():
    title = 'SoilUp - Crop Rec'
    return render_template('lab.html', title=title)


@ app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    title = 'SoilUp - Crop Pred'
    
   
   
    if request.method == 'POST':
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['pottasium'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])
        

        

        if get_city(cityy) != None:
            temp, humi = get_city(cityy)
            data = np.array([[N, P, K, temp, humi, ph, rainfall]])
            my_prediction = model.predict(data)
            final_prediction = my_prediction[0]

            return render_template('result.html', prediction=final_prediction, title=title)

        else:

            return render_template('try_again.html', title=title)


if __name__ == '__main__':
    app.run(debug=True)
