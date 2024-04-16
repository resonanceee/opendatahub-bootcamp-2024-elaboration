# Welcome to the Open Data Hub Bootcamp!
This repo will guide you through the challenge 3, in which you will implement a data elaboration, which uses and writes data to the Open Data Hub.

The goal of this bootcamp is to foster our community around the Open Data Hub, to get to know each other, the technology, but also for you to just learn stuff and make friends. This is not a competition, so don't be afraid to make mistakes and try out new stuff. Our Open Data Hub team is there to help and support you.

While the result of this bootcamp will be a prototype, if the result is convincing, we consider integrating it into the Open Data Hub permanently, so your effort will be a permanent part of the project!

You will also have an opportunity to present the results to the public at our upcoming event, the Open Data Hub Day

## What is an elaboration?
An elaboration is a small application that periodically queries time series data from the Open Data Hub, performs some aggregation or calculation, and then writes the result to the Open Data Hub.

We have elaborations ranging from something as simple as calculating the number of free parking spaces (by subtracting occupied from total capacity) to machine learning models predicting pollution metrics using traffic flow data.

## The challenge
Your challenge will be to implement an elaboration using data from E-charging stations.
You can pick as many things from this list, ordered by increasing difficulty.
We are also open to suggestions if you think you have a cool idea that's not in the list.

- Calculate the average availability percentage of echarging stations, aggregated per hour
- Determine how many times a charging station has been used in a day (number of charging events)
- How long is the average charging duration (aggregated per day)
- Predict the availability of an echarging station within the next hour (free choice of prediction model)

## Tech stack
You are free to use whatever programming language best fits your group, all you need to do is a couple of REST calls and wrangle some JSON.
Ours are written in Java, Python and Go.

We strongly suggest you make your app run in a docker container. This way all group members can develop in a similar environment. It's also how we package our own applications on the Open Data Hub. If you don't know docker, this is a good opportunity to get to know it, and we are happy to help you if you run into any issues.
## Open Data Hub Time Series architecture
There are three APIs you will interact with.
Note that for this challenge you will interact with the `Time Series / Mobility` APIs, and not it's sibling, the `Content / Tourism` domain

### which APIs do I need to use?
In this challenge you will 
- Ask **Keycloak** for an authorization token
- Query the **Ninja API** for e-charging **stations** and their **measurements** of **data type** 'echarging-plug-status'
- Elaborate and aggregate the data
- Push the result to the **BDP API**, along with a new **data type** and a unique **provenance**

### Keycloak
Keycloak is an Open Source Identity and Access management server (keycloak.org).
We use it to authenticate and authorize our services via the OAuth2 standard.
For you, this boils down to making a REST call supplying your credentials (which we will provide to you), and you get back an authorization token.
You then have to pass this token as `Authorization: Bearer <token>` HTTP header on every call to our Open Data Hub APIs.
### Ninja
Ninja is the name of the API you use this to request time series data from the Open Data Hub.
This is where you get your base data from that you elaborate.
The production URL is [mobility.api.opendatahub.com](mobility.api.opendatahub.com)
### BDP
BDP (Big Data Platform) is the API you use to write time series data on the Open Data Hub.
This API is not intended for public use and can only be accessed with authorized credentials.

### Objects and Concepts
Time series data takes the form of `Measurements`.  

__A measurement is a data point with a timestamp.__

Each measurement has exactly one
- `Station`, a geographical points with a name, ID and some additional information. It's the location where measurements are made.
Think a physical e-charging station somewhere on a parking lot. Or a thermometer somewhere in a field. Stations can have a parent station, e.g. a thermometer that is part of a greater weather station
- `Data type`, which, identifies what type of measurement it actually is. Is it a temperature? Is it the number of available cars? Is it the current occupation state of an echarging column? Is it an average, or a discrete value?
- `Provenance`, a unique identifier and version number of the app that provided the measurement.
- `Period`, the timeframe (in seconds) that the measurement references, and the periodicity with which it is updated. e.g. a temperature sensor that sends us it's data every 60 seconds has a period of 60 seconds. 

A **Station** might have measurements of 0-n **Data types**, for example a weather station could have both `temperature` and `humidity` measurements.  
An e-charging station that we know exists, but doesn't provide any real time data, probably has no measurements at all.  
Stations exist independently of measurements.

## Dataset

For this challenge you will use the E-charging datasets, which are part of the Open Data Hub's mobility domain.
To make things simpler, we will limit ourselves to data from only one data provider that has a modest number of stations `origin: DRIVE`.  
If you are feeling adventurous, you can extend it to also include `ALPERIA` and `route220`, 

E-charging stations are organized in two levels:

- station type `EChargingStation` represent a location where one or more EV chargers are located.
- station type `EChargingPlug` represents an individual e-charging column, that is always part of a EChargingStation (it's parent)

The stations have measurements of data type `number-available`, which indicates how many columns are currently available at the location  
The plugs have measurements of data type `echarging-plug-status`, which is 0 or 1, indicating if the column is in use or not 

For most challenges it makes sense to work at the plug level, and then aggregate your result up to station. 
Note that many of our data consumers will want to query on a station level, so you should also provide that data.

## Running a local environment
1. Install docker and docker compose
2. In this directory, run `docker compose up`
3. Wait for the services to start up

If everything is running correctly, you should now have a basic Open Data Hub core running:
|  Service |  Note | Protocol  | Port  |   |
|---|---|---|---|---|
|BDP|time series writer API|http|8081|
|Ninja|time series request API|http|8082|
|Analytics|visual frontend|http|8999|
|Postgis|Postgres database|postgres|5555|

`curl.sh` contains some basic calls so you know it's working.
Refer to the the API documentation and wiki entries linked below for further defails.

For the challenge you will write only to this local instance.

## Authentication
We use Oauth2 for authentication and authorization. 
You will need a valid bearer token to gain write access on the API.
You will probably not need a token to read the data you've wrote from the API.

For this challenge, when using the local instance of the APIs, you can use these credentials:

client_id: odh-mobility-datacollector-development
client_secret: 7bd46f8f-c296-416d-a13d-dc81e68d0830

With these credentials, using the `client_credentials` flow (which effectively means just pass the credentials above in the request) obtain an authentication token from keycloak and add is as `Authorization: Bearer` header

## Documentation Resources
[Swagger Ninja API](mobility.api.opendatahub.com)  
[Ninja API repo](https://github.com/noi-techpark/it.bz.opendatahub.api.mobility-ninja)  
[BDP API swagger](https://swagger.opendatahub.com/?url=https://raw.githubusercontent.com/noi-techpark/bdp-core/main/openapi3.yml)  
[BDP writer repo](https://github.com/noi-techpark/bdp-core)  

[Developing data collectors](https://github.com/noi-techpark/odh-docs/wiki/Getting-started-with-a-new-Data-Collector-development)  
[Some (partly outdated) howtows](https://github.com/noi-techpark/documentation)  

## Example elaborations
In the examples directory you can find a basic prototype of how to push data in python.

The repo with our elaborations can be [found here](https://github.com/noi-techpark/bdp-elaborations)

`parking-free-slot-calculation` is by far the simplest one
