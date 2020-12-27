# -*- coding: utf-8 -*-
"""Defines the URL routes for a Flask application
"""

from datetime import datetime as dt

from flask import current_app, g, render_template, request, send_file
from flask.cli import with_appcontext

from . import db

@with_appcontext
@current_app.route('/')
def home():
    posts = db.get_posts(orderByDate=True, limit=2)
    return render_template('home.html', current='home', posts=posts)

@current_app.route('/post/<int:post_id>')
def post(post_id):
    post = db.get_posts(id=post_id)
    tags =  db.get_tags(post_ref=post_id)
    return render_template('post.html',
                           current='posts',
                           post=post,
                           tags=tags)

@current_app.route('/posts', methods=["GET", "POST"])
def posts():
    tags = db.get_tags()
    request_start = None
    request_end = None
    request_tags = []

    if request.method == "POST":
        request_start = request.form['start']
        request_end = request.form['end']
        request_tags = request.form.getlist('tags')
        posts = db.get_posts(startDate=request_start, endDate=request_end, tags=request_tags)   
    else:
        posts = db.get_posts(orderByDate=True, limit=5)
    return render_template('posts.html', current='posts', tags=tags, posts=posts, \
                                         request_start=request_start, request_end=request_end, \
                                         request_tags=request_tags)
    

@current_app.route('/about')
def about():
    return render_template('about.html', current='about')

@current_app.route('/gallery')
def gallery():
    return render_template('gallery.html', current='gallery', photos=db.get_photos())

@current_app.route('/gallery/<int:photo_id>')
def photo(photo_id):
    photo_path = 'static/' + db.get_photos(photo_id)[0]['path']
    return send_file(photo_path, mimetype='image/gif')