from .. import db
import datetime


class Comment(db.Model):
    """ Comment Model for storing post related details """
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    reply = db.relationship('Comment', backref=db.backref('parent', remote_side='Comment.id'))
    creation_date = db.Column(db.DateTime, nullable=False,
                              default=datetime.datetime.utcnow())

    def __repr__(self):
        return f"<Comment '{self.body}'>"
