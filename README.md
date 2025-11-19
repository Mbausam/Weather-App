# 🌤️ WeatherSphere - Intelligent Weather Dashboard

A modern, responsive weather application built with Streamlit that delivers real-time weather insights with beautiful visualizations and intuitive design.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenWeather](https://img.shields.io/badge/OpenWeather-EE6C4D?style=for-the-badge)

## ✨ Features

### 🌍 Global Weather Intelligence
- **Real-time Weather Data** - Accurate current conditions for any city worldwide
- **Multi-location Support** - Quick access to popular global cities
- **Timezone-Aware** - Local sunrise/sunset times for each location

### 🎨 Premium User Experience
- **Dark/Light Theme Toggle** - Seamless theme switching with persistent preferences
- **Responsive Design** - Optimized for desktop, tablet, and mobile devices
- **Interactive Charts** - Beautiful temperature trends using Plotly
- **Dynamic Weather Icons** - Visual weather representations that update in real-time

### 📊 Advanced Analytics
- **24-Hour Forecast** - Temperature trend visualization
- **Comprehensive Metrics** - Humidity, pressure, wind speed, visibility, and cloud coverage
- **Sunrise/Sunset Tracking** - Plan your day with precise daylight information

### 🔧 Smart Features
- **One-Click Geolocation** - Instant weather for your current area
- **Quick City Access** - Pre-configured popular destinations
- **Unit Conversion** - Switch between Celsius and Fahrenheit
- **Error Handling** - Graceful error management with user-friendly messages

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenWeatherMap API key ([Get it free here](https://openweathermap.org/api))

### Installation & Setup

```bash
# Clone the repository
git clone https://github.com/Mbausam/Weather-App.git
cd Weather-App

# Create virtual environment
python -m venv weather_env

# Activate environment (Windows)
weather_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "OPENWEATHER_API_KEY=your_api_key_here" > .env

# Launch the application
streamlit run app.py
