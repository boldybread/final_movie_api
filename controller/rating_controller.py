import functools

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.rating import Rating, ratings_schema, rating_schema
from models.movie import Movie
from models.user import User
from controller.rating_controller import ratings_bp

ratings_bp = Blueprint('ratings', __name__, url_prefix='/ratings')
ratings_bp.register_blueprint(watchlists_bp)

def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        # if the user is an admin
        if user.is_admin:
            # we will continue and run the decorated function
            return fn(*args, **kwargs)
        # else (if the user is NOT an admin)
        else:
            # return an error
            return {"error": "Not authorised to delete a rating"}, 403
        
    return wrapper

# http://localhost:8080/ratings - GET
@ratings_bp.route('/')
def get_all_ratings():
    stmt = db.select(Rating).order_by(Rating.release.desc())
    ratings = db.session.scalars(stmt)
    return ratings_schema.dump(ratings)


# http://localhost:8080/ratings/4 - GET
@ratings_bp.route('/<int:rating_id>')
def get_one_rating(rating_id): # rating_id = 4
    stmt = db.select(Rating).filter_by(id=rating_id) # select * from ratings where id=4
    rating = db.session.scalar(stmt)
    if rating:
        return rating_schema.dump(rating)
    else:
        return {"error": f"Rating with id {rating_id} not found"}, 404
    

# http://localhost:8080/ratings - POST
@ratings_bp.route('/', methods=["POST"])
@jwt_required()
def create_rating():
    body_data = rating_schema.load(request.get_json())
    # Create a new rating model instance
    rating = Rating(
        date = body_data.get('date'),
        user_rating = body_data.get('user_rating'),
        movie_id = body_data.get('movie_id'),
        user_id = get_jwt_identity()
    )
    # Add that to the session and commit
    db.session.add(rating)
    db.session.commit()
    # return the newly created rating
    return rating_schema.dump(rating), 201

# https://localhost:8080/ratings/6 - DELETE
@ratings_bp.route('/<int:rating_id>', methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_rating(rating_id):
    # # check user's admin status
    # is_admin = is_user_admin()
    # if not is_admin:
    #     return {"error": "Not authorised to delete a rating"}, 403
    # get the rating from the db with id = rating_id
    stmt = db.select(Rating).where(Rating.id == rating_id)
    rating = db.session.scalar(stmt)
    # if rating exists
    if rating:
        # delete the rating from the session and commit
        db.session.delete(rating)
        db.session.commit()
        # return msg
        return {'message': f"Rating '{rating.title}' deleted successfully"}
    # else
    else:
        # return error msg
        return {'error': f"Rating with id {rating_id} not found"}, 404
    
# http://localhost:8080/ratings/5 - PUT, PATCH
@ratings_bp.route('/<int:rating_id>', methods=["PUT", "PATCH"])
@jwt_required()
def update_rating(rating_id):
    # Get the data to be updated from the body of the request
    body_data = rating_schema.load(request.get_json(), partial=True)
    # get the rating from the db whose fields need to be updated
    stmt = db.select(Rating).filter_by(id=rating_id)
    rating = db.session.scalar(stmt)
    # if rating exists
    if rating:
        if str(rating.user_id) != get_jwt_identity():
            return {"error": "Only the owner can edit the rating"}, 403
        # update the fields
        rating.date = body_data.get('date') or rating.date
        rating.user_rating = body_data.get('user_rating') or rating.user_rating
        # commit the changes
        db.session.commit()
        # return the updated rating back
        return rating_schema.dump(rating)
    # else
    else:
        # return error msg
        return {'error': f'Rating with id {rating_id} not found'}, 404
    

# This function has been replaced by the authorise_as_admin decorator
def is_user_admin():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin