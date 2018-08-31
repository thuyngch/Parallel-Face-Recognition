#------------------------------------------------------------------------------
#   Import
#------------------------------------------------------------------------------
from numpy import array, argmax
from face_recognition import face_encodings


#------------------------------------------------------------------------------
#   Function to crop face from frame image.
#	
#	[Input]
#		frame_image		: Image of a frame from the captured video
#		face_locations	: Locations of detected face
#		sq_thres		: The cadidate threshold square
#
#	[Output]
#		face 			: Cropped face
#
#------------------------------------------------------------------------------
def crop_face(frame_image, face_locations, sq_thres):
	"""
	* No need to examine whether [face_locations] is emplty because it is
	verified in the previous stage.

	* [sq_thres] is used to eliminate locations that are too small.

	* In the case that there are more than one face detected, the largest
	face will be accepted and the remainings will be rejected.
	"""
	# Get the accepted face
	sq_vect = face_locations[:, 2] * face_locations[:, 3]
	idx_max = argmax(sq_vect)
	sq = sq_vect[idx_max]
	if sq < sq_thres:
		return []
	else:
		(x, y, w, h) = face_locations[idx_max]

	# Crop the accepted face
	face = frame_image[y: y+h+1, x: x+w+1, :]
	return array(face)


#------------------------------------------------------------------------------
#   Function to encode face.
#
#	[Input]
#		frame_image		: Image of a frame from the captured video
#		face_locations	: Locations of detected face
#		sq_thres		: The cadidate threshold square
#
#	[Output]
#		face_code		: Feature code of the accepted face
#		face_cropped	: Cropped face of the accepted face
#
#------------------------------------------------------------------------------
def encode_face(frame_image, face_locations, sq_thres):
	"""
	* Just one face is chosen and encoded. The largest face is accepted.
	"""
	# Crop face
	face_cropped = crop_face(frame_image, face_locations, sq_thres)
	if len(face_cropped)==0:
		return ([], [])

	# Encode face
	face_code = face_encodings(face_cropped)
	if len(face_code):
		return (face_code, face_cropped)
	else:
		return ([], [])

