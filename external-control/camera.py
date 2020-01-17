import cv2

cap = cv2.VideoCapture(0) # arg is the device index of camera. Usually 0 or -1.
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while True:
	ret, frame = cap.read() # ret is true/false for if the frame is available.

	if ret:
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		cv2.imshow('frame', gray)

		out.write(frame)


		if cv2.waitKey(1) & 0xFF == ord('q'):
			break;
	else:
		break

	

cap.release()
out.release()
cv2.destroyAllWindows()