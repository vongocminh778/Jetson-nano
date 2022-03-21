import os
import shutil
import json
split_size = 0.2 # 20% for test dataset 

path = "Batman-Ironman-Dataset/" # directory
try :
    os.mkdir(path + "train")
    os.mkdir(path +"val")
except :
    print("`train/` and `val/` dir already exist!")
    if input("do you want to delete `train/` and `val/` dir content? [y/n]") == 'y' :
        shutil.rmtree(path + "train")
        shutil.rmtree(path +"val")
        os.mkdir(path + "train")
        os.mkdir(path +"val")

all_filenames = []
for file in os.listdir(path):
    if file.endswith(".jpg"):
        all_filenames.append(file.replace(".jpg", ""))

file_counter = {}
file_group = {}
for name in all_filenames:
    label = name.split("_")[0]
    try :
        file_counter[label] += 1
        file_group[label].append(name)
    except :
        file_counter[label] = 1
        file_group[label] = []
        file_group[label].append(name)
        
print(file_counter)
        
for label in file_counter:
    n_split = int(file_counter[label]*split_size)
    for i, name in enumerate(file_group[label]) :
        if i < n_split :
            shutil.move(path + name + ".jpg", path + "val")
            shutil.move(path + name + ".xml", path + "val")
        else :
            shutil.move(path + name + ".jpg", path + "train")
            shutil.move(path + name + ".xml", path + "train")  

# # create label map pbtxt 
# with open("data/object-detection.pbtxt", "w") as fw:
#     for i, name in enumerate(file_counter, start=1) :
#         fw.write('item {\n')
#         fw.write('\tid : %d\n' % i)
#         fw.write('\tname : "%s"\n' % name)
#         fw.write('}\n')

# # create label map json 
# label_json = {}      
# for i, name in enumerate(file_counter, start=0):
#     label_json[str(i)] = name
    
# with open("object-detection.json", 'w') as f:
#     json.dump(label_json, f)
