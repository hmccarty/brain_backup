#!/usr/bin/env python

"""Wraps functions to manage sqlite database.

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

from flask import current_app as app, g
from flask.cli import with_appcontext
from datetime import datetime as dt
from frontmatter import Frontmatter
import sqlite3
import markdown
import click

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(add_post_command)
    app.cli.add_command(add_photo_command)

def init_db():
    db = get_db()

    with app.open_resource('./schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE_URI'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def query_db(query, args=()):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return rv

def insert_db(insert, args=()):
    db = get_db()
    cur = db.cursor()
    cur.execute(insert, args)
    db.commit()
    rv = cur.lastrowid
    cur.close()
    return rv   

def get_posts(startDate=None, endDate=None, orderByDate=True, \
              tags=None, id=None, values=["*"], limit=None):
    query = 'SELECT '
    args = []
    query += ', '.join(values)
    query += ' FROM post '

    if tags:
        query += 'INNER JOIN ( '
        query += 'SELECT post_ref FROM post_tag '
        tag_list = ','.join('?' * len(tags))
        query += f'WHERE tag_ref IN ({tag_list}) '
        args.extend(tags)
        query += 'GROUP BY post_ref ) '
        query += 'ON id = post_ref '
    
    firstInList = True
    if startDate:
        query += 'WHERE '
        query += '? <= created '
        args.append(startDate)
        firstInList = False

    if endDate:
        if not firstInList:
            query += 'AND '
        else:
            query += 'WHERE ' 
            firstInList = False
        query += '? > created '
        args.append(endDate)
    
    if id:
        if not firstInList:
            query += 'AND '
        else:
            query += 'WHERE ' 
            firstInList = False
        query += '? = id '
        args.append(id)

    if orderByDate:
        query += 'ORDER BY created DESC '

    if limit:
        query += 'LIMIT ? '
        args.append(limit)

    return query_db(query, list(args))

def get_tags(post_ref=None):
    query = 'SELECT * FROM '
    query += 'post_tag INNER JOIN tag ON post_tag.tag_ref = tag.id '
    args = []
    
    if post_ref:
        query += 'WHERE '
        query += '? = post_tag.post_ref '
        args.append(post_ref)

    query += 'GROUP BY tag_ref '

    return query_db(query, args)

def get_photos(photo_id=None):
    query = 'SELECT * FROM photo '
    args = []
    
    if photo_id:
        query += 'WHERE '
        query += '? = photo.id '
        args.append(photo_id)

    return query_db(query, args) 

def add_post(path):
    post = Frontmatter.read_file(path)
    body = markdown.markdown(post['body'])

    sql = ('INSERT INTO post(title, description, body) '
           'VALUES (?, ?, ?)')
    post_ref = insert_db(sql, (post['attributes']['title'],
                               post['attributes']['description'],
                               body))

    tags = post['attributes']['tags']
    for tag in tags:
        tag_ref = None
        query = ('SELECT tag.id FROM tag WHERE tag.name = ?')
        found_tag = query_db(query, [tag])
        if not found_tag:
            sql = ('INSERT INTO tag(name) '
                'VALUES (?)')
            tag_ref = insert_db(sql, [tag])
        else:
            tag_ref = found_tag[0]['id']
        
        sql = ('INSERT INTO post_tag(post_ref, tag_ref) '
               'VALUES (?, ?)')
        insert_db(sql, [post_ref, tag_ref])

    return True

def add_photo(title, path):
    path = path.split("brainbackup/static/",1)[1]
    sql = ('INSERT INTO photo(title, path) '
           'VALUES (?, ?)')
    post_ref = insert_db(sql, [title, path])

    return True

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('add-post')
@click.argument('path')
@with_appcontext
def add_post_command(path):
    """Add new post to the database."""
    if add_post(path):
        click.echo('Post successfully added.')
    else:
        click.echo('Post upload failed.')

@click.command('add-photo')
@click.argument('title')
@click.argument('path')
@with_appcontext
def add_photo_command(title, path):
    """Add new photo to the database."""
    if add_photo(title, path):
        click.echo('Photo successfully added.')
    else:
        click.echo('Photo upload failed.')