import json
import argparse
import funcy
from sklearn.model_selection import train_test_split
import os 
import xlrd
import pandas as pd

import sys

exel_path='./class_list4_2.xlsx'
del_cat = ["pillar", "background_in", "sky", "tree", "background_out", "pavement"]
del_id = [154, 155, 158, 159, 161]

def run(annotations_path, split_save_folder):
    i=0
    #annotations_path='/mnt/c/Users/Eric/Documents/src/koreaData/test_data/task_068_02_002_bbox-2022_08_12_15_21_02-cvat for images 1.1/annotations/instances_default.json'.format(i)
    #split_save_folder='/mnt/c/Users/Eric/Documents/src/koreaData/test_data/task_068_02_002_bbox-2022_08_12_15_21_02-cvat for images 1.1'
    #'coco_split'

    df_sheet_all = pd.read_excel(exel_path,
        sheet_name=None,
        # sheet_name=[0, 'sheet2'],
        engine='openpyxl')
    # print(df_sheet_all)
    change_data=df_sheet_all['Sheet1']
    # print(df_sheet_all)
    # print(df_sheet_all['Sheet1'])
    super_class=change_data['super']
    main_class=change_data['main']
    lsit_main_class=main_class.tolist()
    lsit_super_class=super_class.tolist()
    #print(lsit_main_class)

    def binary_search_recursion(target, start, end, data):
        if start > end:
            return None

        mid = (start + end) // 2

        if data[mid][0] == target:
            return mid
        elif data[mid][0] > target:
            end = mid - 1
        else:
            start = mid + 1        

        return binary_search_recursion(target, start, end, data)


    def class_add_save_coco(file, info, images, annotations, categories):
        with open(file, 'wt', encoding='UTF-8-sig') as coco:
            # json.dump({ 'info': info, 'licenses': licenses, 'images': images, 
            #     'annotations': annotations, 'categories': categories}, coco, indent=2, sort_keys=True)

            
            json.dump({'info': info, 'categories': categories, 'images': images, 'annotations': annotations}, coco, indent=2, sort_keys=False, ensure_ascii = False)


    def filter_annotations(annotations, images):
        image_ids = funcy.lmap(lambda i: int(i['id']), images)
        return funcy.lfilter(lambda a: int(a['image_id']) in image_ids, annotations)

    def category_add(label,id):
        category = {}
        category['supercategory'] = label
        category['id'] = int(id+1)
        category['name'] = label

        return category
        
    with open(annotations_path, 'rt', encoding='UTF-8-sig') as annotations:
        #print("annotations", annotations)
        coco = json.load(annotations)
        # info = coco['info']
        info=[{'description': coco['info']['description'], 'version': "1.0", 'year': "2022"}]
        # licenses = coco['licenses']
        images = coco['images']
        annotations = coco['annotations']
        # print(annotations)
        categories = coco['categories']

        number_of_images = len(images)

        images_with_annotations = funcy.lmap(lambda a: int(a['image_id']), annotations)

        names=[]
        supercategory=[]
        for category in categories:
            supercategory.append(category['supercategory'])
            category_id=category['id']
            names.append(category['name'])
            #category_id=category['id']

        set1=set(lsit_main_class)
        set2=set(names)
        #print(names)
        #print(len(lsit_main_class),len(names))
        add_classes=set1.difference(set2)
        #print(" add_classes : ", add_classes)
        #print(len(add_classes))

        #for add_class in add_classes:
            # print(add_class)
            #categories.append(category_add(add_class,category_id))
            #category_id=category_id+1

        matching_id=[]
        for category in categories:
            old_id=category['id']
            name=category['name']
            
            name_index=lsit_main_class.index(str(name))
            category['supercategory']=str(lsit_super_class[name_index])
            # print(name, lsit_super_class[name_index])

            category_id=lsit_main_class.index(category['name'])
            #category_id = category['id']
            
            category_name = category['name']
           
          
            #print(category['id'])

            del(category['id'])
            del(category['name'])


            if category_name == "road":
                category_id = 155
            elif category_name == "building":
                category_id = 159

            elif category_name == "background_in" or category_name == "background_out" :
                category_name = "background"
                category_id = 161
            string_stg = str(category_id+1)
            #category['id']=string_stg.zfill(3)
            
            category['id']=string_stg
            category['name']=category_name

            matching_id.append((old_id, string_stg))

        #print( matching_id )
        
        
        for anno in annotations:
            anno_area = anno['area']
            anno_bbox = anno['bbox']
            anno_segm = anno['segmentation']
            anno_id = anno['category_id']

            #if anno_id in del_id:
            #    continue                

            del(anno['area'])
            del(anno['bbox'])
            del(anno['segmentation'])

            if 'iscrowd' in anno['attributes']:
                anno['iscrowd']=int(anno['attributes']['iscrowd'])
            else:
                anno['iscrowd']=int(anno['attributes']['0'])

            if(anno['iscrowd'] != 0 and anno['iscrowd'] != 1):
                print("Iscrowd does not exist", annotations_path)

            del(anno['attributes'])
            
            anno['bbox']=anno_bbox

            if anno_segm:
                anno['segmentation']=anno_segm
    
            anno['area']=anno_area
            get_id = binary_search_recursion(anno_id-1, 0, len(matching_id), matching_id)
            anno['category_new_id'] = int(get_id)

        for image in images:
            del(image['license'])
            del(image['flickr_url'])
            del(image['coco_url'])
            del(image['date_captured'])


        # print(categories)
        # for data in images:
        #     # print(data)
        #     image_name=data['file_name'].replace('.jpg','.json')
        #     save_name=os.path.join(split_save_folder,image_name)
            # class_add_save_coco(save_name, info, licenses, data, filter_annotations(annotations, [data]), categories)

        save_name=os.path.join(split_save_folder,'{}st.json'.format(i))
        class_add_save_coco(save_name,info, images, filter_annotations(annotations, images), categories)

if __name__ == "__main__":
    argument = sys.argv[1]
    #argument = "/mnt/c/Users/Eric/Documents/src/koreaData/bbox_split/autoSplit/data/task_036_3_017(411)_polygon(완)-2022_09_02_15_55_34-coco 1.0/annotations/instances_default.json"
    
    basename = os.path.basename(argument)
    abspath = os.path.abspath(argument)
    
    if basename != "instances_default_bbox.json":
        exit()
    #test = annotations.split('/')
    
    splitSavePath = abspath.split('/')
    splitSavePath = '/'.join(splitSavePath[:-1])
    
    print(abspath)

    run(abspath,splitSavePath)
