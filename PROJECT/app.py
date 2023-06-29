import json
import ast
from flask import Flask, render_template, request
import pickle
import numpy as np

#Country Code
with open('./model/countryCode.pkl', 'rb') as file:
    country_code = pickle.load(file)   

#City Mapping
with open('./model/city.pkl','rb') as file:
    city_mapping = pickle.load(file)

#Locality Mapping
with open('./model/locality.pkl', 'rb') as file:
    locality_mapping = pickle.load(file)

#Cuisine Mapping
with open('./model/cuisine.pkl','rb',) as file:
    cuisine_mapping = pickle.load(file)
    
#Country City
with open('./model/countryCity.pkl', 'rb') as file:
    country_city = pickle.load(file)
    
#City Locality
with open('./model/cityLocality.pkl', 'rb') as file:
    city_locality = pickle.load(file)
    
#Locality Cuisine
with open('./model/localityCuisine.pkl', 'rb') as file:
    locality_cuisine = pickle.load(file)
    
countries = list(country_code.keys())
cuisines = list(cuisine_mapping.keys())

with open('./model/model.pkl', 'rb') as file:
    model = pickle.load(file)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', countries=countries, country_city=country_city, city_locality=city_locality, cuisines=cuisines)


@app.route('/submit', methods=['POST'])
def submit():
    country_val = request.form.get("country")
    city = request.form.get("city")
    locality = request.form.get("locality")
    cuisine = request.form.get("cuisine")
    price = int(request.form.get("price"))
    rating = float(request.form.get("rating"))
    votes = int(request.form.get("votes"))
    type = request.form.get("type")
    
    code = country_code[country_val]
    city = city_mapping[city]
    locality = locality_mapping[locality]
    cuisine = cuisine_mapping[cuisine]
    
    dine,delivery = 0,0
    if type == "Dine In":
        dine = 1
    else:
        delivery = 1
    
    
    feed = np.array([[code, city, locality, cuisine, dine, delivery, price, rating, votes]])
    
    result = int(model.predict(feed)[0])
    print(feed, result)      

    return render_template('index.html', answer=result, country_city=country_city, city_locality=city_locality)


if __name__ == "__main__":
    app.run(debug=False)
   
