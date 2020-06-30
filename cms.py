from frontmatter import Frontmatter
import markdown

def get():
    post = Frontmatter.read_file('static/journal/2020-06-30-FirstPost.md')
    post['body'] = markdown.markdown(post['body'])
    return post

