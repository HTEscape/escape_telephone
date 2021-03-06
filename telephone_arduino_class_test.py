from telephone_arduino import *
import json


triggers_list = []
phones_list = []
phone = telephone()

trigger1 = trigger(unlockCode=[2, 6, 0, 7])

print(phone.returnPhoneSettingsList())
print(trigger1.returnTriggerValuesList())

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
                           temp_list['relay active time'], temp_list['relay message timing'], temp_list['message file'])
    triggers_list.append(trigger_temp)

del temp_list

print(phones_list[0].returnPhoneSettingsList())
phones_list[0].wrongNumberMessage = "new file name.mp3"
print(phones_list[0].returnPhoneSettingsList())

for i in range(len(triggers_list)):
    print(triggers_list[i].returnTriggerValuesList())


def send_settings():
    global triggers_list
    global phones_list
    trigger_settings = []
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
            if ((triggers_list[j].id // 100) == phones_list[active_phone].number) and (triggers_list[j].isActive is True):
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


send_settings()
