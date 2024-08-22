import os
import shutil
import glob
from _0_game_num import *

def process_2():
    # 디렉토리 이름 설정
    png_dir = "../data/_num_" + game_num

    # 디렉토리가 없으면 생성
    os.makedirs(png_dir, exist_ok=True)

    # '_x_*.png' 또는 '_y_*.png' 패턴과 일치하는 모든 파일 찾기
    files_to_move = glob.glob("../data/_[xy]_*.png")

    # 찾은 파일들을 새 디렉토리로 이동
    for file in files_to_move:
        shutil.move(file, os.path.join(png_dir, os.path.basename(file)))

    print(f"{len(files_to_move)}개의 파일을 {png_dir} 디렉토리로 이동했습니다.")


if __name__ == "__main__":
    process_2()
