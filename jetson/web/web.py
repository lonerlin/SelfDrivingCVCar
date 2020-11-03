from flask import Flask, render_template, request, redirect, url_for, session
from db import *
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
#app.config['DEBUG'] = True
dbPath='webDB.db'


def listToJson(lst):
    import json
    import numpy as np
    keys = [str(x) for x in np.arange(len(lst))]
    list_json = dict(zip(keys, lst))
    str_json = json.dumps(list_json, indent=2, ensure_ascii=False)  # json转为string
    return str_json


@app.route('/clear/',methods = ['POST', 'GET'])
def clear_data():
    cnn = get_conn(dbPath)
    delete(cnn, "delete from student where id > ?", [(1,)])
    return "true"

@app.route('/student/', methods = ['POST', 'GET'])
def get_student():
    cnn = get_conn(dbPath)
    data = fetchall(cnn, "select  name,record_time from student  order by id desc")
    print(data)
    return listToJson(data)

@app.route('/')
def deviceroute():
   return "连接成功！"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
