# ClothingRec-Microservice
This microservice receives real-time weather data and returns a human-readable clothing recommendation.

## Example Call
To request a clothing recommendation, send a JSON string to the microservice over ZMQ to the service's port (default 5556)with the following format: 
```json
{
    "temperature": 30,
    "temperature_unit": "fahrenheit",
    "precipitation_probability": 60,
    "windspeed": 10
}
```

```python
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")
request_data = {
    "temperature": 30,
    "temperature_unit": "fahrenheit",
    "precipitation_probability": 60,
    "windspeed": 10
}
socket.send_string(json.dumps(request_data))
response = socket.recv_string()
```

## Example Response
The microservice will return a JSON string with a "suggestion" key containing the clothing recommendation:
```json
{
    "suggestion": "It's freezing! Wear a heavy coat, gloves, and a hat. There is a high chance of rain, so bring an umbrella or raincoat."
}
```
If the required fields are missing or invalid, the microservice will return an error of the form:
```json
{
    "error": "Invalid data:temperature must be a numeric value."
}
```
