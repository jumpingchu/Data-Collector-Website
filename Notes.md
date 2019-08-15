# **Notes**

## 在 heroku 創建 postgreSQL 資料庫

    $ heroku addons:create heroku-postgresql hobby-dev -a database_name

## 查看資料庫連結 URI

    $ heroku config

## Run python or bash

    $ heroku run python
    $ heroku run bash

## 點 Submit 後出現 Internal Server Error

### 確認沒有輸入重複 E-mail

* 只有建立本機的資料庫，heroku database 尚未建立

* 方法:

        $ heroku run python
        >> from app import db
        >> db.create_all()

* 確認 heroku database 資料:

        $ heroku pg:psql --app database_name
        
        database_name::DATABASE=> select * from data;

        id |        email_        | height_
        ---+----------------------+---------
        1  |     text@mail.com    |   183
        (1 row)

### 有重複，卻無法跳出"The email has been used!"

* 檢查 heroku logs

        jinja2.exceptions.TemplateNotFound: Index.html

* html 檔案名為小寫 i 的 index，而不是 Index.html
所以TemplateNotFound
* 但這問題在本機執行時卻沒事

## Heroku: Cannot run more than 1 Free size dynos

* in console run:

        heroku ps

* the result is some like this:

        run.4859 (Free): up 2016/01/12 21:28:41 (~ 7m ago): rails c

* So the numbers 4859 represent the session that is open and needs to be closed. To fix the error you need to run(Obviusly, replace the number 4859 by the number obtained):

        heroku ps:stop run.4859
