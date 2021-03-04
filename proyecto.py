from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
from eye import eye_aspect_ratio
from MySQL_Class import MySQL

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")

args = vars(ap.parse_args())

if not args.get("video", False) : 
	camera=cv2.VideoCapture(0)

else: 
	camera = cv2.VideoCapture(args["video"])

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 5

COUNTER = 0 
TOTAL = 0

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Instanciar MySQL
mysql = MySQL()

while True: 
	
	(grabbed, frame) = camera.read()

	if args.get("video") and not grabbed: 
		break
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rects = detector (gray, 1)

	for rect in rects:
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		leftEye = shape [lStart : lEnd]
		righteye = shape [rStart : rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(righteye)

		ear = (leftEAR + rightEAR) / 2.0

		if ear < EYE_AR_THRESH:
			COUNTER += 1

		else:
			if COUNTER >= EYE_AR_CONSEC_FRAMES:
				TOTAL += 1
				mysql.insertdata(1)

			COUNTER = 0

		cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		
		for (x, y) in shape:
			cv2.circle(frame, (x,y), 1, (0, 0, 255), -1)

	cv2.imshow("frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()

