import cv2
from imutils.video import WebcamVideoStream



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
        data=[]
        data.append(jpeg.tobytes())
        return data


