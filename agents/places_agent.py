"""
Child Agent 2: Places Agent
"""
import requests

class PlacesAgent:
    """Agent responsible for fetching tourist places"""
    
    def get_places(self, place, coordinates):
        """Get up to 5 tourist attractions for a place"""
        if not coordinates:
            return None
        
        lat, lon = coordinates
        
        try:
            # Overpass API query to find tourist attractions
            overpass_url = "https://overpass-api.de/api/interpreter"
            
            # Correct Overpass QL syntax for tourism attractions
            # Query for tourism-related places with names within 10km radius
            # Query nodes first (point features work best with 'around')
            query = f"""[out:json][timeout:25];
(
  node["tourism"]["name"](around:10000,{lat},{lon});
);
out;
"""
            
            # Send query as form data (correct format for Overpass API)
            # Overpass API expects the query in 'data' parameter
            response = requests.post(overpass_url, data={"data": query}, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Check for Overpass API errors in response
            if "remark" in data and "error" in data["remark"].lower():
                print(f"Overpass API error: {data.get('remark')}")
                return None
            if "elements" not in data:
                print(f"Unexpected response structure: {data}")
                return None
            
            places = []
            elements = data.get("elements", [])
            
            # Collect unique place names (up to 5)
            seen_names = set()
            for element in elements:
                if len(places) >= 5:
                    break
                    
                tags = element.get("tags", {})
                name = tags.get("name")
                tourism_type = tags.get("tourism", "")
                
                # Filter for relevant tourist attractions with names
                # Accept any tourism type that has a name (since we're already filtering by tourism tag)
                if name and tourism_type:
                    if name not in seen_names:
                        places.append(name)
                        seen_names.add(name)
            
            if places:
                places_list = "\n".join([f"- {p}" for p in places])
                return f"In {place} these are the places you can go:\n{places_list}"
            else:
                return f"I couldn't find specific tourist attractions for {place} in the database."
                
        except requests.RequestException as e:
            print(f"Places API error: {e}")
            return None
        except Exception as e:
            print(f"Error getting places: {e}")
            return None


