from flask import current_app as app
from flask import render_template

from . import cms

@app.route('/')
def home():
    post = cms.get()

    return render_template('home.html',
                           posts=[post])

@app.route('/journal')
def journal():
    return render_template('journal.html')

@app.route('/quotes')
def quotes():
    return render_template('quotes.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')