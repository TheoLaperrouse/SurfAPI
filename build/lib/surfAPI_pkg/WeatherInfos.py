
class WeatherInfos:
    """Résultat pour chaque jour de la requête"""

    def __init__(self):
        self.valueWeather = ''
        self.hours = ''
        self.date = 0
        self.location = ''
        self.vitesseVent = 0
        self.directionVent = ''
        self.tempEau = ''
        self.tempExt = ''
        self.periode = 0
        self.houle = 0
        self.score = 0

    def updateScore(self):
        score = 0
        if self.houle > 1.0:
            score += 1
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
        if self.vitesseVent > 15:
            score -= 1
        if (self.directionVent == 'NNE' or self.directionVent == 'N' or self.directionVent == 'NNO'):
            score += 3
        elif(self.directionVent == 'NO' or self.directionVent == 'NE' or self.directionVent == 'ONO' or self.directionVent == 'ENE'):
            score += 1
        elif(self.directionVent == 'S' or self.directionVent == 'SSE' or self.directionVent == 'SSO'):
            score -= 1
        self.score = score
