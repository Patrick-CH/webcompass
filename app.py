from flask import Flask, redirect, abort, make_response, request, session, url_for
from urllib.parse import urljoin, urlparse
import os

app = Flask("hello")
app.secret_key = os.getenv('SECRET_KEY', 'secret string')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='hello', **kwargs):
    """

    :param default: 获取信息失败时的返回值
    :param kwargs: 可选参数，作用同上
    :return: 重定向到上一个界面，如过无法获取上一个界面则返回default
    """
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


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
    response = make_response(redirect_back())
    response.set_cookie('name', name)
    return response


@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect_back()


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect_back()


@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        return abort(403)
    return 'welcome to admin page'


if __name__ == '__main__':
    app.run()
