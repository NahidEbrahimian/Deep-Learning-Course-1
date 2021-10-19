import cv2
import numpy as np
from config import *
from keras.models import load_model
from retinaface import RetinaFace

model = load_model("weights/model.h5")

video_cap = cv2.VideoCapture(0)
video_cap.set(cv2.CAP_PROP_FPS, 1)

frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))

video_writer = cv2.VideoWriter('GenderClassification.avi', cv2.VideoWriter_fourcc(*'MJPG'), 20, (frame_width, frame_height))

while True:

    rec, frame = video_cap.read()
    if not rec:
        break

    frame_width, frame_height, _ = frame.shape
    face = RetinaFace.extract_faces(img_path=frame, align=True)
    face = face[0]

    if np.all(face != None):
        # cv2.imwrite('face.jpg', face)
        image = cv2.resize(face, (width, height))
        image = image / 255.0
        img2 = image.reshape(1, width, height, 3)

        y_pred = model.predict(img2)
        print(y_pred)
        prediction = np.argmax(y_pred)

        if prediction == 0:
          y_pred = "With Mask"
          color = (255, 0, 0)

        else:
          y_pred =  "Without Mask"
          color = (255, 0, 255)

        cv2.putText(frame, y_pred, (frame_width // 8, frame_height // 8), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2,
                        cv2.LINE_AA)

    cv2.imshow('GenderClassification', frame)
    # video_writer.write(frame_blur)

    if cv2.waitKey(10) == ord('q'):
        break
    elif cv2.waitKey(1) == ord('s'):
        # cv2.imwrite('QrCode-Reader.jpg', frame)
        break

video_cap.release()
video_writer.release()