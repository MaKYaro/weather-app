from flask import Flask, render_template, request
from db_connection import add_city_to_db, is_city_in_db, all_cities
import requests
import sqlalchemy
import sys

app = Flask(__name__)
api_key = "ead8dfd8231f8909a187d06659fa62bf"


@app.route('/', methods=['POST', 'GET'])
def main_page():
    if request.method == "POST":
        city_name = request.form["city_name"]

        if not is_city_in_db(city_name):
            add_city_to_db(city_name)

    cities = all_cities()
    if cities:
        dict_with_weather_info = {}
        for city in cities:
            city_name = city.name
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
            temp_in_the_city = round(requests.get(url).json()["main"]["temp"])
            dict_with_weather_info[city_name.upper()] = temp_in_the_city

        return render_template('index.html', dict_with_weather_info=dict_with_weather_info)
    return render_template('index.html')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
