from flask import Flask, flash, redirect, render_template, request
from db_connection import add_city_to_db, is_city_in_db, all_cities, delete_city
from sqlalchemy.ext.declarative import declarative_base

import requests
import sys

app = Flask(__name__)
app.config.from_object('settings')
api_key = "ead8dfd8231f8909a187d06659fa62bf"


@app.route('/', methods=['POST', 'GET'])
def main_page():
    cities = all_cities()
    if cities:
        dict_with_weather_info = {}
        for city in cities:
            city_name, city_id = city.name, city.id
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
            temp_in_the_city = round(requests.get(url).json()["main"]["temp"])
            dict_with_weather_info[city_name.upper()] = {"temp": temp_in_the_city, "id": city_id}

        return render_template('index.html', dict_with_weather_info=dict_with_weather_info)
    return render_template('index.html')


@app.route("/add", methods=["POST"])
def add():
    if request.method == "POST":
        city_name = request.form["city_name"]
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
            temp_in_the_city = round(requests.get(url).json()["main"]["temp"])
        except KeyError:
            flash("The city doesn't exist!")
            return redirect("/")
        else:
            if is_city_in_db(city_name):
                flash("The city has already been added to the list!")
                return redirect("/")
            else:
                add_city_to_db(city_name)
                return redirect("/")


@app.route("/delete/<city_id>", methods=["POST", "GET"])
def delete(city_id):
    delete_city(city_id)
    return redirect("/")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
