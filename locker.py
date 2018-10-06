from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/items')
def items():
    return render_template("items.html")


@app.route('/status')
def status():
    return render_template("status.html")


@app.route('/schedule')
def schedule():
    return render_template("schedule.html")


@app.route('/notifications')
def notifications():
    return render_template("notifications.html")


if __name__ == '__main__':
    app.run()
