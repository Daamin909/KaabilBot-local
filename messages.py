import os
from os import path
import json


homePath = os.path.expanduser("~")
messagesFilePath= "/AppData/Local/Programs/KaabilBot/chat/messages.json"
numberFilePath= "/AppData/Local/Programs/KaabilBot/chat/number.json"
audioFilePath= "/AppData/Local/Programs/KaabilBot/audio"

def numberExist():
    # true if number json file exists
    return path.exists(homePath+numberFilePath)
def messagesExist():
    # true if json file exists
    return path.exists(homePath+messagesFilePath)
def audioExist():
    # true if audio folder exists
    return path.exists(homePath+audioFilePath)
def createNumberFilePath():
    try:
        os.makedirs(path.dirname(homePath+numberFilePath), exist_ok=True)
        with open(homePath+numberFilePath, 'w') as f:
            f.write('{ "number_of_messages": 0 }')
        return True
    except:
        return False
def createMessageFilePath():
    try:
        os.makedirs(path.dirname(homePath+messagesFilePath), exist_ok=True)
        with open(homePath+messagesFilePath, 'w') as f:
            f.write('{ "empty": true }')
        return True
    except:
        return False   
def createAudioFilePath():
    try:
        os.makedirs(path.dirname(homePath+audioFilePath+'/audio.mp3'), exist_ok=True)
        return True
    except:
        return False
def write(data):
    try:
        with open(homePath+messagesFilePath, 'w') as f:
            data_string = json.dumps(data, indent=4)
            f.write(data_string)
        return True
    except:
        return False
def writeNumber(number):
    try:
        with open(homePath+numberFilePath, 'w') as f:
            f.write('{ "number_of_messages": '+str(number)+' }')
        return True
    except:
        return False
def readFile():
    try:
        with open(homePath+messagesFilePath, 'r') as f:
            return f.read()
    except Exception as e: 
        print(e)
        return False
def readNumberFile():
    try:
        with open(homePath+numberFilePath, 'r') as f:
            return f.read()
    except Exception as e:
        print(e)
        return False