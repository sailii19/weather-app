from flask import Flask, render_template, request
from config import API_KEY
import requests
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

#initial values unknown and hence set to None
    data = None
    temperature = None
    feels_like = None
    humidity = None
    description = None
    wind_speed = None
    city_name = None
    error = None
    icon = None

    if request.method == 'POST':
        print("Inside POST")
        city = request.form['city']
        
        # You can add API call here to fetch weather data for the city
        URL = "https://api.openweathermap.org/data/2.5/weather"
        params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

        response = requests.get(URL, params=params)
        print("Status Code:", response.status_code)
        data = response.json()
        print(data)

        if response.status_code == 200:
            temperature = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            wind_speed = data['wind']['speed']
            city_name = data['name']
            icon = data['weather'][0]['icon']
        else:
            error = "City not found. Please enter a valid city."

    return render_template(
    "index.html",
    temperature=temperature,
    feels_like=feels_like,
    humidity=humidity,
    description=description,
    wind_speed=wind_speed,
    city_name=city_name,
    error = error,
    icon = icon
)

if __name__ == "__main__":
    app.run(debug=True)


