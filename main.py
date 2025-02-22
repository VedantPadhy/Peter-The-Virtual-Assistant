import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

# Initialize the speech engine and pygame mixer only once
pygame.mixer.init()
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "<your api key>"


def speak(text):
    try:
        tts = gTTS(text)
        temp_file = "temp.mp3"
        tts.save(temp_file)

        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        os.remove(temp_file)
    except Exception as e:
        print(f"Speech error: {e}")


def aiProcess(command):
    client = OpenAI(api_key="your_open_ai_api_key")  # Replace with your actual key

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Peter skilled in general tasks like Alexa and Google Assistant. Give short responses, please."},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content


def processCommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn")
    elif c.startswith("play"):
        song = " ".join(c.split(" ")[1:])
        link = musicLibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak("Sorry, I couldn't find that song in the library.")
    elif "news" in c:
        r = requests.get(f'https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}')
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles[:5]:  # Limit to top 5 news headlines
                speak(article['title'])
        else:
            speak("Sorry, I couldn't fetch the news.")
    else:
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Peter...")

    r = sr.Recognizer()
    print("Recognizing...")

    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source, timeout=2, phrase_time_limit=1)
        word = r.recognize_google(audio)
        if word.lower() == "peter":
            speak("Yeah")
            with sr.Microphone() as source:
                print("Peter is active...")
                audio = r.listen(source)
                command = r.recognize_google(audio)
                processCommand(command)
    except sr.UnknownValueError:
        print("Peter could not understand the audio")
    except Exception as e:
        print(f"Error: {e}")
