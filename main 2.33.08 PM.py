import speech_recognition, os, pygame
import pyttsx3
import wikipedia
import requests, json
from datetime import date, datetime
from googlesearch import search
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

# import Screen

# def window():
#     app = QApplication(sys.argv)
#     win = QMainWindow()
#     win.setGeometry(1200, 0, 400, 200)
#     win.setStyleSheet("background-image : url(/Users/ethan/Desktop/siri.png)")
#     win.show()
#     sys.exit(app.exec_())


AI_brain = ""


def say(AI_brain):
    AI_mouth = pyttsx3.init()
    AI_mouth.say(AI_brain)
    AI_mouth.runAndWait()


def hear():
    AI_ear = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as mic:
        print("Robot: I'm listening")
        AI_ear.adjust_for_ambient_noise(mic)
        audio = AI_ear.listen(mic, timeout=6, phrase_time_limit=5)
    print("Robot: ...")
    try:
        you = AI_ear.recognize_google(audio)
    except:
        you = ""
    return you


pygame.init()

x = 1200
y = 0
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
# width, height = 400, 200
win = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Robot")
background_image = pygame.image.load("/Users/ethan/Desktop/siri.png").convert_alpha()
# clock = pygame.time.Clock()
running = True
while running:
    win.blit(background_image, (0, 0))
    event = pygame.event.get()
    if event == pygame.QUIT:
        pygame.quit()
        sys.exit()
    pygame.display.update()
    you = hear()
    print("You :" + you)
    if you == "":
         AI_brain = "I can't here you"
    elif you == "hello" or you == "hi":
        AI_brain = "hello There"
    elif "what date is today" in you or "what day is today" in you:
        today = date.today()
        AI_brain = today.strftime("%B %d, %Y")
    elif "what time is it" in you or "what time now" in you:
        now = datetime.now()
        if int(float(now.strftime("%H"))) > 12:
            AI_brain = now.strftime("%H:%M PM")
        else:
            AI_brain = now.strftime("%H:%M AM")
    elif "bye" in you or pygame.event.wait().type == pygame.QUIT:
        say("Good Bye!")
        break
    elif "Google" in you or "google" in you:
         # to search
        say("What do you want to search for?")
        you = hear()
        for j in search(you, tld="co.in", num=10, stop=10, pause=2):
            print(j)
        AI_brain = "I found some result about it on google"
    elif "weather" in you:
        # base URL
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        API_KEY = "6e4ac8efacca4d669ecaf5357badd82a"
        AI_brain = "Which city you want: "
        print("Robot: " + AI_brain)
        say(AI_brain)
        you = hear()
        print("You: " + you)
        # upadting the URL
        URL = BASE_URL + "q=" + you + "&appid=" + API_KEY
        # HTTP request
        response = requests.get(URL)
        # checking the status code of the request
        if response.status_code == 200:
            # getting data in the json format
            data = response.json()
            # getting the main dict block
            main = data['main']
            # getting temperature
            temperature = (main['temp'] - 273.15) * 9 / 5 + 32
            # getting the humidity
            humidity = main['humidity']
            # getting the pressure
            pressure = main['pressure']
            # weather report
            report = data['weather']
            weather_description = report[0]['description']
            AI_brain = "Now " + you + " " + str(weather_description) + ",temperature is " + str(
                round(temperature)) + " Fahrenheit degree" + ",the humidity " + str(
                humidity) + "% " + ",the pressure: " + str(pressure)
        else:
            # showing the error message
            AI_brain = "Error in the HTTP request"
    elif "my girlfriend" in you:
        AI_brain = "Tam Truong"
    elif "Wikipedia" in you:
        AI_brain = "What you want to searching?"
        print("Robot: " + AI_brain)
        say(AI_brain)
        you = hear()
        try:
            AI_brain = wikipedia.summary(you)
        except:
            AI_brain = "Please try again"

    else:
        AI_brain = "I'm fine. Thank you"

    print("Robot: " + AI_brain)
    say(AI_brain)
pygame.quit()

