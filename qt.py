import sys
import re
import os
import subprocess, shlex
from subprocess import PIPE, Popen
from threading import Thread
from time import sleep
from PyQt4 import QtGui, uic
from PyQt4.QtGui import QMessageBox, QFileDialog

window = None

class MyWindow(QtGui.QDialog):
	def __init__(self):
		super(MyWindow, self).__init__()
		uic.loadUi('python.ui', self)
		self.show()

def threaded_function(path, url, window):
	cmd = shlex.split("wget -r -k -l 7 -p -E -nc %s" % (url))
	process = subprocess.Popen(
		cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	while True:
		out = process.stdout.read(1)
		if out == '' and process.poll() != None:
			break
		if out != '':
			sys.stdout.write(out)
			sys.stdout.flush()


def downloadRoutine(path, url):
	thread = Thread(target = threaded_function, args = (path, url, window, ))
	thread.start()
	QMessageBox.information(window, "OK", "%s" % ("Download finished"))


def buttonClicked():
	if not re.search("(^|[\s.:;?\-\]<\(])(https?:\/\/[-\w;/?:@&=+$\|\_.!~*\|'()\[\]%#,]+[\w/#](\(\))?)(?=$|[\s',\|\(\).:;?\-\[\]>\)])", window.linkEdit.text()):
		QMessageBox.warning(window, "Warning", "%s is not a valid URL" % (window.linkEdit.text()))
	else: 
		file = str(QFileDialog.getExistingDirectory(window, "Select Directory"))
		downloadRoutine(file, window.linkEdit.text())

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = MyWindow()
	window.pushButton.clicked.connect(buttonClicked)
	sys.exit(app.exec_())