import cv2

# Opens the inbuilt camera of laptop to capture video.
cap = cv2.VideoCapture("C:\\Users\pat.surf\\Documents\\third year\\comp 3901\\Homefitness-Ja-main\\vedio_data\\squat.mp4")
i = 0

while(cap.isOpened()):
	ret, frame = cap.read()
	
	# This condition prevents from infinte looping
	# incase video ends.
	if ret == False:
		break
	
	# Save Frame by Frame into disk using imwrite method
	cv2.imwrite('Frame_squat'+str(i)+'.jpg', frame)
	i += 1

cap.release()
cv2.destroyAllWindows()
