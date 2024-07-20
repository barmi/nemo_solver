from collections import Counter

import cv2
import numpy as np
import pytesseract
import re

# import numpy as np
from scipy import stats


def normalize_to_grid(points, grid_size):
    points = np.array(points)
    x, y = points[:, 0], points[:, 1]

    x_min, x_max = np.min(x), np.max(x)
    y_min, y_max = np.min(y), np.max(y)

    # 데이터의 범위 계산
    x_range = x_max - x_min
    y_range = y_max - y_min

    # 데이터 포인트 개수의 제곱근을 사용하여 초기 격자 수 추정
    initial_grid_size = int(np.sqrt(len(points)))

    # 격자 수를 지정된 범위 내로 조정
    # grid_size = np.clip(initial_grid_size, min_grid_size, max_grid_size)
    # grid_size = 30+1

    # 격자 간격 계산 (x와 y 방향 중 큰 값 사용)
    grid_step = max(x_range, y_range) / (grid_size - 1)

    # 각 점을 가장 가까운 격자점으로 이동
    x_normalized = np.round((x - x_min) / grid_step) * grid_step + x_min
    y_normalized = np.round((y - y_min) / grid_step) * grid_step + y_min

    # 정규화된 좌표를 새로운 배열로 결합
    normalized_points = np.column_stack((x_normalized, y_normalized))

    # 정규화된 x값과 y값을 set으로 변환
    x_set = set(x_normalized)
    y_set = set(y_normalized)

    return normalized_points, grid_size, x_set, y_set


def find_grid2(img_name):
    image  = cv2.imread(img_name)
    cv2.imshow("Image", image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray", gray)

    blur = cv2.GaussianBlur(gray, (5,5), 15)
    cv2.imshow("blur", blur)

    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 3, 2)
    cv2.imshow("thresh", thresh)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    c = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:
            if area > max_area:
                max_area = area
                best_cnt = i
                # image = cv2.drawContours(image, contours, c, (0, 255, 0), 3)
                # image = cv2.drawContours(image, contours, c, (0, 0, 255), 3)
        c+=1

    mask = np.zeros((gray.shape),np.uint8)
    cv2.drawContours(mask,[best_cnt],0,255, -1)
    cv2.drawContours(mask,[best_cnt],0,0,5)
    cv2.imshow("mask", mask)

    out = np.zeros_like(gray)
    out[mask == 255] = gray[mask == 255]
    cv2.imshow("New image", out)

    blur = cv2.GaussianBlur(out, (5,5), 0)
    cv2.imshow("blur1", blur)

    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    cv2.imshow("thresh1", thresh)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)





    '''
    '''
    max_area = 0
    c = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:
            if area > max_area:
                max_area = area
                best_cnt = i
                # image = cv2.drawContours(image, contours, c, (0, 255, 0), 3)
                # image = cv2.drawContours(image, contours, c, (0, 0, 255), 3)
        c+=1

    mask = np.zeros((gray.shape),np.uint8)
    cv2.drawContours(mask,[best_cnt],0,255, -1)
    cv2.drawContours(mask,[best_cnt],0,0,5)
    cv2.imshow("mask", mask)

    out = np.zeros_like(gray)
    out[mask == 255] = gray[mask == 255]
    cv2.imshow("New image", out)

    blur = cv2.GaussianBlur(out, (5,5), 0)
    cv2.imshow("blur1", blur)

    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    cv2.imshow("thresh1", thresh)

    '''
    '''







    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    c = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000/2:
            cv2.drawContours(image, contours, c, (0, 255, 0), 1)
        c+=1

    min_w = 9999999
    min_h = 9999999
    # set_x = []
    # set_y = []
    set_xx = set()
    set_yy = set()
    points = []
    min_xx = 9999999
    min_yy = 9999999
    max_xx = 0
    max_yy = 0
    for idx in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[idx])

        points.append((x, y))
        # points.append((x+w, y+h))

        # set_x.append(x)
        # set_y.append(y)
        set_xx.add(x)
        set_xx.add(x+w)
        set_yy.add(y)
        set_yy.add(y+h)

        # print(f'idx: {idx}, x: {x}, y: {y}, w: {w}, h: {h}')
        # cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
        # cv2.imshow("Final Image", image)
        # cv2.waitKey(0)
        if w < min_w:
            min_w = w
        if h < min_h:
            min_h = h
        if x < min_xx:
            min_xx = x
        if y < min_yy:
            min_yy = y
        if x+w > max_xx:
            max_xx = x+w
        if y+h > max_yy:
            max_yy = y+h

    set_xx = sorted(set_xx)
    set_yy = sorted(set_yy)

    count_x = 0
    for i in range(len(set_xx) - 1):
        diff = set_xx[i + 1] - set_xx[i]
        if diff > 10:
            count_x += 1
        print(f'{i}: {set_xx[i]} -> Next: {set_xx[i + 1]}, Difference: {set_xx[i + 1] - set_xx[i]}')

    print(f'count_x: {count_x}')

    normalized, grid_size, set_x, set_y = normalize_to_grid(points, count_x+1)

    set_x = {int(x) for x in set_x}
    set_y = {int(y) for y in set_y}

    print("Original points:", points)
    print("Normalized points:", normalized.tolist())
    print("Estimated grid size:", grid_size)

    print(f'min_w: {min_w}, min_h: {min_h}')
    # sort set_x, set_y
    set_x = sorted(set_x)
    set_y = sorted(set_y)

    x_freq = Counter(set_x)
    y_freq = Counter(set_y)

    print(f'x_freq: {x_freq}')
    print(f'y_freq: {y_freq}')


    for i in range(len(set_x) - 1):
        print(f'{i}: {set_x[i]} -> Next: {set_x[i + 1]}, Difference: {set_x[i + 1] - set_x[i]}')


    min_x = min(set_x)
    max_x = max(set_x)
    min_y = min(set_y)
    max_y = max(set_y)

    gap_x = ((max_xx - min_xx) - (max_x - min_x)) // 2
    gap_y = ((max_yy - min_yy) - (max_y - min_y)) // 2

    set_x = {x + gap_x for x in set_x}
    set_y = {y + gap_y for y in set_y}
    min_x += gap_x
    max_x += gap_x
    min_y += gap_y
    max_y += gap_y

    for x in set_x:
        cv2.line(image, (x, min_y), (x, max_y), (0, 0, 255), 2)
    for y in set_y:
        cv2.line(image, (min_x, y), (max_x, y), (0, 0, 255), 2)

    # cv2.imshow("Final Image", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return set_x, set_y






def find_grid(img_name):
    filter = False

    img = cv2.imread(img_name)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray,90,150,apertureSize = 3)
    kernel = np.ones((3,3),np.uint8)
    edges = cv2.dilate(edges,kernel,iterations = 1)
    kernel = np.ones((5,5),np.uint8)
    edges = cv2.erode(edges,kernel,iterations = 1)
    cv2.imwrite('canny.jpg',edges)

    lines = cv2.HoughLines(edges,1,np.pi/180,150)

    if not lines.any():
        print('No lines were found')
        exit()

    if filter:
        rho_threshold = 15
        theta_threshold = 0.1

        # how many lines are similar to a given one
        similar_lines = {i : [] for i in range(len(lines))}
        for i in range(len(lines)):
            for j in range(len(lines)):
                if i == j:
                    continue

                rho_i,theta_i = lines[i][0]
                rho_j,theta_j = lines[j][0]
                if abs(rho_i - rho_j) < rho_threshold and abs(theta_i - theta_j) < theta_threshold:
                    similar_lines[i].append(j)

        # ordering the INDECES of the lines by how many are similar to them
        indices = [i for i in range(len(lines))]
        indices.sort(key=lambda x : len(similar_lines[x]))

        # line flags is the base for the filtering
        line_flags = len(lines)*[True]
        for i in range(len(lines) - 1):
            if not line_flags[indices[i]]: # if we already disregarded the ith element in the ordered list then we don't care (we will not delete anything based on it and we will never reconsider using this line again)
                continue

            for j in range(i + 1, len(lines)): # we are only considering those elements that had less similar line
                if not line_flags[indices[j]]: # and only if we have not disregarded them already
                    continue

                rho_i,theta_i = lines[indices[i]][0]
                rho_j,theta_j = lines[indices[j]][0]
                if abs(rho_i - rho_j) < rho_threshold and abs(theta_i - theta_j) < theta_threshold:
                    line_flags[indices[j]] = False # if it is similar and have not been disregarded yet then drop it now

    print('number of Hough lines:', len(lines))

    filtered_lines = []

    if filter:
        for i in range(len(lines)): # filtering
            if line_flags[i]:
                filtered_lines.append(lines[i])

        print('Number of filtered lines:', len(filtered_lines))
    else:
        filtered_lines = lines

    for line in filtered_lines:
        rho,theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

    cv2.imwrite(img_name + '_out.png', img)



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
# img_name = '1-4302.jpeg'
img_name = '1-4415.PNG'
# n_list = get_list_from_image('../data/' + img_name)
# save_file(n_list, '../data/' + img_name + '.in')

find_grid2('../data/' + img_name)
