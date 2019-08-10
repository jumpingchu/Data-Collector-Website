from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 設定資料庫位置，讓 Flask 和 SQLAlchemy 連接
# app.config['SQLALCHEMY_DATABASE_URI']=資料庫系統://使用者名稱: 密碼  @本地      /資料庫名
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:密碼@localhost/data_collector'

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
        return render_template("success.html")

# 404 error
# 因為在 index.html 中 submit 的 action 指向是一個檔案(success.html)
# 所以要改成 jinja2 的 {{url_for}} 才抓的到

# 405 Method Not Allowed
# 要在 @app.route() 中加入methods 

if __name__ == "__main__":
    app.run(debug=True)
