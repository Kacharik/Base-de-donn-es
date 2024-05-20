import os
def notSpecialChar(chaine):
    caracteres_speciaux = "!@#$%^&*()-_+=[]{}|;:',.<>?`~"
    for caractere in chaine:
        if caractere in caracteres_speciaux:
            return False
    return True

def isDigit(chaine):
    number = "1234567890"
    for caractere in chaine:
        if caractere not in number:
            return False
    return True

def isDate(chaine):
    for caractere in chaine:
        if(caractere != "/"):
            if(not isDigit(caractere)):
                return False
    if(chaine[5] == chaine[8] != "/"):
        return False
    return True


def effacer_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')