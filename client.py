# Client Side Code
# Importing the required libraries
import socket
import urllib              
import pickle              
import numpy as np
import cv2
# URL of mobile webcam
URL = 'http://192.168.29.83:8080/shot.jpg'

# Create socket for client
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip = "192.168.29.193"
port = 6565
client_socket.connect( (ip,port) )
while True:
    get_data = client_socket.recv(10000000)
    print("Response Recieved")
    
    # Open the webcam URL
    get_img = urllib.request.urlopen(URL)
    # Convert img into array
    array_img = np.array(bytearray(get_img.read()) , dtype=np.uint8)
    # Decode img as it is
    img = cv2.imdecode(array_img , -1)
    # Resize the img
    img = cv2.resize(img , (700,500))
    # Store img in buffer
    ret , buffer = cv2.imencode('.jpg' , img)
    # Convert img into bytes form
    bytedata = pickle.dumps(buffer)
    # Send data to the server
    client_socket.send(bytedata)
    try:
        data = pickle.loads(get_data)
        # Decode received img
        final_img = cv2.imdecode(data , cv2.IMREAD_COLOR) 
        if final_img is not None :
            # Show the output window
            cv2.imshow('Client connected' , final_img)
            if cv2.waitKey(10) == 13 :
                break
    except: 
        print("Waiting for the server connection...!")
cv2.destroyAllWindows()