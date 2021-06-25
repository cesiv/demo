import flask
import json
import sqlite3
from flask import request

server = flask.Flask(__name__)
database = "memo"


def init_db():
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    ddl = '''
        CREATE  TABLE IF NOT EXISTS NOTICE (
            ID INTEGER PRIMARY KEY autoincrement,
            EMAIL TEXT ,
            TITLE TEXT ,
            CONTENT TEXT
            )
      '''
    cursor.execute(ddl)
    print("init table success!")
    cursor.close()
    connect.close()


def insert(data):
    connect = sqlite3.connect(database)
    cursor = connect.cursor()
    insert_sql = '''
    insert into notice values (null,?,?,?)
'''
    cursor.execute(insert_sql, data)
    connect.commit()
    cursor.close()
    connect.close()
    print("init data success")


def query():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    result = cursor.execute("select * from notice")
    for row in result:
        print(row)
    cursor.close()
    conn.close()


@server.route('/test', methods=['get', 'post'])
def test():
    result = {'code': 200, 'message': '登录成功'}
    return json.dumps(result, ensure_ascii=False)  #


@server.route('/add', methods=['get', 'post'])
def add():
    data = request.values.get('data')
    if not data:
        result = {'code': -1, 'message': '添加失败'}
        return json.dumps(result, ensure_ascii=False)  #
    try:
        insert(data)
        result = {'code': 200, 'message': '添加成功'}
    except Exception as ex:
        result = {'code': -1, 'message': str(ex)}
        return json.dumps(result, ensure_ascii=False)  #
    return json.dumps(result, ensure_ascii=False)  #


if __name__ == '__main__':
    init_db()
    server.run(port=45123, host='0.0.0.0')
