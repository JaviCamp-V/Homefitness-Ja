import cv2 # Import opencv 
from imutils.video import WebcamVideoStream
from app.utils.estimator import estimator,drawkeypoints



class WebCam(object):
    def __init__(self,source=0):
        self.stream=WebcamVideoStream(src=source).start()
    def __del__(self):
        self.stream.stop()
    def stop():
        self.stream.stop()
    def get_frame(self):
        image=self.stream.read()
        ret,jpeg=cv2.imencode('.jpg',image)
        #y=estimator(image)
        #print(y)
        data=[]
        data.append(jpeg.tobytes())
        return data


