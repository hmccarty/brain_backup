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

def get_posts(startDate=None, endDate=None, orderByDate=False, \
              tags=None, id=None, values=["*"], limit=None):
    query = 'SELECT '
    args = []
    query += ', '.join(values)
    query += ' FROM post '
    
    firstInList = True
    if startDate:
        query += 'WHERE '
        query += '? <= post.created '
        args.append(startDate)
        firstInList = False

    if endDate:
        if not firstInList:
            query += 'AND '
        else:
            query += 'WHERE ' 
            firstInList = False
        query += '? > post.created '
        args.append(endDate)
    
    if id:
        if not firstInList:
            query += 'AND '
        else:
            query += 'WHERE ' 
            firstInList = False
        query += '? = post.id '
        args.append(id)

    if orderByDate:
        query += 'ORDER BY post.created DESC '

    if limit:
        query += 'LIMIT ? '
        args.append(limit)

    return query_db(query, tuple(args))

def add_post(path):
    db = get_db()
    post = Frontmatter.read_file(path)

    sql = ('INSERT INTO post(title, description, body) '
           'VALUES (?, ?, ?)')
    print(post)
    db.cursor().execute(sql, (post['attributes']['title'],
                              post['attributes']['description'],
                              post['body']))
    db.commit()
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
