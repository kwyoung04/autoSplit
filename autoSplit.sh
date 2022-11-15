#! /bin/bash
echo "Automatic annotation data split"


for file in `find . -name '*.zip'`;
do
  data=`find -wholename ${file}*`;
  echo "data: ${data}";

  if [ $data -z ];then
    continue
  fi

  #echo " unzip "${data}" -d "${data:0:-4}" ";
  unzip "${data}" -d "${data:0:-4}";
done

find . -name 'instances_default.json' -exec python3 coco_class_add.py {} \;
find . -name '0st.json' -exec python3 coco_split.py {} \;

#find . -maxdepth 2 -mindepth 2 -name '22*' -exec python3 lidarAnnoCnt.py -d {} \;

find -wholename '*/split/*.json' | wc -l
find -name '*jpg' | wc -l

echo "Operation complete"
