import requests
from config import Config
from datetime import datetime

class WeatherService:
    @staticmethod
    def get_weather_data(city_name):
        """
        Get current weather data for a city
        """
        try:
            # API endpoint for current weather
            url = f"{Config.BASE_URL}/weather"
            
            # Parameters for the API request
            params = {
                'q': city_name,
                'appid': Config.OPENWEATHER_API_KEY,
                'units': Config.TEMP_UNIT,
                'lang': 'en'
            }
            
            # Make the API request
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    @staticmethod
    def get_weather_by_coords(lat, lon):
        """
        Get weather data by coordinates
        """
        try:
            url = f"{Config.BASE_URL}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': Config.OPENWEATHER_API_KEY,
                'units': Config.TEMP_UNIT,
                'lang': 'en'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data by coords: {e}")
            return None

    @staticmethod
    def get_forecast_data(city_name):
        """
        Get 5-day forecast data for charts
        """
        try:
            url = f"{Config.BASE_URL}/forecast"
            params = {
                'q': city_name,
                'appid': Config.OPENWEATHER_API_KEY,
                'units': Config.TEMP_UNIT,
                'lang': 'en'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast data: {e}")
            return None

    @staticmethod
    def parse_weather_data(weather_data):
        """
        Parse the weather data into a friendly format
        """
        if not weather_data:
            return None
            
        try:
            main = weather_data['main']
            weather = weather_data['weather'][0]
            wind = weather_data.get('wind', {})
            sys = weather_data.get('sys', {})
            
            # Convert sunrise/sunset timestamps
            sunrise = datetime.fromtimestamp(sys.get('sunrise', 0)).strftime('%H:%M') if sys.get('sunrise') else 'N/A'
            sunset = datetime.fromtimestamp(sys.get('sunset', 0)).strftime('%H:%M') if sys.get('sunset') else 'N/A'
            
            parsed_data = {
                'city': weather_data['name'],
                'country': weather_data['sys']['country'],
                'temperature': main['temp'],
                'feels_like': main['feels_like'],
                'humidity': main['humidity'],
                'pressure': main['pressure'],
                'description': weather['description'].title(),
                'icon': weather['icon'],
                'wind_speed': wind.get('speed', 0),
                'visibility': weather_data.get('visibility', 0),
                'sunrise': sunrise,
                'sunset': sunset,
                'clouds': weather_data.get('clouds', {}).get('all', 0)
            }
            
            return parsed_data
            
        except KeyError as e:
            print(f"Error parsing weather data: {e}")
            return None

    @staticmethod
    def parse_forecast_data(forecast_data):
        """
        Parse forecast data for temperature trends
        """
        if not forecast_data or 'list' not in forecast_data:
            return None
            
        try:
            temperatures = []
            times = []
            
            for item in forecast_data['list'][:8]:  # Next 24 hours (3-hour intervals)
                temps = item['main']['temp']
                time_str = datetime.fromtimestamp(item['dt']).strftime('%H:%M')
                temperatures.append(temps)
                times.append(time_str)
                
            return {
                'times': times,
                'temperatures': temperatures
            }
            
        except KeyError as e:
            print(f"Error parsing forecast data: {e}")
            return None