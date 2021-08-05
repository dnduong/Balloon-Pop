import numpy as np
import cv2 
import mediapipe as mp
import math
import random
import balloon
import imageio

def play_game(save_gif = False, save_path = None):
    BALLOONS = []
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    SCORE = 0
    NB_BALLOONS = 5
    VELOCITY = 6
    COLORS = [(0,0,255),
             (0,255,255),
             (255,0,0)]
    
    SIZES = [15,20,25]
    frames = []
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    drawing_styles = mp.solutions.drawing_styles
    # For webcam input:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    for i in range(NB_BALLOONS):
        random_index = random.randint(0,2)
        BALLOONS.append(balloon.Balloon(frame_width,frame_height,VELOCITY,SIZES[random_index],COLORS[random_index]))
        
    with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while True:
            fingers = []
            pixel_coordinates_landmark = (0,0)
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for landmark in results.multi_hand_landmarks :
                    normalized_landmark = landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    pixel_coordinates_landmark = mp_drawing._normalized_to_pixel_coordinates(normalized_landmark.x,
                                                                                        normalized_landmark.y,
                                                                                        frame_width,
                                                                                        frame_height)
                    fingers.append(pixel_coordinates_landmark)
                    
            for b in BALLOONS :
                b.move()
                b.draw(image)
                if b.touch(fingers,2):
                    SCORE += 1
                    b.respawn()
                if b.y < 0:
                    b.respawn()
            
            cv2.putText(image, f'SCORE : {SCORE}', (int(frame_width-200), 50), FONT ,1, (0,0,0), 2)
            if save_gif:
                frames.append(image)
            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(1) == ord('q'):
                break
            
        cap.release()
        cv2.destroyAllWindows()
    if save_gif:
        print("Saving GIF file")
        with imageio.get_writer(save_path, mode="I") as writer:
            for frame in frames:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                writer.append_data(frame)
        
if __name__ == "__main__":
    play_game(save_gif = True, save_path = 'play.gif')