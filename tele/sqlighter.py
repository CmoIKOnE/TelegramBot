import pymysql
import pymysql.cursors
import datetime
import hashlib
from pymysql.cursors import DictCursor

def check_login(login):
    isis = True
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='D5bwNv6vzgq4HCkY',
        db='mcspace_me_db',
        charset='utf8mb4',
        cursorclass=DictCursor
    )
    try:
      
     
        with connection.cursor() as cursor:
           
            sql = "SELECT * FROM users WHERE login=%s"
            cursor.execute(sql, login)
     
            for row in cursor:
                if row:
                    isis = False
                else:
                    isis = True
                 
    finally:     
        connection.close()

    return isis

def checkEmail(email):
    isis = False
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='D5bwNv6vzgq4HCkY',
        db='mcspace_me_db',
        charset='utf8mb4',
        cursorclass=DictCursor
    )
    try:
      
     
        with connection.cursor() as cursor:
           
            sql = "SELECT login FROM users WHERE email=%s"
            cursor.execute(sql, email)
     
            for row in cursor:
                if row:
                    isis = True
                else:
                    isis = False
                 
    finally:     
        connection.close()

    return isis

def checkUserByData(login, email, password):
    canConnect = False
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='D5bwNv6vzgq4HCkY',
        db='mcspace_me_db',
        charset='utf8mb4',
        cursorclass=DictCursor
    )
    try:
      
     
        with connection.cursor() as cursor:
           
            sql = "SELECT login FROM users WHERE login=%s AND password=%s AND email=%s"
            hash_password = hashlib.md5(password.encode())
            password = hash_password.hexdigest()
            hash_password = hashlib.md5(password.encode())
            password = hash_password.hexdigest()
            args = (login,password,email)
            cursor.execute(sql, args)
            for row in cursor:
                if row:
                    canConnect = True
                else:
                    canConnect = False
            connection.commit()
                 
    finally:     
        connection.close()

    return canConnect

def changeAccountType(login, tele_id):
    msg = False
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='D5bwNv6vzgq4HCkY',
        db='mcspace_me_db',
        charset='utf8mb4',
        cursorclass=DictCursor
    )

    try:
      
     
        with connection.cursor() as cursor:
           
            sql = "UPDATE users SET email=%s, tele_id=%s WHERE login=%s LIMIT 1"
            email = str(tele_id) + 'teleMCS'
            args = (email,tele_id,login)
            cursor.execute(sql, args)
            if cursor.rowcount == 1:
                msg = True
            else:
                msg = False
            connection.commit()
                 
    finally:     
        connection.close()

    return msg

def add_account(login, password, tele_id):
    msg = False
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='D5bwNv6vzgq4HCkY',
        db='mcspace_me_db',
        charset='utf8mb4',
        cursorclass=DictCursor
    )

    try:
      
     
        with connection.cursor() as cursor:
           
            sql = "INSERT INTO users(login,email,tele_id,password,register) VALUES (%s,%s,%s,%s,%s)"
            email = str(tele_id) + 'teleMCS'
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            hash_password = hashlib.md5(password.encode())
            password = hash_password.hexdigest()
            hash_password = hashlib.md5(password.encode())
            password = hash_password.hexdigest()
            args = (login,email,tele_id,password,date)
            cursor.execute(sql, args)
            if cursor.rowcount == 1:
                msg = True
            else:
                msg = False
            connection.commit()
                 
    finally:     
        connection.close()

    return msg


def check_tele_id(tele_id):
    isid = True
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='D5bwNv6vzgq4HCkY',
        db='mcspace_me_db',
        charset='utf8mb4',
        cursorclass=DictCursor
    )
    try:

        with connection.cursor() as cursor:
           
            sql = "SELECT * FROM users WHERE tele_id=%s"
            cursor.execute(sql, tele_id)
     
            for row in cursor:
                if row:
                    isid = False
                else:
                    isid = True
                 
    finally:     
        connection.close()

    return isid

def hasAccountTelegram(login):
    isIt = False
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='D5bwNv6vzgq4HCkY',
        db='mcspace_me_db',
        charset='utf8mb4',
        cursorclass=DictCursor
    )

    try:

        with connection.cursor() as cursor:
           
            sql = "SELECT tele_id FROM users WHERE login=%s"
            cursor.execute(sql, login)
            glogin = cursor.fetchone()
            if(glogin != None and glogin['tele_id'] != 0):
                isIt = True
            else: isIt = False

    finally:     
        connection.close()

    return isIt


def get_login(tele_id):
    login = ''
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='D5bwNv6vzgq4HCkY',
        db='mcspace_me_db',
        charset='utf8mb4',
        cursorclass=DictCursor
    )
    try:

        with connection.cursor() as cursor:
           
            sql = "SELECT login FROM users WHERE tele_id=%s"
            cursor.execute(sql, tele_id)
            glogin = cursor.fetchone()
            if(glogin != None):
                login = glogin['login']

    finally:     
        connection.close()

    return login

def reset_password(password, tele_id):
    msg = False
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='D5bwNv6vzgq4HCkY',
        db='mcspace_me_db',
        charset='utf8mb4',
        cursorclass=DictCursor
    )
    try:
      
     
        with connection.cursor() as cursor:
           
            sql = "UPDATE users SET password=%s WHERE tele_id=%s LIMIT 1"
            hash_password = hashlib.md5(password.encode())
            password = hash_password.hexdigest()
            hash_password = hashlib.md5(password.encode())
            password = hash_password.hexdigest()
            args = (password,tele_id)
            cursor.execute(sql, args)
            if cursor.rowcount == 1:
                msg = True
            else:
                msg = False
            connection.commit()
                 
    finally:     
        connection.close()

    return msg