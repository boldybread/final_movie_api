from datetime import date

from flask import Blueprint

from init import db, bcrypt
from models.user import User
from models.movie import Movie
from models.watchlist import Watchlist
from models.rating import Rating

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print("Tables created")

@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_tables():
    users = [
        User(
            name="admin",
            email="admin@email.com",
            password=bcrypt.generate_password_hash('123456').decode('utf-8'),
            is_admin=True
        ),
        User(
            name="Harry Grant",
            email="harrygrant@email.com",
            password=bcrypt.generate_password_hash('123456').decode('utf-8')
        ),
        User(
            name="Cam Munster",
            email="munstercameron@email.com",
            password=bcrypt.generate_password_hash('123456').decode('utf-8')
        ),
        User(
            name="Jahrome Hughes",
            email="jhughes@email.com",
            password=bcrypt.generate_password_hash('123456').decode('utf-8')
        )
    ]
    # A session represents the connection between an application and the relational database that stores its persistent objects
    # we add list of users to the session; use add_all for multiple users, add for singular
    db.session.add_all(users)

    movies = [
        Movie(
            title="The Accountant",
            description="As a math savant uncooks the books for a new client, the Treasury Department closes in on his activities, and the body count starts to rise.",
            release=2016,
            genre="Action",
            viewing_platform="Netflix"
        ),
        Movie(
            title="The Town",
            description="A proficient group of thieves rob a bank and hold an assistant manager hostage. Things begin to get complicated when one of the crew members falls in love",
            release=2010,
            genre="Action",
            viewing_platform="Prime"
        ),
        Movie(
            title="Deadpool",
            description="Deadpool is a 2016 American superhero film based on the Marvel Comics character of the same name.",
            release=2016,
            genre="Comedy",
            viewing_platform="Binge"
        ),
        Movie(
            title="Oppenheimer",
            description="Oppenheimer is a 2023 biographical war film centered around the life of J. Robert Oppenheimer",
            release=2023,
            genre="Drama",
            viewing_platform="Stan"
        ),
    ]

    db.session.add_all(movies)

    watchlists = [
        Watchlist(
            watchlist_title="Watchlist 1",
            user=users[0],
            movie=movies[0, 1]
        ),
        Watchlist(
            watchlist_title="My Watchlist",
            user=users[1],
            movie=movies[1, 2]
        ),
        Watchlist(
            watchlist_title="Munnies Movies",
            user=users[2],
            movie=movies[3]
        ),
        Watchlist(
            watchlist_title="Cool watchlist",
            user=users[3],
            movie=movies[1, 2, 3]
        )
    ]

    db.session.add_all(watchlists)

    ratings = [
        Rating(
            date=date.today(),
            user_rating=4,
            user=users[0],
            movie=movies[0]
        ),
        Rating(
            date=date.today(),
            user_rating=7,
            user=users[1],
            movie=movies[1]
        ),
        Rating(
            date=date.today(),
            user_rating=8,
            user=users[1],
            movie=movies[2]
        ),
        Rating(
            date=date.today(),
            user_rating=10,
            user=users[2],
            movie=movies[1]
        ),
        Rating(
            date=date.today(),
            user_rating=5,
            user=users[2],
            movie=movies[3]
        ),
        Rating(
            date=date.today(),
            user_rating=9,
            user=users[3],
            movie=movies[2]
        )
    ]

    db.session.add_all(ratings)

    db.session.commit()

    print("Tables seeded")