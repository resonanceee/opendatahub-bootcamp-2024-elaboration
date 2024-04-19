import requests
import json

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx

        # If the response was successful, parse the data
        data = response.json()

        # TODO: Process the data as needed

        return data  # Return the data

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as err:
        print(f'Error occurred: {err}')
    except ValueError:
        print('Response content is not in JSON format.')
    except Exception as e:
        print(f'An error occurred: {e}')

# TODO: Replace with your actual URL
url = "https://mobility.api.opendatahub.com/v2/flat/EChargingStation?limit=200&offset=0&shownull=false&distinct=true"

response = requests.get('https://mobility.api.opendatahub.com/v2/flat/EChargingPlug?limit=-1&offset=0&shownull=false&distinct=true&where=sactive.eq.true&')

response_dict = response.json()

# Pretty Printing JSON string back
print(json.dumps(response_dict, indent=4, sort_keys=True))

print(fetch_data(url))
