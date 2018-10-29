class telephone:
    def __init__(self, number=None, name=None, ringer=True, dialTone=True, ringerMessage=True,
                 wrongNumberMessage=True, wrongNumberFile='wrong Number File.mp3', isActive=False):
        self.number = number
        self.name = name
        self.ringer = ringer
        self.dialTone = dialTone
        self.ringerMessage = ringerMessage
        self.wrongNumberMessage = wrongNumberMessage
        self.wrongNumberFile = wrongNumberFile
        self.isActive = isActive

    def returnPhoneSettingsList(self):
        returnList = [self.number, self.name, self.ringer, self.dialTone, self.ringerMessage, self.wrongNumberMessage,
                      self.wrongNumberFile, self.isActive]
        return returnList


class trigger:
    def __init__(self, number=None, id=None, name=None, unlockCode=None, isActive=False, triggerMessage=None,
                 relayMode=None, relayActiveTime=1, relayMessageTiming=0,
                 messageFile='message file name.mp3'):
        self.number = number
        self.id = id
        self.name = name
        if (unlockCode is None):
            self.unlockCode = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '*', '#']
        else:
            self.unlockCode = list(unlockCode)
        self.isActive = isActive
        self.triggerMessage = triggerMessage
        self.relayMode = relayMode
        self.relayActiveTime = relayActiveTime
        self.relayMessageTiming = relayMessageTiming
        self.messageFile = messageFile

    def returnTriggerValuesList(self):
        returnList = [self.number, self.id, self.name, self.unlockCode, self.isActive, self.triggerMessage, self.relayMode,
                      self.relayActiveTime, self.relayMessageTiming,
                      self.messageFile]
        return returnList

