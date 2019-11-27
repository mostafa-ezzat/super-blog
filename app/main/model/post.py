from .. import db
import datetime

# many to many relationships ( Post, Category )

cats = db.Table('cats',
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                db.Column('cate_id', db.Integer, db.ForeignKey('category.id'))
                )


class Post(db.Model):
    """ Post Model for storing post related details """
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean, default=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False,
                              default=datetime.datetime.utcnow())
    categories = db.relationship('Category', secondary=cats,
                                 backref=db.backref('categories', lazy='immediate'))

    like = db.relationship('Like', backref='like', lazy='immediate')
    comment = db.relationship('Comment', backref='pcomment', lazy='immediate')

    def __repr__(self):
        return "<Post '{}'>".format(self.title)
