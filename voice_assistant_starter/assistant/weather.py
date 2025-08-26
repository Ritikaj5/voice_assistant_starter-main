import requests

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

def get_coords(city: str):
    r = requests.get(GEO_URL, params={"name": city, "count": 1})
    r.raise_for_status()
    data = r.json()
    results = data.get("results") or []
    if not results:
        return None
    first = results[0]
    return first["latitude"], first["longitude"], first.get("name") or city, first.get("country_code")

def get_weather(city: str):
    coords = get_coords(city)
    if not coords:
        return None
    lat, lon, disp_name, country = coords
    r = requests.get(FORECAST_URL, params={
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    })
    r.raise_for_status()
    data = r.json()
    cw = data.get("current_weather")
    if not cw:
        return None
    # Map weather codes (simplified subset)
    code_map = {
        0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
        45: "foggy", 48: "depositing rime fog",
        51: "light drizzle", 53: "moderate drizzle", 55: "dense drizzle",
        61: "light rain", 63: "rain", 65: "heavy rain",
        71: "snow", 80: "rain showers", 95: "thunderstorm"
    }
    desc = code_map.get(cw.get("weathercode"), "current weather")
    return {
        "city": disp_name,
        "country": country,
        "temperature_c": cw.get("temperature"),
        "windspeed_kmh": cw.get("windspeed"),
        "description": desc
    }
