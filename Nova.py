from openai import OpenAI
import speech_recognition as sr
import re
import os
import pyttsx3
import random
halo_voice = pyttsx3.init()
halo_voice.setProperty('rate', 180)  # Imposta la velocità
halo_voice.setProperty('volume', 1)  # Imposta il volume (da 0.0 a 1.0)

def speak():
    while True:
        user_input = ""

        # Usa il microfono per catturare l'input dell'utente
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Parla ora...")
            audio = recognizer.listen(source)
            try:
                user_input = recognizer.recognize_google(audio, language='it-IT')  # Riconoscimento vocale con Google
                print(f"Tu: {user_input}")
            except sr.UnknownValueError:
                print("Non ho capito, per favore ripeti.")
                continue
            except sr.RequestError:
                print("Errore nella richiesta al servizio di riconoscimento vocale.")
                continue

            if user_input.lower() == "pausa":
                print("👋 Chat terminata. Arrivederci!")
                bye = byes[random.randint(0, len(byes) - 1)]
                halo_voice.say(bye)
                halo_voice.runAndWait()
                break

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

        response = completion.choices[0].message.content

        # Fa parlare il chatbot con voce umana usando gTTS

        if how_dare_you(user_input):
            print(response)
            halo_voice.say(remove_emoji(response))
            halo_voice.runAndWait()
def how_dare_you(user_input):
    user_input = user_input.lower()
    if any(badword in user_input for badword in badwords):
        answer = random.choice(nova_is_a_badass)
        halo_voice.say(answer)
        halo_voice.runAndWait()
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

badwords = ["sei brutta", "sei brutto", "idiota", "sei un idiota", "sei stupida", "sei stupido", "stupida", "stupido", "vai a cagare", "hai rotto", "stai zitta", "stai zitto", "fai schifo", "non capisci niente", "ma cosa vuoi", "ma che vuoi", "ma vacci tu", "sei scema", "scema", "scemo", "deficiente", "cretina"]

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
recognizer = sr.Recognizer()
while True:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("say hey Nova to start!")
        audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio, language='it-IT')  # Riconoscimento vocale con Google
            print(user_input)
            if user_input.lower() in names:
                greet = greetings[random.randint(0, len(greetings) - 1)]
                print(greet)
                halo_voice.say(greet+", sono nova!")
                halo_voice.runAndWait()
                speak()
        except sr.UnknownValueError:
            print("non ho capito...")
        except sr.RequestError:
            print("Errore nella richiesta al servizio di riconoscimento vocale.")

