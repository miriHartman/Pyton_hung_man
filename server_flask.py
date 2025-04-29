import random
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from user import User
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)

# הרשמה
set_user = []
file1 = open('users.json').read()
h = json.loads(file1)


# @cross_origin(app, supports_credentials=True)
# @app.route('/register', methods=['POST'])
# דקורטור לבדיקה האם המשתמש מחובר (העוגיה תקפה)
def decorator1(func):
    def wrapper(*args, **kwargs):
        user_pass = request.cookies.get('user_pass')
        if user_pass:
            return func(*args, **kwargs)
        return 'cookie not found:('

    wrapper.__name__ = func.__name__
    return wrapper

# הרשמה
@cross_origin(app, supports_credentials=True)
@app.route('/register', methods=['POST'])
def register():
    user_to_add = str(request.json)
    place = user_to_add.find(',')
    u_name = user_to_add[2:(place - 1)]
    u_pass = user_to_add[(place + 3):len(user_to_add) - 2]
    for i in set_user:
        if i.user_pass == u_pass and i.user_name == u_name:
            return jsonify('you are already connected...')
    f1 = open('users.json')
    file_text = f1.read()
    f1.close()
    file_text = file_text[0:len(file_text) - 1]

    user1 = User(u_name, u_pass)
    set_user.append(user1)
    jsus = str(user1)
    with open('users.json', 'w') as file2:
        file2.write(f'{file_text},"{u_pass}":{jsus}' + "}")
    file2.close()

    return jsonify(f' hello {u_name}!!')
    # else:
    # return jsonify('cant add this object as a user!!')


# enter
@cross_origin(app, supports_credentials=True)
@app.route('/enter', methods=['POST'])
def enter():
    user_to_connect = str(request.json)
    place = user_to_connect.find(',')
    u_name = user_to_connect[2:(place - 1)]
    u_pass = user_to_connect[(place + 3):len(user_to_connect) - 2]
    for i in set_user:
        if i.user_pass == u_pass and i.user_name == u_name:
            return jsonify(
                f'your name: {i.user_name}, your password: {i.user_pass},till now you played : {i.num_play} times , you use this sentences: {len(i.set_words)}, you won till now  {i.num_win} times')


# all users
@cross_origin(app, supports_credentials=True)
@app.route('/all_users', methods=['GET'])
def all_users():
    return h

# שליפת מילה רנדומלית מקובץ המילים
@decorator1
@cross_origin(app, supports_credentials=True)
@app.route('/mix', methods=['POST'])
def mix():
    num = request.json
    word_file = open('./words.txt', 'r')
    words = list(map(lambda x: x.strip(), word_file.readlines()))
    random.shuffle(words)
    place = num % len(words)
    word_file.close()

    return words[place]

# יצירת עוגיה
@cross_origin(app, supports_credentials=True)
@app.route('/set_cookie', methods=["POST"])
def set_cookie():
    user_to_connect = str(request.json)
    response = make_response("Cookie set!")
    response.set_cookie('user_pass', user_to_connect, max_age=20, httponly=True, secure=False)
    return response

# בקשה לקבלת העוגיה אם קיימת
@cross_origin(app, supports_credentials=True)
@app.route('/get_cookie', methods=['GET'])
def get_cookie():
    user_pass = request.cookies.get('user_pass')
    print(f"Get: {user_pass}")
    if user_pass:
        return user_pass
    return 'cookie not found:(  '

#  שליפת המשתמש הנוכחי אם כבר נרשם פעם
@decorator1
@cross_origin(app, supports_credentials=True)
@app.route('/get_my_user_name', methods=["POST"])
def get_my_user_name():
    us_pass = str(request.json)
    for i in set_user:
        if i.user_pass == us_pass:
            return jsonify(i.user_name)

# שליפת ההיסטוריה של המשתמש
@decorator1
@cross_origin(app, supports_credentials=True)
@app.route('/history', methods=["POST"])
def history():
    us_pass = request.json
    for i in set_user:
        if i.user_pass == us_pass:
            return jsonify(
                f'hello {i.user_name}.you win {i.num_win} times .you played {i.num_play} times .you used this words{str(i.set_words)}')

# עדכון המשחק בהיסטורית המשתמש
@decorator1
@cross_origin(app, supports_credentials=True)
@app.route('/update_my_play', methods=["POST"])
def update_my_play():
    pro = str(request.json)
    us_pass = pro[2:pro.find(',') - 1]
    word = pro[pro.find(',') + 1:len(pro) - 1]
    for i in set_user:
        if i.user_pass == us_pass:
            i.num_play = i.num_play + 1
            uu = i.set_words.add(word)
            return jsonify('update is ok')

# רק במקרה של ניצחון עדכון
@decorator1
@cross_origin(app, supports_credentials=True)
@app.route('/update_my_win', methods=["POST"])
def update_my_win():
    us_pass = str(request.json)
    for i in set_user:
        if i.user_pass == us_pass:
            i.num_win = i.num_win + 1
            return jsonify("update success[win]")

# פונקציה שמנהלת  את המשחק - מאופשרת רק במקרה שמחובר
@decorator1
@cross_origin(app, supports_credentials=True)
@app.route('/history', methods=["GET"])
def start_play():
    return jsonify('you can play...')


if __name__ == "__main__":
    # u = User("ooo", '88')
    # set_user.append(u)
    app.run(debug=True)
