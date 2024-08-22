from _1_image_process import process_1
from _2_mv_png_dir import process_2
from _3_num_dir_to_in_file import process_3

game_num = '1-4788'
img_name = game_num + '.PNG'
use_saved_setxy = True

if __name__ == "__main__":
	process_1()
	process_2()
	process_3()
