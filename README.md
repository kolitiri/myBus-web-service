# MyBus Web Service

This is a flask API that was created to support the [MyBus Garmin watch app](https://github.com/chris220688/garmin-myBus-app).

It acts as a proxy service between the watch and TFL's endpoints.

Requests from the Garmin app go through this service and their responses are filtered before they return to the watch app.

This way I can control the size of the responses and avoid crashing the watch application. (It can only handle responses of limited size)

All the requests are forwarded to the TFL's unified API that can be found [here](https://api.tfl.gov.uk/)

# API Usage

Currently there are only to requests that are supported:

## Bus stops request

* **URL:** /stops

* **Method:** POST

* **Data**

```json
{
	"location": {
		"latitude": "51.492628",
		"longtitude": "-0.223060",
		"radius": "200",
		"stopTypes": "NaptanPublicBusCoachTram",
		"returnLines": "False"
	}
}
```

* **Sample Call:**
```
curl --header "Content-Type: application/json" --request POST --data @stops.json https://gmmybus.tk/stops
```

## Bus predictions request

* **URL:** /predictions

* **Method:** POST

* **Data**

```json
{
	"stop": {
		"naptanId": "490004290L"
	}
}
```

* **Sample Call:**
```
curl --header "Content-Type: application/json" --request POST --data @predictions.json https://gmmybus.tk/predictions
```

### Acknowledgements

This application is Powered by TfL Open Data and contains OS data © Crown copyright and database rights 2016

### Authors

Chris Liontos
