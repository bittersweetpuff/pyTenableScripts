import json

#Function returns tenable.sc adress specified in SC_Data.json file
def GetSCAdress():
    """
    Function returns tenable.sc adress specified in SC_Data.json file
    """
    with open("SC_Data.json", "r") as read_file:
        data = json.load(read_file)
    idValue = data['adress']
    return(idValue)

def GetUser():
    """
    Function returns username specified in SC_Data.json file
    """
    with open("SC_Data.json", "r") as read_file:
        data = json.load(read_file)
    idValue = data['username']
    return(idValue)


def GetPass():
    """
    Function returns password adress specified in SC_Data.json file
    """
    with open("SC_Data.json", "r") as read_file:
        data = json.load(read_file)
    idValue = data['password']
    return(idValue)


def GetNessusConsole():
    """
    Function returns nessus console adress adress specified in SC_Data.json file
    """
    with open("SC_Data.json", "r") as read_file:
        data = json.load(read_file)
    idValue = data['console']
    return(idValue)
