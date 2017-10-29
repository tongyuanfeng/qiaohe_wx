from flask import Flask, request, jsonify, make_response
import hashlib
import os
import pymysql

from OpenSSL import SSL

from flask import render_template
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tongyf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


@app.route('/')
def index():
    # url_for('static', filename='style.css')
    # return app.send_static_file('index.html')
    # return render_template('playbook.html')
    return render_template('index.html')
    # return url_for('static', filename='style.css')


@app.route('/.well-known/pki-validation/fileauth.txt')
def fileauth():
    # url_for('static', filename='style.css')
    # return app.send_static_file('index.html')
    # return render_template('playbook.html')
    # return render_template('index.html')
    return url_for('static', filename='.well-known/pki-validation/fileauth.txt')


@app.route('/skillExchange/user_num')
def user_num():
    # from ssdb import SSDB
    import pyssdb
    c = pyssdb.Client()
    # ssdb = SSDB('127.0.0.1', 8888)
    ret = c.hsize('skillExchange')  # ssdb.hsize('skillExchange')
    return str(ret)


@app.route('/skillExchange/register', methods=['POST', 'GET'])
def register():
    error = None
    if request.method == 'POST':
        gdata = request.get_json(force=True)
        payload = eval(gdata.get('payload', {}))

        uname = payload.get('username')
        data = str(payload)
        import pyssdb
        c = pyssdb.Client()
        ret = c.hset('skillExchange', uname, data)

        if ret:
            return str(ret)
        else:
            error = 'Invalid username/password'

    return render_template('hello.html', error=error)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=60):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):

        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(60)
    return jsonify({'token': token.decode('ascii'), 'duration': 60})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@app.route('/wx', methods=['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        print('coming Get')
        data = request.args
        token = 'helloqiaohe'
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s).encode("utf-8")
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)


@app.route('/wx/getuserinfo', methods=['GET', 'POST'])
def get_wx_userinfo():
    if request.method == 'POST':
        gdata = request.get_json(force=True)
        print(gdata)

        payload = gdata.get('payload', "{}")

        nickname = payload.get('nickname')
        db = pymysql.connect(host="qiaohequan.com", user="root", passwd="qiaohejiayou", db="qiaohe", port=3306,
                             charset='utf8')
        print(get_user_info(db, nickname))

        payload['weixin_id'] = ''
        payload['name'] = ''
        payload['cellphone'] = ''
        payload['level'] = ''


        for line in get_user_info(db, nickname):
            print(line)
            payload['weixin_id'] = line[1]
            payload['name'] = line[2]
            payload['cellphone'] = line[3]
            payload['level'] = line[4]

        db.close()
        return jsonify(payload)



@app.route('/wx/baoming', methods=['GET', 'POST'])
def baoming():
    if request.method == 'POST':
        gdata = request.get_json(force=True)
        print(gdata)

        payload = gdata.get('payload', "{}")
        nickname = payload.get('nickname')
        name = payload.get('name')
        cellphone = payload.get('cellphone')
        level = payload.get('level')
        weixin_id = payload.get('weixin_id')
        time = payload.get('time')
        db = pymysql.connect(host="qiaohequan.com", user="root", passwd="qiaohejiayou", db="qiaohe", port=3306,
                             charset='utf8')
        baoming_sql(db, nickname, name, cellphone, weixin_id,time)
        db.close()
        return 'success'



@app.route('/wx/update_userinfo', methods=['GET', 'POST'])
def update_userinfo():
    if request.method == 'POST':
        gdata = request.get_json(force=True)
        print(gdata)

        payload = gdata.get('payload', "{}")
        nickname = payload.get('nickname')
        name = payload.get('name')
        cellphone = payload.get('cellphone')
        level = payload.get('level')
        weixin_id = payload.get('weixin_id')
        db = pymysql.connect(host="qiaohequan.com", user="root", passwd="qiaohejiayou", db="qiaohe", port=3306,
                             charset='utf8')
        update_or_insert_userinfo(db, nickname, name, cellphone, weixin_id)
        db.close()
        return 'success'



@app.route('/wx/get_user_level_list',methods=['GET','POST'])
def get_user_level_list():
    if request.method == 'POST':
        gdata = request.get_json(force=True)
        print(gdata)
        payload = {'p_count':0,'level':'F','items':[]}
        nickname = gdata.get('nickname', "")
        db = pymysql.connect(host="qiaohequan.com", user="root", passwd="qiaohejiayou", db="qiaohe", port=3306,
                             charset='utf8')
        cursor = db.cursor()
        cmd = "select level from qiaohe.user where nickname='%s'" % nickname
        cursor.execute(cmd)
        res = cursor.fetchone()
        level = 'F'
        if res:
            payload['level'] = res[0]
            level = res[0]

        cmd = "SELECT count(nickname) FROM qiaohe.user  WHERE level<'%s'" % level

        cursor.execute(cmd)
        res = cursor.fetchone()
        if res:
            payload['p_count'] = res[0]

        cmd = "SELECT nickname,LEVEL FROM qiaohe.user  WHERE LEVEL <'F' ORDER BY LEVEL   LIMIT 10 "
        cursor.execute(cmd)
        res = cursor.fetchall()
        for line in res:
            payload['items'].append({'nickname':line[0],'level':line[1] })


        return jsonify(payload)


def baoming_sql(db, nickname, name, cellphone, weixin_id,time):


    if len(get_user_info(db, nickname)) == 0 :
        "insert"
        cmd = "INSERT INTO qiaohe.baoming (nickname, name, cellphone, weixin_id,level,time) VALUES( '%s', '%s', '%s','%s','%s', '%s') " % (
        nickname, name, cellphone, weixin_id, 'F',time)
    else:
        "update"
        cmd = "UPDATE  qiaohe.baoming SET nickname = '%s', name = '%s', cellphone = '%s' ,weixin_id='%s'  time='%s' WHERE   nickname = '%s' " % (
        nickname, name, cellphone,  weixin_id ,time, nickname)

    cursor = db.cursor()
    print(cmd)
    cursor.execute(cmd)
    db.commit()


def update_or_insert_userinfo(db, nickname, name, cellphone, weixin_id):


    if len(get_user_info(db, nickname)) == 0 :
        "insert"
        cmd = "INSERT INTO qiaohe.user (nickname, name, cellphone, weixin_id,level) VALUES( '%s', '%s', '%s','%s', '%s') " % (
        nickname, name, cellphone, weixin_id, 'F')
    else:
        "update"
        cmd = "UPDATE  qiaohe.user SET nickname = '%s', name = '%s', cellphone = '%s' ,weixin_id='%s'  WHERE   nickname = '%s' " % (
        nickname, name, cellphone,  weixin_id ,nickname)

    cursor = db.cursor()
    print(cmd)
    cursor.execute(cmd)
    db.commit()


def get_user_info(db, nickname):
    sql_cmd = "SELECT nickname ,weixin_id, name , cellphone,level FROM qiaohe.user WHERE nickname='%s'" % nickname
    cursor = db.cursor()
    cursor.execute(sql_cmd)
    res = cursor.fetchall()
    if res:
        return res
    else:
        return []


def insert_sql(db, sql_cmd, args):
    cursor = db.cursor()
    print(sql_cmd)
    cursor.execute(sql_cmd, args)
    db.commit()



# import numpy as np
# import cv2
# def gen(filename):
#     cap = cv2.VideoCapture(filename)
#     cap.isOpened()
#     while True:
#         ret, frame = cap.read()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#     cap.release()
#     cv2.destroyAllWindows()
#
#
#
# from flask import send_from_directory,Response
# @app.route('/v/<filename>')
# def get_file(filename):
#     return Response(gen(filename),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

from flask import send_from_directory
@app.route('/v/<filename>')
def get_file(filename):
    return send_from_directory('video',filename)


if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()

    my_db = pymysql.connect(host="qiaohequan.com", user="root", passwd="qiaohejiayou", db="qiaohe", port=3306,
                            charset='utf8')

    # context = ('server.crt','server.key')
    # app.run(host='0.0.0.0', debug=False,port=443,ssl_context=context)
    context = ('214197211740425.pem', '214197211740425.key')
    app.run(host='0.0.0.0', debug=False, port=443, ssl_context=context)


    # app.run(host='0.0.0.0', debug=False,port=80)
