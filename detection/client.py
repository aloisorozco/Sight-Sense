import socket, pickle
import cv2
import argparse
from tkinter import *
from PIL import Image, ImageTk 

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    app = Tk() 

    # Bind the app with Escape keyboard to 
    # quit app whenever pressed 
    app.bind('<Escape>', lambda e: app.quit()) 
    app.title('Sight Sense')
    app.geometry("1920x1080+10+20")

    # Create a label and display it on app 
    label_widget = Label(app) 
    label_widget.pack()

    #message = input(" -> ")  # take input

    while True:
        #client_socket.send(message.encode())  # send message

        data = client_socket.recv(4096)

        print(data)

        frame = pickle.loads(data)
        #data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + frame)  # show in terminal
        
        app.update_idletasks()
        app.update()

        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 

        # Capture the latest frame and transform to image 
        captured_image = Image.fromarray(opencv_image) 

        # Convert captured image to photoimage 
        photo_image = ImageTk.PhotoImage(image=captured_image) 

        # Displaying photoimage in the label 
        label_widget.photo_image = photo_image 

        # Configure image in the label 
        label_widget.configure(image=photo_image) 

        # Repeat the same process after every 10 seconds 
        #label_widget.after(10, open_camera)

        #message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()