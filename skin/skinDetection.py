import numpy as np
import cv2
from skin.faceDetection import get_skin_color
from skin.face_landmark_detection import getEyesMouth
from skin.otherFaceDetection import new_skin_color

def skinRange(H,S,V):
	e8 = (H<=25) and (H>=0)
	e9 = (S<174) and (S>58)
	e10 = (V<=255) and (V>=50)
	return (e8 and e9 and e10)

def doDiff(img,want_color1,skin_color,size):
	diff01=want_color1[0]/skin_color[0]
	diff02=(255-want_color1[0])/(255-skin_color[0])
	diff03=(255*(want_color1[0]-skin_color[0]))/(255-skin_color[0])
	diff11=want_color1[1]/skin_color[1]
	diff12=(255-want_color1[1])/(255-skin_color[1])
	diff13=(255*(want_color1[1]-skin_color[1]))/(255-skin_color[1])
	diff21=want_color1[2]/skin_color[2]
	diff22=(255-want_color1[2])/(255-skin_color[2])
	diff23=(255*(want_color1[2]-skin_color[2]))/(255-skin_color[2])
	diff1=[diff01,diff11,diff21]
	diff2=[diff02,diff12,diff22]
	diff3=[diff03,diff13,diff23]
	for  i in range(size[0]):
		for j in range(size[1]):
			doDiffHelp(img,i,j,skin_color,diff1,diff2,diff3)

def doDiffHelp(img,i,j,skin_color,diff1,diff2,diff3):
	for k in range(3):
		if(img[i,j,k]<skin_color[k]):
			img[i,j,k]*=diff1[k]
		else:
			img[i,j,k]=(diff2[k]*img[i,j,k])+diff3[k]

def make_lower_upper(skin_color,Hue,Saturation,Value):	
	if(skin_color[0]>Hue):
		if(skin_color[0]>(180-Hue)):
			if(skin_color[1]>Saturation+10):
				lower1=np.array([skin_color[0]-Hue, skin_color[1]-Saturation,Value], dtype = "uint8")
				upper1=np.array([180, 255,255], dtype = "uint8")
				lower2=np.array([0, skin_color[1]-Saturation,Value], dtype = "uint8")
				upper2=np.array([(skin_color[0]+Hue)%180, 255,255], dtype = "uint8")
				return (True,lower1,upper1,lower2,upper2)
			else:
				lower1=np.array([skin_color[0]-Hue, 10,Value], dtype = "uint8")
				upper1=np.array([180, 255,255], dtype = "uint8")
				lower2=np.array([0, 10,Value], dtype = "uint8")
				upper2=np.array([(skin_color[0]+Hue)%180, 255,255], dtype = "uint8")
				return (True,lower1,upper1,lower2,upper2)
		else:
			if(skin_color[1]>Saturation+10):
				lower=np.array([skin_color[0]-Hue, skin_color[1]-Saturation,Value], dtype = "uint8")
				upper=np.array([skin_color[0]+Hue, 255,255], dtype = "uint8")
				return (False,lower,upper)
			else:
				lower=np.array([skin_color[0]-Hue, 10,Value], dtype = "uint8")
				upper=np.array([skin_color[0]+Hue, 255,255], dtype = "uint8")
				return (False,lower,upper)
	else:
		if(skin_color[1]>Saturation+10):
				lower1=np.array([0, skin_color[1]-Saturation,Value], dtype = "uint8")
				upper1=np.array([skin_color[0]+Hue, 255,255], dtype = "uint8")
				lower2=np.array([180-Hue+skin_color[0], skin_color[1]-Saturation,Value], dtype = "uint8")
				upper2=np.array([180, 255,255], dtype = "uint8")
				return (True,lower1,upper1,lower2,upper2)
		else:
			lower1=np.array([0, 10,Value], dtype = "uint8")
			upper1=np.array([skin_color[0]+Hue, 255,255], dtype = "uint8")
			lower2=np.array([180-Hue+skin_color[0], 10,Value], dtype = "uint8")
			upper2=np.array([180, 255,255], dtype = "uint8")
			return (True,lower1,upper1,lower2,upper2)

def change_skin(image_file,want_color1,output_path):

	# Input the image, convert it to the HSV color space,
	# and determine the HSV pixel intensities that fall into
	# the speicifed upper and lower boundaries
	if(isinstance(image_file,str)):
		img=cv2.imread(image_file,1)
	else:
		img=cv2.imdecode(np.fromstring(image_file.read(), np.uint8),1)
	converted = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	img1=np.float32(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
	size=img.shape

	# Define the upper and lower boundaries of the HSV pixel
	# intensities to be considered 'skin'
	(faceBool,skin_color)=get_skin_color(img)
	if(skin_color[0]==0 and skin_color[0]==0 and skin_color[0]==0):
		lower=np.array([0, 58,50], dtype = "uint8")
		upper=np.array([25, 173,255], dtype = "uint8")
		skinMask=cv2.inRange(converted, lower, upper)
		tmpImage=cv2.bitwise_and(img,img,mask=skinMask)
		skin_color=new_skin_color(tmpImage)
	if(skinRange(skin_color[0],skin_color[1],skin_color[2])):
		Hue=10
		Saturation=65
		Value=50
		result=make_lower_upper(skin_color,Hue,Saturation,Value)
		if(result[0]):
			lower1=result[1]
			upper1=result[2]
			lower2=result[3]
			upper2=result[4] 
			skinMask1=cv2.inRange(converted, lower1, upper1)
			skinMask2=cv2.inRange(converted, lower2, upper2)
			skinMask=cv2.bitwise_or(skinMask1,skinMask2)
		else:
			lower=result[1]
			upper=result[2]
			skinMask = cv2.inRange(converted, lower, upper)

	skinMaskInv=cv2.bitwise_not(skinMask)

	# # OMMITED_STARTS
	# # Apply a series of erosions and dilations to the mask
	# # using an elliptical kernel
	# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
	# skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
	# skinMask = cv2.erode(skinMask, kernel, iterations = 2)

	# # Blur the mask to help remove noise, then apply the
	# # mask to the frame
	# skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
	# # OMITTED_ENDS

	skin_color = np.uint8([[skin_color]])
	skin_color = cv2.cvtColor(skin_color,cv2.COLOR_HSV2RGB)
	skin_color=skin_color[0][0]
	skin_color=np.int16(skin_color)
	want_color1=np.int16(want_color1)

	# Change the color maintaining the texture.
	doDiff(img1,want_color1,skin_color,size)
	img2=np.uint8(img1)
	img2=cv2.cvtColor(img2,cv2.COLOR_RGB2BGR)

	# Get the two images ie. the skin and the background.
	imgLeft=cv2.bitwise_and(img,img,mask=skinMaskInv)
	skinOver = cv2.bitwise_and(img2, img2, mask = skinMask)

	# # Do facial landmark optimisation if possible.
	# skin=np.zeros((size[0],size[1],3))
	# for i in range(size[0]):
	# 	for j in range (size[1]):
	# 		if(faceBool):
	# 			(le,re,mo)=getEyesMouth(img)
	# 			le=np.array(le,dtype=np.int32)
	# 			re=np.array(re,dtype=np.int32)
	# 			mo=np.array(mo,dtype=np.int32)
	# 			if((len(le)>0 and cv2.pointPolygonTest(le,(j,i),False)==-1.0) and (len(re)>0 and cv2.pointPolygonTest(re,(j,i),False)==-1.0) and (len(mo)>0 and cv2.pointPolygonTest(mo,(j,i),False)==-1.0)):
	# 				if np.array_equal(skinOver[i,j,:],[0,0,0]):
	# 					skin[i,j,:]=imgLeft[i,j,:]
	# 				elif np.array_equal(imgLeft[i,j,:],[0,0,0]):
	# 					skin[i,j,:]=skinOver[i,j,:]
	# 				else:
	# 					skin[i,j,0]=imgLeft[i,j,0]*0.5+skinOver[i,j,0]*0.5
	# 					skin[i,j,1]=imgLeft[i,j,1]*0.5+skinOver[i,j,1]*0.5
	# 					skin[i,j,2]=imgLeft[i,j,2]*0.5+skinOver[i,j,2]*0.5
	# 			else:
	# 				skin[i,j,:]=img[i,j,:]
	# 		else:
	# 			if np.array_equal(skinOver[i,j,:],[0,0,0]):
	# 				skin[i,j,:]=imgLeft[i,j,:]
	# 			elif np.array_equal(imgLeft[i,j,:],[0,0,0]):
	# 				skin[i,j,:]=skinOver[i,j,:]
	# 			else:
	# 				skin[i,j,0]=imgLeft[i,j,0]*0.5+skinOver[i,j,0]*0.5
	# 				skin[i,j,1]=imgLeft[i,j,1]*0.5+skinOver[i,j,1]*0.5
	# 				skin[i,j,2]=imgLeft[i,j,2]*0.5+skinOver[i,j,2]*0.5

	skin = cv2.add(imgLeft,skinOver)

	# Return the Byte String of the output image.

	res=cv2.imencode('.jpg',skin)[1].tostring()
	return res
	
# change_skin("1.jpg",[115, 65, 43])