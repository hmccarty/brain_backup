from datetime import datetime as dt
import sqlite3

from frontmatter import Frontmatter
import markdown
import click
from flask import current_app as app, g
from flask.cli import with_appcontext

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(add_post_command)

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
