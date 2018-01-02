import cv2
from skin.faceDetection import get_skin_color
from skin.otherFaceDetection import new_skin_color

def obtain_skin_color(image_file):
	if(isinstance(image_file,str)):
		img=cv2.imread(image_file,1)
	else:
		img=cv2.imdecode(np.fromstring(image_file.read(), np.uint8),1)
	converted = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# Define the upper and lower boundaries of the HSV pixel
	# intensities to be considered 'skin'
	(_,skin_color)=get_skin_color(img)
	if(skin_color[0]==0 and skin_color[0]==0 and skin_color[0]==0):
		lower=np.array([0, 58,50], dtype = "uint8")
		upper=np.array([25, 173,255], dtype = "uint8")
		skinMask=cv2.inRange(converted, lower, upper)
		tmpImage=cv2.bitwise_and(img,img,mask=skinMask)
		skin_color=new_skin_color(tmpImage)

	return skin_color