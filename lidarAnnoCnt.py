import sys
import os
import json
import argparse

from pathlib import Path

import csv


def cheak_abs_name(name_list):
    for part_name in name_list:
        if (part_name >= '0' and part_name <= '9999999' and len(part_name) == 7):
          return part_name

    return 0


class custom_dataset:
    def __init__(self, info, licenses):
        self.cocoFormat = {'info': info, 'licenses': licenses, 'images': [], 'annotations': [], 'categories': []}
        self.categorieFlag = 1
        
        self.id_cnt = 1

        self.annoClass = dict()
        self.ratioClass = dict()
        #self.annoClass = {"Pedestrian": 0, \
        #                    "Unknown": 0, \
        #                    "Car": 0, \
        #                    "Bus": 0, \
        #                    "Truck": 0, \
        #                    "BicycleRider": 0, \
        #                    "MotorcyleRider": 0, \
        #                    "Misc": 0}
        #                

    def invisible_data(self, inKey):
        pairName = {'images': 'images', 'categories': 'Categories', 'annotations': 'annotations'}
        for val in pairName.values():
            if val in inKey:
                continue
            else:
                print("error 0")
                exit()

    def count_keypoint(self, keypoints):
        cnt = 0
        i = 2
        while i < 50:
            if keypoints[i] == 0:
                cnt = cnt + 1
            i = i+3   

        return 17 - cnt

    def calc_area(self,bbox):
        return abs(bbox[2] - bbox[0]) * (bbox[3] - bbox[1])

    def set_coco_format(self, data):
        image = dict()        
        for imagesData in data['images']:
            image['license'] = 0
            image['file_name'] = imagesData['file_name']
            image['coco_url'] = "NULL"
            image['height'] = imagesData['height']
            image['width'] = imagesData['width']
            #image['date_captured'] = imagesData['date_created']
            image['flickr_url'] = "NULL"
            #image['id'] = imagesData['id']
            image['id'] = int(cheak_abs_name(imagesData['file_name'].split('_')))
            self.cocoFormat['images'].append(image)
        
        annotation = dict()
        for annotations in data['annotations']:
            #if annotations['category_id'] != 1 or len(annotations['keypoints']) == 0:
            if len(annotations['keypoints']) == 0:
                continue
            #annotation['segmentation'] = 0
            annotation['num_keypoints'] = self.count_keypoint(annotations['keypoints'])
            annotation['area'] = self.calc_area(annotations['bbox'])
            annotation['iscrowd'] = 0
            for i in range(17):
                vible = annotations['keypoints'][i*3+2]
                if vible == 0:
                    continue
                annotations['keypoints'][i*3+2] = vible -1 
            annotation['keypoints'] = annotations['keypoints']
            #annotation['image_id'] = annotations['image_id']
            annotation['image_id'] = int(cheak_abs_name(imagesData['file_name'].split('_')))
            annotation['bbox'] = annotations['bbox']
            annotation['category_id'] = annotations['category_id']
            annotation['id'] = self.id_cnt
            self.cocoFormat['annotations'].append(annotation)
            self.id_cnt = self.id_cnt + 1

        if self.categorieFlag:
            categorie = dict()
            categorie['supercategory'] = data['Categories'][0]['supercategory']
            categorie['id'] = data['Categories'][0]['id']
            categorie['name'] = data['Categories'][0]['name']
            categorie['keypoints'] = data['Categories'][0]['keypoints']
            categorie['skeleton'] = data['Categories'][0]['skeleton']
            self.cocoFormat['categories'].append(categorie)
            self.categorieFlag = 0

    def push_json(self, jsonFile):
        with open(jsonFile, 'rt', encoding='UTF-8-sig') as file:
            datas = json.load(file)
            annos = datas['annotations']
            for anno in annos:
                className = anno['category_id']
                if className > 150:
                    continue
                self.annoClass[className] = self.annoClass[className] + 1
                


    def compare_jpg_json(self):
        pass
   
    def calc_class(self, len):
        allSum = sum(self.annoClass.values())

        print("all\t\t", allSum)
        for i in range(150):
            #print("id", i+1, self.annoClass[i+1]/allSum * 100)
            self.ratioClass[i+1] = self.annoClass[i+1]/allSum * 100
            

    def save_json(self, abspath):
        filePath = abspath + "/" + "person_keypoints_val2017.json"
        #filePath = "/home/ubuntu/koreaData/kapao_custom/data/datasets/test/annotations" + "/" + "person_keypoints_val2017.json"
        with open(filePath, 'w') as outfile:
            json.dump(self.cocoFormat, outfile)

    def save_csv(self, abspath):
        filePath = abspath + "/../../" + abspath[-6:] + "_statistics.csv"
        with open(filePath, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(self.ratioClass.values())


    def creat_id(self):
        for i in range(150):
            self.annoClass[i+1] = 0
            

def get_json():
    pass

def find_jsonSet(path):
    jsonList=[]
    
    for dirpath, dirname, filename in os.walk(path, topdown=False):
        if dirpath[-5:] != "split":
            continue
        aliveSet = ['json']
        jsonList.extend([dirpath+'/'+i for i in filename if i[-4:] in aliveSet])

    return jsonList



if __name__ == '__main__':
    #print("### Change NIA Format to COCO Format")
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='datasetDir', default='/mnt/c/Users/Eric/Documents/src/koreaData/bbox_split/data/220818', help='path to directory')

    args = parser.parse_args()

    basename = os.path.basename(args.datasetDir)
    abspath = os.path.abspath(args.datasetDir)
    
    
    info = dict()
    info["description"] = "NIA korea Dataset"
    info["url"] = "https://aihub.or.kr/"
    info["version"] = "1.0"
    info["year"] =  2022
    info["contributor"] = "COCO Consortium"
    info["date_created"] = "2022/09/01"


    jsonList = find_jsonSet(abspath)
    
    coco_keypoint = custom_dataset(info,'licenses')
    coco_keypoint.creat_id()
    
    for file in jsonList:
        coco_keypoint.push_json(file)
        
    coco_keypoint.calc_class(len(jsonList))
    coco_keypoint.save_csv(abspath)


    
    print("### complete")
    