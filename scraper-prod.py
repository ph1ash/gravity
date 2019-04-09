from flask_restful import Resource, reqparse
import requests
import json
import numpy as np
from appId import AppId

class Scraper(Resource):
    def get(self):
        return ValidateAppIdThenRun(GetPaoUrl)

    # def post(self):
    #    args = parser.parse_args()

class Weather(Resource):
    def get(self):
        return ValidateAppIdThenRun(GetWeather)

def ValidateAppIdThenRun(functionToCall):
    parser = reqparse.RequestParser()
    parser.add_argument('appId')
    args = parser.parse_args()
    if (args['appId'] is not None) and (args['appId'] == AppId.id):
        return functionToCall()
    else:
        return {"message": "Invalid App ID provided", "code": "invalidAppId"}

def GetPaoUrl():
    baseUrl = "https://www.artstation.com/users/pao/projects.json"
    pageIdx = 1
    jpgList = []

    while 1:
        page = requests.get(baseUrl + "?page=" + str(pageIdx))
        parseJson = json.loads(page.text)
        # If the data is empty, break out of the loop
        if parseJson['data'] == []:
            break
        else: # Otherwise add the entry into the list
            for entry in parseJson['data']:
                jpgList.append(str(entry['cover']['thumb_url'].encode('utf-8').decode('latin-1')))
                #jpgList.append(str(entry['cover']['micro_square_image_url'].encode('utf-8').decode('latin-1')))
        pageIdx += 1
    selectionValue = int(np.random.uniform(low=0, high=len(jpgList)))
    return (jpgList[selectionValue]), 200

def GetWeather():
    baseUrl = "https://api.openweathermap.org/data/2.5/weather?"
    appId = AppId.weatherApiKey
    parser = reqparse.RequestParser()
    lat = lon = ""
    parser.add_argument('lat')
    parser.add_argument('lon')
    args = parser.parse_args()

    if (args['lat'] is not None) and (args['lon'] is not None):
        try :
            lat = str(np.around(float(args['lat']), decimals=3))
            lon = str(np.around(float(args['lon']), decimals=3))
        except ValueError:
            response = {"message": "lat or lon input is invalid", "code": "badLatLon"}
            return response
        except:
            response = {"message": "Unknown error occured", "code":"weatherUnknown"}
            return response
        baseUrl = baseUrl + "lat=" + lat + "&lon=" + lon + "&appid=" + appId + "&units=imperial"
        page = requests.get(baseUrl)
        parseJson = json.loads(page.text)
        return parseJson
    else:
        return "", 400


def ScraperAddApi(api):
    api.add_resource(Scraper, "/api/artwork")
    api.add_resource(Weather, "/api/weather")
