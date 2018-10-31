import serial
import time
import RPi.GPIO as GPIO
import pygame
from telephone_arduino import *
import json

MP3_PLAYING_PIN = 5
arduino = serial.Serial('/dev/serial0', 4800, timeout=2)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(MP3_PLAYING_PIN, GPIO.OUT, initial=0)
pygame.mixer.init()
triggers_list = []
phones_list = []
trigger_settings = []


def get_phone_settings():
    triggers_list.clear()
    phones_list.clear()
    with open('phone_settings_arduino.json') as f:
        loaded_data = json.load(f)
    temp_list = []
    for i in range(len(loaded_data['phone settings'])):
        temp_list = loaded_data['phone settings'][i]
        phone_temp = telephone(temp_list['number'], temp_list['name'], temp_list['ringer'], temp_list['dial tone'],
                               temp_list['ringer message'], temp_list['wrong number message'],
                               temp_list['wrong number file'], temp_list['is active'])
        phones_list.append(phone_temp)

    for i in range(len(loaded_data['triggers'])):
        temp_list = loaded_data['triggers'][i]
        trigger_temp = trigger(temp_list['number'], temp_list['id'], temp_list['name'], temp_list['unlock code'],
                               temp_list['is active'], temp_list['trigger message'], temp_list['relay mode'],
                               temp_list['relay active time'], temp_list['relay message timing'],
                               temp_list['message file'])
        triggers_list.append(trigger_temp)

    del temp_list


def playAudio(fileName):
    GPIO.output(MP3_PLAYING_PIN, 1)
    audioFile = "/home/pi/escape_phone_app/Audio Files/" + fileName
    print(audioFile)
    pygame.mixer.music.load(audioFile)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() is True:
        if (arduino.in_waiting):
            received_line = arduino.readline().decode("utf-8")[1:-2]
            if (received_line == "STOP"):
                pygame.mixer.music.stop()
            else:
                print("This was received during the playAudio Funtion:", received_line)
        time.sleep(0.005)
    GPIO.output(MP3_PLAYING_PIN, 0)


def playRingtone(length=None):
    if length is None:
        GPIO.output(MP3_PLAYING_PIN, 1)
        pygame.mixer.music.load("/home/pi/escape_phone_app/Audio Files/ringtone.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() is True:
            if (arduino.in_waiting):
                received_line = arduino.readline().decode("utf-8")[1:-2]
                if (received_line == "PICKED_UP"):
                    pygame.mixer.music.stop()
                    GPIO.output(MP3_PLAYING_PIN, 0)
            time.sleep(0.005)
    else:
        GPIO.output(MP3_PLAYING_PIN, 1)
        pygame.mixer.music.load("/home/pi/escape_phone_app/Audio Files/ringtone.mp3")
        pygame.mixer.music.play()
        time.sleep(length)
        pygame.mixer.music.stop()
        GPIO.output(MP3_PLAYING_PIN, 0)


def playWrongNumber():
    GPIO.output(MP3_PLAYING_PIN, 1)
    pygame.mixer.music.load("/home/pi/escape_phone_app/Audio Files/Wrong Number Message.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() is True:
        if (arduino.in_waiting):
            received_line = arduino.readline().decode("utf-8")[1:-2]
            if (received_line == "STOP"):
                pygame.mixer.music.stop()
                GPIO.output(MP3_PLAYING_PIN, 0)
            else:
                print("This was received during the Wrong Number Message Playing Function: ", received_line)
        time.sleep(0.005)
    GPIO.output(MP3_PLAYING_PIN, 0)


def send_settings():
    trigger_settings.clear()
    active_phone = None
    for k in range(len(phones_list)):
        if phones_list[k].isActive is True:
            active_phone = k
            break

    phoneSettings = "<PHONE,"
    if active_phone is None:
        phoneSettings += "0,0,0,0,0>"
    else:
        if phones_list[active_phone].ringer is True:
            phoneSettings += '1,'
        else:
            phoneSettings += '0,'

        if phones_list[active_phone].dialTone is True:
            phoneSettings += '1,'
        else:
            phoneSettings += '0,'

        if phones_list[active_phone].ringerMessage is True:
            phoneSettings += '1,'
        else:
            phoneSettings += '0,'

        if phones_list[active_phone].wrongNumberMessage is True:
            phoneSettings += '1,'
        else:
            phoneSettings += '0,'

        count = 0
        for j in range(len(triggers_list)):
            if ((triggers_list[j].id // 100) == phones_list[active_phone].number) and (
                    triggers_list[j].isActive is True):
                temp_trigger = "<TRIGGER,"
                for l in triggers_list[j].unlockCode:
                    temp_trigger += str(l)
                temp_trigger += ',' + str(triggers_list[j].id) + ',' + str(triggers_list[j].triggerMessage) + ','

                if triggers_list[j].relayMode is None:
                    temp_trigger += '0,'
                elif triggers_list[j].relayMode == "time":
                    temp_trigger += '1,'
                else:
                    temp_trigger += '2,'

                temp_trigger += str(triggers_list[j].relayActiveTime) + ','

                if triggers_list[j].relayMessageTiming == "beginning":
                    temp_trigger += '0>'
                else:
                    temp_trigger += '1>'

                trigger_settings.append(temp_trigger)
                count = count + 1

        if count == 0:
            phoneSettings += '0>'
            # send settings    -----TO DO-----
            return
        else:
            phoneSettings += str(count)
            phoneSettings += '>'
            # send settings    -----TO DO-----

    print("Here are the current phone settings")
    print(phoneSettings)
    print("Here are the current Triggers")
    print(trigger_settings)


get_phone_settings()

while True:
    if (arduino.in_waiting):
        received = arduino.readline().decode("utf-8")[:-1]
        if (received == '<TRIGGER>'):
            time.sleep(.005)
            triggerNum = arduino.readline().decode("utf-8")[1:-2]
            try:
                number = int(triggerNum)
                audioName = triggerNum + ".mp3"
                playAudio(audioName)

            except ValueError:
                print("The trigger number that was sent in not an int.")
                print("Value Received", triggerNum)
        elif (received == '<RING>'):
            print("ringing")
            playRingtone()
        elif (received == '<RING TWICE>'):
            print("ringing")
            playRingtone(10.5)
        elif (received == '<WRONG NUMBER>'):
            playWrongNumber()
        elif received == "<CONNECT>":
            print(received)
            arduino.write(b"<CONNECT>")
        elif received == "<SETTINGS>":
            print(received)
            arduino.write(b"<PHONE,1,1,1,1,2>")
        elif received == "<TRIGGERS>":
            print(received)
            arduino.write(b"<TRIGGER,123456,101,1,1,1,5,1>")
            while arduino.in_waiting == 0:
                time.sleep(.01)
            received = arduino.readline().decode("utf-8")[:-1]
            if received == "<NEXT>":
                arduino.write(b"<TRIGGER,987654,102,1,1,1,10,1>")
            else:
                print("Did not receive the <NEXT> command.  Received:", received)
        elif (received == '<RING MESSAGE>'):
            playAudio("Ring Message.mp3")
        else:
            print(received)
    time.sleep(0.001)
