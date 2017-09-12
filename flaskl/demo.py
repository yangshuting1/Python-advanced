# -*- coding: UTF-8 -*-

# all import
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

# 获取整个文件的内容

app = Flask(__name__)

# 更新配置
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'user.db'),
    SECRET_KEY='development key'
))
# 加载配置
app.config.from_object(__name__)
app.config.from_envvar('FLASKL_SETTINGS', silent=True)


# 连接数据库
def connect_db():
    """Connects to the specific database. """
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


# 定义一个字段，用于接收连接数据库返回的值
_database = connect_db()


# 校验
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # 说明并没有连接上，需要重新连接
        db = g._database = connect_db()
    return db


# 最后确定数据库存在，再初始化数据库
def init_db():
    # 搭建应用环境
    with app.app_context():
        # g对象与app进行关联
        db = get_db()
        # 找到表
        with app.open_resource('user.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# 做视图
# 要用rout装饰器加路径

@app.route('/')
def show_choose():
    # 显示一句话
    flash('this is the main page')
    # 取数据库查所有的用户名，密码
    #cur = g.db.execute('SELECT name, userpass FROM entries ORDER BY id DESC')
    #entries = [dict(name=row[0], userpass=row[1]) for row in cur.fetchall()]
    return render_template('login.html')

@app.route('/main')
def show_main():
    flash('this is the main page')
    cur = g.db.execute('SELECT name, userpass FROM entries ORDER BY id DESC')
    entries = [dict(name=row[0], userpass=row[1]) for row in cur.fetchall()]
    return render_template('show_main.html',entries=entries)




# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        g.db.execute('INSERT INTO entries (name, userpass) VALUES (? ,?)',
                     [request.form['username'], request.form['userpass']])
        g.db.commit()
        flash('register success')
        return render_template('login.html')

    return render_template('register.html')


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['userpass']
        admin = g.db.execute("SELECT * FROM  entries WHERE name=='username' AND userpass == 'userpass'")
        if admin is None:
            error = 'Invalid username'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_main'))
    return render_template('login.html', error=error)


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)
