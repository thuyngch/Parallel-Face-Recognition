#------------------------------------------------------------------------------
#   Import
#------------------------------------------------------------------------------
import cv2
import numpy as np
from face_recognition import face_locations, face_encodings
from fnc.matching import isTempExisted
from scipy.io import savemat


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
ft_path = "./template/"
name = input(">>> Please type name of the registration person: ")
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
		len_locs = len(face_locs)
		if len_locs!=1:
			print("In registration mode, there must be one person in the front of camera")
		else:
			x = face_locs[0][0];	y = face_locs[0][1]
			w = face_locs[0][2];	h = face_locs[0][3]
			face = img[x:w+1, h:y+1]
			face_code = face_encodings(face)
			if len(face_code):
				if isTempExisted(face_code, ft_path, threshold):
					print("Your template is registered before")
				else:
					save_dict = {"temp_code": face_code, "face":face}
					savemat("%s%s.mat" % (ft_path, name), save_dict)
					print("%s, your registration is succesful" % name)
					break

	# Exit
	k = cv2.waitKey(5) & 0xff
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()