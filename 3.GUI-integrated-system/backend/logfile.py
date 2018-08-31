#------------------------------------------------------------------------------
#   Import
#------------------------------------------------------------------------------
from time import gmtime, strftime
from os import listdir
from os.path import getsize, exists


#------------------------------------------------------------------------------
#   Class of Logfile system.
#------------------------------------------------------------------------------
class LogFile():
	def __init__(self, fp_logfile="logfile/", num_file=10, file_len=5120):
		super(LogFile, self).__init__()
		self.fp_logfile = fp_logfile
		self.num_file = num_file
		self.file_len = file_len


	def get_logfile_id(self):
		files = listdir(self.fp_logfile)
		numfile = len(files)
		if numfile == 0:
			return 1
		else:
			if getsize("%s%d.log" % (self.fp_logfile, numfile)) < self.file_len:
				return numfile
			else:
				if numfile==self.num_file:
					return 0
				else:
					return numfile+1


	def write_logfile(self, content):
		# Get file ID
		file_id = self.get_logfile_id()
		str_time = strftime("%Y-%m-%d %H:%M:%S-------------------\n", gmtime())

		# Full
		if file_id==0:
			pass

		# Available
		else:
			filepath = "%s%d.log" % (self.fp_logfile, file_id)
			if exists(filepath):
				fp = open(filepath, "a")
			else:
				fp = open(filepath, "w")
			fp.write(str_time)
			fp.write(content)
			fp.write("\n")
			fp.close()

