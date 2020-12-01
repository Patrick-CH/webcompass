from flask import Flask, redirect, abort, make_response, request, session, url_for, render_template, flash, Markup
from urllib.parse import urljoin, urlparse
import os, click, pymysql, wtforms, flask_wtf
from flask_sqlalchemy import SQLAlchemy
from Forms import SigninForm, RegisterForm, SearchForm, TranslateForm, PicForm
from get_trans import get_translation

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:112358@localhost:3306/flask"  # os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


def get_url(search_engine, keywords):
    url = "/index"
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


@app.cli.command()
def initdb():
    db.drop_all()
    db.create_all()
    click.echo("Initialized database")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        flash('You are already logged in!')
        return redirect(url_for('index'))
    signin_form = SigninForm()
    if signin_form.submit.data and signin_form.validate():
        username = signin_form.username.data
        password = signin_form.password.data
        from models import User
        user = User.query.filter(User.username==username).first()
        if user is not None:
            if user.password == password:
                flash('%s, log in successfully.' % username)
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash('wrong password')
                return redirect(url_for('login'))
        else:
            flash('user does not exist')
    return render_template('login_form.html', signin_form=signin_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.submit.data and register_form.validate():
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data
        if not username or not email or not password:
            return 'input error'
        from models import User
        newobj = User(username=username, email=email, password=password)
        db.session.add(newobj)
        db.session.commit()
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


@app.route('/translate', methods=['GET', 'POST'])
def translate():
    translate_form = TranslateForm()
    text = None
    d = {
        '0': 'zh',
        '1': 'en',
        '2': 'fra',
        '3': 'de'
    }
    if translate_form.submit.data:
        content_language = translate_form.content_language.data
        content = translate_form.content.data
        aim_language = translate_form.aim_language.data
        # [(0, "Chinese"), (1, "English"), (2, 'French'), (3, 'German')]
        text = get_translation(d[content_language], d[aim_language], content)
        # return redirect(url_for('translate'))
    return render_template("translate.html", translate_form=translate_form, text=text)


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('index'))


@app.route('/get_pics', methods=['GET', 'POST'])
def get_pics():
    if 'logged_in' in session:
        username = session['username']
        from models import User
        user = User.query.filter(User.username==username).first()
        from get_pics import get_imgs
        pic_search_form = PicForm()
        if pic_search_form.submit.data:
            flash("Email will be send to you soon.")
            content = pic_search_form.content.data
            print("content = " + content)
            zipfile = get_imgs(content)
            from send_email import Send_Email
            Send_Email(zipfile, [user.email])
            return redirect(url_for('index'))
        return render_template("picsearch.html", pic_search_form=pic_search_form)
    else:
        flash("Please log in first")
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
