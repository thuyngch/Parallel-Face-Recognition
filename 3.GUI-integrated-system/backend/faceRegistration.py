#------------------------------------------------------------------------------
#   Import
#------------------------------------------------------------------------------
from PyQt5.QtWidgets import QWidget, QMessageBox
from backend.faceEncode import encode_face
from backend.faceMatch import isTempExisted
from os.path import exists
from os import rename


#------------------------------------------------------------------------------
#   Class to crop face
#------------------------------------------------------------------------------
class FaceRegistration(QWidget):
	# Initialize class
	def __init__(self, sc_thres=0.4, fp_db="template/", pipe_file="pipe.mat"):
		super().__init__()
		self.sc_thres = sc_thres
		self.fp_db = fp_db
		self.pipe_file = pipe_file


	# Register a face account
	def register(self, name):
		# There is no Registration queue
		if not exists(self.pipe_file):
			return

		# There is a Registration queue
		else:
			if self.is_name_existed(name):
				QMessageBox.warning(self, 							\
					'Warning', "The name has existed!",				\
					QMessageBox.Ok, QMessageBox.Ok)
			else:
				rename(self.pipe_file, "%s%s.mat" % (self.fp_db, name))
				QMessageBox.information(self, 						\
					'Notification', "Register successfully!",		\
					QMessageBox.Ok, QMessageBox.Ok)


	# Verify whether a name has existed in the database
	def is_name_existed(self, name):
		if exists("%s%s.mat" % (self.fp_db, name)):
			return True
		else:
			return False

