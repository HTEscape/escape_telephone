class telephone:
    def __init__(self, ringer=True, dialTone=True, ringerMessage=True, wrongNumberMessage='wrong Number File.mp3'):
        self.ringer = ringer
        self.dialTone = dialTone
        self.ringerMessage = ringerMessage
        self.wrongNumberMessage = wrongNumberMessage

    def unlockTrigger(self, unlockCode=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '*', '#'], isActive=False, triggerMessage=None,
                 relayMode=None, relayActiveTime=1,  relayActive=False, relayTimer=0, relayMessageTiming=0,
                 messageFile='message file name.mp3'):
        self.unlockCode = unlockCode
        self.isActive = isActive
        self.triggerMessage = triggerMessage
        self.relayMode = relayMode
        self.relayActiveTime = relayActiveTime
        self.relayActive = relayActive
        self.relayTimer = relayTimer
        self.relayMessageTiming = relayMessageTiming
        self.messageFile = messageFile
