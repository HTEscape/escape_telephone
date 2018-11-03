from telephone import *
import json
import time
from pad4pi import rpi_gpio
import RPi.GPIO as GPIO

def main(pipe=1):
    global triggers_list
    global phones_list
    global HANDSET_PIN
    HANDSET_PIN = 26
    triggers_list = []
    phones_list = []
    TONE_PIN_1 = 25
    TONE_PIN_2 = 26
    HANDSET_PIN = 19
    HUNG_UP_LOGIC = 0
    unlock_code = [2, 6, 0, 7]
    global phone_on_hook
    phone_on_hook = True
    global DTMF_Tone1
    global DTMF_Tone2
    DTMF_Tone1 = [941, 697, 697, 697, 770, 770, 770, 852, 852, 852, 941, 941]
    DTMF_Tone2 = [1336, 1209, 1336, 1477, 1209, 1336, 1477, 1209, 1336, 1477, 1209, 1477]

    def playDtmfTones(key):
        global DTMF_Tone1
        global DTMF_Tone2
        stopTones()
        try:
            int_key = int(key)
            if int_key >= 0 and int_key <= 9:
                tone1.ChangeFrequency(DTMF_Tone1[key])
                tone2.ChangeFrequency(DTMF_Tone2[key])
                tone1.start(50)
                tone2.start(50)
        except ValueError:
            if key == '*':
                tone1.ChangeFrequency(DTMF_Tone1[10])
                tone2.ChangeFrequency(DTMF_Tone2[10])
                tone1.start(50)
                tone2.start(50)
            elif key == '#':
                tone1.ChangeFrequency(DTMF_Tone1[11])
                tone2.ChangeFrequency(DTMF_Tone2[11])
                tone1.start(50)
                tone2.start(50)
    
    def stopTones():
        tone1.stop()
        tone2.stop()

    def playDialTone():
        tone1.ChangeFrequency(350)
        tone2.ChangeFrequency(440)
        tone1.start(50)
        tone2.start(50)
    
    def cleanup():
        global keypad
        keypad.cleanup()
        
    def printKeyPressed(key):
        global keypad
        try:
            int(key)
            print(str(key))
            print(keypad.enteredCode)
        except ValueError:
            print(keypad.enteredCode)
            print(key)
        
    def keypadAction(key):
        global keypad
        if key == -1: #Button was realeased
            stopTones()    
        else:
            playDtmfTones(key)
            print(str(key))
            print(keypad.enteredCode)
            
    def checkHandset():
        global keypad
        global phone_on_hook
        if (GPIO.input(HANDSET_PIN) == HUNG_UP_LOGIC):
            keypad.clearEnteredCode
            print("Phone was hung up")
            phone_on_hook = True
        else:
            playDialTone()
            print("Phone was picked up")
            phone_on_hook = False    
    
    
    def load_phone_settings():
        global triggers_list
        global phones_list
        triggers_list = []
        phones_list = []
        with open('phone_settings.json') as f:
            loaded_data = json.load(f)
        temp_list = []
        for i in range(len(loaded_data['phone settings'])):
            temp_list = loaded_data['phone settings'][i]
            phone_temp = telephone(temp_list['number'], temp_list['name'], temp_list['ringer'], temp_list['dial tone'],
                                   temp_list['ringer message'], temp_list['wrong number'])
            phones_list.append(phone_temp)

        for i in range(len(loaded_data['triggers'])):
            temp_list = loaded_data['triggers'][i]
            trigger_temp = trigger(temp_list['number'], temp_list['name'], temp_list['unlock code'],
                                   temp_list['is active'], temp_list['trigger message'], temp_list['relay mode'],
                                   temp_list['relay active time'], temp_list['relay active'],
                                   temp_list['relay message timing'], temp_list['message file'])
            triggers_list.append(trigger_temp)

        del temp_list

    def check_handset():
        '''
        global phone_on_hook
        global HANDSET_PIN
        if (GPIO.input(HANDSET_PIN) == OFF_THE_HOOK):
            phone_on_hook = True
        else:
            phone_on_hook = False
        '''
        pass

    #GPIO.add_event_detect(HANDSET_PIN, GPIO.BOTH, callback=check_handset, bouncetime=30)  #Add interrupt for handset
    load_phone_settings()
    print(str(pipe))
    print(phones_list[0].returnPhoneSettingsList())
    print(triggers_list[0].returnTriggerValuesList())
    
    try:
        factory = rpi_gpio.KeypadFactory()
        keypad = factory.create_4_by_3_keypad() # makes assumptions about keypad layout and GPIO pin numbers
        keypad.registerKeyPressHandler(keypadAction)
        GPIO.setup(HANDSET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(TONE_PIN_1, GPIO.OUT)
        GPIO.setup(TONE_PIN_2, GPIO.OUT)
        GPIO.add_event_detect(HANDSET_PIN, GPIO.BOTH, callback=checkHandset, bouncetime=40)
        tone1 = GPIO.PWM(TONE_PIN_1, 50)
        tone2 = GPIO.PWM(TONE_PIN_2, 50)
        #pygame.mixer.init()
    
        print("Enter your passcode (hint: {0})".format(unlock_code))
        
        while True:
            time.sleep(.001)
            if (keypad.released):
                keypad.released = False
            if (keypad.enteredCode == unlock_code):
                time.sleep(.05)
                print("You Win the game!!!")
                keypad.clearEnteredCode()
            
    except KeyboardInterrupt:
        print("Goodbye")

    finally:
        cleanup()