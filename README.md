# 한국형 데이터 변환

# 코드 작동

1. 코드 설치

```bash
git clone https://github.com/kwyoung04/autoSplit.git
```

1. 데이터 자동 분리(auto split)

```bash
source autoSplit.sh
```

1. 4-2 에서 bbox 변환

```bash
find . -name 'instances_default.json' -exec python3 cocoToBbox.py {} \;
```

# 데이터 위치

data 폴더를 만들고 안에 데이터를 폴더 단위로 두고 작동