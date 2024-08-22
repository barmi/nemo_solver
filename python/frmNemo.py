import glob
import os
import pickle
import shutil
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
		self.selected_file_name = ''
		self.initUI()

	def initUI(self):
		self.setWindowTitle('Nemo')
		self.setGeometry(0, 0, 900, 850)

		layout_margin = 5
		main = QWidget()
		layout = QGridLayout()
		layout.setSpacing(layout_margin)
		layout.setContentsMargins(layout_margin, layout_margin, layout_margin, layout_margin)
		main.setLayout(layout)
		self.setCentralWidget(main)

		row = 0

		hbox = QHBoxLayout()

		image = QImage('../data/1-4757.PNG')
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

		image = QImage('../data/1-4757.PNG_out_num.PNG')
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

		row += 1
		hbox = QHBoxLayout()
		self.edtNum = QLineEdit()
		hbox.addWidget(self.edtNum)
		btn = QPushButton('값 수정')
		btn.clicked.connect(self.OnModifyNumValue)
		hbox.addWidget(btn)

		self.edtNewNum1 = QLineEdit()
		hbox.addWidget(self.edtNewNum1)
		self.edtNewNum2 = QLineEdit()
		hbox.addWidget(self.edtNewNum2)
		self.edtNewNum3 = QLineEdit()
		hbox.addWidget(self.edtNewNum3)
		btn = QPushButton('값 분리')
		btn.clicked.connect(self.OnSplitNumValue)
		hbox.addWidget(btn)

		self.comboXY = QComboBox()
		self.comboXY.addItem('x')
		self.comboXY.addItem('y')
		hbox.addWidget(self.comboXY)
		lbl = QLabel('pos1')
		hbox.addWidget(lbl)
		self.edtInPos1 = QLineEdit()
		hbox.addWidget(self.edtInPos1)
		lbl = QLabel('pos2')
		hbox.addWidget(lbl)
		self.edtInPos2 = QLineEdit()
		hbox.addWidget(self.edtInPos2)
		lbl = QLabel('1')
		hbox.addWidget(lbl)
		self.edtInNum1 = QLineEdit()
		hbox.addWidget(self.edtInNum1)
		lbl = QLabel('2')
		hbox.addWidget(lbl)
		self.edtInNum2 = QLineEdit()
		hbox.addWidget(self.edtInNum2)
		lbl = QLabel('3')
		hbox.addWidget(lbl)
		self.edtInNum3 = QLineEdit()
		hbox.addWidget(self.edtInNum3)
		btn = QPushButton('값 삽입')
		btn.clicked.connect(self.OnInsertNumValue)
		hbox.addWidget(btn)

		layout.addLayout(hbox, row, 0, 1, 3)

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
		self.selected_file_name = ''
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
		self.selected_file_name = ''
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
		image = self.img1_org.copy()
		if num_info_key in self.num_info_dict:
			print(self.num_info_dict[num_info_key])
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

		self.selected_file_name = file_name
		self.edtNewNum1.clear()
		self.edtNewNum2.clear()
		self.edtNewNum3.clear()


	def OnModifyNumValue(self):
		if self.selected_file_name == '':
			return
		parts = self.selected_file_name.split('_')
		if len(parts) != 5:
			return
		parts[4] = self.edtNum.text() + '.png'
		new_file_name = '_'.join(parts)
		new_file_name = new_file_name.replace(' ', '')
		data_dir = '../data/_num_' + self.listFile.currentItem().text()
		old_file_path = os.path.join(data_dir, self.selected_file_name)
		if not os.path.exists(old_file_path):
			return
		new_file_path = os.path.join(data_dir, new_file_name)
		os.rename(old_file_path, new_file_path)

	def OnSplitNumValue(self):
		if self.selected_file_name == '':
			return
		parts = self.selected_file_name.split('_')
		if len(parts) != 5:
			return

		# 분리되는 개수 확인
		split_list = []
		if self.edtNewNum1.text() != '':
			split_list.append(self.edtNewNum1.text())
		if self.edtNewNum2.text() != '':
			split_list.append(self.edtNewNum2.text())
		if self.edtNewNum3.text() != '':
			split_list.append(self.edtNewNum3.text())
		split_count = len(split_list)
		if split_count == 0:
			return

		# 뒤에 미뤄야 할 값이 있는 지 확인
		start_index = int(parts[3]) + 1
		end_index = start_index

		while True:
			num_info_key = parts[1] + '_' + parts[2] + '_' + str(end_index)
			if num_info_key in self.num_info_dict:
				end_index += 1
			else:
				break

		end_index -= 1
		data_dir = '../data/_num_' + self.listFile.currentItem().text()

		while end_index >= start_index:
			# 뒤에서부터 변경할 파일 찾음
			old_file_pattern = '_' + parts[1] + '_' + parts[2] + '_' + str(end_index) + '_*.png'
			old_file_list = glob.glob(os.path.join(data_dir, old_file_pattern))
			if len(old_file_list) != 1:
				print('error: ' + old_file_pattern)
				return
			pts = os.path.basename(old_file_list[0]).split('_')
			pts[3] = str(end_index + split_count - 1)
			new_file_name = '_'.join(pts)
			new_file_name = new_file_name.replace(' ', '')
			new_file_path = os.path.join(data_dir, new_file_name)
			os.rename(old_file_list[0], new_file_path)

			end_index -= 1

		sp_start_index = int(parts[3])
		sp_file_name = self.selected_file_name
		for i in range(split_count):
			new_file_name = '_' + parts[1] + '_' + parts[2] + '_' + str(sp_start_index + i) + '_' + split_list[i] + '.png'
			if sp_file_name == new_file_name:
				continue
			if i == 0:
				os.rename(os.path.join(data_dir, sp_file_name), os.path.join(data_dir, new_file_name))
				sp_file_name = new_file_name
			else:
				shutil.copy(os.path.join(data_dir, sp_file_name), os.path.join(data_dir, new_file_name))


	def OnInsertNumValue(self):
		# 삽입되는 개수 확인
		insert_list = []
		if self.edtInNum1.text() != '':
			insert_list.append(self.edtInNum1.text())
		if self.edtInNum2.text() != '':
			insert_list.append(self.edtInNum2.text())
		if self.edtInNum3.text() != '':
			insert_list.append(self.edtInNum3.text())
		insert_count = len(insert_list)
		if insert_count == 0:
			return

		data_dir = '../data/_num_' + self.listFile.currentItem().text()

		# 뒤에 미뤄야 할 값이 있는 지 확인
		start_index = int(self.edtInPos2.text())
		end_index = start_index

		while True:
			num_info_key = self.comboXY.currentText() + '_' + self.edtInPos1.text() + '_' + str(end_index)
			file_pattern = '_' + self.comboXY.currentText() + '_' + self.edtInPos1.text() + '_' + str(end_index) + '_*.png'
			file_list = glob.glob(os.path.join(data_dir, file_pattern))
			if len(file_list) == 0:
				break
			end_index += 1

		end_index -= 1

		while end_index >= start_index:
			# 뒤에서부터 변경할 파일 찾음
			old_file_pattern = '_' + self.comboXY.currentText() + '_' + self.edtInPos1.text() + '_' + str(end_index) + '_*.png'
			old_file_list = glob.glob(os.path.join(data_dir, old_file_pattern))
			if len(old_file_list) != 1:
				print('error: ' + old_file_pattern)
				return
			pts = os.path.basename(old_file_list[0]).split('_')
			pts[3] = str(end_index + insert_count)
			new_file_name = '_'.join(pts)
			new_file_name = new_file_name.replace(' ', '')
			new_file_path = os.path.join(data_dir, new_file_name)
			os.rename(old_file_list[0], new_file_path)

			end_index -= 1

		insert_start_index = int(self.edtInPos2.text())
		for i in range(insert_count):
			new_file_name = '_' + self.comboXY.currentText() + '_' + self.edtInPos1.text() + '_' + str(insert_start_index + i) + '_' + insert_list[i] + '.png'
			new_file_path = os.path.join(data_dir, new_file_name)
			with open(new_file_path, 'w') as f:
				os.utime(new_file_path, None)

def main():
	app = QApplication(sys.argv)
	frmMain = frmNemo()
	frmMain.show()

	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
