"""
Parent Agent: Tourism AI Agent (Orchestrator)
"""
import google.generativeai as genai
from agents.weather_agent import WeatherAgent
from agents.places_agent import PlacesAgent
from utils.geocoding import get_coordinates
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()
class TourismAIAgent:
    """Main orchestrator agent that coordinates weather and places agents"""
    
    def __init__(self):
        """Initialize the Tourism AI Agent with Google Gemini"""
        # Set up Google Gemini API
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set!")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Initialize child agents
        self.weather_agent = WeatherAgent()
        self.places_agent = PlacesAgent()
    
    def extract_place(self, query):
        """Extract place name from user query using Gemini"""
        prompt = f"""
        Extract the place/city name from this tourism-related query: "{query}"
        
        Return ONLY the place/city name, nothing else. 
        Examples:
        - "I'm going to go to Bangalore" -> Bangalore
        - "What's the weather in Paris?" -> Paris
        - "Tell me about Tokyo" -> Tokyo
        
        If no specific place is mentioned, return "None".
        """
        try:
            response = self.model.generate_content(prompt)
            place = response.text.strip().replace('"', '').replace("'", "").strip()
            # Clean up any extra text that might come from the model
            if "\n" in place:
                place = place.split("\n")[0].strip()
            # Remove common prefixes/suffixes
            place = place.replace("The place is:", "").replace("Place:", "").strip()
            return place if place.lower() != "none" and len(place) > 0 else None
        except Exception as e:
            print(f"Error extracting place: {e}")
            return None
    
    def determine_need(self, query):
        """Determine what the user needs: weather, places, or both"""
        query_lower = query.lower()
        
        # Check for weather-related keywords
        weather_keywords = ['weather', 'temperature', 'temp', 'rain', 'forecast', 'climate', 'hot', 'cold']
        needs_weather = any(word in query_lower for word in weather_keywords)
        
        # Check for places-related keywords
        places_keywords = ['place', 'visit', 'attraction', 'tourist', 'see', 'go', 'plan', 'trip', 'sightseeing']
        needs_places = any(word in query_lower for word in places_keywords)
        
        # If query mentions "and" or "also", likely wants both
        if 'and' in query_lower or 'also' in query_lower:
            if needs_weather or needs_places:
                needs_weather = True if 'weather' in query_lower or 'temperature' in query_lower else needs_weather
                needs_places = True if any(pk in query_lower for pk in places_keywords) else needs_places
        
        # If no specific need mentioned, check if it's a vague query about the place
        if not needs_weather and not needs_places:
            # Vague queries like "tell me about X" or "I'm going to X" default to places
            vague_keywords = ['tell me', 'going to', 'going', 'about', 'information', 'know']
            if any(word in query_lower for word in vague_keywords):
                needs_places = True
            else:
                # Default to places for trip planning
                needs_places = True
        
        return needs_weather, needs_places
    
    def process_query(self, query):
        """Main method to process user query"""
        # Handle empty or very short queries
        if not query or len(query.strip()) < 3:
            return "Please provide a valid query with a place name. For example: 'I'm going to go to Bangalore, let's plan my trip.'"
        
        # Extract place from query
        place = self.extract_place(query)
        
        if not place:
            # Try to extract place using simple keyword extraction as fallback
            query_words = query.split()
            common_places = ['to', 'visit', 'going', 'go']
            place_candidates = []
            for i, word in enumerate(query_words):
                if word.lower() in common_places and i + 1 < len(query_words):
                    # Check if next word might be a place
                    next_word = query_words[i + 1]
                    if next_word and len(next_word) > 2:
                        place_candidates.append(next_word.strip(',').strip('.'))
            
            if place_candidates:
                place = place_candidates[0]
            else:
                return "I couldn't identify the place you want to visit. Could you please specify the place name? For example: 'I'm going to go to Bangalore'"
        
        # Check if place exists by trying to get coordinates
        coords = get_coordinates(place)
        if not coords:
            return f"I don't know if this place exists: {place}. Could you please check the spelling or provide a more specific location?"
        
        # Determine what user needs (for formatting, but we'll call both agents in parallel anyway)
        needs_weather, needs_places = self.determine_need(query)
        
        # ALWAYS call both agents in parallel for any non-vague query (as per user requirement)
        weather_info = None
        places_info = None
        
        # Execute both agents in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=2) as executor:
            # Submit both tasks to run concurrently
            weather_future = executor.submit(self.weather_agent.get_weather, place, coords)
            places_future = executor.submit(self.places_agent.get_places, place, coords)
            
            # Wait for both to complete with timeout handling
            try:
                weather_info = weather_future.result(timeout=30)
            except Exception as e:
                print(f"Error getting weather: {e}")
                weather_info = None
            
            try:
                places_info = places_future.result(timeout=35)
            except Exception as e:
                print(f"Error getting places: {e}")
                places_info = None
        
        # Handle API failures
        if weather_info is None:
            weather_info = None  # Will handle in formatting
        elif "couldn't" in weather_info.lower() or "error" in weather_info.lower():
            weather_info = None
        
        if places_info is None:
            places_info = None
        elif "couldn't find" in places_info.lower() or "error" in places_info.lower():
            places_info = None
        
        # Format response according to PDF examples
        # If user explicitly asks for both or one, format accordingly
        # Otherwise, show both if available
        
        # Extract data from weather response
        temp_value = None
        rain_value = None
        if weather_info and "currently" in weather_info.lower():
            # Parse: "In {place} it's currently {temp}°C with a chance of {rain}% to rain."
            try:
                if "°C" in weather_info:
                    temp_part = weather_info.split("°C")[0]
                    temp_value = temp_part.split("currently")[-1].strip() + "°C"
                if "%" in weather_info and "chance" in weather_info.lower():
                    rain_part = weather_info.split("%")[0]
                    rain_value = rain_part.split()[-1] + "%"
            except:
                pass
        
        # Extract places list
        places_list = []
        if places_info and "places you can go" in places_info.lower():
            lines = places_info.split("\n")
            for line in lines[1:]:  # Skip first line
                line = line.strip("- ").strip()
                if line:
                    places_list.append(line)
        
        # Format output based on available data and user intent
        # Match PDF examples exactly
        if weather_info and places_info:
            # Both available - format like Example 3
            if temp_value and rain_value:
                response = f"In {place} it's currently {temp_value} with a chance of {rain_value} to rain."
            elif temp_value:
                response = f"In {place} it's currently {temp_value}."
            else:
                response = f"In {place}"
            
            if places_list:
                response += " And these are the places you can go:\n" + "\n".join([f"- {p}" for p in places_list])
            elif places_info:
                # Fallback if parsing failed but we have places_info
                lines = places_info.split("\n")
                if len(lines) > 1:
                    response += " And " + "\n".join(lines[1:])
            return response
        
        elif weather_info and not places_info:
            # Only weather available - format like Example 2
            if temp_value and rain_value:
                return f"In {place} it's currently {temp_value} with a chance of {rain_value} to rain."
            elif temp_value:
                return f"In {place} it's currently {temp_value}."
            else:
                # Fallback to original format
                return weather_info
        
        elif places_info and not weather_info:
            # Only places available - format like Example 1 (note the comma!)
            if places_list:
                return f"In {place} these are the places you can go,\n" + "\n".join([f"- {p}" for p in places_list])
            else:
                # Fallback if parsing failed
                return places_info
        
        else:
            # Neither available - return helpful error message
            return f"Sorry, I couldn't retrieve information for {place} at the moment. Please try again later."

