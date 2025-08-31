import os
from dotenv import load_dotenv
import speech_recognition as sr
import webbrowser
import pyttsx3 #For text to speech
import musicLibrary
import requests

load_dotenv()

recognizer = sr.Recognizer()
engine = pyttsx3.init()

NEWS_API = os.getenv("NEWS_API")

rate = engine.setProperty("rate", 250)
# rate =  engine.getProperty("rate")
# print(f"Current speed {rate}")

def speak(text):
    engine.say(text)
    engine.runAndWait()


def processCommand(command):
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in command.lower():
        webbrowser.open("https://youtube.com")
    elif "open instagram" in command.lower():
        webbrowser.open("https://instagram.com")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://linkedin.com")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in command.lower():
        res = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API}")
        if res.status_code == 200:
            data = res.json()

            articles = data.get('articles', [])
            # Prints the headlines
            for article in articles:
                speak(article['title'])
    

if __name__ == "__main__":
    speak("Initializing JARVIS...")

    while True:
        #Listen to the wake word 
        #Obtain audio from microphone
        r = sr.Recognizer()
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=3, phrase_time_limit=3)
            word = r.recognize_google(audio)
            # print(word) 
            if word.lower() == "jarvis":
                speak("yes")
                #Listen for the command
                with sr.Microphone() as source:
                    print("Activating...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))