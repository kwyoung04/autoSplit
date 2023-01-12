from email.errors import StartBoundaryNotFoundDefect
import json
import argparse
import os 

import sys

#STUFF_LIST = {151, 152, 153, 154, 156, 157, 158, 159, 160, 155, 161}
#STUFF_LIST = {162, 161, 160, 158, 157, 156, 155, 154, 153, 152, 151}
STUFF_LIST = {152, 153, 154, 155, 156, 157, 145, 158, 98, 99, 100}


def run(jsonPath, splitSavePath):
    with open(jsonPath, 'rt', encoding='UTF-8-sig') as data:
        coco = json.load(data)
        annotations = coco['annotations']
        lenAn = len(annotations)
        i = 0
        
        while (i < lenAn):
            try:
            #del(annotations[i]['sZegmentation'])
                annotations[i]['segmentation'] = []
            except KeyError:
                pass
            if annotations[i]['category_id'] in STUFF_LIST:
                del(annotations[i])
                lenAn = lenAn -1
                i = i-1

            i = i+1     


        coco['annotations'] = annotations
        del(coco['categories'][158-1])
        del(coco['categories'][157-1])
        del(coco['categories'][156-1])
        del(coco['categories'][155-1])
        del(coco['categories'][154-1])
        del(coco['categories'][153-1])
        del(coco['categories'][152-1])
        del(coco['categories'][145-1])
        del(coco['categories'][100-1])
        del(coco['categories'][99-1])
        del(coco['categories'][98-1])


    save_coco(splitSavePath, coco)

def save_coco(file, data):
    with open(file, 'wt', encoding='UTF-8') as coco:
        json.dump(data, coco, indent=2, sort_keys=False, ensure_ascii = False)


if __name__ == "__main__":
    argument = sys.argv[1]
    
    basename = os.path.basename(argument)
    abspath = os.path.abspath(argument)
    print(argument)

    if basename != "instances_default.json":
        exit()
    
    splitSavePath = argument[:-5] + "_bbox.json"

    run(argument,splitSavePath)

