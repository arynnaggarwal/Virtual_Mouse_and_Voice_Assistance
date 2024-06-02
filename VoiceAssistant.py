import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser

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
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in TTS: {e}")


def take_command():
    listener = sr.Recognizer()
    command = ""
    try:
        with sr.Microphone() as origin:
            print('listening...')
            listener.adjust_for_ambient_noise(origin)
            voice = listener.listen(origin)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'happy' in command:
                command = command.replace('happy', '')
                #print(command)

    except Exception as e:
        print(e)
        pass

    return command

def run_happy():
    while True:
        command = take_command()
        print(command)

        if 'open' in command:
            for key in sites:
                if key in command:
                    open_website(sites[key], key)
                    break

        elif 'play' in command:
            song = command.replace('play', '')
            print('Playing' + song)
            talk('Playing' + song)
            pywhatkit.playonyt(song)

        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            print('Current time is ' + time)
            talk('Current time is ' + time)

        elif 'date' in command:
            print('sorry, I have a headache')
            talk('sorry, I have a headache')

        elif 'who is' in command:
            person = command.replace('who is', '')
            info = wikipedia.summary(person, 2)
            print(info)
            talk(info)

        elif 'what is' in command:
            thing = command.replace('what is', '')
            info = wikipedia.summary(thing, 2)
            print(info)
            talk(info)

        elif 'joke' in command:
            joke = pyjokes.get_joke()
            print(joke)
            talk(joke)

        elif 'bye' in command:
            print('Ok bye. Have a nice day')
            talk('Ok bye. Have a nice day')
            exit()

        else:
            print("Sorry, I don't understand that command. Please Repeat it.")
            talk("Sorry, I don't understand that command. Please Repeat it.")


def main():
    try:
        print('Hello, I am happy and how can I help you today?')
        talk('Hello, I am happy and how can I help you today?')
        while True:
            run_happy()
    except KeyboardInterrupt:
        print("Program terminated by user.")
        exit()

if __name__ == "__main__":
    main()
