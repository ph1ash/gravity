from flask import Flask
from flask_restful import Api, Resource, reqparse
import requests
import json
import numpy as np

app = Flask(__name__)
api = Api(app)

class Url(Resource):
    def get(self):
        return GetPaoUrl(), 200

#@app.route("/")
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
    return (jpgList[selectionValue])

if __name__ == '__main__':
    api.add_resource(Url, "/getPaoUrl")
    #app.run()
    app.run(ssl_context=('/etc/letsencrypt/live/mattdresser.com/fullchain.pem','/etc/letsencrypt/live/mattdresser.com/privkey.pem'), host="0.0.0.0")
