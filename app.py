from flask import Flask, redirect, abort, make_response, request, session, url_for
import os

app = Flask("hello")
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'human')
    response = '<h1>hello, %s</h1>' % name
    # 根据登录状态返回不同值
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response


@app.route('/hi')
def hi():
    return redirect(url_for('hello'))


@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(request.referrer or url_for('hello')))
    response.set_cookie('name', name)
    return response


@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(request.referrer or url_for('hello'))


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(request.referrer or url_for('hello'))


@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        return abort(403)
    return 'welcome to admin page'


if __name__ == '__main__':
    app.run()
