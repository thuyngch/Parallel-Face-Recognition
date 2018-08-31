#------------------------------------------------------------------------------
#   Import
#------------------------------------------------------------------------------
import cv2
from numpy import ndarray
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, QBasicTimer
from backend.faceEncode import encode_face
from backend.faceMatch import matching
from os.path import exists
from scipy.io import savemat


#------------------------------------------------------------------------------
#   Class to crop face
#------------------------------------------------------------------------------
class FaceRecognition(QWidget):
	# Signals
	Name = pyqtSignal(str)

	# Initialize class
	def __init__(self, log_file, sc_thres=0.4, sq_thres=18000, scale=(150, 150),\
				fp_db="template/", pipe_file="pipe.mat", time_idle=5000):
		super().__init__()
		self.log_file = log_file
		self.sc_thres = sc_thres
		self.sq_thres = sq_thres
		self.scale = scale
		self.fp_db = fp_db
		self.pipe_file = pipe_file
		self.time_idle = time_idle
		
		self.image = QtGui.QImage()
		self.timer = QBasicTimer()


	# Recognize face from the frame image
	def recognize(self, frame_locations):
		# Unroll arguments
		frame_image = frame_locations[0]
		face_locations = frame_locations[1]

		# Encode and match face
		face_code, face_cropped = encode_face(frame_image, 	\
											face_locations, self.sq_thres)
		if len(face_code)==0:
			self.timer.start(self.time_idle, self)
			return
		else:
			self.timer.stop()
			res, name, face = matching(face_code, self.fp_db, self.sc_thres)

		# Draw face and print name
		existed_flg = exists(self.pipe_file)
		if res:		# The person has registered before
			if not existed_flg:
				face_image = cv2.resize(face, self.scale)
				self.image = self.get_qimage(face_image)
				self.update()
				self.log_file.write_logfile(name)
				self.Name.emit(name)
		else:		# The person has not registered before
			self.Name.emit("Person unknown")
			if not existed_flg:
				savemat(self.pipe_file, {"temp_code": face_code, 
										 "face": face_cropped})
				face_image = cv2.resize(face_cropped, self.scale)
				self.image = self.get_qimage(face_image)
				self.update()


	# Convert np.ndarray to qimage
	def get_qimage(self, image: ndarray):
		height, width, colors = image.shape
		bytesPerLine = 3*width
		QImage = QtGui.QImage
		image = QImage(image.data, width, height, bytesPerLine,	\
											QImage.Format_RGB888)
		image = image.rgbSwapped()
		return image


	# Paint image into the window of the application
	def paintEvent(self, event):
		painter = QtGui.QPainter(self)
		painter.drawImage(0, 0, self.image)


	# Update Recognition frame
	def timerEvent(self, event):
		if (event.timerId() != self.timer.timerId()):
			return
		else:
			self.image = QtGui.QImage()
			self.update()
			self.Name.emit("No face detected")


