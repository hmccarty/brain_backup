from flask import render_template
from flask import current_app as app
from datetime import datetime as dt
from .models import db, Post
from .cms import ContentMgmt

content_mgmt = ContentMgmt()

@app.route('/')
def home():
    content_mgmt.update()
    return render_template('home.html', posts=content_mgmt.get_posts())

@app.route('/post/<int:post_id>')
def post(post_id):
    post = content_mgmt.get_post(post_id)
    return render_template('post.html',
        post=post)

@app.route('/journal')
def journal():
    return render_template('journal.html')

@app.route('/quotes')
def quotes():
    return render_template('quotes.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')