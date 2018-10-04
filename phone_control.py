from telephone import *
import json
import time

def main(pipe=1):
    global triggers_list
    global phones_list
    global HANDSET_PIN
    HANDSET_PIN = 26
    triggers_list = []
    phones_list = []
    global handset_picked_up

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
        global handset_picked_up
        global HANDSET_PIN
        if (GPIO.input(HANDSET_PIN) == OFF_THE_HOOK):
            handset_picked_up = True
        else:
            handset_picked_up = False
        '''
        pass

    #GPIO.add_event_detect(HANDSET_PIN, GPIO.BOTH, callback=check_handset, bouncetime=30)  #Add interrupt for handset
    load_phone_settings()
    print(str(pipe))
    print(phones_list[0].returnPhoneSettingsList())
    print(triggers_list[0].returnTriggerValuesList())
