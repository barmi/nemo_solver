import os
import pickle
import sys
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class frmNemo(QMainWindow):
	def __init__(self):
		super().__init__()
		self.num_info_dict = {}
		self.img1_org = None
		self.img2_org = None
		self.initUI()

	def initUI(self):
		self.setWindowTitle('Nemo')
		self.setGeometry(0, 0, 900, 700)

		layout_margin = 5
		main = QWidget()
		layout = QGridLayout()
		layout.setSpacing(layout_margin)
		layout.setContentsMargins(layout_margin, layout_margin, layout_margin, layout_margin)
		main.setLayout(layout)
		self.setCentralWidget(main)

		row = 0

		hbox = QHBoxLayout()

		image = QImage('../data/1-4746.PNG')
		# Define crop range
		crop_y_start = 350
		crop_y_end = 1800
		crop_height = crop_y_end - crop_y_start
		image = image.copy(0, crop_y_start, image.width(), crop_height)
		self.aspect_ratio = image.width() / image.height()
		self.new_height = 600
		self.crop_y_start = 350
		self.org_width = image.width()
		self.org_height = image.height()
		self.new_width = int(self.new_height * self.aspect_ratio)
		image = image.scaled(self.new_width, self.new_height, Qt.KeepAspectRatio)
		self.img1 = QLabel()
		self.img1.setPixmap(QPixmap.fromImage(image))
		self.img1.setFixedWidth(self.new_width)
		self.img1.setFixedHeight(self.new_height)
		hbox.addWidget(self.img1)

		image = QImage('../data/1-4746.PNG_out_num.PNG')
		image = image.copy(0, crop_y_start, image.width(), crop_height)
		image = image.scaled(self.new_width, self.new_height, Qt.KeepAspectRatio)
		self.img2 = QLabel()
		self.img2.setPixmap(QPixmap.fromImage(image))
		self.img2.setFixedWidth(self.new_width)
		self.img2.setFixedHeight(self.new_height)
		hbox.addWidget(self.img2)
		layout.addLayout(hbox, row, 0, 1, 3)

		row += 1

		btn = QPushButton('refresh')
		btn.clicked.connect(self.OnRefresh)
		layout.addWidget(btn, row, 0)

		row += 1
		self.listFile = QListWidget()
		self.listFile.setFixedWidth(120)
		self.listFile.itemClicked.connect(self.OnFileSelected)
		layout.addWidget(self.listFile, row, 0)

		self.listNum = QListWidget()
		self.listNum.setFixedWidth(50)
		self.listNum.itemClicked.connect(self.OnNumSelected)
		layout.addWidget(self.listNum, row, 1)

		self.scroll_area = QScrollArea()
		self.scroll_area.setWidgetResizable(True)
		layout.addWidget(self.scroll_area, row, 2)

		self.center()

		self.show()


	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		qr.setTop(qr.top() - 15)
		self.move(qr.topLeft())


	def OnRefresh(self):
		data_dir = '../data'
		self.listFile.clear()
		dir_list = os.listdir(data_dir)
		dir_list.sort()
		for item in dir_list:
			if os.path.isdir(os.path.join(data_dir, item)) and item.startswith('_num_'):
				self.listFile.addItem(item[5:])


	def OnFileSelected(self):
		data_dir = '../data/_num_' + self.listFile.currentItem().text()
		self.listNum.clear()
		num_list = []
		for item in os.listdir(data_dir):
			if os.path.isdir(os.path.join(data_dir, item)):
				num_list.append(item)
		num_list.sort(key=int)
		for item in num_list:
			self.listNum.addItem(item)

		image = QImage('../data/' + self.listFile.currentItem().text() + '.PNG')
		# Define crop range
		crop_y_start = 350
		crop_y_end = 1800
		crop_height = crop_y_end - crop_y_start
		image = image.copy(0, crop_y_start, image.width(), crop_height)
		image = image.scaled(self.new_width, self.new_height, Qt.KeepAspectRatio)
		self.img1.setPixmap(QPixmap.fromImage(image))
		self.img1_org = self.img1.pixmap().toImage()

		image = QImage('../data/' + self.listFile.currentItem().text() + '.PNG_out_num.PNG')
		image = image.copy(0, crop_y_start, image.width(), crop_height)
		image = image.scaled(self.new_width, self.new_height, Qt.KeepAspectRatio)
		self.img2.setPixmap(QPixmap.fromImage(image))
		self.img2_org = self.img2.pixmap().toImage()

		pickle_file = '../data/' + self.listFile.currentItem().text() + '.PNG_num_info.pickle'
		if os.path.exists(pickle_file):
			with open(pickle_file, 'rb') as f:
				self.num_info_dict = pickle.load(f)


	def OnNumSelected(self):
		data_dir = '../data/_num_' + self.listFile.currentItem().text() + '/' + self.listNum.currentItem().text()
		png_files = [f for f in os.listdir(data_dir) if f.endswith('.png')]

		# Create a new widget to hold the images
		image_container = QWidget()
		grid_layout = QGridLayout(image_container)

		# Define the number of columns
		columns = 5

		# Store references to the QLabel widgets
		self.image_labels = {}

		max_image_width = 0
		for file_name in png_files:
			image = QImage(os.path.join(data_dir, file_name))
			if image.width() > 0:
				new_height = 80
				aspect_ratio = image.width() / image.height()
				new_width = int(new_height * aspect_ratio)
				max_image_width = max(max_image_width, new_width)
		if max_image_width == 0:
			return

		columns = self.scroll_area.width() // (max_image_width + 20)
		if columns == 0:
			columns = 1

		# Add images to the grid layout
		for index, file_name in enumerate(png_files):
			row = index // columns
			col = index % columns
			image_path = os.path.join(data_dir, file_name)
			image = QImage(image_path)
			# pixmap = QPixmap.fromImage(image)

			if image.width() == 0:
				image = QImage(10, 10, QImage.Format_RGB32)
				image.fill(Qt.white)

			# Calculate the new width while maintaining the aspect ratio
			new_height = 80
			aspect_ratio = image.width() / image.height()
			new_width = int(new_height * aspect_ratio)

			# Resize the image
			image = image.scaled(new_width, new_height, Qt.KeepAspectRatio)
			pixmap = QPixmap.fromImage(image)

			# Create a QLabel to display the image
			label = QLabel()
			label.setPixmap(pixmap)
			label.setStyleSheet("border: 3px solid darkgray;")
			# label.setScaledContents(True)  # Ensure the image fits the grid cell
			label.mousePressEvent = lambda event, fname=file_name, lbl=label: self.OnImageClick(event, fname, lbl)
			grid_layout.addWidget(label, row, col)

			# Store the label reference
			self.image_labels[file_name] = label

		# Set the new widget as the scroll area's widget
		self.scroll_area.setWidget(image_container)

	def OnImageClick(self, event, file_name, label):
		# Reset borders for all images
		for lbl in self.image_labels.values():
			lbl.setStyleSheet("border: 3px solid darkgray;")

		# Set border for the clicked image
		label.setStyleSheet("border: 3px solid green;")

		# Print the file name
		print(file_name)
		parts = file_name.split('_')
		print(parts)
		num_info_key = parts[1] + '_' + parts[2] + '_' + parts[3]
		if num_info_key in self.num_info_dict:
			print(self.num_info_dict[num_info_key])
		image = self.img1_org.copy()
		painter = QPainter(image)
		pen = QPen(Qt.green)
		pen.setWidth(1)
		painter.setPen(pen)
		ratio = self.new_width / self.org_width
		x = int(self.num_info_dict[num_info_key][0]) * ratio
		y = (int(self.num_info_dict[num_info_key][1]) - self.crop_y_start) * ratio
		h = int(self.num_info_dict[num_info_key][3]) * ratio
		w = int(self.num_info_dict[num_info_key][2]) * ratio
		painter.drawRect(x-1, y-1, w+3, h+3)
		painter.end()
		self.img1.setPixmap(QPixmap.fromImage(image))


	def OnGridClick(self, row, col):
		print(f"Grid cell clicked at row {row}, col {col}")


def main():
	app = QApplication(sys.argv)
	frmMain = frmNemo()
	frmMain.show()

	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
