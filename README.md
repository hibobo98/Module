# Module
modularization, fastapi, yolo, image captioning


- 실행코드
  ```
  # Terminal
  uvicorn mainapp:app
  ```

- 다운받은 html 적용 방법
  - html 출처 : https://www.free-css.com/free-css-templates
  - 1) static 폴더 만들어서 css, js, font 등 넣기
  - 2) index.html의 마지막 부분에 'js/bootstrap.js' --> 'static/js/bootstrap.js' 이런 식으로 경로 다 바꿔주기
  - 3) mainapp.py에 static폴더와 index.html이 있는 경로를 설정해서 fastapi가 인식하도록하기
    ```
    # mainapp.py 내부 예시
    ...
    templates = Jinja2Templates(directory="./") # index.html이 있는 경로
    app.mount('/static', StaticFiles(directory='static'), name="static") # font, css 등이 있는 폴더명=static
    ...

    ```



- 
