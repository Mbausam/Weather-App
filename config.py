import os
from dotenv import load_dotenv
from pathlib import Path

# Get the absolute path to the .env file
env_path = Path('.') / '.env'

# Load environment variables from .env file using absolute path
load_dotenv(dotenv_path=env_path)

class Config:
    # OpenWeatherMap API configuration
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    BASE_URL = "http://api.openweathermap.org/data/2.5"
    
    # App configuration
    DEFAULT_CITY = "London"
    TEMP_UNIT = "metric"  # metric for Celsius, imperial for Fahrenheit

# Debug print
print(f"DEBUG: API Key loaded = {Config.OPENWEATHER_API_KEY is not None}")