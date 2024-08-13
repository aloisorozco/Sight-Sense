# Sight Sense: Smart DoorBell using ML and Computer Vision
**Created by Alois Orozco, Daniel Grimut, Dom Doesburg, Augusto Moto Pinheiro**


## What is Sight Sense:
For ConuHacks 8, Quebec's largest Hackathon of the past decade, our team created an exceptional tool to increase home security with the help of ML and Computer Vision. SightSence utilizes multiple machine learning models to identify faces and uses mathematical concepts such as the Kalman Filter, IoU (intersect over Union), and the EAR (eye aspect ratio) to perform lighting-fast human authentications without the use of infra-red cameras.


## How we did it:
Our team used a pre-trained computer vision model and fed it multiple images of faces. We used Python and OpenCV to work with the model, and enhance it.


## Why we did it:
Our team cares passionately about making the world a better place. Through our years working together on academic projects, we have discussed our motives behind pursuing Computer Science and we all strongly believed in the great opportunities that software development has to make people's lives better, and safer.


## Features:
# Face Detection
The AI is able to detect faces, and associate unique IDs to each - these IDs make it easy for the admin to select a detected individual to authenticate.
<img width="1468" alt="Screenshot 2024-08-13 at 4 39 48 PM" src="https://github.com/user-attachments/assets/ba955c4a-65e9-4b7c-8fad-ab42be98205d">

To maintain and track IDs was a challenge, as the AI processes and annotates each frame individually. Additionally, we found it inefficient to load a new model to track the faces - we wanted to learn to do this stuff ourselves. So, we used the Kalman Filter to track the faces and IoU to associate the Kalman Predictions to the detected faces at each new frame. 

Kalman Filter is a relatively complex mathematical algorithm, which we certainly had trouble understanding. The filter makes these predictions by considering the object's velocity in 3D space, while also accounting for noise—essentially the variations and uncertainties in parameters like velocity, position, and acceleration. We used the Intersection over Union (IoU) to find the closest match of the newly detected faces, against the Kalman predictions, which allowed us to track the same face, and maintain its ID throughout its existence on the screen. This predictive capability enhances the accuracy and reliability of object-tracking systems and allows us to determine if a detected person disappears from the frame - at which point we halt any authentication process started for that target. In the following image, you can see the Kalman prediction of the center of the new bounding box (blue circle) against the actual position of the face's bounding box (red circle):
<img width="336" alt="Screenshot 2024-08-13 at 4 43 35 PM" src="https://github.com/user-attachments/assets/567be1b6-4f1a-4cf0-a810-c335ecf3bf5e">


# Face Meshing
We used an open-source Face Mesh model from Google to map the facial landmarks on the detected face. This is done after the target has been identified and selected by ID, allowing us to begin the human authentication process (more on it in the next section). It is worth noting, that for efficiency, we isolated the part of the frame that contained the face and only passed that to the model, adjusting the new coordinate system accordingly after the face landmark detection, to display the landmarks on the screen.
<img width="502" alt="Screenshot 2024-08-13 at 4 41 03 PM" src="https://github.com/user-attachments/assets/234e1169-cdf2-4074-86df-e496ab4bbd60">


# Human Authentication
We annihilated the if the target is a human by generating a sequence of blinks the person has to perform, holding each blink for 'n' number of seconds. Using the facial landmarks obtained from our Facial Detection Module, we detected each blink using the Eye-Aspect Ratio (EAR) we learned about in the following paper https://peerj.com/articles/cs-943/.
<img width="502" alt="Screenshot 2024-08-13 at 4 42 13 PM" src="https://github.com/user-attachments/assets/edc7a988-ceda-4a5b-870d-ea13e63ede53">
<img width="822" alt="Screenshot 2024-08-13 at 4 41 49 PM" src="https://github.com/user-attachments/assets/32e10c10-26bd-47a1-b1d2-17141bc08bb8">


# Concurency Control
We utilized asyncio with socketio to create a Python server to host the models and app. Using Locks and Semaphores, we made our app thread-safe allowing multiple users to join the broadcast, but only allowing one (for now) to perform an authentication.
<img width="1465" alt="Screenshot 2024-08-13 at 4 43 17 PM" src="https://github.com/user-attachments/assets/38f6dd14-f026-44cb-b8df-855bcdd94d12">


# Future Plans
We plan the following for the near future:
- Deploy Website
- Port to mobile app
- More cool AI stuff we don't want to spoil (although this repo is public so you probably can figure it out through our code if you want 👀)


# Tech Stack
- Python
- asyncio, socketio
- JS, React
- OpenCV, YOLOv8, Keras, Tensorflow
