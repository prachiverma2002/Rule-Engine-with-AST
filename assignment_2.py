import requests
import time
from collections import defaultdict

API_KEY = "a3eabc018adbcd5cd58395001747a53f"  
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {city}")
        return None


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


# Store weather summaries for each city
daily_summaries = defaultdict(lambda: {'temps': [], 'conditions': []})

def process_weather_data(city, weather_data):
    temp = kelvin_to_celsius(weather_data['main']['temp'])
    condition = weather_data['weather'][0]['main']
    daily_summaries[city]['temps'].append(temp)
    daily_summaries[city]['conditions'].append(condition)

def calculate_daily_summary(city):
    temps = daily_summaries[city]['temps']
    avg_temp = sum(temps) / len(temps) if temps else 0
    max_temp = max(temps, default=0)
    min_temp = min(temps, default=0)
    
    # Dominant weather condition (mode)
    dominant_condition = max(set(daily_summaries[city]['conditions']), key=daily_summaries[city]['conditions'].count)
    
    return {
        'avg_temp': avg_temp,
        'max_temp': max_temp,
        'min_temp': min_temp,
        'dominant_condition': dominant_condition
    }

class WeatherAlert:
    def __init__(self, threshold_temp):
        self.threshold_temp = threshold_temp
        self.alert_triggered = False

    def check_alert(self, city):
        if len(daily_summaries[city]['temps']) < 2:
            return  # Not enough data to trigger alert

        # Check the last two temperatures
        if (daily_summaries[city]['temps'][-1] > self.threshold_temp and 
            daily_summaries[city]['temps'][-2] > self.threshold_temp):
            self.alert_triggered = True
            print(f"ALERT: Temperature in {city} exceeded {self.threshold_temp}°C for two consecutive updates!")
        else:
            self.alert_triggered = False

def display_summary(city):
    summary = calculate_daily_summary(city)
    print(f"Daily Weather Summary for {city}:")
    print(f"Average Temperature: {summary['avg_temp']:.2f}°C")
    print(f"Maximum Temperature: {summary['max_temp']:.2f}°C")
    print(f"Minimum Temperature: {summary['min_temp']:.2f}°C")
    print(f"Dominant Weather Condition: {summary['dominant_condition']}")
    print()

def run_weather_monitoring():
    alert_system = WeatherAlert(threshold_temp=35)  # Set temperature threshold for alerting
    
    while True:
        for city in cities:
            weather_data = get_weather(city)
            if weather_data:
                process_weather_data(city, weather_data)
                alert_system.check_alert(city)
                display_summary(city)
        
        print("Waiting for next update...\n")
        time.sleep(300)  # Wait 5 minutes between updates

if __name__ == "__main__":
    run_weather_monitoring()
