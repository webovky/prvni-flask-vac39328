from flask import Flask, render_template, request, redirect, url_for, session, flash
import functools
import random
import string
# from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = b"totoj e zceLa n@@@hodny retezec nejlep os.urandom(24)"
app.secret_key = b"x6\x87j@\xd3\x88\x0e8\xe8pM\x13\r\xafa\x8b\xdbp\x8a\x1f\xd41\xb8"


slova = ("Super", "Perfekt", "Úža category", "Flask")


def prihlasit(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("login", url=request.path))

    return wrapper


@app.route("/", methods=["GET"])
def index():
    return render_template("base.html")


@app.route("/info/")
def info():
    return render_template("info.html")


@app.route("/abc/")
def abc():
    if "uživatel" not in session:
        flash('Nejsi přihlášen. Tato stránka vyžaduje přihlášení.', 'error')
        return redirect(url_for("login",page=request.full_path))
    return render_template("abc.html", slova=slova)

@app.route("/zkracovač/")
def zkracovač():
    return render_template("zkracovač.html")

@app.route("/zkracovač/", methods = ["POST"])
def zkracovač_post():
    url = request.form.get("url")
    zkratka = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    with SQLite("data1.db") as cur:
                cur.execute("INSERT INTO user (zkratka, adresa) VALUES (?,?)", [zkratka, url])
    return redirect(url_for("zkracovač"))

@app.route("/malina/", methods=["GET", "POST"])
def malina():
    if "uživatel" not in session:
        flash('Nejsi přihlášen. Tato stránka vyžaduje přihlášení.', 'error')
        return redirect(url_for("login",page=request.full_path))

    hmotnost = request.args.get("hmotnost")
    vyska = request.args.get("vyska")

    print(hmotnost, vyska)
    if hmotnost and vyska:
        try:
            hmotnost = float(hmotnost)
            vyska = float(vyska)
            bmi = hmotnost / (0.01 * vyska) ** 2
        except (ZeroDivisionError, ValueError):
            bmi = None
            # err = 'Je třeba zadat dvě nenulová čísla!'
    else:
        bmi = None

    return render_template("malina.html", bmi=bmi)


@app.route("/login/", methods=["GET"])
def login():
    jmeno = request.args.get("jmeno")
    heslo = request.args.get("heslo")
    print(jmeno, heslo)
    return render_template("login.html")


@app.route("/login/", methods=["POST"])
def login_post():
    jmeno = request.form.get("jmeno")
    heslo = request.form.get("heslo")
    page = request.args.get("page")
    if jmeno == "filip" and heslo == "balon":
        session["uživatel"] = jmeno
        if page:
            return redirect(page)
    else:
        flash("Nesprávné přihlašovací údaje", "error")
    if page:
        return redirect(url_for("login", page=page))
    return redirect(url_for("login"))
"""
@app.route("/registrace/", methods=["GET", "POST"])
def registrace():

    if request.method == "GET":
        return render_template("registrace.html")

    if request.method == "POST":
        jmeno = request.form.get("jmeno")
        heslo = request.form.get("heslo")
        heslo2 = request.form.get("heslo znovu")
        if not (jmeno and heslo2 and heslo):
            flash("Není vše vyplňeno!", "message")
            return redirect(url_for("registrace"))
        if heslo != heslo2:
            flash("Hesla se neshodují!", "message")
            return redirect(url_for("registrace"))
        try:
            with SQLite("data1.db") as cur:
                cur.execute("INSERT INTO user (login, passwd) VALUES (?,?)", [jmeno, generate_password_hash(heslo)])
                cur execute("SELECT passwd FROM user WHERE login = ?",[jmeno])
                flash("Jsi registrován", "message")
                flash("Jsi přihlášen", "message")
                session["uživatel"] = jmeno
                return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash("Jmeno již existuje!", "message")
            return redirect(url_for("registrace"))

    return redirect(url_for("registrace"))
"""
@app.route("/logout/", methods=["GET", "POST"])
def logout():
    session.pop("uživatel", None)
    return redirect(url_for("index"))
