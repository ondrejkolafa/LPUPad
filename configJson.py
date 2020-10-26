import json
import os

defaultMotorConfig = {'alwaysOn': 1, 'defaultText': 'RZ \n\nVIN \n\nPS \n\nJMENO \n\nRC \n\nICO \n\nTEL \n\nEMAIL \n\nUCET \n\nINFO \n\nDATUM \n'}

def readConfig(path):
    "Načte config.json z předané cesty. Pokud neexistuje, vytvoří se dafaultní config"
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        with open(path+'\\config.json') as f:
            config = json.load(f)
    except FileNotFoundError:
        global defaultMotorConfig
        config = defaultMotorConfig
    print(config)
    return(config)


def setVzdyNahore(config, flag):
    "Nastaví hodnotu atributu v config knihovně"
    config["alwaysOn"] = flag


def setDefaultText(config, text):
    "Nastaví hodnotu atributu v config knihovně"
    config["defaultText"] = text


def saveConfig(path, config):
    "Uloží do předané cesty konfigurační data"
    with open(path+'\\config.json', 'w') as f:
        json.dump(config, f)

def returnToDefault(path) :
    global defaultMotorConfig
    saveConfig(path, defaultMotorConfig)