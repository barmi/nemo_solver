import cv2
import numpy as np
import pytesseract


def get_list_from_image(img_name):
    rgb = cv2.imread(img_name)
    small = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    cv2.imshow('small', small)
    # cv2.imshow('small', small)
    # bw = cv2.adaptiveThreshold(small, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 99, 4)
    _, bw = cv2.threshold(small, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # bw = 255 - bw.copy()
    # cv2.floodFill(bw, None, (0, 0), (0, 0, 0), (5, 5, 5, 5), (5, 5, 5, 5))
    cv2.imshow('bw', bw)
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
        if r > 0.35 and 8 < w < 70 and 8 < h < 28 and y < 1600:
            num_base[y-margin:y+h+margin*2, x-margin:x+w+margin*2] = 1
            cv2.rectangle(rgb, (x, y), (x+w-1, y+h-1), (0, 255, 0), 2)
            # num_img.fill(0)
            # num_img[12:12+h, 20:20+w] = bw[y:y+h, x:x+w].copy()
            num_img = bw[y-2:y+h+4, x-2:x+w+4].copy()
            # cv2.imshow('num', num_img)
            # cv2.waitKey()
            num = pytesseract.image_to_string(num_img, config='-l snum --psm 6')
            if (num[0] == 'l' and num[1] in ('\n', 'l')) or (num[0] in ('i', 'j') and num[1] in ('\n', 'i')):
                num = "1"
            elif num[0] == 'l' and num[1] == 'o':
                num = "10"
            elif num[0] == 's' and num[1] == '\n':
                num = "3"
            elif num[0] == '\f':
                continue

            try:
                num = int(num)
            except ValueError as e:
                print(num)
                cv2.imshow('num', num_img)
                # cv2.waitKey()
                num = 0
            print(idx, x, y, w, h, num)
            _list.append([x, y, w, h, int(x + w / 2), int(y + h / 2), num])
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


def reindex_list(_list, num):
    _list = sorted(_list, key=lambda x: x[num])
    print("-------------------------------------------------")
    prev_num = 0
    index = -1
    for i in _list:
        if abs(prev_num - i[num]) > 6:
            index += 1
        prev_num = i[num]
        i[num] = index
        print(" ".join(map(str, i)))


def save_file(_list, out_file):
    reindex_list(_list, 5)
    reindex_list(_list, 4)
    max_col = max(sub[4] for sub in _list) + 1
    max_row = max(sub[5] for sub in _list) + 1
    num_list = np.zeros((max_row, max_col), dtype=np.uint8)
    num_list[0:max_row, 0:max_col] = 0
    for i in _list:
        num_list[i[5], i[4]] = i[6]
    print(num_list)

    x = max_col - 1
    while num_list[max_row-1, x] == 0:
        x -= 1
    x += 1
    print("min x = ", x)
    y = max_row - 1
    while num_list[y, x] == 0:
        y -= 1
    y += 1
    print("min y = ", y)

    f = open(out_file, 'wt')
    f.write("{0} {1}\n".format(max_col - x, max_row - y))

    for i in range(x, max_col):
        col_num = []
        for j in range(y):
            if num_list[j, i]:
                col_num.append(num_list[j, i])
        f.write("{0} ".format(len(col_num)))
        f.write(" ".join(map(str, col_num)))
        f.write("\n")

    f.write('\n')
    for j in range(y, max_row):
        row_num = []
        for i in range(x):
            if num_list[j, i]:
                row_num.append(num_list[j, i])
        f.write("{0} ".format(len(row_num)))
        f.write(" ".join(map(str, row_num)))
        f.write("\n")

    f.close()

    return num_list


n_list = get_list_from_image('./nemo_1_566.png')
save_file(n_list, '../data/nemo_1_566.in')
