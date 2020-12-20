import requests
import sys
#jwt key = paczexpol123paczexpol123paczexpol123
jwt_header = {"Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDg0Nzc3NjYsIm5iZiI6MTYwODQ3Nzc2NiwianRpIjoiYjAwMmU4MzktNTJhYi00MDQ0LWIwNjAtNDUwNGRkMTNhMzE3IiwiZXhwIjozNDAwNDc4NjY2LCJpZGVudGl0eSI6ImNvdXJpZXIwMDEiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.S1SDIay7nMes7vNX1u1zBvq-IBnTky-2i2N6sTJ4j94"}
api_url = "https://paczex-api.herokuapp.com"

def print_all_packages():
    packages = get_packages()
    print_packages(packages);

def get_packages():
    try:
        response = requests.get(api_url+'/sender/packages', headers=jwt_header).json()
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
        response = requests.put(api_url+f'/sender/package/{packageID}',headers=jwt_header).json()
    except:
        return print("Couldn't connect to API")
    print('Update status: ' + response['msg'])

if __name__ == '__main__':
    print('Paczex-Pol courier console app\n')
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
            print('exit - quits console app')
        elif command[0] == 'exit':
            break
        else:
            print('Error: Unknown command.')