from telephone import *
import json

triggers_list = []
phones_list = []
phone = telephone()

trigger1 = trigger(unlockCode=[2,6,0,7])

print(phone.returnPhoneSettingsList())
print(trigger1.returnTriggerValuesList())

with open('phone_settings.json') as f:
    loaded_data = json.load(f)
temp_list = []
for i in range(len(loaded_data['phone settings'])):
    temp_list = loaded_data['phone settings'][i]
    phone_temp = telephone(temp_list['number'], temp_list['ringer'], temp_list['dial tone'],
                           temp_list['ringer message'], temp_list['wrong number'])
    phones_list.append(phone_temp)

for i in range(len(loaded_data['triggers'])):
    temp_list = loaded_data['triggers'][i]
    trigger_temp = trigger(temp_list['number'], temp_list['unlock code'], temp_list['is active'],
                           temp_list['trigger message'], temp_list['relay mode'], temp_list['relay active time'],
                           temp_list['relay active'], temp_list['relay message timing'], temp_list['message file'])
    triggers_list.append(trigger_temp)

del temp_list

print(phones_list[0].returnPhoneSettingsList())
phones_list[0].wrongNumberMessage = "new file name.mp3"
print(phones_list[0].returnPhoneSettingsList())

print(triggers_list[0].returnTriggerValuesList())
