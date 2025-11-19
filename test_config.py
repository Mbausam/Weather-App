import os
from dotenv import load_dotenv

print("=== Testing Configuration ===")

# Check if .env file exists
env_path = '.env'
if os.path.exists(env_path):
    print("✅ .env file found")
else:
    print("❌ .env file NOT found")
    print(f"Current directory: {os.getcwd()}")
    print(f"Looking for: {os.path.abspath(env_path)}")

# Try to load environment variables
load_dotenv()

# Check if API key is loaded
api_key = os.getenv('OPENWEATHER_API_KEY')
print(f"API Key from .env: {api_key}")

if api_key and api_key != "your_api_key_here":
    print("✅ API Key loaded successfully!")
else:
    print("❌ API Key NOT loaded")