import zmq
import json

def get_clothing_suggestion(data):
    # Extract values from the generic weather JSON
    temp = data.get("temperature", 70)
    unit = data.get("temperature_unit", "fahrenheit").lower()
    prob_rain = data.get("precipitation_probability", 0)
    wind_speed = data.get("windspeed", 0)

    #convert temperature to Fahrenheit if it's in Celsius
    if unit == "celsius":
        temp = (temp * 9/5) + 32
    
    suggestions = []

    # Temperature Logic 
    if temp < 40:
        suggestions.append("It's freezing! Wear a heavy coat, gloves, and a hat.")
    elif temp < 60:
        suggestions.append("It's chilly; a jacket or sweater is recommended.")
    else:
        suggestions.append("The weather is warm; light clothing is fine.")

    # Rain Logic 
    if prob_rain > 50:
        suggestions.append("There is a high chance of rain, so bring an umbrella or raincoat.")
    elif 20 <= prob_rain <= 50:
        suggestions.append("It might rain; consider a waterproof layer.")

    # Wind Logic
    if wind_speed > 18:
        suggestions.append("It's windy; a windbreaker or layered clothing would help.")

    return " ".join(suggestions)

def start_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")  # Port for the clothing service
    print("Clothing Suggestion Service is running...")

    while True:
        # Receive JSON string from another service/app
        message = socket.recv_string()        
        try:
            data = json.loads(message)            
            response_text = get_clothing_suggestion(data)      
            socket.send_string(json.dumps({"suggestion": response_text}))
        except Exception as e:
            # Error Pattern for the group
            socket.send_string(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    start_server()