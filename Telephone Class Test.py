from telephone import *

phone = telephone()

trigger1 = trigger(unlockCode=[2,6,0,7])

print(phone.returnPhoneSettingsList())
print(trigger1.returnTriggerValuesList())

