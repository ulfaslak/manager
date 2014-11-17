from __future__ import division
from random import randrange

def location_coordinates():
    noise = randrange(-10,10)*2/100
    latitude = 37.761915 + noise
    longitude = -122.444467 + noise

    LOCATION_COORDINATES = '\'lat\': ' + '\'' + str(latitude) + '\'' + ", " + '\'long\': '  + '\'' + str(longitude) + '\''

    array = [latitude, longitude, LOCATION_COORDINATES]
    
    return array
 
