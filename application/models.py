from . import db

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

class Post(db.Model):
    """Data model for posts"""
    
    id = db.Column (
        db.Integer,
        primary_key=True
    )

    date = db.Column (
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )

    title = db.Column (
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )

    description = db.Column (
        db.String(128),
        index=False,
        unique=False,
        nullable=False
    )

    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('pages', lazy=True))

    content = db.Column (
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return '<Post {}>'.format(self.id)

class Tag(db.Model):
    """ Data model for tags """

    id = db.Column (
        db.Integer,
        primary_key=True
    )

    name = db.Column (
        db.String(32),
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return '<Tag {}>'.format(self.id)