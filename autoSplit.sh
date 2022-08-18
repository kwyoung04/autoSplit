#! /bin/bash
echo "Automatic annotation data split"


for file in `find . -name '*.zip'`;
do
  data=`find -wholename ${file}*`;
  echo "${data}";

  if [ $data -z ];then
    continue
  fi

  #echo " unzip "${data}" -d "${data:0:-4}" ";
  unzip "${data}" -d "${data:0:-4}";
done

find . -name 'instances_default.json' -exec python3 coco_class_add.py {} \;
find . -name '0st.json' -exec python3 coco_split.py {} \;



echo "Operation complete"
