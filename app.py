from flask import Flask, request, render_template_string
import datetime
import logging
import requests

app = Flask(__name__)
PORT = 5000

# Logger
logging.basicConfig(level=logging.INFO)
logging.info(f"Aplikacja uruchomiona {datetime.datetime.now()}, Autor: Emil Los, Port: {PORT}")

# Klucz API do OpenWeatherMap
API_KEY = '97dd91235059d8c078f4a153519a99bf'

# Predefiniowana lista krajów i miast
cities = {
    "Polska": ["Warszawa", "Kraków"],
    "USA": ["New York", "San Francisco"]
}

# OpenWeatherMap
def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            temp = data['main']['temp']
            return f"Aktualna temperatura w {city}: {temp}°C"
        else:
            return "Błąd: Nie udało się pobrać danych pogodowych."
    except Exception as e:
        return f"Błąd: {str(e)}"

html_template = '''
    <form method="POST">
        <label>Kraj:</label>
        <select name="country">
            {% for country in cities %}
                <option value="{{ country }}" {% if country == selected_country %}selected{% endif %}>{{ country }}</option>
            {% endfor %}
        </select>
        <label>Miasto:</label>
        <select name="city">
            {% for city in cities[selected_country] %}
                <option value="{{ city }}">{{ city }}</option>
            {% endfor %}
        </select>
        <input type="submit" value="Sprawdź pogodę">
    </form>
    {% if weather %}
        <h3>Pogoda: {{ weather }}</h3>
    {% endif %}
'''

@app.route("/", methods=["GET", "POST"])
def index():
    weather = ""
    selected_country = "Polska"
    if request.method == "POST":
        selected_country = request.form["country"]
        city = request.form["city"]
        weather = get_weather(city)
    return render_template_string(html_template, weather=weather, cities=cities, selected_country=selected_country)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
