from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from scipy.ndimage import label


class frmNemo(QMainWindow):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setWindowTitle('Nemo')
		self.setGeometry(300, 300, 800, 600)

		layout_margin = 5
		main = QWidget()
		layout = QGridLayout()
		layout.setSpacing(layout_margin)
		layout.setContentsMargins(layout_margin, layout_margin, layout_margin, layout_margin)
		main.setLayout(layout)
		self.setCentralWidget(main)

		row = 0
		btn = QPushButton('refresh')
		btn.clicked.connect(self.OnRefresh)
		layout.addWidget(btn, row, 0)

		image = QImage('../data/1-4751.PNG')
		# Define crop range
		crop_y_start = 350
		crop_y_end = 1800
		crop_height = crop_y_end - crop_y_start

		# Crop the image
		image = image.copy(0, crop_y_start, image.width(), crop_height)
		# Calculate aspect ratio
		aspect_ratio = image.width() / image.height()
		new_height = 500
		new_width = int(new_height * aspect_ratio)

		# Resize image
		image = image.scaled(new_width, new_height, Qt.KeepAspectRatio)
		label = QLabel()
		label.setPixmap(QPixmap.fromImage(image))
		label.setFixedWidth(new_width)
		label.setFixedHeight(new_height)
		layout.addWidget(label, row, 1, 2, 1)




		# Create a QLabel and QScrollArea
		scroll_area = QScrollArea()
		scroll_area.setWidgetResizable(True)
		image_container = QWidget()
		grid_layout = QGridLayout(image_container)

		# Load the image
		image = QImage('../data/1-4751.PNG')
		# Define the size for each image
		image_width = image.width() // 3
		image_height = image.height() // 6

		# Add images to the grid layout
		for i in range(6):
			for j in range(3):
				cropped_image = image.copy(j * image_width, i * image_height, image_width, image_height)
				label = QLabel()
				label.setPixmap(QPixmap.fromImage(cropped_image))
				label.mousePressEvent = lambda event, row=i, col=j: self.OnGridClick(row, col)
				grid_layout.addWidget(label, i, j)

		scroll_area.setWidget(image_container)
		layout.addWidget(scroll_area, row, 2, 2, 1)



		row += 1
		self.listFile = QListWidget()
		self.listFile.setFixedHeight(170)
		self.listFile.itemClicked.connect(self.OnFileSelected)
		layout.addWidget(self.listFile, row, 0)


		# self.edtLog2 = QTextEdit()

		self.center()

		self.show()

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		qr.setTop(qr.top() - 15)
		self.move(qr.topLeft())

	def OnRefresh(self):
		pass

	def OnFileSelected(self):
		pass


	def OnGridClick(self, row, col):
		print(f"Grid cell clicked at row {row}, col {col}")


def main():
	import sys
	app = QApplication(sys.argv)
	frmMain = frmNemo()
	frmMain.show()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
