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