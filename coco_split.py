import json
import argparse
import funcy
from sklearn.model_selection import train_test_split
import os 
import xlrd
import pandas as pd

import sys

# parser = argparse.ArgumentParser(description='Splits COCO annotations file into training and test sets.')
# parser.add_argument('annotations', metavar='coco_annotations', type=str,
#                     help='Path to COCO annotations file.')
# parser.add_argument('--train_ratio', type=float, dest='ratio_train', help='set train dataset ratio')
# parser.add_argument('--valid_ratio', type=float,  dest='ratio_valid',help='set valid dataset ratio')
# parser.add_argument('--test_ratio', type=float,  dest='ratio_test',help='set test dataset ratio')
# parser.add_argument('--trainJson_name', type=str, default='train.json', help='Where to store COCO training annotations')
# parser.add_argument('--validJson_name', type=str, default='valild.json', help='Where to store COCO valid annotations')
# parser.add_argument('--testJson_name', type=str, default='test.json', help='Where to store COCO test annotations')
# parser.add_argument('--annotations', dest='annotations', action='store_true',
#                     help='Ignore all images without annotations. Keep only these with at least one annotation')
# parser.add_argument('--split_save_folder', type=str, default='test.json', help='Where to store COCO test annotations')
# args = parser.parse_args()

# ratio_train = args.ratio_train
# ratio_valid = args.ratio_valid
# ratio_test = args.ratio_test

def save_coco(file, info, images, annotations, categories):

    images['id']="0"
    for annotation in annotations:
        annotation['image_id']=0

    with open(file, 'wt', encoding='UTF-8') as coco:
        json.dump({ 'info': info, 'categories': categories, 'images': [images], 
            'annotations': annotations}, coco, indent=2, sort_keys=False)

def filter_annotations(annotations, images):

    image_ids = funcy.lmap(lambda i: int(i['id']), images)
    return funcy.lfilter(lambda a: int(a['image_id']) in image_ids, annotations)

def main(annotations, split_save_folder):
    with open(annotations, 'rt', encoding='UTF-8') as annotations:
        coco = json.load(annotations)
        info = coco['info']
        # licenses = coco['licenses']
        images = coco['images']
        annotations = coco['annotations']
        categories = coco['categories']

        number_of_images = len(images)

        images_with_annotations = funcy.lmap(lambda a: int(a['image_id']), annotations)

        if annotations:
            images = funcy.lremove(lambda i: i['id'] not in images_with_annotations, images)

        # train_before, test = train_test_split(
        #     images, test_size=ratio_test)

        # ratio_remaining = 1 - ratio_test
        # ratio_valid_adjusted = ratio_valid / ratio_remaining

        # train_after, valid = train_test_split(
        #     train_before, test_size=ratio_valid_adjusted)
 

        for data in images:
            #print(data)
            image_name=data['file_name'].replace('.jpg','.json')
            save_name=os.path.join(split_save_folder,image_name)
            save_data = filter_annotations(annotations, [data])

            split_data=[]
            for split_categories in save_data:
                split_data.append(split_categories['category_id'])
      
            new_categories=[]           
            for split_id in split_data:
                new_categories.append(categories[split_id - 1])

            save_coco(save_name, info, data, save_data, new_categories)

        
        # save_coco(args.trainJson_name, info, licenses, train_after, filter_annotations(annotations, train_after), categories)
        # save_coco(args.testJson_name, info, licenses, test, filter_annotations(annotations, test), categories)
        # save_coco(args.validJson_name, info, licenses, valid, filter_annotations(annotations, valid), categories)

        # print("Saved {} entries in {} and {} in {} and {} in {}".format(len(train_after), args.trainJson_name, len(test), args.testJson_name, len(valid), args.validJson_name))

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


if __name__ == "__main__":
    argument = sys.argv[1]

    basename = os.path.basename(argument)
    abspath = os.path.abspath(argument)
    
    print(abspath)
    if basename != "0st.json":
        exit()
    #test = annotations.split('/')
    
    splitSavePath = abspath.split('/')
    splitSavePath = '/'.join(splitSavePath[:-2]) +"/split"

    createFolder(splitSavePath)
    

    main(abspath,splitSavePath)

    os.remove(abspath)