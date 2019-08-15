from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)

# 設定資料庫位置，讓 Flask 和 SQLAlchemy 連接
# app.config['SQLALCHEMY_DATABASE_URI']=資料庫系統://使用者名稱: 密碼  @本地      /資料庫名
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:password@localhost/data_collector'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mfiujoyihkbyrm:6c7e8fdd0020a47329c8699e83e379ec6921a3882c00e9c060d20ed5f30eee50@ec2-184-72-237-95.compute-1.amazonaws.com:5432/d9orup86i20k62?sslmode=require'
# 將 app 建立為 SQLAlchemy 物件
db = SQLAlchemy(app)

# 建立資料庫
class Data(db.Model):
    # 設定 table 名
    __tablename__ = 'data'  
    
    # 設定 Columns 資料
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True)
    height_ = db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_
        

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form['email_name']
        height = request.form['height_name']
        # 確認 E-mail 不在資料庫內 => query email 的數量應該要是 0
        if db.session.query(Data).filter(Data.email_==email).count() == 0:  
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()
            # sqlalchemy.sql.func.avg(Data.height_): 平均值的SQL語法
            # scalar(): 取得SQL語法所跑出的資料
            average_height = db.session.query(func.avg(Data.height_)).scalar()
            average_height = round(average_height, 1)
            count = db.session.query(Data).count()
            send_email(email, height, average_height, count)
            return render_template("success.html")
        
        else:
            return render_template("Index.html", text="The email has been used!")

# 404 error
# 因為在 index.html 中 submit 的 action 指向是一個檔案(success.html)
# 所以要改成 jinja2 的 {{url_for}} 才抓的到

# 405 Method Not Allowed
# 要在 @app.route() 中加入methods 

if __name__ == "__main__":
    app.run(debug=True)
