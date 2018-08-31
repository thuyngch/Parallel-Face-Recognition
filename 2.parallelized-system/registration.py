#------------------------------------------------------------------------------
#   Import
#------------------------------------------------------------------------------
import cv2
from multiprocessing import Process, Pipe
from fnc.parallelPool import pool_display_video, pool_face_localize, pool_registration


#------------------------------------------------------------------------------
#   Main
#------------------------------------------------------------------------------
ft_path = "./template/"
name = input(">>> Please type name of the registration person: ")
threshold = 0.4
cap = cv2.VideoCapture(0)

conn_12, conn_21 = Pipe()
conn_23, conn_32 = Pipe()
conn_31, conn_13 = Pipe()
p1 = Process(target=pool_display_video, args=(cap, conn_12, conn_13))
p2 = Process(target=pool_face_localize, args=(conn_21, conn_23))
p3 = Process(target=pool_registration, args=(conn_31, conn_32, ft_path, name, threshold))
p1.start(); p2.start(); p3.start()
p1.join() ; p2.join() ; p3.join()

cap.release()
cv2.destroyAllWindows()

