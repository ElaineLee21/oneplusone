from pymongo import MongoClient
from flask import Flask,render_template,request,redirect,url_for,jsonify
from datetime import datetime, timedelta
import jwt
import hashlib


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = "ONEPLUSONE"

client = MongoClient('mongodb://54.180.135.167', 27017, username="test", password="test")
db = client.oneplusone

@app.route("/")
def home():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template("index.html")
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login"), msg="로그인 시간이 만료되었습니다.")
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"), msg="로그인 정보가 존재하지 않습니다.")

@app.route("/sign_in")
def login():
    return render_template("login.html")

@app.route("/beverages", methods=["GET"])
def get_beverages() :
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        posts = list(db.product.find({}).sort("like", -1))

        for post in posts :
            post["_id"] = str([post["_id"]])
            post["count_like"] = db.likes.count_documents({"post_id": post["_id"], "type":"like"})
            post["like_by_me"] = bool(db.likes.find_one({"post_id": post["id"], "type":"like", "username":payload["id"]}))
        return jsonify({"result": "success", "msg":"포스팅 완료", "posts":posts})

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError) :
        return redirect(url_for("home"))

@app.route("/likes", methods=["POST"])
def update_like():
    token_receive = request.cookies.get("mytoken")

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        user_info = db.users.find_one({"username": payload["id"]})
        post_id_receive = request.form["post_id_give"]
        type_receive = request.form["type_give"]
        action_receive =request.form["action_give"]

        doc = {
            "post_id": post_id_receive,
            "username": user_info["username"],
            "type": type_receive
        }

        if action_receive == "like":
            db.likes.insert_one(doc)
        else:
            db.likes.delete_one(doc)
        count = db.likes.count_documents({"post_id":post_id_receive,"type":type_receive})
        return jsonify({"result":"success","msg":"업데이트", "count":count})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/signup", methods=["POST"])
def sign_up():
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    password_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()

    doc = {
        "username": username_receive,
        "password" : password_hash,
        "profile_name": username_receive,
        "profile_pic": "",
        "profile_pic_real": "profile_pics/profile_placeholder.png",
        "profile_info": ""
    }
    db.users.insert_one(doc)
    return jsonify({"result":"success"})

@app.route("/login", methods=["POST"])
def sign_in() :
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]

    password_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    result = db.users.find_one({"username": username_receive, "password": password_hash})

    if result is not None :
        payload = {
            "id" : username_receive,
            "exp" : datetime.utcnow() + timedelta(seconds= 60 * 60 * 24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256").decode("utf-8")

        return jsonify({
            "result": "success",
            "token" : token
        })
    else :
        return  jsonify({
            "result": "fail",
            "msg": "아이디와 비밀번호가 일치하지 않습니다."
        })

if __name__ == "__main__" :
    app.run("0.0.0.0", port=5000, debug=True)

