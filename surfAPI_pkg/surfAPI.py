import http.client
import json
import csv
import os
from os import system, path
import time
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


URL = 'api.worldweatheronline.com'
api_key = '5b4541479ee849d29a8152452202505'
locations = {}
datas = []
DayWeek = ['Lundi', 'Mardi', 'Mercredi',
           'Jeudi', 'Vendedi', 'Samedi', 'Dimanche']
Month = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
         'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']


class WeatherInfos:
    """Résultat pour chaque jour de la requête"""

    def __init__(self):
        self.valueWeather = ''
        self.hours = ''
        self.date = 0
        self.location = []
        self.vitesseVent = 0
        self.directionVent = ''
        self.tempEau = 0
        self.tempExt = 0
        self.periode = 0
        self.houle = 0
        self.score = 0
        self.maree = ''

    def updateScore(self):
        score = 0
        if self.maree == 'Montante':
            score += 3
        if self.houle > 1.0:
            score += 10
        elif self.houle > 0.5:
            score += 7
        if self.periode > 11:
            score += 3
        elif self.periode > 8:
            score += 1
        if self.tempEau > 16:
            score += 3
        elif self.tempEau > 12:
            score += 1
        if self.tempExt > 20:
            score += 3
        elif self.tempExt > 12:
            score += 1
        if self.vitesseVent > 30:
            score -= 1
        elif self.vitesseVent > 40:
            score -= 3
        score += self.directionVentScore()
        self.score = score

    def directionVentScore(self):
        if(self.location[2] == 'Nord'):
            if self.directionVent in ['N', 'NNE', 'NNO']:
                return 3
            elif self.directionVent in ['NO', 'ONO', 'NE', 'ENE']:
                return 1
        elif(self.location[2] == 'Sud'):
            if self.directionVent in ['S', 'SSE', 'SSO']:
                return 3
            elif self.directionVent in ['SO', 'OSO', 'SE', 'ESE']:
                return 1
        elif(self.location[2] == 'Ouest'):
            if self.directionVent in ['ONO', 'O', 'OSO']:
                return 3
            elif self.directionVent in ['NO', 'SO', 'NNO', 'SSO']:
                return 1
        elif(self.location[2] == 'Est'):
            if self.directionVent in ['E', 'ENE', 'ESE']:
                return 3
            elif self.directionVent in ['NE', 'SE', 'SSE', 'NNE']:
                return 1
        if(self.location[2] == 'Nord-Ouest'):
            if self.directionVent in ['NO', 'NNO', 'ONO']:
                return 3
            elif self.directionVent in ['O', 'N', 'NNE', 'OSO']:
                return 1
        elif(self.location[2] == 'Nord-Est'):
            if self.directionVent in ['ENE', 'NNE', 'NE']:
                return 3
            elif self.directionVent in ['N', 'E', 'NNO', 'ESE']:
                return 1
        elif(self.location[2] == 'Sud-Ouest'):
            if self.directionVent in ['SO', 'SSO', 'OSO']:
                return 3
            elif self.directionVent in ['O', 'ONO', 'S', 'SSE']:
                return 1
        elif(self.location[2] == 'Sud-Est'):
            if self.directionVent in ['SE', 'SSE', 'ESE']:
                return 3
            elif self.directionVent in ['ENE', 'SSO', 'S', 'E']:
                return 1
        return 0


def sendMail(previsionSurf):
    gmail_user = 'theolaperrousesendmail@gmail.com'
    gmail_password = 'sendmail35235'
    receveir = 'theolaperrouse@gmail.com'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = 'theolaperrouse@gmail.com'
    msg['Subject'] = 'Prévision Sessions Surf pour la semaine'
    body = previsionSurf
    body = MIMEText(body)
    msg.attach(body)

    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, receveir, msg.as_string())
    server.close()


def writeBestSpot():
    global datas
    res = ''
    stringTab = []
    datas = (sorted(datas, key=lambda spotHours: spotHours.score, reverse=True))
    for weatherHours in datas:
        if weatherHours.score > 11:
            stringTab.append(f'''{weatherHours.location[0]}: Score {weatherHours.score}
{weatherHours.date} à {weatherHours.hours}, le vent soufflera vers {weatherHours.directionVent} à {weatherHours.vitesseVent} km/s
{weatherHours.tempExt}°C à l\'extérieur / {weatherHours.tempEau}°C dans l\'eau
Temps : {weatherHours.valueWeather} / Marée {weatherHours.maree}
La houle des vagues est de {weatherHours.houle}m et leur période est de {weatherHours.periode}s
 ''')

    if len(stringTab) == 0:
        res = f'Il n\'y a pas de bonnes sessions à {datas[0].location[0]} pour cette semaine, réessayer plus tard \n'
    else:
        res = '\n'.join(stringTab)
    datas.clear()
    return res


def initSpots():
    global locations
    locations = {}
    if not os.path.exists("./spots/spots.csv"):
        open("./spots/spots.csv", "w")
    fichierSpots = open(f'./spots/spots.csv', 'r')
    spots = csv.reader(fichierSpots, delimiter=';', dialect='excel')
    for spot in spots:
        locations[len(locations)] = [spot[0], spot[1], spot[2]]
    fichierSpots.close()


def addSpot():
    nom_spot = input('Renseigner le nom du spot :\n')
    location = input(
        'Renseigner la localisation du spot sous cette forme 48.15,2.82 (Google Maps est ton ami):\n')
    orientPlage = orientPlage = input(
        'La mer est orienté vers quel point cardinal (Sud,Nord,Est,Ouest,Sud-Ouest,Sud-Est,Nord-Est,Nord-Ouest) :\n')
    while (orientPlage not in ['Sud', 'Nord', 'Est', 'Ouest', 'Sud-Ouest', 'Sud-Est', 'Nord-Est', 'Nord-Ouest']):
        orientPlage = input(
            'Renseignez une valeur dans celle ci Sud,Nord,Est,Ouest,Sud-Ouest,Sud-Est,Nord-Est,Nord-Ouest :\n')
    fichierSpots = open(f'./spots/spots.csv', 'a+', newline='')
    writer = csv.writer(fichierSpots, delimiter=';', dialect='excel')
    writer.writerow([nom_spot, location, orientPlage])
    fichierSpots.close()
    initSpots()


def serverResponse(posLocation):
    conn = http.client.HTTPSConnection(URL)
    payload = ""
    parameters = f"/premium/v1/marine.ashx?q={posLocation}&key={api_key}&lang=fr&format=json&tide=yes&tp=3&num_of_days=7"
    conn.request("GET", parameters, payload)
    res = conn.getresponse().read()
    infosMeteo = json.loads(res)
    return infosMeteo


def parseResponse(infos, spot):
    global datas
    semaineMeteo = infos['data']['weather']
    for jour in semaineMeteo:
        for hours in jour['hourly']:
            weatherHours = WeatherInfos()
            weatherHours.location = spot
            weatherHours.valueWeather = hours['lang_fr'][0]['value']
            weatherHours.date = getJour(jour['date'])
            weatherHours.hours = getHour(hours['time'])
            weatherHours.maree = getTypeMaree(
                weatherHours.hours, jour['tides'][0])
            weatherHours.houle = float(hours['swellHeight_m'])
            weatherHours.periode = float(hours['swellPeriod_secs'])
            weatherHours.tempEau = float(hours['waterTemp_C'])
            weatherHours.tempExt = float(hours['tempC'])
            weatherHours.directionVent = hours['winddir16Point']
            weatherHours.vitesseVent = float(hours['windspeedKmph'])
            weatherHours.updateScore()
            datas.append(weatherHours)


# Ajouter taille des marées : Grand Coeff = Bien --> tide['tideHeight_mt']
def getTypeMaree(hour, tides):
    tidesDay = tides['tide_data']
    heurePrevision = datetime.datetime.strptime(hour, '%H:%M')
    for tide in tidesDay:
        heureMaree = datetime.datetime.strptime(tide['tideTime'], '%I:%M %p')
        if heurePrevision > heureMaree:
            if (tide['tide_type'] == 'HIGH'):
                return 'descendante'
            else:
                return 'montante'


def getHour(hour):
    if(len(hour) == 0 or len(hour) == 3):
        return datetime.datetime.strptime(hour[0], '%H').strftime('%H:%M')
    else:
        return datetime.datetime.strptime(hour[:2], '%H').strftime('%H:%M')


def getJour(date):
    dateTime = datetime.datetime.strptime(date, ('%Y-%m-%d'))
    nomJour = DayWeek[dateTime.weekday()]
    nomMois = Month[dateTime.month-1]
    return f'{nomJour} {dateTime.day} {nomMois}'


def choiceList():
    print("Choisissez l\'un de vos spots préférés en renseignant le nombre qui lui est associé (exemple : 0):")
    for spot in range(0, len(locations)):
        print(f'{spot}°) {locations[spot][0]}')
    return int(input("Choix auxiliaires :\n-1°) Recevoir un mail des Prévisions de la semaine sur vos spots en mode auto tous les jours \n-2°) Ajoutez en un \nVotre choix : "))


def clientChoice():
    system('clear')
    if(len(locations) <= 0):
        print(
            "Vous n'avez pas encore de spots enregistrés, veuillez en enregistrez au moins un :")
        addSpot()
    indexChoice = choiceList()

    if (indexChoice < len(locations) and indexChoice > -1):
        infos = serverResponse(locations[indexChoice][1])
        system('clear')
        parseResponse(infos, locations[indexChoice])
        previsionSurf = writeBestSpot()
        print(previsionSurf)
    elif (indexChoice == -1):
        allSpots()
    elif (indexChoice == -2):
        addSpot()
        clientChoice()

    else:
        print('Le choix renseigné n\'est pas valable !')
        clientChoice()


def allSpots():
    res = []
    for indexSpot in range(0, len(locations)):
        infos = serverResponse(locations[indexSpot][1])
        parseResponse(infos, locations[indexSpot])
        previsionSurf = writeBestSpot()
        res.append(previsionSurf)
    print('\n'.join(res))
    sendMail(previsionSurf)
    time.sleep(60*60*24)
    allSpots()


def main():
    while True:
        clientChoice()
        input('Taper Entrée pour retourner à la liste de choix')


initSpots()
if __name__ == '__main__':
    main()
