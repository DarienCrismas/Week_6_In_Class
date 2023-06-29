#housing various functions doing differnt things in program, miscellania 

from flask import request, jsonify
from functools import wraps
import secrets
import decimal
import requests
import json

from drone_inventory.models import User


def token_required(our_flask_function):
    @wraps(our_flask_function)
    #could b a number of different things based on api route
    def decorated(*args, **kwargs):
        token = None

        #grab value at key, skipping over Bearer just to get the token
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"].split()[1]
            print(token)

        #returning as key: value pair
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        
        try:
            our_user = User.query.filter_by(token=token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is invalid'}), 401 #Client error 
        except:
            our_user = User.query.filter_by(token=token).first()
            #compare_digest built in secrets function
            if token != our_user.token and secrets.compare_digest(token, our_user.token):
                return jsonify({'message': 'Token is invalid'}), 401
        return our_flask_function(our_user, *args, **kwargs)
    return decorated

#needs to jsonify passed in data, can handle most data.but cannot handle decimals, so we're extending that now
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        #below default referring to default json function 
        return json.JSONEncoder(JSONEncoder, self).default(obj)
    

#dad joke generator
def random_joke_generator():
    url = "https://dad-jokes.p.rapidapi.com/random/joke"

    headers = {
	    "X-RapidAPI-Key": "b8bd7899e7msh07e0ad2abe72116p1374c6jsndbe2e976064c",
	    "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return data["body"][0]["setup"] + " " + data["body"][0]["punchline"]


