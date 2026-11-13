import sys
import requests


def get_weather(city_name, api_key):
    base_url ="http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q" : city_name,
        "appid": api_key,
        "units":"metric" 
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data.get("cod") != 200:
            print(f"Error: {data.get('message', 'City not found.')}")
            return

        city = data["name"]
        country = data["sys"][ "country"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        desc = data["weather"][0]["description"].capitalize()


        print(f"\n---Weather in {city}, {country} ---")
        print(f"Temperature: {temp}\u00b0C")
        print(f"condition: {desc}")
        print(f"Humidity: {humidity}%\n")

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")


if __name__ == "__main__":
    API_KEY =input("Enter your OpenWeatherMap API Key: ").strip()
    city = input("Enter the city name: ").strip()


    if API_KEY and city:
        get_weather(city, API_KEY)
    else:
        print("API key and city name cannot be empty.")