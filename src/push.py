import requests

def push_data(url, data, auth_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }

    response = requests.post(url, json=data, headers=headers)
    return response

def get_auth_token():
    auth_url = "https://auth.opendatahub.testingmachine.eu/auth/realms/noi/protocol/openid-connect/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': 'odh-mobility-datacollector-development',
        'client_secret': '7bd46f8f-c296-416d-a13d-dc81e68d0830',
        'scope': 'openid'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(auth_url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Error getting auth token: {response.text}")
        return None

def main():
    url = "http://localhost:8081/json/pushRecords"
    data = {
        "name": "(default)",
        "branch": {
            "termperature-station-id-1": {
                "name": "(default)",
                "branch": {
                    "temperature": {
                        "name": "(default)",
                        "branch": {},
                        "data": [
                            {
                                "timestamp": 1668522653400,
                                "value": 1234,
                                "period": 100,
                                "_t": "it.bz.idm.bdp.dto.SimpleRecordDto"
                            }
                        ]
                    }
                },
                "data": []
            }
        },
        "data": [],
        "provenance": "provenance_id"
    }

    auth_token = get_auth_token()
    if auth_token:
        response = push_data(url, data, auth_token)
        print(f"Status Code: {response.status_code}")

main()