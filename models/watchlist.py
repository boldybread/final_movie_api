from init import db, ma
from marshmallow import fields

# model needs to be class, extends from the model class in SQLAlchemy
class Watchlist(db.Model):
    __tablename__ = "watchlist"

    # structure of table, each column
    id = db.Column(db.Integer, primary_key=True)
    watchlist_title = db.Column(db.String(20))

    # FKs linking to Movie/User tables
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)

    user = db.relationship('User', back_populates='watchlist')
    movie = db.relationship('Movie', back_populates='watchlist')

# user schema, also class, using schema class provided by marshmallow
class WatchlistSchema(ma.Schema):
    # Nested tells marshmallow it is relationship field rather than its own field
    user = fields.Nested('UserSchema', only=['name', 'email'])

    movie = fields.Nested('MovieSchema', exclude=['watchlist'])

    class Meta:
        fields = ('id', 'watchlist_title' 'user', 'movie')

# create schema for handling one user, and schema for handling many users
watchlist_schema = WatchlistSchema()
watchlists_schema = WatchlistSchema(many=True)