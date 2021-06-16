# Server Side Code

# Importing the required libraries
import socket
import pickle
import cv2

# Capturing the video
cap = cv2.VideoCapture(0)

# Create socket for server
server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip="192.168.29.193"
port=6565

server_sock.bind( (ip,port) )
print("Binded successfully !")

server_sock.listen()
print("Listening at-->",ip)
csession , addr = server_sock.accept()
print("Connected to {}".format(addr))

while True:
    ret , photo = cap.read()
    ret, buffer = cv2.imencode(' .jpg',photo)
    bytedata = pickle.dumps(buffer)
    csession.send(bytedata)
   
    get_data = csession.recv(1000000)

    try:
        data = pickle.loads(get_data)
        final_img = cv2.imdecode(data , cv2.IMREAD_COLOR)
        if final_img is not None :
            cv2.imshow('Server connected' , final_img)
            if cv2.waitKey(10) == 13 :
                break
    except:
        print("Waiting for the client request!")
cv2.destroyAllWindows()