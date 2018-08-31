#------------------------------------------------------------------------------
#	Import
#------------------------------------------------------------------------------
import cv2
import numpy as np
from face_recognition import face_locations, face_encodings
from scipy.io import savemat
from fnc.matching import isTempExisted, matching


#------------------------------------------------------------------------------
#   Draw face localtions on an image
#------------------------------------------------------------------------------
def draw_face_locations(img, face_locs):
	corner1 = []
	corner2 = []
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
#	Pool of displaying video
#------------------------------------------------------------------------------
def pool_display_video(cap, conn_loc, conn_encd):
	ret, img = cap.read()
	conn_loc.send(img)
	while 1:
		# Read image from video
		ret, img = cap.read()

		# Communicate with Location pool, send data to Encode pool
		face_locs = []
		if conn_loc.poll():
			face_locs = conn_loc.recv()
			conn_encd.send(img)
			conn_loc.send(img)

		# Get data from Encode pool (implicitly Registration or Verification)
		if conn_encd.poll():
			read = conn_encd.recv()
			if isinstance(read, str) and read=="break":	# Registration
				return
			if isinstance(read, list) and len(read):	# Verification
				print(">>> Recognized people:")
				for name in read:
					print("    %s" % name)

		# Display image
		img_loc, corner1, corner2 = draw_face_locations(img, face_locs)
		cv2.imshow("Facial Recognition System", img_loc)

		# Wait for break signal from keyboard and send to another pools
		k = cv2.waitKey(5) & 0xff
		if k == 27:
			conn_loc.send("break")
			conn_encd.send("break")
			return


#------------------------------------------------------------------------------
#   Pool of localizing face
#------------------------------------------------------------------------------
def pool_face_localize(conn_disp, conn_encd):
	while 1:
		if conn_disp.poll():
			img = conn_disp.recv()
			if isinstance(img, str) and img=="break":
				return
			face_locs = face_locations(img)
			conn_disp.send(face_locs)
			conn_encd.send(face_locs)

		if conn_encd.poll():
			read = conn_encd.recv()
			if isinstance(read, str) and read=="break":
				return


#------------------------------------------------------------------------------
#   Pool of registration
#------------------------------------------------------------------------------
def pool_registration(conn_disp, conn_loc, ft_path, name, threshold):
	while True:
		# Get data
		img = []
		face_locs = []
		if conn_loc.poll():
			face_locs = conn_loc.recv()
			img = conn_disp.recv()

		# Break signal
		if conn_disp.poll():
			read = conn_disp.recv()
			if isinstance(read, str) and read=="break":
				return

		# Encode face
		face_code = []
		face = []
		len_locs = len(face_locs)
		if len_locs and len(img):
			if len_locs!=1:
				print(">>> In registration mode, there must be one person in the front of camera!!!")
			else:
				x = face_locs[0][0];	y = face_locs[0][1]
				w = face_locs[0][2];	h = face_locs[0][3]
				face = img[x:w+1, h:y+1]
				face_code = face_encodings(face)

		# Verify whether the face template existed
		if len(face_code):
			if isTempExisted(face_code, ft_path, threshold):
				print(">>> Your template is registered before!")
			else:
				savemat("%s%s.mat" % (ft_path, name), 	\
										{"temp_code": face_code, "face":face})
				print(">>> %s, your registration is succesful." % name)

				# Send break signal to Display and Location pool
				if conn_disp.poll():
					conn_disp.recv()
				if conn_loc.poll():
					conn_loc.recv()
				conn_disp.send("break")
				conn_loc.send("break")
				return


#------------------------------------------------------------------------------
#   Pool of verification
#------------------------------------------------------------------------------
def pool_verification(conn_disp, conn_loc, ft_path, threshold):
	while True:
		# Get data from Location pool
		img = []
		face_locs = []
		if conn_loc.poll():
			face_locs = conn_loc.recv()
			img = conn_disp.recv()

		# Break signal from Display pool
		if conn_disp.poll():
			read = conn_disp.recv()
			if isinstance(read, str) and read=="break":
				return

		# Encode faces
		len_locs = len(face_locs)
		face_codes = []; face = []
		if len_locs and len(img):
			for i in range(len_locs):
				x = face_locs[i][0];	y = face_locs[i][1]
				w = face_locs[i][2];	h = face_locs[i][3]
				face = img[x:w+1, h:y+1]
				face_code = face_encodings(face)
				if len(face_code):
					face_codes.append(face_code)

		# Compare faces to templates in database
		names = [];	faces = []
		for i in range(len(face_codes)):
			face_code = face_codes[i]
			res, name, face = matching(face_code, ft_path, threshold)
			if res:
				names.append(name)
				faces.append(face)

		# Send result to Display pool
		if len(names):
			if conn_disp.poll():
				conn_disp.recv()
			conn_disp.send(names)

