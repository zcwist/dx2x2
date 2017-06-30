import ConfigParser
import os

dir = os.path.dirname(__file__)

configParser = ConfigParser.RawConfigParser()   
configFilePath = os.path.join(dir,"../database/.config")
configParser.read(configFilePath)

def getDBStr():
    return configParser.get('my-config', 'db')

if __name__ == "__main__":
    print getDBStr()