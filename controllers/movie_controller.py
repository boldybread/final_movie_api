import functools

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.movie import Movie, movies_schema, movie_schema
from models.rating import Rating
from models.user import User
from models.watchlist import Watchlist
from controllers.watchlist_controller import watchlists_bp
from controllers.rating_controller import ratings_bp

movies_bp = Blueprint('movies', __name__, url_prefix='/movies')
movies_bp.register_blueprint(watchlists_bp)

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
            return {"error": "Not authorised to delete a movie"}, 403
        
    return wrapper

# http://localhost:8080/movies - GET
@movies_bp.route('/')
def get_all_movies():
    stmt = db.select(Movie).order_by(Movie.release.desc())
    movies = db.session.scalars(stmt)
    return movies_schema.dump(movies)


# http://localhost:8080/movies/4 - GET
@movies_bp.route('/<int:movie_id>')
def get_one_movie(movie_id): # movie_id = 4
    stmt = db.select(Movie).filter_by(id=movie_id) # select * from movies where id=4
    movie = db.session.scalar(stmt)
    if movie:
        return movie_schema.dump(movie)
    else:
        return {"error": f"Movie with id {movie_id} not found"}, 404
    

# http://localhost:8080/movies - POST
@movies_bp.route('/', methods=["POST"])
@jwt_required()
def create_movie():
    body_data = movie_schema.load(request.get_json())
    # Create a new movie model instance
    movie = Movie(
        title = body_data.get('title'),
        description = body_data.get('description'),
        release = body_data.get('release'),
        genre = body_data.get('genre'),
        viewing_platform = body_data.get('viewing_platform'),
        user_id = get_jwt_identity()
    )
    # Add that to the session and commit
    db.session.add(movie)
    db.session.commit()
    # return the newly created movie
    return movie_schema.dump(movie), 201

# https://localhost:8080/movies/6 - DELETE
@movies_bp.route('/<int:movie_id>', methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_movie(movie_id):
    # # check user's admin status
    # is_admin = is_user_admin()
    # if not is_admin:
    #     return {"error": "Not authorised to delete a movie"}, 403
    # get the movie from the db with id = movie_id
    stmt = db.select(Movie).where(Movie.id == movie_id)
    movie = db.session.scalar(stmt)
    # if movie exists
    if movie:
        # delete the movie from the session and commit
        db.session.delete(movie)
        db.session.commit()
        # return msg
        return {'message': f"Movie '{movie.title}' deleted successfully"}
    # else
    else:
        # return error msg
        return {'error': f"Movie with id {movie_id} not found"}, 404
    
# http://localhost:8080/movies/5 - PUT, PATCH
@movies_bp.route('/<int:movie_id>', methods=["PUT", "PATCH"])
@jwt_required()
def update_movie(movie_id):
    # Get the data to be updated from the body of the request
    body_data = movie_schema.load(request.get_json(), partial=True)
    # get the movie from the db whose fields need to be updated
    stmt = db.select(Movie).filter_by(id=movie_id)
    movie = db.session.scalar(stmt)
    # if movie exists
    if movie:
        if str(movie.user_id) != get_jwt_identity():
            return {"error": "Only the owner can edit the movie"}, 403
        # update the fields
        movie.title = body_data.get('title') or movie.title
        movie.description = body_data.get('description') or movie.description
        movie.release = body_data.get('release') or movie.release
        movie.genre = body_data.get('genre') or movie.genre
        movie.viewing_platform = body_data.get('viewing_platform') or movie.viewing_platform
        
        # commit the changes
        db.session.commit()
        # return the updated movie back
        return movie_schema.dump(movie)
    # else
    else:
        # return error msg
        return {'error': f'Movie with id {movie_id} not found'}, 404
    

# This function has been replaced by the authorise_as_admin decorator
def is_user_admin():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin