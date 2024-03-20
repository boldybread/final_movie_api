from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma

VALID_RATINGS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

# model needs to be class, extends from the model class in SQLAlchemy
class Rating(db.Model):
    __tablename__ = "rating"

    # structure of table, each column
    rating_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date) # Date the rating was added
    user_rating = db.Column(db.Integer)

    # FKs linking to Movie/User tables
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    user = db.relationship('User', back_populates='rating')
    movie = db.relationship('Movie', back_populates='rating')

# user schema, also class, using schema class provided by marshmallow
class RatingSchema(ma.Schema):
    title = fields.String(required=True, validate=And(
        Length(min=2, error="Title must be at least 2 characters long"),
        Regexp('^[a-zA-Z0-9 ]+$', error="Title can only have alphanumeric characters")
    ))

    user_rating = fields.Integer(validate=OneOf(VALID_RATINGS))

# Nested tells marshmallow it is relationship field rather than its own field
    user = fields.Nested('UserSchema', only = ['name', 'email'])

    movie = fields.List(fields.Nested('MovieSchema', exclude=['rating']))

    class Meta:
        fields = ('rating_id', 'date', 'user_rating', 'user', 'movies')
        ordered = True

# create schema for handling one user, and schema for handling many users
rating_schema = RatingSchema()
ratings_schema = RatingSchema(many=True)