from flask import Flask, render_template, request
import requests
import sys

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/add', methods=['POST', 'GET'])
def add_city():
    if request.method == "POST":
        api_key = "ead8dfd8231f8909a187d06659fa62bf"
        city_name = request.form["city_name"]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
        temp_in_the_city = round(requests.get(url).json()["main"]["temp"])
        dict_with_weather_info = {"city_name": city_name.upper(), "temp": temp_in_the_city}
        return render_template('index.html', dict_with_weather_info=dict_with_weather_info)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
