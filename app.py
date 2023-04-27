from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from utils import login_required
import os
import sqlite3


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.secret_key = os.urandom(12).hex()
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

admins = {
    "abdulrahem" : "0000",
    "chris" : "1111",
    "humaid" : "2222"
}

conn = sqlite3.connect("inventory.db", check_same_thread=False)
c = conn.cursor()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    # Get flashed messages and clear session
    if session.get("_flashes"):
        flashes = session.get("_flashes")
        session.clear()
        session["_flashes"] = flashes
    else:
        session.clear()

    # If user clicked on the site
    if request.method == "GET":
        return render_template("login.html")
    # If user has been sending a request to site
    elif request.method == "POST":
        if not request.form.get("username"):
            flash(message="Please enter a username", category="error")
            return redirect(url_for('login'))
        elif not request.form.get("password"):
            flash("Incorrect password", category="error")
            return redirect(url_for('login'))

        username = request.form.get("username")
        pw = request.form.get('password')
        if pw != admins[username]:
            flash("Login unsuccessful", category="error")
            return redirect(url_for('login'))
        else:
            session["user_id"] = username
            flash("Login successful", category="success")
            return redirect('/admin')


@app.route('/admin')
@login_required
def admin():
    c.execute("SELECT * FROM inventory")
    items = c.fetchall()
    items_name = [item[0] for item in items]
    items_price = [item[1] for item in items]
    items = dict(map(lambda i, j: (i, j), items_name, items_price))
    inv = []
    for key, value in items.items():
        inv.append({"name": key, "price": value})
    return render_template("admin.html", items=inv)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect('/')


@app.route("/delete", methods = ["GET", "POST"])
@login_required
def delete():
    if request.method == "GET":
        return redirect('admin')
    else:
        name = request.form.get("name")
        c.execute(f"DELETE FROM inventory WHERE name = '{name}'")
        conn.commit()
        return redirect('admin')


@app.route("/edit", methods = ["GET", "POST"])
@login_required
def edit():
    if request.method == "GET":
        name = request.args.get('edited')
        return render_template('edit.html', name=name)
    else:
        name = request.form.get("edited")
        new_price = request.form.get("price")
        new_price = float(new_price)
        if new_price and new_price >= 0:
            c.execute(f"UPDATE inventory SET price = {new_price} WHERE name = '{name}'")
            conn.commit()
            flash(f"{name} edited successfully", category="success")
            return redirect("admin")
        else:
            flash("Incorrect price given", category="error")
            return redirect("admin")
