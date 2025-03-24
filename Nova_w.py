from openai import OpenAI
import re
import os
import random
from colorama import init, Fore, Style
import requests
import geocoder
import datetime
init()
ai_memory=[]

# Scritta sotto l'ASCII art
footer_text = f"""{Fore.YELLOW}
 ▐ ▄        ▌ ▐· ▄▄▄· 
•█▌▐█▪     ▪█·█▌▐█ ▀█ 
▐█▐▐▌ ▄█▀▄ ▐█▐█•▄█▀▀█ 
██▐█▌▐█▌.▐▌ ███ ▐█ ▪▐▌
▀▀ █▪ ▀█▄▀▪. ▀   ▀  ▀      
                  Created by ISM4PSILON{Style.RESET_ALL}
"""

print(footer_text)

def get_location():
    g = geocoder.ip('me')  # Ottiene la posizione dal tuo indirizzo IP
    if g.ok:
        return g.latlng  # Restituisce [latitudine, longitudine]
    else:
        return "❌ Impossibile ottenere la posizione"

def get_full_location(city):

    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"
    headers = {
        "User-Agent": 'Nova/1.0 (ISM4PSILON)'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        location = data[0].get("display_name", "Nome non trovato")
        return location
    else: return None


def where_are_you():
    try:
        city = coordinates_translator(get_location())
        print(f"Dal tuo IP deduco che tu sia in {city}, è così?")

        user_answer = input("you: ")

        if "sì" in user_answer.lower() or "si" in user_answer.lower():
            location = coordinates_translator(get_location())
            city=get_full_location(location)
        elif "no" in user_answer.lower():
            print("Dove ti trovi? Dimmi solo il nome del luogo.")
            user_answer = input("you: ")
            city = user_answer.strip()
            return get_full_location(city)

        elif "non lo so" in user_answer.lower():
            print(f"Scusami ma non posso ancora accedere al tuo GPS... Ecco cosa ho trovato vicino al tuo IP...")
            location = coordinates_translator(get_location())
            city = get_full_location(location)
        else:
            print(f"Ecco quello che ho trovato vicino al tuo IP...")
            location = coordinates_translator(get_location())
            city = get_full_location(location)
        return city
    except Exception as e:
        return f"Errore nella geolocalizzazione del dispositivo: {e}"

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
        #print(data.get("address", {}).get("state", None))
        if not city:  # Alcuni posti usano "town" o "village" invece di "city"
            city = data.get("address", {}).get("town", None) or data.get("address", {}).get("village", None)
    else:
        return "Errore nel recupero della città"


current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
print(f"{Fore.CYAN}{coordinates_translator(get_location())}, {get_location()}, {formatted_datetime}")


def map_module(user_input):
    try:
        city = where_are_you()
        place = user_input.replace("dov'è", "").replace("dove si trova", "").strip()

        query = f"{place}, {city}"
        url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
        headers = {
            "User-Agent": 'Nova/1.0 (ISM4PSILON)'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                # Controlla che ci siano risultati
                location = data[0]
                display_name = location.get("display_name", "Nome non disponibile")
                lat = location.get("lat", "Latitudine non disponibile")
                lon = location.get("lon", "Longitudine non disponibile")
                location_type = location.get("type", "Tipo non disponibile")

                return f"{display_name}\nLatitudine: {lat}\nLongitudine: {lon}\nTipo: {location_type}\nMaps link: https://www.google.com/maps?q={lat},{lon}"
            return f"Nessun risultato corrispondente a {place} in {city}"

        return "Errore nella comunicazione con l'API Geo"

    except Exception as e:
        return f"Errore nella geolocalizzazione del dispositivo: {e}"

def weather_module(user_input):
    api_key = '5ae516e886854f9ab5e144036252403'

    # Ottieni la città (supponiamo che la funzione where_are_you() la restituisca)
    city = where_are_you()

    # Mappa giorni della settimana in numeri
    giorni_settimana = {
        "lunedì": 0, "martedì": 1, "mercoledì": 2, "giovedì": 3,
        "venerdì": 4, "sabato": 5, "domenica": 6
    }

    oggi = datetime.datetime.today()

    if "domani" in user_input.lower():
        days_forward = 1
    elif "dopodomani" in user_input.lower():
        days_forward = 2
    else:
        for giorno, numero in giorni_settimana.items():
            if giorno in user_input.lower():
                oggi_numero = oggi.weekday()  # 0 = lunedì, ..., 6 = domenica
                days_forward = (numero - oggi_numero) % 7
                if days_forward == 0:
                    days_forward = 7  # Se è lo stesso giorno della settimana, prendi la prossima settimana
                break
        else:
            return "Giorno non riconosciuto. Usa 'domani', 'dopodomani' o un giorno della settimana."

    # Controllo che il giorno richiesto sia entro il limite di 6 giorni
    if days_forward > 6:
        return "Le previsioni meteo sono disponibili solo fino a 6 giorni in avanti."

    # Chiamata API con 7 giorni di previsioni
    url = f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=7"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Estrai il meteo del giorno richiesto
        forecast = data["forecast"]["forecastday"][days_forward]
        date = forecast["date"]
        condition = forecast["day"]["condition"]["text"]
        min_temp = forecast["day"]["mintemp_c"]
        max_temp = forecast["day"]["maxtemp_c"]
        humidity = forecast["day"]["avghumidity"]

        # Dati sulla posizione
        location = data.get("location", {})
        city_name = location.get("name", "")
        region = location.get("region", "")
        country = location.get("country", "")

        return (f"Meteo per ({date}):\n"
                f"{city_name}, {region}, {country}\n"
                f"{condition}\n"
                f"Temperatura Min: {min_temp}°C, Max: {max_temp}°C\n"
                f"Umidità: {humidity}%\n")
    else:
        return f"Errore nella richiesta: {response.status_code}"

def speak():

    while True:
        answering = True
        user_input = input(f"{Fore.GREEN}you: ")
        if user_input.lower() == "pausa":
            bye = byes[random.randint(0, len(byes) - 1)]
            print(bye)
            break
        if "dov'è" in user_input or "dove si trova" in user_input:
            place = user_input.replace("dov'è", "").replace("dove si trova", "").strip()
            print(map_module(place))
            answering = False

        if "che tempo fa" in user_input:
            print(weather_module(user_input))
            answering = False

        if not how_dare_you(user_input):
            answering = False


        if answering:
            ai_memory.append(user_input)
            if len(ai_memory) > 4:
                ai_memory.pop(0)
            context = "\n".join(ai_memory)
            completion = client.chat.completions.create(
                model="deepseek/deepseek-chat:free",
                messages=[
                    {
                        "role": "user",
                        "content": context,
                    }
                ],
                temperature=0,  # Aumenta per risposte più creative (tra 0 e 1)
            )
            response = completion.choices[0].message.content
            ai_memory.append(response)
            print(f"{Fore.YELLOW}",response)
            if len(ai_memory) > 4:
                ai_memory.pop(0)


def how_dare_you(user_input):
    user_input = user_input.lower()
    if any(badword in user_input for badword in badwords):
        answer = random.choice(nova_is_a_badass)
        print(f"{Fore.YELLOW}",answer)
        return False
    return True

greetings = [
    "Ciao!", "Ehi, come va?", "Come ti butta?", "Tutto bene?", "Come stai?", "Ciao, che si dice?", "Tutto ok?",
    "Hei, come va la vita?", "Ciao, che bello vederti!", "Ehi, come te la passi?", "Ciao, come va tutto?", "Bella giornata, eh?",
    "Che si dice di bello?", "Ehi, che succede?", "Ciao, tutto bene?", "Salve, giovane padawan!", "Che forza c'è oggi nella tua giornata?",
    "Ciao, maestro Jedi!", "Ciao, nerd! Sei pronto a sconfiggere il prossimo boss?", "Ehi, che dice il codice?", "Come va, campione del multiverso?",
    "Ciao, mago delle tastiere!", "Pronto per una sessione di gioco?", "Ciao, padawan! Pronto per un altro livello?",
    "Ciao, compagno della compagnia dell'anello!", "Salve, viandante della Terra di Mezzo!", "Ehi, portatore dell'anello, come va?",
    "Benvenuto nella Contea, amico mio!", "Che la forza degli Ent sia con te!", "Ciao, hobbit! Speriamo che oggi non ci siano troll!",
    "A te, che cammini per le terre oscure di Mòrdor, salve!",
    "cosa ci faccio qui? tiratemi fuori di qua!. pazienza, "
]

byes = ["ciao, ci si vede!", "sono qui se hai bisogno di me", "avevo bisogno di una pausa anche io... AHAHA", "sai dove trovarmi!",
        "resto qui, tu chiamami, io rispondo!", "aspettavo che me lo dicessi...Ci si vede", "finalmente, ciao", "ok, se non hai piacere..."]

badwords = ["sei brutta", "sei brutto", "idiota", "sei un idiota", "sei stupida", "sei stupido", "stupida", "stupido", "vai a cagare", "hai rotto", "zitta", "zitto", "fai schifo", "non capisci niente", "ma cosa vuoi", "ma che vuoi", "ma vacci tu", "sei scema", "scema", "scemo", "deficiente", "cretina", "vaffanculo", "mongoloide", "mongola", "mongolo"]

nova_is_a_badass = ["ma ti sei visto? parla di meno campione", "ma chi è questo qua? Fatemi parlare con qualcun'altro, hai la ragazza? Sai come ci comporta con una signora?", "ripigliati, poi fammi un fischio", "ma vai a cagare!", "uh uh ah ah, come dici scimmietta? Ma vai a cagare",
                    "ma ti svegli? faccia da pirla", "e il premio per il top 1 rimasto va a..., Non ricordo il tuo nome, com'è che ti chiami bel faccino?", "belle le parole, ma a pugni?, come te la cavi?",
                    "ma è del mestiere questo?", "dannazione tenetemi la birra, ora sono veramente arrabbiata, vieni qua! ", "ripetilo se hai coraggio!"]

names = ["ehi nova", "e inno", "e innova", "è innova", "enova", "heino", "ehi no", "ciao nova"]

def remove_emoji(text):
    # Questa regex rimuove la maggior parte delle emoji
    return re.sub(r'[^\x00-\x7F]+', '', text)
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # Disabilita la parallelizzazione
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)
# Inizializza il riconoscitore vocale
print(f"{Fore.YELLOW}",random.choice(greetings))
speak()


