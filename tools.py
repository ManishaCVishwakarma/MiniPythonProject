# tools.py - Tools for the agent
import requests

def get_current_weather(city: str) -> str:
    """
    Get current weather for a city using free Open-Meteo API
    """
    try:
        # Get coordinates
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_response = requests.get(
            geo_url, 
            params={'name': city, 'count': 1, 'format': 'json'},
            timeout=10
        )
        
        if geo_response.status_code != 200:
            return f"ERROR: Could not fetch coordinates for {city}"
        
        geo_data = geo_response.json()
        if not geo_data.get('results'):
            return f"ERROR: City '{city}' not found"
        
        loc = geo_data['results'][0]
        lat, lon, city_name = loc['latitude'], loc['longitude'], loc['name']
        
        # Get weather data
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_response = requests.get(
            weather_url,
            params={
                'latitude': lat,
                'longitude': lon,
                'current_weather': True,
                'hourly': 'relativehumidity_2m',
                'timezone': 'auto'
            },
            timeout=10
        )
        
        if weather_response.status_code != 200:
            return f"ERROR: Could not get weather data for {city}"
        
        weather_data = weather_response.json()
        
        if 'current_weather' not in weather_data:
            return f"ERROR: No weather data available for {city}"
        
        current = weather_data['current_weather']
        
        # Get humidity
        humidity = 'N/A'
        if 'hourly' in weather_data and 'relativehumidity_2m' in weather_data['hourly']:
            if weather_data['hourly']['relativehumidity_2m']:
                humidity = weather_data['hourly']['relativehumidity_2m'][0]
        
        # Weather code mapping
        code_map = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Light rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Light snow",
            73: "Moderate snow",
            75: "Heavy snow",
            95: "Thunderstorm"
        }
        
        condition = code_map.get(current['weathercode'], "Unknown")
        
        return f"{city_name}: {condition}, Temperature: {current['temperature']}°C, Humidity: {humidity}%"
        
    except Exception as e:
        return f"ERROR: {str(e)}"

def get_weather_forecast(city: str, days: int = 3) -> str:
    """
    Get weather forecast for a city
    """
    try:
        # Get coordinates
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_response = requests.get(
            geo_url,
            params={'name': city, 'count': 1, 'format': 'json'},
            timeout=10
        )
        
        if geo_response.status_code != 200:
            return f"ERROR: Could not fetch coordinates for {city}"
        
        geo_data = geo_response.json()
        if not geo_data.get('results'):
            return f"ERROR: City '{city}' not found"
        
        loc = geo_data['results'][0]
        lat, lon, city_name = loc['latitude'], loc['longitude'], loc['name']
        
        # Get forecast
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_response = requests.get(
            weather_url,
            params={
                'latitude': lat,
                'longitude': lon,
                'daily': 'temperature_2m_max,temperature_2m_min,weathercode',
                'forecast_days': days
            },
            timeout=10
        )
        
        if weather_response.status_code != 200:
            return f"ERROR: Could not get forecast for {city}"
        
        data = weather_response.json()
        
        if 'daily' not in data:
            return f"ERROR: No forecast data available for {city}"
        
        daily = data['daily']
        
        # Weather code mapping
        code_map = {
            0: "Clear",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            51: "Drizzle",
            61: "Rain",
            71: "Snow",
            95: "Thunderstorm"
        }
        
        forecast_data = []
        for i in range(len(daily['time'])):
            condition = code_map.get(daily['weathercode'][i], "Unknown")
            forecast_data.append(
                f"{daily['time'][i]}: {condition}, High: {daily['temperature_2m_max'][i]}°C, Low: {daily['temperature_2m_min'][i]}°C"
            )
        
        return f"Forecast for {city_name}:\n" + "\n".join(forecast_data)
        
    except Exception as e:
        return f"ERROR: {str(e)}"