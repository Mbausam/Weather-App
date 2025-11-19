import requests
import streamlit as st
from config import Config
from datetime import datetime

class WeatherService:
    
    # We now pass 'unit' as an argument to force the cache to refresh when units change
    @staticmethod
    @st.cache_data(ttl=600)
    def get_weather_data(city_name, unit):
        try:
            url = f"{Config.BASE_URL}/weather"
            params = {
                'q': city_name,
                'appid': Config.OPENWEATHER_API_KEY,
                'units': unit,
                'lang': 'en'
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            return {'cod': response.status_code, 'message': response.json().get('message')}
        except requests.exceptions.RequestException:
            return None

    @staticmethod
    @st.cache_data(ttl=600)
    def get_weather_by_coords(lat, lon, unit):
        try:
            url = f"{Config.BASE_URL}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': Config.OPENWEATHER_API_KEY,
                'units': unit,
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

    @staticmethod
    @st.cache_data(ttl=600)
    def get_forecast_data(city_name, unit):
        try:
            url = f"{Config.BASE_URL}/forecast"
            params = {
                'q': city_name,
                'appid': Config.OPENWEATHER_API_KEY,
                'units': unit,
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception:
            return None

    @staticmethod
    def parse_weather_data(data):
        if not data or 'main' not in data:
            return None
        
        sys = data.get('sys', {})
        coord = data.get('coord', {})
        sunrise = datetime.fromtimestamp(sys.get('sunrise', 0)).strftime('%H:%M')
        sunset = datetime.fromtimestamp(sys.get('sunset', 0)).strftime('%H:%M')
        
        return {
            'city': data.get('name'),
            'country': sys.get('country'),
            'lat': coord.get('lat'),
            'lon': coord.get('lon'),
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'description': data['weather'][0]['description'].title(),
            'icon': data['weather'][0]['icon'],
            'wind_speed': data.get('wind', {}).get('speed', 0),
            'clouds': data.get('clouds', {}).get('all', 0),
            'sunrise': sunrise,
            'sunset': sunset
        }

    @staticmethod
    def parse_forecast_data(data):
        if not data or 'list' not in data:
            return None
            
        temps = []
        times = []
        for item in data['list'][:8]:
            temps.append(item['main']['temp'])
            times.append(datetime.fromtimestamp(item['dt']).strftime('%H:%M'))
            
        return {'times': times, 'temperatures': temps}