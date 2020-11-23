from flask import Flask, redirect, abort, make_response, request, session, url_for, render_template, flash, Markup
from urllib.parse import urljoin, urlparse
import os, wtforms, flask_wtf
from Forms import SigninForm, RegisterForm, SearchForm

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


def get_url(search_engine, keywords):
    url = ""
    if search_engine == "0":
        url = "https://www.baidu.com/s?wd={}&rsv_spt=1&rsv_iqid=0x9f603f1b000665af&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=\
        utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=9&rsv_sug1=8&rsv_sug7=100&rsv_sug2=0&inputT=3638&rsv_sug4=3638&\
        rsv_sug=2".format(keywords)
    elif search_engine == "1":
        url = "https://www.google.com.hk/search?q={}&oq={}&aqs=chrome..\
        69i57j35i39i362l7...7.888j0j15&sourceid=chrome&ie=UTF-8".format(keywords, keywords)
    elif search_engine == "2":
        url = "https://cn.bing.com/search?q={}&qs=n&form=QBLHCN&sp=-1&pq={}&sc=0-15&sk=&\
        cvid=ED80265A56B248A58E26BCB71FE22015".format(keywords, keywords)
    return url


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
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    signin_form = SigninForm()
    if signin_form.submit.data and signin_form.validate():
        username = signin_form.username.data
        flash('%s, you just submit the Signin Form.' % username)
        return redirect(url_for('index'))
    return render_template('login_form.html', signin_form=signin_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.submit.data and register_form.validate():
        username = register_form.username.data
        flash('%s, you just submit the Register Form.' % username)
        return redirect(url_for('index'))
    return render_template('register_form.html', register_form=register_form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    search_form = SearchForm()
    if search_form.submit.data:
        search_engine = search_form.SearchEngine.data
        content = search_form.content.data
        return redirect(get_url(search_engine, content))
    return render_template("search.html", search_form=search_form)


if __name__ == '__main__':
    app.run(debug=True)
