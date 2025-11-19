import streamlit as st
import plotly.graph_objects as go
from weather_service import WeatherService
from config import Config
import time

# Page configuration - MUST be first command
st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'current_city' not in st.session_state:
    st.session_state.current_city = Config.DEFAULT_CITY
if 'trigger_search' not in st.session_state:
    st.session_state.trigger_search = False
if 'search_city' not in st.session_state:
    st.session_state.search_city = ""

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 1rem;
        color: var(--text-color);
    }
    .weather-card {
        background-color: var(--secondary-background-color);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
    }
    .search-section {
        margin-bottom: 2rem;
    }
    .popular-city-btn {
        width: 100%;
        margin: 2px 0;
    }
</style>
""", unsafe_allow_html=True)

# Apply theme CSS
if st.session_state.theme == 'dark':
    st.markdown("""
    <style>
        :root {
            --text-color: #FAFAFA;
            --border-color: #555;
            --secondary-background-color: #262730;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        :root {
            --text-color: #31333F;
            --border-color: #e6e6e6;
            --secondary-background-color: #f0f2f6;
        }
    </style>
    """, unsafe_allow_html=True)

# Theme toggle function
def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
    st.rerun()

# Function to search for a city
def search_city(city_name):
    st.session_state.search_city = city_name
    st.session_state.trigger_search = True
    st.session_state.current_city = city_name
    st.rerun()

# Function to use common cities as "my location"
def use_my_location():
    search_city("London")  # Default to London for "my location"

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Theme toggle
    theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    theme_text = "Dark Mode" if st.session_state.theme == 'light' else "Light Mode"
    
    if st.button(f"{theme_icon} {theme_text}", use_container_width=True, key="theme_btn"):
        toggle_theme()
    
    st.write("---")
    
    # Temperature unit
    temp_unit = st.radio(
        "Temperature Unit:",
        ["Celsius", "Fahrenheit"],
        index=0,
        key="temp_unit"
    )
    Config.TEMP_UNIT = "metric" if temp_unit == "Celsius" else "imperial"
    
    st.write("---")
    st.header("📍 Quick Locations")
    
    # Common cities as "my location" alternatives
    if st.button("🏠 Use My Location", use_container_width=True, key="location_btn"):
        use_my_location()
    
    st.write("**Popular Cities:**")
    
    # Popular cities in a compact layout
    popular_cities = ["New York", "London", "Tokyo", "Paris", "Sydney", "Dubai"]
    
    # Create 2 columns for the buttons
    col1, col2 = st.columns(2)
    
    for i, city in enumerate(popular_cities):
        with col1 if i % 2 == 0 else col2:
            if st.button(city, key=f"pop_{city}", use_container_width=True):
                search_city(city)

# Main app
st.markdown('<h1 class="main-header">🌤️ Weather App</h1>', unsafe_allow_html=True)
st.write("Get current weather information for any city around the world!")

# Search section with better alignment
st.markdown('<div class="search-section">', unsafe_allow_html=True)

# Use columns for better alignment
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    # The search input - this is now just for display and manual entry
    city_input = st.text_input(
        "Enter city name:",
        placeholder="e.g., London, New York, Tokyo...",
        value=st.session_state.current_city,
        label_visibility="collapsed",
        key="city_input"
    )

with col2:
    # This button triggers a search with the input field value
    if st.button("Get Weather", type="primary", use_container_width=True, key="get_weather_btn"):
        search_city(city_input)

with col3:
    if st.button("Clear", use_container_width=True, key="clear_btn"):
        st.session_state.current_city = ""
        st.session_state.trigger_search = False
        st.session_state.search_city = ""
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Determine which city to search for
city_to_search = ""
if st.session_state.trigger_search:
    city_to_search = st.session_state.search_city
    st.session_state.trigger_search = False  # Reset after use
elif city_input and st.session_state.get('auto_search', False):
    city_to_search = city_input

# Get and display weather data
if city_to_search:
    # Update current city display
    st.session_state.current_city = city_to_search
    
    with st.spinner(f"🌤️ Fetching weather data for {city_to_search}..."):
        weather_data = WeatherService.get_weather_data(city_to_search)
        forecast_data = WeatherService.get_forecast_data(city_to_search)
        
    if weather_data and 'cod' in weather_data and weather_data['cod'] == 200:
        parsed_data = WeatherService.parse_weather_data(weather_data)
        forecast_parsed = WeatherService.parse_forecast_data(forecast_data)
        
        if parsed_data:
            # Header with city and weather icon
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                # Dynamic weather icon
                icon_url = f"http://openweathermap.org/img/w/{parsed_data['icon']}.png"
                st.image(icon_url, width=100)
                
            with col2:
                st.markdown(f"<h2 style='text-align: center; margin: 0;'>{parsed_data['city']}, {parsed_data['country']}</h2>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; font-size: 1.2rem; margin: 0;'>{parsed_data['description']}</p>", unsafe_allow_html=True)
                
            with col3:
                st.metric(
                    label="Temperature",
                    value=f"{parsed_data['temperature']:.1f}°{'C' if temp_unit == 'Celsius' else 'F'}",
                    delta=f"Feels like {parsed_data['feels_like']:.1f}°"
                )
            
            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
            
            # Main weather metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("💧 Humidity", f"{parsed_data['humidity']}%")
                
            with col2:
                st.metric("🔽 Pressure", f"{parsed_data['pressure']} hPa")
                
            with col3:
                st.metric("💨 Wind Speed", f"{parsed_data['wind_speed']} m/s")
                
            with col4:
                st.metric("☁️ Clouds", f"{parsed_data['clouds']}%")
            
            # Sunrise/Sunset and Visibility
            col5, col6, col7 = st.columns(3)
            
            with col5:
                st.metric("🌅 Sunrise", parsed_data['sunrise'])
                
            with col6:
                st.metric("🌇 Sunset", parsed_data['sunset'])
                
            with col7:
                visibility_km = parsed_data['visibility'] / 1000 if parsed_data['visibility'] > 0 else "N/A"
                visibility_text = f"{visibility_km:.1f} km" if isinstance(visibility_km, float) else visibility_km
                st.metric("👁️ Visibility", visibility_text)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Temperature trend chart
            if forecast_parsed:
                st.subheader("📈 Temperature Trend (Next 24 Hours)")
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=forecast_parsed['times'],
                    y=forecast_parsed['temperatures'],
                    mode='lines+markers',
                    name='Temperature',
                    line=dict(color='#FF6B6B', width=3),
                    marker=dict(size=8, color='#FF6B6B')
                ))
                
                fig.update_layout(
                    xaxis_title="Time",
                    yaxis_title=f"Temperature (°{'C' if temp_unit == 'Celsius' else 'F'})",
                    template="plotly_dark" if st.session_state.theme == 'dark' else "plotly_white",
                    height=300,
                    margin=dict(l=20, r=20, t=30, b=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    else:
        error_message = weather_data.get('message', 'Unknown error') if weather_data else 'Network error'
        st.error(f"❌ Could not fetch weather data: {error_message}")
        st.info("💡 Tip: Check if the city name is spelled correctly")

# Display current theme in footer
st.write("---")
current_theme_icon = "🌙" if st.session_state.theme == 'dark' else "☀️"
st.markdown(
    f"<div style='text-align: center; color: gray;'>"
    f"Powered by OpenWeatherMap API • "
    f"Theme: {current_theme_icon} {st.session_state.theme.title()} Mode"
    "</div>", 
    unsafe_allow_html=True
)