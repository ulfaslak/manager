from __future__ import division
from random import randrange

def location_coordinates():
    noise = randrange(-10,10)/100
    latitude = 34.043300 + noise
    longitude = -118.247829 + noise

    LOCATION_COORDINATES = '\'lat\': ' + '\'' + str(latitude) + '\'' + ", " + '\'long\': '  + '\'' + str(longitude) + '\''

    array = [latitude, longitude, LOCATION_COORDINATES]
    
    return array
 
