Skin Detection
===================


This is a tool which creates a skin color changing effect. It takes an image and a color or another image as input and returns an the first image with the skin color changed to either the given color or the skin color detected from the second image.

Usage
-------------
Clone this repository and run setup.py and requirements.txt. Also install below mentioned dependencies. Then pass the following command-line arguments to \_\_init\_\_.py in **skin** folder.
```
python3 __init__.py color/image path_to_image_to_be_changed color_in_RGB_like_[12,34,56]/path_to_other_image path_where_image_is_to_be_saved
```
- Also instead of the path to image file, Python **File Object** of that image can also be passed in as an argument.
- Similarly instead of writing out output images, the program can also return the **File Object** of the output images.

Examples
-------------
Following are some results of skin color changing :      
![Light](https://raw.githubusercontent.com/KubricIO/skin-detection/master/demos/Light.jpg)
![Dark](https://raw.githubusercontent.com/KubricIO/skin-detection/master/demos/Dark.jpg)
![Very Dark](https://raw.githubusercontent.com/KubricIO/skin-detection/master/demos/VeryDark.jpg)

How It Works
-----------------
1. In the first image, obtain the bounding box around the face (if a face is detected) using **Haar Cascade Frontal Face Classifier**.
2. Apply **k-Means Clustering** to this bounding box to obtain the most dominant color which is assumed to be the skin color.
3. If a face is not detected, then a **"basic"** skin-detection is performed to obtain the skin regions and then k-Means Clustering is applied to these regions to obtain the skin color.
4. Using this skin color, apply a **"better"** skin-detection to the first image to obtain the region of image which is skin.
5. Now using the skin color and the desired color, create a **function** which maps a pixel's color in the original image to what it should be in the final image.
6. Now overlay the skin region on to the original image to obtain a new image which has **skin color changed**.

Requirements
-------------
These are the requirements apart from what is mentioned in *requirements.txt* :

>- X11 (Xquartz on macOS)
>- Boost and Boost-Python
>- Dlib

For macOS : https://www.learnopencv.com/install-dlib-on-macos/     
For Linux : https://www.learnopencv.com/install-dlib-on-ubuntu/      
For Windows : https://www.learnopencv.com/install-opencv-3-and-dlib-on-windows-python-only/

Citations
-------------
Most of the help for this project came from these posts
>- https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/
>- https://stackoverflow.com/questions/8753833/exact-skin-color-hsv-range
