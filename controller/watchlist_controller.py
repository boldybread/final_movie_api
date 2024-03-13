from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.movie import Movie
from models.watchlist import Watchlist, watchlist_schema

watchlists_bp = Blueprint('watchlists', __name__, url_prefix="/<int:movie_id>/watchlists")
    
@watchlists_bp.route("/", methods=["POST"])
@jwt_required()
def create_watchlist(movie_id):
    body_data = request.get_json()
    stmt = db.select(Movie).filter_by(id=movie_id)
    movie = db.session.scalar(stmt)
    if movie:
        watchlist = Watchlist(
            watchlist_title = body_data.get('message'),
            user_id = get_jwt_identity(),
            movie = movie
        )
        db.session.add(watchlist)
        db.session.commit()
        return watchlist_schema.dump(watchlist), 201
    else:
        return {"error": f"Movie with id {movie_id} doesn't exist"}, 404
    
@watchlists_bp.route("/<int:watchlist_id>", methods=["DELETE"])
@jwt_required()
def delete_watchlist(movie_id, watchlist_id):
    stmt = db.select(Watchlist).filter_by(id=watchlist_id)
    watchlist = db.session.scalar(stmt)
    if watchlist and watchlist.movie.id == movie_id:
        db.session.delete(watchlist)
        db.session.commit()
        return {"message": f"Watchlist with id {watchlist_id} has been deleted"}
    else:
        return {"error": f"Watchlist with id {watchlist_id} not found in movie with id {movie_id}"}, 404
    
@watchlists_bp.route("/<int:watchlist_id>", methods=["PUT", "PATCH"])
@jwt_required()
def edit_watchlist(movie_id, watchlist_id):
    body_data = request.get_json()
    stmt = db.select(Watchlist).filter_by(id=watchlist_id, movie_id=movie_id)
    movie = db.session.scalar(stmt)
    if movie:
        movie.title = body_data.get('title') or movie.title
        db.session.commit()
        return watchlist_schema.dump(watchlist)
    else:
        return {"error": f"Watchlist with id {watchlist_id} not found in movie with id {movie_id}"}