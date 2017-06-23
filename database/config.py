import ConfigParser

configParser = ConfigParser.RawConfigParser()   
configFilePath = 'database/.config'
# configFilePath = '.config'
configParser.read(configFilePath)

def getDBStr():
    return configParser.get('my-config', 'db')

if __name__ == "__main__":
    print getDBStr()