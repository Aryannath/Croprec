from re import search
from flask import Flask, render_template, request ,session
import requests
import config
import pickle
import numpy as np



model_path = 'model\XGBoost.pkl'             # file se lega
model = pickle.load(open(model_path, 'rb'))

def get_city(city):                                                      
    
    api_key = config.weather_api_key
    base_url = "https://api.openweathermap.org/data/2.5/forecast?"            

    complete_url = base_url + "q=" + city + "&appid=" + api_key        
    response = requests.get(complete_url)
    x = response.json()

    if  x["cod"] != "404":
        y = x["list"]
        
        temp = round (( ((y[7]['main']['temp'] + y[14]['main']['temp'] + y[21]['main']['temp'] + y[28]['main']['temp']+y[35]['main']['temp'])/5) - 273.15), 2)
        humi = ((y[7]['main']['humidity']+ y[14]['main']['humidity'] + y[21]['main']['humidity'] + y[28]['main']['humidity']+y[35]['main']['humidity'])/5)
        return temp, humi
    else:
        
        return None

 

 
 

app = Flask(__name__)
app.secret_key = "hello"


# render home page


@ app.route('/')
def home():
    title = 'SoilUp Home page'
    return render_template('index.html') #this title can be used in the front end from here the backend

# render crop recommendation form page


@ app.route('/city', methods=['GET']) #maybe a herf should be used 
def city():
       # if request.method == "GET": 
        #state = request.form.get("stt") ,,this is not used because we don't need home state
        # return render_template('test.html' , ci=cityy) 
        return render_template('city.html')     # cityy ke andr data hi nhi ara hai shyd this is due to request method post

@ app.route('/crop-recommend', methods=['GET','POST']) #this slash is like the slash we have in an web URL
def crop_recommend():
    
    
     
    session["op"]= request.args.__getitem__("city") # collecting and passinfg the city from the brower link which we got from the "get" method
    

    return render_template('lab.html')


@ app.route('/crop-predict', methods=['POST'])
def crop_prediction():
   
    
   
   
    if request.method == 'POST':               
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['pottasium'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])
        

       
        
        citu = session["op"]  #temporary test variable to test session variable


        if get_city(citu)!= None:
            temp, humi = get_city(citu)
            data = np.array([[N, P, K, temp, humi, ph, rainfall]])
            my_prediction = model.predict(data)
            final_prediction = my_prediction[0]

            return render_template('result.html', prediction=final_prediction)

        else:

            return render_template('try_again.html')


if __name__ == '__main__':
    app.run(debug=True)
