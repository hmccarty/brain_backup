from frontmatter import Frontmatter
import database
import markdown

def init():
    dbms = database.Database(database.SQLITE, dbname='mydb.sqlite')
    dbms.create_db_tables()

def get():
    post = Frontmatter.read_file('static/journal/2020-06-30-FirstPost.md')
    post['body'] = markdown.markdown(post['body'])
    return post

