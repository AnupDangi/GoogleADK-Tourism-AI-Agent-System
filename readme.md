# **Tourism AI Agent (Google AI SDK – Multi-Agent Orchestrator)**

This project is a **Tourism AI Assistant** built using the **Google AI SDK (Gemini)**.
It uses a **parent orchestrator agent** that coordinates two specialized child agents:

* **WeatherAgent** → Fetches real-time weather for a place
* **PlacesAgent** → Fetches top tourist attractions for a location

The main agent processes natural language queries, extracts the place, determines what the user needs, and runs both agents **in parallel** using `ThreadPoolExecutor` for faster responses.

## **📸 Reference Project Image**
<img width="1913" height="1028" alt="image" src="https://github.com/user-attachments/assets/a3612c14-2993-40b3-8461-9ea104d649eb" />


---

## **📁 Project Structure**

```
.
├── agents/
│   ├── weather_agent.py
│   ├── places_agent.py
│
├── templates/
│
├── utils/
│   ├── geocoding.py
│
├── venv/
│
├── app.py
├── main.py
├── .env
├── .gitignore
├── requirements.txt
├── Inkle_Assignment.pdf
└── image.png
```

### **Important Files**

* **main.py** → Contains `TourismAIAgent` (Parent orchestrator agent)
* **agents/weather_agent.py** → Child weather agent
* **agents/places_agent.py** → Child tourist-places agent
* **utils/geocoding.py** → Helper for converting place name → latitude/longitude
* **app.py** → FastAPI/Flask app (depending on your setup)
* **.env** → Stores API keys
* **requirements.txt** → Python dependencies

---

## **🚀 Features**

### **1. Parent Orchestrator (TourismAIAgent)**

* Extracts location from natural language queries using Gemini
* Determines whether user is asking for:

  * **Weather info**
  * **Tourist places**
  * **Both**
* Runs both child agents **concurrently** for fast responses
* Cleans and formats results to match example outputs from your assignment/PDF
* Handles vague queries & fallback extraction logic
* Validates if a place exists using geocoding

### **2. Weather Agent**

* Accepts city name + coordinates
* Fetches:

  * Current temperature
  * Rain probability / weather summary
* Returns user-friendly weather descriptions

### **3. Places Agent**

* Accepts city name + coordinates
* Retrieves:

  * Popular attractions
  * Sightseeing spots
  * Places to visit

### **4. Combined Multi-Agent Output**

If both agents succeed, the final answer includes:

* Weather summary
* Tourist attractions list

Example:

```
In Paris it's currently 16°C with a chance of 22% to rain. 
And these are the places you can go:
- Eiffel Tower
- Louvre Museum
- Notre Dame Cathedral
```

---

## **🛠️ Setup Instructions**

### **1. Clone the project**

```sh
git clone <your-repo-url>
cd <project-folder>
```

### **2. Create and activate virtual environment**

```sh
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### **3. Install dependencies**

```sh
pip install -r requirements.txt
```

### **4. Configure Environment Variables**

Create a **.env** file:

```
GOOGLE_API_KEY=your_google_api_key_here
WEATHER_API_KEY=your_api_key
PLACES_API_KEY=your_api_key
GEOCODING_API_KEY=your_api_key
```

Replace only what you actually use.

---

## **▶️ Running the App**

If using **app.py** as the API server:

```sh
python app.py
```

If running directly from **main.py** (interactive testing):

```sh
python main.py
```

---

## **💡 Example Queries**

Try asking:

```
I'm planning to visit Bangalore, what's the weather and places to explore?
Tell me about Paris
What are the places to visit in Delhi?
What's the weather like in Tokyo?
```

---

## **🧠 How the Main Agent Works**

1. Takes a natural language query
2. Extracts place using Gemini prompt
3. Uses geocoding to verify location
4. Identifies intent (weather, tourism, or both)
5. Runs weather + places agents in parallel
6. Formats response according to assignment output rules
7. Handles errors gracefully

---

## **📌 Requirements**

* Python 3.9+
* Google Generative AI SDK (`google-generativeai`)
* Requests / Geopy / any weather or places API
* dotenv

---


