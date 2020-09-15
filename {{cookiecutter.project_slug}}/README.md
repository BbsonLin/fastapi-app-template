## 環境安裝(Setup) & 進入環境

```
$ poetry install
$ poetry shell
```


## 本地運行(Run)

```
$ uvicorn app.main:app --port 5050 --host 0.0.0.0 --reload
```

> API URL: http://localhost:5050/
> Swagger doc: http://localhost:5050/docs
> Redoc doc: http://localhost:5050/redoc
