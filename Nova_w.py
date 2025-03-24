from openai import OpenAI
import re
import os
import random
from colorama import init, Fore, Style
import requests
import subprocess
import json
import geocoder



init()

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

print(get_location())

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
        if not city:  # Alcuni posti usano "town" o "village" invece di "city"
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
            city = coordinates_translator(get_location())  # Assumiamo che `get_location` ritorni la città
        elif "no" in user_answer.lower():
            print("Dove ti trovi? Dimmi solo il nome del luogo.")
            user_answer = input("you: ")
            city = user_answer.strip()  # L'utente inserisce il nome della città
        elif "non lo so" in user_answer.lower():
            print(f"Scusami ma non posso ancora accedere al tuo GPS... Ecco cosa ho trovato vicino al tuo IP...")
            city = coordinates_translator(get_location())
        else:
            print(f"Ecco quello che ho trovato vicino al tuo IP...")
            city = coordinates_translator(get_location())

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

        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat:free",
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            temperature=0,  # Aumenta per risposte più creative (tra 0 e 1)
        )
        if not how_dare_you(user_input):
            answering = False


        if answering:
            response = completion.choices[0].message.content
            print(f"{Fore.YELLOW}",response)


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


