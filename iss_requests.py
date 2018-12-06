import requests, datetime


def get_astronauts():

    response = requests.get("http://api.open-notify.org/astros.json")
    response = response.json()

    prepareAstronautsPhrase = []
    makeAstronautsNumberSentence = 'Currently, there are {numberOfPeople} people in Space!\n'.format(numberOfPeople=response['number'])

    for astronaut in response['people']:
        makeSentence = '{astronautName} on {astronautCraft} craft.\n'.format(astronautName=astronaut['name'], astronautCraft=astronaut['craft'])
        prepareAstronautsPhrase.append(makeSentence)

    astronautNamesPhrase = ''.join(prepareAstronautsPhrase)

    responsePhrase = makeAstronautsNumberSentence + astronautNamesPhrase

    return responsePhrase


def get_nextISSpasses(lat, lon):

    preparePhrase = []
    parameters = {'lat': lat, 'lon': lon}
    response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
    response = response.json()

    makeSentence = 'Find next passes below:\n'

    for nextpass in response['response']:
        timestamp = datetime.datetime.fromtimestamp(nextpass['risetime'])
        duration = nextpass['duration']
        minutes, seconds = divmod(duration, 60)
        if seconds < 10:
            seconds = str(seconds)
            seconds = seconds.zfill(2)
        prepareStatement = 'Date {datetime}, will last {minutes}:{seconds}'.format(datetime=timestamp.strftime('%d-%m-%Y, time %H:%M:%S'), minutes=minutes, seconds=seconds)

        preparePhrase.append(prepareStatement)

    prepareResponse = '\n'.join(preparePhrase)

    finalResponse = makeSentence + prepareResponse

    return finalResponse
