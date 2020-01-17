import cv2
import numpy as np

img = cv2.imread('assets/m2.png', 0) # flag can be 0, 1, -1 == grayscale, color, original
print(img) # if the images DNE, img will be None

cv2.imshow('image', img)

cv2.waitKey(0) # the argument is the number of milliseconds before auto-close. 0 makes it infinite.

cv2.destroyAllWindows()

im2_list = []


for i in range(0, img.shape[0]):
	tmp = []
	for j in range(0, img.shape[1]):
		num = img[i][j]

		# if num > 200:
		# 	num = 255

		num = 255-((255-num)/2)
		# print(type(num))
		tmp += [num]

	im2_list += [tmp]

im2 = np.asarray(im2_list, dtype=np.uint8)

print(im2.shape)
print(img.shape)

cv2.imshow('image', im2)

cv2.waitKey(0)

cv2.imwrite('assets/aman_copy.png', img)

cv2.destroyAllWindows()
