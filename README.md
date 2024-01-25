## Структура проекта:

### Backend

```
Back/
    ├── migrations/                                     #
    ├── src/                                            #
        ├── app/                                        #
           ├── admin_operations/                        #
                ├── operations.py                       # операции, которые админ может совершать над пользователем  
                └── schemas.py                          # схема ответа сервера для создании пагинации пользователей
           ├── authentication/                          #
                ├── cookie.py                           # настройка стратегии/куки 
                ├── fastapi_users_custom.py             #
                ├── login.py                            # роутер с входом 
                ├── logout.py                           # роутер с выходом
                ├── models.py                           # модель пользователя
                ├── register.py                         # роутер с регистрацией
                ├── schemas.py                          # pydantic схема пользователя
                └── user_manager.py                     #
           └── background_tasks/                        #
                ├── send_email.py                       # генирация шаблона и отправка его на почту 
                └── create_user_after_confirm_email.py  # проверка токена и создание пользователя после подтверждения почты
        ├── router/                                     #
            ├── router_user.py                          # роутеры, которе относятся к пользователю 
            └── router_admin.py                         # роутеры, которе относятся к админу
        ├── config.py                                   # получение паролей с .env
        ├── database.py                                 # создание движка/получение сессии
        └── main.py                                     # подключение роутеров/css/запуск regis
    ├── alembic.ini                                     #
    └── requirements.txt                                # файл  с зависимостями
```

---

### Frontend

 ```
Front/                                      
     ├── sass/                              #
         └── css/                           #
              ├── admin/                    #
                   └── admin.css            #
              └── authentication/           #
                   ├── login.css            #
                   └── register.css         #
     ├── html/                              #
          ├── admin/                        #
               ├── admin_panel.html         #
               └── user_info_table.html     #
          ├── authentication/               #
               ├── login.html               # страница с входом
               ├── register.html            # страница с регистраией
               └── verified.html            #
          ├── error.html                    # страница с ошибкой
          └── base.html                     # базовый шаблон
     ├── img/                               #
          ├── focalor/                      #
          ├── logo/                         #
          └── slider/                       #
     └── js/                                #
          ├── admin.js                      #
          ├── login.js                      #
          ├── main.js                       #
          └── register.js                   #
```