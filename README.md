<div align="center">
<img src= "Front\img\home.png" alt="превью" width="550">

___
![Static Badge](https://img.shields.io/badge/python_3.10-%233776AB?logo=python&labelColor=grey)
![Static Badge](https://img.shields.io/badge/fastapi_0.108.0-%23009688?logo=fastapi&labelColor=grey)
![Static Badge](https://img.shields.io/badge/SQLAlchemy_2.0.25-%23D71F00?logo=sqlalchemy&labelColor=grey)
---
</div>  

## Структура проекта:

### Backend

```
Back/
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