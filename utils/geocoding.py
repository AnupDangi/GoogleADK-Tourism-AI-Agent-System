"""
Geocoding utility using Nominatim API
"""
import requests
import time

def get_coordinates(place):
    """
    Get coordinates (latitude, longitude) for a place using Nominatim API
    
    Args:
        place: Name of the place/city
        
    Returns:
        tuple: (latitude, longitude) or None if not found
    """
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": place,
            "format": "json",
            "limit": 1
        }
        
        headers = {
            "User-Agent": "Tourism-AI-Agent/1.0"  # Required by Nominatim
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data:
            result = data[0]
            lat = float(result.get("lat", 0))
            lon = float(result.get("lon", 0))
            return (lat, lon)
        else:
            return None
            
    except requests.RequestException as e:
        print(f"Geocoding API error: {e}")
        return None
    except Exception as e:
        print(f"Error getting coordinates: {e}")
        return None
    finally:
        # Be polite to Nominatim API - rate limiting
        time.sleep(1)


