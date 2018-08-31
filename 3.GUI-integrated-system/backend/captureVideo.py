#------------------------------------------------------------------------------
#   Import
#------------------------------------------------------------------------------
import cv2
from numpy import ndarray
from PyQt5.QtCore import QObject, pyqtSignal, QBasicTimer


#------------------------------------------------------------------------------
#   Class to capture and display video from webcam
#------------------------------------------------------------------------------
class CaptureVideo(QObject):
	# Signals
	image_data = pyqtSignal(ndarray)

	# Initialize class
	def __init__(self, camera_port=0):
		super().__init__()
		self.camera = cv2.VideoCapture(camera_port)
		self.timer = QBasicTimer()
		self.timer.start(1, self)	# Period in miliseconds


	# Update video frame
	def timerEvent(self, event):
		if (event.timerId() != self.timer.timerId()):
			return
		read, frame = self.camera.read()
		if read:
			self.image_data.emit(frame)

