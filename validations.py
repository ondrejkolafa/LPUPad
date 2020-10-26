# import regexp
import re
# import kontroly VINu
import vinlib
# import validace datumu
from datetime import datetime

def validateValue(item):
    "Validace hodnot klíčových slov (napr. platnost rodneho cisla). Vstup ve formátu key - value"
    if len(item[1]) > 0:

        if item[0].upper() == "RC":
            return rc(item[1])
        elif item[0].upper() == "TEL":
            return tel(item[1])
        elif item[0].upper() == "PS":
            return ps(item[1])
        elif item[0].upper() == "IC":
            return ico(item[1])
        elif item[0].upper() == "ICO":
            return ico(item[1])
        elif item[0].upper() == "VIN":
            return vin(item[1])
        elif item[0].upper() == "EMAIL":
            return email(item[1])
        elif item[0].upper() in ("JMENO", "INFO"):
            return textValue(item[1:])
        elif item[0].upper() == "UCET":
            return bankAccount(item[1])
        elif item[0].upper() == "DATUM":
            return datum(item[1:3])

    return ("?", item[1])


def textValue(text):
    return ("?", " ".join(text))


def rc(rc):
    "Validace rodného čísla"
    rc = rc.replace("/", "")
    try:
        int(rc)
    except ValueError:
        return ("nok", rc)

    rcLength = len(rc)
    rcYear = rc[:2]
    rcMonth = rc[2:4]
    rcDay = rc[4:6]

    rcMod = 0
    if rcLength == 10 :
        rcMod = int(rc) % 11

    if (

        9 <= rcLength <= 10
        and 0 <= int(rcYear) <= 99
        and (
            0 <= int(rcMonth) <= 12
            or 21 <= int(rcMonth) <= 32
            or 51 <= int(rcMonth) <= 62
            or 71 <= int(rcMonth) <= 82
            )
        and 1 <= int(rcDay) <= 31
        and rcMod == 0

        ) :
        return ("ok", rc)

    else:
        return ("nok", rc)



def tel(telItem):
    "Validace telefonního čísla"
    if telItem.find("+") == 0:
        correctLength = 13
    else:
        correctLength = 9

    try:
        int(telItem)
    except ValueError:
        return ("nok", telItem)

    telLength = len(telItem)

    if telLength == correctLength:
        return ("ok", telItem)
    else:
        return ("nok", telItem)


def ps(psItem):
    "Validace čísla smlouvy"
    # deset po sobě jdoucích číslic
    psValid = bool(re.match(r"^(\d{10})$", psItem))
    if psValid:
        return ("ok", psItem)
    else:
        return ("nok", psItem)


def email(emailItem):
    "Validace čísla smlouvy"
    # deset po sobě jdoucích číslic
    emailValid = bool(re.match(r"[^@]+@[^@]+\.[^@]+", emailItem))
    if emailValid:
        return ("ok", emailItem)
    else:
        return ("nok", emailItem)


def ico(icoItem):
    "Validace IČa"
    # osm po sobě jdoucích číslic
    icoValid = bool(re.match(r"^(\d{8})$", icoItem))
    if icoValid:
        return ("ok", icoItem)
    else:
        return ("nok", icoItem)


def vin(vinItem):
   " Validace VIN čísla. K validaci se používá balíček https://pypi.org/project/vinlib/ "
   vinValid = vinlib.check_vin(vinItem)
   if vinValid:
       return ("ok", vinItem)
   else:
       return ("nok", vinItem)



def baModulus(baNum):
    checkNum = [1, 2, 4, 8, 5, 10, 9, 7, 3, 6, 1, 2, 4, 8, 5, 10, 9, 7, 3, 6]
    try :
        int(baNum)
    except :
        return (False)
    baNum = [int(d) for d in str(baNum)]
    baNumChecked = []
    for i in range(len(baNum)) :
        baNumChecked.append(baNum[i] * checkNum[i])
    print("Ciferný součet validace čísla:",sum(baNumChecked))
    if sum(baNumChecked) % 11 == 0 : return(True)
    else : return(False)


def bankAccount(baItem):
    baItemShort = baItem.split("/")[0]
    firstNum = baItemShort.split("-")[0][::-1].replace("/", "") # Zvol předčíslí a obrať jeho pořadí
    print("firstNum", firstNum)
    if len(baItemShort.split("-")) == 1:
        if baModulus(firstNum): return ("ok", baItem)
        else : return ("nok", baItem)
    elif len(baItemShort.split("-")) == 2:
        secondNum = baItem.split("-")[1][::-1] # Zvol druhé číslo a obrať jeho pořadí a odstraň lomeno
        print("secondNum", secondNum)
        if baModulus(firstNum) and baModulus(secondNum) : return ("ok", baItem)
        else : return ("nok", baItem)



def datum(dItem):
    print("dItem",dItem)
    datum = ("").join(dItem)
    print("datum", datum)
    datum = datum.replace(".", "").replace( "/", "").replace("-", "").replace(":", "").replace(" ", "")
#    print(datum)
    if len(datum) == 8 :
        try:
            datum = datetime.strptime(datum, '%d%m%Y')
#            print(datum.strftime('%d.%m.%Y'))
            return ('ok', str(datum.strftime('%d.%m.%Y')))
        except ValueError :
            return ('nok', dItem)
    elif len(datum) == 12 :
        try:
            datum = datetime.strptime(datum, '%d%m%Y%H%M')
#            print(datum.strftime('%d.%m.%Y'))
            return ('ok', str(datum.strftime('%d.%m.%Y %H:%M')))
        except ValueError :
            return ('nok', dItem)
    else: return ('nok', dItem)

