from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma

# Create accepted genres/ viewing platforms
VALID_GENRE = ('Action', 'Drama', 'Comedy', 'Thriller', 'Horror')
VALID_PLATFORM = ('Netflix', 'Prime', 'Binge', 'Stan')

# model needs to be class, extends from the model class in SQLAlchemy
class Movie(db.Model):
    __tablename__ = "movie"

    # structure of table, each column
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True)
    description = db.Column(db.Text)
    release = db.Column(db.String(4))
    genre = db.Column(db.String)
    viewing_platform = db.Column(db.String)

    rating = db.relationship('Rating', back_populates='movie')
    watchlist = db.relationship('Watchlist', back_populates='movie')

# movie schema, also class, using schema class provided by marshmallow
class MovieSchema(ma.Schema):

    title = fields.String(required=True, validate=And(
        Length(min=2, error="Title must be at least 2 characters long"),
        Regexp('^[a-zA-Z0-9 ]+$', error="Title can only have alphanumeric characters")
    ))

    release = fields.Integer(required=True, validate=And(
        Length(min=4, max=4, error="Release year must be 4 digits, eg '2016'")
    ))

    genre = fields.String(validate=OneOf(VALID_GENRE))

    viewing_platform = fields.String(validate=OneOf(VALID_PLATFORM))

    rating = fields.Nested('RatingSchema', only = ['user_rating'])

    watchlist = fields.List(fields.Nested('WatchlistSchema', exclude=['movie']))

    class Meta:
        fields = ('id', 'title', 'description', 'release', 'genre', 'viewing_platform', 'rating', 'watchlist')
        ordered = True

# create schema for handling one user, and schema for handling many users
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)