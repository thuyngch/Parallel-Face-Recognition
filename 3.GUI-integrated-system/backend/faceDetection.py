#------------------------------------------------------------------------------
#   Import
#------------------------------------------------------------------------------
import cv2
from numpy import ndarray, array
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal


#------------------------------------------------------------------------------
#   Class to detect faces' locations
#------------------------------------------------------------------------------
class FaceDetection(QWidget):
	# Signals
	frame_locations = pyqtSignal(tuple)

	# Initialize class
	def __init__(self, haarcascade_fp):
		super().__init__()
		self.classifier = cv2.CascadeClassifier(haarcascade_fp)
		self.image = QtGui.QImage()
		self.black = (0, 0, 0)
		self.green = (0, 255, 0)
		self.width = 2
		self.min_size = (30, 30)


	# Detect locations that contain faces
	def detect_faces(self, image: ndarray):
		gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		gray_image = cv2.equalizeHist(gray_image)
		face_locs = self.classifier.detectMultiScale(gray_image,	\
									scaleFactor=1.3, 				\
									minNeighbors=4,  				\
									flags=cv2.CASCADE_SCALE_IMAGE, 	\
									minSize=self.min_size)
		return array(face_locs)


	# Draw bounding boxes of faces
	def draw_bounding_boxes(self, image_data):
		# Prepare
		image = array(image_data)

		# Indicate bounding boxes
		face_locs = self.detect_faces(image_data)
		for (x, y, w, h) in face_locs:
			corner1 = (x, y); corner2 = (x+w, y+h)
			cv2.rectangle(image, corner1, corner2, self.green, self.width)

		# Border of the image
		corner1 = (0, 0)
		corner2 = (image_data.shape[1], image_data.shape[0])
		cv2.rectangle(image, corner1, corner2, self.black, self.width)

		# Draw bounding boxes
		self.image = self.get_qimage(image)
		if self.image.size() != self.size():
			self.setFixedSize(self.image.size())
		self.update()

		# Wrap and send signals to [draw_cropped_face]
		if len(face_locs):
			self.frame_locations.emit((image_data, face_locs))


	# Convert np.ndarray to qimage
	def get_qimage(self, image: ndarray):
		height, width, colors = image.shape
		bytesPerLine = 3 * width
		QImage = QtGui.QImage
		image = QImage(image.data, width, height, bytesPerLine, 	\
												QImage.Format_RGB888)
		image = image.rgbSwapped()
		return image


	# Paint image into the window of the application
	def paintEvent(self, event):
		painter = QtGui.QPainter(self)
		painter.drawImage(0, 0, self.image)


#------------------------------------------------------------------------------
#   Class to crop face
#------------------------------------------------------------------------------
class FaceCrop(QWidget):
	# Initialize class
	def __init__(self):
		super().__init__()
		self.image = QtGui.QImage()


	# Crop face from frame image and draw it
	def draw_cropped_face(self, frame_locations):
		# Unroll arguments
		frame_image = frame_locations[0]
		face_locations = frame_locations[1]

		# Crop face from frame image
		if len(face_locations) != 1:
			return
		else:
			(x, y, w, h) = face_locations[0]
			square = w*h
			if square < 18000:
				return
			else:
				face = frame_image[y: y+h+1, x: x+w+1]

		# Draw face
		face_image = cv2.resize(face, (150, 150))
		self.image = self.get_qimage(face_image)
		self.update()


	# Convert np.ndarray to qimage
	def get_qimage(self, image: ndarray):
		height, width, colors = image.shape
		bytesPerLine = 3 * width
		QImage = QtGui.QImage
		image = QImage(image.data, width, height, bytesPerLine,	\
											QImage.Format_RGB888)
		image = image.rgbSwapped()
		return image


	# Paint image into the window of the application
	def paintEvent(self, event):
		painter = QtGui.QPainter(self)
		painter.drawImage(0, 0, self.image)

