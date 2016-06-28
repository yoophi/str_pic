# DummyImage

dummy image 를 만들 수 있는 서비스입니다.

## 실행방법

### 설치

    pip install https://github.com/yoophi/flask_dummyimage.git
    python setup.py install 

### 실행 

    python flask_dummyimage:app    
    
또는 

    gunicorn flask_dummyimage:app 


## 사용방법 

- <http://localhost:5000/dummyimage> 가로 세로 200px 사이즈의 정방형 png 이미지가 생성됩니다. 
- <http://localhost:5000/dummyimage/200.png> 가로 세로 200px 사이즈의 정방형 png 이미지가 생성됩니다. 
- <http://localhost:5000/dummyimage/640x480.jpg> 가로 640, 세로 480 사이즈의 jpg 이미지가 생성됩니다.

### QueryString

- `text`: 이미지에 표시할 글씨 
- `color`: 글씨 색상
- `bgcolor`: 배경 색상
- `zoom`: 이미지에 글씨를 가득 차게 표시할지 여부 (True/False)
- `font-size`: 글꼴 크기 (`zoom` 기능 사용시 무시됨)

## Flask 프로젝트에서 사용하기

```
app = Flask(__name__)
dummy_image = DummyImage()
dummy_image.init_app(app)
```

또는 

```
app = Flask(__name__)
dummy_image = DummyImage(app)
```