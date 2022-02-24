import glob
import os
import pickle
import xml.etree.ElementTree as ET
from os import listdir, getcwd
from os.path import join

classes = ['cosilicon', 'kosilicon'] # labels


def getImagesInDir(dir_path):
    image_list = []
    for filename in glob.glob(dir_path + '/*.jpg'):
        image_list.append(filename)

    return image_list


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(dir_path, output_path, image_path):
    print(f"dir_path : {dir_path}")
    print(f"output_path : {output_path}")
    print(f"image_path : {image_path}")

    basename = os.path.basename(image_path)
    print(f"basename : {basename}")
    basename_no_ext = os.path.splitext(basename)[0]
    print(f"basename_no_ext : {basename_no_ext}")

    in_file = open(dir_path + '/' + basename_no_ext + '.xml')
    out_file = open(output_path + basename_no_ext + '.txt', 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


cwd = getcwd() # get current directory
full_dir_path = cwd + "/data/"
_images_path = full_dir_path + "JPEGImages"
_annotations_path = full_dir_path + "Annotations"
output_path = full_dir_path + 'yolo/' # create folder save yolo labels

if not os.path.exists(output_path):
    os.makedirs(output_path)

image_paths = getImagesInDir(_images_path)
list_file = open(output_path + 'yolo.txt', 'w')

for image_path in image_paths:
    list_file.write(image_path + '\n')
    convert_annotation(_annotations_path, output_path, image_path)
list_file.close()

