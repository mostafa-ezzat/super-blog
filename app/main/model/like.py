from .. import db


class Like(db.Model):
    """ Like Model for storing like related details """
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
