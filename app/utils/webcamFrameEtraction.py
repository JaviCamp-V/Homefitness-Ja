import cv2 as cv2


from utils.estimator import estimator,drawkeypoints


def webCam2():
	# Opens the inbuilt camera of laptop to capture video.
	cap = cv2.VideoCapture(0)
	i = 0
	while cv2.waitKey(1) < 0:
		hasFrame, frame = cap.read()
		if not hasFrame:
			cv2.waitKey()
			break
		points=estimator(frame)
		frame=drawkeypoints(points,frame)
		# Save Frame by Frame into disk using imwrite method
		cv2.imwrite('webcam_test-'+str(i)+'.jpg', frame)
		i += 1

	cap.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	webCam2()
