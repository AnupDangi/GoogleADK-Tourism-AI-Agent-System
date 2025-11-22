"""
Child Agent 1: Weather Agent
"""
import requests

class WeatherAgent:
    """Agent responsible for fetching weather information"""
    
    def get_weather(self, place, coordinates):
        """Get current weather for a place"""
        if not coordinates:
            return None
        
        lat, lon = coordinates
        
        try:
            # Open-Meteo API call
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,precipitation_probability",
                "temperature_unit": "celsius",
                "precipitation_unit": "mm"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current", {})
            temp = current.get("temperature_2m", "N/A")
            rain_prob = current.get("precipitation_probability", 0)
            
            return f"In {place} it's currently {temp}°C with a chance of {rain_prob}% to rain."
            
        except requests.RequestException as e:
            print(f"Weather API error: {e}")
            return None
        except Exception as e:
            print(f"Error getting weather: {e}")
            return None


