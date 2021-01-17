import requests
import http.client
import json
import jwt
from decouple import config

PREGENERATED_JWT = config("PREGENERATED_JWT")
API_URL = config("API_URL")
AUTH0_CLIENT_SECRET = config("AUTH0_CLIENT_SECRET")
AUTH0_CLIENT_ID = config("AUTH0_CLIENT_ID")

def print_all_packages():
    packages = get_packages()
    print_packages(packages);

def get_packages():
    try:
        response = requests.get(API_URL+'/sender/packages', headers=jwt_header).json()
    except:
        return print("Couldn't connect to API")

    return response['_embedded']['packages']

def print_packages(packages):
    i = 1
    for package in packages:
        print(f"{i}. Name: {package['name']}, Locker ID: {package['lockerID']}, Size: {package['size']}, Status: {package['status']}, Package ID: {package['uuid']}")
        i = i + 1

def update_packages(packageID):
    try:
        response = requests.put(API_URL+f'/sender/package/{packageID}',headers=jwt_header).json()
        print('Update status: ' + response['msg'])
    except:
        print("Couldn't connect to API")

if __name__ == '__main__':
    print('Paczex-Pol courier console app\n')

    while True:
        print('Enter email (courier1@pw.edu.pl):')
        username = input()
        print('Enter password (haslo123.):')
        password = input()

        conn = http.client.HTTPSConnection("2021.eu.auth0.com")

        payload = {"client_id":"yyFpfXiwQ9OrYGWpXfcISeyPnEbTaN3L", "client_secret":"T_euP2wBikEt7Ge13b1GiQy6NtFUKUo4f_5xtHBivwf2n5FSv6bmeAHvxb9_3zgz","audience":"https://paczex-api.herokuapp.com/", "grant_type":"password", "username":username, "password":password, "scope":"openid"}

        headers = {'content-type': "application/json"}

        conn.request("POST", "/oauth/token", json.dumps(payload), headers)

        res = conn.getresponse()
        data = res.read()
        data = eval(data.decode("utf-8"))
        if 'error' in data.keys():
            print("Error message: " + data['error'])

        if 'access_token' in data.keys() and 'id_token' in data.keys():
            access_token = data['access_token']
            id_token = data['id_token']
            break;

        print('Try again!\n\n')

    jwt_content = jwt.decode(id_token,AUTH0_CLIENT_SECRET,audience = AUTH0_CLIENT_ID ,algorithms=["HS256"])
    user = jwt_content['name']
    if user != 'courier1':
        jwt_header = {"Authorization": "Bearer " + PREGENERATED_JWT}

    print("Welcome " + user + "!")
    print('List of all packages:')
    print_all_packages()
    while True:
        print('Enter command:')
        command = input().split(' ')
        if command[0] == 'print':
            print_all_packages()
        elif command[0] == 'update':
            update_packages(command[1])
        elif command[0] == 'help':
            print('All avaiable commands:')
            print('update {package ID} - updates package status')
            print('print - prints all registered packages')
            print('tokens - print auth0 jwt')
            print('exit - quits console app')
        elif command[0] == 'tokens':
            print('Identity token: ' + id_token)
            print('Access token: ' + access_token)
        elif command[0] == 'exit':
            break
        else:
            print('Error: Unknown command.')