import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from weather_service import WeatherService
from config import Config
import geocoder 

# Page configuration
st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 1. Session State ---
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = None
if 'forecast_data' not in st.session_state:
    st.session_state.forecast_data = None
if 'temp_unit_state' not in st.session_state:
    st.session_state.temp_unit_state = 'metric'

# --- 2. CSS & Theme Logic ---
themes = {
    "light": {
        "bg_color": "#FFFFFF",
        "text_color": "#000000",
        "input_bg": "#E8E8E8",      # Darker gray for better visibility
        "input_text": "#000000",
        "sidebar_bg": "#F0F2F6",
        "card_bg": "#F8F9FA",
        "border": "#999999"         # Stronger border
    },
    "dark": {
        "bg_color": "#0E1117",
        "text_color": "#FFFFFF",
        "input_bg": "#262730",
        "input_text": "#FFFFFF",
        "sidebar_bg": "#262730",
        "card_bg": "#1E1E1E",
        "border": "#3B3C40"
    }
}

current_theme = themes[st.session_state.theme]

st.markdown(f"""
<style>
    /* Main Background */
    .stApp {{
        background-color: {current_theme['bg_color']};
        color: {current_theme['text_color']};
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {current_theme['sidebar_bg']};
    }}
    
    /* General Text */
    h1, h2, h3, p, span, div, label {{
        color: {current_theme['text_color']} !important;
    }}
    
    /* FIX: Input Fields (Make them pop!) */
    .stTextInput input {{
        background-color: {current_theme['input_bg']} !important;
        color: {current_theme['input_text']} !important;
        border: 2px solid {current_theme['border']} !important;
        font-weight: 500;
    }}
    
    /* Button Visibility */
    button {{
        color: {current_theme['text_color']} !important;
        border-color: {current_theme['border']} !important;
    }}

    /* Weather Card */
    .weather-card {{
        background-color: {current_theme['card_bg']};
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid {current_theme['border']};
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. Helper Functions ---

# Determine current unit string for API
def get_unit_string():
    return "metric" if st.session_state.temp_unit_state == "Celsius" else "imperial"

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

def fetch_weather_by_city(city_name):
    unit = get_unit_string()
    with st.spinner(f"🌤️ Fetching weather for {city_name}..."):
        w_data = WeatherService.get_weather_data(city_name, unit)
        f_data = WeatherService.get_forecast_data(city_name, unit)
        if w_data and w_data.get('cod') == 200:
            st.session_state.weather_data = w_data
            st.session_state.forecast_data = f_data
        else:
            st.error("City not found. Please check the spelling.")

def fetch_weather_by_coords(lat, lon):
    unit = get_unit_string()
    with st.spinner("📍 Locating you..."):
        w_data = WeatherService.get_weather_by_coords(lat, lon, unit)
        if w_data:
            f_data = WeatherService.get_forecast_data(w_data['name'], unit)
            st.session_state.weather_data = w_data
            st.session_state.forecast_data = f_data

def use_my_location():
    g = geocoder.ip('me')
    if g.latlng:
        fetch_weather_by_coords(g.latlng[0], g.latlng[1])
    else:
        st.error("Could not determine location.")

# --- 4. Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    btn_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    btn_text = "Dark Mode" if st.session_state.theme == 'light' else "Light Mode"
    
    if st.button(f"{btn_icon} {btn_text}", use_container_width=True):
        toggle_theme()
        st.rerun()
        
    st.write("---")
    
    # Temperature Unit Radio
    # We rely on session state directly here to trigger updates
    temp_mode = st.radio(
        "Temperature Unit:", 
        ["Celsius", "Fahrenheit"], 
        index=0 if st.session_state.temp_unit_state == 'Celsius' else 1,
        key="temp_unit_radio"
    )
    
    # Check if unit changed, if so, update state and refresh data if city is selected
    if temp_mode != st.session_state.temp_unit_state:
        st.session_state.temp_unit_state = temp_mode
        # If we already have a city loaded, re-fetch with new unit
        if st.session_state.weather_data:
            city = st.session_state.weather_data['name']
            fetch_weather_by_city(city)
        st.rerun()

    st.write("---")
    st.header("📍 Quick Locations")
    
    if st.button("🏠 Use My Location", use_container_width=True):
        use_my_location()
        
    st.write("**Popular Cities:**")
    popular_cities = ["New York", "London", "Tokyo", "Paris", "Sydney", "Dubai"]
    col1, col2 = st.columns(2)
    for i, city in enumerate(popular_cities):
        with col1 if i % 2 == 0 else col2:
            if st.button(city, key=f"pop_{city}", use_container_width=True):
                fetch_weather_by_city(city)

# --- 5. Main UI ---
st.markdown('<h1 style="text-align:center;">🌤️ Weather App</h1>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    city_input = st.text_input("Enter city name", placeholder="e.g., Nairobi", label_visibility="collapsed")
with col2:
    if st.button("Search", type="primary", use_container_width=True):
        if city_input:
            fetch_weather_by_city(city_input)
with col3:
    if st.button("Clear", use_container_width=True):
        st.session_state.weather_data = None
        st.session_state.forecast_data = None
        st.rerun()

# Display Data
if st.session_state.weather_data:
    w_data = WeatherService.parse_weather_data(st.session_state.weather_data)
    f_data = WeatherService.parse_forecast_data(st.session_state.forecast_data)
    
    # Determine Unit Label
    unit_label = "°C" if st.session_state.temp_unit_state == "Celsius" else "°F"
    speed_label = "m/s" if st.session_state.temp_unit_state == "Celsius" else "mph"
    
    if w_data:
        # Header
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.image(f"http://openweathermap.org/img/w/{w_data['icon']}.png", width=100)
        with col2:
            st.markdown(f"<h2 style='text-align: center; margin:0'>{w_data['city']}, {w_data['country']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-size: 1.2rem;'>{w_data['description']}</p>", unsafe_allow_html=True)
        with col3:
            st.metric("Temp", f"{w_data['temperature']:.1f}{unit_label}", delta=f"Feels: {w_data['feels_like']:.1f}{unit_label}")
        
        # Weather Card
        st.markdown('<div class="weather-card">', unsafe_allow_html=True)

        row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
        row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)

        row1_col1.metric("💧 Humidity", f"{w_data['humidity']}%")
        row1_col2.metric("🔽 Pressure", f"{w_data['pressure']} hPa")
        row1_col3.metric("💨 Wind", f"{w_data['wind_speed']} {speed_label}")
        row1_col4.metric("☁️ Clouds", f"{w_data['clouds']}%")

        row2_col1.metric("🌅 Sunrise", w_data['sunrise'])
        row2_col2.metric("🌇 Sunset", w_data['sunset'])

        st.markdown('</div>', unsafe_allow_html=True)
        
        # Charts
        if f_data:
            st.subheader("Temperature Trend (24h)")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=f_data['times'], 
                y=f_data['temperatures'],
                mode='lines+markers',
                line=dict(color='#FF6B6B', width=3)
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=current_theme['text_color']),
                xaxis=dict(showgrid=False, title='Time'),
                yaxis=dict(showgrid=True, gridcolor=current_theme['border'], title=f'Temp ({unit_label})'),
                margin=dict(l=20, r=20, t=30, b=20),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)

        # Map
        st.subheader(f"📍 Map of {w_data['city']}")
        map_data = pd.DataFrame({'lat': [w_data['lat']], 'lon': [w_data['lon']]})
        st.map(map_data, zoom=10)