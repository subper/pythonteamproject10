import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/calender')
def show_calender():
    return render_template('calender.html')

if __name__ == '__main__':
    app.debug=True
    app.run(host="127.0.0.1")