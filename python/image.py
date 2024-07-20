import cv2
import numpy as np
import pytesseract
import re

def get_list_from_image(img_name):
    err_count = 0
    rgb = cv2.imread(img_name)
    small = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    # cv2.imshow('small', small)
    # cv2.imshow('small', small)
    # bw = cv2.adaptiveThreshold(small, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 99, 4)
    _, bw = cv2.threshold(small, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # bw = 255 - bw.copy()
    # cv2.floodFill(bw, None, (0, 0), (0, 0, 0), (5, 5, 5, 5), (5, 5, 5, 5))
    # cv2.imshow('bw', bw)
    # cv2.waitKey()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
    # using RETR_EXTERNAL instead of RETR_CCOMP
    contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # contours, hierarchy = cv2.findContours(None, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    num_img = np.zeros((40, 80), dtype=np.uint8)
    mask = np.zeros(bw.shape, dtype=np.uint8)
    num_base = np.zeros(bw.shape, dtype=np.uint8)
    margin = 10
    _list = []
    for idx in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[idx])
        mask[y:y+h, x:x+w] = 0
        cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
        r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)
        # print(x, y, w, h, r)
        # 20x20
        # if r > 0.35 and (8 < w < 70) and (8 < h < 28) and y < 1900:
        # 25x25
        # if r > 0.35 and (8 < w < 70) and (8 < h < 35) and (200 < y < 1900):
        # 30x30
        if r > 0.35 and (8 < w < 70) and (8 < h < 35) and (200 < y < 1900):
            num_base[y-margin:y+h+margin*2, x-margin:x+w+margin*2] = 1
            cv2.rectangle(rgb, (x, y), (x+w-1, y+h-1), (0, 255, 0), 2)
            # num_img.fill(0)
            # num_img[12:12+h, 20:20+w] = bw[y:y+h, x:x+w].copy()
            num_img = bw[y-2:y+h+4, x-2:x+w+4].copy()

            ##
            # cv2.imshow('num-1', num_img)
            # cv2.waitKey()
            ##

            num = pytesseract.image_to_string(num_img, config='-l snum --psm 6')
            num_org = num
            num = num.replace("ji", "1")
            num = num.replace("ii", "1")
            num = num.replace("ll", "1")
            num = num.replace("T", "1")
            num = num.replace("i", "1")
            num = num.replace("j", "1")
            num = num.replace("l", "1")
            num = num.replace("\n", "")
            num = num.replace("s", "3")
            num = num.replace("S", "5")
            num = num.replace("e", "8")

            # if (num[0] == 'T') or (num[0] == 'l' and num[1] in ('\n', 'l')) or (num[0] in ('i', 'j') and num[1] in ('\n', 'i')):
            #     num = "1"
            # elif num[0] == 'l' and num[1] == 'o':
            #     num = "10"
            # elif num[0] == 's' and num[1] == '\n':
            #     num = "3"
            # elif num[0] == '\f':
            #     continue
            try:
                num = re.findall('(\d+)', num)[0]
            except:
                err_count += 1
                cv2.imwrite(img_name + '_err_' + str(err_count) + '.png', num_img)


            try:
                num = int(num)
            except ValueError as e:
                print(num)
                # cv2.imshow('num-err', num_img)

                ##
                # cv2.waitKey()
                ##

                num = 0
            print(idx, x, y, w, h, int(x + w / 2), int(y + h / 2), num)
            _list.append([idx, x, y, w, h, int(x + w / 2), int(y + h / 2), num])
        else:
            cv2.rectangle(rgb, (x, y), (x+w-1, y+h-1), (255, 0, 0), 2)

    # con2, _ = cv2.findContours(num_base.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # for c in con2:
    #     x, y, w, h = cv2.boundingRect(c)
    #     cv2.rectangle(rgb, (x, y), (x+w-1, y+h-1), (0, 0, 255), 2)

    # show image with contours rect
    cv2.imshow('rects', rgb)
    cv2.imwrite(img_name + '_out.png', rgb)
    # cv2.waitKey()

    return _list


def is_in(prev_x, prev_w, cur_x, cur_w):
    return not ((prev_x > cur_x + cur_w) or (prev_x + prev_w < cur_x))

index_x = 5
index_y = 6
index_value = 7

def reindex_list(_list, num):
    # 일단 뒤집어서 경계영역부터 찾는다.
    _list = sorted(_list, reverse=True, key=lambda x: x[num])
    base_count = len(_list) // 3
    base_max = 0
    num_reverse = index_x
    if num == num_reverse:
        num_reverse = index_y

    for i in range(base_count):
        if base_max < (_list[i][num_reverse-4] + _list[i][num_reverse-2]):
            base_max = _list[i][num_reverse - 4] + _list[i][num_reverse - 2]

    _list = sorted(_list, key=lambda x: x[num])

    print("-------------------------------------------------")
    prev_xy = 0
    prev_wh = 0
    index = -1
    for i in _list:
        if i[num_reverse-4] > base_max:
            i[num] = -1
            continue
        if (not is_in(prev_xy, prev_wh, i[num-4], i[num-2])) or prev_xy == 0:
            index += 1
            # 비교범위 새로
            prev_xy = i[num-4]
            prev_wh = i[num-2]
        # 비교범위 확장
        if prev_xy > i[num-4]:
            prev_wh += prev_xy - i[num-4]
            prev_xy = i[num-4]
        if prev_xy+prev_wh < i[num-4]+i[num-2]:
            prev_wh += i[num-4]+i[num-2] - (prev_xy+prev_wh)

        i[num] = index
        print(" ".join(map(str, i)))
    return _list

# idx, x, y, w, h, mid_x, mid_y, value
def save_file(_list, out_file):
    # 그룹별로 위치만 정한다
    _list = reindex_list(_list, index_y)
    _list = reindex_list(_list, index_x)

    # 그룹 내에서 순서를 정한다.
    max_col = max(sub[index_x] for sub in _list) + 1
    max_row = max(sub[index_y] for sub in _list) + 1

    f = open(out_file, 'wt')
    f.write("{0} {1}\n".format(max_col, max_row))

    _list = sorted(_list, key=lambda x: x[2] + x[index_x] * 100000)
    w_list = []
    prev_xy = 0
    for i in _list:
        if i[index_x] >= 0:
            if prev_xy != i[index_x]:
                prev_xy = i[index_x]
                f.write("{0} ".format(len(w_list)))
                f.write(" ".join(map(str, w_list)))
                f.write("\n")
                w_list = [ i[index_value] ]
            else:
                w_list.append(i[index_value])

    f.write("{0} ".format(len(w_list)))
    f.write(" ".join(map(str, w_list)))
    f.write("\n")
    f.write("\n")

    _list = sorted(_list, key=lambda x: x[1] + x[index_y] * 100000)
    w_list = []
    prev_xy = 0
    for i in _list:
        if i[index_y] >= 0:
            if prev_xy != i[index_y]:
                prev_xy = i[index_y]
                f.write("{0} ".format(len(w_list)))
                f.write(" ".join(map(str, w_list)))
                f.write("\n")
                w_list = [ i[index_value] ]
            else:
                w_list.append(i[index_value])

    f.write("{0} ".format(len(w_list)))
    f.write(" ".join(map(str, w_list)))
    f.write("\n")
    f.write("\n")

    f.close()

# img_name = '1-3249.jpeg'    # 25 x 25
# img_name = '1-130.jpeg'     # 30 x 30
# img_name = '1-133.PNG'
img_name = '1-4415.PNG'
n_list = get_list_from_image('../data/' + img_name)
save_file(n_list, '../data/' + img_name + '.in')
