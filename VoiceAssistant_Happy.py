import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import re

# Initialize speech recognition and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Set voice properties
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Function to speak out the given text
def talk(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in TTS: {e}")

# Function to listen to voice command
def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print('listening...')
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            
            # Check if 'happy' is in the command and remove it
            if 'happy' in command:
                command = command.replace('happy', '')

    except Exception as e:
        print(e)
        pass

    return command

# Function to execute commands based on voice input
def run_happy():
    while True:
        command = take_command()
        print(command)

        if 'open' in command:
            open_website(command)

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

# Function to open a website based on the command
def open_website(command):
    # Extract the website name from the command using regular expression
    site = re.search('open (.+)', command).group(1)
    print('Opening ' + site)
    talk('Opening ' + site)
    
    # Construct the URL dynamically
    site_url = f"https://www.{site}.com"
    webbrowser.open(site_url)

# Main function to initiate the program
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
