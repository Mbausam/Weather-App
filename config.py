import os
import streamlit as st

def get_api_key():
    """Get API key from Streamlit secrets or environment"""
    try:
        # First try Streamlit secrets (for cloud)
        if hasattr(st, 'secrets') and 'OPENWEATHER_API_KEY' in st.secrets:
            return st.secrets['OPENWEATHER_API_KEY']
        # Then try environment variable (for local)
        return os.getenv('OPENWEATHER_API_KEY', "60ddbc0e93f0a38fc9dc988c6f3e1079")
    except:
        return "60ddbc0e93f0a38fc9dc988c6f3e1079"  # Fallback

class Config:
    # OpenWeatherMap API configuration
    OPENWEATHER_API_KEY = get_api_key()
    BASE_URL = "http://api.openweathermap.org/data/2.5"
    
    # App configuration
    DEFAULT_CITY = "London"
    TEMP_UNIT = "metric"