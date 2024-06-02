import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import sys

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

sites = {
    "wikipedia": "https://www.wikipedia.org",
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
}

def open_website(site_url, key):
    print('Opening' + key)
    talk('Opening' + key)
    webbrowser.open(site_url)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_instruction():
    listener = sr.Recognizer()
    instruction = ""
    try:
        with sr.Microphone() as origin:
            print('listening...')
            listener.adjust_for_ambient_noise(origin)
            voice = listener.listen(origin)
            instruction = listener.recognize_google(voice)
            instruction = instruction.lower()
            if 'happy' in instruction:
                instruction = instruction.replace('happy', '')
                #print(instruction)

    except Exception as e:
        print(e)
        pass

    return instruction

def run_happy():
    while True:
        instruction = take_instruction()
        print(instruction)

        if 'open' in instruction:
            for key in sites:
                if key in instruction:
                    open_website(sites[key], key)
                    break

        elif 'play' in instruction:
            song = instruction.replace('play', '')
            print('Playing ' + song)
            talk('Playing' + song)
            pywhatkit.playonyt(song)

        elif 'time' in instruction:
            time = datetime.datetime.now().strftime('%I:%M %p')
            print('Current time is ' + time)
            talk('Current time is ' + time)

        elif 'date' in instruction:
            print('sorry, I have a headache')
            talk('sorry, I have a headache')

        elif 'who is' in instruction:
            person = instruction.replace('who is', '')
            info = wikipedia.summary(person, 2)
            print(info)
            talk(info)

        elif 'what is' in instruction:
            thing = instruction.replace('what is', '')
            info = wikipedia.summary(thing, 2)
            print(info)
            talk(info)

        elif 'joke' in instruction:
            joke = pyjokes.get_joke()
            print(joke)
            talk(joke)

        elif 'bye' in instruction:
            print('Ok bye. Have a nice day')
            talk('Ok bye. Have a nice day')
            exit()

        else:
            print("Sorry, I don't understand that command. Please Repeat it.")
            talk("Sorry, I don't understand that command. Please Repeat it.")


if __name__ == "__main__":
    run_happy()
