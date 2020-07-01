from . import db

class Post(db.Model):
    """Data model for posts"""

    __tablename__ = 'posts'
    
    id = db.Column (
        db.Integer,
        primary_key=True
    )

    created = db.Column (
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )

    path = db.Column (
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )

    def __repr__(self):
        return '<Post {}>'.format(self.id)