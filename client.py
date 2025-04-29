import requests
from requests import session
import time

import Exeptions
import server_flask
from user import User

#
session = session()
basic_url = "http://127.0.0.1:5000"

logo = """ 
    _    _
   | |  | |
   | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
   |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ 
   | |  | | (_| | | | | (_| | | | | | | (_| | | | |
   |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                        __/ |
                       |___/"""


# הרשמה -הוספת משתמש
def add_user():
    name_us, password = input(print('your name: ')), input(print("my password"))
    while True:
        try:
            if not name_us.isalpha():
                raise Exeptions.NotAString()
            break
        except Exeptions.NotAString as e:
            print(e)
            name_us = input(print('error!! your name again please: '))
        except:
            name_us = input(print('error!! your name again please: '))
    user1 = (name_us, password)
    us = str(user1)
    response = session.post(f'{basic_url}/register', json=us)
    if response.status_code == 200:
        print(response.text)
    else:
        print(f'errr:{response.status_code}')


# כניסה
def enter():
    print('welcome to enter')
    name_us, password = input(print('your name: ')), input(print("my password"))
    while True:
        try:
            if not name_us.isalpha():
                raise Exeptions.NotAString()
            break
        except Exeptions.NotAString as e:
            print(e)
            name_us = input(print('error!! your name again please: '))
        except:
            name_us = input(print('error!! your name again please: '))
    use = (name_us, password)
    user1 = str(use)
    response = session.post(f'{basic_url}/enter', json=user1)
    if response.status_code == 200:
        set_cookie(password)
        pass_us = get_cookie()
        print(f'pass:  {pass_us}')
        print(f'hello to you--{get_my_user_name(pass_us)}')
        return print("you are in")
    else:
        print('you are not connected , please register before...')
        add_user()
        return False


# שליפת שם המשתמש הנוכחי
def get_my_user_name(password):
    password = str(password)
    response = session.post(f'{basic_url}/get_my_user_name', json=password)
    if response.status_code == 200:
        return response.json()

    elif response.status_code == 500:
        print('no cookie found you have to login...')
        enter()
    else:
        return response.status_code


# עדכון ההיסטוריה בעת נצחון
def update_my_win(password):
    password = str(password)
    response = session.post(f'{basic_url}/update_my_win', json=password)

    if response.status_code == 200:
        return response.text
    elif response.status_code == 500:
        print('no cookie found you have to login...')
        x = False
        while not x:
            if enter() != False:
                break
    else:
        return response.status_code


# עדכון תוצאות המשחק
def update_my_play(password, word1):
    password = str(password)
    word1 = str(word1)
    obj = (password, word1)
    response = session.post(f'{basic_url}/update_my_play', json=obj)

    if response.status_code == 200:
        return response.status_code
    elif response.status_code == 500:
        print('no cookie found you have to login...')
        enter()
    else:
        return response.status_code


# יצירת עוגיה בעת כניסה
def set_cookie(password):
    response_co = session.post(f'{basic_url}/set_cookie', json=password)
    if response_co.status_code == 200:
        print(f'cookie set!!!')
        cookies = response_co.cookies.get_dict()  # חילוץ העוגיות מהבקשה הקודמת
        print(f"Cookie: {cookies}")
        return print(response_co.text)
    else:
        print('cookie not set')


# שלייפת העוגיה אם קיימת
def get_cookie():
    response = session.get(f'{basic_url}/get_cookie')
    return response.text


# שליפת כל השתמשים - לא בשימוש - אך היא מהקובץ
def all_users():
    response = session.get(f'{basic_url}/all_users')
    if response.status_code == 200:
        return print(response.json())
    else:
        print(f"errr:{response.status_code}")


# הגרלת מילה .מילים
def mix():
    numb = input(print("Enter a number it will random for you a word or sentence: "))
    while True:
        try:
            if not numb.isdigit():
                raise Exeptions.NotANumber()
            break
        except Exeptions.NotANumber as e:
            print(e.message)
            numb = input(print("error! Enter a number again : "))
        except:
            numb = input(print(" error! Enter a number again: "))

    num = int(numb)
    response = session.post(f'{basic_url}/mix', json=num)
    if response.status_code == 200:
        return response.text
    elif response.status_code == 500:
        print('no cookie found you have to login...')
        enter()
    else:
        print(f"errr:{response.status_code}")


# המשחק עצמו
def word():
    response = session.get(f'{basic_url}/start_play')
    if response.status_code == 200:
        return response.status_code
    elif response.status_code == 500:
        print('no cookie found you have to login...if you dont want to finish')
        x = False
        while x == False:
            if enter() != False:
                print("you are in and start play")
                break
    w1 = str(mix())
    word_keep = w1
    count_loss = 0
    count_ch = 0
    my_word = ''
    pass_us = get_cookie()
    for i in w1:
        if i == ' ':
            my_word += ' '
            count_ch += 1
        else:
            my_word += '_'
    while count_loss < 8 and count_ch != len(w1):
        print(my_word)
        ch = input(print("put a char: "))
        while True:
            try:
                if not ch.isalpha() or len(ch) != 1:
                    raise Exeptions.NotAString()
                break
            except Exeptions.NotAString as e:
                print(e)
                ch = input(print('error!! your choice again please: '))
            except:
                ch = input(print('error!! your choice again please: '))
        if w1.find(ch) == -1:
            count_loss += 1
            if count_loss > 7:
                print("you loss this time,try again... may you success next time:)")
                update_my_play(pass_us, word_keep)

                return
            print(levels(count_loss)[0]), print(levels(count_loss)[1])

            print(f'you can loss jost {7 - count_loss} times...')
        #     the file
        while w1.find(ch) != -1:
            count_ch += 1
            place = w1.find(ch)
            if place < len(w1):
                my_word = my_word[:place] + ch + my_word[place + 1:]
                w1 = w1[:place] + '0' + w1[place + 1:]
            else:
                my_word = my_word[:place] + ch
                w1 = w1[:place] + '0'
        if count_ch == len(word_keep):
            print("you are win!!")
            update_my_win(pass_us)
            update_my_play(pass_us, word_keep)
            break
            return


# היטורית השחקן
def history(password):
    password = str(password)
    response = session.post(f'{basic_url}/history', json=password)
    if response.status_code == 200:
        print(response.text)
        return
    elif response.status_code == 500:
        print('no cookie found you have to login...')
        x = False
        while not x:
            if enter() != False:
                print("you are in -history")
                break
    else:
        return response.status_code


# מחזירה את מצב ההמן התלוי לפי הכשלונות עד כה
def levels(num_loss):
    file_level = open('./hung man.txt', 'r')
    level = file_level.read()
    level = level.split('\n\n')
    file_level.close()
    return "your hung man is: ", level[int(num_loss - 1)]


# פונקציית ניהול המשחק
def start_play():
    print(logo)
    response = session.get(f'{basic_url}/start_play')
    if response.status_code == 200:
        return response.status_code
    elif response.status_code == 500:
        print('no cookie found you have to login...')

    # try enter
    if enter() == False:
        ok = False
    else:
        ok = True
        #     if enter fall register
    if not ok:
        add_user()
    #         after register - enter till it will work
    while ok == False:
        if enter() != False:
            break
    num = 1
    while num != 3:
        num = input(print("press your choice ---1-to start game 2-see your history 3-to get out"))
        while True:
            try:
                if not num.isdigit() or int(num) > 3 or int(num) < 1:
                    raise Exeptions.NotInRage()
                break
            except Exeptions.NotInRage as e:
                print(e)
                num = input(print("error! Enter a number in the range again : "))
            except:
                num = input(print(" error! Enter a number in the range again: "))
        num = int(num)

        if num == 1:
            word()
        if num == 2:
            pass_us = get_cookie()
            print(history(pass_us))
    #     num = int(input(print("press your choice ---1-to start game 2-see your history 3-to get out")))
    sure = input(print("are you sure ?? press any key if not "))
    if sure != '':
        start_play()
    else:
        print('see you later...:) it was fun with you!!')


if __name__ == '__main__':
    start_play()
