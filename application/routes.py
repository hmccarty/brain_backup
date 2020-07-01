from flask import render_template
from flask import current_app as app
from .models import db, Post

@app.route('/')
def home():

    return render_template('home.html')

@app.route('/journal')
def journal():
    return render_template('journal.html')

@app.route('/quotes')
def quotes():
    return render_template('quotes.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')