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
'''
for i in range(len(loaded_data['cycles'])):
    temp_list = loaded_data['cycles'][i]
    cycle_temp = cycle(temp_list['number'], temp_list['name'], temp_list['start time hour'],
                       temp_list['start time minute'], temp_list['days of week'], temp_list['stations'],
                       temp_list['durations'], temp_list['enabled'])
    cycle_list.append(cycle_temp)
'''
del temp_list

print(phones_list[0].returnPhoneSettingsList())