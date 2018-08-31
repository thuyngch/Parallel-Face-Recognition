#------------------------------------------------------------------------------
#   Import
#------------------------------------------------------------------------------
import cv2
import numpy as np
from face_recognition import face_locations, face_encodings
from fnc.matching import matching


#------------------------------------------------------------------------------
#   Draw face localtions on an image
#------------------------------------------------------------------------------
def draw_face_locations(img, face_locs):
	corner1 = None
	corner2 = None
	len_locs = len(face_locs)
	if len_locs:
		corner1 = np.zeros([len_locs, 2], dtype=int)
		corner2 = np.zeros([len_locs, 2], dtype=int)
		cl_blue = (255, 0, 0)
		i = 0
		for (x,y,w,h) in face_locs:
			c1 = (h, x)
			c2 = (y, w)
			corner1[i,:] = c1
			corner2[i,:] = c2
			cv2.rectangle(img, c1, c2, cl_blue, 3)
			i += 1
	return img, corner1, corner2


#------------------------------------------------------------------------------
#   Main
#------------------------------------------------------------------------------
ft_path = "template/"
threshold = 0.4
cap = cv2.VideoCapture(0)

while True:
	# Detect face
	ret, img = cap.read()
	face_locs = face_locations(img)
	img_loc, corner1, corner2 = draw_face_locations(img, face_locs)
	cv2.imshow("Facial Recognition System", img_loc)

	# Encode face
	if corner1 is not None:
		for face_loc in face_locs:
			x = face_loc[0];	y = face_loc[1]
			w = face_loc[2];	h = face_loc[3]
			face = img[x:w+1, h:y+1]
			face_code = face_encodings(face)
			flg, name, _ = matching(face_code, ft_path, threshold)
			if flg:
				print(name, "is recognized")

	# Exit
	k = cv2.waitKey(5) & 0xff
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()