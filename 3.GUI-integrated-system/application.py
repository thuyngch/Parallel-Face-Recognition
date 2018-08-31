#------------------------------------------------------------------------------
#   Import
#------------------------------------------------------------------------------
from os.path import exists
from os import remove

from PyQt5.QtWidgets import QVBoxLayout, QMainWindow
from PyQt5.QtGui import QFont, QImage

from frontend import design
from backend.captureVideo import CaptureVideo
from backend.faceDetection import FaceDetection
from backend.faceRecognition import FaceRecognition
from backend.faceRegistration import FaceRegistration
from backend.faceRegistration import FaceRegistration
from backend.logfile import LogFile


#------------------------------------------------------------------------------
#   Class of Application
#------------------------------------------------------------------------------
class Application(QMainWindow, design.Ui_MainWindow):
	def __init__(self):
		super(Application, self).__init__()
		self.setupUi(self)
		self.setup_logfile()
		self.setup_wgVideo()
		self.setup_wgFaceCrop()
		self.setup_registration()

	def setup_wgVideo(self):
		# Functions
		self.wgVideo.capture_video = CaptureVideo(camera_port=0)
		self.wgVideo.face_detection = FaceDetection(
						haarcascade_fp="haarcascade_frontalface_default.xml")

		# Connect the [image_data] to [draw_bounding_boxes]
		draw_bounding_boxes = self.wgVideo.face_detection.draw_bounding_boxes
		self.wgVideo.capture_video.image_data.connect(draw_bounding_boxes)

		# Layout
		layout = QVBoxLayout()
		layout.addWidget(self.wgVideo.face_detection)
		self.wgVideo.setLayout(layout)


	def setup_wgFaceCrop(self):
		# Functions
		self.wgFaceCrop.face_recognition = FaceRecognition(
											self.logfile, 			\
											sc_thres=0.4, 			\
											sq_thres=18000, 		\
											scale=(150, 150),		\
											fp_db="template/", 		\
											pipe_file="pipe.mat", 	\
											time_idle=5000)

		# Remove [pipe_file]
		if exists(self.wgFaceCrop.face_recognition.pipe_file):
			remove(self.wgFaceCrop.face_recognition.pipe_file)

		# Connect the [Name] to [update_lbInfo]
		self.wgFaceCrop.face_recognition.Name.connect(self.update_lbInfo)

		# Connect the [frame_locations] to [draw_cropped_face]
		recognize = self.wgFaceCrop.face_recognition.recognize
		self.wgVideo.face_detection.frame_locations.connect(recognize)

		# Layout
		layout = QVBoxLayout()
		layout.addWidget(self.wgFaceCrop.face_recognition)
		self.wgFaceCrop.setLayout(layout)


	def setup_registration(self):
		# Functions
		self.registration = FaceRegistration(sc_thres=0.4, 			\
											fp_db="template/", 		\
											pipe_file="pipe.mat")

		# Connect textChanged event in [txtName] to [txtNameEnterPressEvent]
		self.txtName.textChanged.connect(self.txtNameEnterPressEvent)

		# Connect clicked event in [btnCancel] to [cancelClickEvent]
		self.btnCancel.clicked.connect(self.cancelClickEvent)


	def setup_logfile(self):
		# Functions
		self.logfile = LogFile(fp_logfile="logfile/", 		\
								num_file=10, 				\
								file_len=5120)


	def update_lbInfo(self, text_info):
		self.lbInfo.setText(text_info)


	def txtNameEnterPressEvent(self):
		name = self.txtName.toPlainText()
		if len(name)>=1 and name[-1] == "\n":
			self.registration.register(name[0:-1])
			self.txtName.clear()


	def cancelClickEvent(self):
		self.txtName.clear()
		self.wgFaceCrop.face_recognition.image = QImage()
		self.update()
		self.lbInfo.setText("No face detected")
		if exists(self.registration.pipe_file):
			remove(self.registration.pipe_file)

