import pyttsx3
import speech_recognition as sr
import eel
import time
import os
from plyer import notification

def speak(text):
    text = str(text)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():
    
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 6, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
       
    except Exception as e:
        return ""
    
    return query.lower()

def alarm(query):
    timehere = open("engine\\Alarmtext.txt","a")
    timehere.write(query)
    timehere.close()
    os.startfile("engine\\alarm.py")
    

@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "schedule my day" in query:
            tasks = [] #Empty list
            speak("Do you want to clear old tasks (Plz speak YES or NO)")
            preferance = takecommand()
            print(preferance)
            if "yes" in preferance:
                file = open("engine\\tasks.txt","w")
                file.write(f"")
                file.close()
                no_tasks = int(input("Enter the no. of tasks :- "))
                i = 0
                for i in range(no_tasks):
                    tasks.append(input("Enter the task :- "))
                    file = open("engine\\tasks.txt","a")
                    file.write(f"{i}. {tasks[i]}\n")
                    file.close()
            elif "no" in preferance:
                i = 0
                no_tasks =int(input("Enter the no. of tasks :- "))
                for i in range(no_tasks):
                    tasks.append(input("Enter the task :- "))
                    file = open("engine\\tasks.txt","a")
                    file.write(f"{i}. {tasks[i]}\n")
                    file.close()
        elif "show my schedule" in query:
            file = open("engine\\tasks.txt","r")
            content = file.read()
            file.close()
            notification.notify(
                title = "My schedule :-",
                message = content,
                timeout = 15
            )

        elif "set an alarm" in query:
            speak("input time example:- 10 and 10 and 10")
            speak("set the time")
            speak("Please tell the time:-")
            time = takecommand()
            alarm(time)
            speak("Done,sir")
            

        
        elif "send message" in query or "call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            # message = ''
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "sms" in query: 
                        speak("what message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "call" in query:
                        makeCall(name, contact_no)
                    else:
                        print("not run")
                        speak("please try again")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = 'send message'
                        speak("what message to send")
                        query = takecommand()
                                        
                    elif "call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name)

        else:
            from engine.features import chatBot
            chatBot(query)
    except:
        print("error")
    
    eel.ShowHood()

