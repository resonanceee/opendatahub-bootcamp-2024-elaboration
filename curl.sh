## Lifted from:
## https://github.com/noi-techpark/odh-docs/wiki/Getting-started-with-a-new-Data-Collector-development

## Get Authorization token
BDP_TOKEN=`curl -X POST -L "https://auth.opendatahub.testingmachine.eu/auth/realms/noi/protocol/openid-connect/token" \
    --header 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode 'grant_type=client_credentials' \
    --data-urlencode 'client_id=odh-mobility-datacollector-development' \
    --data-urlencode 'client_secret=7bd46f8f-c296-416d-a13d-dc81e68d0830'\
| jq -r '.access_token'`

# Some example calls to BDP
curl -X POST -L "http://localhost:8081/json/syncStations/EChargingStation" \
    --header 'Content-Type: application/json' \
    --header "Authorization: bearer ${BDP_TOKEN}" \
    -d '[
          {
            "id": "example-station-id-1",
            "name": "example-station-name-1",
            "origin": "docs-example",
            "latitude": 46.333,
            "longitude": 11.356,
            "municipality": "Bolzano", 
            "metaData" : {
              "additional": "fields"
            }
          },
          {
            "id": "example-station-id-2",
            "name": "example-station-name-2",
            "origin": "docs-example",
            "latitude": 46.333,
            "longitude": 11.356,
            "municipality": "Bolzano", 
            "metaData" : {
              "additional": "fields"
            }
          }
      ]'


# Example ninja call
curl -X GET "http://localhost:8082/tree/ExampleStation" \
     --header 'Content-Type: application/json' \
     --header "Authorization: Bearer ${BDP_TOKEN}"

# and so on... See documentation/swagger for endpoints