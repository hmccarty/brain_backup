from frontmatter import Frontmatter
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
import markdown

db = SQLAlchemy(app)
db.init_app(app)
db.create_all()

def update():
    post = Post (
        created=dt.now(),
        path='static/journal/2020-06-30-FirstPost.md'
    )
    db.session.add(post)
    db.session.commit()
    print (Post.query.all())

def get():
    post = Frontmatter.read_file('static/journal/2020-06-30-FirstPost.md')
    post['body'] = markdown.markdown(post['body'])
    return post