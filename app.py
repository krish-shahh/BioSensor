# Import the library
import grandeur.device as grandeur
import time
import threading

# Define the apiKey and Auth token
apiKey = "grandeurlvcg71200dja0jifadqx7zug"
token = "37460718c7b237cd5a252abdcf184677a881d8ef029fe20d75e5252ebe2c8a3e"
deviceID = "devicelvciwtip0isa0jif5kes0tb9"

# Event listener on connection state
def onConnection(state):
    # Print the current state
    print(state)

# Callback function to handle state change event
def updateHandler(path, state):
    # Print
    print(data)

# Callback function to handle current state
def dataHandler(code, res):
    # Print
    print(res["data"])

# Init the SDK and get reference to the project
project = grandeur.init(apiKey, token)

# Place listener
project.onConnection(onConnection)

# Get a reference to device class
device = project.device(deviceID)

# Function to fetch data every 5 seconds
def fetchData():
    while True:
        # Get current state
        device.data().get("millis", dataHandler)
        time.sleep(5)

# Start the data fetching loop in a new thread
fetch_thread = threading.Thread(target=fetchData)
fetch_thread.daemon = True
fetch_thread.start()

# Block main thread
while True:
    pass
