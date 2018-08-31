#------------------------------------------------------------------------------
#	Import
#------------------------------------------------------------------------------
from os import listdir
from fnmatch import filter
from scipy.io import loadmat
from face_recognition import compare_faces


#------------------------------------------------------------------------------
#   Verify whether a template exists in database
#------------------------------------------------------------------------------
def isTempExisted(test_temp, ft_path, threshold):
	files = listdir(ft_path)
	numfile = len(filter(files, '*.mat'))
	if numfile == 0:
		return False
	else:
		for file in files:
			db_temp = loadmat("%s%s" % (ft_path, file))['temp_code']
			if compare_faces(test_temp, db_temp, threshold)[0]:
				return True
	return False


#------------------------------------------------------------------------------
#   Verify whether a template is in database, return (bool, name, face image)
#------------------------------------------------------------------------------
def matching(test_temp, ft_path, threshold):
	if not len(test_temp):
		return False, '', []

	files = listdir(ft_path)
	numfile = len(filter(files, '*.mat'))
	if numfile == 0:
		return False, '', []
	else:
		for file in files:
			db_data = loadmat("%s%s" % (ft_path, file))
			db_temp = db_data['temp_code']
			db_face = db_data['face']
			if compare_faces(test_temp, db_temp, threshold)[0]:
				return True, file[:-4], db_face
	return False, '', []

