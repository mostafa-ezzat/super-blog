from .. import db


class Category(db.Model):
    """ Category Model for storing user related details """
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return self.cat

# POST -> Category
