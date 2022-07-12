import speech_recognition as sr
from file_handler import searchfiles, log_all_files
import os
import json
import datetime
import time
import pyjokes
import webbrowser
import pyttsx3
import wikipedia

# word booleans
positive = ['yes', 'sure', 'alright', 'ok', 'okay', 'k', 'yeah', 'yep', 'positive', 'mhm', 'alr', 'done', 'affirmative']
negative = ['no', 'never', 'nope', 'nah', 'negative', 'meh']

# Voice Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')

def speak(msg):
    engine.setProperty('voice', voices[1].id)
    engine.say(msg)
    engine.runAndWait()
speak('Listening, Master...')
def listener(loc):
    listener = sr.Recognizer()
    voice = listener.listen(loc)
    try:
        command = listener.recognize_google(voice)
        return command
    except:
        return ""
def please():
    with sr.Microphone() as source:
        command = listener(source)
        if 'please' in command:
            if command.replace('please ', '').startswith('open'):
                file = command.replace('please open ', '')
                print(file)
                try:
                    with open('preferences.json', 'r') as preff:
                        pref = json.load(preff)
                        if pref[file].startswith('http'):
                            webbrowser.open(pref[file])
                        else:
                            os.system('"' + pref[file] + '"')
                except:
                    search = searchfiles(file)
                    if type(search) == list:
                        if len(search) > 0:
                            speak("Multiple Options found, which would you like to open?")
                            command = listener(source)
                            for word in command:
                                try:
                                    os.system('"'+search[int(word)+1]+'"')
                                except:
                                    pass

                        if len(search) == 0:
                            speak("No Matching results for " + file + ". Would you like to set a Preference?")
                            command = listener(source)
                            command = command.split(' ')
                            print(command)
                            done = False
                            for reply in command:
                                if reply in positive and not done:
                                    speak("Please Enter a path to "+file)
                                    enter = input("Please Enter a path to "+file+":")
                                    done = True
                                    if enter:
                                        with open('preferences.json', 'w') as preff:
                                            pref[file] = enter
                                            json.dump(pref, preff)
                                            os.system('"'+enter+'"')

                        else:
                            try:
                                for file in search:
                                    if file.endswith('.lnk'):
                                        os.system('"' + str(file) + '"')
                                print(search)
                            except:
                                pass

                    else:
                        try:
                            os.system('"'+str(search)+'"')
                        except:
                            pass

            elif 'time' in command:
                speak('Currently, it is ' + datetime.datetime.now().strftime("%I:%M %p"))
            elif 'who is ' in command or 'tell me about ' in command or 'what is ' in command:
                details = wikipedia.summary(command.replace('please ', '').replace('who is ', '').replace('tell me about ', ''), 1)
                speak(details)
            elif 'joke' in command or 'something funny' in command or 'laugh' in command or 'hilarious' in command:
                speak(pyjokes.get_joke())
            elif 'sleep ' in command:
                try:
                    if 'minute' in command:
                        dur = int(command.replace('please', '').split(' ')[-2])*60
                    elif 'hour' in command:
                        dur = int(command.replace('please', '').split(' ')[-2])*3600
                    else:
                        dur = int(command.replace('please', '').split(' ')[-1])
                    speak("Sleeping for "+str(dur)+" Seconds. Zzzz...")
                    return dur
                except:
                    speak("I did not catch that properly... please try again.")
            else:
                speak("I did not catch that properly... please try again.")
def keep_alive():
    vas = please()
    while True:
        if not vas:
            vas = please()
        elif vas:
            time.sleep(int(vas))
            vas = please()

keep_alive()
log_all_files(['exe', 'py', 'lnk'])
