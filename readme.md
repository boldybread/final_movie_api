# Movie_API README

## SETUP

To run from local machine:

- Create a postgresql database:

```py
CREATE DATABASE movie_db;
```

- Create a new postgresql user and give permissions from within Postgre interface:

```py
- CREATE ROLE movie_dev && GRANT ALL ON movie_db TO movie_dev;
```

- Edit ".env" file so "SQL_DATABASE_URI" matches user and database details:

```py
DATABASE_URI="postgresql+psycopg2://movie_dev:123456@localhost:5432/movie_db"
JWT_SECRET_KEY="secret"
```

- Start & activate virtual environment:

```py
python3 -m venv venv && source .venv/bin/activate
```

- Install requirements:

```py
pip3 install -r requirements.txt
```

- Create/seed tables:

```py
python3 -m flask db drop && python3 -m flask db create && python3 -m flask db seed
```

- Run flask app:

```py
python3 -m flask run
```

## Identification of the problem you are trying to solve by building this particular app

I wanted to create an app that could store movies to a watchlist for a user to watch as well as post their ratings of those movies. I like using watchlists on the streaming services I subscribe to, but would like to have a watchlist that wasn't restricted to the one platform, and could not only store the movies that I wanted to watch, but also tell me what platform they are available to be viewed.

## Why is it a problem that needs solving

While many streaming services have a watchlist for their particular app I wanted to make one that wasn't limited to just one streaming service but one where a user could add movies from any app to their watchlist and then rate them accordingly after watching them.

## Why have you chosen this database system. What are the drawbacks compared to others?

When choosing a database for my Movie API I looked at the advantages and disadvantages of various databases, eventually choosing PostgreSQL for the following reasons.

- It is extensible, allowing a developer to come up with functions, data types, languages, all manner of different changes easily installed by creating that extension and it will do everything else for you.

- Full ACID compliance providing reliable and robust transations able to support high concurrent loads. Without transactions much extra code would be required for all the error handling, thankfully PostgreSQL provides transactions. When you make a change to a table it will make that change immeidately which is really important for complex relational applicationswhere it is typical to make changes at the same time as making changes to underlining database schema.

- Postgres also benefits from many adjustable parameters, many other databases only allow you to set enviromental parameters at the whole database level. Postgres  enables developers to make easy changes where they need to. For instance you could set parameters for a single session or even just a single transaction and function.

- Postgres also offers a robust security that has some international recognition, as well as the aforementioned extensions to further increase security if required. The app is secured on the basis of user privileges or rather than granting permission to a specific user you can also create permission on something to be able to have it ongoing.

Ultimately I decided PostgreSQL would be the best choice for my movie API based on these features and advantages offering the ability to handle complex data operations with high accuracy and security.

## Identify and discuss the key functionalities and benefits of an ORM

Object relational mapping or ORM is a technique used to bridge relational databases and object orientated programs. When using object orientated programming (OOP) languages to interact with a database you will perfrom different operations like creating, reading, updating and deleting (CRUD) data from a database.

Benefits of using an ORM include simplified access to a database which is intuitive and easier to understand. Developers are able to interact with the database using objects and methods rather that writing raw SQL queries. These interactions are simplified by allowing a developer to write in their preferred programming language rather than in SQL. ORM frameworks can also automatically create tables again reducing the SQL code required. This structured approach makes the database easy to maintain.

The ability to map database tables and their relationsips to object classes and their relationships makes it easier to focus on the domain model rather than the database schema. Due to the level of abstraction between database and application when using ORM frameworks it is easier to switch to different databases or use multiple databases simultaneously without having to change application code.

## Document all endpoints for your API

## POST /auth/register

### This is to register a new user

name - string containing the username of new user

email - string containing the email of new user

- must be unique and not null
- else returns error

password - string containing password for new user

- mustn't be null
- returns error is null violation

is_admin - boolean containing admin status

- is false by default

Integrity errors will catch any null or unique email address violations.

## POST /auth/login

### This is to login a preexisting user

name - string containing username or user

password - string containing user's password

- if successful a JWT is created and returned along with name and admin status
- if unsuccessful 401 error returned

## POST /movies

### Creates a new movie

title - string containing movie title

description - text containing movie description

release - integer containing year of movie release

- 4 digit limit

genre - string containing genre of movie

- only valid responses allowed
- else error returned

viewing_platform - string containing genre of movie

- only valid responses allowed
- else error returned

## POST /rating

### Creates a new rating

date - datetime when rating was created

user_rating - integer rating score for watched movie

- must be valid response between 1 and 10 else error returned

movie_id - integer foreign key obtained from movie table

user_id - integer foreign key obtained from users table

## POST /watchlist

### Creates a new watchlist for a user

watchlist_title - string containing name of watchlist

user_id - integer foreign key from users table

movie - checks if movie exists:

- if exists, retrieves data from movie table

- else returns error 404

## GET /movies

### Retrieves all movies from Table movie

Checks for movies in movie table:

- If successful a list of all movies is displayed.

- If unsuccessful an error message is displayed.

## GET /movies/4

### Retrieves select movie from Table movie with corresponding movie_id

movie_id - Integer ID of the movie to retrieve. If not provided, all movies will be retrieved.

- If successful retrieve movie where movie_id = 4

- If unsuccessful a 404 error message is displayed.

## GET /rating

### Retrieves all ratings from rating table

Checks for ratings in rating table:

- If successful a list of all movies is displayed in order of release.

- If unsuccessful a 404 error message is displayed.

## GET /rating/4

### Retrieves all ratings from Table rating

rating_id - Integer ID of the rating to retrieve. If not provided, all movies will be retrieved.

- If successful, retrieve rating where rating_id = 4

- If unsuccessful a 404 error message is displayed.

## DELETE /movies/6

### Deletes an instance of a movie with corresponding movie_id

check user's admin status

- If they are an admin, check if movie exists

    - if movie exists then delete movie successfully

    - if movie does not exist then return error 404 not found

- If they are not an admin

    - return error 403 not authorised

## DELETE /rating/6

### Deletes an instance of a rating with corresponding rating_id

check user's admin status

- If they are an admin, check if rating exists

    - if rating exists then delete rating successfully

    - if rating does not exist then return error 404 not found

- If they are not an admin

    - return error 403 not authorised

## DELETE /watchlist/6

### Deletes an instance of a watchlist with corresponding watchlist_id

check user's admin status

- If they are an admin, check if watchlist exists

    - if watchlist exists then delete watchlist successfully

    - if watchlist does not exist then return error 404 not found

- If they are not an admin

    - return error 403 not authorised

## PUT PATCH /movies/5

### Modifies all or some existing data in movie table

Get the data to be updated from the body of the request and get the movie from the db whose fields need to be updated

- If movie does not exist return error 404

- If movie exists, check user

    - if not correct user return error 403

    - else update the fields:

title - string containing movie title

description - text containing movie description

release - integer containing year of movie release

- 4 digit limit

genre - string containing genre of movie

- only valid responses allowed
- else error returned

viewing_platform - string containing genre of movie

- only valid responses allowed
- else error returned

## PUT PATCH /rating/5

### Modifies all or some existing data in rating table

Get the data to be updated from the body of the request and get the rating from the db whose fields need to be updated

- If rating does not exist return error 404

- If rating exists, check user:

    - if not correct user return error 403 unauthorised user

    - if correct user, update the fields:

date - Datetime indicating when the rating was added

user_rating - Integer between 1 and 10 indicating user's rating of movie watched

- If user_rating not between 1 and 10 validation error returned

## PUT PATCH /watchlist/5

### Modifies all or some existing data in watchlist table

Get the data to be updated from the body of the request and get the rating from the db whose fields need to be updated

- If watchlist does not exist return error 404

- If watchlist exists, check user:

    - if not correct user return error 403 unauthorised user

    - if correct user, update the fields:

watchlist_title - String containing watchlist title

movie_id - Integer containing the movie id to be added to the watchlist

- Must exist else return 404 error

## Error Handling for Endpoints

### Error handling was used for some endpoints

Some examples of error handling code from main.py lines 25-36:

```py
    @app.errorhandler(400)
    def bad_request(err):
        return {"error": str(err)}, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {"error": str(err)}, 404

    @app.errorhandler(ValidationError)
    def validation_error(error):
        return {"error": error.messages}, 400
```

The following error code is from movie_controller.py lines 122-124 and returns an error if a movie cannot be found matching the supplied movie_id:

```py
    else:
        return {'error': f'Movie with id {movie_id} not found'}, 404
```

The following error code is from auth_controller.py lines 37-42 and returns an error if a user's info is not null or not unique where required to be:

```py
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name} is required"}
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use"}, 409
```

## An ERD for Movie API

![ERD](images\Mov_ERD.jpg "ERD")

### User Model

#### Table Name

- users

#### Attributes

- user_id = Integer & Primary Key

- name = String

- email = String, unique & not null

- password = String, not null

- is_admin = Boolean, default is false

#### Associations

- One-to-Many with Rating: A user can have multiple ratings on different movies.

- One-to-One with Watchlist: A user can have one watchlist.

### Rating Model

#### Table Name

- rating

#### Attributes

- rating_id = Integer & Primary Key

- movie_id = Integer, Foreign Key & not null

- user_id = Integer, Foreign Key & not null

- date = date (date the rating was added)

- user_rating = Integer

#### Associations

- Many-to-One with User: Multiple ratings can exist per user.

- Many-to-One with Movie: Multiple ratings can exist for each movie.

### Watchlist Model

#### Table Name

- watchlist

#### Attributes

- watchlist_id = Integer & Primary Key

- watchlist_title = String, 20 character limit

- movie_id = Integer, Foreign Key & not null

- user_id = Integer, Foreign Key & not null

#### Associations

- Many-to-Many with Movie: Many watchlists can exist with multiple movies listed.

- One-to-One with User: One watchlist can exist to one user.

### Movie Model

#### Table Name

- movie

#### Attributes

- movie_id = Integer & primary_key

- title = String, character limit 60

- description = Text

- release = String, character limit 4

- genre = String, 5 valid genres accepted

- viewing_platform = String, 4 valid platforms accepted

#### Associations

- Many-to-Many with Watchlist: Many movies can exist within multiple watchlists.

- One-to-Many with Rating: A movie can have many ratings.

## Detail any third party services that your app will use

### SQLAlchemy

SQLAlchemy is a Python SQL toolkit and object relational mapper to enable developers extra flexibility when creating an application without the need to rely on writing lots of raw SQL code. It is designed for efficient and high performing database access.

### Marshmallow

Marshmallow is an ORM framework library built for converting more complex datatypes such as objects to and from native Python datatypes.

### Bcrypt

Bcrypt is a password hashing function designed to allow developers the quick and easy ability to quickly hash a password for their software and servers.

### JWTManager

JWTManager is an object used to hold JSON Web Token (JWT) settings and callback functions for Flask. It offers basic JWT features to the developers application.

### Flask

Flask is a Python web micro framework that provides tools, libraries, and technologies for building web applications offering a simple yet powerful API that allows developers to  quickly and effienctly create web applications. Flask is used to build the API for this application.

### Psycopg2

Psycopg2 is a popular PostgreSQL adapter for Python providing a user friendly interface for developers to interact with PostgreSQL databases. Psycopg2 is used to connect to the PostgreSQL database for this application.

## Describe your projects models in terms of the relationships they have with each other

### User Model

User model represents a user in the system. User model has a direct relationship with watchlist and rating models providing them both with user_id as a Foreign Key. If user instance is deleted it will delete the corresponding rating and watchlist information.

```py
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
```

### Rating Model

Rating Model represents ratings created by a user to rate any movies that they have watched. Rating Model has a direct relationship with User and Movie models containing a foreign key from each. If a movie is deleted, all of its associated ratings will be deleted as well.

```py
    rating_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    user_rating = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    user = db.relationship('User', back_populates='rating')
    movie = db.relationship('Movie', back_populates='rating', cascade='all, delete')

```

### Watchlist Model

The watchlist model represents the watchlist that a user creates to store his/her movies that they are interested in watching. Watchlist model has a direct relationship with User and Movie model using both of their Primary Keys as Foreign Keys.

```py
    id = db.Column(db.Integer, primary_key=True)
    watchlist_title = db.Column(db.String(20))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)

    user = db.relationship('User', back_populates='watchlist')
    movie = db.relationship('Movie', back_populates='watchlist')
```

### Movie Model

Movie Model represents the movies that are stored in the database. It has a direct relationship with rating and watchlist model using its Primary Key "movie_id" as a Foreign Key for them both.

```py
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True)
    description = db.Column(db.Text)
    release = db.Column(db.String(4))
    genre = db.Column(db.String)
    viewing_platform = db.Column(db.String)

    rating = db.relationship('Rating', back_populates='movie')
    watchlist = db.relationship('Watchlist', back_populates='movie')
```

## Discuss the database relations to be implemented in your application

In my application I have implemented a PostgreSQL database using SQLAlchemy ORM. The movie DB contains four tables, users, rating, watchlist and movie which function together to allow a user to assign stored movies to a watchlist that they want to watch, and rate movies that they have already watched. Users table stores user information such as name, email and password. The password is hashed with bcrypt and authenticates a user with the correct password. The users profile also holds whether they are an admin user or not and allows additional privileges if they are.

Rating table holds user's ratings, Watchlist table stores user's watchlists and movie table stores a list of movies in the database. Rating and Watchlist table both contain 2 foreign keys one referencing users table and one referencing movie table.  

## Describe the way tasks are allocated and tracked in your project

I utilised Trello for project management where I created 4 lists:

- Project Resources

- To do

- Pending

- Done

![Trello Project Overview](images\api_project.jpg "Trello Project Overview")

### Project Resources

Within Project Resources I created a project plan as well as label definitions to help provide understanding to the labelling convention I used.

![Trello Project Overview](images\api_project_labels.jpg "Trello Project Overview")

### To do

All tasks to be completed began in the to do list, this allowed me to have an oversight of my current and upcoming workload so I was better able to manage my time and plan what I would work on next and where my prioirities and time constraints were.

![Trello Project Overview](images\api_project_readme_task.jpg "Trello Project Overview")

### Pending

Once tasks were started they were moved to the pending list. Here I could manage exactly what was in progress and look more specifically at the sub tasks involved with completing that particular overall task. I used a checklist to tick off individual sub tasks. Once all sub tasks were ticked off and I was satisfied that the task was complete it was moved from pending to the Done list.

### Done

This list was utilised for any tasks deemed completed. By the end of the project all tasks were in here signifying completion of the project. I made sure tasks weren't moved from pending to done list until all checkmarks had been ticked off and I was satisfied that I has reviewed the task and it was error free.