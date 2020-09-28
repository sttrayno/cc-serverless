import json
import requests

def main(event, context):

    joke = getJoke()

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(joke)
    }


def getJoke():

    url = "https://icanhazdadjoke.com"
    headers = {
        "Accept":"application/json"
    }

    response = requests.request("GET", url=url, headers=headers)
    return response.json()["joke"]
