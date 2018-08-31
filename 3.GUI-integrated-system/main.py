#------------------------------------------------------------------------------
#   Import
#------------------------------------------------------------------------------
from sys import argv
from PyQt5.QtWidgets import QApplication
from application import Application


#------------------------------------------------------------------------------
#   Main execution
#------------------------------------------------------------------------------
app = QApplication(argv)
form = Application()
form.show()
app.exec_()

