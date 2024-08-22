import os
import re
import shutil
from _0_game_num import *


def natural_sort_key(s):
	"""
    Split the input string into a list of integers and non-integer parts,
    and return the list. This allows for natural human sorting based on
    both numerical and non-numerical parts of strings.
    """
	return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def process_3():
	# game_num = "1-4536"
	num_dir = "../data/_num_{0}".format(game_num)
	in_file = "../data/{0}.in".format(game_num)

	# num_dir 아래에 숫자로 시작하는 디렉토리가 있으면 모두 지우고 시작한다.
	if os.path.exists(num_dir):
		for root, dirs, files in os.walk(num_dir, topdown=False):
			for name in dirs:
				shutil.rmtree(os.path.join(root, name))

	def cp_num_file(filename, num):
		# mkdir num_dir/num force
		if not os.path.exists("{0}/{1}".format(num_dir, num)):
			os.makedirs("{0}/{1}".format(num_dir, num))
		system_cmd = "cp {0} {1}/{2}".format(filename, num_dir, num)
		os.system(system_cmd)

	# read all files in num_dir
	num_files = sorted(os.listdir(num_dir), key=natural_sort_key)
	print(num_files)

	list_x = []
	list_y = []
	sum_x = 0
	sum_y = 0

	prev_f_2 = 0
	for f in num_files:
		try:
			f1 = f.split("_")
			val = int(f1[4].split(".")[0])
			f_2 = int(f1[2])
			f_3 = int(f1[3])

			if f1[1] == "x":
				sum_x += val

				if (int(f_2) >= len(list_x)):
					list_x.append([])
				if (int(f_3) >= len(list_x[int(f_2)])):
					list_x[int(f_2)].append(val)
				else:
					print("error: {0}".format(f))
					exit(0)

			if f1[1] == "y":
				sum_y += val

				if (int(f_2) >= len(list_y)):
					list_y.append([])
				if (int(f_3) >= len(list_y[int(f_2)])):
					list_y[int(f_2)].append(val)
				else:
					print("error: {0}".format(f))
					exit(0)

			cp_num_file("{0}/{1}".format(num_dir, f), val)
		except:
			print("error: {0}".format(f))
			continue

	print("sum_x: {0}, sum_y: {1}".format(sum_x, sum_y))

	f = open(in_file, 'wt')
	f.write("{0} {1}\n".format(len(list_x), len(list_y)))
	for i in list_x:
		f.write("{0} ".format(len(i)))
		f.write(" ".join(map(str, i)))
		f.write("\n")
	f.write("\n")
	for i in list_y:
		f.write("{0} ".format(len(i)))
		f.write(" ".join(map(str, i)))
		f.write("\n")
	f.write("\n")
	f.close()

if __name__ == "__main__":
	process_3()
