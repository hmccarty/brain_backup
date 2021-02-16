#!/usr/bin/env python

"""Defines the URL routes for a Flask application.

BSD 3-Clause License

Copyright (c) 2020, Harrison McCarty
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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

@current_app.route('/gallery/<string:photo_title>')
def photo(photo_title):
    photo_path = 'static/' + db.get_photos(photo_title)[0]['path']
    return send_file(photo_path, mimetype='image/gif')