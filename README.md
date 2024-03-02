<div align="center">

![Static Badge](https://img.shields.io/badge/python_3.10-%233776AB?logo=python&labelColor=grey)
![Static Badge](https://img.shields.io/badge/fastapi_0.108.0-%23009688?logo=fastapi&labelColor=grey)
![Static Badge](https://img.shields.io/badge/SQLAlchemy_2.0.25-%23D71F00?logo=sqlalchemy&labelColor=grey)

---
</div>  

## Запуск:
- <code>uvicorn main:app --reload</code> запуск сервера через терминал
- <code>celery -A src.background_tasks.send_email:celery worker --loglevel=INFO --pool=solo</code> запуск celery (перезагружать после изменения кода)
- <code>celery -A core.config:celery flower</code> запуск веб интерфейса
- <code>http://127.0.0.1:8000/docs</code> документация fastapi
- <code>http://localhost:5555</code> интерфейс графический celery
---

## Структура проекта:

### Backend

```
Back/
    ├── core/                       #
    ├── migrations/                 #
    ├── src/                        #
        ├── app/                    #
            └──  authentication/    #
                ├── models/         #
                ├── operations/     #
                ├── shemas/         #
                    ...
        ├── background_tasks/       #
        ├── help_func/              #
        ├── router/                 #
        ├── config.py               # получение паролей с .env
        ├── database.py             # создание движка/получение сессии
        └── main.py                 # подключение роутеров/css/запуск regis
    ├── alembic.ini                 #
    └── requirements.txt            # файл  с зависимостями
```

---

### Frontend

 ```
Front/                 #
    ├── audio/          #
    ├── html/           #
        ├── admin/      #
        ├── base.html   # базовый шаблон                                         
        ...
    ├── img/            #
    ├── js/             #
    └── styles          #
        ├── css/        #
        └── sass/       #
```