# -*- coding: utf-8 -*-
"""Defines the URL routes for a Flask application

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

"""

from datetime import datetime as dt

from flask import current_app, g, render_template, request
from flask.cli import with_appcontext

from . import db

@with_appcontext
@current_app.route('/')
def home():
    posts = db.get_posts(orderByDate=True)
    return render_template('home.html', current='home', posts=posts)

@current_app.route('/post/<int:post_id>')
def post(post_id):
    post = db.get_posts(id=post_id)
    tags =  db.get_tags(post_ref=post_id)
    print(tags)
    return render_template('post.html',
                           current='journal',
                           post=post,
                           tags=tags)

@current_app.route('/journal', methods=["GET", "POST"])
def journal():
    if request.method == "POST":
        start = request.form['start']
        end = request.form['end']
        tags = request.form.getlist('tags')
        posts = db.get_posts(startDate=start, endDate=end, tags=tags)
        return render_template('journal.html', current='journal', posts=posts)
    else:
        tags = db.get_tags()
        return render_template('journal.html', current='journal', tags=tags, searching=True)
    

@current_app.route('/about')
def quotes():
    return render_template('about.html', current='about')

@current_app.route('/gallery')
def gallery():
    return render_template('gallery.html', current='gallery')
