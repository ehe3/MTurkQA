import argparse
import cv2
import os
import json
import numpy as np

# fname: image file name
def get_json_fname(fname):
    return os.path.splitext(fname)[0] + '.json'

# fname: image file name
def get_txt_fname(fname):
    return os.path.splitext(fname)[0] + '.txt'

# path: image path
def generate_img(img_path, json_path):
    img = cv2.imread(img_path)
    if not os.path.isfile(json_path):
        return cv2.resize(img, (img.shape[1]*2, img.shape[0]*2))
    with open(json_path, 'r') as json_file:
        annotation_data = json.load(json_file)
        shapes = annotation_data['shapes']
        for shape in shapes:
            pts = np.empty((len(shape['points']), 2), np.int32)
            for idx, point in enumerate(shape['points']):
                pts[idx] = point
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (0, 255, 255))
    return cv2.resize(img, (img.shape[1]*2, img.shape[0]*2))

parser = argparse.ArgumentParser()
parser.add_argument('src', help='directory to evaluate', type=str)
parser.add_argument('reverse', help='review selected images', type=bool, nargs='?', default=False)
args = parser.parse_args()

files = []
if not args.reverse:
    for r, d, f in os.walk(args.src):
        for img in f:
            if '.png' in img and not os.path.isfile(os.path.join(args.src, get_txt_fname(img))):
                files.append(img)
else:
    for r, d, f in os.walk(args.src):
        for img in f:
            if '.png' in img and os.path.isfile(os.path.join(args.src, get_txt_fname(img))):
                files.append(img)
files = sorted(files)

curr_img_num = 0
print(files[curr_img_num])
img = generate_img(os.path.join(args.src, files[0]), os.path.join(args.src, get_json_fname(files[0])))
while True:
    cv2.imshow('Have fun!', img)
    k = cv2.waitKey()
    # space bar pressed
    if k == 32:
        approved_file = os.path.join(args.src, get_txt_fname(files[curr_img_num]))
        if not os.path.isfile(approved_file):
            f = open(approved_file, 'w+')
            f.write('Approved, Matey!')
            f.close() 
        if curr_img_num != len(files) - 1:
            curr_img_num = curr_img_num + 1
            print(files[curr_img_num])
            img = generate_img(os.path.join(args.src, files[curr_img_num]), os.path.join(args.src, get_json_fname(files[curr_img_num])))
    # del key pressed
    elif k == 255:
        approved_file = os.path.join(args.src, get_txt_fname(files[curr_img_num]))
        if os.path.isfile(approved_file):
            os.remove(approved_file)
        if curr_img_num != len(files) - 1:
            curr_img_num = curr_img_num + 1
            print(files[curr_img_num])
            img = generate_img(os.path.join(args.src, files[curr_img_num]), os.path.join(args.src, get_json_fname(files[curr_img_num])))
    # b key pressed
    elif k == 98:
        if curr_img_num != 0: 
            curr_img_num = curr_img_num - 1
            print(files[curr_img_num])
            img = generate_img(os.path.join(args.src, files[curr_img_num]), os.path.join(args.src, get_json_fname(files[curr_img_num])))
        
    # q key pressed
    elif k == 113:
        break;


