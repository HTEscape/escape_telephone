class telephone:
    def __init__(self, number=None, name=None, ringer=True, dialTone=True, ringerMessage=True,
                 wrongNumberMessage='wrong Number File.mp3'):
        self.number = number
        self.name = name
        self.ringer = ringer
        self.dialTone = dialTone
        self.ringerMessage = ringerMessage
        self.wrongNumberMessage = wrongNumberMessage

    def returnPhoneSettingsList(self):
        returnList = [self.number, self.name, self.ringer, self.dialTone, self.ringerMessage, self.wrongNumberMessage]
        return returnList


class trigger:
    def __init__(self, number=None, name=None, unlockCode=None, isActive=False, triggerMessage=None,
                 relayMode=None, relayActiveTime=1,  relayActive=False, relayMessageTiming=0,
                 messageFile='message file name.mp3'):
        self.number = number
        self.name = name
        if (unlockCode is None):
            self.unlockCode = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '*', '#']
        else:
            self.unlockCode = list(unlockCode)
        self.isActive = isActive
        self.triggerMessage = triggerMessage
        self.relayMode = relayMode
        self.relayActiveTime = relayActiveTime
        self.relayActive = relayActive
        self.relayTimer = 0
        self.relayMessageTiming = relayMessageTiming
        self.messageFile = messageFile

    def returnTriggerValuesList(self):
        returnList = [self.number, self.name, self.unlockCode, self.isActive, self.triggerMessage, self.relayMode,
                      self.relayActiveTime, self.relayActive, self.relayTimer, self.relayMessageTiming,
                      self.messageFile]
        return returnList

