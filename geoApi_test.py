import geocoder
import requests

def get_location():
    g = geocoder.ip('me')  # Ottiene la posizione dal tuo indirizzo IP
    if g.ok:
        return g.latlng  # Restituisce [latitudine, longitudine]
    else:
        return "❌ Impossibile ottenere la posizione"

def coordinates_translator(coordinates):
    lat = coordinates[0]
    lon = coordinates[1]
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    headers = {
        "User-Agent": 'Nova/1.0 (ISM4PSILON)'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        city = data.get("address", {}).get("city", None)
        if not city:
            city = data.get("address", {}).get("town", None) or data.get("address", {}).get("village", None)
        return city if city else "Città non trovata"
    else:
        return "Errore nel recupero della città"

def map_module(user_input):
    try:
        city = coordinates_translator(get_location())  # Assumiamo che get_location() restituisca la città dell'utente
        print(f"Dal tuo IP deduco che tu sia in {city}, è così?")

        user_answer = input("you: ")

        if "sì" in user_answer.lower() or "si" in user_answer.lower():
            city = coordinates_translator(get_location())
        elif "no" in user_answer.lower():
            print("Dove ti trovi? Dimmi solo il nome del luogo.")
            user_answer = input("you: ")
            city = user_answer.strip()
        elif "non lo so" in user_answer.lower():
            print(f"Scusami ma non posso ancora accedere al tuo GPS... Ecco cosa ho trovato vicino al tuo IP...")
            city = coordinates_translator(get_location())
        else:
            print(f"Ecco quello che ho trovato vicino al tuo IP...")
            city = coordinates_translator(get_location())

        place = user_input.replace("dov'è", "").replace("dove si trova", "").strip()

        # Crea la stringa di ricerca come "place, city"
        query = f"{place}, {city}"

        # API OpenStreetMap per la ricerca del luogo con la query formattata
        url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
        headers = {
            "User-Agent": 'Nova/1.0 (ISM4PSILON)'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                location = data[0]
                display_name = location.get("display_name", "Nome non disponibile")
                lat = location.get("lat", "Latitudine non disponibile")
                lon = location.get("lon", "Longitudine non disponibile")
                address = location.get("address", "Indirizzo non disponibile")
                location_type = location.get("type", "Tipo non disponibile")

                return f"{display_name}\nLatitudine: {lat}\nLongitudine: {lon}\nIndirizzo: {address}\nTipo: {location_type}"
            return f"Nessun risultato corrispondente a {place} in {city}"

        return "Errore nella comunicazione con l'API Geo"

    except Exception as e:
        return f"Errore nella geolocalizzazione del dispositivo: {e}"

user_input="dov'è duomo"
print(map_module(user_input))
