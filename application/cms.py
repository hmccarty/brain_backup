from frontmatter import Frontmatter
from datetime import datetime as dt
from .models import db, Post, Tag
import markdown

class ContentMgmt:
    def __init__(self):
        pass

    def update(self):
        post_data = Frontmatter.read_file("application/static/journal/2020-06-30-FirstPost.md")

        if not Post.query.filter(Post.title == post_data['attributes']['title']):
            for tag in post_data['attributes']['tags']:
                db.session.add(Tag(
                    name=tag
                ))
            db.session.commit()

            post = Post (
                date=dt.now(),
                title=post_data['attributes']['title'],
                description=post_data['attributes']['description'],
                content=post_data['body']
            )
            db.session.add(post)
            db.session.commit()

    def get_posts(self):
        post_entries = Post.query.filter(Post.date).limit(10)
        posts = []
        for post in post_entries:
            post.content = markdown.markdown(post.content)
            posts.append(post)
        return posts

    def get_post(self, post_id):
        post = Post.query.filter(Post.id == post_id).first()
        post.content = markdown.markdown(post.content)
        return post