from skin.skinDetection import change_skin
from skin.noFaceSkinDetection import obtain_skin_color
import cv2
import numpy as np
import argparse

if __name__ == "__main__": 
	parser=argparse.ArgumentParser()
	parser.add_argument("which", help="Color Change or Skin Match?")
	parser.add_argument("img", help="Image to be changed")
	parser.add_argument("col", help="Required skin color or the OTHER image")
	parser.add_argument("res", help="Path where image is to be saved")
	args=parser.parse_args()

	with open(args.img,'rb') as inputImage:
		if(args.which=="color"):
			a=args.col.strip('[] ')
			b=a.split(',')
			result=change_skin(inputImage,[int(b[0].strip()),int(b[1].strip()),int(b[2].strip())])
		elif(args.which=="image"):
			color=obtain_skin_color(args.col)
			color=np.uint8([[color]])
			color=cv2.cvtColor(color,cv2.COLOR_HSV2RGB)
			color=color[0][0]
			result=change_skin(inputImage,color,args.res)
		else:
			print("Please enter correct detection type.")

	with open(args.res,'wb') as resultFile:
		resultFile.write(result)